#!/usr/bin/env python
# coding: utf-8

# # Resizing and resampling a mock image for Fourier content
# 
# This document is designed to explore the signal processing considerations involved in taking a mock image like the ALMA logo, pasting it on the sky, and generating mock visiblility samples from it.

# In[1]:


get_ipython().run_line_magic('matplotlib', 'notebook')
import numpy as np
import matplotlib
import matplotlib.pyplot as plt 
from scipy.signal import windows
from astropy.io import fits
from astropy import wcs

arcsec = np.pi / (180.0 * 3600)  # [radians]  = 1/206265 radian/arcsec

image_raw = plt.imread("alma-logo-white-outline.png")
print("shape", image_raw.shape)
# (M, N, 4) for RGBA images.
# (703, 498, 4)
ny, nx, nchan = image_raw.shape

image_raw = image_raw[
    :, :, 0
]  # loose the last color dimension. Since it's white, it doesn't matter which channel we take.


# For reference, here is the image itself

# In[2]:


fig,ax = plt.subplots(nrows=1, figsize=(3,3))
ax.imshow(image_raw, origin="lower", interpolation="none")


# Since we'll be using the FFT, and it assumes a circular image, our first step is to pad the image with zeros to make the edges consistent with each other. We'll also take this opportunity to make it a square image and flip it to conform to our $l,m$ and $u,v$ conventions, since we'll be using the FFT. These are that East ($l$) and North ($m$) *increase* with array index. 

# In[3]:


# do the padding
# ncol > nrow
# pad top and bottom to make square
N = 800
x0 = (N - nx) // 2
x1 = x0 + nx
y0 = (N - ny) // 2
y1 = y0 + ny
# now pad into a 256 x 256 array
image_pad = np.zeros((N, N), dtype=np.float64)
image_pad[y0:y1, x0:x1] = image_raw

# flip the image to be N/S
# AND
# flip image to be E/W
# l,m are increasing with array index. l corresponds to east.
image_stock = np.fliplr(np.flipud(image_pad))


# To plot this image up so that it looks normal, we need to use `origin="lower"` and flip LR. 

# In[4]:


fig,ax = plt.subplots(nrows=1, figsize=(3,3))
ax.imshow(np.fliplr(image_stock), origin="lower", interpolation="none")


# ## Some thoughts on the information content of this image
# 
# This "stock" image contains 800x800 pixels. The next step of the image generation process will be to assign a `cell_size` to each pixel, essentially specifying how big the image will appear on sky. Since we're working with ALMA to study protoplanetary disks, we will say that this image corresponds to a diameter of 4 arcseconds, meaning that

# In[5]:


cell_size = 4.0 / N 
print("cell_size is {:.4f} arcseconds".format(cell_size))


# The array configuration and observing frequency specify a maxmimum spatial frequency that we sample in our measurement set. This defines the "minimum recoverable image scale" that is probed by our dataset. Now, of course, if we wanted to make prior assumptions then we could go further, but let's just for a moment consider the case where we have perfect (noiseless) Nyquist sampling. 

# The Nyquist frequency is 
# 
# $$
# u = \frac{1}{2 \times \mathrm{cell\_size}}
# $$
# 
# or 

# In[6]:


max_spatial_freq = 1e-6 / (2 * cell_size * arcsec) 
print("max_spatial_freq {:.3f} Mlambda".format(max_spatial_freq))


# So that means that, with its current `cell_size` and `npix`, there is information in this image that won't be sampled by ALMA. On one hand, that's OK, and we probably do want to include an image that has a lot of extra high spatial frequencies.
# 
# On the other hand, however, we probably also want an image that has max spatial frequencies closer to what ALMA can actually sample. What is the maximum spatial frequency probed by 16 km baselines at 1.3mm? 

# In[7]:


max_baseline_Ml = 1e-6 * 16 / (1.3e-6) # [kl]
print("max ALMA spatial freq at 1.3mm is {:.3f} Mlambda".format(max_baseline_Ml))


# To help us calculate the maximum spatial frequency included in a certain sized image, let's make a function

# In[8]:


def get_max_spatial_freq(npix, diameter=4):
    cell_size = diameter / npix # arcsec
    return 1e-6 / (2 * cell_size * arcsec)  # Mlambda


# In[9]:


fig,ax = plt.subplots(nrows=1, figsize=(3,3))
npixs = np.array([256,512,1024])
ax.plot(npixs, get_max_spatial_freq(npixs))
ax.axhline(max_baseline_Ml, color="0.3")
ax.set_xlabel("npix")
ax.set_ylabel("max $u$ [M$\lambda$]")
fig.subplots_adjust(left=0.2,bottom=0.2)


# So this plot tells us that a 512x512 image spanning 4 arcseconds in diameter is a nice image size providing a maximal amount of information content that could be measured by ALMA in its longest baseline configuration at Band 6. 

# # Rescaling and Resampling an Image to a lower resolution
# 
# Say we'd like to take our 800x800 image and rescale it to a 512x512 image. What's the right thing to do to? [Wikipedia](https://en.wikipedia.org/wiki/Image_scaling) actually has a few helpful notes about upscaling. There's also the idea about low-pass filtering. I think really what we want to do is [low-pass filter](https://en.wikipedia.org/wiki/Low-pass_filter) and resample. This is very much looking at what the response is going to be like in the Fourier domain vs image domain. An "ideal" low pass filter has the nasty Sinc effect. We want something that has better sidelobes. First, let's take a look at what the FFT looks like (amplitude only).

# In[10]:


fft_stock = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(image_stock)))
amp_stock = np.abs(fft_stock)


# In[11]:


fig, ax = plt.subplots(nrows=1, figsize=(3,3))
norm = matplotlib.colors.LogNorm(np.min(amp_stock), np.max(amp_stock))
ax.imshow(amp_stock, interpolation="none", origin="lower", norm=norm)


# In[38]:


def create_window(window_function, npix_start, npix_end):
    assert npix_start > npix_end, "must downscale image"
    npad = npix_start - npix_end
    assert npad % 2 == 0, "must have even numbers of start and end pixels"
    w_middle = window_function(npix_end, False) # we want the max to be at the x = 0 pixel
    w_stub = np.zeros(npad//2)
    return np.concatenate([w_stub, w_middle, w_stub])

def truncate_array(array, npix_start, npix_end):
    npad = npix_start - npix_end
    ntrunc = npad // 2
    return array[ntrunc:-ntrunc,ntrunc:-ntrunc]


# In[13]:


def create_apodizer(window_function, npix_start, npix_end):
    '''
    Make an image
    '''
    one_D = create_window(window_function, npix_start, npix_end)
    return np.outer(one_D, one_D)


# In[14]:


apod_blackman = create_apodizer(windows.blackmanharris, 800, 512)
apod_boxcar = create_apodizer(windows.boxcar, 800, 512)


# In[15]:


fig, ax = plt.subplots(nrows=1,figsize=(3,3))
ax.imshow(apod_boxcar, origin="lower", interpolation="none")


# In[16]:


fft_boxcar = fft_stock * apod_boxcar
image_boxcar = np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(fft_boxcar)))


# In[17]:


fig, ax = plt.subplots(nrows=1, figsize=(3,3))
ax.imshow(np.fliplr(np.real(image_boxcar)), interpolation="none", origin="lower")


# In[39]:


fft_blackman = fft_stock * apod_blackman
fft_blackman_trunc = truncate_array(fft_blackman, 800, 512)
image_blackman = np.fft.fftshift(np.fft.ifft2(np.fft.fftshift(fft_blackman_trunc)))


# In[40]:


fig, ax = plt.subplots(ncols=2, figsize=(6,3))
ax[0].imshow(np.fliplr(np.real(image_blackman)), interpolation="none", origin="lower")
ax[1].imshow(np.fliplr(np.imag(image_blackman)), interpolation="none", origin="lower")


# So the answer is clearly that apodization is very important! But, these images still have 800 x 800 pixels, what happens if we drop things down to 512x512. How would we do this? My first thought is to just get rid of the extra space in the Fourier Plane, this is equivalent to "unpadding" with zeros.

# In[41]:


amp_blackman = np.abs(fft_blackman)
fig, ax = plt.subplots(nrows=1, figsize=(3,3))
norm = matplotlib.colors.LogNorm(vmin=0.01, vmax=np.max(amp_blackman))
ax.imshow(amp_blackman, interpolation="none", origin="lower", norm=norm)


# In[42]:


# write the FITS file
# create the FITS file
w = wcs.WCS(naxis=2)

w.wcs.crpix = np.array([1, 1])
w.wcs.cdelt = np.array([-cell_size, cell_size]) * arcsec * 180.0 / np.pi  # decimal degrees
w.wcs.ctype = ["RA---TAN", "DEC--TAN"]

header = w.to_header()

# add in the kwargs to the header
# if header_kwargs is not None:
#     for k, v in header_kwargs.items():
#         header[k] = v
# hdu = fits.PrimaryHDU(self.cube.detach().cpu().numpy(), header=header)

hdu = fits.PrimaryHDU(np.fliplr(np.real(image_blackman)), header=header)
hdul = fits.HDUList([hdu])
hdul.writeto("logo_cont.fits", overwrite=True)
hdul.close()


# In[ ]:





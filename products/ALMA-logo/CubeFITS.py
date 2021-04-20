#!/usr/bin/env python
# coding: utf-8

# # Image Cube
# 
# Use the ALMA logo to scale and rotate and make an image cube. Basically, we're going to add an extra dimension to the cube and rotate it a little. We can't rotate very far because there isn't much blank buffer, but enough to get the idea.

# In[62]:


from scipy.interpolate import interp1d
from scipy.ndimage import rotate
from astropy.io import fits 
import astropy.wcs
import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
from astropy.coordinates import SkyCoord


# In[63]:


hdul = fits.open("logo_cont.fits")
header = hdul[0].header 
img_data = hdul[0].data


# In[64]:


header


# In[65]:


# set a direction 
indirection = "04h55m10.98834s +030d21m58.879285s"
c = SkyCoord(indirection, unit=(u.hourangle, u.deg))

header["CRVAL1"] = c.ra.deg
header["CRVAL2"] = c.dec.deg


# ## Cube parameters 

# In[67]:


nchan = 9
rot_total = 10.0 # degrees
drot_dchan = rot_total / (nchan - 1)
rots = drot_dchan * np.arange(nchan) - rot_total//2


# In[68]:


brightness = 1 - 0.15 * np.abs(rots)

plt.plot(rots, brightness)
plt.show()


# In[69]:


# update the header with 12CO HD163296
header.insert(5, ("NAXIS3", nchan))
header.insert(9, ("CRPIX3", 1.000000000000E+00))
header.insert(12, ("CDELT3", 1.537983987427E+05))
header.insert(15, ("CUNIT3", "Hz"))
header.insert(18, ("CTYPE3", "FREQ"))
header.insert(21, ("CRVAL3", 2.305239582062E+11))
header["RESTFRQ"] = 2.305380000000E+11
header["SPECSYS"] = "LSRK"
header["VELREF"] = 257
header["NAXIS"] = 3


# In[71]:


header = astropy.wcs.WCS(header).to_header()


# In[72]:


img_cube = np.empty((nchan, *img_data.shape), dtype=np.float64)


# In[73]:


for i in range(nchan):
    img_cube[i] = 5e-5 * brightness[i] * rotate(img_data, rots[i], reshape=False, prefilter=False, order=1)


# In[75]:


print("total flux {:} Jy".format(np.sum(img_cube)))


# In[77]:


hdu = fits.PrimaryHDU(img_cube, header=header)
hdul = fits.HDUList([hdu])
hdul.writeto("logo_cube.fits", overwrite=True)
hdul.close()


# In[ ]:





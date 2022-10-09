from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from mpol import gridding, coordinates


def plot_dataset(fname):

    # load extracted visibilities from npz file
    dnpz = np.load(fname)
    uu = dnpz["uu"]
    vv = dnpz["vv"]
    weight = dnpz["weight"]
    data = dnpz["data"]

    # creating Gridder object
    coords = coordinates.GridCoords(cell_size=0.003, npix=512)
    gridder = gridding.Gridder(
        coords=coords,
        uu=uu,
        vv=vv,
        weight=weight,
        data_re=data.real,  # separating the real and imaginary values of our data
        data_im=data.imag,
    )

    img, beam = gridder.get_dirty_image(
        weighting="briggs",
        robust=0.0,
        unit="Jy/arcsec^2",
    )

    kw = {"origin": "lower", "extent": gridder.coords.img_ext}
    fig, ax = plt.subplots(ncols=1)
    im = ax.imshow(np.squeeze(img), **kw)
    plt.colorbar(im)
    ax.set_xlabel(r"$\Delta \alpha \cos \delta$ [${}^{\prime\prime}$]")
    ax.set_ylabel(r"$\Delta \delta$ [${}^{\prime\prime}$]")
    plt.xlim(left=0.75, right=-0.75)
    plt.ylim(bottom=-0.75, top=0.75)
    fig.savefig("{:}.png".format(fname))


plot_dataset("HD143006_continuum.npz")
plot_dataset("HD143006_continuum_trimmed.npz")
plot_dataset("HD143006_continuum_trimmed_single.npz")

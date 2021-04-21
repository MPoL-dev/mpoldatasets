from astropy.io import fits
import numpy as np
import casatasks

import os
import shutil


def get_extent(header):
    # get the coordinate labels
    nx = header["NAXIS1"]
    ny = header["NAXIS2"]

    assert (
        nx % 2 == 0 and ny % 2 == 0
    ), "We don't have an even number of pixels, assumptions in the routine are violated."

    # RA coordinates
    CDELT1 = 3600 * header["CDELT1"]  # arcsec (converted from decimal deg)
    # DEC coordinates
    CDELT2 = 3600 * header["CDELT2"]  # arcsec

    RA = (np.arange(nx) - nx / 2) * CDELT1  # [arcsec]
    DEC = (np.arange(ny) - ny / 2) * CDELT2  # [arcsec]

    # extent needs to include extra half-pixels.
    # RA, DEC are pixel centers

    ext = (
        RA[0] - CDELT1 / 2,
        RA[-1] + CDELT1 / 2,
        DEC[0] - CDELT2 / 2,
        DEC[-1] + CDELT2 / 2,
    )  # [arcsec]

    return RA, DEC, ext


def truncate_data(data, RA, DEC, radius):
    # truncate to radius
    npix = len(RA)
    CDELT = DEC[1] - DEC[0]

    # Midpoints
    i_mid = int(npix / 2)
    il = i_mid - int(round(radius / CDELT))
    ir = i_mid + int(round(radius / CDELT))

    data = data[:, il:ir, il:ir]
    RA = RA[il:ir]
    DEC = DEC[il:ir]
    ext = (RA[0], RA[-1], DEC[0], DEC[-1])

    return data, RA, DEC, ext


def get_beam(hdul, header):
    if header.get("CASAMBM") is not None:
        # Get the beam info from average of record array
        data2 = hdul[1].data
        BMAJ = np.median(data2["BMAJ"])
        BMIN = np.median(data2["BMIN"])
        BPA = np.median(data2["BPA"])
    else:
        # Get the beam info from the header, like normal
        BMAJ = 3600 * header["BMAJ"]
        BMIN = 3600 * header["BMIN"]
        BPA = header["BPA"]

    return BMAJ, BMIN, BPA


def load_image(fits_name, channel=0, beam=False):
    hdu_list = fits.open(fits_name)
    hdu = hdu_list[0]
    if len(hdu.data.shape) == 3:
        data = hdu.data[channel]  # first channel
    elif len(hdu.data.shape) == 2:
        data = hdu.data
    header = hdu.header

    RA, DEC, ext = get_extent(hdu.header)

    if beam:
        return data, RA, DEC, ext, get_beam(hdu_list, header)
    else:
        return data, RA, DEC, ext


def get_vels_from_freqs(header):

    assert header["CTYPE3"] == "FREQ", "Image cube not stored as frequency"

    restfreq = header["RESTFRQ"]  # [Hz]
    freqs = header["CRVAL3"] + np.arange(header["NAXIS3"]) * header["CDELT3"]  # [Hz]

    vels = beam_utils.constants.c_kms * (restfreq - freqs) / restfreq

    return vels


def load_cube(fits_name, beam=False):
    """
    Args:
        fits_name: FITS file to load
        restfreq: in GHz
    """
    hdu_list = fits.open(fits_name)
    hdu = hdu_list[0]
    data = hdu.data  # assuming (nchan, npix, npix)
    header = hdu.header

    assert header["NAXIS"] == 3, "Image cube has dimensions other than 3"

    RA, DEC, ext = get_extent(hdu.header)

    if header["CTYPE3"] == "FREQ":
        vels = get_vels_from_freqs(header)

        # do we need to reverse the data?
        if vels[1] < vels[0]:
            data = data[::-1]
            vels = vels[::-1]

    elif header["CTYPE3"] == "VELO-LSR":
        if header["CUNIT3"] == "M/S":
            vels = 1e-3 * (
                header["CRVAL3"] + np.arange(header["NAXIS3"]) * header["CDELT3"]
            )  # [km/s]
    else:
        raise NotImplementedError("Implement velocity kwd.")

    if beam:
        beam = get_beam(hdu_list, header)

    return data, RA, DEC, ext, vels, beam


def get_rms(dirty_image_path, mask_path):
    # Estimate the RMS of the un-masked pixels of the dirty image
    rms = casatasks.imstat(
        imagename=dirty_image_path, mask='"{}" < 1.0'.format(mask_path)
    )["rms"][0]

    return rms


def clear_extensions(imname):
    for ext in [
        ".image",
        ".mask",
        ".model",
        ".pb",
        ".psf",
        ".residual",
        ".sumwt",
        ".image.pbcor",
    ]:
        fname = imname + ext
        if os.path.exists(fname):
            shutil.rmtree(fname)


def exportfits(infile, outfile):
    if os.path.exists(outfile):
        os.remove(outfile)

    casatasks.exportfits(infile, outfile, dropdeg=True, dropstokes=True)

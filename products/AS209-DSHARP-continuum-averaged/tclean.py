# reproduce the DSHARP image using casa6
import casatasks
import mpoldatasets.image
import time

""" Define simple masks and clean scales for imaging """
mask_pa = 86  # position angle of mask in degrees
mask_maj = 1.3  # semimajor axis of mask in arcsec
mask_min = 1.1  # semiminor axis of mask in arcsec
mask_ra = "16h49m15.29s"
mask_dec = "-14.22.09.04"

common_mask = "ellipse[[%s, %s], [%.1farcsec, %.1farcsec], %.1fdeg]" % (
    mask_ra,
    mask_dec,
    mask_maj,
    mask_min,
    mask_pa,
)

imagename = "AS209"

vis = "AS209_continuum.ms"
imagename = "AS209_tclean"
mpoldatasets.image.clear_extensions(imagename)

casatasks.delmod(vis=vis)

tic = time.perf_counter()

casatasks.tclean(
    vis=vis,
    imagename=imagename,
    specmode="mfs",
    deconvolver="multiscale",
    scales=[0, 5, 30, 100, 200],
    weighting="briggs",
    robust=-0.5,
    gain=0.2,
    imsize=3000,
    cell=".003arcsec",
    niter=50000,
    threshold="0.08mJy",
    cycleniter=300,
    cyclefactor=1,
    uvtaper=[".037arcsec", ".01arcsec", "162deg"],
    mask=common_mask,
    nterms=1,
    savemodel="modelcolumn",
)

toc = time.perf_counter()
print("tclean elapsed time {:}s".format(toc - tic))

mpoldatasets.image.exportfits(imagename + ".image", imagename + ".fits")

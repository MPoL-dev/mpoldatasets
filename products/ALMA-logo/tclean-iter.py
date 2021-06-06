import mpoldatasets.image
import time
import casatasks

ms_path = "logo_cube.noise.ms"

imname = "logo_cube.tclean"
mpoldatasets.image.clear_extensions(imname)

imsize = 512

tic = time.perf_counter()

# produce a dirty image
casatasks.tclean(
    vis=ms_path,
    imagename=imname,
    specmode="cube",
    weighting="briggs",
    deconvolver="multiscale",
    scales=[0, 5, 30, 75],
    robust=1.5,
    imsize=800,
    cell="0.007arcsec",
    niter=10000,
    threshold="0.5mJy",
    interactive=False,
    perchanweightdensity=False,
    restoringbeam="common",
    savemodel="modelcolumn",
)

toc = time.perf_counter()
print("tclean elapsed time {:}s".format(toc - tic))

# produce a cleaned image
mpoldatasets.image.exportfits(imname + ".image", imname + ".fits")
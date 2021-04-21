import mpoldatasets.image

import casatasks

ms_path = "logo_cube.noise.ms"

imname = "logo_cube.dirty"
mpoldatasets.image.clear_extensions(imname)

imsize = 512

# produce a dirty image
casatasks.tclean(
    vis=ms_path,
    imagename=imname,
    specmode="cube",
    weighting="briggs",
    robust=0.5,
    imsize=800,
    cell="0.007arcsec",
    niter=0,
    interactive=False,
    perchanweightdensity=False,
    restoringbeam="common",
)

# produce a cleaned image
mpoldatasets.image.exportfits(imname + ".image", imname + ".fits")
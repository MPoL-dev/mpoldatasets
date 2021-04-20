import beam_utils
import beam_utils.image

import casatasks

ms_path = "sim.alma.cycle7.7.noisy.ms"

imname = "cube"
beam_utils.image.clear_extensions(imname)

imsize = 512

# produce a dirty image
casatasks.tclean(
    vis=ms_path,
    imagename=imname,
    specmode="cube",
    weighting="briggs",
    robust=0.5,
    imsize=800,
    cell="0.005arcsec",
    niter=0,
    interactive=False,
    perchanweightdensity=False,
    restoringbeam="common",
)

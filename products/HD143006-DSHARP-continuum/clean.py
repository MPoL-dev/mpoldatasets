# reproduce the DSHARP image using casa6
import casatasks 
import beam_utils
import beam_utils.image

mask_ra  = '15h58m36.9s'
mask_dec = '-22.57.15.60'
mask_rad = 0.7
common_mask = 'circle[[%s, %s], %.1farcsec]' % (mask_ra, mask_dec, mask_rad)

vis = "HD143006_continuum.ms"
imagename = "HD143006"
beam_utils.image.clear_extensions(imagename)

casatasks.tclean(vis= vis, 
    imagename = imagename, 
    specmode = 'mfs', 
    deconvolver = 'multiscale',
    scales = [0, 5, 30, 75], 
    weighting='briggs', 
    robust = 0.0,
    gain = 0.3,
    imsize = 3000,
    cell = '.003arcsec', 
    niter = 50000,
    threshold = "0.05mJy",    
    cycleniter = 300,
    cyclefactor = 1, 
    uvtaper = ['.042arcsec', '.020arcsec', '172.1deg'], 
    mask = common_mask,
    nterms = 1)

beam_utils.image.exportfits(imagename + '.image', imagename + '.fits')
import casatasks

# Generate an mock measurement set of the spectral cube

fits_path = "logo_cube.fits"

casatasks.simobserve(
    skymodel=fits_path,
    hourangle="transit",
    totaltime="3600s",
    graphics="none",
    thermalnoise="tsys-atm",
    overwrite=True,
    obsmode="int",  # interferometer
    antennalist="alma.cycle7.7.cfg",
)

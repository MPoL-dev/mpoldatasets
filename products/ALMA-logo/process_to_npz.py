from visread import examine
import numpy as np

fname = "logo_cube.noise.ms"

# only one spw
spw = 0

# calculate rescale factor and replot
sigma_rescale = examine.get_sigma_rescale_datadescid(fname, spw)

# get processed visibilities
# including complex conjugation
d = examine.get_processed_visibilities(fname, spw, sigma_rescale=sigma_rescale)

flag = d["flag"]

# assert no flags
assert (
    np.sum(flag) == 0
), "There are flagged visibilities, packing assumptions violated."

np.savez(
    "logo_cube.noise.npz",
    uu=d["uu"],
    vv=d["vv"],
    weight=d["weight"],
    data=d["data"],
)

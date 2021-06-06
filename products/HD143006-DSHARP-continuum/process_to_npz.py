from visread import examine
import numpy as np

fname = "HD143006_continuum.ms"

# get all spws
spws = examine.get_unique_datadescid(fname)

uu = []
vv = []
weight = []
data = []

# for a given spw
for spw in spws:
    # calculate rescale factor and replot
    sigma_rescale = examine.get_sigma_rescale_datadescid(fname, spw)

    # get processed visibilities
    # including complex conjugation
    d = examine.get_processed_visibilities(fname, spw, sigma_rescale=sigma_rescale)

    # flatten and concatenate
    flag = d["flag"]
    uu.append(d["uu"][~flag])
    vv.append(d["vv"][~flag])
    weight.append(d["weight"][~flag])
    data.append(d["data"][~flag])

np.savez(
    "HD143006_continuum.npz",
    uu=np.concatenate(uu),
    vv=np.concatenate(vv),
    weight=np.concatenate(weight),
    data=np.concatenate(data),
)

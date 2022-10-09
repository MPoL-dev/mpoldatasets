from visread import examine
import numpy as np
import matplotlib.pyplot as plt

fname = "HD143006_continuum.ms"

# get all spws
spws = examine.get_unique_datadescid(fname)

uu = []
vv = []
weight = []
model_data = []
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
    model_data.append(d["model_data"][~flag])

# concatenate all files together
uu = np.concatenate(uu)
vv = np.concatenate(vv)
weight = np.concatenate(weight)
data = np.concatenate(data)
model_data = np.concatenate(model_data)

# estimate S/N of all visibilities using amplitude
sigma = np.sqrt(1 / weight)
# data_amp = np.abs(data)
# substitute for the "signal"
model_data_amp = np.abs(model_data)

SN = model_data_amp / sigma

fig, ax = plt.subplots(nrows=1)
ax.hist(SN, bins=40)
ax.set_xscale("log")
fig.savefig("SN.png", dpi=300)


# filter all that have S/N < 0.05
thresh = 0.05
ind = SN > thresh

# convert to single precision.

np.savez(
    "HD143006_continuum_trimmed.npz",
    uu=uu[ind],
    vv=vv[ind],
    weight=weight[ind],
    data=data[ind],
)


np.savez(
    "HD143006_continuum_trimmed_single.npz",
    uu=uu[ind].astype(np.single),
    vv=vv[ind].astype(np.single),
    weight=weight[ind].astype(np.single),
    data=data[ind].astype(np.complex64),
)

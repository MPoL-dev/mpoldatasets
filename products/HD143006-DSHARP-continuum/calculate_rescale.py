from visread import examine
import os
import matplotlib.pyplot as plt

fname = "HD143006_continuum.ms"

# get all spws
spws = examine.get_unique_datadescid(fname)
# checks out that there are 29 spws

curdir = os.getcwd()

# make a pre-scaled directory
noscaledir = "rawscale"
if not os.path.exists(noscaledir):
    os.makedirs(noscaledir)

# make a rescaled directory
scaledir = "rescale"
if not os.path.exists(scaledir):
    os.makedirs(scaledir)

# for a given spw
for spw in spws:
    fig = examine.plot_scatter_datadescid(fname, spw)
    fig.savefig("{:}/{:02d}.png".format(noscaledir, spw), dpi=300)

    # calculate rescale factor and replot
    sigma_rescale = examine.get_sigma_rescale_datadescid(fname, spw)
    fig = examine.plot_scatter_datadescid(fname, spw, sigma_rescale=sigma_rescale)
    fig.savefig("{:}/{:02d}.png".format(scaledir, spw), dpi=300)

    plt.close("all")

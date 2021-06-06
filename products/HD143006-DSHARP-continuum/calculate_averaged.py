from visread import examine
import os
import matplotlib.pyplot as plt

fname = "HD143006_continuum.ms"

# get all spws
spws = examine.get_unique_datadescid(fname)
# checks out that there are 29 spws

curdir = os.getcwd()

# make a directory for the rescaled plots
avgdir = "average"
if not os.path.exists(avgdir):
    os.makedirs(avgdir)

# for a given spw
for spw in spws:
    # calculate rescale factor and replot
    sigma_rescale = examine.get_sigma_rescale_datadescid(fname, spw)

    # get processed visibilities
    d = examine.get_processed_visibilities(fname, spw, sigma_rescale=sigma_rescale)
    scatter = examine.get_averaged_scatter(d)

    fig = examine.plot_averaged_scatter(scatter)
    fig.savefig("{:}/{:02d}.png".format(avgdir, spw), dpi=300)

    plt.close("all")

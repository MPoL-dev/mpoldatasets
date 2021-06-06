# make a histogram of the spw scatter using visread
from visread import examine

fname = "logo_cube.noise.ms"
# calculate the rescale factor
factor = examine.get_sigma_rescale_datadescid(fname, 0)

fig = examine.plot_scatter_datadescid(fname, 0, sigma_rescale=2)
fig.savefig("spw_histogram.png", dpi=300)

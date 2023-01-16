import numpy as np
from visread import process, scatter
import casatools
import asdf

msmd = casatools.msmetadata()

fname = "AS209_continuum.ms"

# get all spws

msmd.open(fname)
spws = msmd.datadescids() 
msmd.done()

spw_tree = {}

# for a given spw
for spw in spws:
    # calculate rescale factor and replot
    sigma_rescale = scatter.get_sigma_rescale_datadescid(fname, spw)

    # get processed visibilities
    # including complex conjugation
    d = process.get_processed_visibilities(fname, spw, sigma_rescale=sigma_rescale)

    # each spw has a different number of channels, and is technically at a different frequency
    # we could average each visibility across frequency *if* the change in u-v was insignificant
    # otherwise we need to retain each point

    # in this instance, we'll assume that DSHARP already performed frequency averaging to the 
    # maximum extent possible

    # to save complexity further on, we could expand and concatenate visibilities. But we might want 
    # to use this dataset to test out various sensitivity plotting operations.

    # drop the "model_data" key from this dictionary, we no longer need it
    d.pop("model_data")

    # add this sub-dictionary to a larger dictionary
    spw_tree[spw] = d

# add this to a yet-larger tree
tree = {"spws": spw_tree}

# Create the ASDF file object from our data tree
af = asdf.AsdfFile(tree)

# Write the data to a new file
af.write_to("AS209_continuum.asdf")

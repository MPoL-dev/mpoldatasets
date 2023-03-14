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

data_list = []
weight_list = []
uu_list = []
vv_list = []

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

    data = d["data"]
    weight = d["weight"]
    uu = d["uu"]
    vv = d["vv"]
    flag = d["flag"]
    frequencies = d["frequencies"]

    # in this instance, we'll assume that DSHARP already performed frequency averaging to the 
    # maximum extent possible

    # to save complexity further on, we could expand and concatenate visibilities. But we might want 
    # to use this dataset to test out various sensitivity plotting operations.

    # obtain average frequency
    avg_frequency = np.average(frequencies)

    # convert uv to klambda
    uu = process.convert_baselines(uu, avg_frequency)
    vv = process.convert_baselines(vv, avg_frequency)

    # process the (nchan, nvis) flag to a (nvis) flag by 
    # flagging all channels if any one channel is bogus 
    flag = np.any(flag, axis=0)

    # average the data across channels to go from (nchan, nvis) to (nvis)
    data = np.average(data, axis=0)
    
    # apply flags
    data = data[~flag]
    weight = weight[~flag]
    uu = uu[~flag]
    vv = vv[~flag]
  
    # destroy channel axis and concatenate
    data_list.append(data.flatten())
    weight_list.append(weight.flatten())
    uu_list.append(uu.flatten())
    vv_list.append(vv.flatten())

# concatenate all files at the end
data = np.concatenate(data_list)
weight = np.concatenate(weight_list)
uu = np.concatenate(uu_list)
vv = np.concatenate(vv_list)

# add this to a yet-larger tree
tree = {"data": data, "weight":weight, "uu":uu, "vv":vv}

# Create the ASDF file object from our data tree
af = asdf.AsdfFile(tree)

# Write the data to a new file
af.write_to("AS209_continuum_averaged.asdf")

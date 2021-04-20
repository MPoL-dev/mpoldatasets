import visread
import glob
import numpy as np

# find all MS inside ms_split
mss = glob.glob("ms_split/*.ms")

uus = []
vvs = []
weights = []
data_res = []
data_ims = []

for ms in mss:
    cube = visread.read(ms)

    # swap convention
    cube.swap_convention(CASA_convention=False)

    mask = cube.mask  # [nchan, nvis]

    # apply mask and flatten
    uu = cube.uu[mask]
    vv = cube.vv[mask]
    weight = cube.weight[mask]
    data_re = cube.data_re[mask]
    data_im = cube.data_im[mask]

    # concatenate
    uus.append(uu)
    vvs.append(vv)
    weights.append(weight)
    data_res.append(data_re)
    data_ims.append(data_im)

uu = np.concatenate(uus)
vv = np.concatenate(vvs)
weight = np.concatenate(weights)
data_re = np.concatenate(data_res)
data_im = np.concatenate(data_ims)

cube = visread.Cube(
    np.array([230.0]),
    uu[np.newaxis, :],
    vv[np.newaxis, :],
    weight[np.newaxis, :],
    data_re[np.newaxis, :],
    data_im[np.newaxis, :],
    CASA_convention=False,
)
# save to NPZ
cube.to_npz("cont.npz")
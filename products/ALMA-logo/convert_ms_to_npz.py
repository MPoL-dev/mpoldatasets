import visread

cube = visread.read("logo_cube.noise.ms")
# swap convention
cube.swap_convention(CASA_convention=False)
cube.to_npz("logo_cube.noise.npz")

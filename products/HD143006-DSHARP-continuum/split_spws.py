import casatasks
import casatools
import pathlib

# initialize the relevant CASA tools
tb = casatools.table()
ms = casatools.ms()

vis = "HD143006_continuum.ms"
stem = "{:02d}.ms"

# all available SPW IDs
tb.open(vis + "/DATA_DESCRIPTION")
SPECTRAL_WINDOW_ID = tb.getcol("SPECTRAL_WINDOW_ID")
tb.close()

pathlib.Path("ms_split").mkdir(parents=True, exist_ok=True)

# split each spw to its own ms
for spw in SPECTRAL_WINDOW_ID:
    output = "ms_split/" + stem.format(spw)
    casatasks.mstransform(
        vis=vis,
        outputvis=output,
        spw="{:d}".format(spw),
        datacolumn="data",
        keepflags=False,
    )

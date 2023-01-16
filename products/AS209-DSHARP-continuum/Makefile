.PHONY: all Makefile clean 

# download the files 
AS209_continuum.fits:
	wget https://almascience.eso.org/almadata/lp/DSHARP/images/AS209_continuum.fits

AS209_continuum.ms.tgz:
	wget https://almascience.eso.org/almadata/lp/DSHARP/MSfiles/AS209_continuum.ms.tgz

# extract tar file 
AS209_continuum.ms: AS209_continuum.ms.tgz
	tar xvzf $<
	touch -t 2008010000 AS209_continuum.ms # update timestamp to be newer than .tar.gz

# make our own tclean version to check
AS209_tclean.fits: AS209_continuum.ms tclean.py
	python tclean.py

PLOTS := rawscaled/00.png rescaled/00.png averaged/00.png

# make scatter diagnostic plots
rawscaled/00.png: AS209_continuum.ms AS209_tclean.fits
	plot_spectral_windows.py $< --rawscaled

rescaled/00.png: AS209_continuum.ms AS209_tclean.fits
	plot_spectral_windows.py $< --rescaled

averaged/00.png: AS209_continuum.ms AS209_tclean.fits
	plot_spectral_windows.py $< --averaged

# process ms into an npz file using python script 
AS209_continuum.asdf: AS209_continuum.ms AS209_tclean.fits process_to_npz.py
	python process_to_npz.py
	cp AS209_continuum.asdf ../zenodo-staging/

all: AS209_continuum.asdf AS209_continuum.fits AS209_continuum.ms AS209_tclean.fits ${PLOTS}
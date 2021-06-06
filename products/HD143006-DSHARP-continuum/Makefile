all: HD143006_continuum.fits HD143006_continuum.ms HD143006_tclean.fits HD143006_continuum.npz

.PHONY: all Makefile clean 

# download the files 
HD143006_continuum.fits:
	wget https://almascience.eso.org/almadata/lp/DSHARP/images/HD143006_continuum.fits

HD143006_continuum.ms.tgz:
	wget https://almascience.eso.org/almadata/lp/DSHARP/MSfiles/HD143006_continuum.ms.tgz

# extract tar file 
HD143006_continuum.ms: HD143006_continuum.ms.tgz
	tar xvzf $<
	touch -t 2008010000 HD143006_continuum.ms # update timestamp to be newer than .tar.gz

# make our own tclean version to check
HD143006_tclean.fits: HD143006_continuum.ms tclean.py
	python tclean.py

rawscale/00.png rescale/00.png: calculate_rescale.py HD143006_continuum.ms
	python calculate_rescale.py

average/00.png: calculate_averaged.py HD143006_continuum.ms
	python calculate_averaged.py

# process ms into an npz file using python script 
# assumes virtual environment has been activated prior
# to running
HD143006_continuum.npz: HD143006_continuum.ms HD143006_tclean.fits process_to_npz.py
	python process_to_npz.py
	cp HD143006_continuum.npz ../zenodo-staging/

clean:
	rm -rf *.log
	rm -rf HD143006_tclean.*
	rm -rf HD143006_continuum.npz
	rm -rf ms_split
	rm -rf HD143006_continuum.ms
	rm -rf HD143006_continuum.fits
	rm -rf rawscale 
	rm -rf rescale 
	rm -rf average

cleanall: clean
	rm -rf HD143006_continuum.ms.tgz
	
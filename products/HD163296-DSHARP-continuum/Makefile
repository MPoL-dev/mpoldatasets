.PHONY: Makefile clean 

all: HD163296_continuum.fits HD163296_continuum.ms

# download the files 
HD163296_continuum.fits:
	wget https://almascience.eso.org/almadata/lp/DSHARP/images/HD163296_continuum.fits

HD163296_continuum.ms.tgz:
	wget https://almascience.eso.org/almadata/lp/DSHARP/MSfiles/HD163296_continuum.ms.tgz

# extract tar file 
HD163296_continuum.ms: HD163296_continuum.ms.tgz
	tar xvzf $<

# process ms into an npz file using python script 
# assumes virtual environment has been activated prior
# to running
HD163296_continuum.npz: HD163296_continuum.ms
	python process_to_npz.py

clean:
	rm -rf HD163296_continuum.fits
	rm -rf HD163296_continuum.ms.tgz
	rm -rf HD163296_continuum.ms
	rm -rf HD163296_continuum.npz


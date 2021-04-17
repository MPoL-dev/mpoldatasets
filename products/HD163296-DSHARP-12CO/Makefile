.PHONY: Makefile clean all

all: HD163296_CO.fits HD163296_COcube.ms.contsub

# download the files 
HD163296_CO.fits: 
	wget https://almascience.eso.org/almadata/lp/DSHARP/images/HD163296_CO.fits

HD163296_CO.ms.tgz:
	wget https://almascience.eso.org/almadata/lp/DSHARP/MSfiles/HD163296_CO.ms.tgz

# extract tar file 
HD163296_COcube.ms.contsub: HD163296_CO.ms.tgz
	tar xvzf $<
 
# process ms into an npz file using python script 
# assumes virtual environment has been activated prior
# to running
HD163296_CO.npz: HD163296_CO.ms 
	python process_to_npz.py

clean:
	rm -rf HD163296_CO.fits
	rm -rf HD163296_CO.ms.tgz
	rm -rf HD163296_COcube.ms.contsub
	rm -rf HD163296_CO.npz

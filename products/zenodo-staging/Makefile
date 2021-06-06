.PHONY: Makefile clean all upload

PRODUCTS := logo_cont.fits logo_cube.fits HD143006_continuum.npz logo_cube.dirty.fits logo_cube.noise.ms.tar.gz logo_cube.noise.npz logo_cube.tclean.fits

# calculate md5 sums of all products that are on disk locally
locallist.chk: ${PRODUCTS}
	md5sum ${PRODUCTS} > locallist.chk

# get list of files (+ their md5 sums) in zenodo repository
zenodolist.chk: query_zenodo_list.py locallist.chk
	python query_zenodo_list.py

# make a "payload" of all local files that are not currently on zenodo
payloadlist.txt: locallist.chk zenodolist.chk 
	python assemble_payload.py

# create a new version of the repository (pre-publication)
# and upload the files 
# final publication should be done manually through zenodo.org interface
upload: payloadlist.txt zenodolist.chk locallist.chk	
	python upload_payload.py

clean:
	rm -rf logo_cont.fits 
	rm -rf logo_cube.fits
	rm -rf HD143006_continuum.npz 
	rm -rf logo_cube.dirty.fits
	rm -rf logo_cube.tclean.fits
	rm -rf logo_cube.noise.ms.tar.gz
	rm -rf logo_cube.noise.npz
	rm -rf locallist.chk 
	rm -rf zenodolist.chk
	
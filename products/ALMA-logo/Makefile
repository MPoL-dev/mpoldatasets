.PHONY: Makefile clean all

all: logo_cont.fits logo_cube.fits logo_cube.noise.ms.tar.gz logo_cube.noise.npz logo_cube.dirty.fits logo_cube.tclean.fits spw_histogram.png

# make FITS cubes from PNG
logo_cont.fits: alma-logo-white-outline.png make_logo_cont.py
	python make_logo_cont.py
	cp logo_cont.fits ../zenodo-staging/

logo_cube.fits: logo_cont.fits 
	python make_logo_cube.py
	cp logo_cube.fits ../zenodo-staging/

# make mock datasets using simobserve 
logo_cube.noise.ms: logo_cube.fits simobserve_cube.py 
	python simobserve_cube.py 
	mv sim/sim.alma.cycle7.7.noisy.ms logo_cube.noise.ms

logo_cube.noise.ms.tar.gz: logo_cube.noise.ms
	tar cvzf logo_cube.noise.ms.tar.gz logo_cube.noise.ms
	cp logo_cube.noise.ms.tar.gz ../zenodo-staging/

logo_cube.noise.npz: logo_cube.noise.ms convert_ms_to_npz.py
	python convert_ms_to_npz.py
	cp logo_cube.noise.npz ../zenodo-staging/

logo_cube.dirty.fits: logo_cube.noise.ms tclean-dirty.py 
	python tclean-dirty.py 
	cp logo_cube.dirty.fits ../zenodo-staging/

logo_cube.tclean.fits: logo_cube.noise.ms tclean-iter.py 
	python tclean-iter.py 
	cp logo_cube.tclean.fits ../zenodo-staging/

spw_histogram.png: tclean-iter.py logo_cube.tclean.fits logo_cube.noise.ms spw_scatter.py
	python spw_scatter.py 

clean:
	rm -rf logo_cont.fits
	rm -rf logo_cube.fits
	rm -rf sim
	rm -rf logo_cube.noise.ms 
	rm -rf logo_cube.noise.ms.tar.gz 
	rm -rf logo_cube.noise.npz
	rm -rf logo_cube.dirty.* 
	rm -rf logo_cube.tclean.* 
	rm -rf casa*.log
	rm -rf *.last
	
	
# mpoldatasets

The MPoL package relies upon real and mock datasets of calibrated visibilities for testing and tutorials. Most of these datasets are pretty substantial (> 100 Mb) and some are even truly large (> 1 Gb). 

In many instances, there is a set of pre-processing steps to go from "raw" data to calibrated visibilities. For example, data downloaded from the ALMA archive often needs to have the pipeline run to restore the calibrated visibilities. And, the set of visibilities that we might want to image (e.g., 2 Gb for a spectral line) is often much smaller than the full dataset (e.g., 300 Gb for a multiple execution-block measurement set), which frequently contains spectral channels of other transitions or calibrators.

Therefore, these "raw" datasets need to be processed before they are uploaded into a minimal format on Zenodo so they can be used efficiently in MPoL tutorials.

## What is this repository? 

This repository collects all of the processing scripts together so that they can be version controlled and updated as the MPoL package evolves. It includes a set of common routines in the `/src/mpoldatasets` package, but the primary code lives in the subdirectories of `/products`. Each subdirectory in `/products` should contain a Makefile and scripts necessary to produce the tutorial dataset product.

The products from this are uploaded to [this Zenodo repository](https://doi.org/10.5281/zenodo.4498438), which is administered by Ian Czekala.

## What if I want to contribute my own tutorial to MPoL?

Follow the [MPoL developer documentation](https://mpol-dev.github.io/MPoL/developer-documentation.html) about writing a tutorial using a Jupyter notebook. If your tutorial requires a dataset, the simplest solution is to upload your own dataset to your own Zenodo repository and provide that link in the tutorial. Be sure to document what pre-processing steps you took (e.g., the script) in the Zenodo repository for reference.

You might also consider integrating the processing script into this package by opening a pull request. Please raise a [Github issue](https://github.com/MPoL-dev/mpoldatasets/issues) to coordinate the preparation of this script.

## Installation

This package depends on CASA6 `casatools` and so must be installed in the following manner

    $ pip install --extra-index-url https://casa-pip.nrao.edu/repository/pypi-casa-release/simple -e .

For more information on this requirement, see the discussion in the [visread documentation](https://visread.readthedocs.io/en/latest/installation.html).

## Environment variables 

The Makefiles and scripts rely upon the following environment variables:

* ``ZENODO_BASE_ID``: integer corresponding to the repository. Should be 4498439 for the live repository. But this can be changed to a different id if you are working with a sandbox environment.
* ``ZENODO_BASE_URL``: should be "https://zenodo.org" for the live repository, or "https://sandbox.zenodo.org" for the sandbox environment
* ``ZENODO_API_TOKEN``: the personal access token corresponding to the live or sandbox repository, whichever one you're using.
* ``DSETS_SCRATCH_DIR``: the scratch directory where the Makefiles will be run.

## Generating products with this package

This package will copy all finalized products to the `zenodo-staging` directory in the ``DSETS_SCRATCH_DIR``. Once that is complete, ``cd`` to this directory and run the Makefile there to upload the files to an unpublished staging area of the zenodo repository.
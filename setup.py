import setuptools
import os.path

with open("README.md", "r") as fh:
    long_description = fh.read()


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


version = get_version("src/mpoldatasets/__init__.py")


EXTRA_REQUIRES = {
    "test": ["pytest", "matplotlib"],
    "docs": ["matplotlib",],
}

EXTRA_REQUIRES["dev"] = (
    EXTRA_REQUIRES["test"] + EXTRA_REQUIRES["docs"] + ["pylint", "black", "jupyter"]
)

setuptools.setup(
    name="mpoldatasets",
    version=version,
    author="Ian Czekala",
    author_email="iczekala@psu.edu",
    description="Real and Mock Datasets for Regularized Maximum Likelihood Imaging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MPoL-dev/mpoldatasets",
    install_requires=["numpy", "astropy", "requests"],
    extras_require=EXTRA_REQUIRES,
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

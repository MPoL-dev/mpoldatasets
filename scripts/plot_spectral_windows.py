#!/usr/bin/env python3

from visread import examine
import os
import matplotlib.pyplot as plt
import argparse


def plot_raw(fname):
    # make a pre-scaled directory
    noscaledir = "rawscaled"
    if not os.path.exists(noscaledir):
        os.makedirs(noscaledir)

    for spw in examine.get_unique_datadescid(fname):
        fig = examine.plot_scatter_datadescid(fname, spw)
        fig.savefig("{:}/{:02d}.png".format(noscaledir, spw), dpi=300)

    plt.close("all")


def plot_rescaled(fname):
    # make a rescaled directory
    scaledir = "rescaled"
    if not os.path.exists(scaledir):
        os.makedirs(scaledir)

    for spw in examine.get_unique_datadescid(fname):
        # calculate rescale factor and replot
        sigma_rescale = examine.get_sigma_rescale_datadescid(fname, spw)
        fig = examine.plot_scatter_datadescid(fname, spw, sigma_rescale=sigma_rescale)
        fig.suptitle(r"$\sigma = {:.2f}$".format(sigma_rescale))
        fig.savefig("{:}/{:02d}.png".format(scaledir, spw), dpi=300)

        plt.close("all")


def plot_averaged(fname):
    # make a directory for the rescaled plots
    avgdir = "averaged"
    if not os.path.exists(avgdir):
        os.makedirs(avgdir)

    for spw in examine.get_unique_datadescid(fname):
        # calculate rescale factor and replot
        sigma_rescale = examine.get_sigma_rescale_datadescid(fname, spw)

        # get processed visibilities
        d = examine.get_processed_visibilities(fname, spw, sigma_rescale=sigma_rescale)
        scatter = examine.get_averaged_scatter(d)

        fig = examine.plot_averaged_scatter(scatter)
        fig.savefig("{:}/{:02d}.png".format(avgdir, spw), dpi=300)

        plt.close("all")


def main():
    parser = argparse.ArgumentParser(
        description="Examine the scatter in each spectral window of a measurement set."
    )
    parser.add_argument("filename", help="Filename of measurement set")
    parser.add_argument(
        "--rawscaled",
        help="Plot the raw scatter of each polarization",
        action="store_true",
    )
    parser.add_argument(
        "--rescaled",
        help="Plot the scatter for each polarization using the calculated scatter",
        action="store_true",
    )
    parser.add_argument(
        "--averaged",
        help="Plot the scatter of the averaged polarizations, using the calculated scatter. Mimicks the exported product.",
        action="store_true",
    )

    args = parser.parse_args()

    if args.rawscaled:
        plot_raw(args.filename)

    if args.rescaled:
        plot_rescaled(args.filename)

    if args.averaged:
        plot_averaged(args.filename)


if __name__ == "__main__":
    main()

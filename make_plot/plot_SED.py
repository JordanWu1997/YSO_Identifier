#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np


def plot_SED(SED_mag_array,
             JHK_system='2MASS',
             title_name=None,
             mag_lim=(-6, 6),
             new_fig=True,
             save_fig=True,
             output_name='./output.png'):
    """

    """
    wavelength_2MASS_SPITZER = [1.235, 1.662, 2.159, 3.6, 4.5, 5.8, 8.0, 24.0]
    wavelength_UKIDSS_SPITZER = [
        1.2483, 1.6313, 2.2010, 3.6, 4.5, 5.8, 8.0, 24.0
    ]

    wavelengths = wavelength_UKIDSS_SPITZER
    if JHK_system == '2MASS':
        wavelengths = wavelength_2MASS_SPITZER

    if new_fig:
        plt.figure()
    for wavelength in wavelengths:
        plt.axvline(wavelength, ls='-', c='k', lw=0.5)
    for SED_mag in SED_mag_array:
        if not -999. in SED_mag:
            shifted_mag = SED_mag - (SED_mag[1] - 1.) * np.ones(len(SED_mag))
            plt.plot(wavelengths, shifted_mag, ls='-.', lw=0.5, alpha=0.5)
    plt.xlabel('wavelength (um)', fontsize=20)
    plt.ylabel('shifted magnitude', fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.ylim(*mag_lim)
    plt.xscale('log')
    if title_name is None:
        plt.title('SED magnitude shifted to K_mag=1.0', fontsize=20)
    else:
        plt.title(title_name, fontsize=20)
    if save_fig:
        plt.savefig(output_name)

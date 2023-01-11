#!/usr/bin/env python

import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.append('./make_plot')
from plot_SED import plot_SED


def main():
    SED_mag_array = np.loadtxt('./tables/C2D_HREL-ALL-SED_mag_exXU.txt',
                               ndmin=2)[:, :8]
    evolved_star_mag_array = np.loadtxt('./tables/evolved_star_SED_mag.txt',
                                        ndmin=2)[:, :8]
    star_mag_array = np.loadtxt('./tables/star_SED_mag.txt', ndmin=2)[:, :8]
    galaxy_mag_array = np.loadtxt('./tables/galaxy_SED_mag.txt',
                                  ndmin=2)[:, :8]
    YSO_mag_array = np.loadtxt(
        './results/C2D_HREL-ALL-SED_mag_exXU/result_model_evolved_star_star_galaxy_bin1.0/YSO-SED_mag.txt',
        ndmin=2)[:, :8]

    plt.subplots(2, 2, figsize=(20, 16))
    plt.subplot(2, 2, 1)
    plot_SED(star_mag_array,
             JHK_system='2MASS',
             title_name='Star sample SED',
             mag_lim=(-10, 10),
             new_fig=False,
             save_fig=False)
    plt.subplot(2, 2, 2)
    plot_SED(evolved_star_mag_array,
             JHK_system='UKIDSS',
             title_name='Evolved star sample SED',
             mag_lim=(-10, 10),
             new_fig=False,
             save_fig=False)
    plt.subplot(2, 2, 3)
    plot_SED(galaxy_mag_array,
             JHK_system='UKIDSS',
             title_name='Galaxy sample SED',
             mag_lim=(-10, 10),
             new_fig=False,
             save_fig=False)
    plt.subplot(2, 2, 4)
    plot_SED(YSO_mag_array,
             JHK_system='2MASS',
             title_name='YSO sample SED',
             mag_lim=(-10, 10),
             new_fig=False,
             save_fig=False)
    plt.suptitle('SED in magnitude shifted to K magnitude = 1.0', fontsize=28)
    plt.tight_layout()
    plt.savefig('./figures/SED_this_work_sample.png')


if __name__ == '__main__':
    main()

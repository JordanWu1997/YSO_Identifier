#!/usr/bin/env python

from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np

# F0 (mJy): J, IR1, IR2, IR3, IR4, MP1
f0_2MASS_Spitzer = [
    1594000., 1024000., 666700., 280900., 179700., 115000., 64130., 7140.
]
# F0 (mJy): J, IR1, IR2, IR3, IR4, MP1
f0_UKIDSS_Spitzer = [
    1530000., 1019000., 631000., 280900., 179700., 115000., 64130., 7140.
]

# Supergiant Stars Table:
#  SpCl   J      H    Ks   IRAC1  IRAC2  IRAC3  IRAC4  MIPS1
SG_star_table = {
    'B0': [2.646, 1.594, 1., 0.383, 0.247, 0.149, 0.078, 0.009],
    'B5': [2.391, 1.550, 1., 0.403, 0.265, 0.163, 0.087, 0.010],
    'A0': [2.201, 1.522, 1., 0.417, 0.278, 0.171, 0.092, 0.011],
    'A5': [2.141, 1.508, 1., 0.427, 0.286, 0.176, 0.095, 0.011],
    'F0': [2.026, 1.494, 1., 0.435, 0.293, 0.181, 0.098, 0.011],
    'F5': [1.864, 1.467, 1., 0.438, 0.295, 0.183, 0.099, 0.011],
    'G0': [1.639, 1.427, 1., 0.446, 0.277, 0.179, 0.098, 0.011],
    'G5': [1.503, 1.401, 1., 0.450, 0.249, 0.175, 0.101, 0.012],
    'K0': [1.401, 1.375, 1., 0.455, 0.241, 0.177, 0.103, 0.012],
    'K5': [0.988, 1.278, 1., 0.462, 0.220, 0.179, 0.108, 0.013],
    'M0': [0.961, 1.266, 1., 0.463, 0.220, 0.179, 0.108, 0.013],
    'M2': [0.901, 1.220, 1., 0.480, 0.226, 0.191, 0.118, 0.014]
}
# Giant stars Table:
#  SpCl   J      H    Ks   IRAC1  IRAC2  IRAC3  IRAC4  MIPS1
G_star_table = {
    'G5': [1.408, 1.381, 1., 0.441, 0.263, 0.174, 0.097, 0.011],
    'K0': [1.326, 1.363, 1., 0.448, 0.247, 0.175, 0.100, 0.012],
    'K5': [0.988, 1.278, 1., 0.451, 0.221, 0.176, 0.104, 0.012],
    'M0': [0.978, 1.266, 1., 0.461, 0.221, 0.181, 0.108, 0.013]
}
# Main Sequence Table:
#  SpCl   J      H    Ks   IRAC1  IRAC2  IRAC3  IRAC4  MIPS1
MS_star_table = {
    'O8': [2.901, 1.608, 1., 0.378, 0.242, 0.145, 0.076, 0.008],
    'B0': [2.796, 1.608, 1., 0.379, 0.244, 0.147, 0.077, 0.008],
    'B3': [2.646, 1.579, 1., 0.394, 0.257, 0.156, 0.083, 0.009],
    'B5': [2.574, 1.564, 1., 0.400, 0.263, 0.161, 0.086, 0.010],
    'B8': [2.481, 1.550, 1., 0.406, 0.269, 0.165, 0.088, 0.010],
    'A0': [2.391, 1.536, 1., 0.416, 0.277, 0.170, 0.092, 0.010],
    'A5': [2.201, 1.508, 1., 0.422, 0.279, 0.171, 0.092, 0.010],
    'F0': [1.989, 1.480, 1., 0.429, 0.285, 0.175, 0.094, 0.011],
    'F5': [1.882, 1.453, 1., 0.432, 0.282, 0.175, 0.094, 0.011],
    'G0': [1.797, 1.440, 1., 0.436, 0.276, 0.174, 0.094, 0.011],
    'G5': [1.670, 1.421, 1., 0.436, 0.271, 0.174, 0.094, 0.011],
    'K0': [1.551, 1.401, 1., 0.438, 0.260, 0.174, 0.096, 0.011],
    'K5': [1.176, 1.325, 1., 0.453, 0.251, 0.185, 0.105, 0.012],
    'M0': [1.113, 1.301, 1., 0.471, 0.272, 0.209, 0.121, 0.015],
    'M2': [1.053, 1.266, 1., 0.483, 0.278, 0.218, 0.127, 0.016],
    'M5': [1.044, 1.176, 1., 0.488, 0.289, 0.223, 0.130, 0.016],
}

# Wavelength for UKIDSS + Spitzer (unit: micrometer)
wavelength_UKIDSS_SPITZER = [
    1.2483, 1.6313, 2.2010, 3.6, 4.5, 5.8, 8.0, 24.0, 70.0
]
wavelength_2MASS_SPITZER = [
    1.235, 1.662, 2.159, 3.6, 4.5, 5.8, 8.0, 24.0, 70.0
]

# C_av for UKIDSS + Spitzer at Rv 5.5
# Parameters [band, flux index, mag index, C_av(Exctintion_coef)]
C_av_2MASS_Spitzer = [
    0.2741, 0.1622, 0.1119, 0.0671, 0.0543, 0.0444, 0.0463, 0.0259
]
C_av_UKIDSS_Spitzer = [
    0.2702, 0.1673, 0.1095, 0.0671, 0.0543, 0.0444, 0.0463, 0.0259
]

SEIP_error_mag_list = [0.5, 0.5, 0.5, 0.2, 0.2, 0.2, 0.2, 0.5]


def calculate_flux(mag_Ks, spectral_class, star_table, f0_2MASS_Ks=666.7):
    """
    flux_list unit: Jy
    """
    flux_list = []
    for value in star_table[spectral_class]:
        flux = 10**(-mag_Ks / 2.5) * f0_2MASS_Ks * value
        flux_list.append(flux)
    return flux_list


def flux2mag(flux_list, f0_list=f0_2MASS_Spitzer):
    """
    f0_list unit: mJy
    """
    mag_list = []
    for flux, f0 in zip(flux_list, f0_list):
        mag = -2.5 * np.log10(flux / (f0 * 1e-3))
        mag_list.append(mag)
    return mag_list


def TwoMass2UKIDSS(mag_list, index_J=0, index_H=1, index_Ks=2):
    """

    """
    mag_J, mag_H, mag_Ks = mag_list[index_J], mag_list[index_H], mag_list[
        index_Ks]
    mag_J_UKIDSS = mag_J - 0.065 * (mag_J - mag_H)
    mag_H_UKIDSS = mag_H + 0.07 * (mag_J - mag_H)
    mag_K_UKIDSS = mag_Ks + 0.01 * (mag_J - mag_Ks)

    new_mag_list = mag_list
    new_mag_list[index_J] = mag_J_UKIDSS
    new_mag_list[index_H] = mag_H_UKIDSS
    new_mag_list[index_Ks] = mag_K_UKIDSS
    return new_mag_list


def generate_spectral_class_star_mag(mag_Ks,
                                     spectral_class,
                                     star_table,
                                     to_UKIDSS=True):
    """

    """
    flux_list = calculate_flux(mag_Ks, spectral_class, star_table)
    mag_list = flux2mag(flux_list)
    if to_UKIDSS:
        mag_list = TwoMass2UKIDSS(mag_list)
    return mag_list


def generate_star_table_mag(star_table,
                            mag_Ks_min=0.,
                            mag_Ks_max=20.,
                            mag_interval=0.1,
                            to_UKIDSS=True):
    """

    """
    all_spectral_class_mag_list = []
    for spectral_class, table in star_table.items():
        for mag_Ks in np.arange(mag_Ks_min, mag_Ks_max, mag_interval):
            star_mag = generate_spectral_class_star_mag(mag_Ks,
                                                        spectral_class,
                                                        star_table,
                                                        to_UKIDSS=to_UKIDSS)
            all_spectral_class_mag_list.append(star_mag)
    return all_spectral_class_mag_list


def plot_star_table_MMD(
        SEIP_band_name=['J', 'H', 'Ks', 'IR1', 'IR2', 'IR3', 'IR4', 'MP1'],
        savefig=True,
        mag_interval=1):
    """

    """
    # Generate star sed from table
    SG_star_sed = np.array(
        generate_star_table_mag(SG_star_table, mag_interval=mag_interval))
    G_star_sed = np.array(
        generate_star_table_mag(G_star_table, mag_interval=mag_interval))
    MS_star_sed = np.array(
        generate_star_table_mag(MS_star_table, mag_interval=mag_interval))

    # Plot MMD
    plt.subplots(9, 7, figsize=(32, 20))
    for i, comb in enumerate(
            combinations([i for i, _ in enumerate(SEIP_band_name)], 2)):
        plt.subplot(4, 7, i + 1)
        id1, id2 = comb

        plt.scatter(SG_star_sed[:, id1],
                    SG_star_sed[:, id2],
                    s=0.1,
                    alpha=0.5,
                    color='r',
                    label='SG_star')
        plt.scatter(G_star_sed[:, id1],
                    G_star_sed[:, id2],
                    s=0.1,
                    alpha=0.5,
                    color='g',
                    label='G_star')
        plt.scatter(MS_star_sed[:, id1],
                    MS_star_sed[:, id2],
                    s=0.1,
                    alpha=0.5,
                    color='b',
                    label='MS_star')

        plt.xlabel('{} (mag)'.format(SEIP_band_name[id1]), fontsize=16)
        plt.ylabel('{} (mag)'.format(SEIP_band_name[id2]), fontsize=16)
        plt.grid(alpha=0.2)
        plt.legend()
        plt.suptitle('Magnitude-Magnitude Diagram of Star from Template',
                     fontsize=20)
    if savefig:
        plt.savefig('template_star_MMD.png')
    else:
        plt.show()


def generate_star_from_template(savetxt=True,
                                mag_interval=0.1,
                                to_UKIDSS=True):
    # Generate star sed from table
    SG_star_sed = np.array(
        generate_star_table_mag(SG_star_table,
                                mag_interval=mag_interval,
                                to_UKIDSS=to_UKIDSS))
    G_star_sed = np.array(
        generate_star_table_mag(G_star_table,
                                mag_interval=mag_interval,
                                to_UKIDSS=to_UKIDSS))
    MS_star_sed = np.array(
        generate_star_table_mag(MS_star_table,
                                mag_interval=mag_interval,
                                to_UKIDSS=to_UKIDSS))
    star_sed_from_template = np.concatenate(
        (SG_star_sed, G_star_sed, MS_star_sed), axis=0)
    return star_sed_from_template


def add_Av(star_sed_mag,
           C_av_list=C_av_UKIDSS_Spitzer,
           Av_min=0.0,
           Av_max=8.0,
           Av_interval=0.5):
    new_mag_list = []
    for sed_mag in star_sed_mag:
        for Av in np.arange(Av_min, Av_max, Av_interval):
            new_sed_mag = [
                sed_mag[i] + C_av * Av for i, C_av in enumerate(C_av_list)
            ]
            new_mag_list.append(new_sed_mag)
    return new_mag_list


def add_error(star_sed_mag, error_mag_list=SEIP_error_mag_list, error_num=3):
    new_mag_list = []
    for sed_mag in star_sed_mag:
        for error_mag in error_mag_list:
            for error in np.linspace(-abs(error_mag),
                                     abs(error_mag),
                                     error_num,
                                     endpoint=True):
                sed_mag = np.array(sed_mag)
                new_sed_mag = sed_mag + error * np.ones(len(sed_mag))
                new_mag_list.append(new_sed_mag)
    return new_mag_list


def main():
    # Template star
    template_star_SED_mag = generate_star_from_template(to_UKIDSS=False)
    # Add Av
    template_star_WI_max_Av_50_SED_mag = add_Av(template_star_SED_mag,
                                                Av_max=50.0)
    # Save result
    np.savetxt('template_star_SED_mag.txt', template_star_SED_mag)
    np.savetxt('template_star_WI_max_Av_50_SED_mag.txt',
               template_star_WI_max_Av_50_SED_mag)


if __name__ == '__main__':
    main()

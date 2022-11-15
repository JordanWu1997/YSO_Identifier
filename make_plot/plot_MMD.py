#!/usr/bin/env python

from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np


def extract_mag_from_dict_npy(input_dict_npy, binsize,
                              lower_bound=np.zeros(8)):
    """

    """
    input_dict = np.load(input_dict_npy, allow_pickle=True).item()
    bin_array = np.array(list(input_dict.keys()))
    mag_array = lower_bound + binsize * (bin_array)
    return mag_array


def extract_mag_from_array_npy(input_array_npy,
                               binsize,
                               lower_bound=np.zeros(8)):
    """

    """
    bin_array = np.load(input_array_npy, allow_pickle=True)
    mag_array = lower_bound + binsize * (bin_array)
    return mag_array


def generate_mag_array_list(input_catalog_list,
                            input_type_list=None,
                            input_binsize_list=None,
                            input_lower_bound_list=None):
    """

    """
    mag_array_list = []
    for i, (input_type, input_catalog) in enumerate(
            zip(input_type_list, input_catalog_list)):
        if input_type == 'txt':
            mag_array = np.loadtxt(input_catalog)
        elif input_type == 'arr':
            mag_array = extract_mag_from_array_npy(input_catalog,
                                                   input_binsize_list[i],
                                                   input_lower_bound_list[i])
        elif input_type == 'dict':
            mag_array = extract_mag_from_dict_npy(input_catalog,
                                                  input_binsize_list[i],
                                                  input_lower_bound_list[i])
        else:
            print('Wrong input type')
        mag_array_list.append(mag_array)
    return mag_array_list


def generate_filtered_input_array_list(input_catalog_list, filtered=-999.):
    """

    """
    input_array_list = []
    for input_catalog in input_catalog_list:
        input_array = np.loadtxt(input_catalog, dtype=float)[:, :8]
        filtered_list = []
        for array in input_array:
            if not np.all(array != filtered):
                array[array == filtered] = np.nan
            else:
                # print('{} input is filtered out'.format(str(filtered)))
                pass
            filtered_list.append(array)
        input_array_list.append(np.array(filtered_list))
    return input_array_list


def plot_MMD(
        input_array_list,
        input_label_list,
        input_color_list,
        input_size_list,
        input_alpha_list,
        band_name_list=['J', 'H', 'Ks', 'IR1', 'IR2', 'IR3', 'IR4', 'MP1'],
        axis_unit='mag',
        suptitle_name=None,
        show_legend=True,
        save_fig=True,
        output_name='output.png',
        MP1_only=False):
    """

    """
    if MP1_only:
        plt.subplots(2, 4, figsize=(16, 10))
        for i in range(7):
            plt.subplot(2, 4, i + 1)
            for j, input_array in enumerate(input_array_list):
                input_array_1 = input_array[:, i]
                input_array_2 = input_array[:, 7]
                input_array_1[input_array_1 == -999.0] = np.nan
                input_array_2[input_array_2 == -999.0] = np.nan
                plt.scatter(input_array_1,
                            input_array_2,
                            label=input_label_list[j],
                            c=input_color_list[j],
                            s=input_size_list[j],
                            alpha=input_alpha_list[j])
                plt.xlabel('{} ({})'.format(band_name_list[i], axis_unit),
                           fontsize=20)
                plt.ylabel('{} ({})'.format(band_name_list[7], axis_unit),
                           fontsize=20)
                plt.grid(alpha=0.2)
                if show_legend:
                    plt.legend(fontsize=20, framealpha=0.3)

    else:
        plt.subplots(9, 7, figsize=(32, 20))
        for i, comb in enumerate(
                combinations([i for i, _ in enumerate(band_name_list)], 2)):
            plt.subplot(4, 7, i + 1)
            id1, id2 = comb
            for j, input_array in enumerate(input_array_list):
                input_array_1 = input_array[:, id1]
                input_array_2 = input_array[:, id2]
                input_array_1[input_array_1 == -999.0] = np.nan
                input_array_2[input_array_2 == -999.0] = np.nan
                plt.scatter(input_array_1,
                            input_array_2,
                            label=input_label_list[j],
                            c=input_color_list[j],
                            s=input_size_list[j],
                            alpha=input_alpha_list[j])
                plt.xlabel('{} ({})'.format(band_name_list[id1], axis_unit),
                           fontsize=20)
                plt.ylabel('{} ({})'.format(band_name_list[id2], axis_unit),
                           fontsize=20)
                plt.xticks(fontsize=20)
                plt.yticks(fontsize=20)
                plt.grid(alpha=0.2)
                if show_legend:
                    plt.legend(fontsize=20, framealpha=0.3)

    if suptitle_name is None:
        suptitle_name = 'Magnitude-Magnitude Diagram (MMD)\n'
        for input_label in input_label_list:
            suptitle_name += '{}, '.format(input_label)
    plt.suptitle(suptitle_name, fontsize=28)
    plt.tight_layout()

    if save_fig:
        plt.savefig(output_name)


def main():
    """

    """
    input_catalog_list = [
        # '../tables/SEIP_galaxy-SED_UKIDSS_mag_exXUS.txt',
        # '../models/SEIP_galaxy_bin1.0_filled_bounds_grid.npy',
        # '../tables/star_from_template_sed_mag_WI_max_Av_30.txt',
        # '../models/template_star_max_Av_30_bin1.0_filled_bounds_grid.npy',
        # '../tables/C2D_HREL-star-ALL-SED_mag_exXU.txt',
        # '../models/C2D_star_bin1.0_filled_bounds_grid.npy',
        '../tables/SWIRE-ELAIS_N1-SED_mag_exXU.txt',
        '../models/SWIRE_galaxy_bin1.0_filled_bounds_grid.npy',
    ]
    input_array_list_all = generate_mag_array_list(
        input_catalog_list,
        input_type_list=['txt', 'arr'],
        input_binsize_list=[None, 1.0],
        input_lower_bound_list=[np.ones(8)] * 2)
    input_color_list = ['g', 'r']
    input_size_list = [5, 40]
    input_alpha_list = [0.3, 1.0]
    input_label_list = ['SWIRE_galaxy', 'binned_SWIRE_galaxy']
    # input_label_list = ['TS_max_Av_30', 'binned_TS_max_Av_30']
    output_name = 'test1.png'
    plot_MMD(input_array_list_all,
             input_label_list,
             input_color_list,
             input_size_list,
             input_alpha_list,
             output_name=output_name)


if __name__ == '__main__':
    main()

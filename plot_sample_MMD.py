#!/usr/bin/env python

import sys

import numpy as np

sys.path.append('./make_plot/')

from plot_MMD import generate_filtered_input_array_list, plot_MMD


def main():
    input_catalog_list = [
        './tables/star_SED_mag.txt',
        './tables/galaxy_SED_mag.txt',
        './tables/evolved_star_SED_mag.txt',
    ]
    input_color_list = [
        'k',
        'g',
        'r',
    ]
    input_size_list = [
        0.5,
        1,
        5,
    ]
    input_alpha_list = [
        0.3,
        0.3,
        0.3,
    ]
    input_label_list = [
        'star (black)',
        'galaxy (green)',
        'evolved star (red)',
    ]
    input_array_list = generate_filtered_input_array_list(input_catalog_list)
    output_name = './figures/MMD_sample.png'
    plot_MMD(input_array_list,
             input_label_list,
             input_color_list,
             input_size_list,
             input_alpha_list,
             show_legend=False,
             output_name=output_name)


if __name__ == '__main__':
    main()

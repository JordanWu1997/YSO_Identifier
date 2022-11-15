#!/usr/bin/env python

import sys

sys.path.append('./make_plot/')

from plot_MMD import generate_filtered_input_array_list, plot_MMD


def main():
    input_catalog_list = [
        './tables/star_SED_mag.txt',
        './results/C2D_HREL-ALL-SED_mag_exXU/result_model_evolved_star_star_galaxy_bin1.0/YSO-SED_mag.txt',
    ]
    input_color_list = [
        'k',
        'b',
    ]
    input_size_list = [
        0.5,
        5,
    ]
    input_alpha_list = [
        0.3,
        1.0,
    ]
    input_label_list = [
        'star sample (black)',
        'YSO candidate (blue)',
    ]
    input_array_list = generate_filtered_input_array_list(input_catalog_list)
    output_name = './figures/MMD_result.png'
    plot_MMD(input_array_list,
             input_label_list,
             input_color_list,
             input_size_list,
             input_alpha_list,
             show_legend=False,
             output_name=output_name)


if __name__ == '__main__':
    main()

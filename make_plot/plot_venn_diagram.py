#!/usr/bin/env python
# -*- coding:utf-8 -*-

# ############################################################################
# :Author: Kuan-Hsien Wu
# :Email: jordankhwu@gapp.nthu.edu.tw
# :Date: 2022-01-16
# :Description: This code is to plot Venn diagram for 3 input SED catalog
#               which first gridded in magnitude space
# ############################################################################

from itertools import combinations

import numpy as np
from matplotlib import pyplot as plt
from matplotlib_venn import venn3, venn3_unweighted


def generate_set_list(input_catalog_list):
    """

    """
    input_set_list = []
    for input_catalog in input_catalog_list:
        try:
            input_dict = np.load(input_catalog, allow_pickle=True).item()
            input_set = {key for key in input_dict.keys()}
        except ValueError:
            input_array = np.load(input_catalog, allow_pickle=True)
            input_set = {tuple(array) for array in input_array}
        input_set_list.append(input_set)
    return input_set_list


def plot_venn3_diagram(input_set_list,
                       input_label_list,
                       input_color_list,
                       title='',
                       weighted=False,
                       newfig=False,
                       showfig=True,
                       savefig=True,
                       output='out.png'):
    """

    """
    if newfig:
        plt.figure()
    if weighted:
        v = venn3(subsets=input_set_list,
                  set_labels=input_label_list,
                  set_colors=input_color_list)
        for t in v.subset_labels:
            if t is not None:
                t.set_fontsize(0)
    else:
        v = venn3_unweighted(subsets=input_set_list,
                             set_labels=input_label_list,
                             set_colors=input_color_list)
        for t in v.subset_labels:
            # t.set_fontsize(12)
            t.set_fontsize(16)
    for t in v.set_labels:
        # t.set_fontsize(14)
        t.set_fontsize(20)
    # plt.title(title, fontsize=14)
    plt.title(title, fontsize=20)
    if savefig:
        plt.savefig(output)
    if showfig:
        plt.show()


def plot_venn3_diagram_diff_binsize(load_dir,
                                    binsize_list,
                                    suffix_list,
                                    name_list,
                                    input_label_list,
                                    input_color_list=['blue', 'red', 'green'],
                                    showfig=True,
                                    savefig=True,
                                    projection=True,
                                    output='out.png'):
    """

    """
    plt.subplots(2, len(binsize_list), figsize=(16, 9))
    for i, binsize in enumerate(binsize_list):
        input_catalog_list = [
            '{}/{}_bin{:.1f}_{}.npy'.format(load_dir, name, binsize,
                                            suffix_list[i])
            for i, name in enumerate(name_list)
        ]
        input_set_list = generate_set_list(input_catalog_list)
        if projection:
            title = 'W/I Projection\nBin: {:.1f} mag'.format(binsize)
        else:
            title = 'W/O Projection\nBin: {:.1f} mag'.format(binsize)
        plt.subplot(2, len(binsize_list), i + 1)
        plot_venn3_diagram(input_set_list,
                           input_label_list,
                           input_color_list,
                           title=title,
                           weighted=False,
                           newfig=False,
                           showfig=False,
                           savefig=False,
                           output='bin{:.1f}.png'.format(binsize))
        plt.subplot(2, len(binsize_list), i + 1 + len(binsize_list))
        plot_venn3_diagram(input_set_list,
                           input_label_list,
                           input_color_list,
                           title=title,
                           weighted=True,
                           newfig=False,
                           showfig=False,
                           savefig=False,
                           output='bin{:.1f}.png'.format(binsize))
    if savefig:
        plt.savefig(output)
    if showfig:
        plt.show()


def main():
    """  """
    pass


if __name__ == '__main__':
    main()

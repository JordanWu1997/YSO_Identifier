#!/usr/bin/env python

import sys

sys.path.append('./make_plot/')

from plot_venn_diagram import plot_venn3_diagram_diff_binsize


def main():
    ##############################################################################
    # This work models with no projection
    ##############################################################################
    # Blue Red Green
    load_dir = './models'
    binsize_list = [0.2, 0.5, 1.0]
    suffix_list = [
        "filled_bounds_grid",
        "filled_bounds_grid",
        "filled_bounds_grid",
    ]
    name_list = [
        'star',
        'galaxy',
        'evolved_star',
    ]
    input_label_list = [
        'star',
        'galaxy',
        'evolved star',
    ]
    plot_venn3_diagram_diff_binsize(
        load_dir,
        binsize_list,
        suffix_list,
        name_list,
        input_label_list,
        showfig=False,
        projection=False,
        output='./figures/VD_WO_projection.png',
    )

    ##############################################################################
    # This work models with projection
    ##############################################################################
    # Blue Red Green
    load_dir = './models'
    binsize_list = [0.2, 0.5, 1.0]
    suffix_list = [
        "projected_grid",
        "projected_grid",
        "projected_grid",
    ]
    name_list = [
        'star',
        'galaxy',
        'evolved_star',
    ]
    input_label_list = [
        'star',
        'galaxy',
        'evolved star',
    ]
    plot_venn3_diagram_diff_binsize(
        load_dir,
        binsize_list,
        suffix_list,
        name_list,
        input_label_list,
        showfig=False,
        projection=True,
        output='./figures/VD_WI_projection.png',
    )


if __name__ == '__main__':
    main()

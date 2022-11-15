#!/usr/bin/env python

import sys

sys.path.append('./probe_model')
from probe_model.probe_populated_region_boundary import \
    probe_sample_and_generate_populated_region_grid_dicts

sys.path.append('./')
from model import Model


def main():
    output_dir = './models'
    input_catalog_list = [
        './tables/evolved_star_SED_mag.txt',
        './tables/star_SED_mag.txt',
        './tables/galaxy_SED_mag.txt',
    ]
    input_name_list = [
        'evolved_star',
        'star',
        'galaxy',
    ]
    binsize_list = [1.0, 0.5, 0.2]
    for binsize in binsize_list:
        print()
        probe_sample_and_generate_populated_region_grid_dicts(
            binsize,
            output_dir=output_dir,
            input_catalog_list=input_catalog_list,
            input_name_list=input_name_list,
            lower_bound_mag=Model.lower_bound_mag,
            upper_bound_mag=Model.upper_bound_mag,
            project_axis_vector=Model.axis_dir_vector,
            lower_indicator=Model.bright_indicator,
            upper_indicator=Model.faint_indicator,
            lack_indicator=Model.lack_indicator,
            verbose=True)


if __name__ == '__main__':
    main()

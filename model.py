#!/usr/bin/env python

import numpy as np


class Model():
    """

    """
    band_name_list = ['J', 'H', 'K', 'IR1', 'IR2', 'IR3', 'IR4', 'MP1']
    band_name_array = np.array(band_name_list, dtype=str)
    axis_dir_vector = np.ones(len(band_name_list), dtype=int)
    lower_bound_mag = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    upper_bound_mag = np.array(
        [19.0, 18.0, 18.0, 17.0, 17.0, 17.0, 17.0, 15.0])
    binsize_mag = 1.0
    do_reclassify = True

    IR2_ID, IR3_ID, MP1_ID = 4, 5, 7
    lack_indicator = -999.0
    bright_indicator = -9999.0
    faint_indicator = 9999.0

    def __init__(self, evolved_star_lower_bound_dict,
                 evolved_star_upper_bound_dict, star_lower_bound_dict,
                 star_upper_bound_dict, galaxy_lower_bound_dict,
                 galaxy_upper_bound_dict):
        """

        """
        if (evolved_star_lower_bound_dict
                is not None) and (evolved_star_upper_bound_dict is not None):
            self.evolved_star_lower_bound_array = np.array(list(
                np.load(evolved_star_lower_bound_dict,
                        allow_pickle=True).item().keys()),
                                                           dtype=int)
            self.evolved_star_upper_bound_array = np.array(list(
                np.load(evolved_star_upper_bound_dict,
                        allow_pickle=True).item().keys()),
                                                           dtype=int)
        self.star_lower_bound_array = np.array(list(
            np.load(star_lower_bound_dict, allow_pickle=True).item().keys()),
                                               dtype=int)
        self.star_upper_bound_array = np.array(list(
            np.load(star_upper_bound_dict, allow_pickle=True).item().keys()),
                                               dtype=int)
        self.galaxy_lower_bound_array = np.array(list(
            np.load(galaxy_lower_bound_dict, allow_pickle=True).item().keys()),
                                                 dtype=int)
        self.galaxy_upper_bound_array = np.array(list(
            np.load(galaxy_upper_bound_dict, allow_pickle=True).item().keys()),
                                                 dtype=int)

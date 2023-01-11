#!/usr/bin/env python

import numpy as np


class Model():
    """

    """
    # Name of band
    band_name_list = ['J', 'H', 'K', 'IR1', 'IR2', 'IR3', 'IR4', 'MP1']
    band_name_array = np.array(band_name_list, dtype=str)
    # Axis vector of diagonal direction
    axis_dir_vector = np.ones(len(band_name_list), dtype=int)
    # Lower (bright) boundary in unit of magnitude
    lower_bound_mag = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    # Upper (faint) boundary in unit of magnitude
    upper_bound_mag = np.array(
        [19.0, 18.0, 18.0, 17.0, 17.0, 17.0, 17.0, 15.0])
    # Binsize
    binsize_mag = 1.0
    # Do reclassification process
    do_reclassify = True
    # Band index for IR2,IR3,MP1 band for HL_AGB_star_classifier
    IR2_ID, IR3_ID, MP1_ID = 4, 5, 7
    # Lack of detection band magnitude indicator
    lack_indicator = -999.0
    # Bright band magnitude indicator
    bright_indicator = -9999.0
    # Faint band magnitude indicator
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

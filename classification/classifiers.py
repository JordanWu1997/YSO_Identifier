#!/usr/bin/env python

import sys

import numpy as np

sys.path.append('../')
from model import Model


def bright_flag(SED_mag, lower_bound_mag=Model.lower_bound_mag):
    """

    """
    is_bright = False
    if np.any(SED_mag < lower_bound_mag):
        is_bright = True
    return is_bright


def faint_flag(SED_mag, upper_bound_mag=Model.upper_bound_mag):
    """

    """
    is_faint = False
    if np.any(SED_mag > upper_bound_mag):
        is_faint = True
    return is_faint


def HL_AGB_star_classifier(IR2_mag, IR3_mag, MP1_mag):
    """

    """
    X23 = IR2_mag - IR3_mag
    Y35 = IR3_mag - MP1_mag

    if (X23 >= 0.0) and (X23 < 2.0) and (Y35 <= 2.0):
        if X23 - Y35 >= 0.0:
            is_AGB_star = True
        else:
            is_AGB_star = False
    elif (X23 >= 2.0) and (Y35 <= 2.0):
        is_AGB_star = True

    else:
        is_AGB_star = False
    return is_AGB_star


def HL_AGB_star_flag(SED_mag,
                     IR2_ID=Model.IR2_ID,
                     IR3_ID=Model.IR3_ID,
                     MP1_ID=Model.MP1_ID,
                     lack_indicator=Model.lack_indicator):
    """

    """
    is_AGB_star = False
    IR2_mag, IR3_mag, MP1_mag = SED_mag[IR2_ID], SED_mag[IR3_ID], SED_mag[
        MP1_ID]
    if lack_indicator not in [IR2_mag, IR3_mag, MP1_mag]:
        is_AGB_star = HL_AGB_star_classifier(IR2_mag, IR3_mag, MP1_mag)
    return is_AGB_star


def evolved_star_flag(binned_SED,
                      evolved_star_lower_bound_array,
                      evolved_star_upper_bound_array,
                      criteria='within_bounds',
                      axis_dir_vector=Model.axis_dir_vector,
                      return_isolated_flag=False):
    """

    """
    is_evolved_star, is_isolated = False, True
    for lower_bound, upper_bound in zip(evolved_star_lower_bound_array,
                                        evolved_star_upper_bound_array):
        if along_same_axis_flag(lower_bound, binned_SED, axis_dir_vector):
            is_isolated = False
            if criteria == 'within_bounds':
                if within_bounds_flag(binned_SED, lower_bound, upper_bound):
                    is_evolved_star = True
            elif criteria == 'above_lower_bound':
                if not lower_than_lower_bound_flag(binned_SED, lower_bound,
                                                   upper_bound):
                    is_evolved_star = True
    if return_isolated_flag:
        return is_evolved_star, is_isolated
    else:
        return is_evolved_star


def bin_SED_mag(SED_mag,
                binsize,
                lower_bound_mag=Model.lower_bound_mag,
                upper_bound_mag=Model.upper_bound_mag,
                lack_indicator=Model.lack_indicator):
    """

    """
    binned_SED = []
    for i, mag in enumerate(SED_mag):
        lower, upper = lower_bound_mag[i], upper_bound_mag[i]
        if not ((mag > upper) or (mag < lower)):
            binned_SED.append(np.rint((mag - lower) / binsize))
        else:
            print("bright/faint object found ... np.nan is assigned")
            binned_SED.append(lack_indicator)
    return np.array(binned_SED, dtype=int)


def along_same_axis_flag(lower_bound, binned_SED, axis_dir_vector):
    """

    """
    projected_binned_SED = binned_SED - (binned_SED[0] -
                                         lower_bound[0]) * axis_dir_vector
    # print(projected_binned_SED)
    is_along_same_axis = False
    if np.all(projected_binned_SED == lower_bound):
        is_along_same_axis = True
    return is_along_same_axis


def decompose_separation_to_nearest_bound(bound_array,
                                          binned_SED,
                                          axis_dir_vector,
                                          return_lower_flag=False):
    """

    """
    rel_sep_orthojection_list = []

    rel_sep_orthojection_vector_list, rel_radius_list = [], []
    for bound in bound_array:
        # Vector
        rel_sep_vector = bound - binned_SED
        rel_sep_orthojection_vector = (
            np.dot(rel_sep_vector, axis_dir_vector) /
            np.dot(axis_dir_vector, axis_dir_vector)) * axis_dir_vector
        rel_radial_vector = (rel_sep_vector - rel_sep_orthojection_vector)
        rel_sep_orthojection_vector_list.append(rel_sep_orthojection_vector)

        # Scalar length
        rel_radius = np.dot(rel_radial_vector, rel_radial_vector)**0.5
        rel_radius_list.append(rel_radius)
        rel_sep_orthojection = np.dot(rel_sep_orthojection_vector,
                                      rel_sep_orthojection_vector)**0.5
        rel_sep_orthojection_list.append(rel_sep_orthojection)

    # List to array
    rel_radius_array = np.array(rel_radius_list)
    rel_sep_orthojection_vector_array = np.array(
        rel_sep_orthojection_vector_list)

    # Find nearest bound
    rel_radius_nearest_array = rel_radius_array[rel_radius_array == np.min(
        rel_radius_array)]
    rel_sep_orthojection_vector_nearest_array = rel_sep_orthojection_vector_array[
        rel_radius_array == np.min(rel_radius_array)]
    nearest_array = rel_sep_orthojection_vector_nearest_array[:, 0]

    # Conservative way: if any nearest SEDs is upper than bound, object -> galaxy
    if np.any(nearest_array <= 0.):
        is_lower = False
        nearest_index = np.argwhere(
            nearest_array == np.max(nearest_array[nearest_array <= 0.]))[0][0]
        nearest_rel_radius = rel_radius_nearest_array[nearest_index]
        nearest_sep_orthojection_vector = rel_sep_orthojection_vector_nearest_array[
            nearest_index]
        nearest_sep_orthojection = -np.dot(
            nearest_sep_orthojection_vector,
            nearest_sep_orthojection_vector)**0.5
    else:
        is_lower = True
        nearest_index = np.argwhere(
            nearest_array == np.min(nearest_array[nearest_array > 0.]))[0][0]
        nearest_rel_radius = rel_radius_nearest_array[nearest_index]
        nearest_sep_orthojection_vector = rel_sep_orthojection_vector_nearest_array[
            nearest_index]
        nearest_sep_orthojection = np.dot(nearest_sep_orthojection_vector,
                                          nearest_sep_orthojection_vector)**0.5

    # Return
    if return_lower_flag:
        return nearest_rel_radius, nearest_sep_orthojection, is_lower
    else:
        return nearest_rel_radius, nearest_sep_orthojection


def within_bounds_flag(binned_SED, lower_bound, upper_bound):
    """

    """
    is_within_bounds = False
    if np.all(binned_SED >= lower_bound) and np.all(binned_SED <= upper_bound):
        is_within_bounds = True
    return is_within_bounds


def lower_than_lower_bound_flag(binned_SED, lower_bound, upper_bound):
    """

    """
    is_lower_than_lower_bound = False
    if np.all(binned_SED < lower_bound):
        is_lower_than_lower_bound = True
    return is_lower_than_lower_bound


def star_flag(binned_SED,
              star_lower_bound_array,
              star_upper_bound_array,
              criteria='within_bounds',
              axis_dir_vector=Model.axis_dir_vector,
              return_isolated_flag=False):
    """

    """
    is_star, is_isolated = False, True
    for lower_bound, upper_bound in zip(star_lower_bound_array,
                                        star_upper_bound_array):
        if along_same_axis_flag(lower_bound, binned_SED, axis_dir_vector):
            is_isolated = False
            if criteria == 'within_bounds':
                if within_bounds_flag(binned_SED, lower_bound, upper_bound):
                    is_star = True
            elif criteria == 'above_lower_bound':
                if not lower_than_lower_bound_flag(binned_SED, lower_bound,
                                                   upper_bound):
                    is_star = True
    if return_isolated_flag:
        return is_star, is_isolated
    else:
        return is_star


def galaxy_flag(binned_SED,
                galaxy_lower_bound_array,
                galaxy_upper_bound_array,
                criteria='above_lower_bound',
                axis_dir_vector=Model.axis_dir_vector,
                return_isolated_flag=False):
    """

    """
    is_galaxy, is_isolated = False, True
    for lower_bound, upper_bound in zip(galaxy_lower_bound_array,
                                        galaxy_upper_bound_array):
        if along_same_axis_flag(lower_bound, binned_SED, axis_dir_vector):
            is_isolated = False
            if criteria == 'within_bounds':
                if within_bounds_flag(binned_SED, lower_bound, upper_bound):
                    is_galaxy = True
            elif criteria == 'above_lower_bound':
                if not lower_than_lower_bound_flag(binned_SED, lower_bound,
                                                   upper_bound):
                    is_galaxy = True

    if return_isolated_flag:
        return is_galaxy, is_isolated
    else:
        return is_galaxy

#!/usr/bin/env python
# -*- coding:utf-8 -*-

# ############################################################################
# :Author: Kuan-Hsien Wu
# :Email: jordankhwu@gapp.nthu.edu.tw
# :Date: 2022-01-16
# :Description: This code is to probe boundary of photometry catalog by
#               projecting object in N-d magnitude space to N-1-d magnitude
#               space along axis parallel to diagonal line.
# ############################################################################

import sys
from os import path, system

import numpy as np


def draw_progress_bar(percent, bar_len=50):
    """
    draw progress bar
    """
    # percent float from 0 to 1.
    sys.stdout.write("\r")
    sys.stdout.write("[{:<{}}] {:.3f}%".format("=" * int(bar_len * percent),
                                               bar_len, (percent * 100)))
    sys.stdout.flush()


def calculate_shape_of_grid_mag_space(
        binsize,
        lower_bound_mag=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        upper_bound_mag=[19.0, 18.0, 18.0, 17.0, 17.0, 17.0, 17.0, 15.0],
        verbose=False):
    """

    """
    assert (len(lower_bound_mag) == len(upper_bound_mag)
            ), 'length of input lower bound and upper bound must be the same'
    shape = []
    for lower, upper in zip(lower_bound_mag, upper_bound_mag):
        shape.append(int(round((upper - lower) / binsize)) + 1)
    shape = np.array(shape)
    if verbose:
        print(
            "Information about magnitude space ================================="
        )
        print('Binsize: {:.1f} mag'.format(binsize))
        print('Lower bound (mag):', lower_bound_mag)
        print('Upper_bound (mag):', upper_bound_mag)
        print("Shape of nD space (number of axis points)", shape)
        print(
            "===================================================================\n"
        )
    return shape


def grid_object_array_in_1D(object_array,
                            lower,
                            upper,
                            binsize,
                            lower_indicator=-9999,
                            upper_indicator=9999):
    """

    """
    grid_object_array = np.empty_like(object_array, dtype=int)
    for i, obj in enumerate(object_array):
        if obj > upper:
            grid_object_array[i] = upper_indicator
        elif obj < lower:
            grid_object_array[i] = lower_indicator
        else:
            grid_object_array[i] = np.rint((obj - lower) / binsize)
    return grid_object_array


def filter_bright_faint(grid_array,
                        mag_array,
                        bright_indicator=-9999,
                        faint_indicator=9999):
    """

    """
    grid_no_bright_faint = []
    mag_no_bright_faint = []
    for grid, mag in zip(grid_array, mag_array):
        if (bright_indicator not in grid) and (faint_indicator not in grid):
            grid_no_bright_faint.append(grid)
            mag_no_bright_faint.append(mag)
    grid_no_bright_faint_array = np.array(grid_no_bright_faint)
    mag_no_bright_faint_array = np.array(mag_no_bright_faint)
    return grid_no_bright_faint_array, mag_no_bright_faint_array


def grid_object_in_mag_space(
        mag_array,
        binsize,
        lower_bound_mag=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        upper_bound_mag=[19.0, 18.0, 18.0, 17.0, 17.0, 17.0, 17.0, 15.0],
        lower_indicator=-9999,
        upper_indicator=9999):
    """

    """
    grid_object_array_in_mag_space = []
    for i, mag in enumerate(mag_array.T):
        grid_object_array_in_mag_space.append(
            grid_object_array_in_1D(mag,
                                    lower_bound_mag[i],
                                    upper_bound_mag[i],
                                    binsize,
                                    lower_indicator=lower_indicator,
                                    upper_indicator=upper_indicator))
    grid_object_array_in_mag_space = np.array(grid_object_array_in_mag_space).T
    return grid_object_array_in_mag_space


def sort_input_array(input_array):
    """

    """
    input_array_t = np.transpose(input_array)
    sorted_index_array = np.lexsort(tuple(input_array_t))
    sorted_input_array = input_array[sorted_index_array]
    return sorted_index_array, sorted_input_array


def count_object_in_grid(grid_array, mag_array, verbose=False):
    """

    """
    print(grid_array)
    sorted_index_array, sorted_grid_array = sort_input_array(grid_array)
    sorted_mag_array = mag_array[sorted_index_array]
    grid_dict = dict()
    if verbose: print('Count object in grid (binning process) ...')
    for i, (grid, mag) in enumerate(zip(sorted_grid_array, sorted_mag_array)):
        if verbose:
            draw_progress_bar(float(i + 1) / len(grid_array))
        grid = tuple(grid)
        if grid in grid_dict.keys():
            grid_dict[grid].append(mag)
        else:
            grid_dict[grid] = mag
            grid_dict[grid] = [grid_dict[grid]]
    if verbose: print()
    return grid_dict


def project_to_plane_in_grid(grid_dict,
                             project_axis_vector=np.ones(8, dtype=int),
                             plane_ax_id=0,
                             verbose=False):
    """

    """
    projected_dict = dict()
    if verbose:
        print(
            'Project binned data to plane along axis (projection  process) ...'
        )
    for i, (key, _) in enumerate(grid_dict.items()):
        if verbose:
            draw_progress_bar(float(i + 1) / len(grid_dict.keys()))
        projected_key = np.array(key) - key[plane_ax_id] * project_axis_vector
        projected_key = tuple(projected_key)
        if projected_key in projected_dict.keys():
            projected_dict[projected_key].append(np.array(key))
        else:
            projected_dict[projected_key] = np.array(key)
            projected_dict[projected_key] = [projected_dict[projected_key]]
    if verbose: print()
    return projected_dict


def find_bound_in_grid_mag_space(projected_dict, grid_dict, verbose=False):
    """

    """
    lower_bound_dict, upper_bound_dict = dict(), dict()
    if verbose: print('Find boundary in binned magnitude space ...')
    for i, (key, value) in enumerate(projected_dict.items()):
        if verbose:
            draw_progress_bar(float(i + 1) / len(projected_dict.keys()))
        lower_bound_key, upper_bound_key = tuple(value[0]), tuple(value[-1])
        upper_bound_dict[upper_bound_key] = grid_dict[upper_bound_key]
        lower_bound_dict[lower_bound_key] = grid_dict[lower_bound_key]
    if verbose: print()
    return lower_bound_dict, upper_bound_dict


def get_populated_regions_with_bounds(lower_bounds, upper_bounds):
    """

    """
    populated_regions = []
    for lower_bound, upper_bound in zip(lower_bounds, upper_bounds):
        if lower_bound == upper_bound:
            populated_regions.append(np.array(lower_bound, dtype=int))
        else:
            for i in range(upper_bound[0] - lower_bound[0] + 1):
                populated_region = np.array(
                    lower_bound,
                    dtype=int) + i * np.ones(len(lower_bound), dtype=int)
                populated_regions.append(populated_region)
    return populated_regions


def save_output(output_list,
                common_name,
                binsize,
                out_dir='./',
                suffix_list=[
                    'grid', 'projected_grid', 'lower_bound', 'upper_bound',
                    'filled_bounds_grid'
                ]):
    """

    """
    assert len(output_list) == len(
        suffix_list), 'length of output_list and suffix_list must be the same'

    if not path.isdir(out_dir):
        system('mkdir -p {}'.format(out_dir))

    for i, suffix in enumerate(suffix_list):
        filename = '{}_bin{:.1f}_{}.npy'.format(common_name, binsize, suffix)
        np.save('{}/{}'.format(out_dir, filename), output_list[i])


def probe_sample_and_generate_populated_region_grid_dicts(
        binsize,
        output_dir="./",
        input_catalog_list=[],
        input_name_list=[],
        lower_bound_mag=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        upper_bound_mag=[19.0, 18.0, 18.0, 17.0, 17.0, 17.0, 17.0, 15.0],
        project_axis_vector=np.ones(8, dtype=int),
        lower_indicator=-9999,
        upper_indicator=9999,
        lack_indicator=-999.,
        verbose=False):
    """

    """
    shape = calculate_shape_of_grid_mag_space(binsize, verbose=True)
    for input_catalog, input_name in zip(input_catalog_list, input_name_list):
        print("{}: {}\n".format(input_name, input_catalog))
        mag_array = np.loadtxt(input_catalog, ndmin-2)
        mag_array[mag_array == lack_indicator] = 0.

        # Grid in magnitude space
        grid_in_mag_space = grid_object_in_mag_space(
            mag_array,
            binsize,
            lower_bound_mag=lower_bound_mag,
            upper_bound_mag=upper_bound_mag)

        # Filter out sources outside grid space
        filtered_grid, filtered_mag = filter_bright_faint(
            grid_in_mag_space,
            mag_array,
            bright_indicator=lower_indicator,
            faint_indicator=upper_indicator)

        # Count objects within single grid
        grid_dict = count_object_in_grid(filtered_grid,
                                         filtered_mag,
                                         verbose=verbose)

        # Project
        projected_dict = project_to_plane_in_grid(
            grid_dict, project_axis_vector=project_axis_vector, verbose=verbose)

        # Find boundary of populated region
        lower_bound_dict, upper_bound_dict = find_bound_in_grid_mag_space(
            projected_dict, grid_dict, verbose=verbose)

        # Fill region between boundaries
        filled_grid_array = get_populated_regions_with_bounds(
            lower_bound_dict, upper_bound_dict)

        # Save all dictionaries
        output_list = [
            grid_dict, projected_dict, lower_bound_dict, upper_bound_dict,
            filled_grid_array
        ]
        save_output(output_list, input_name, binsize, out_dir=output_dir)
        if verbose: print()


def main():
    """  """
    # Catalogs
    output_dir = './test'
    input_dir = '../tables'
    input_catalog_list = [
        '{}/evolved_star_SED_mag.txt'.format(input_dir),
    ]
    input_name_list = ['evolved_star']
    binsize_list = [1.0]
    for binsize in binsize_list:
        print()
        probe_sample_and_generate_populated_region_grid_dicts(
            binsize,
            output_dir=output_dir,
            input_catalog_list=input_catalog_list,
            input_name_list=input_name_list,
            verbose=True)


if __name__ == '__main__':
    main()

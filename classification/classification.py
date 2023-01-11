#!/usr/bin/env python

import sys

import numpy as np

from classifiers import (HL_AGB_star_flag, bin_SED_mag, bright_flag,
                         decompose_separation_to_nearest_bound,
                         evolved_star_flag, faint_flag, galaxy_flag, star_flag)

sys.path.append('../')
from model import Model


def draw_progress_bar(percent, barLen=50):
    """
    draw progress bar
    """
    # percent float from 0 to 1.
    sys.stdout.write("\r")
    sys.stdout.write("[{:<{}}] {:.3f}%".format("=" * int(barLen * percent),
                                               barLen, (percent * 100)))
    sys.stdout.flush()


def pipeline(
    SED_mag_array,
    model,
    min_no_lack=3,
    multiple_labels=False,
    decomposition=True,
    evolved_star_flag_model='HL_AGB_star',
    evolved_star_criteria='within_bounds',
    star_criteria='within_bounds',
    galaxy_criteria='above_lower_bound',
    band_mask='0,0,0,0,0,0,0,0',
    classifier_mask='0,0,0,0,0,0',
    PSF_mask=False,
    PSF_array=None,
):
    """

    """
    result_list = []
    unknown_ID_list, bright_ID_list, faint_ID_list = [], [], []
    evolved_star_ID_list, star_ID_list = [], []
    YSO_ID_list, galaxy_ID_list, isolated_ID_list = [], [], []
    if model.do_reclassify:
        non_rc_isolated_ID_list = []
        rc_YSO_ID_list, rc_galaxy_ID_list = [], []
        non_rc_YSO_ID_list, non_rc_galaxy_ID_list = [], []

    # Load masks
    band_mask_array = np.array(band_mask.split(','), dtype=int)
    classifier_mask_array = np.array(classifier_mask.split(','), dtype=int)

    print('\n# of input SED: {:d}'.format(len(SED_mag_array)))
    for i, SED_mag in enumerate(SED_mag_array):
        draw_progress_bar(float(i + 1) / len(SED_mag_array))

        # Band mask (mask input band)
        band_mask_classifier = np.where(band_mask_array == 1)[0]
        SED_mag[band_mask_classifier] = Model.lack_indicator

        # PSF_mask (mask input band with imtype (PSF qualifier))
        if PSF_mask and (PSF_array is not None):
            non_im1_mask = np.where(PSF_array[i] != 1)[0] + 2
            SED_mag[non_im1_mask] = Model.lack_indicator

        # Find and record lack band
        non_lack_index_array = np.where(SED_mag != Model.lack_indicator)[0]
        objectband = np.array(['0'] * len(SED_mag))
        objectband[non_lack_index_array] = '1'
        result = ','.join(objectband) + '\t'

        # Num of no lack band < min_no_lack -> unknown
        if len(non_lack_index_array) < min_no_lack:
            objecttype = 'unknown'
            unknown_ID_list.append(i)
            result += '{}'.format(objecttype)
            result_list.append(result)
            continue

        # Mask boundary lack-band component
        SED_mag_no_lack = SED_mag[non_lack_index_array]
        axis_dir_vector = np.ones(len(SED_mag_no_lack), dtype=int)
        lower_bound_mag_no_lack = model.lower_bound_mag[non_lack_index_array]
        upper_bound_mag_no_lack = model.upper_bound_mag[non_lack_index_array]
        galaxy_lower_bound_no_lack_array = model.galaxy_lower_bound_array[:,
                                                                          non_lack_index_array]
        galaxy_upper_bound_no_lack_array = model.galaxy_upper_bound_array[:,
                                                                          non_lack_index_array]
        star_lower_bound_no_lack_array = model.star_lower_bound_array[:,
                                                                      non_lack_index_array]
        star_upper_bound_no_lack_array = model.star_upper_bound_array[:,
                                                                      non_lack_index_array]
        if (evolved_star_flag_model != 'HL_AGB_star') and (
                model.evolved_star_lower_bound_array
                is not None) and (model.evolved_star_upper_bound_array
                                  is not None):
            evolved_star_lower_bound_no_lack_array = model.evolved_star_lower_bound_array[:,
                                                                                          non_lack_index_array]
            evolved_star_upper_bound_no_lack_array = model.evolved_star_upper_bound_array[:,
                                                                                          non_lack_index_array]

        # Faint classifier
        if (classifier_mask_array[1] != 1) and faint_flag(
                SED_mag_no_lack, upper_bound_mag=upper_bound_mag_no_lack):
            objecttype = 'faint'
            faint_ID_list.append(i)
            result += '{}'.format(objecttype)
            result_list.append(result)
            if not multiple_labels:
                continue

        # Bright classifier
        if (classifier_mask_array[0] != 1) and bright_flag(
                SED_mag_no_lack, lower_bound_mag=lower_bound_mag_no_lack):
            objecttype = 'bright'
            bright_ID_list.append(i)
            result += '{}'.format(objecttype)
            result_list.append(result)
            if not multiple_labels:
                continue

        # Bin SED
        binned_SED_no_lack = bin_SED_mag(SED_mag_no_lack, model.binsize)

        # Evolved star lassifier
        if classifier_mask_array[2] != 1:
            if evolved_star_flag_model == 'HL_AGB_star':
                if (model.IR2_ID in non_lack_index_array) and (
                        model.IR3_ID
                        in non_lack_index_array) and (model.MP1_ID
                                                      in non_lack_index_array):
                    if HL_AGB_star_flag(SED_mag):
                        objecttype = 'evolved_star'
                        evolved_star_ID_list.append(i)
                        result += '{}'.format(objecttype)
                        result_list.append(result)
                        if not multiple_labels:
                            continue
            else:
                if evolved_star_flag(binned_SED_no_lack,
                                     evolved_star_lower_bound_no_lack_array,
                                     evolved_star_upper_bound_no_lack_array,
                                     criteria=evolved_star_criteria,
                                     axis_dir_vector=axis_dir_vector,
                                     return_isolated_flag=False):
                    objecttype = 'evolved_star'
                    evolved_star_ID_list.append(i)
                    result += '{}'.format(objecttype)
                    result_list.append(result)
                    if not multiple_labels:
                        continue

        # Star classifier
        is_star = star_flag(binned_SED_no_lack,
                            star_lower_bound_no_lack_array,
                            star_upper_bound_no_lack_array,
                            criteria=star_criteria,
                            axis_dir_vector=axis_dir_vector,
                            return_isolated_flag=False)
        if (classifier_mask_array[3] != 1) and is_star:
            objecttype = 'star'
            star_ID_list.append(i)
            result += '{}'.format(objecttype)
            result_list.append(result)
            if not multiple_labels:
                continue

        # Decomposition object separation to nearest lower_boundary
        if decomposition or model.do_reclassify:
            radius, orthojection, is_lower = decompose_separation_to_nearest_bound(
                galaxy_lower_bound_no_lack_array,
                binned_SED_no_lack,
                axis_dir_vector,
                return_lower_flag=True)

        # Galaxy classifier
        is_galaxy, is_isolated = galaxy_flag(binned_SED_no_lack,
                                             galaxy_lower_bound_no_lack_array,
                                             galaxy_upper_bound_no_lack_array,
                                             criteria=galaxy_criteria,
                                             axis_dir_vector=axis_dir_vector,
                                             return_isolated_flag=True)
        if (classifier_mask_array[4] != 1) and is_galaxy:
            objecttype = 'galaxy'
            galaxy_ID_list.append(i)
            if model.do_reclassify:
                non_rc_galaxy_ID_list.append(i)
            result += '{}_RR_{:.1f}_RH_{:.1f}'.format(objecttype, radius,
                                                      orthojection)
            result_list.append(result)
            if not multiple_labels:
                continue

        # Isolated classifier, reclassification operator
        if (classifier_mask_array[5] !=
                1) and is_isolated and model.do_reclassify:
            # Isolated before reclassification
            non_rc_isolated_ID_list.append(i)
            if is_lower:
                # YSO after reclassification
                objecttype = 'YSO'
                YSO_ID_list.append(i)
                if model.do_reclassify:
                    rc_YSO_ID_list.append(i)
                result += 'RC{}_RR_{:.1f}_RH_{:.1f}'.format(
                    objecttype, radius, orthojection)
                result_list.append(result)
                if not multiple_labels:
                    continue
            else:
                # Galaxy after reclassification
                objecttype = 'galaxy'
                galaxy_ID_list.append(i)
                rc_galaxy_ID_list.append(i)
                result += 'RC{}_RR_{:.1f}_RH_{:.1f}'.format(
                    objecttype, radius, orthojection)
                result_list.append(result)
                if not multiple_labels:
                    continue
        elif (classifier_mask_array[5] !=
              1) and is_isolated and (not model.do_reclassify):
            # Isolated W/O reclassification process
            objecttype = 'isolated'
            isolated_ID_list.append(i)
            result += '{}_RR_{:.1f}_RH_{:.1f}'.format(objecttype, radius,
                                                      orthojection)
            result_list.append(result)
            if not multiple_labels:
                continue
        else:
            # If not types above -> YSO
            objecttype = 'YSO'
            YSO_ID_list.append(i)
            if model.do_reclassify:
                non_rc_YSO_ID_list.append(i)
            result += '{}_RR_{:.1f}_RH_{:.1f}'.format(objecttype, radius,
                                                      orthojection)
            result_list.append(result)
            if not multiple_labels:
                continue

    objecttype_ID_dict = dict()
    objecttype_ID_dict['unknown'] = unknown_ID_list
    objecttype_ID_dict['evolved_star'] = evolved_star_ID_list
    objecttype_ID_dict['faint'] = faint_ID_list
    objecttype_ID_dict['bright'] = bright_ID_list
    objecttype_ID_dict['star'] = star_ID_list
    objecttype_ID_dict['galaxy'] = galaxy_ID_list
    objecttype_ID_dict['YSO'] = YSO_ID_list
    objecttype_ID_dict['isolated'] = isolated_ID_list
    if model.do_reclassify:
        objecttype_ID_dict['rc_galaxy'] = rc_galaxy_ID_list
        objecttype_ID_dict['rc_YSO'] = rc_YSO_ID_list
        objecttype_ID_dict['non_rc_galaxy'] = non_rc_galaxy_ID_list
        objecttype_ID_dict['non_rc_YSO'] = non_rc_YSO_ID_list
        objecttype_ID_dict['non_rc_isolated'] = non_rc_isolated_ID_list
    return result_list, objecttype_ID_dict


def analyze_objecttype(objecttype_ID_dict, WI_RC=True):
    """

    """
    print('\n# of unknown: {:d}'.format(len(objecttype_ID_dict['unknown'])))
    print('# of evolved star: {:d}'.format(
        len(objecttype_ID_dict['evolved_star'])))
    print('# of faint: {:d}'.format(len(objecttype_ID_dict['faint'])))
    print('# of bright: {:d}'.format(len(objecttype_ID_dict['bright'])))
    print('# of star: {:d}'.format(len(objecttype_ID_dict['star'])))
    print('# of galaxy: {:d}'.format(len(objecttype_ID_dict['galaxy'])))
    if WI_RC:
        print('\t# of rc_galaxy: {:d}'.format(
            len(objecttype_ID_dict['rc_galaxy'])))
        print('\t# of non_rc_galaxy: {:d}'.format(
            len(objecttype_ID_dict['non_rc_galaxy'])))
    print('# of YSO: {:d}'.format(len(objecttype_ID_dict['YSO'])))
    if WI_RC:
        print('\t# of rc_YSO: {:d}'.format(len(objecttype_ID_dict['rc_YSO'])))
        print('\t# of non_rc_YSO: {:d}'.format(
            len(objecttype_ID_dict['non_rc_YSO'])))
    if WI_RC:
        print('# of non_rc_isolated: {:d}'.format(
            len(objecttype_ID_dict['non_rc_isolated'])))
    else:
        print('# of isolated: {:d}'.format(len(
            objecttype_ID_dict['isolated'])))


def save_objecttype_index(objecttype_ID_dict, out_dir='./'):
    """

    """
    for name, ID_list in objecttype_ID_dict.items():
        ID_array = np.array(ID_list, dtype=int)
        np.savetxt('{}/{}-ID.txt'.format(out_dir, name), ID_array, fmt='%d')


def save_objecttype_SED_mag(SED_mag_array, objecttype_ID_dict, out_dir='./'):
    """

    """
    for name, ID_list in objecttype_ID_dict.items():
        ID_array = np.array(ID_list, dtype=int)
        cut_SED_mag_array = SED_mag_array[ID_array]
        np.savetxt('{}/{}-SED_mag.txt'.format(out_dir, name),
                   cut_SED_mag_array)


def save_classification_result(result_list, out_dir='./'):
    """

    """
    result_array = np.array(result_list, dtype=str)
    np.savetxt('{}/classification_result.txt'.format(out_dir),
               result_array,
               fmt='%s')


def main():
    """ """
    # Model
    evolved_star_lower_bound_dict = '../models/evolved_star_bin1.0_lower_bound.npy'
    evolved_star_upper_bound_dict = '../models/evolved_star_bin1.0_upper_bound.npy'
    star_lower_bound_dict = '../models/star_bin1.0_lower_bound.npy'
    star_upper_bound_dict = '../models/star_bin1.0_upper_bound.npy'
    galaxy_lower_bound_dict = '../models/galaxy_bin1.0_lower_bound.npy'
    galaxy_upper_bound_dict = '../models/galaxy_bin1.0_upper_bound.npy'
    model = Model(evolved_star_lower_bound_dict, evolved_star_upper_bound_dict,
                  star_lower_bound_dict, star_upper_bound_dict,
                  galaxy_lower_bound_dict, galaxy_upper_bound_dict)

    # Classification
    out_dir = './test/classification/'
    model.binsize = 1.0
    model.do_reclassify = True
    SED_mag_array = np.loadtxt('../tables/C2D_HREL-ALL-SED_mag_exXU.txt',
                               dtype=float,
                               ndmin=2)[:, :8]
    result_list, objecttype_ID_dict = pipeline(
        SED_mag_array,
        model,
        evolved_star_flag_model='not_HL_AGB_star',
        band_mask='0,0,0,0,0,0,0,0')
    analyze_objecttype(objecttype_ID_dict)
    save_objecttype_index(objecttype_ID_dict, out_dir=out_dir)
    save_objecttype_SED_mag(SED_mag_array, objecttype_ID_dict, out_dir=out_dir)
    save_classification_result(result_list, out_dir=out_dir)


if __name__ == '__main__':
    main()

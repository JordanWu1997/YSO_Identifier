#!/usr/bin/env python

import os
import sys
from os.path import basename as bn

import numpy as np

from classification import (analyze_objecttype, pipeline,
                            save_classification_result, save_objecttype_index,
                            save_objecttype_SED_mag)

sys.path.append('../')
from model import Model


def create_output_dir(out_dir):
    """

    """
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    else:
        print('{} dir exists, use existed one'.format(out_dir))


def generate_input_list(catalog_list,
                        galaxy_model_list,
                        star_model_list,
                        evolved_star_model_list,
                        binsize_model_list,
                        output_par_dir='./results'):
    """

    """
    input_SED_mag_txt_list = []
    evolved_star_lower_bound_dict_list = []
    evolved_star_upper_bound_dict_list = []
    evolved_star_flag_model_list = []
    star_lower_bound_dict_list = []
    star_upper_bound_dict_list = []
    galaxy_lower_bound_dict_list = []
    galaxy_upper_bound_dict_list = []
    binsize_list = []
    out_dir_list = []
    for binsize in binsize_model_list:
        for catalog in catalog_list:
            for galaxy_model in galaxy_model_list:
                for star_model in star_model_list:
                    for evolved_star_model in evolved_star_model_list:
                        # evolved star model
                        if evolved_star_model != 'HL_AGB_star':
                            evolved_star_flag_model_list.append(
                                'not_HL_AGB_star')
                            evolved_star_lower_bound_dict_list.append(
                                '{}_bin{:.1f}_lower_bound.npy'.format(
                                    evolved_star_model, binsize))
                            evolved_star_upper_bound_dict_list.append(
                                '{}_bin{:.1f}_upper_bound.npy'.format(
                                    evolved_star_model, binsize))
                            out_dir = '{}/{}/result_model_{}_{}_{}_bin{:.1f}'.format(
                                output_par_dir,
                                bn(catalog).strip('.txt'),
                                bn(evolved_star_model), bn(star_model),
                                bn(galaxy_model), binsize)
                        else:
                            evolved_star_flag_model_list.append('HL_AGB_star')
                            evolved_star_lower_bound_dict_list.append(None)
                            evolved_star_upper_bound_dict_list.append(None)
                            out_dir = '{}/{}/result_model_{}_{}_bin{:.1f}'.format(
                                output_par_dir,
                                bn(catalog).strip('.txt'), bn(star_model),
                                bn(galaxy_model), binsize)

                        star_lower_bound_dict_list.append(
                            '{}_bin{:.1f}_lower_bound.npy'.format(
                                star_model, binsize))
                        star_upper_bound_dict_list.append(
                            '{}_bin{:.1f}_upper_bound.npy'.format(
                                star_model, binsize))
                        galaxy_lower_bound_dict_list.append(
                            '{}_bin{:.1f}_lower_bound.npy'.format(
                                galaxy_model, binsize))
                        galaxy_upper_bound_dict_list.append(
                            '{}_bin{:.1f}_upper_bound.npy'.format(
                                galaxy_model, binsize))
                        input_SED_mag_txt_list.append(catalog)
                        binsize_list.append(binsize)
                        out_dir_list.append(out_dir)

    input_lists = [
        input_SED_mag_txt_list, evolved_star_flag_model_list,
        evolved_star_lower_bound_dict_list, evolved_star_upper_bound_dict_list,
        star_lower_bound_dict_list, star_upper_bound_dict_list,
        galaxy_lower_bound_dict_list, galaxy_upper_bound_dict_list,
        binsize_list, out_dir_list
    ]
    return input_lists


def run_classification(input_SED_mag_txt,
                       evolved_star_lower_bound_dict,
                       evolved_star_upper_bound_dict,
                       star_lower_bound_dict,
                       star_upper_bound_dict,
                       galaxy_lower_bound_dict,
                       galaxy_upper_bound_dict,
                       binsize,
                       out_dir='./',
                       min_no_lack=3,
                       evolved_star_flag_model='HL_evolved_star',
                       evolved_star_criteria='within_bounds',
                       star_criteria='within_bounds',
                       galaxy_criteria='above_lower_bound',
                       PSF_mask=False,
                       PSF_array=None,
                       classifier_mask='0,0,0,0,0,0',
                       do_reclassify=True):
    """
    """
    models = Model(evolved_star_lower_bound_dict,
                   evolved_star_upper_bound_dict, star_lower_bound_dict,
                   star_upper_bound_dict, galaxy_lower_bound_dict,
                   galaxy_upper_bound_dict)
    models.binsize = binsize
    models.do_reclassify = do_reclassify
    SED_mag_array = np.loadtxt(input_SED_mag_txt, dtype=float)[:, :8]
    result_list, objecttype_ID_dict = pipeline(
        SED_mag_array,
        models,
        min_no_lack=min_no_lack,
        evolved_star_flag_model=evolved_star_flag_model,
        evolved_star_criteria=evolved_star_criteria,
        star_criteria=star_criteria,
        galaxy_criteria=galaxy_criteria,
        PSF_mask=PSF_mask,
        PSF_array=PSF_array,
        classifier_mask=classifier_mask)
    analyze_objecttype(objecttype_ID_dict)
    save_objecttype_index(objecttype_ID_dict, out_dir=out_dir)
    save_objecttype_SED_mag(SED_mag_array, objecttype_ID_dict, out_dir=out_dir)
    save_classification_result(result_list, out_dir=out_dir)


def main():
    """ """
    input_SED_mag_txt_list = [
        '../tables/C2D_HREL-ALL-SED_mag_exXU.txt',
    ]
    evolved_star_lower_bound_dict_list = [
        '../models/evolved_star_bin1.0_lower_bound.npy',
    ]
    evolved_star_upper_bound_dict_list = [
        '../models/evolved_star_bin1.0_upper_bound.npy',
    ]
    star_lower_bound_dict_list = [
        '../models/star_bin1.0_lower_bound.npy',
    ]
    star_upper_bound_dict_list = [
        '../models/star_bin1.0_upper_bound.npy',
    ]
    galaxy_lower_bound_dict_list = [
        '../models/galaxy_bin1.0_lower_bound.npy',
    ]
    galaxy_upper_bound_dict_list = [
        '../models/galaxy_bin1.0_upper_bound.npy',
    ]
    binsize_list = [
        1.0,
    ]
    out_dir_list = [
        './test/results/C2D_HREL-ALL-SED_mag_exXU/result_model_evolved_star_star_galaxy_bin1.0',
    ]

    for i, out_dir in enumerate(out_dir_list):
        print()
        print(out_dir)
        create_output_dir(out_dir)
        run_classification(
            input_SED_mag_txt_list[i],
            evolved_star_lower_bound_dict_list[i],
            evolved_star_upper_bound_dict_list[i],
            star_lower_bound_dict_list[i],
            star_upper_bound_dict_list[i],
            galaxy_lower_bound_dict_list[i],
            galaxy_upper_bound_dict_list[i],
            binsize_list[i],
            out_dir=out_dir_list[i],
            min_no_lack=3,
        )


if __name__ == '__main__':
    main()

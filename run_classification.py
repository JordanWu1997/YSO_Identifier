#!/usr/bin/env python

import sys

sys.path.append('./classification/')
from classification_pipe import (create_output_dir, generate_input_list,
                                 run_classification)


def main():
    """  """

    # Output directory
    output_dir = './results'

    # Input variables
    catalog_list = [
        './tables/C2D_HREL-ALL-SED_mag_exXU.txt',
    ]
    evolved_star_model_list = [
        './models/evolved_star',
    ]
    star_model_list = [
        './models/star',
    ]
    galaxy_model_list = ['./models/galaxy']
    binsize_model_list = [
        1.0,
    ]

    # Interactive Mode
    if (len(sys.argv) == 2) and (sys.argv[1] == 'interactive'):
        # Output directory
        output_dir = input(
            "--> Enter result output directory (Default: {}):\n--> ".format(
                output_dir)) or output_dir
        print('--> Use {}\n'.format(output_dir))
        # Input SED catalog
        catalog_list = [
            input(
                "--> Enter SED catalog for classification (Default: {}):\n--> "
                .format(catalog_list[0])) or catalog_list[0]
        ]
        print('--> Use {}\n'.format(catalog_list[0]))
        # Input evolved star model
        evolved_star_model_list = [
            input(
                "--> Enter evolved star model for classification (Default: {}):\n--> "
                .format(evolved_star_model_list[0]))
            or evolved_star_model_list[0]
        ]
        print('--> Use {}\n'.format(evolved_star_model_list[0]))
        # Input star model
        star_model_list = [
            input(
                "--> Enter star model for classification (Default: {}):\n--> ".
                format(star_model_list[0])) or star_model_list[0]
        ]
        print('--> Use {}\n'.format(star_model_list[0]))
        # Input galaxy model
        galaxy_model_list = [
            input(
                "--> Enter galaxy model for classification (Default: {}):\n--> "
                .format(galaxy_model_list[0])) or galaxy_model_list[0]
        ]
        print('--> Use {}\n'.format(galaxy_model_list[0]))
        # Input binsize
        binsize_model_list = [
            float(
                input(
                    "--> Enter binsize for model and classification (Default: {:.1f}):\n--> "
                    .format(binsize_model_list[0])) or binsize_model_list[0])
        ]
        print('--> Use {:.1f}\n'.format(binsize_model_list[0]))

    # Generate input list
    input_lists = generate_input_list(catalog_list,
                                      galaxy_model_list,
                                      star_model_list,
                                      evolved_star_model_list,
                                      binsize_model_list,
                                      output_par_dir=output_dir)
    input_SED_mag_txt_list = input_lists[0]
    evolved_star_flag_model_list = input_lists[1]
    evolved_star_lower_bound_dict_list = input_lists[2]
    evolved_star_upper_bound_dict_list = input_lists[3]
    star_lower_bound_dict_list = input_lists[4]
    star_upper_bound_dict_list = input_lists[5]
    galaxy_lower_bound_dict_list = input_lists[6]
    galaxy_upper_bound_dict_list = input_lists[7]
    binsize_list = input_lists[8]
    out_dir_list = input_lists[9]

    # Start classification
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
            evolved_star_flag_model=evolved_star_flag_model_list[i],
        )


if __name__ == "__main__":
    main()

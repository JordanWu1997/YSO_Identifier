#!/usr/bin/env bash

# Generate template star catalog
python3 ./generate_template_star.py

# Concataate C2D star catalog with PSF in MIPS1 band and template star catalog with maximal extinction 50
cat "./C2D_HREL-star_ALL-SED_mag_exXU_imtype=1.txt" "./template_star_WI_max_Av_50_SED_mag.txt" > "./star_SED_mag.txt"

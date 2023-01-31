# YSO Identifier: Identifying Young Stellar Objects in Multi-dimensional Magnitude Space

Table of Contents
=================

* [YSO Identifier: Identifying Young Stellar Objects in Multi-dimensional Magnitude Space](#yso-identifier-identifying-young-stellar-objects-in-multi-dimensional-magnitude-space)
* [Context](#context)
   * [1. Introduction](#1-introduction)
      * [1.1 YSO Identification](#11-yso-identification)
      * [1.2 How Magnitude Space Works](#12-how-magnitude-space-works)
   * [2. Method](#2-method)
      * [2.1 Find Object-populated Region](#21-find-object-populated-region)
      * [2.2 Classification Pipeline](#22-classification-pipeline)
      * [2.3 Isolated Object and Reclassification Process](#23-isolated-object-and-reclassification-process)
   * [3. TL;DR How to use this tool?](#3-tldr-how-to-use-this-tool)
      * [3.1. Preparation](#31-preparation)
         * [3.1.1. Install Required Python Packages (Python 3)](#311-install-required-python-packages-python-3)
         * [3.1.2. Prepare Sample Catalogs](#312-prepare-sample-catalogs)
         * [3.1.3. Check Parameters](#313-check-parameters)
      * [3.2 Probe Object-populated Region](#32-probe-object-populated-region)
      * [3.3 Run Classification](#33-run-classification)
         * [3.3.1. With Interactively Input Catalogs](#331-with-interactively-input-catalogs)
         * [3.3.2. With Preset Input Catalogs](#332-with-preset-input-catalogs)
      * [3.4 Visualization](#34-visualization)
         * [3.4.1 Magnitude-Magnitude Diagram (MMD)](#341-magnitude-magnitude-diagram-mmd)
         * [3.4.2 Spectral Energy Distribution (SED) in Magnitude](#342-spectral-energy-distribution-sed-in-magnitude)
         * [3.4.3 Venn Diagram for Models](#343-venn-diagram-for-models)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)

# Context

## 1. Introduction
Young Stellar Objects (YSOs) are young stars at early stage of evolution. They are consists of protostar and pre-main-sequence stars.
Identifying YSOs is important to derive statistical properties e.g. star formation rate (SFR) which helps to better constrain star formation theories.
In this work, we take the indirect approach to find YSOs by constructing a pipeline to classify astronomical objects: evolved stars, stars, galaxies, and YSOs, solely based on their photometry measurements from multiple bands.
The classification is based on object-populated regions of evolved stars, stars, and galaxies in the multi-dimensional magnitude space, and sources are classified as YSOs if they are not in the previous regions.

### 1.1 YSO Identification
There are two major approaches to do YSO identification: direct approach and indirect approach
- __Direct approach__: Find objects with feature of YSOs
    - Spectroscopy (pros: accurate; cons __NOT very efficient__)
- __Indirect approach__: Remove objects that are not YSOs
    - Evans et al. 2007: Color-color diagram (CCD), Color-magnitude diagram (CMD)
    - Hsieh and Lai 2013: Multi-D magnitude space (__this approach is adopted by this work__)
    - Chiu et al. 2021: Machine Learning

### 1.2 How Magnitude Space Works
Each location in magnitude space corresponds to a type of spectral energy distribution (SED) which can represent composition of objects.
This means classifying objects in magnitude space is equivalent to __classifying objects with SED based on their composition__.

| ![Cartoon_MMD_and_SED](./figures/Cartoon_MMD_and_SED.png)                           |
| :--:                                                                                |
| Blue/Green dots in 3D magnitude space corresponds to different types of 3-band SEDs |

For locations along the __faint direction__ (diagonal direction), SED shape of each location is identical but with different magnitude.
This can be viewed as the __same type of objects__ with different brightness due to the distance

| ![Cartoon_SED_AND_MMD_diagonal_probe](./figures/Cartoon_SED_AND_MMD_diagonal_probe.png) |
| :---:                                                                                   |
| Green dots within orange probe in faint direction can be viewed as same type of objects |

However, since YSOs and galaxies have similar composition, both are made of star and dust, we cannot simply use SED shape to separate them.
But since their distances to us are very different, most YSOs we can observe locate within Milky Way Galaxy, as most galaxies are far-away from our Milky Way Galaxy.
Therefore, we __use their brightness difference to separate them__.
Note that this method has a caveat, since the separation of YSOs and galaxies are based on brightness, we might miss __very faint YSOs__ and contaminate YSOs with __very bright galaxies__.
Fortunately, there are not so many very bright galaxies.

| ![Cartoon_SED_AND_MMD_YSO_AND_Galaxy](./figures/Cartoon_SED_AND_MMD_YSO_AND_Galaxy.png)                 |
| :--:                                                                                                    |
| Green/Blue dots within orange probe indicate Galaxies/YSOs separated due to their brightness difference |

## 2. Method
In this work, we use object samples to __naturally defined object-populated region__ in multi-D magnitude space.
The object will be classified into evolved star, star, galaxy or YSO __based on the object-populated region it locates__.
The concept of multi-D magnitude space is first proposed by Hsieh & Lai 2013, this work improves their work to the higher dimension.

| ![Multi-D_magnitude_space](./figures/Multi-D_magnitude_space.png)    |
| :--:                                                                 |
| Multi-D magnitude space in this work (2D magnitude space schematics) |

### 2.1 Find Object-populated Region
In Hsieh & Lai 2013, they use __multi-D array to construct the whole multi-D magnitude space__, however it needs enormous RAM to store that array.
To solve the RAM problem, in this work, we change the storage method from multi-d array to __2D array composed by sets of location of boundary points__.
We first project all object samples along the faint direction (as shown in previous section, they have identical SED shapes) to find all SED shapes of samples.
Then, we find __the brightest dot and the faintest dot for the individual type of SED shape__ and store them as __bright-end boundary__ and __faint-end boundary__ respectively.
In this work,  we assume object-populated region are always continuous, therefore the bright-end boundaries and faint-end boundaries define the object-populated region of the samples.
For samples used in this work, please check [./tables/README.md](./tables/README.md).

| ![Cartoon_Finding_Boundary](./figures/Cartoon_Finding_Boundary.png)                     |
| :--:                                                                                    |
| Probe green samples with orange probe and find both bright-end and faint-end boundaries |

### 2.2 Classification Pipeline
Input objects will first be __binned to save computation time__ and __compared their location in multi-D magnitude space to object-populated regions__ that are probed with the method in previous section.
Note that here we define the bright and faint regions to classify those objects outside the region of interest (where all samples locate) and give them object type bright and faint.
For those bright/faint objects, due to their brightness/faintness, we suggest them as YSOs/galaxies.
For more detailed description, please check [./classification/README.md](./classification/README.md).

| ![Cartoon_Classification_Pipeline_2D_MMD](./figures/Cartoon_Classification_Pipeline_2D_MMD.png) |
| :--:                                                                                            |
| This work classification pipeline with 2D magnitude space schematics                            |

### 2.3 Isolated Object and Reclassification Process
Since the multi-D magnitude space is huge and it is hard to observe all SED shapes in practice, there are some regions that do not have observed samples.
This region is called the __isolated region__ because of __missing SED shapes of samples__ and objects locate in this region are called __isolated objects__.

| ![Isolated_Region](./figures/Isolated_Region.png)                                                  |
| :--:                                                                                               |
| Isolated region defined in this work, which also indicates the region that we do not have samples |

To maximize usage of the samples, we introduce reclassification process to do classification to those isolated objects.
This process is to classify isolated objects using boundary points with the most similar SED as a reference.
This process acts equivalently to do interpolation/extrapolation to our samples.
Note that we only do this process to galaxy samples in this work.

| ![Reclassification_Process](./figures/Reclassification_Process.png) |
| :--:                                                                |
| Reclassification process and detailed criteria                      |

## 3. TL;DR How to use this tool?

### 3.1. Preparation

#### 3.1.1. Install Required Python Packages (Python 3)

```bash
python3 -m pip install -r ./requirements.txt
```

#### 3.1.2. Prepare Sample Catalogs
This work needs three sample catalogs for evolved stars, stars and galaxies.
We provides these three catalogs in [./tables](./tables) directory.
But note that since the size of template star catalog is too large (~120 MB) for github, we provide the scripts for user to generate template star on their own.
Also, you can just skip this section if you want to use your own sample catalogs.
For sample catalog format, please check [./tables/README.md](./tables/README.md).

```bash
cd ./tables # Make sure you are in table directory
chmod u+x ./generate_star_sample_catalog.sh
./generate_star_sample_catalog.sh
cd ..
```

#### 3.1.3. Check Parameters
Python object `Model` stores parameters for multi-dimensional magnitude space.
For more details, please check [./model.py](./model.py) file.
Use vim or whatever editor you like to check variable in `Model`.

```bash
vim ./model.py
```

### 3.2 Probe Object-populated Region
Probe object samples in multi-dimensional magnitude space to get object-populated region.
By default, we probe evolved star, star and galaxy samples with input sample catalogs in [./tables](./tables) directory with bin size `1.0`, `0.5`, `0.2` magnitude respectively.
For more details about input/output/module files, please check [./probe_model](./probe_model) directory.
Use vim or whatever editor you like to check inputs.

```bash
vim ./run_probe_model.py
```

Please check following 1D lists in `main()`, especially you are using your own sample catalogs

1. `input_catalog_list`: input catalog list for samples (e.g. evolved star, star, and galaxy)
2. `input_name_list`: input catalog name list (this would be later used as output model name)
3. `binsize_model_list`: bin size list (bin size used to probe multi-D space)

If input checking is done, run

```bash
python3 ./run_probe_model.py
```

### 3.3 Run Classification
Choose either ways to run classification.
For more details about input/output/module files, please check [./classification](./classification) directory.

#### 3.3.1. With Interactively Input Catalogs

```bash
python3 ./run_classification.py interactively
```

#### 3.3.2. With Preset Input Catalogs
Recommended if you have a lot of catalogs for classification.
But note that you have to assign models (e.g. evolved star, star, galaxy, and bin size) for every input catalog.
Use vim or whatever editor you like to check inputs.

```bash
vim ./run_classification.py
```

Please check following 1D lists in `main()` to make sure you have correct inputs, especially you are using your own models generated from your own sample catalogs.
Note that list 1~5 should have same list length.

1. `catalog_list`: input catalog list
2. `evolved_star_model_list`: evolved star model name list
3. `star_model_list`: star model name list
4. `galaxy_model_list`: galaxy model name list
5. `binsize_model_list`: bin size list

If input check is done, run

```bash
python3 ./run_classification.py
```

### 3.4 Visualization
For more details about input/output/module files, please check [./make_plot](./make_plot) directory.

#### 3.4.1 Magnitude-Magnitude Diagram (MMD)

```bash
vim ./plot_sample_MMD.py # Check input catalogs
python3 ./plot_sample_MMD.py
```
![MMD_sample](./figures/MMD_sample.png)

```bash
vim ./plot_result_MMD.py # Check input catalogs
python3 ./plot_result_MMD.py
```
![MMD_result](./figures/MMD_result.png)

#### 3.4.2 Spectral Energy Distribution (SED) in Magnitude

```bash
vim ./plot_sample_SED.py # Check input catalogs
python3 ./plot_sample_SED.py
```
![SED_this_work_sample](./figures/SED_this_work_sample.png)

#### 3.4.3 Venn Diagram for Models

```bash
vim ./plot_model_venn_diagram.py # Check input catalogs
python3 ./plot_model_venn_diagram.py
```
![VD_WO_projection](./figures/VD_WO_projection.png)
![VD_WI_projection](./figures/VD_WI_projection.png)

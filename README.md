# This Dataset

- _Your name, affiliation, and contact_
- _Brief description_
- _Anything else you like to say_

# ULTERA Database
This template repository was developed for contributing to the [**ULTERA Database**](https://ultera.org) carried under the 
[**DOE ARPA-E ULTIMATE program**](https://arpa-e.energy.gov/?q=arpa-e-programs/ultimate) that
aims to develop a new generation of materials for turbine blades in gas turbines and related
applications. 

The main scope of this dataset is collecting data on compositionally complex alloys (CCAs), also known as high entropy alloys (HEAs) and multi-principle-element alloys (MPEAs), with extra attention given to (1) high-temperature (refractory) mechanical data, (2) phases present under different processing conditions. Although low-entropy alloys (incl. binaries) are typically not presented to the end-user (or counted in statistics), some are present and used in ML efforts; thus **all high-quality alloy data contributions are welcome!**



# How to Contribute
You pretty much only need to restructure your data into a spreadsheet. **Publishing should take less than brewing a coffee.** Simply:

1. Fork this repository (button in the top-right corner). Please add a unique identifier (not belonging to any other fork) to the fork's name, i.e., ULTERA-contribute`-yourNameHere`, such as, e.g.:
   
    `-AlloyDataAMK`, `-amkrajewski`, `-10.20517-jmi.2021.05`, or `-jmi2021adetal`.
   
   Please note that on a personal GitHub account, you can only have a single fork of a repository; thus, if you want to upload data from multiple sources, it is advisable to follow one of the first two examples above. Then, you can keep each source in a separate spreadsheet.
   
3. See how the sample template is filled. The fields have short descriptions and examples above them. The `templateSampleFilled_v4.xlsx` contains some filled examples.

4. Remove the `templateSampleFilled_v4.xlsx` sample file (just to keep things neat) and rename `template_v4.xlsx` to something describing what you are uploading and that will help you remember what is inside, e.g., `refractory_bcc_heas`, `CrMoNiBased_DuctilityAndHardness`, `HardnessCollectionHEA` or, for single-publication data, the DOI `10.20517-jmi.2021.05`.

   _Avoid_ putting the version number or year in the name, as it will make correcting errors in the datasets much more difficult.


7. Fill out the spreadsheet with your data. Do not hesitate to [open an issue in this (source) repository](https://github.com/PhasesResearchLab/ULTERA-contribute/issues) in case you have any questions!

8. (optional/recommended) Enable the `Issues` page for your fork by (1) going to `Settings`, (2) scrolling down to `Features`, and (3) checking the box next to Issues. This will allow others to let you know if they find any problems with your data, or just want to ask questions.
   
9. Let us know your data is ready! We will clone your forked repository as a submodule and automatically process the data to ULTERA. 

ULTERA Data Templates Repository: [github.com/PhasesResearchLab/ULTERA-contribute](https://github.com/PhasesResearchLab/ULTERA-contribute)

## This Dataset

- _Your name, affiliation, and contact_
- _Brief description_
- _Anything else you like to say_

## ULTERA Database
This template repository was developed for contributing to the [**ULTERA Database**](https://ultera.org) carried under the 
[**DOE ARPA-E ULTIMATE program**](https://arpa-e.energy.gov/?q=arpa-e-programs/ultimate) that
aims to develop a new generation of materials for turbine blades in gas turbines and related
applications. 

The main scope of this dataset is collecting data on compositionally complex alloys (CCAs), also known as high entropy alloys (HEAs) and multi-principle-element alloys (MPEAs), with extra attention given to (1) high-temperature (refractory) mechanical data, (2) phases present under different processing conditions. Although low-entropy alloys (incl. binaries) are typically not presented to the end-user (or counted in statistics), some are present and used in ML efforts; thus **all high-quality alloy data contributions are welcome!**



## How to Contribute?
You pretty much only need to restructure your data into a spreadsheet. **Publishing should take less than brewing a coffee.** Simply:

1. Fork this repository (button in the top-right corner). Please add a unique identifier (not belonging to any other fork) to the fork's name, i.e., ULTERA-contribute`-yourNameHere`, such as, e.g.:
   
    `-AlloyDataAMK`, `-amkrajewski`, `-10.20517-jmi.2021.05`, or `-jmi2021adetal`.
   
   Please note that on a personal GitHub account, you can only have a single fork of a repository; thus, if you want to upload data from multiple sources, it is advisable to follow one of the first two examples above. Then, you can keep each source in a separate spreadsheet.
   
3. See how the sample template is filled. The fields have short descriptions and examples above them. The `templateSampleFilled_v4.xlsx` contains some filled examples.

4. Remove the `templateSampleFilled_v4.xlsx` sample file (just to keep things neat) and rename `template_v4.xlsx` to something describing what you are uploading and that will help you remember what is inside, e.g., `refractory_bcc_heas`, `CrMoNiBased_DuctilityAndHardness`, `HardnessCollectionHEA` or, for single-publication data, the DOI `10.20517-jmi.2021.05`.

   _Avoid_ putting the version number or year in the name, as it will make correcting errors in the datasets much more difficult.


7. Fill out the spreadsheet with your data. Do not hesitate to [open an issue in this (source) repository](https://github.com/PhasesResearchLab/ULTERA-contribute/issues) in case you have any questions!

8. (optional/recommended) Enable the `Issues` page for your fork by (1) going to `Settings`, (2) scrolling down to `Features`, and (3) checking the box next to Issues. This will allow others to let you know if they find any problems with your data, or just want to ask questions.
   
9. Let us know your data is ready! We will clone your forked repository as a submodule and automatically process the data into the ULTERA through [the pushing meta-repository (github.com/PhasesResearchLab/ULTERA-push)](https://github.com/PhasesResearchLab/ULTERA-push)


## I want to contribute in the future, but I'm not ready to make it public yet

Forking a repository is an elegant one-click solution to clone the templates, make your contributions discoverable, and keep everything up-to-date. One caveat is that GitHub will not allow you to change the visibility of the repository - it will have to be public. It has a number of advantages, like enabling the community to review your data and efficiently communicate issues by simply opening them on the fork; however, we know that some people may want to keep their data private until they are ready to publish it.

To create a contribution to ULTERA (or any other dataset following the template schema) you will need to _import_ the repository. You can do so by going to the `Create new...` in the top-right corner of GitHub page and selecting `Import Repository`. 

<img src="assets/images/githubimport_screenshot.png" alt="githubimport" width="200"/>

Once the page opens, paste the URL of the original repository:

      https://github.com/PhasesResearchLab/ULTERA-contribute

Then select your repository name. Please follow the `ULTERA-contribute-*******` pattern and try to make the name informative. Lastly, select the visibility you would like to have. Go forward, wait a minute, and refresh the page; you should now see your data repository!

Now, since it's not a fork, things get a bit more complex since you can't just click a button and synchronize your fork, resolving all the issues on the fly in GitHub. However, _if the modifications you make do not introduce any conflicts_ (keep up-to-date with template when introducing changes), you should be able to just add the public template repository as one of the remotes:

      git remote add public https://github.com/PhasesResearchLab/ULTERA-contribute

and then, whenever you want to make your repository up-to-date, simply pull changes from ULTERA-contribute

      git pull public main
   
and push it to yours:

      git push origin main

With that, you should be ready to store all of your data and make it public when you are ready. Then just let us know, so we can add it to [the pushing meta-repository (github.com/PhasesResearchLab/ULTERA-push)](https://github.com/PhasesResearchLab/ULTERA-push)






## The ULTERA Database
This template repository was developed for contributing to the [**ULTERA Database**](https://ultera.org) carried under the [**DOE ARPA-E ULTIMATE program**](https://arpa-e.energy.gov/?q=arpa-e-programs/ultimate) that aims to develop a new generation of materials for turbine blades in gas turbines and related applications. 

The main scope of this dataset is collecting data on compositionally complex alloys (CCAs), also known as high entropy alloys (HEAs) and multi-principle-element alloys (MPEAs), with extra attention given to (1) high-temperature (refractory) mechanical data, (2) phases present under different processing conditions. Although low-entropy alloys (incl. binaries) are typically not presented to the end-user (or counted in statistics), some are present and used in ML efforts; thus **all high-quality alloy data contributions are welcome!**

## How to Contribute?
Contributing is pretty much restructuring your data into a spreadsheet. 

Before you start:

1. Fork the [ULTERA-contribute](https://github.com/PhasesResearchLab/ULTERA-contribute/tree/main) repository, renaming your fork with a unique identifier, i.e., ULTERA-contribute`-yourUniqueIdentifier`, e.g.: `-PSU`, `-PhasesResearchLab`, `-researcherid`, etc.

2. Enable `GitHub Actions` for your fork by (1) going to `Settings > Actions (General) > Actions permissions`, (2) Select `Allow all Actions and Reusable Workflows` and save, and (3) Scroll down to `Workflow permissions`, select `Read and write permissions`, and save.

Once your forked repository is ready:

1. Make a copy of [`template_v5.xlsx`](./template_v5.xlsx) and rename it to something describing what you are uploading to help you remember what is inside, e.g., `refractory_bcc_heas.xlsx`, `CrMoNiBased_DuctilityAndHardness.xlsx`, `HardnessCollectionHEA.xlsx`. 

   PS: Keep your copied file in the root of the repository as this is the only directory monitored for new contributions.

2. Fill out your spreadsheet copy with your datapoints, folowing the ULTERA manual [`manual_v1.pdf`](./manual_v1.pdf) instructions and examples provided in the template.

3. Repeat steps 1 and 2 as necessary until you have completed adding all of your data to your repository. 

4. Once you're done, commit your changes to your repository and notify the ULTERA team by opening an issue at [ULTERA-contribute](https://github.com/PhasesResearchLab/ULTERA-contribute/issues/new?assignees=&labels=new+contribution&projects=&template=newcontribution.md&title=%5BNew+Contribution%5D). The [@PhasesResearchLab/ULTERA](https://github.com/orgs/PhasesResearchLab/teams/ULTERA) team will receive a notification of your contributions and will automatically analyze and process the data into the ULTERA database.

For further instructions on the contribution proccess or *if you want to contribute without making your data public*, please refer to [`manual_v1.pdf`](./manual_v1.pdf). 

In case you have any questions, please do not hesitate to [open an issue](https://github.com/PhasesResearchLab/ULTERA-contribute/issues) to get help!

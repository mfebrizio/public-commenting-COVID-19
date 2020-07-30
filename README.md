# public-commenting-COVID-19
Has public commenting changed during the COVID-19 pandemic? How?

This repository contains my ongoing efforts to evaluate that question, using public submissions data from the [Regulations.gov API](https://regulationsgov.github.io/developers/). Data cover the January 1, 2020 – June 30, 2020 time period and were retrieved from the API on July 13, 2020, unless otherwise noted.

As requested under the Regulations.gov API [terms of service](https://regulationsgov.github.io/developers/terms/), I offer the following disclaimer:
> Regulations.gov and the Federal government cannot verify and are not responsible for the accuracy or authenticity of the data or analyses derived from the data after the data has been retrieved from Regulations.gov.

Here is a quick overview of the organization of this repository:

- **API Retrieval**
  - This folder contains Jupyter Notebooks (written in Python) that retrieve data from the API, conduct data cleaning, and export csv files for analysis. The files focus on Environmental Protection Agency public submissions and rulemaking documents.

- **Data for Analysis**
  - This folder contains the output csv files produced from the retrieved API data. I include files with daily and monthly timeframes. I also include files, ending with filterSR, that filter out the EPA rulemaking docket, [*Strengthening Transparency in Regulatory Science*](https://www.regulations.gov/document?D=EPA-HQ-OA-2018-0259-9322), because it is a major outlier. I also include a Stata do file for graphing the results.

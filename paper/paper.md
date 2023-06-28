---
title: 'Sound-Extraction: A Python package for subsampling audio files'
tags:
  - Python
  - acoustic data
  - audio extraction and segmentation
  - sampling audio
  - bioacoutics
authors:
  - name: Prayag N. Shah
    orcid: 0009-0000-5447-7961
    affiliation: 1
  - name: Douglas P. Hynes
    orcid:
    affiliation: 1
date: 13 August 2017
bibliography: paper.bib

---

# Summary

The `sound-extraction` Python package is for processing and handling observation acoustic data from devices such as ARU, Solar powered Data collector, etc. Functionality in `sound-extraction` is primarily handled using three key open source python packages, `soundfile`[https://pypi.org/project/soundfile/], `suncalc`[(https://pypi.org/project/suncalc/)] and `astral`[(https://astral.readthedocs.io/en/latest/)]. 

A defined processing workflow is included in `sound-extraction` for extracting sample audio from the original recordings. Example files are provided in the documentation for the trial use. 

Workflow image will go at the bottom.

# Statement of need

The availability of relatively low-cost hardware has facilitated the deployment of semi-permanent acoustic sensors that record ambient sounds continuously and produce datasets that have the potential to offer greater understanding of long-term environmental change. Further facilitating monitoring of soundscapes is the increased availability of software tools that extract ecologically significant acoustic information from such broad scales, for example, through the computation of acoustic indices or by discriminating features with machine learning techniques. However, these tools still often require expert validation at the level of the sound itself (e.g., the identification of a bird species from its song), which result in the creation of inventories made by labelling (aka tagging) sounds within a smaller subset of audio. Hence, long-duration, or variable-duration recordings, must be often stratified, subsampled, selected and extracted (i.e., copied and moved), and organized into a new folder structure. Thus, to help expedite these resource-intensive subsetting tasks, we present an audio extraction program that enables users to, sample, select, copy, and extract (aka “clip”) recordings to some pre-defined subsample regime. Written in Python, users define and import a list of subsample filenames, which are copied and move to a user-defined duration and folder structure. The program utilizes basic data structures like dictionaries, datetime objects, strings, lists and offers customization options for those working with different audio formats (i.e., FLAC or WAV), and frequencies (0–256000 Hertz). We hope that the program which will help facilitate comparison of original and archival acoustic datasets by extraction of audio recordings with standardized durations.

There are various open-source tools available for calculating sunrise and sunset times based on the latitude and longitude of a location. However, libraries like Astral and suncalc are often limited in calculating sunrise and sunset times. In contrast, our sound-extraction tool goes beyond that by enabling users to sample recording times according to Nocturnal, Dusk, Early breeding, mid breeding and Late breeding and extract specific audio samplings with just a few command line arguments.

While there are existing public libraries like FFmpeg (https://ffmpeg.org/) for sampling recordings, there is no single program available that provides flexible audio extraction into desired segments according to user preferences. The purpose of Sound-Extraction is to address this gap by offering a Python package that implements customized tools. These tools allow users to sample recordings based on the sunrise and sunset times of a specific location. The sample times are stored in a dictionary, with the original recordings serving as keys and the corresponding sample files as values.

Additionally, Sound-Extraction categorizes the filtered values into the appropriate original recordings category. To process the audio files, we utilize the soundfile library, which is built on top of the NumPy library (Harris et al., 2020). Soundfile provides efficient and convenient functions for reading, writing, and processing audio files, further enhancing the capabilities of our tool.

# Examples



# Citations

# Acknowledgements

The authors of sound-extraction will like to thank Canadian Wildlife Service (CWS) and Environment and Climate Change Canada (ECCC) for putting the tool to use in their research. Thank you to Douglas Hynes for testing and providing feedback and suggestions. Their feedback and suggestions have played a crucial role in driving the development of sound-extraction. 




# References

Harris, C. R., Millman, K. J., van der Walt, S. J., Gommers, R., Virtanen, P., Cournapeau,
    D., Wieser, E., Taylor, J., Berg, S., Smith, N. J., Kern, R., Picus, M., Hoyer, S., van
    Kerkwijk, M. H., Brett, M., Haldane, A., del Rıo, J. F., Wiebe, M., Peterson, P., … ́
    Oliphant, T. E. (2020). Array programming with NumPy. Nature, 585(7825), 357–362.
    https://doi.org/10.1038/s41586-020-2649-2
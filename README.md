# Text Mining Project
Title: Analyse ECB's official press statements<br>
Author: Hans-Peter Hoellwirth<br>
Date: 06.2017<br>

## Data
Web scrapping official press statements published at https://www.ecb.europa.eu/press/pressconf/2017/html/index.en.html for the years 1998-2017.

## Text Analysis
Latent Dirichlet Allocation (LDA) and Structural Topic Model (STM) for 3 and 10 topics

## Main Result(s)
3 topics: Topics are mainly associated to presidencies<br>
10 topics: Most topics are associated to major events and policies in ECB's history

## Code Instructions
Run in the following order:
 - 01_web_scraping.py: Creates file data/combined.csv (optional if already existing)
 - 02_pre_processing.py: Requires file data/combined.csv to exist
 - 03_lda.py: Takes output of previous step (text_process) as input
 - 04_stm.R: Requires file data/combined.csv to exist. Independently executable from steps 2 and 3

 Note: Before execution, update the working directory in each code file.

# Survey-Data-Analysis
Modules for EDA of periodic surveys with slightly different structure in each iteration

## Purpose
The code here lays out a small scale pipeline for analysis of survey data collected every few years. Variable names, missing value codes, categorical groupings, geographic availability, etc. vary a good deal across survey years, so I've set up typed dictionaries in the specs file to store details for each survey year (only one survey year's specifications included here). Having all the information aligned, some basic analyses can be run across survey years.

The functions file has a few simple tools for introductory analysis and graphics. The main file feeds the specs data in calls to the analysis functions for each survey.

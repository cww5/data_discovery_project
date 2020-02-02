# Data Discovery Project

## Visualization for Data Discovery in Open Data Portals (Discovery)

Currently existing data portals (as examples): NYC open data, Boston open data, data.gov
* [NYC Open Data] https://opendata.cityofnewyork.us/ - Used for gathering the data sets
* [Boston Open Data] https://data.boston.gov/ - Another data portal
* [US Government Data] https://www.data.gov/ - Another data portal

The above data portals have a large abundance of data, but are not very accessible; there is little support for discovering links across data sets. As an example of this, there may be 100 data sets about education, and 50 of them may be about students, but we don't know if the set of students is the same or different across the data sets. What if a data consumer is interested in race and gender attribute? These might exist across health, education, and crime data sets. Unless they download all the files and manually check for an overlap, the consumer can't find these patterns.

## Goal

Help users visually understand these links and also understand what information can be gained by such links (e.g., linking data sets A, B, and C might easily have links, but maybe they also link with G, M, and Z). Here, visualization can be used to suggest interesting patterns otherwise difficult to detect. To guide the users along in discovering these links, we have already started by computing our own links amongst the data sets, and have composed an interactive journal article for users to read a story while playing with graphs.

## TODO

- [x] Initialize repo
- [x] Build project requirements
- [x] Narrow down data sets
- [x] Come up with a design for the application
- [x] Come up with 3 designs for the application
- [x] Present final product

# Getting Started

## Prerequisites / Built With

* [Python 3] https://www.python.org/ - Link for downloading Python
* [Anaconda] https://docs.anaconda.com/anaconda/install/ - Anaconda Distribution (Matplotlib, Seaborn, Pandas)
* [Install Dash by Plotly] https://dash.plot.ly/installation - Link for installation

## Running the Application

1) Download final_discovery_app.py
2) Run the following command: python final_discovery_app.py
3) Open an Internet Browser and visit the URL given in the CMD. Should be something like: http://127.0.0.1:8050/
4) Tested/verified with Google Chrome Version 78.0.3904.108 (Official Build) (64-bit)

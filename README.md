Introduction
============

ccg is a program which enables you to plot ERSL atmospheric gas data from the US National Oceanic and Atmospheric Administration (NOAA) web site.

Example data sources:

``` bash
cd data
wget https://gml.noaa.gov/aftp/data/trace_gases/co2/flask/co2_flask_surface_2021-07-30.tar.gz
tar -xzvf co2_flask_surface_2021-07-30.tar.gz
cd ..
python3 ccg2.py
ls *.jpg
```

Introduction
============

ccg is a program which enables you to plot ERSL atmospheric gas data from the US National Oceanic and Atmospheric Administration (NOAA) web site.

For Carbon Dioxide:

``` bash
cd data
rm -rf surface
wget https://gml.noaa.gov/aftp/data/trace_gases/co2/flask/co2_flask_surface_2021-07-30.tar.gz
tar -xzvf co2_flask_surface_2021-07-30.tar.gz
cd ..
python3 ccg2.py --title "Atmospheric CO2"
ls *.jpg *.kml
```

For Methane:

``` bash
cd data
rm -rf surface
wget https://gml.noaa.gov/aftp/data/trace_gases/ch4/flask/ch4_flask_surface_2021-07-30.tar.gz
tar -xzvf ch4_flask_surface_2021-07-30.tar.gz
cd ..
python3 ccg2.py --title "Atmospheric CH4"
ls *.jpg *.kml
```

Introduction
============

ccg is a program which enables you to plot ERSL atmospheric gas data from the US National Oceanic and Atmospheric Administration (NOAA) web site.

For Carbon Dioxide:

``` bash
cd data
rm -rf surface_co2
wget https://gml.noaa.gov/aftp/data/trace_gases/co2/flask/surface/co2_surface-flask_1_ccgg_ASCIItext.tar.gz
tar -xzvf co2_surface-flask_1_ccgg_ASCIItext.tar.gz
mv co2_surface-flask_1_ccgg_ASCIItext surface_co2
cd ..
python3 ccg2.py --title "Atmospheric CO2"
ls *.jpg *.kml
```

For Methane:

``` bash
cd data
rm -rf surface_ch4
wget https://gml.noaa.gov/aftp/data/trace_gases/ch4/flask/surface/ch4_surface-flask_1_ccgg_ASCIItext.tar.gz
tar -xzvf ch4_surface-flask_1_ccgg_ASCIItext.tar.gz
mv ch4_surface-flask_1_ccgg_ASCIItext surface_ch4
cd ..
python3 ccg2.py --title "Atmospheric CH4" --dir data/surface_ch4
ls *.jpg *.kml
```

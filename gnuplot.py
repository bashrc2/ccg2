__filename__ = "gnuplot.py"
__author__ = "Bob Mottram"
__license__ = "GPL3+"
__version__ = "2.0.0"
__maintainer__ = "Bob Mottram"
__email__ = "bob@libreserver.org"
__status__ = "Production"
__module_group__ = "Commandline Interface"

import os


def _get_value_range(series: {},
                     start_year: int, end_year: int) -> (float, float):
    """Returns the minimum and maximum values
    """
    minimum_value = 99999999
    maximum_value = -99999999
    for year in range(start_year, end_year + 1, 1):
        if series.get(year):
            for month_index in range(12):
                if series[year][month_index] == 0:
                    continue
                if series[year][month_index] > maximum_value:
                    maximum_value = series[year][month_index]
                if series[year][month_index] < minimum_value:
                    minimum_value = series[year][month_index]
    return minimum_value, maximum_value


def plot_time_series(series: {}, title: str,
                     start_year: int, end_year: int) -> None:
    """Plot monthly time series graph
    """
    minimum_value, maximum_value = \
        _get_value_range(series, start_year, end_year)

    subtitle = "Source https://gml.noaa.gov/dv/data.html"
    x_label = 'Year'
    y_label = 'Parts Per Million'
    if 'CH4' in title or 'methane' in title.lower():
        y_label = 'Parts Per Billion'
    indent = 0.39
    vpos = 0.94
    image_width = 1000
    image_height = 1000
    plot_name = 'ccg'
    image_format = 'jpg'
    image_format2 = 'jpeg'
    filename = plot_name + '.' + image_format
    script_filename = plot_name + '.gnuplot'
    data_filename = plot_name + '.data'
    min_year = end_year
    max_year = start_year
    with open(data_filename, 'w+') as fp_data:
        for year in range(start_year, end_year + 1, 1):
            if series.get(year):
                if year < min_year:
                    min_year = year
                if year > max_year:
                    max_year = year
                for month_index in range(12):
                    fraction = year + (float(month_index) / 12)
                    fp_data.write(str(fraction) + "    " +
                                  str(series[year][month_index]) + '\n')
    title += " " + str(min_year) + ' - ' + str(max_year)
    script = \
        "reset\n" + \
        "set title \"" + title + "\"\n" + \
        "set label \"" + subtitle + "\" at screen " + \
        str(indent) + ", screen " + str(vpos) + "\n" + \
        "set yrange [" + str(minimum_value) + ":" + \
        str(maximum_value) + "]\n" + \
        "set xrange [" + str(min_year) + ":" + str(max_year + 1) + "]\n" + \
        "set lmargin 9\n" + \
        "set rmargin 2\n" + \
        "set xlabel \"" + x_label + "\"\n" + \
        "set ylabel \"" + y_label + "\"\n" + \
        "set grid\n" + \
        "set key right bottom\n" + \
        "set terminal " + image_format2 + \
        " size " + str(image_width) + "," + str(image_height) + "\n" + \
        "set output \"" + filename + "\"\n" + \
        "plot \"" + data_filename + "\" using 1:2 notitle with lines\n"
    with open(script_filename, 'w+') as fp_script:
        fp_script.write(script)
    os.system('gnuplot ' + script_filename)


def plot_time_series_annual(series: {}, title: str,
                            start_year: int, end_year: int) -> None:
    """Plot annual time series graph
    """
    minimum_value, maximum_value = \
        _get_value_range(series, start_year, end_year)

    subtitle = "Source https://gml.noaa.gov/dv/data.html"
    x_label = 'Year'
    y_label = 'Parts Per Million'
    if 'CH4' in title or 'methane' in title.lower():
        y_label = 'Parts Per Billion'
    indent = 0.39
    vpos = 0.94
    image_width = 1000
    image_height = 1000
    plot_name = 'ccg_annual'
    image_format = 'jpg'
    image_format2 = 'jpeg'
    filename = plot_name + '.' + image_format
    script_filename = plot_name + '.gnuplot'
    data_filename = plot_name + '.data'
    min_year = end_year
    max_year = start_year
    with open(data_filename, 'w+') as fp_data:
        for year in range(start_year, end_year + 1, 1):
            if series.get(year):
                if year < min_year:
                    min_year = year
                if year > max_year:
                    max_year = year
                av1 = 0
                hits = 0
                for month_index in range(12):
                    if series[year][month_index] > 0:
                        hits += 1
                        av1 += series[year][month_index]
                if hits > 0:
                    av1 /= hits
                fp_data.write(str(year) + "    " + str(av1) + '\n')
    title += " " + str(min_year) + ' - ' + str(max_year) + ' Annual'
    script = \
        "reset\n" + \
        "set title \"" + title + "\"\n" + \
        "set label \"" + subtitle + "\" at screen " + \
        str(indent) + ", screen " + str(vpos) + "\n" + \
        "set yrange [" + str(minimum_value) + ":" + \
        str(maximum_value) + "]\n" + \
        "set xrange [" + str(min_year) + ":" + str(max_year) + "]\n" + \
        "set lmargin 9\n" + \
        "set rmargin 2\n" + \
        "set xlabel \"" + x_label + "\"\n" + \
        "set ylabel \"" + y_label + "\"\n" + \
        "set grid\n" + \
        "set key right bottom\n" + \
        "set terminal " + image_format2 + \
        " size " + str(image_width) + "," + str(image_height) + "\n" + \
        "set output \"" + filename + "\"\n" + \
        "plot \"" + data_filename + "\" using 1:2 notitle with lines\n"
    with open(script_filename, 'w+') as fp_script:
        fp_script.write(script)
    os.system('gnuplot ' + script_filename)


def plot_time_series_annual_change(series: {}, title: str,
                                   start_year: int, end_year: int) -> None:
    """Plot annual change time series graph
    """
    subtitle = "Source https://gml.noaa.gov/dv/data.html"
    x_label = 'Year'
    y_label = 'Parts Per Million'
    if 'CH4' in title or 'methane' in title.lower():
        y_label = 'Parts Per Billion'
    indent = 0.39
    vpos = 0.94
    image_width = 1000
    image_height = 1000
    plot_name = 'ccg_change'
    image_format = 'jpg'
    image_format2 = 'jpeg'
    filename = plot_name + '.' + image_format
    script_filename = plot_name + '.gnuplot'
    data_filename = plot_name + '.data'
    min_year = end_year
    max_year = start_year
    minimum_value = 99999999
    maximum_value = -99999999
    with open(data_filename, 'w+') as fp_data:
        for year in range(start_year - 5, end_year + 1, 1):
            if not series.get(year):
                continue
            if not series.get(year - 1):
                continue
            av1 = 0
            hits = 0
            for month_index in range(12):
                if series[year][month_index] > 0:
                    if series[year - 1][month_index] > 0:
                        hits += 1
                        av1 += \
                            series[year][month_index] - \
                            series[year - 1][month_index]
            if hits > 0:
                av1 /= hits
                change = av1
                if change < minimum_value:
                    minimum_value = change
                if change > maximum_value:
                    maximum_value = change
                if year >= start_year:
                    if year < min_year:
                        min_year = year
                    if year > max_year:
                        max_year = year
                    fp_data.write(str(year) + "    " + str(change) + '\n')
    title += " " + str(min_year) + ' - ' + str(max_year) + ' Annual Change'
    script = \
        "reset\n" + \
        "set title \"" + title + "\"\n" + \
        "set label \"" + subtitle + "\" at screen " + \
        str(indent) + ", screen " + str(vpos) + "\n" + \
        "set yrange [" + str(minimum_value) + ":" + \
        str(maximum_value) + "]\n" + \
        "set xrange [" + str(min_year) + ":" + str(max_year) + "]\n" + \
        "set lmargin 9\n" + \
        "set rmargin 2\n" + \
        "set xlabel \"" + x_label + "\"\n" + \
        "set ylabel \"" + y_label + "\"\n" + \
        "set grid\n" + \
        "set key right bottom\n" + \
        "set terminal " + image_format2 + \
        " size " + str(image_width) + "," + str(image_height) + "\n" + \
        "set output \"" + filename + "\"\n" + \
        "plot \"" + data_filename + "\" using 1:2 notitle with lines\n"
    with open(script_filename, 'w+') as fp_plot:
        fp_plot.write(script)
    os.system('gnuplot ' + script_filename)

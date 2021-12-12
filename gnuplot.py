__filename__ = "gnuplot.py"
__author__ = "Bob Mottram"
__license__ = "GPL3+"
__version__ = "2.0.0"
__maintainer__ = "Bob Mottram"
__email__ = "bob@libreserver.org"
__status__ = "Production"
__module_group__ = "Commandline Interface"

import os


def _getValueRange(series: {}, startYear: int, endYear: int) -> (float, float):
    """Returns the minimum and maximum values
    """
    minimumValue = 99999999
    maximumValue = -99999999
    for year in range(startYear, endYear + 1, 1):
        if series.get(year):
            for monthIndex in range(12):
                if series[year][monthIndex] == 0:
                    continue
                if series[year][monthIndex] > maximumValue:
                    maximumValue = series[year][monthIndex]
                if series[year][monthIndex] < minimumValue:
                    minimumValue = series[year][monthIndex]
    return minimumValue, maximumValue


def plotTimeSeries(series: {}, title: str,
                   startYear: int, endYear: int) -> None:
    """Plot monthly time series graph
    """
    minimumValue, maximumValue = _getValueRange(series, startYear, endYear)

    subtitle = "Source https://gml.noaa.gov/dv/data.html"
    Xlabel = 'Year'
    Ylabel = 'Parts Per Million'
    if 'CH4' in title or 'methane' in title.lower():
        Ylabel = 'Parts Per Billion'
    indent = 0.39
    vpos = 0.94
    imageWidth = 1000
    imageHeight = 1000
    plotName = 'ccg'
    imageFormat = 'jpg'
    imageFormat2 = 'jpeg'
    filename = plotName + '.' + imageFormat
    scriptFilename = plotName + '.gnuplot'
    dataFilename = plotName + '.data'
    minYear = endYear
    maxYear = startYear
    with open(dataFilename, 'w+') as fp:
        for year in range(startYear, endYear + 1, 1):
            if series.get(year):
                if year < minYear:
                    minYear = year
                if year > maxYear:
                    maxYear = year
                for monthIndex in range(12):
                    fraction = year + (float(monthIndex) / 12)
                    fp.write(str(fraction) + "    " +
                             str(series[year][monthIndex]) + '\n')
    title += " " + str(minYear) + ' - ' + str(maxYear)
    script = \
        "reset\n" + \
        "set title \"" + title + "\"\n" + \
        "set label \"" + subtitle + "\" at screen " + \
        str(indent) + ", screen " + str(vpos) + "\n" + \
        "set yrange [" + str(minimumValue) + ":" + \
        str(maximumValue) + "]\n" + \
        "set xrange [" + str(minYear) + ":" + str(maxYear + 1) + "]\n" + \
        "set lmargin 9\n" + \
        "set rmargin 2\n" + \
        "set xlabel \"" + Xlabel + "\"\n" + \
        "set ylabel \"" + Ylabel + "\"\n" + \
        "set grid\n" + \
        "set key right bottom\n" + \
        "set terminal " + imageFormat2 + \
        " size " + str(imageWidth) + "," + str(imageHeight) + "\n" + \
        "set output \"" + filename + "\"\n" + \
        "plot \"" + dataFilename + "\" using 1:2 notitle with lines\n"
    with open(scriptFilename, 'w+') as fp:
        fp.write(script)
    os.system('gnuplot ' + scriptFilename)


def plotTimeSeriesAnnual(series: {}, title: str,
                         startYear: int, endYear: int) -> None:
    """Plot annual time series graph
    """
    minimumValue, maximumValue = _getValueRange(series, startYear, endYear)

    subtitle = "Source https://gml.noaa.gov/dv/data.html"
    Xlabel = 'Year'
    Ylabel = 'Parts Per Million'
    if 'CH4' in title or 'methane' in title.lower():
        Ylabel = 'Parts Per Billion'
    indent = 0.39
    vpos = 0.94
    imageWidth = 1000
    imageHeight = 1000
    plotName = 'ccg_annual'
    imageFormat = 'jpg'
    imageFormat2 = 'jpeg'
    filename = plotName + '.' + imageFormat
    scriptFilename = plotName + '.gnuplot'
    dataFilename = plotName + '.data'
    minYear = endYear
    maxYear = startYear
    with open(dataFilename, 'w+') as fp:
        for year in range(startYear, endYear + 1, 1):
            if series.get(year):
                if year < minYear:
                    minYear = year
                if year > maxYear:
                    maxYear = year
                av = 0
                hits = 0
                for monthIndex in range(12):
                    if series[year][monthIndex] > 0:
                        hits += 1
                        av += series[year][monthIndex]
                if hits > 0:
                    av /= hits
                fp.write(str(year) + "    " + str(av) + '\n')
    title += " " + str(minYear) + ' - ' + str(maxYear) + ' Annual'
    script = \
        "reset\n" + \
        "set title \"" + title + "\"\n" + \
        "set label \"" + subtitle + "\" at screen " + \
        str(indent) + ", screen " + str(vpos) + "\n" + \
        "set yrange [" + str(minimumValue) + ":" + \
        str(maximumValue) + "]\n" + \
        "set xrange [" + str(minYear) + ":" + str(maxYear) + "]\n" + \
        "set lmargin 9\n" + \
        "set rmargin 2\n" + \
        "set xlabel \"" + Xlabel + "\"\n" + \
        "set ylabel \"" + Ylabel + "\"\n" + \
        "set grid\n" + \
        "set key right bottom\n" + \
        "set terminal " + imageFormat2 + \
        " size " + str(imageWidth) + "," + str(imageHeight) + "\n" + \
        "set output \"" + filename + "\"\n" + \
        "plot \"" + dataFilename + "\" using 1:2 notitle with lines\n"
    with open(scriptFilename, 'w+') as fp:
        fp.write(script)
    os.system('gnuplot ' + scriptFilename)


def plotTimeSeriesAnnualChange(series: {}, title: str,
                               startYear: int, endYear: int) -> None:
    """Plot annual change time series graph
    """
    subtitle = "Source https://gml.noaa.gov/dv/data.html"
    Xlabel = 'Year'
    Ylabel = 'Parts Per Million'
    if 'CH4' in title or 'methane' in title.lower():
        Ylabel = 'Parts Per Billion'
    indent = 0.39
    vpos = 0.94
    imageWidth = 1000
    imageHeight = 1000
    plotName = 'ccg_change'
    imageFormat = 'jpg'
    imageFormat2 = 'jpeg'
    filename = plotName + '.' + imageFormat
    scriptFilename = plotName + '.gnuplot'
    dataFilename = plotName + '.data'
    minYear = endYear
    maxYear = startYear
    minimumValue = 99999999
    maximumValue = -99999999
    with open(dataFilename, 'w+') as fp:
        for year in range(startYear - 5, endYear + 1, 1):
            if not series.get(year):
                continue
            if not series.get(year - 1):
                continue
            av = 0
            hits = 0
            for monthIndex in range(12):
                if series[year][monthIndex] > 0:
                    if series[year - 1][monthIndex] > 0:
                        hits += 1
                        av += \
                            series[year][monthIndex] - \
                            series[year - 1][monthIndex]
            if hits > 0:
                av /= hits
                change = av
                if change < minimumValue:
                    minimumValue = change
                if change > maximumValue:
                    maximumValue = change
                if year >= startYear:
                    if year < minYear:
                        minYear = year
                    if year > maxYear:
                        maxYear = year
                    fp.write(str(year) + "    " + str(change) + '\n')
    title += " " + str(minYear) + ' - ' + str(maxYear) + ' Annual Change'
    script = \
        "reset\n" + \
        "set title \"" + title + "\"\n" + \
        "set label \"" + subtitle + "\" at screen " + \
        str(indent) + ", screen " + str(vpos) + "\n" + \
        "set yrange [" + str(minimumValue) + ":" + \
        str(maximumValue) + "]\n" + \
        "set xrange [" + str(minYear) + ":" + str(maxYear) + "]\n" + \
        "set lmargin 9\n" + \
        "set rmargin 2\n" + \
        "set xlabel \"" + Xlabel + "\"\n" + \
        "set ylabel \"" + Ylabel + "\"\n" + \
        "set grid\n" + \
        "set key right bottom\n" + \
        "set terminal " + imageFormat2 + \
        " size " + str(imageWidth) + "," + str(imageHeight) + "\n" + \
        "set output \"" + filename + "\"\n" + \
        "plot \"" + dataFilename + "\" using 1:2 notitle with lines\n"
    with open(scriptFilename, 'w+') as fp:
        fp.write(script)
    os.system('gnuplot ' + scriptFilename)

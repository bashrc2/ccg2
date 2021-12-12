__filename__ = "timeseries.py"
__author__ = "Bob Mottram"
__license__ = "GPL3+"
__version__ = "2.0.0"
__maintainer__ = "Bob Mottram"
__email__ = "bob@libreserver.org"
__status__ = "Production"
__module_group__ = "Commandline Interface"


def averageMonthlyValues(sites: {}) -> None:
    """Averages monthly values for each site
    """
    for site, item in sites.items():
        for year, yearItem in item['data'].items():
            for monthIdx in range(12):
                hits = yearItem['hits'][monthIdx]
                if hits > 0:
                    yearItem['month'][monthIdx] /= hits
            months = yearItem['month'].copy()
            item['data'][year] = months


def getTimeSeries(sites: {}) -> {}:
    """Returns the overall time series for all sites
    """
    series = {}

    # sum the month values
    for site, item in sites.items():
        for year, monthsList in item['data'].items():
            if not series.get(year):
                series[year] = {
                    "month": [0] * 12,
                    "hits": [0] * 12
                }
            for monthIndex in range(12):
                if monthsList[monthIndex] == 0:
                    continue
                series[year]['month'][monthIndex] += monthsList[monthIndex]
                series[year]['hits'][monthIndex] += 1

    # average the months
    for year, item in series.items():
        for monthIndex in range(12):
            if series[year]['hits'][monthIndex] > 0:
                series[year]['month'][monthIndex] /= series[year]['hits'][monthIndex]
        months = series[year]['month'].copy()
        series[year] = months
    return series

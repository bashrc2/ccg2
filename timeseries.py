__filename__ = "timeseries.py"
__author__ = "Bob Mottram"
__license__ = "GPL3+"
__version__ = "2.0.0"
__maintainer__ = "Bob Mottram"
__email__ = "bob@libreserver.org"
__status__ = "Production"
__module_group__ = "Commandline Interface"


def average_monthly_values(sites: {}) -> None:
    """Averages monthly values for each site
    """
    for _, item in sites.items():
        for year, year_item in item['data'].items():
            for month_idx in range(12):
                hits = year_item['hits'][month_idx]
                if hits > 0:
                    year_item['month'][month_idx] /= hits
            months = year_item['month'].copy()
            item['data'][year] = months


def get_time_series(sites: {}) -> {}:
    """Returns the overall time series for all sites
    """
    series = {}

    # sum the month values
    for _, item in sites.items():
        for year, months_list in item['data'].items():
            if not series.get(year):
                series[year] = {
                    "month": [0] * 12,
                    "hits": [0] * 12
                }
            for month_index in range(12):
                if months_list[month_index] == 0:
                    continue
                series[year]['month'][month_index] += months_list[month_index]
                series[year]['hits'][month_index] += 1

    # average the months
    for year, item in series.items():
        for month_index in range(12):
            if series[year]['hits'][month_index] > 0:
                series[year]['month'][month_index] /= \
                    series[year]['hits'][month_index]
        months = series[year]['month'].copy()
        series[year] = months
    return series

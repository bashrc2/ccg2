__filename__ = "ccg2.py"
__author__ = "Bob Mottram"
__license__ = "GPL3+"
__version__ = "2.0.0"
__maintainer__ = "Bob Mottram"
__email__ = "bob@libreserver.org"
__status__ = "Production"
__module_group__ = "Commandline Interface"

import os
import sys
import argparse
from parseData import load_sites
from timeseries import average_monthly_values
from timeseries import get_time_series
from gnuplot import plot_time_series
from gnuplot import plot_time_series_annual
from gnuplot import plot_time_series_annual_change
from kml import save_sites_as_kml
from tests import run_all_tests


def str2bool(value) -> bool:
    """Returns true if the given value is a boolean
    """
    if isinstance(value, bool):
        return value
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    if value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    raise argparse.ArgumentTypeError('Boolean value expected.')


parser = argparse.ArgumentParser(description='ccg2')
parser.add_argument('--dir', '-d', dest="dataDir", type=str,
                    default='data/surface_co2',
                    help='Directory for data')
parser.add_argument('--startyear', dest="startYear", type=int,
                    default=2010,
                    help='Start year')
parser.add_argument('--endyear', dest="endYear", type=int,
                    default=2050,
                    help='End year')
parser.add_argument('--minlat', dest="minLatitude", type=float,
                    default=-90,
                    help='Minimum Latitude')
parser.add_argument('--maxlat', dest="maxLatitude", type=float,
                    default=90,
                    help='Maximum Latitude')
parser.add_argument('--minlong', dest="minLongitude", type=float,
                    default=-180,
                    help='Minimum Longitude')
parser.add_argument('--maxlong', dest="maxLongitude", type=float,
                    default=180,
                    help='Maximum Longitude')
parser.add_argument('--minalt', dest="minAltitude", type=float,
                    default=0,
                    help='Minimum Altitude')
parser.add_argument('--maxalt', dest="maxAltitude", type=float,
                    default=9999999,
                    help='Maximum Altitude')
parser.add_argument('--title', dest="title", type=str,
                    default="Atmospheric CO2",
                    help='Title of the graph')
parser.add_argument("--tests", type=str2bool, nargs='?',
                    const=True, default=False,
                    help="Run unit tests")
args = parser.parse_args()

if args.tests:
    run_all_tests()
    sys.exit()


if __name__ == "__main__":
    # load event data from files
    sites = {}
    for subdir, dirs, files in os.walk(args.dataDir):
        for f in files:
            if not f.endswith('event.txt'):
                continue
            filename = args.dataDir + '/' + f
            load_sites(sites, filename, args.startYear, args.endYear,
                       args.minLatitude, args.maxLatitude,
                       args.minLongitude, args.maxLongitude,
                       args.minAltitude, args.maxAltitude)
        break
    average_monthly_values(sites)
    series = get_time_series(sites)
    save_sites_as_kml(sites, 'ccg.kml')
    plot_time_series(series, args.title, args.startYear, args.endYear)
    plot_time_series_annual(series, args.title, args.startYear, args.endYear)
    plot_time_series_annual_change(series, args.title,
                                   args.startYear, args.endYear)
    print('Done')
    sys.exit()

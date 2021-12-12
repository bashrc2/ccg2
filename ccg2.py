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
from parseData import loadSites
from timeseries import averageMonthlyValues
from timeseries import getTimeSeries
from gnuplot import plotTimeSeries
from tests import runAllTests


def str2bool(v) -> bool:
    """Returns true if the given value is a boolean
    """
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


parser = argparse.ArgumentParser(description='ccg2')
parser.add_argument('--dir', '-d', dest="dataDir", type=str,
                    default='data/surface',
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
    runAllTests()
    sys.exit()


if __name__ == "__main__":
    # load event data from files
    sites = {}
    for subdir, dirs, files in os.walk(args.dataDir):
        for f in files:
            if not f.endswith('event.txt'):
                continue
            filename = args.dataDir + '/' + f
            loadSites(sites, filename, args.startYear, args.endYear,
                      args.minLatitude, args.maxLatitude,
                      args.minLongitude, args.maxLongitude,
                      args.minAltitude, args.maxAltitude)
        break
    averageMonthlyValues(sites)
    series = getTimeSeries(sites)
    plotTimeSeries(series, args.title, args.startYear, args.endYear)
    print('Done')
    sys.exit()

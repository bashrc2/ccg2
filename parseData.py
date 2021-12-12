__filename__ = "parseData.py"
__author__ = "Bob Mottram"
__license__ = "GPL3+"
__version__ = "2.0.0"
__maintainer__ = "Bob Mottram"
__email__ = "bob@libreserver.org"
__status__ = "Production"
__module_group__ = "Commandline Interface"


def _getFieldNames(lines: []) -> []:
    """Returns a list of field names
    """
    for line in lines:
        if 'data_fields:' in line:
            fieldsStr = line.split('data_fields:')[1].strip()
            return fieldsStr.split(' ')
    return None


def _getFieldIndex(fieldnames: [], name: str) -> int:
    """Returns the index with the given field name
    """
    for i in range(len(fieldnames)):
        if name in fieldnames[i]:
            return i
    return -1


def loadSites(sites: {}, filename: str, startYear: int, endYear: int,
              minLatitude: float, maxLatitude: float,
              minLongitude: float, maxLongitude: float,
              minAltitude: float, maxAltitude: float) -> bool:
    """Loads sites from file
    """
    lines = []
    try:
        with open(filename, 'r') as fp:
            lines = fp.readlines()
    except OSError:
        print('Unable to open ' + filename)
        return False

    fieldnames = _getFieldNames(lines)
    if not fieldnames:
        print('No fieldnames found in ' + filename)
        return False

    siteIndex = _getFieldIndex(fieldnames, 'site')
    yearIndex = _getFieldIndex(fieldnames, 'year')
    monthIndex = _getFieldIndex(fieldnames, 'month')
    valueIndex = _getFieldIndex(fieldnames, 'value')
    latitudeIndex = _getFieldIndex(fieldnames, 'latitude')
    longitudeIndex = _getFieldIndex(fieldnames, 'longitude')
    altitudeIndex = _getFieldIndex(fieldnames, 'altitude')

    for line in lines:
        if line.startswith('#'):
            continue
        while '  ' in line:
            line = line.replace('  ', ' ')
        fields = line.replace('\n', ' ').split(' ')
        if not fields[yearIndex]:
            continue
        year = int(fields[yearIndex])
        if year < startYear:
            continue
        if year > endYear:
            continue
        if not fields[monthIndex]:
            continue
        if not fields[valueIndex]:
            continue
        site = fields[siteIndex]
        month = int(fields[monthIndex])
        value = float(fields[valueIndex])
        latitude = float(fields[latitudeIndex])
        if latitude < minLatitude or latitude > maxLatitude:
            continue
        longitude = float(fields[longitudeIndex])
        if maxLongitude > minLongitude:
            if longitude < minLongitude or longitude > maxLongitude:
                continue
        else:
            if longitude < maxLongitude and longitude > minLongitude:
                continue        
        altitude = float(fields[altitudeIndex])
        if altitude < minAltitude or altitude > maxAltitude:
            continue
        if not sites.get(site):
            sites[site] = {
                "latitude": latitude,
                "longitude": longitude,
                "altitude": altitude,
                "data": {}
            }
        if not sites[site]['data'].get(year):
            sites[site]['data'][year] = {
                "month": [0] * 12,
                "hits": [0] * 12
            }
        sites[site]['data'][year]['month'][month - 1] += value
        sites[site]['data'][year]['hits'][month - 1] += 1

    return True

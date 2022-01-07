__filename__ = "parseData.py"
__author__ = "Bob Mottram"
__license__ = "GPL3+"
__version__ = "2.0.0"
__maintainer__ = "Bob Mottram"
__email__ = "bob@libreserver.org"
__status__ = "Production"
__module_group__ = "Commandline Interface"


def _get_field_names(lines: []) -> []:
    """Returns a list of field names
    """
    for line in lines:
        if 'data_fields:' in line:
            fields_str = line.split('data_fields:')[1].strip()
            return fields_str.split(' ')
    return None


def _get_field_index(fieldnames: [], name: str) -> int:
    """Returns the index with the given field name
    """
    for idx in range(len(fieldnames)):
        if name in fieldnames[idx]:
            return idx
    return -1


def load_sites(sites: {}, filename: str, start_year: int, end_year: int,
               min_latitude: float, max_latitude: float,
               min_longitude: float, max_longitude: float,
               min_altitude: float, max_altitude: float) -> bool:
    """Loads sites from file
    """
    lines = []
    try:
        with open(filename, 'r') as fp_load:
            lines = fp_load.readlines()
    except OSError:
        print('Unable to open ' + filename)
        return False

    fieldnames = _get_field_names(lines)
    if not fieldnames:
        print('No fieldnames found in ' + filename)
        return False

    site_index = _get_field_index(fieldnames, 'site')
    year_index = _get_field_index(fieldnames, 'year')
    month_index = _get_field_index(fieldnames, 'month')
    value_index = _get_field_index(fieldnames, 'value')
    latitude_index = _get_field_index(fieldnames, 'latitude')
    longitude_index = _get_field_index(fieldnames, 'longitude')
    altitude_index = _get_field_index(fieldnames, 'altitude')

    for line in lines:
        if line.startswith('#'):
            continue
        while '  ' in line:
            line = line.replace('  ', ' ')
        fields = line.replace('\n', ' ').split(' ')
        if not fields[year_index]:
            continue
        year = int(fields[year_index])
        if year < start_year:
            continue
        if year > end_year:
            continue
        if not fields[month_index]:
            continue
        if not fields[value_index]:
            continue
        site = fields[site_index]
        month = int(fields[month_index])
        value = float(fields[value_index])
        if value == 0:
            continue
        latitude = float(fields[latitude_index])
        if latitude < min_latitude or latitude > max_latitude:
            continue
        longitude = float(fields[longitude_index])
        if max_longitude > min_longitude:
            if longitude < min_longitude or longitude > max_longitude:
                continue
        else:
            if longitude < max_longitude and longitude > min_longitude:
                continue
        altitude = float(fields[altitude_index])
        if altitude < min_altitude or altitude > max_altitude:
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

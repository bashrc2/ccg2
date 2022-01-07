__filename__ = "kml.py"
__author__ = "Bob Mottram"
__license__ = "GPL3+"
__version__ = "2.0.0"
__maintainer__ = "Bob Mottram"
__email__ = "bob@libreserver.org"
__status__ = "Production"
__module_group__ = "Commandline Interface"


def save_sites_as_kml(sites: {}, filename: str) -> None:
    """Save sites in KML format for visualization
    """
    kml_str = \
        "<?xml version=\"1.0\" encoding='UTF-8'?>\n" + \
        "<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n" + \
        "<Document>\n"
    for site, item in sites.items():
        kml_str += \
            "  <Placemark>\n" + \
            "    <name>" + site + "</name>\n" + \
            "    <description>" + str(item['latitude']) + \
            ' ' + str(item['longitude']) + '</description>\n' + \
            "    <Point>\n" + \
            "      <coordinates>" + str(item['longitude']) + "," + \
            str(item['latitude']) + "," + str(item['altitude']) + \
            "</coordinates>\n" + \
            "    </Point>\n" + \
            "  </Placemark>\n"
    kml_str += \
        "</Document>\n" + \
        "</kml>\n"
    with open(filename, 'w+') as fp_kml:
        fp_kml.write(kml_str)

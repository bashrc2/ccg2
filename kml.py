__filename__ = "kml.py"
__author__ = "Bob Mottram"
__license__ = "GPL3+"
__version__ = "2.0.0"
__maintainer__ = "Bob Mottram"
__email__ = "bob@libreserver.org"
__status__ = "Production"
__module_group__ = "Commandline Interface"


def saveSitesAsKML(sites: {}, filename: str) -> None:
    """Save sites in KML format for visualization
    """
    kmlStr = \
        "<?xml version=\"1.0\" encoding='UTF-8'?>\n" + \
        "<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n" + \
        "<Document>\n"
    for site, item in sites.items():
        kmlStr += \
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
    kmlStr += \
        "</Document>\n" + \
        "</kml>\n"
    with open(filename, 'w+') as fp:
        fp.write(kmlStr)

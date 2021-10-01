# -*- coding: utf-8 -*-
def classFactory(iface):  # pylint: disable=invalid-name
    from .gpx_shp import gpx_shp
    return gpx_shp(iface)

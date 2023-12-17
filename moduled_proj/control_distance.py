from pyproj import Geod
from pyproj import Transformer

transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857")
inverse_transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326")
wgs84_geod = Geod(ellps='WGS84')

def distance(lat1, lon1, lat2, lon2):
    az12, az21, dist = wgs84_geod.inv(lon1, lat1, lon2, lat2)
    return dist
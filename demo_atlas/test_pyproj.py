from pyproj import Transformer

transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857")

print(transformer.transform(21.0131, 105.8040))

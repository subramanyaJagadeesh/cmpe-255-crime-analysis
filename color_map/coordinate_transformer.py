import json
import pyproj
import copy

# Load GeoJSON data from a file (adjust the file path as needed)
geojson_file_path = "datasets/LAPD_Division.geojson"
with open(geojson_file_path, "r") as file:
    geojson_data = json.load(file)

# Transformer from State Plane (EPSG:2229) to WGS 84 (EPSG:4326)
transformer = pyproj.Transformer.from_crs("EPSG:2229", "EPSG:4326", always_xy=True)

# Function to transform coordinates
def transform_coordinates(coordinate_list):
    return [transformer.transform(*coord) for coord in coordinate_list]

# Deep copy the GeoJSON data to avoid modifying the original
transformed_geojson = copy.deepcopy(geojson_data)

# Iterate over all features and transform their coordinates
for feature in transformed_geojson["features"]:
    geometry_type = feature["geometry"]["type"]
    coordinates = feature["geometry"]["coordinates"]

    if geometry_type == "Point":
        feature["geometry"]["coordinates"] = transform_coordinates([coordinates])[0]
    elif geometry_type in ["LineString", "MultiPoint"]:
        feature["geometry"]["coordinates"] = transform_coordinates(coordinates)
    elif geometry_type in ["Polygon", "MultiLineString"]:
        feature["geometry"]["coordinates"] = [
            transform_coordinates(coord_set) for coord_set in coordinates
        ]
    elif geometry_type == "MultiPolygon":
        feature["geometry"]["coordinates"] = [
            [transform_coordinates(coord_set) for coord_set in coord_set_list]
            for coord_set_list in coordinates
        ]

# Save the transformed GeoJSON to a file or output it
with open("transformed_geojson.geojson", "w") as f:
    json.dump(transformed_geojson, f)

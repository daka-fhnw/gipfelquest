from read_gipfel_koordinaten import read_gipfel_koordinaten
import json
import requests
from enum import Enum
import geopandas as gpd


##### API Aufrufdefinition #####

# https://docs.geo.admin.ch/access-data/get-elevation-profile.html
PROFILE_API_URL = "https://api3.geo.admin.ch/rest/services/profile.json"

class Direction(Enum):    # in Nord und Ost Richtung
    NORTH = 1
    EAST = 2

def get_profile_json(xy_lv95: tuple[float, float],
                     direction: Direction,
                     radius_m: int = 1000,
                     nb_points: int = 200) -> list[dict]:
    x1 = xy_lv95[0]
    y1 = xy_lv95[1]
    x2 = xy_lv95[0]
    y2 = xy_lv95[1]
    if direction == Direction.NORTH:
        y1 -= radius_m
        y2 += radius_m
    else:
        x1 -= radius_m
        x2 += radius_m
    geom = {
        "type": "LineString", 
        "coordinates": ((x1, y1), (x2, y2)),
    }
    geom_string = json.dumps(geom)
    params = {"geom": geom_string, "sr": 2056, "nb_points": nb_points}
    response = requests.get(PROFILE_API_URL, params=params)
    response.raise_for_status()
    return response.json()
    
def get_profile_data(xy_lv95: tuple[float, float],
                     direction: Direction,
                     radius_m: int = 1000,
                     nb_points: int = 200) -> list[tuple[float, float]]:
    json = get_profile_json(xy_lv95, direction, radius_m, nb_points)
    if direction == Direction.NORTH:
        x_label = "northing"
    else:
        x_label = "easting"
    xy_list = list(map(lambda entry: [
        entry[x_label], 
        entry["alts"]["COMB"],
    ], json))
    return xy_list


##### Schreiben Profil in zwei Dictonarys für Nord und Ost #####

def get_profil(data):
    profil = []
    for row in data.itertuples():
        name = row.Name
        easting = row.geometry.x
        northing = row.geometry.y
        koordinaten_tupel=[float(easting), float(northing)]
        data_E = get_profile_data(koordinaten_tupel, Direction.EAST)
        data_N = get_profile_data(koordinaten_tupel, Direction.NORTH)

        profil.append({
            # z.B. Gebietsname, Profilkoordinaten, ...
            "east": data_E,
            "north": data_N,
        })
    return profil

if __name__ == "__main__":
    data = read_gipfel_koordinaten()
    liste = get_profil(data)
    print(liste)
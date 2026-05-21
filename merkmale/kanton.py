import pandas as pd
import geopandas as gpd

# https://www.swisstopo.admin.ch/de/landschaftsmodell-swissboundaries3d
SB3D_FILE_PATH = "quellen/swissBOUNDARIES3D_1_5_LV95_LN02.gpkg"
KANTON_LAYER = "tlm_kantonsgebiet"

kanton_nr_zu_namen = {
     1: "Zürich",
     2: "Bern",
     3: "Luzern",
     4: "Uri",
     5: "Schwyz",
     6: "Obwalden",
     7: "Nidwalden",
     8: "Glarus",
     9: "Zug",
    10: "Fribourg",
    11: "Solothurn",
    12: "Basel-Stadt",
    13: "Basel-Landschaft",
    14: "Schaffhausen",
    15: "Appenzell Ausserrhoden",
    16: "Appenzell Innerrhoden",
    17: "St. Gallen",
    18: "Graubünden",
    19: "Aargau",
    20: "Thurgau",
    21: "Tessin",
    22: "Waadt",
    23: "Wallis",
    24: "Neuenburg",
    25: "Genf",
    26: "Jura",
}

data = pd.read_csv('data/gipfel-koordinaten.csv')
data = gpd.GeoDataFrame(data, 
    geometry=gpd.points_from_xy(data['easting'], data['northing']),
    crs='EPSG:2056'
)

kantone = gpd.read_file(SB3D_FILE_PATH, layer=KANTON_LAYER)
kantone = kantone[["name", "kantonsnummer", "geometry"]]
kantone = kantone.rename(columns={"name": "kanton"})

closest = data.sjoin_nearest(kantone, how='left', distance_col='distance', max_distance=100)
closest = closest[["name", "kantonsnummer", "kanton"]]

liste = []
for row in data.itertuples():
    gefiltert = closest[closest.name == row.name]
    kanton = None
    if gefiltert["kanton"].count() != 0:
        kanton_nr = gefiltert.iloc[0]["kantonsnummer"]
        kanton = kanton_nr_zu_namen[kanton_nr]
    liste.append({"kanton": kanton})

print(liste)

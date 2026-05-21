import pandas as pd
import geopandas as gpd

# https://www.swisstopo.admin.ch/de/landschaftsmodell-swissboundaries3d
SB3D_FILE_PATH = "quellen/swissBOUNDARIES3D_1_5_LV95_LN02.gpkg"
KANTON_LAYER = "tlm_kantonsgebiet"

data = pd.read_csv('data/gipfel-koordinaten.csv')
data = gpd.GeoDataFrame(data, 
    geometry=gpd.points_from_xy(data['easting'], data['northing']),
    crs='EPSG:2056'
)

kantone = gpd.read_file(SB3D_FILE_PATH, layer=KANTON_LAYER)
kantone = kantone[["name", "kantonsnummer", "geometry"]]
kantone = kantone.rename(columns={"name": "kanton"})

closest = data.sjoin_nearest(kantone, how='left', distance_col='distance', max_distance=100)
closest = closest[["name", "kanton"]]

liste = []
for row in data.itertuples():
    gefiltert = closest[closest.name == row.name]
    kanton = None
    if gefiltert["kanton"].count() != 0:
        kanton = gefiltert.iloc[0]["kanton"]
    liste.append({"kanton": kanton})

print(liste)

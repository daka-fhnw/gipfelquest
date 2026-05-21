import pandas as pd
import geopandas as gpd

# https://www.swisstopo.admin.ch/de/landschaftsmodell-swissboundaries3d
SB3D_FILE_PATH = "quellen/swissBOUNDARIES3D_1_5_LV95_LN02.gpkg"
GEMEINDE_LAYER = "tlm_hoheitsgebiet"

data = pd.read_csv('data/gipfel-koordinaten.csv')
data = gpd.GeoDataFrame(data, 
    geometry=gpd.points_from_xy(data['easting'], data['northing']),
    crs='EPSG:2056'
)

gemeinden = gpd.read_file(SB3D_FILE_PATH, layer=GEMEINDE_LAYER)
gemeinden = gemeinden[["name", "geometry"]]
gemeinden = gemeinden.rename(columns={"name": "gemeinde"})

closest = data.sjoin_nearest(gemeinden, how='left', distance_col='distance', max_distance=100)
closest = closest[["name", "gemeinde"]]

liste = []
for row in data.itertuples():
    gefiltert = closest[closest.name == row.name]
    gemeinde = None
    if gefiltert["gemeinde"].count() != 0:
        gemeinde = gefiltert.iloc[0]["gemeinde"]
    liste.append({"gemeinde": gemeinde})

print(liste)

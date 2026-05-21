import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

data = pd.read_csv('data/gipfel-koordinaten.csv')
data = gpd.GeoDataFrame(data, 
    geometry=gpd.points_from_xy(data['easting'], data['northing']),
    crs='EPSG:2056'
)

liste = []

for row in data.itertuples():
    name = row.name
    easting = row.easting
    northing = row.northing
    # spezifischer Code
    liste.append({
        # z.B. Gebietsname, Profilkoordinaten, ...
        "property1": 1,
        "property2": 2,
    })

print(liste)

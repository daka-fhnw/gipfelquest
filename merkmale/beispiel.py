import geopandas as gpd

data = gpd.read_file('data/gipfel-koordinaten.csv')

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

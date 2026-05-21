import geopandas as gpd
from read_gipfel_koordinaten import read_gipfel_koordinaten

# https://www.swisstopo.admin.ch/de/landschaftsmodell-swissboundaries3d
SB3D_FILE_PATH = "quellen/swissBOUNDARIES3D_1_5_LV95_LN02.gpkg"
GEMEINDE_LAYER = "tlm_hoheitsgebiet"

def get_gemeinden(data):
    gemeinden = gpd.read_file(SB3D_FILE_PATH, layer=GEMEINDE_LAYER)
    gemeinden = gemeinden[["name", "geometry"]]
    gemeinden = gemeinden.rename(columns={"name": "gemeinde"})

    closest = data.sjoin_nearest(gemeinden, how='left', distance_col='distance', max_distance=100)
    closest = closest[["Name", "gemeinde"]]

    liste = []
    for row in data.itertuples():
        gefiltert = closest[closest.Name == row.Name]
        gemeinde = None
        if gefiltert["gemeinde"].count() != 0:
            gemeinde = gefiltert.iloc[0]["gemeinde"]
        liste.append({"gemeinde": gemeinde})
    return liste

if __name__ == "__main__":
    data = read_gipfel_koordinaten()
    liste = get_gemeinden(data)
    print(liste)

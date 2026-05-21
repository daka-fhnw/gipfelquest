import geopandas as gpd
from read_gipfel_koordinaten import read_gipfel_koordinaten

# https://www.swisstopo.admin.ch/de/landschaftsmodell-swissboundaries3d
SB3D_FILE_PATH = "quellen/swissBOUNDARIES3D_1_5_LV95_LN02.gpkg"
KANTON_LAYER = "tlm_kantonsgebiet"
KANTON_NR_ZU_NAME = {
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

def get_kantone(data):
    kantone = gpd.read_file(SB3D_FILE_PATH, layer=KANTON_LAYER)
    kantone = kantone[["name", "kantonsnummer", "geometry"]]
    kantone = kantone.rename(columns={"name": "kanton"})

    closest = data.sjoin_nearest(kantone, how='left', distance_col='distance', max_distance=100)
    closest = closest[["Name", "kantonsnummer", "kanton"]]

    liste = []
    for row in data.itertuples():
        gefiltert = closest[closest.Name == row.Name]
        kanton = None
        if gefiltert["kanton"].count() != 0:
            kanton_nr = gefiltert.iloc[0]["kantonsnummer"]
            kanton = KANTON_NR_ZU_NAME[kanton_nr]
        liste.append({"kanton": kanton})
    return liste

if __name__ == "__main__":
    data = read_gipfel_koordinaten()
    liste = get_kantone(data)
    print(liste)

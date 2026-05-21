import geopandas as gpd

def read_gipfel_koordinaten():
    return gpd.read_file("./data/gipfel-koordinaten.gpkg")

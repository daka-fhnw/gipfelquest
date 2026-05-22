import geopandas as gpd

def read_gipfel_koordinaten():
    #return gpd.read_file("./data/gipfel-koordinaten.gpkg")
    return gpd.read_file("./data/bekannte-gipfel-koordinaten.gpkg")

import geopandas as gpd
 
data = gpd.read_file("./quellen/Bekannte_Berggipfel_2.gpkg")

data["Name"] = data["name"]
data["Hoehe"] = data["hoehe"].str.replace(" m", "", regex=False).astype(float)
data["geometry"] = data["geometry"].force_2d()

data = data[["Name", "geometry", "Hoehe"]]
data.to_file("data/bekannte-gipfel-koordinaten.gpkg", driver="GPKG")

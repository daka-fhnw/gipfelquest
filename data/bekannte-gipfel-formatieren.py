import geopandas as gpd
 
data = gpd.read_file("./quellen/Bekannte_Berggipfel_2_alle_mit_Region.gpkg")

data["Name"] = data["name"]
data["Hoehe"] = data["hoehe"].str.replace(" m", "", regex=False).astype(float)
data["geometry"] = data["geometry"].force_2d()
data["Region"] = data["region"]

data = data[["Name", "geometry", "Hoehe", "Region" ]]
data.to_file("data/bekannte-gipfel-koordinaten.gpkg", driver="GPKG")

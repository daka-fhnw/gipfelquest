import geopandas as gpd
 
data = gpd.read_file("./quellen/Berggipfel_unbereinigt_2.gpkg")

bergipfel_buchstaben = data[data["Name"].str.match("^[A-Za-z]", na=False)].explode()

bergipfel_clean = bergipfel_buchstaben.copy() 

bergipfel_clean["Name"] = bergipfel_clean["Name"].str.replace(r"\s*\(.*\)", "", regex=True)

bergipfel= bergipfel_clean[["Name", "geometry"]]
bergipfel["Hoehe"]= bergipfel.geometry.apply(lambda g: g.z)
bergipfel["geometry"]= bergipfel["geometry"].force_2d()
bergipfel_4000= bergipfel.query("Hoehe >= 4000")
bergipfel_4000.to_file("data/gipfel-koordinaten.gpkg", driver="GPKG")

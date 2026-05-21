import geopandas as gpd
import pandas as pd

DATEIPFAD = "quellen/swissnames3d_2026_2056.gpkg"
POLY_LAYER = "swissnames3d_ply"

relevante_arten = ["Grossregion", "Gebiet", "Haupttal", "Landschaftsname", "Gletscher", "Huegelzug"]
def load_data():
    Gipfel = gpd.read_file("data/gipfel-koordinaten.csv", crs="EPSG:2056")
    Gipfel = gpd.GeoDataFrame(
        Gipfel,
        geometry=gpd.points_from_xy(Gipfel["easting"], Gipfel["northing"]),
        crs="EPSG:2056"
    )

    namen = gpd.read_file(DATEIPFAD, layer=POLY_LAYER)
    namen = namen.loc[namen["sprachcode"] == "Hochdeutsch inkl. Lokalsprachen"]
    namen = namen.loc[namen["objektart"].isin(relevante_arten)]
    namen = namen[["name", "objektart", "objektklasse_tlm", "geometry"]]

    return Gipfel, namen

def join_normal(Gipfel, namen):
    namen_ohne_gletscher = namen[namen["objektart"] != "Gletscher"]

    j = gpd.sjoin(
        Gipfel,
        namen_ohne_gletscher,
        how="left",
        predicate="within"
    ).rename(columns={"name_right": "objektname", "name_left": "name"})

    return j[["name", "objektart", "objektname", "geometry"]]

def join_border(Gipfel, namen):
    namen_ohne_gletscher = namen[namen["objektart"] != "Gletscher"]

    Gipfel_buffer = Gipfel.copy()
    Gipfel_buffer["buffer_grenze"] = Gipfel_buffer.geometry.buffer(200)

    j = gpd.sjoin(
        Gipfel_buffer.set_geometry("buffer_grenze"),
        namen_ohne_gletscher,
        how="left",
        predicate="intersects"
    ).rename(columns={"name_right": "objektname", "name_left": "name"})

    if "geometry_left" in j.columns:
        j = j.drop(columns=["geometry_left"])
    if "geometry_right" in j.columns:
        j = j.rename(columns={"geometry_right": "geometry"})

    return j[["name", "objektart", "objektname", "geometry"]]

def join_gletscher(Gipfel, namen):
    gletscher = namen[namen["objektart"] == "Gletscher"]

    Gipfel_buffer = Gipfel.copy()
    Gipfel_buffer["buffer_gletscher"] = Gipfel_buffer.geometry.buffer(1000)

    j = gpd.sjoin(
        Gipfel_buffer.set_geometry("buffer_gletscher"),
        gletscher,
        how="left",
        predicate="intersects"
    ).rename(columns={"name_right": "objektname", "name_left": "name"})

    if "geometry_left" in j.columns:
        j = j.drop(columns=["geometry_left"])
    if "geometry_right" in j.columns:
        j = j.rename(columns={"geometry_right": "geometry"})

    return j[["name", "objektart", "objektname", "geometry"]]

def combine_and_filter(join_normal_df, join_border_df, join_gletscher_df):
    joined = pd.concat(
        [join_normal_df, join_border_df, join_gletscher_df],
        ignore_index=True
    )

    # Distanz zum Polygonzentrum
    joined["centroid"] = joined.geometry.centroid
    joined["distanz"] = joined.apply(
        lambda r: r.geometry.distance(r.centroid),
        axis=1
    )

    # Pro Objektart nur den nächsten behalten
    idx = joined.groupby(["name", "objektart"])["distanz"].idxmin()
    joined = joined.loc[idx].drop(columns=["centroid", "distanz"])

    return joined

def main():
    Gipfel, namen = load_data()

    j1 = join_normal(Gipfel, namen)
    j2 = join_border(Gipfel, namen)
    j3 = join_gletscher(Gipfel, namen)

    joined = combine_and_filter(j1, j2, j3)

    result = (
        joined.groupby("name")
        .apply(lambda x: {row.objektart: row.objektname for _, row in x.iterrows()})
        .reset_index()
        .rename(columns={0: "objekte"})
    )

    print(result)


if __name__ == "__main__":
    main()

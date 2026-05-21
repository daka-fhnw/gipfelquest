import geopandas as gpd
import pandas as pd
from read_gipfel_koordinaten import read_gipfel_koordinaten

DATEIPFAD = "quellen/swissnames3d_2026_2056.gpkg"
POLY_LAYER = "swissnames3d_ply"

RELEVANTE_ARTEN = [
    "Grossregion",
    "Gebiet",
    "Haupttal",
    "Landschaftsname",
    "Gletscher",
    "Huegelzug"
]

def load_namen():
    namen = gpd.read_file(DATEIPFAD, layer=POLY_LAYER)

    moegliche_namen = [
        "name",
        "NAME",
        "Objektname",
        "OBJNAME",
        "objektname",
        "objektname_tlm",
        "objektname_de",
        "objektname_offiziell"
    ]

    name_spalte = next(
        (c for c in moegliche_namen if c in namen.columns),
        None
    )

    if name_spalte is None:
        raise ValueError("Keine Namensspalte gefunden")

    namen = (
        namen.rename(columns={name_spalte: "objektname"})
        .query("sprachcode == 'Hochdeutsch inkl. Lokalsprachen'")
    )

    namen = namen[namen["objektart"].isin(RELEVANTE_ARTEN)]

    return namen[
        ["objektname", "objektart", "objektklasse_tlm", "geometry"]
    ]


def perform_join(data, namen, predicate, buffer=None):
    data = data.copy()

    if buffer:
        data["geometry"] = data.geometry.buffer(buffer)

    j = gpd.sjoin(
        data,
        namen,
        how="left",
        predicate=predicate
    )

    return j[["Name", "objektart", "objektname", "geometry"]]

def combine_and_filter(*joins):
    joined = pd.concat(joins, ignore_index=True)

    joined["centroid"] = joined.geometry.centroid

    # Distanz Polygon → eigenes Zentrum
    joined["distanz"] = (
        joined.geometry.distance(joined["centroid"])
    )

    idx = (
        joined.groupby(["Name", "objektart"])
        ["distanz"]
        .idxmin()
    )

    return joined.loc[idx].drop(
        columns=["centroid", "distanz"]
    )

def get_gebietsname(data):
    namen = load_namen()

    normal = perform_join(
        data,
        namen[namen["objektart"] != "Gletscher"],
        predicate="within"
    )

    border = perform_join(
        data,
        namen[namen["objektart"] != "Gletscher"],
        predicate="intersects",
        buffer=200
    )

    gletscher = perform_join(
        data,
        namen[namen["objektart"] == "Gletscher"],
        predicate="intersects",
        buffer=1000
    )

    joined = combine_and_filter(
        normal,
        border,
        gletscher
    )

    result = (
        joined.groupby("Name")
        .apply(
            lambda x: {
                r.objektart: r.objektname
                for _, r in x.iterrows()
            }
        )
        .to_dict()
    )

    liste = []

    for row in data.itertuples():
        eintrag = {
            "gipfel": row.Name,
            "easting": row.geometry.x,
            "northing": row.geometry.y
        }

        eintrag.update(
            result.get(row.Name, {})
        )

        liste.append(eintrag)

    return liste

if __name__ == "__main__":
    data = read_gipfel_koordinaten()
    liste = get_gebietsname(data)

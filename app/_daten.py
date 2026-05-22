import pandas as pd
from pandas import DataFrame, Series
from _konstanten import ANTWORT_OPTIONEN, ANZAHL_GIPFEL


def get_gipfel_daten() -> DataFrame:
    gipfel_daten = pd.read_json("data/gipfel-daten.json").reset_index(drop=True)
    gipfel_daten.insert(0, column="id", value=gipfel_daten.index + 1)
    return gipfel_daten

def get_gipfel_auswahl(gipfel_alle: DataFrame, region="alle Berge") -> DataFrame:
    if region != "alle Berge":
        gipfel_region = gipfel_region = gipfel_alle[gipfel_alle["region"] == region]
    else:
        gipfel_region = gipfel_alle
    return gipfel_region.sample(n=ANZAHL_GIPFEL).reset_index(drop=True)

def get_antwort_optionen(gipfel_alle: DataFrame, gipfel_zeile: Series) -> DataFrame:
    alle_ohne_gipfel = gipfel_alle[gipfel_alle["id"] != gipfel_zeile["id"]]
    falsche_optionen = alle_ohne_gipfel.sample(ANTWORT_OPTIONEN - 1)
    alle_optionen = pd.concat((gipfel_zeile.to_frame().T, falsche_optionen), ignore_index=True)
    durchmischt = alle_optionen.sample(frac=1).reset_index(drop=True)
    return durchmischt

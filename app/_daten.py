import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from _konstanten import ANTWORT_OPTIONEN, ANZAHL_GIPFEL, REGION_ALLE

def get_gipfel_daten() -> DataFrame:
    gipfel_daten = pd.read_json("data/gipfel-daten.json").reset_index(drop=True)
    gipfel_daten = gipfel_daten.replace({np.nan: None})
    gipfel_daten.insert(0, column="id", value=gipfel_daten.index + 1)
    return gipfel_daten

def filtern_nach_region(gipfel_alle: DataFrame, region: str) -> DataFrame:
    if region != REGION_ALLE:
        return gipfel_alle[gipfel_alle["region"] == region]
    return gipfel_alle

def get_gipfel_auswahl(gipfel_alle: DataFrame, region: str = REGION_ALLE) -> DataFrame:
    gefiltert = filtern_nach_region(gipfel_alle, region)
    return gefiltert.sample(n=ANZAHL_GIPFEL).reset_index(drop=True)

def get_antwort_optionen(gipfel_alle: DataFrame, gipfel_zeile: Series, region: str = REGION_ALLE) -> DataFrame:
    gefiltert = filtern_nach_region(gipfel_alle, region)
    ohne_gipfel = gefiltert[gefiltert["id"] != gipfel_zeile["id"]]
    falsche_optionen = ohne_gipfel.sample(ANTWORT_OPTIONEN - 1)
    alle_optionen = pd.concat((gipfel_zeile.to_frame().T, falsche_optionen), ignore_index=True)
    durchmischt = alle_optionen.sample(frac=1).reset_index(drop=True)
    return durchmischt

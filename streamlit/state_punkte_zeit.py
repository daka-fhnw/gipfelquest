import time
import streamlit as st
import pandas as pd
from pandas import DataFrame, Series

STATE_KEY = "app-state"

START_SEITE = 1
SPIEL_SEITE = 2
ERGEBNIS_SEITE = 3

ZEIT_SEKUNDEN = 60
MERKMAL_ZEIT_ABZUG = 10
RESTZEIT_FAKTOR = 1
ANZAHL_GIPFEL = 10
ANTWORT_OPTIONEN = 4

class SpielState: 
    punkte: int = 0
    start_zeit: int = 0
    zeit_abzug: int = 0
    gipfel_auswahl: DataFrame = DataFrame([])
    gipfel_index: int = 0
    antwort_optionen: DataFrame = DataFrame([])

class ErgebnisState:
    punkte: int = 0

class AppState:
    gipfel_alle: DataFrame = DataFrame([])
    seite: int = START_SEITE
    spiel: SpielState | None = None
    ergebnis: ErgebnisState | None = None

def get_state() -> AppState: 
    if STATE_KEY not in st.session_state:
        st.session_state[STATE_KEY] = AppState()
    return st.session_state[STATE_KEY]

state = get_state()
if state.gipfel_alle.empty:
    gipfel_daten = pd.read_json("data/gipfel-daten.json").reset_index(drop=True)
    gipfel_daten.insert(0, column="id", value=gipfel_daten.index + 1)
    state.gipfel_alle = gipfel_daten

def get_gipfel_daten() -> DataFrame:
    return pd.read_json("data/gipfel-daten.json").reset_index(drop=True)

def get_gipfel_auswahl() -> DataFrame:
    return state.gipfel_alle.sample(n=ANZAHL_GIPFEL).reset_index(drop=True)

def get_gipfel_zeile() -> Series:
    return state.spiel.gipfel_auswahl.iloc[state.spiel.gipfel_index]

def get_antwort_optionen() -> DataFrame:
    gipfel_zeile = get_gipfel_zeile()
    alle_ohne_gipfel = state.gipfel_alle[state.gipfel_alle["id"] != gipfel_zeile["id"]]
    falsche_optionen = alle_ohne_gipfel.sample(ANTWORT_OPTIONEN - 1)
    alle_optionen = pd.concat((gipfel_zeile.to_frame().T, falsche_optionen), ignore_index=True)
    durchmischt = alle_optionen.sample(frac=1).reset_index(drop=True)
    return durchmischt

def spiel_starten(): 
    state.seite = SPIEL_SEITE
    state.spiel = SpielState()
    state.spiel.punkte = 0
    state.spiel.zeit_abzug = 0
    state.spiel.start_zeit = time.time()
    state.spiel.gipfel_auswahl = get_gipfel_auswahl()
    state.spiel.antwort_optionen = get_antwort_optionen()

def spiel_aufgeben():
    state.seite = START_SEITE
    state.spiel = None
    state.ergebnis = None

def spiel_beendet():
    state.seite = ERGEBNIS_SEITE
    state.ergebnis = ErgebnisState()
    state.ergebnis.punkte = state.spiel.punkte
    state.spiel = None

def naechster_gipfel():
    state.spiel.gipfel_index += 1
    total = state.spiel.gipfel_auswahl.shape[0]
    if state.spiel.gipfel_index >= total:
        spiel_beendet()
        return
    state.spiel.zeit_abzug = 0
    state.spiel.start_zeit = time.time()
    state.spiel.antwort_optionen = get_antwort_optionen()

def get_restzeit() -> int:
    abzug = state.spiel.zeit_abzug
    verstrichen = time.time() - state.spiel.start_zeit
    return round(ZEIT_SEKUNDEN - verstrichen - abzug)

def zeit_abgelaufen():
    naechster_gipfel()
    st.rerun()

def falsche_antwort():
    naechster_gipfel()

def richtige_antwort():
    restzeit = get_restzeit()
    state.spiel.punkte += int(restzeit * RESTZEIT_FAKTOR)
    naechster_gipfel()

def zeit_abzug(wert: int):
    state.spiel.zeit_abzug += wert

def start_seite():
    st.markdown("# Willkomen")
    st.button("Starten", on_click=spiel_starten)

def gipfel_anzeige():
    st.markdown(f"## Berggipfel {state.spiel.gipfel_index + 1}")

@st.fragment(run_every=1)
def zeit_anzeige():
    restzeit = get_restzeit()
    if restzeit <= 0:
        zeit_abgelaufen()
    minuten, sekunden = divmod(max(restzeit, 0), 60)
    zeit_str = '{:02}:{:02}'.format(int(minuten), int(sekunden))
    st.markdown(f"### Zeit: {zeit_str}")

def punkt_anzeige():
    st.markdown(f"### Punkte: {state.spiel.punkte}")

def optionen_anzeige():
    richtige_zeile = get_gipfel_zeile()
    for zeile in state.spiel.antwort_optionen.itertuples():
        if (richtige_zeile["id"] == zeile.id):
            st.button(f"{zeile.name} (richtig)", on_click=richtige_antwort)
        else:
            st.button(zeile.name, on_click=falsche_antwort)

def spiel_seite():
    st.markdown("# Spiel")
    st.button("Aufgeben", on_click=spiel_aufgeben)
    st.button("Aufklappen", on_click=zeit_abzug, args=[10])
    gipfel_anzeige()
    zeit_anzeige()
    punkt_anzeige()
    optionen_anzeige()

def ergebnis_seite():
    st.markdown("# Ergebnis")
    st.markdown(f"## Punkte: {state.ergebnis.punkte}")
    st.button("Zurück", on_click=spiel_aufgeben)

if state.seite == START_SEITE:
    start_seite()
elif state.seite == SPIEL_SEITE:
    spiel_seite()
elif state.seite == ERGEBNIS_SEITE:
    ergebnis_seite()

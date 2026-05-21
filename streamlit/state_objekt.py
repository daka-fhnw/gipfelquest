import streamlit as st
from pandas import DataFrame

STATE_KEY = "app-state"
START_SEITE = 1
SPIEL_SEITE = 2
ERGEBNIS_SEITE = 3

class SpielState: 
    gipfel_auswahl: DataFrame
    gipfel_index: int = 0
    antwort_optionen: DataFrame
    punkte: int = 100
    start_zeit: int

class ErgebnisState:
    punkte: int

class AppState:
    gipfel_alle: DataFrame
    seite: int = START_SEITE
    spiel: SpielState | None
    ergebnis: ErgebnisState | None

def get_state() -> AppState: 
    if STATE_KEY not in st.session_state:
        st.session_state[STATE_KEY] = AppState()
    return st.session_state[STATE_KEY]

state = get_state()

def spiel_starten(): 
    state.seite = SPIEL_SEITE
    state.spiel = SpielState()

def spiel_aufgeben():
    state.seite = START_SEITE
    state.spiel = None

if state.seite == START_SEITE:
    with st.container():
        st.markdown("# Willkomen")
        if st.button("Starten"):
            spiel_starten()

if state.seite == SPIEL_SEITE:
    with st.container():
        st.markdown("# Spiel")
        if st.button("Aufgeben"):
            spiel_aufgeben()
        st.markdown(f"{state.spiel.punkte}")
        if st.button("punkte"):
            state.spiel.punkte += 1
        if st.button("rerun"):
            st.rerun()

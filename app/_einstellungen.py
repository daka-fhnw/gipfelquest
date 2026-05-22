import streamlit as st

from _konstanten import REGION_ALLE, REGION_BERNER_WALLISER_ALPEN, REGION_INNERACHWEIZ_OSTSCHWEIZ, REGION_JURA_WESTSCHWEIZ, REGION_TESSIN_GRAUBUENDEN
from _state import AppState

REGIONEN_OPTIONEN = [
    REGION_ALLE, 
    REGION_BERNER_WALLISER_ALPEN,
    REGION_INNERACHWEIZ_OSTSCHWEIZ,
    REGION_JURA_WESTSCHWEIZ,
    REGION_TESSIN_GRAUBUENDEN,
]

def einstellungen_inhalt(state: AppState):
    auswahl_index = REGIONEN_OPTIONEN.index(state.einstellungen.region)
    region = st.radio("Mit welchen Bergen möchtest du spielen?", REGIONEN_OPTIONEN, index=auswahl_index)
    state.einstellungen.region = region
    st.button('Zurück', on_click=state.start_anzeigen)

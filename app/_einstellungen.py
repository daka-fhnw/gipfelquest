import streamlit as st

from _konstanten import REGION_ALLE, REGION_BERNER_WALLISER_ALPEN, REGION_INNERACHWEIZ_OSTSCHWEIZ, REGION_JURA_WESTSCHWEIZ, REGION_TESSIN_GRAUBUENDEN
from _state import AppState

REGION_KEY = "region_key"

REGIONEN_OPTIONEN = [
    REGION_ALLE, 
    REGION_BERNER_WALLISER_ALPEN,
    REGION_INNERACHWEIZ_OSTSCHWEIZ,
    REGION_JURA_WESTSCHWEIZ,
    REGION_TESSIN_GRAUBUENDEN,
]

def einstellungen_inhalt(state: AppState):
    def region_on_change():
        state.einstellungen.region = st.session_state[REGION_KEY]
    auswahl_index = REGIONEN_OPTIONEN.index(state.einstellungen.region)
    st.radio("Mit welchen Bergen möchtest du spielen?", REGIONEN_OPTIONEN, 
             index=auswahl_index, key=REGION_KEY, on_change=region_on_change)
    st.button('Zurück', on_click=state.start_anzeigen)

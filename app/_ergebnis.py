import streamlit as st

from _state import AppState

def ergebnis_inhalt(state: AppState):
    st.markdown("# Ergebnis")
    st.markdown(f"## Punkte: {state.ergebnis.punkte}")
    st.button("Zurück", on_click=state.start_anzeigen)

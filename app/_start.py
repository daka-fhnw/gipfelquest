import streamlit as st

from _state import AppState

def start_inhalt(state: AppState):
    st.markdown("# Willkomen")
    st.button("Starten", on_click=state.spiel_starten)

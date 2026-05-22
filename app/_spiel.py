import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from _state import AppState

def gipfel_anzeige(state: AppState):
    st.markdown(f"## Berggipfel {state.spiel.gipfel_index + 1}")

@st.fragment(run_every=1)
def zeit_anzeige(state: AppState, parent: DeltaGenerator = st):
    restzeit = state.get_restzeit()
    if restzeit <= 0:
        state.zeit_abgelaufen()
        st.rerun()
    minuten, sekunden = divmod(max(restzeit, 0), 60)
    zeit_str = '{:02}:{:02}'.format(int(minuten), int(sekunden))
    parent.markdown(f"### Zeit: {zeit_str}")

def punkt_anzeige(state: AppState, parent: DeltaGenerator = st):
    parent.markdown(f"### Punkte: {state.spiel.punkte}")

def optionen_anzeige(state: AppState, parent: DeltaGenerator = st):
    richtige_zeile = state.get_gipfel_zeile()
    for zeile in state.spiel.antwort_optionen.itertuples():
        if (richtige_zeile["id"] == zeile.id):
            parent.button(f"{zeile.name} (richtig)", on_click=state.richtige_antwort)
        else:
            parent.button(zeile.name, on_click=state.falsche_antwort)

def spiel_inhalt(state: AppState):
    st.markdown("# Spiel")
    st.button("Aufgeben", on_click=state.start_anzeigen)
    gipfel_anzeige(state)
    zeit_anzeige(state)
    punkt_anzeige(state)
    optionen_anzeige(state)
    st.markdown("# Merkmale")
    with state.merkmal_box("merkmal1", "Merkmal 1", st):
        st.markdown("Test 123...")
    with state.merkmal_box("merkmal2", "Merkmal 2", st):
        st.markdown("Test 123...")
    with state.merkmal_box("merkmal3", "Merkmal 3", st):
        st.markdown("Test 123...")
    with state.merkmal_box("merkmal4", "Merkmal 4", st):
        st.markdown("Test 123...")

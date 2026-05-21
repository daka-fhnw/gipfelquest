import streamlit as st
import pandas as pd

#Auswahl Berg und Anwortmöglichkeiten
alle_berge = pd.read_json("data/gipfel-daten.json").reset_index(drop=True)
if 'richtiger_berg' not in st.session_state:
    st.session_state['richtiger_berg'] = alle_berge.sample(n=1, random_state=None)
if 'falsche_berge' not in st.session_state:
    st.session_state['falsche_berge'] = alle_berge.drop(st.session_state.richtiger_berg.index).sample(n=3, random_state=None)
if 'antwortmoeglichkeiten' not in st.session_state:
    st.session_state['antwortmoeglichkeiten'] = pd.concat([st.session_state.richtiger_berg, st.session_state.falsche_berge], ignore_index=True).sample(frac=1).reset_index(drop=True)

# richtiger_berg = alle_berge.sample(n=1, random_state=None)
# andere_berge = alle_berge.drop(richtiger_berg.index)
# falsche_berge= andere_berge.sample(n=3, random_state=None)
# antwortmoeglichkeiten = pd.concat([richtiger_berg, falsche_berge], ignore_index=True)
# antwortmoeglichkeiten_random = antwortmoeglichkeiten.sample(frac=1).reset_index(drop=True)
st.write(st.session_state.richtiger_berg["name"],st.session_state.falsche_berge["name"], st.session_state.antwortmoeglichkeiten["name"])

gewaehlter_berg = st.radio(
    "Welcher Berg ist es?",
    st.session_state.antwortmoeglichkeiten["name"]  # Direkt aus Spalte

)





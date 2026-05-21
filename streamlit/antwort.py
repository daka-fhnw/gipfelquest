import streamlit as st
import pandas as pd

alle_berge = pd.read_json("data/gipfel-daten.json")
richtiger_berg = alle_berge.sample(n=1, random_state=None)
andere_berge = alle_berge.drop(richtiger_berg.index)
print(richtiger_berg, andere_berge)

gewaehlter_berg = st.radio(
    "Welcher Berg ist es?",
    ["***Drama***", "Documentary :movie_camera:"],
)

if gewaehlter_berg == ":rainbow[Comedy]":
    st.write("You selected comedy.")
else:
    st.write("You didn't select comedy.")


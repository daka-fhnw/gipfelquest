import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

alle_berge = pd.read_json("data/gipfel-daten.json").reset_index(drop=True)
if 'richtiger_berg' not in st.session_state:
    st.session_state['richtiger_berg'] = alle_berge.sample(n=1, random_state=None)

st.set_page_config(layout="wide", page_title="Gipfelquest")

st.title("Willkommen zu Gipfelquest!",text_alignment="center",width="stretch")


schweiz = gpd.read_file("streamlit/LANDESGEBIET.gpkg")

punkt_x = st.session_state.richtiger_berg['koordinate_x'].iloc[0]
punkt_y = st.session_state.richtiger_berg['koordinate_y'].iloc[0]

fig, ax = plt.subplots(figsize=(12,12))

schweiz.plot(
    ax=ax,
    facecolor="white",
    edgecolor="black",
    linewidth=1
)

ax.scatter(
    punkt_x,
    punkt_y,
    s=80,
    color="red"
)

ax.axis("off")

plt.tight_layout()

st.pyplot(fig)
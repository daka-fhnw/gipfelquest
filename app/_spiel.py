import streamlit as st
from streamlit.delta_generator import DeltaGenerator
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes
from _state import AppState
import numpy as np
import rasterio

def gipfel_anzeige(state: AppState):
    st.markdown(f"## Berg {state.spiel.gipfel_index + 1}")

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

def plot_profile_data(data: tuple[list[float], list[float]], 
                      ax: Axes) -> None:
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    x, y = zip(*data)

    # Feststellung Extremwerte für spätere gleiche Einfärbung
    y_E = np.array([p[1] for p in data_E])
    y_N = np.array([p[1] for p in data_N])
    global_min = min(y_E.min(), y_N.min())

    ax.plot(x,y,color="black",linewidth=1)  # <- Design Graph, vielleicht anpassan an Gesamtdesign
    ax.fill_between(x,y,global_min,color="lightgray") # <- Hintergrundfarbe Profil, vielleicht anpassan an Gesamtdesign
    ax.set_facecolor("#D3ECF8") # <- Hintergrundfarbe Himmel, vielleicht anpassan an Gesamtdesign


def spiel_inhalt(state: AppState):
   
    gipfelzeile = state.get_gipfel_zeile()
    st.markdown("# Gipfelquest")

    data_E = gipfelzeile["profil_ost"]
    data_N = gipfelzeile["profil_nord"]
    fig = plt.figure()
    gs = fig.add_gridspec(1, 2, wspace=0)
    (ax1, ax2) = gs.subplots(sharey=True)
    plot_profile_data(data_E, ax1)
    plot_profile_data(data_N, ax2)
    ax1.set_title("Profil von West nach Ost")
    ax2.set_title("Profil von Süd nach Nord")

    st.pyplot(fig)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("## Merkmale")
    
        with state.merkmal_box("merkmal4", "Merkmal Koordinaten / Höhe", st):
            schweiz = rasterio.open("streamlit/Uebersichtskarte_Schweiz.tif")
            r = schweiz.read(1)
            g = schweiz.read(2)
            b = schweiz.read(3)
            rgb = np.dstack((r, g, b))

            punkt_x = gipfelzeile['koordinate_x']
            punkt_y = gipfelzeile['koordinate_y']

            row, col = schweiz.index(punkt_x, punkt_y)

            fig, ax = plt.subplots(figsize=(15, 9))

            ax.imshow(rgb, interpolation="nearest")
            ax.plot(col, row, "ro", markersize=8)
        
            ax.axis("off")
            st.pyplot(fig)

            st.write(f"Ost: {gipfelzeile['koordinate_x']}")
            st.write(f"Nord: {gipfelzeile['koordinate_y']}")
            st.write(f"Höhe: {gipfelzeile['hoehe']}")
        
        with state.merkmal_box("merkmal1", "Metadaten Berg", st):
            st.write(f"Kanton: {gipfelzeile['kanton']}")                                     #Gebietsnamen/ Kanton")
            st.write(f"Gebiet: {gipfelzeile['gebiet']}")
            st.write(f"Haupttal: {gipfelzeile['haupttal']}")
            st.write(f"Gletscher: {gipfelzeile['gletscher']}")
            st.write(f"Gemeinde: {gipfelzeile['gemeinde']}")
            st.write(f"Landschaftsname: {gipfelzeile['landschaftsname']}")

    with col2:
        gipfel_anzeige(state)

        with state.merkmal_box("merkmal2", "Merkmal Orthophoto / Region", st):
            st.image(gipfelzeile["ortho_url"])

    with col3: 
        zeit_anzeige(state)
        punkt_anzeige(state)
    
        st.markdown("## Optionen")
        optionen_anzeige(state)

    
    st.button("Aufgeben", on_click=state.start_anzeigen)
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from _state import AppState
import numpy as np
import rasterio

def gipfel_anzeige(state: AppState):
    st.markdown(f"## Berg {state.spiel.gipfel_index + 1}")

@st.fragment(run_every=1)
def zeit_und_punkte_anzeige(state: AppState):
    restzeit = state.get_restzeit()
    if restzeit <= 0:
        state.zeit_abgelaufen()
        st.rerun()
    minuten, sekunden = divmod(max(restzeit, 0), 60)
    zeit_str = '{:02}:{:02}'.format(int(minuten), int(sekunden))
    st.markdown(f"### Zeit: {zeit_str}, Punkte: {state.spiel.punkte}")

def optionen_anzeige(state: AppState):
    st.markdown("### Antwortmöglichkeiten")
    richtige_zeile = state.get_gipfel_zeile()
    for zeile in state.spiel.antwort_optionen.itertuples():
        funktion = state.richtige_antwort if richtige_zeile["id"] == zeile.id else state.falsche_antwort
        st.button(zeile.name, on_click=funktion, use_container_width=True)

def profil_plot(data: list[list[float,float]], ax: Axes, global_min: int):
    x, y = zip(*data)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.plot(x, y, color="black", linewidth=1)  # <- Design Graph, vielleicht anpassan an Gesamtdesign
    ax.fill_between(x, y, global_min, color="lightgray") # <- Hintergrundfarbe Profil, vielleicht anpassan an Gesamtdesign
    ax.set_facecolor("#D3ECF8") # <- Hintergrundfarbe Himmel, vielleicht anpassan an Gesamtdesign

def profil_merkmal(state: AppState):
    gipfel_zeile = state.get_gipfel_zeile()
    data_E = gipfel_zeile["profil_ost"]
    data_N = gipfel_zeile["profil_nord"]

    # Feststellung Extremwerte für spätere gleiche Einfärbung
    y_E = np.array([p[1] for p in data_E])
    y_N = np.array([p[1] for p in data_N])
    global_min = min(y_E.min(), y_N.min())

    fig = plt.figure()
    gs = fig.add_gridspec(1, 2, wspace=0)
    (ax1, ax2) = gs.subplots(sharey=True)
    ax1.set_title("Profil von West nach Ost")
    ax2.set_title("Profil von Süd nach Nord")

    profil_plot(data_E, ax1, global_min)
    profil_plot(data_N, ax2, global_min)

    with st.expander("Bergprofil", expanded=True):
        st.pyplot(fig)

def koordinaten_hoehe_merkmal(state: AppState):
    gipfel_zeile = state.get_gipfel_zeile()
    with state.merkmal_box("merkmal_koord_hoehe", "Koordinaten / Höhe", st):
        schweiz = rasterio.open("streamlit/Uebersichtskarte_Schweiz.tif")
        r = schweiz.read(1)
        g = schweiz.read(2)
        b = schweiz.read(3)
        rgb = np.dstack((r, g, b))

        punkt_x = gipfel_zeile['koordinate_x']
        punkt_y = gipfel_zeile['koordinate_y']
        hoehe = gipfel_zeile["hoehe"]

        row, col = schweiz.index(punkt_x, punkt_y)

        fig, ax = plt.subplots(figsize=(15, 9))

        ax.imshow(rgb, interpolation="nearest")
        ax.plot(col, row, "ro", markersize=8)
        ax.axis("off")

        st.html(f"<b>Ost:</b> {punkt_x}, <b>Nord:</b> {punkt_y}, <b>Höhe:</b> {hoehe}")
        st.pyplot(fig)

def gebietsnamen_merkmal(state: AppState):
    gipfel_zeile = state.get_gipfel_zeile()
    with state.merkmal_box("merkmal_gebietsnamen", "Gebietsnamen", st):
        st.html(f"""<b>Kanton:</b> {gipfel_zeile['kanton'] or "-"}<br/>
                    <b>Gemeinde:</b> {gipfel_zeile['gemeinde'] or "-"}<br/>
                    <b>Gebiet:</b> {gipfel_zeile['gebiet'] or "-"}<br/>
                    <b>Haupttal:</b> {gipfel_zeile['haupttal'] or "-"}<br/>
                    <b>Gletscher:</b> {gipfel_zeile['gletscher'] or "-"}<br/>
                    <b>Landschaftsname:</b> {gipfel_zeile['landschaftsname'] or "-"}""")

def orthophoto_merkmal(state: AppState):
    gipfel_zeile = state.get_gipfel_zeile()
    with state.merkmal_box("merkmal_orthophoto", "Orthophoto / Region", st):
        st.image(gipfel_zeile["ortho_url"])

def spiel_hauptbereich(state: AppState):
    st.markdown(f"# Gipfelquest - Gipfel {state.spiel.gipfel_index + 1}")
    profil_merkmal(state)
    spalte1, spalte2 = st.columns(2)
    with spalte1:
        koordinaten_hoehe_merkmal(state)
        gebietsnamen_merkmal(state)
    with spalte2:
        orthophoto_merkmal(state)

def spiel_bereich_rechts(state: AppState):
    zeit_und_punkte_anzeige(state)
    st.button("Aufgeben", on_click=state.start_anzeigen)
    optionen_anzeige(state)

def spiel_inhalt(state: AppState):
    (haupt, rechts) = st.columns(spec=[0.7, 0.3])
    with haupt:
        spiel_hauptbereich(state)  
    with rechts:
        spiel_bereich_rechts(state)

    
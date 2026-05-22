import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import rasterio
import numpy as np


alle_berge = pd.read_json("data/gipfel-daten.json").reset_index(drop=True)
if 'richtiger_berg' not in st.session_state:
    st.session_state['richtiger_berg'] = alle_berge.sample(n=1, random_state=None)


st.set_page_config(layout="wide")  # wichtig für volle Breite
st.set_page_config(page_title="Gipfelquest")

     

st.title("Willkommen zu Gipfelquest!",text_alignment="center",width="stretch")


col1, col2, col3 = st.columns(3)

with col1:
    with st.expander("Merkmal: Schnitt Nord", expanded=True): st.write("")                  #Nordschnitt


    with st.expander("Merkmal: Koordinaten / Höhe"):  

        #Karte Schweiz mit Punkt
        schweiz = rasterio.open("streamlit/Uebersichtskarte_Schweiz.tif")
        r = schweiz.read(1)
        g = schweiz.read(2)
        b = schweiz.read(3)
        rgb = np.dstack((r, g, b))

        punkt_x = st.session_state.richtiger_berg['koordinate_x'].iloc[0]
        punkt_y = st.session_state.richtiger_berg['koordinate_y'].iloc[0]

        row, col = schweiz.index(punkt_x, punkt_y)

        fig, ax = plt.subplots(figsize=(15, 9))

        ax.imshow(rgb, interpolation="nearest")
        ax.plot(col, row, "ro", markersize=8)
    
        ax.axis("off")
        st.pyplot(fig)

        st.write(f"Ost: {st.session_state.richtiger_berg['koordinate_x'].iloc[0]}")
        st.write(f"Nord: {st.session_state.richtiger_berg['koordinate_y'].iloc[0]}")
        st.write(f"Höhe: {st.session_state.richtiger_berg['hoehe'].iloc[0]}")

    with st.expander("Merkmal: Ort Daten"):
        st.write(f"Kanton: {st.session_state.richtiger_berg['kanton'].iloc[0]} /                                     #Gebietsnamen/ Kanton")
        st.write(f"Gebiet: {st.session_state.richtiger_berg['gebiet'].iloc[0]}")
        st.write(f"Haupttal: {st.session_state.richtiger_berg['haupttal'].iloc[0]}")
        st.write(f"Gletscher: {st.session_state.richtiger_berg['gletscher'].iloc[0]}")
        st.write(f"Gemeinde: {st.session_state.richtiger_berg['gemeinde'].iloc[0]}")
        st.write(f"Landschaftsname: {st.session_state.richtiger_berg['landschaftsname'].iloc[0]}")


with col2:
    with st.expander("Merkmal: Schnitt Ost", expanded=True): st.write("")                   #Ostschnitt

    with st.expander("Merkmal: Orthophoto / Region"): 
        st.image(st.session_state.richtiger_berg["ortho_url"].iloc[0])  #Orthophoto
        st.write(f"Region: {st.session_state.richtiger_berg['grossregion'].iloc[0]}")
        

with col3:
    st.text('''Timer: 00:00 ''')
    st.text("Punktzahl: 100")

    st.text(st.session_state.richtiger_berg['name'].iloc[0])


import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

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
        schweiz = gpd.read_file("streamlit/LANDESGEBIET.gpkg")
        punkt_x = st.session_state.richtiger_berg['koordinate_x'].iloc[0]
        punkt_y = st.session_state.richtiger_berg['koordinate_y'].iloc[0]

        fig, ax = plt.subplots(figsize=(12,12))

        schweiz.plot(
            ax=ax,
            facecolor="white",
            edgecolor="black",
            linewidth=1)
        ax.scatter(
            punkt_x,
            punkt_y,
            s=150,
            color="red")

        ax.axis("off")
        plt.tight_layout()
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


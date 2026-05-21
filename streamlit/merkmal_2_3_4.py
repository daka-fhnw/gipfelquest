import streamlit as st
import pandas as pd

alle_berge = pd.read_json("data/gipfel-daten.json")
richtiger_berg = alle_berge.sample(n=1, random_state=None)


st.set_page_config(layout="wide")  # wichtig für volle Breite
st.set_page_config(page_title="Gipfelquest")

     

st.title("Willkommen zu Gipfelquest!",text_alignment="center",width="stretch")


col1, col2, col3 = st.columns(3)

with col1:
    with st.expander("Merkmal: Schnitt Nord", expanded=True): st.write("")

    with st.expander("Merkmal: Höhe / Koordinaten"): 
        st.write(f"Höhe: {richtiger_berg['hoehe'].iloc[0]}")
        st.write(f"Koordinate Ost: {richtiger_berg['koordinate_x'].iloc[0]}")
        st.write(f"Koordinate Nord: {richtiger_berg['koordinate_y'].iloc[0]}")

    with st.expander("Merkmal: Gebietsnamen / Kanton"): 
        st.write(f"Region: {richtiger_berg['Grossregion'].iloc[0]}")
        st.write(f"Kanton: {richtiger_berg['kanton'].iloc[0]}")
with col2:
    with st.expander("Merkmal: Schnitt Ost", expanded=True): st.write("")

    with st.expander("Merkmal: Orthophoto"): st.image(richtiger_berg["ortho_url"].iloc[0])
with col3:
    st.text('''Timer: 00:00 ''')
    st.text("Punktzahl: 1000")

    st.text(richtiger_berg['gipfel'].iloc[0])


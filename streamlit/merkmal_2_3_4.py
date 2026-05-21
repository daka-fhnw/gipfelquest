import streamlit as st
import pandas as pd

alle_berge = pd.read_json("data/gipfel-daten.json").reset_index(drop=True)
if 'richtiger_berg' not in st.session_state:
    st.session_state['richtiger_berg'] = alle_berge.sample(n=1, random_state=None)
if 'falsche_berge' not in st.session_state:
    st.session_state['falsche_berge'] = alle_berge.drop(st.session_state.richtiger_berg.index).sample(n=3, random_state=None)
if 'antwortmoeglichkeiten' not in st.session_state:
    st.session_state['antwortmoeglichkeiten'] = pd.concat([st.session_state.richtiger_berg, st.session_state.falsche_berge], ignore_index=True).sample(frac=1).reset_index(drop=True)



st.set_page_config(layout="wide")  # wichtig für volle Breite
st.set_page_config(page_title="Gipfelquest")

     

st.title("Willkommen zu Gipfelquest!",text_alignment="center",width="stretch")


col1, col2, col3 = st.columns(3)

with col1:
    with st.expander("Merkmal: Schnitt Nord", expanded=True): st.write("")                  #Nordschnitt

    with st.expander("Merkmal: Höhe / Koordinaten"):                                        #Höhe/ Koordinaten
        st.write(f"Höhe: {st.session_state.richtiger_berg['hoehe'].iloc[0]}")
        st.write(f"Koordinate Ost: {st.session_state.richtiger_berg['koordinate_x'].iloc[0]}")
        st.write(f"Koordinate Nord: {st.session_state.richtiger_berg['koordinate_y'].iloc[0]}")

    with st.expander("Merkmal: Gebiet / Gletscher / Tal"):                                     #Gebietsnamen/ Kanton
        st.write(f"Gebiet: {st.session_state.richtiger_berg['gebiet'].iloc[0]}")
        st.write(f"Haupttal: {st.session_state.richtiger_berg['haupttal'].iloc[0]}")
        st.write(f"Gletscher: {st.session_state.richtiger_berg['gletscher'].iloc[0]}")
        st.write(f"Gemeinde: {st.session_state.richtiger_berg['gemeinde'].iloc[0]}")
        st.write(f"Landschaftsname: {st.session_state.richtiger_berg['landschaftsname'].iloc[0]}")


with col2:
    with st.expander("Merkmal: Schnitt Ost", expanded=True): st.write("")                   #Ostschnitt

    with st.expander("Merkmal: Orthophoto / Ort"): 
        st.image(st.session_state.richtiger_berg["ortho_url"].iloc[0])  #Orthophoto
        st.write(f"Kanton: {st.session_state.richtiger_berg['kanton'].iloc[0]} /  Region: {st.session_state.richtiger_berg['grossregion'].iloc[0]}")
        

with col3:
    st.text('''Timer: 00:00 ''')
    st.text("Punktzahl: 100")

    st.text(st.session_state.richtiger_berg['name'].iloc[0])


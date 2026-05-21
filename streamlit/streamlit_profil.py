import streamlit as st

st.set_page_config(layout="wide")  # wichtig für volle Breite
st.set_page_config(page_title="Gipfelquest")

with st.columns(3)[1]:
     

     st.title("Willkommen zu Gipfelquest!",text_alignment="center")
     st.markdown(
        """ 
        Hier kannst du herausfinden, ob du die Berge so gut kennst wie du denkst. 
    
        Klicke auf den Button unten, um das Spiel zu starten. Viel Spaß! 
        """,text_alignment="center"
     )

col1, col2, col3 = st.columns(3)

with col1:
    ""
with col2:
    col1, col2 = st.columns(2)
    with col1:
        st.button("Anleitung")
    with col2:
        st.button("Spiel starten!",icon="🎉")
with col3:
    ""


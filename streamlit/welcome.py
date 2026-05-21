import streamlit as st

st.set_page_config(layout="wide")  # wichtig für volle Breite
st.set_page_config(page_title="Gipfelquest")

     

st.title("Willkommen zu Gipfelquest!",text_alignment="center",width="stretch")
st.markdown(
        """ 
        Finde heraus, ob du die Berge so gut kennst wie du denkst. Errate den Namen des Gipfeld anhand der verschiedenen Merkmale. 
        Je länger Zeit und je mehr Merkmale du brauchst, desto weniger Punkte bekommst du.
    
        Klicke auf den Button unten, um das Spiel zu starten. Viel Spass! 
        """,text_alignment="center"
     )

col1, col2, col3 = st.columns(3)

with col1:
    ""
with col2:
    if st.button("Spiel starten!",icon="🎉",icon_position="right",): st.snow()
with col3:
    ""


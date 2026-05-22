import streamlit as st

region_moeglichkeiten = ["alle Berge", "Berner/Walliser Alpen", "Innerschweiz/Ostschweiz", "Jura/Westschweiz", "Tessin/Graubünden"]

region = st.radio("Mit welchen Bergen möchtest du spielen?", region_moeglichkeiten)

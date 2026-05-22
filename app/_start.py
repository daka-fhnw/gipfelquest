import base64
import time as time
import streamlit as st

from _state import AppState

@st.cache_data
def hintergrund_als_base64():
    with open("data/Matterhorn.jpg", "rb") as img:
        return base64.b64encode(img.read()).decode()

def start_inhalt(state: AppState):
    img = hintergrund_als_base64()

    st.snow()

    st.html(f"""
    <style>
    .stApp {{
        background:
            linear-gradient(
                rgba(80,80,80,0.55),
                rgba(80,80,80,0.55)
            ),
            url("data:image/jpg;base64,{img}");
        background-size: cover;
    }} </style>""")

    st.html("""
        <h1 style='
            text-align: center;
            font-size: 80px;
            color: white;
            margin-top: 40px;
            margin-bottom: 0;
        '>
        Gipfelquest
        </h1>
        """)
    
    st.html("""
        <div style='
            text-align: center;
            font-size: 24px;
            margin-top: 0;
            color: white;
        '>    
            Erkenne bekannte Berge anhand ihrer Merkmale 🏔️<br/>
            Jeder zusätzliche Hinweis den du brauchst kostet Zeit ⏱️<br/>
            Bist du bereit für die Gipfelquest?
        </div>
        """)
    
    st.html("""
        <style>
        div.stButton > button {
            height: 50px;
            border-radius: 18px;
            background-color: #009ACD;
            color: white;
            margin-top: 30px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }
        div.stButton > button p {
            font-size: 22px;
        }
        div.stButton > button:hover {
            background-color: #29608f;
            transform: scale(1.05);
            transition: 0.2s;
        }
        </style>
        """)
    
    columns = st.columns((2, 1, 1, 2))
    columns[1].button('Spiel starten', on_click=state.spiel_starten)
    columns[2].button('Einstellungen', on_click=state.einstellungen_anzeigen)

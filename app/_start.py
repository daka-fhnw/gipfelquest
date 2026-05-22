import base64

import streamlit as st

from _state import AppState

def get_base64(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

img = get_base64("data/Matterhorn.jpg")

def start_inhalt(state: AppState):
    st.markdown(f"""
    <style>
    .stApp {{
        background:
            linear-gradient(
                rgba(80,80,80,0.55),
                rgba(80,80,80,0.55)
            ),
            url("data:image/jpg;base64,{img}");
        background-size: cover;
    }} </style>""", unsafe_allow_html=True)

    st.markdown("""
        <h1 style='
            text-align: center;
            font-size: 80px;
            color: white;
            margin-top: 40px;
        '>
        Gipfelquest
        </h1>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='
            text-align: center;
            font-size: 24px;
            margin-top: 60px;
            color: white;
        '>    
        Erkenne bekannte Berge anhand ihrer Merkmale 🏔️

        Jeder zusätzliche Hinweis den du brauchst kostet Zeit ⏱️

        Bist du bereit für die Gipfelquest?

        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
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
        """, unsafe_allow_html=True)

    columns = st.columns((2, 1, 2))
    columns[1].button('Start Game',use_container_width=True,on_click=state.spiel_starten)
    #st.button("Starten", on_click=state.spiel_starten)



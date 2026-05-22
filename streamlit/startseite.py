import streamlit as st
import base64


st.set_page_config(layout="wide",page_title="Gipfelquest")  # wichtig für volle Breite

def get_base64(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

img = get_base64("quellen/Matterhorn.jpg")

st.markdown(f"""
<style>
.stApp {{
    background:
        linear-gradient(
            rgba(100,20,100,0.55),
            rgba(100,100,100,0.55)
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


columns = st.columns((3, 1, 3))
button_pressed = columns[1].button('Start Game',use_container_width=True)
if button_pressed:
    st.snow() 




import streamlit as st
import json
import os


HIGHSCORE_FILE = "streamlit/highscores.json"

# Platzhalter
DEFAULT_DATA = {
    "Spieler1": "---", "score1": 0,
    "Spieler2": "---", "score2": 0,
    "Spieler3": "---", "score3": 0,
    "Spieler4": "---", "score4": 0,
    "Spieler5": "---", "score5": 0,
}

def load_scores():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_DATA.copy()

def save_scores(data):
    with open(HIGHSCORE_FILE, "w") as f:
        json.dump(data, f, indent=4)


st.set_page_config(layout="wide", page_title="Gipfelquest")

state = get_state()
punkte = state.ergebnis.punkte


if "scores" not in st.session_state:
    st.session_state.scores = load_scores()


Spieler1 = st.session_state.scores["Spieler1"]
Spieler2 = st.session_state.scores["Spieler2"]
Spieler3 = st.session_state.scores["Spieler3"]
Spieler4 = st.session_state.scores["Spieler4"]
Spieler5 = st.session_state.scores["Spieler5"]

score1 = st.session_state.scores["score1"]
score2 = st.session_state.scores["score2"]
score3 = st.session_state.scores["score3"]
score4 = st.session_state.scores["score4"]
score5 = st.session_state.scores["score5"]


st.title("Ergebnis", text_alignment="center", width="stretch")
st.markdown(f"Deine Punktzahl: {punkte}", text_alignment="center")

left_space, col1, col2, right_space = st.columns([2,1,1,2])

with col1:
    st.button(
        "Nochmal spielen!",
        use_container_width=True,
        on_click=spiel_starten
    )

with col2:
    st.button(
        "Zurück zur Startseite",
        use_container_width=True,
        on_click=spiel_aufgeben        
    )


if punkte > score1:
    st.markdown("Herzlichen Glückwunsch! Du hast den ersten Platz erreicht!", text_alignment="center")
    erster = st.text_input("Geben Sie hier Ihren Usernamen ein:")
    if erster:
        Spieler1 = erster
        score1 = punkte
        score2 = score1
        score3 = score2
        score4 = score3
        score5 = score4

if punkte > score2 and punkte <= score1:
    st.markdown("Glückwunsch! Du hast den zweiten Platz erreicht!", text_alignment="center")
    zweiter = st.text_input("Geben Sie Ihren Usernamen ein:")
    if zweiter:
        Spieler2 = zweiter
        score2 = punkte
        score3 = score2
        score4 = score3
        score5 = score4

if punkte > score3 and punkte <= score2:
    st.markdown("Glückwunsch! Du hast den dritten Platz erreicht!", text_alignment="center")
    dritter = st.text_input("Geben Sie Ihren Usernamen ein:")
    if dritter:
        Spieler3 = dritter
        score3 = punkte
        score4 = score3
        score5 = score4

if punkte > score4 and punkte <= score3:
    st.markdown("Glückwunsch! Du hast den vierten Platz erreicht!", text_alignment="center")
    vierter = st.text_input("Geben Sie Ihren Usernamen ein:")
    if vierter:
        Spieler4 = vierter
        score4 = punkte
        score5 = score4

if punkte > score5 and punkte <= score4:
    st.markdown("Glückwunsch! Du hast den fünften Platz erreicht!", text_alignment="center")
    fuenfter = st.text_input("Geben Sie Ihren Usernamen ein:")
    if fuenfter:
        Spieler5 = fuenfter
        score5 = punkte

st.session_state.scores = {
    "Spieler1": Spieler1, "score1": score1,
    "Spieler2": Spieler2, "score2": score2,
    "Spieler3": Spieler3, "score3": score3,
    "Spieler4": Spieler4, "score4": score4,
    "Spieler5": Spieler5, "score5": score5,
}

save_scores(st.session_state.scores)

st.markdown("### Die Top 5 Highscores:", text_alignment="center")
st.markdown(f"Nr. 1: {Spieler1} – {score1} Punkte", text_alignment="center")
st.markdown(f"Nr. 2: {Spieler2} – {score2} Punkte", text_alignment="center")
st.markdown(f"Nr. 3: {Spieler3} – {score3} Punkte", text_alignment="center")
st.markdown(f"Nr. 4: {Spieler4} – {score4} Punkte", text_alignment="center")
st.markdown(f"Nr. 5: {Spieler5} – {score5} Punkte", text_alignment="center")

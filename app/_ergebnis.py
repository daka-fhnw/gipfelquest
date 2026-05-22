import streamlit as st
import json
import os

from _state import AppState
HIGHSCORE_FILE = "app/highscores.json"

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


def ergebnis_inhalt(state: AppState):
    punkte = state.ergebnis.punkte

    st.markdown("# Ergebnis")
    st.markdown(f"## Punkte: {punkte}")
    st.button("Zurück", on_click=state.start_anzeigen)

    if "highscore_entered" not in st.session_state:
        st.session_state.highscore_entered = False

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

    if st.session_state.highscore_entered:
        st.info("Highscore wurde bereits eingetragen 🎉")
    else:

        if punkte > score1:
            st.markdown("Herzlichen Glückwunsch! Du hast den ersten Platz erreicht! 🥇", text_alignment="center")
            st.balloons()
            st.toast("🎉 Neuer Highscore! Platz 1! 🎉")
            st.success("🔥 Stark! Du bist die neue Nummer 1! 🔥")

            erster = st.text_input("Geben Sie hier Ihren Usernamen ein:")
            if erster:
                st.session_state.highscore_entered = True

                Spieler5 = Spieler4
                Spieler4 = Spieler3
                Spieler3 = Spieler2
                Spieler2 = Spieler1
                Spieler1 = erster

                score5 = score4
                score4 = score3
                score3 = score2
                score2 = score1
                score1 = punkte

        elif punkte > score2:
            st.markdown("Glückwunsch! Du hast den zweiten Platz erreicht! 🥈", text_alignment="center")
            st.balloons()
            st.toast("🎉 Neuer Highscore! Platz 2! 🎉")
            st.success("🔥 Gut gemacht! Du bist auf dem zweiten Platz! 🔥")

            zweiter = st.text_input("Geben Sie Ihren Usernamen ein:")
            if zweiter:
                st.session_state.highscore_entered = True

                Spieler5 = Spieler4
                Spieler4 = Spieler3
                Spieler3 = Spieler2
                Spieler2 = zweiter

                score5 = score4
                score4 = score3
                score3 = score2
                score2 = punkte

        elif punkte > score3:
            st.markdown("Glückwunsch! Du hast den dritten Platz erreicht! 🥉", text_alignment="center")
            st.balloons()
            st.toast("🎉 Neuer Highscore! Platz 3! 🎉")
            st.success("🔥 Stark! Du bist in den Top 3! 🔥")

            dritter = st.text_input("Geben Sie Ihren Usernamen ein:")
            if dritter:
                st.session_state.highscore_entered = True

                Spieler5 = Spieler4
                Spieler4 = Spieler3
                Spieler3 = dritter

                score5 = score4
                score4 = score3
                score3 = punkte

        elif punkte > score4:
            st.markdown("Glückwunsch! Du hast den vierten Platz erreicht! 🏅", text_alignment="center")
            st.balloons()
            st.toast("🎉 Neuer Highscore! Platz 4! 🎉")
            st.success("🔥 Gut gemacht! Du bist auf dem vierten Platz! 🔥")

            vierter = st.text_input("Geben Sie Ihren Usernamen ein:")
            if vierter:
                st.session_state.highscore_entered = True

                Spieler5 = Spieler4
                Spieler4 = vierter

                score5 = score4
                score4 = punkte

        elif punkte > score5:
            st.markdown("Glückwunsch! Du hast den fünften Platz erreicht! 🎖️", text_alignment="center")
            st.balloons()
            st.toast("🎉 Neuer Highscore! Platz 5! 🎉")
            st.success("🔥 Gut gemacht! Du bist auf dem fünften Platz! 🔥")

            fuenfter = st.text_input("Geben Sie Ihren Usernamen ein:")
            if fuenfter:
                st.session_state.highscore_entered = True

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
    st.markdown(f"Nr. 1: {Spieler1} - {score1} Punkte", text_alignment="center")
    st.markdown(f"Nr. 2: {Spieler2} - {score2} Punkte", text_alignment="center")
    st.markdown(f"Nr. 3: {Spieler3} - {score3} Punkte", text_alignment="center")
    st.markdown(f"Nr. 4: {Spieler4} - {score4} Punkte", text_alignment="center")
    st.markdown(f"Nr. 5: {Spieler5} - {score5} Punkte", text_alignment="center")

import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import pandas as pd


#####################################################################################
#Auswahl Berg und Anwortmöglichkeiten
alle_berge = pd.read_json("../data/gipfel-daten.json").reset_index(drop=True)
if 'richtiger_berg' not in st.session_state:
    st.session_state['richtiger_berg'] = alle_berge.sample(n=1, random_state=None)
####################################################################################

import numpy as np

def plot_profile_data(data: tuple[list[float], list[float]], 
                      ax: Axes) -> None:
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    x, y = zip(*data)

    # Feststellung Extremwerte für spätere gleiche Einfärbung
    y_E = np.array([p[1] for p in data_E])
    y_N = np.array([p[1] for p in data_N])
    global_min = min(y_E.min(), y_N.min())

    ax.plot(x,y,color="black",linewidth=1)  # <- Design Graph, vielleicht anpassan an Gesamtdesign
    ax.fill_between(x,y,global_min,color="lightgray") # <- Hintergrundfarbe Profil, vielleicht anpassan an Gesamtdesign
    ax.set_facecolor("#D3ECF8") # <- Hintergrundfarbe Himmel, vielleicht anpassan an Gesamtdesign

berg = st.session_state['richtiger_berg'].iloc[0]
data_E = berg.profil_ost
data_N = berg.profil_nord

#print(data_N)


fig = plt.figure()
gs = fig.add_gridspec(1, 2, wspace=0)
(ax1, ax2) = gs.subplots(sharey=True)
plot_profile_data(data_E, ax1)
plot_profile_data(data_N, ax2)
ax1.set_title("Profil von West nach Ost")
ax2.set_title("Profil von Süd nach Nord")

st.pyplot(fig)


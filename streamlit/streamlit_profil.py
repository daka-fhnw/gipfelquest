import json
import requests
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from enum import Enum
import pandas as pd


#####################################################################################
#Auswahl Berg und Anwortmöglichkeiten
alle_berge = pd.read_json("../data/gipfel-daten.json").reset_index(drop=True)
if 'richtiger_berg' not in st.session_state:
    st.session_state['richtiger_berg'] = alle_berge.sample(n=1, random_state=None)
####################################################################################


def plot_profile_data(data: tuple[list[float], list[float]], 
                      ax: Axes) -> None:
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    x, y = zip(*data)
    ax.plot(x, y)

berg = st.session_state['richtiger_berg'].iloc[0]
data_E = berg.profil_ost
data_N = berg.profil_nord

print(data_E)


fig = plt.figure()
gs = fig.add_gridspec(1, 2, wspace=0)
(ax1, ax2) = gs.subplots(sharey=True)
plot_profile_data(data_E, ax1)
plot_profile_data(data_N, ax2)

st.pyplot(fig)


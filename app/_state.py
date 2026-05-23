import time
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from pandas import DataFrame
from collections.abc import Callable

from _konstanten import *
from _daten import * 

STATE_KEY = "app-state"

class SpielState: 
    punkte: int = 0
    start_zeit: int = 0
    zeit_abzug: int = 0
    gipfel_auswahl: DataFrame 
    gipfel_index: int = 0
    antwort_optionen: DataFrame
    merkmale: dict[str, bool] = {}

class ErgebnisState:
    punkte: int = 0

class EinstellungenState:
    region: str = REGION_ALLE

class AppState:
    gipfel_alle: DataFrame = DataFrame([])
    seite: int = START_SEITE
    spiel: SpielState | None = None
    ergebnis: ErgebnisState | None = None
    einstellungen: EinstellungenState = EinstellungenState()

    def start_anzeigen(self):
        self.seite = START_SEITE
        self.spiel = None
        self.ergebnis = None

    def einstellungen_anzeigen(self):
        self.seite = EINSTELUNGEN_SEITE

    def spiel_starten(self): 
        self.seite = SPIEL_SEITE
        self.spiel = SpielState()
        self.spiel.punkte = 0
        self.spiel.zeit_abzug = 0
        self.spiel.start_zeit = time.time()
        self.spiel.gipfel_auswahl = get_gipfel_auswahl(self.gipfel_alle, self.einstellungen.region)
        self.spiel.antwort_optionen = get_antwort_optionen(
            self.gipfel_alle, self.get_gipfel_zeile(), self.einstellungen.region)
        st.session_state.highscore_entered = False

    def _merkmal_anzeigen(self, id: str):
        if not self.spiel.merkmale[id]:
            self.spiel.merkmale[id] = True
            self.zeit_abziehen(MERKMAL_ZEIT_ABZUG)

    def merkmal_box(self, 
                    id: str, 
                    label: str, 
                    inhalt_funktion: Callable):
        if id not in self.spiel.merkmale.keys():
            self.spiel.merkmale[id] = False
        anzeigen = self.spiel.merkmale[id]
        with st.expander(label, expanded=True):
            if anzeigen: 
                with st.container():
                    inhalt_funktion()
            else:
                st.button(f"Anzeigen ({MERKMAL_ZEIT_ABZUG} Sekunden Abzug)", 
                          key = f"anzeigen_{id}",
                          on_click=self._merkmal_anzeigen, args=[id])

    def _merkmale_reset(self): 
        for id in self.spiel.merkmale.keys():
            self.spiel.merkmale[id] = False

    def get_gipfel_zeile(self) -> Series:
        return self.spiel.gipfel_auswahl.iloc[self.spiel.gipfel_index]

    def naechster_gipfel(self):
        self.spiel.gipfel_index += 1
        total = self.spiel.gipfel_auswahl.shape[0]
        if self.spiel.gipfel_index >= total:
            self._spiel_beendet()
            return
        self.spiel.zeit_abzug = 0
        self.spiel.start_zeit = time.time()
        self.spiel.antwort_optionen = get_antwort_optionen(
            self.gipfel_alle, self.get_gipfel_zeile(), self.einstellungen.region)
        self._merkmale_reset()

    def zeit_abgelaufen(self):
        self.naechster_gipfel()

    def falsche_antwort(self):
        self.naechster_gipfel()

    def richtige_antwort(self):
        restzeit = self.get_restzeit()
        self.spiel.punkte += int(restzeit * RESTZEIT_FAKTOR)
        self.naechster_gipfel()

    def _spiel_beendet(self):
        self.seite = ERGEBNIS_SEITE
        self.ergebnis = ErgebnisState()
        self.ergebnis.punkte = self.spiel.punkte
        self.spiel = None

    def get_restzeit(self) -> int:
        abzug = self.spiel.zeit_abzug
        verstrichen = time.time() - self.spiel.start_zeit
        return round(ZEIT_SEKUNDEN - verstrichen - abzug)

    def zeit_abziehen(self, sekunden: int):
        self.spiel.zeit_abzug += sekunden

def get_state() -> AppState: 
    if STATE_KEY not in st.session_state:
        state = AppState()
        state.gipfel_alle = get_gipfel_daten()
        st.session_state[STATE_KEY] = state
    return st.session_state[STATE_KEY]

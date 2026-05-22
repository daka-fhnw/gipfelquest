import time
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from pandas import DataFrame

from _konstanten import *
from _daten import * 

STATE_KEY = "app-state"

class MerkmalState:
    id: str = ""
    zeit_abzug: int = 0
    aktiviert: bool = False

class SpielState: 
    punkte: int = 0
    start_zeit: int = 0
    zeit_abzug: int = 0
    gipfel_auswahl: DataFrame = DataFrame([])
    gipfel_index: int = 0
    antwort_optionen: DataFrame = DataFrame([])
    merkmale: dict[str, MerkmalState] = {}

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

    def merkmal_box(self, 
                    id: str, 
                    label: str, 
                    parent: DeltaGenerator, 
                    zeit_abzug: int = MERKMAL_ZEIT_ABZUG) -> DeltaGenerator:
        if id not in self.spiel.merkmale.keys():
            merkmal_state = MerkmalState()
            merkmal_state.id = id
            merkmal_state.zeit_abzug = zeit_abzug
            self.spiel.merkmale[id] = merkmal_state
        label_mit_abzug = f"{label} (-{zeit_abzug} Sekunden)"
        return parent.expander(label_mit_abzug, key=id, on_change=self._merkmal_on_change, args=[id])

    def _merkmal_on_change(self, id: str):
        aufgeklappt = st.session_state[id]
        merkmal_state = self.spiel.merkmale[id]
        if aufgeklappt and not merkmal_state.aktiviert:
            self.zeit_abziehen(merkmal_state.zeit_abzug)
            merkmal_state.aktiviert = True

    def _merkmale_reset(self):
        merkmale = self.spiel.merkmale
        ids = merkmale.keys()
        for id in ids:
            st.session_state[id] = False
            merkmale[id].aktiviert = False

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

from _konstanten import START_SEITE, SPIEL_SEITE, ERGEBNIS_SEITE
from _state import AppState, get_state
from _start import start_inhalt
from _spiel import spiel_inhalt
from _ergebnis import ergebnis_inhalt

state: AppState = get_state()

if state.seite == START_SEITE:
    start_inhalt(state)
elif state.seite == SPIEL_SEITE:
    spiel_inhalt(state)
elif state.seite == ERGEBNIS_SEITE:
    ergebnis_inhalt(state)

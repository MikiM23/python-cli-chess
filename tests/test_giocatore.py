"""Test per il modulo del Giocatore."""

import os
import sys

import pytest

# Aggiungo la root del progetto al path per importare Parser
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scacchi.GestoreEccezioni import GestoreEccezioni as GE
from scacchi.Giocatore import Giocatore
from scacchi.Pezzi.Pedone import Pedone


def test_creazione_giocatore():
    """Test della creazione del giocatore con nome e colore."""
    giocatore = Giocatore("bianco")
    giocatore.imposta_nome("Luigi")
    assert giocatore.ottieni_nome() == "Luigi"
    assert giocatore.ottieniColore() == "bianco"

    giocatore = Giocatore("nero")
    giocatore.imposta_nome("Marco")
    assert giocatore.ottieni_nome() == "Marco"
    assert giocatore.ottieniColore() == "nero"

    with pytest.raises(
        GE.ColoreNonValido,
        match=(
            "Il colore deve essere 'bianco' o 'nero'."
        ),
    ):
        giocatore = Giocatore("blu")

def test_pezzi_mangiati_giocatore():
    """Test dei pezzi mangiati dal giocatore."""
    giocatore = Giocatore("bianco")
    pezzo = Pedone("nero")
    giocatore.aggiungiPezzoMangiato(pezzo)
    assert giocatore.numeroPezziMangiati() == 1

def test_arrocco_eseguito_giocatore():
    """Test dell'arrocco eseguito da un giocatore."""
    giocatore = Giocatore("bianco")
    giocatore.arroccoEseguito("corto")
    assert giocatore.arroccoCorto()
    assert not giocatore.arroccoLungo()
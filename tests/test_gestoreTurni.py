"""Tests per il modulo del Gestore Turni."""

import os
import sys

# Aggiungo la root del progetto al path per importare Parser
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scacchi.GestoreTurni import GestoreTurni
from scacchi.Giocatore import Giocatore


def test_primo_turno():
    """Test di chi è il primo turno."""
    g1 = Giocatore("bianco")
    g2 = Giocatore("nero")
    turno = GestoreTurni(g1, g2)
    assert turno.ottieni_turno().ottieniColore() == "bianco"
    assert turno.ottieni_turno().ottieniColore() != "nero"

def test_cambio_del_turno():
    """Test del cambio del turno."""
    g1 = Giocatore("bianco")
    g2 = Giocatore("nero")
    turno = GestoreTurni(g1, g2)
    turno.cambia_turno()
    assert turno.ottieni_turno().ottieniColore() == "nero"
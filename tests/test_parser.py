"""Tests per il modulo del Parser."""

import os
import sys

import pytest

# Aggiungo la root del progetto al path per importare Parser
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scacchi.GestoreEccezioni import GestoreEccezioni as GE
from scacchi.Parser import Parser


def test_riconosci_mosse():
    """Test che verifica il riconoscimento corretto delle mosse valide e non valide."""
    parser = Parser()

    assert parser.riconosciMossa("e8")
    assert parser.riconosciMossa("e8D")
    assert parser.riconosciMossa("a2xe8")
    assert parser.riconosciMossa("axb3")
    assert parser.riconosciMossa("2xb3")
    assert parser.riconosciMossa("0-0")
    assert parser.riconosciMossa("0-0-0")
    assert parser.riconosciMossa("xg8")

    assert not parser.riconosciMossa("22")
    assert not parser.riconosciMossa("z9")
    assert not parser.riconosciMossa("a9")
    assert not parser.riconosciMossa("e0")
    assert not parser.riconosciMossa("e8X")  # X maiuscola non ammessa
    

def test_parser_parsa_mossa_senza_cattura():
    """Test parsing di una mossa senza cattura senza promozione."""
    parser = Parser()
    mossa = parser.parsa_mossa_senza_cattura("e8")
    assert mossa["dest_riga"] == 0
    assert mossa["dest_col"] == 4


def test_parser_parsa_mossa_senza_cattura_promozione_donna():
    """Test parsing di una mossa con promozione a Donna senza cattura."""
    parser = Parser()
    mossa = parser.parsa_mossa_senza_cattura("e8D")
    assert mossa["dest_riga"] == 0
    assert mossa["dest_col"] == 4
    assert mossa["promozione"] == "D"  # promozione a Donna (Regina)


def test_parser_parsa_mossa_senza_cattura_promozione_cavallo():
    """Test parsing di una mossa con promozione a Cavallo senza cattura."""
    parser = Parser()
    mossa = parser.parsa_mossa_senza_cattura("h1C")
    assert mossa["dest_riga"] == 7
    assert mossa["dest_col"] == 7
    assert mossa["promozione"] == "C"  # promozione a Cavallo


def test_parser_parsa_mossa_senza_cattura_promozione_torre():
    """Test parsing di una mossa con promozione a Torre senza cattura."""
    parser = Parser()
    mossa = parser.parsa_mossa_senza_cattura("a8T")
    assert mossa["dest_riga"] == 0
    assert mossa["dest_col"] == 0
    assert mossa["promozione"] == "T"  # promozione a Torre


def test_parser_parsa_mossa_senza_cattura_promozione_alfiere():
    """Test parsing di una mossa con promozione ad Alfiere senza cattura."""
    parser = Parser()
    mossa = parser.parsa_mossa_senza_cattura("d1A")
    assert mossa["dest_riga"] == 7
    assert mossa["dest_col"] == 3
    assert mossa["promozione"] == "A"  # promozione ad Alfiere

def test_parser_parsa_mossa_con_cattura_errata():
    """Test parsing di una mossa che non matcha la mossa con cattura."""
    parser = Parser()
    with pytest.raises(
        GE.NotazioneNonValida, match="Notazione non valida per la mossa con cattura."
    ):
        parser.parsa_mossa_con_cattura("ad1")
    
    with pytest.raises(
        GE.NotazioneNonValida, match="Notazione non valida per la mossa con cattura."
    ):
        parser.parsa_mossa_con_cattura("1d1")

def test_parser_parsa_mossa_pedone_con_cattura_errata():
    """Test parsing di una mossa che non matcha la mossa con cattura del pedone."""
    parser = Parser()
    # errore colonna non specificata
    with pytest.raises(
        GE.NotazioneNonValida,
        match=(
            "Notazione errata: stai cercando di mangiare con un pedone senza "
            "specificare la colonna di partenza."
        ),
    ):
        parser.parsa_mossa_con_cattura("xd1")

def test_parser_info_mossa():
    """Test ottenimento informazioni mossa."""
    parser = Parser()
    # mosse valide
    info_mossa = parser.ottieniInfoMossa("0-0")
    assert info_mossa["arrocco"] == "corto"

    info_mossa = parser.ottieniInfoMossa("0-0-0")
    assert info_mossa["arrocco"] == "lungo"

    info_mossa = parser.ottieniInfoMossa("Axd3")
    assert info_mossa["pezzo"] == "A"
    assert info_mossa["dest_riga"] == 5
    assert info_mossa["dest_col"] == 3
    assert info_mossa["cattura"] is True

    info_mossa = parser.ottieniInfoMossa("T2xa4")
    assert info_mossa["pezzo"] == "T"
    assert info_mossa["disamb_riga"] == 6
    assert info_mossa["dest_riga"] == 4
    assert info_mossa["dest_col"] == 0
    assert info_mossa["cattura"] is True

    # mosse valide ma con errori nelle informazioni
    info_mossa = parser.ottieniInfoMossa("0-0")
    assert info_mossa["arrocco"] != "lungo"

    info_mossa = parser.ottieniInfoMossa("0-0-0")
    assert info_mossa["arrocco"] != "corto"

    info_mossa = parser.ottieniInfoMossa("Cxa3")
    assert info_mossa["pezzo"] != "A"
    assert info_mossa["dest_riga"] != 6
    assert info_mossa["dest_col"] != 2
    assert not info_mossa["cattura"] is not True
"""Tests per il modulo della scacchiera."""

import os
import sys

import pytest

# Aggiungo la root del progetto al path per importare Parser
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scacchi.GestoreEccezioni import GestoreEccezioni as GE
from scacchi.GestoreTurni import GestoreTurni
from scacchi.Giocatore import Giocatore
from scacchi.Pezzi.Cavallo import Cavallo
from scacchi.Pezzi.Pedone import Pedone
from scacchi.Pezzi.Regina import Regina
from scacchi.Pezzi.Torre import Torre
from scacchi.Scacchiera import Scacchiera


def test_posizionamento_pezzi():
    """Test set e get del pezzo Pedone nella scacchiera."""
    scacchiera = Scacchiera()
    pedone = Pedone("bianco")
    posizione = (0,0)
    scacchiera.set_pezzo(posizione, pedone)
    pezzo = scacchiera.get_pezzo(posizione)
    assert isinstance(pezzo, Pedone)

def test_rimozione_pezzo():
    """Test rimuozione di un pezzo dalla scacchiera."""
    scacchiera = Scacchiera()
    pedone = Pedone("bianco")
    posizione = (0,0)
    scacchiera.set_pezzo(posizione, pedone)
    scacchiera.rimuoviPezzo(posizione)
    pezzo = scacchiera.get_pezzo(posizione)
    assert pezzo is None

def test_posizione_libera_scacchiera():
    """Test della posizione libera sulla scacchiera."""
    scacchiera = Scacchiera()
    posizione = (4,4)
    assert scacchiera.posizioneLibera(posizione)

def test_generazione_pezzo_per_promozione():
    """Test della generazione di un pezzo."""
    scacchiera = Scacchiera()
    pezzo = scacchiera.generaPezzo("D", "bianco")

    assert isinstance(pezzo, Regina) and pezzo.getColore() == 'bianco'

def test_generazione_pezzi_non_validi_per_promozione():
    """Test della generazione di re e pedone."""  
    scacchiera = Scacchiera()
    with pytest.raises(
        GE.PromozioneNonValida,
        match=(
            "Non puoi promuovere un pedone a Re."
        ),
    ):
        scacchiera.generaPezzo("R", "nero")

    with pytest.raises(
        GE.PromozioneNonValida,
        match=(
            "Non puoi promuovere un pedone a Pedone."
        ),
    ):
        scacchiera.generaPezzo("P", "bianco")
    
def test_copia_scacchiera():
    """Test della copia della scacchiera."""
    scacchiera = Scacchiera()
    scacchiera_copia = scacchiera.copia_scacchiera()
    assert isinstance(scacchiera_copia, Scacchiera)

def test_arrocco_tipo_non_valido():
    """Test dell'arrocco con tipo non valido."""
    scacchiera = Scacchiera()
    g1 = Giocatore("bianco")
    g2 = Giocatore("nero")
    turno = GestoreTurni(g1, g2)

    with pytest.raises(
        GE.ErroreArrocco,
        match=(
            "Colore o tipo di arrocco non valido. Colore deve essere 'bianco' o 'nero' "
            "e tipo deve essere 'corto' o 'lungo'."
        )
    ):
        scacchiera.arroccoPossibile(turno, "errore")


def test_arrocco_corto_gia_eseguito():
    """Test dell'arrocco corto già eseguito."""
    scacchiera = Scacchiera()
    g1 = Giocatore("bianco")
    g2 = Giocatore("nero")
    turno = GestoreTurni(g1, g2)

    turno.ottieni_turno().arroccoEseguito("corto")
    scacchiera.rimuoviPezzo((7, 6))
    scacchiera.rimuoviPezzo((7, 5))

    with pytest.raises(
        GE.ErroreArrocco,
        match="Hai già effetuato l'arrocco corto"
    ):
        scacchiera.arroccoPossibile(turno, "corto")


def test_arrocco_lungo_torre_assente():
    """Test dell'arrocco lungo quando la torre è assente dalla posizione iniziale."""
    scacchiera = Scacchiera()
    g1 = Giocatore("bianco")
    g2 = Giocatore("nero")
    turno = GestoreTurni(g1, g2)

    scacchiera.rimuoviPezzo((7, 0))

    with pytest.raises(
        GE.ErroreArrocco,
        match="La Torre non è presente nella posizione iniziale."
    ):
        scacchiera.arroccoPossibile(turno, "lungo")


def test_arrocco_lungo_con_ostacolo():
    """Test dell'arrocco lungo con un ostacolo tra re e torre."""
    scacchiera = Scacchiera()
    g1 = Giocatore("bianco")
    g2 = Giocatore("nero")
    turno = GestoreTurni(g1, g2)

    scacchiera.set_pezzo((7, 0), Torre("bianco"))
    scacchiera.set_pezzo((7, 1), Cavallo("bianco"))

    with pytest.raises(
        GE.ErroreArrocco,
        match="Una delle caselle utile per l'arrocco è occupata."
    ):
        scacchiera.arroccoPossibile(turno, "lungo")


def test_arrocco_lungo_re_sotto_scacco():
    """Test dell'arrocco lungo quando il re è sotto scacco."""
    scacchiera = Scacchiera()
    g1 = Giocatore("bianco")
    g2 = Giocatore("nero")
    turno = GestoreTurni(g1, g2)

    scacchiera.set_pezzo((7, 0), Torre("bianco"))
    g1.sottoScacco = True

    with pytest.raises(
        GE.ErroreArrocco,
        match="Una delle caselle utile per l'arrocco è occupata."
    ):
        scacchiera.arroccoPossibile(turno, "lungo")


def test_arrocco_corto_valido():
    """Test dell'arrocco corto valido."""
    scacchiera = Scacchiera()
    g1 = Giocatore("bianco")
    g2 = Giocatore("nero")
    turno = GestoreTurni(g1, g2)

    scacchiera.rimuoviPezzo((7, 5))
    scacchiera.rimuoviPezzo((7, 6))
    arrocco = scacchiera.arroccoPossibile(turno, "corto")
    assert arrocco


def test_arrocco_lungo_valido():
    """Test dell'arrocco lungo valido."""
    scacchiera = Scacchiera()
    g1 = Giocatore("bianco")
    g2 = Giocatore("nero")
    turno = GestoreTurni(g1, g2)

    scacchiera.rimuoviPezzo((7, 1))
    scacchiera.rimuoviPezzo((7, 2))
    scacchiera.rimuoviPezzo((7, 3))

    arrocco = scacchiera.arroccoPossibile(turno, "lungo")
    assert arrocco



    

    
    



from typing import TYPE_CHECKING

from scacchi.GestoreEccezioni import GestoreEccezioni as GE
from scacchi.GestoreTurni import GestoreTurni
from scacchi.Pezzi.Pezzo import Pezzo

if TYPE_CHECKING:
    from scacchi.Scacchiera import Scacchiera

class Cavallo(Pezzo):
    """<<Entity>> Classe che rappresenta il cavallo ereditata dalla classe Pezzo.
    
    Il cavallo ha le seguenti caratteristiche:
    - si muove solo a 'L'
    - si muove di due caselle in orizzontale o in verticale e di una perpendicolare
    - può saltare altri pezzi durante la sua traiettoria
    
    """

    def __init__(self, colore):
        super().__init__(colore)
        """Inizializza il colore del cavallo.
        
        Args:
            colore: imposta il colore del pezzo (bianco o nero)
            
        """
    
    def simbolo(self) -> str:
        """Restituisce il simbolo del cavallo in accordo con il colore.
        
        Returns:
            char: simbolo del cavallo
        
        """
        return '♘' if self.colore == 'bianco' else '♞'
    
    def mosseValide(self, posIniziale, scacchiera: "Scacchiera") -> list:
        """Mosse disponibili col cavallo.

        Args:
            posIniziale: posizione del cavallo da muovere
            scacchiera: scacchiera su cui si muovono i pezzi

        Returns:
            mosse (list): potenziali mosse per il movimento del cavallo

        """
        mosse = []
        rigaIniziale, colIniziale = posIniziale

        spostamenti = [
            (-2, +1), (-1, +2), (-2, -1), (-1, -2),
            (+2, +1), (+1, +2), (+2, -1), (+1, -2)
        ]

        for dr, dc in spostamenti:
            nuovaRiga = rigaIniziale + dr
            nuovaCol = colIniziale + dc
            if 0 <= nuovaRiga < 8 and 0 <= nuovaCol < 8:
                pezzo = scacchiera.get_pezzo((nuovaRiga, nuovaCol))
                if pezzo is None or pezzo.getColore() != self.colore:
                    mosse.append((nuovaRiga, nuovaCol))

        return mosse

    def mossaValida(self, posIniziale, posArrivo, scacchiera) -> bool:
        """Restituisce se la mossa è valida per il cavallo.

        Args:
            posIniziale: posizione del cavallo da muovere
            posArrivo: posizione in cui si vuole che il cavallo arrivi
            scacchiera: scacchiera su cui si muovono i pezzi.

        Returns:
            posArrivo (bool): validità o meno della mossa inserita dall'utente
        
        """
        mosse = self.mosseValide(posIniziale, scacchiera)
        return posArrivo in mosse

    
    def __str__(self) -> str:
        """Stampa del pezzo Cavallo.
        
        Returns:
            str: stringa rappresentativa del pezzo
            
        """
        return f"{self.simbolo()} {type(self).__name__}"
    
    @staticmethod
    def trovaCavallo(
        scacchiera,
        info_mossa: dict,
        turno: GestoreTurni,
    ) -> tuple[int, int] | None:
        r_dest, c_dest = info_mossa["dest_riga"], info_mossa["dest_col"]
        colore = turno.ottieniColore()
        disamb_col = info_mossa.get("disamb_col")
        disamb_riga = info_mossa.get("disamb_riga")

        coords = [
            (r_dest - 2, c_dest - 1), (r_dest - 2, c_dest + 1),
            (r_dest - 1, c_dest - 2), (r_dest - 1, c_dest + 2),
            (r_dest + 1, c_dest - 2), (r_dest + 1, c_dest + 2),
            (r_dest + 2, c_dest - 1), (r_dest + 2, c_dest + 1),
        ]

        candidati = []
        for r, c in coords:
            if 0 <= r < 8 and 0 <= c < 8:
                pezzo = scacchiera.get_pezzo((r, c))
                if isinstance(pezzo, Cavallo) and pezzo.getColore() == colore:
                    candidati.append((r, c))

        if disamb_col is not None:
            candidati = [(r, c) for r, c in candidati if c == disamb_col]
        if disamb_riga is not None:
            candidati = [(r, c) for r, c in candidati if r == disamb_riga]

        if len(candidati) == 1:
            return candidati[0]
        if len(candidati) == 0:
            return None
        
        raise GE.NotazioneNonValida( 
            "Ci sono due cavalli candidati per quella posizione, "
            "controlla la notazione"
        )




from typing import TYPE_CHECKING

from scacchi.GestoreEccezioni import GestoreEccezioni as GE
from scacchi.Giocatore import Giocatore
from scacchi.Pezzi.Pezzo import Pezzo

if TYPE_CHECKING:
    from scacchi.Scacchiera import Scacchiera


class Torre(Pezzo):
    """<<Entity>> Classe che rappresenta la torre ereditata dalla classe Pezzo.
    
    La Torre ha le seguenti caratteristiche:
    - avanza di qualsiasi numero di caselle in avanti
    - cattura in orizzontale o verticale
    - può indietreggiare e catturare sia all'indietro che in avanti.
    
    """ 

    def __init__(self, colore):
        """Inizializza il colore della torre.
        
        Args:
            colore: colore della torre
        
        """
        super().__init__(colore)
        self._mosso = False

    def simbolo(self) -> str:
        """Restituisce il simbolo della torre in accordo con il colore.
        
        Returns:
            char: simbolo della torre
        
        """        
        return '♖' if self.colore == 'bianco' else '♜'

    def __str__(self) -> str:
        """Stampa del pezzo Torre.

        Returns:
            str: stringa rappresentativa del pezzo

        """
        return f"{self.simbolo()} {type(self).__name__}"
    
    def mosseValide(self, posIniziale, scacchiera: "Scacchiera") -> list:
        """Mosse disponibili con la torre.

        Args:
            posIniziale: posizione della torre da muovere
            scacchiera: scacchiera su cui si muovono i pezzi

        Returns:
            mosse (list): potenziali mosse per il movimento della torre
        
        """
        mosse = []
        riga, col = posIniziale

        # Movimento in sù
        for r in range(riga - 1, -1, -1):
            pezzo = scacchiera.get_pezzo((r, col))
            if pezzo is None:
                mosse.append((r, col))
            elif pezzo.getColore() != self.colore:
                mosse.append((r, col))
                break
            else:
                break

        # Movimento in giù
        for r in range(riga + 1, 8):
            pezzo = scacchiera.get_pezzo((r, col))
            if pezzo is None:
                mosse.append((r, col))
            elif pezzo.getColore() != self.colore:
                mosse.append((r, col))
                break
            else:
                break

        # Movimento a sinistra
        for c in range(col - 1, -1, -1):
            pezzo = scacchiera.get_pezzo((riga, c))
            if pezzo is None:
                mosse.append((riga, c))
            elif pezzo.getColore() != self.colore:
                mosse.append((riga, c))
                break
            else:
                break

        # Movimento a destra 
        for c in range(col + 1, 8):
            pezzo = scacchiera.get_pezzo((riga, c))
            if pezzo is None:
                mosse.append((riga, c))
            elif pezzo.getColore() != self.colore:
                mosse.append((riga, c))
                break
            else:
                break
            
        return mosse
    
    def mossaValida(self, posIniziale, posArrivo, scacchiera: "Scacchiera") -> bool:
        """Restituisce se la mossa è valida per la torre.

        Args:
            posIniziale: posizione della torre da muovere
            posArrivo: posizione in cui si vuole che la torre arrivi
            scacchiera: scacchiera su cui si muovono i pezzi.

        Returns:
            posArrivo (bool): validità o meno della mossa inserita dall'utente
        
        """
        mosse = self.mosseValide(posIniziale, scacchiera)
        return posArrivo in mosse
    
    @staticmethod
    def trovaTorre(
        scacchiera: "Scacchiera",
        info_mossa: dict,
        turno: Giocatore
    ) -> tuple[int, int] | None:
        """Trova tutte le torri che possono eseguire una mossa verso una posizione.

        Args:
            scacchiera (Scacchiera): La scacchiera contenente i pezzi.
            info_mossa (dict): Informazioni sulla mossa della torre.
            turno (Giocatore): Il giocatore che deve effettuare la mossa.

        Returns:
            list [(riga, colonna)] delle torri che possono eseguire la mossa.
            None se nessuna torre valida Ã¨ trovata.
            
        """
        colore = turno.ottieniColore()
        dest_riga = info_mossa["dest_riga"]
        dest_col = info_mossa["dest_col"]
        disamb_riga = info_mossa.get("disamb_riga")
        disamb_col = info_mossa.get("disamb_col")

        torri_valide = []

        for r in range(8):
            for c in range(8):
                pezzo = scacchiera.get_pezzo((r, c))
                if (
                    pezzo is not None
                    and pezzo.getColore() == colore
                    and isinstance(pezzo, Torre)
                ):
                    if disamb_riga is not None and disamb_riga != r:
                        continue
                    if disamb_col is not None and disamb_col != c:
                        continue
                    if pezzo.mossaValida((r, c), (dest_riga, dest_col), scacchiera):
                        torri_valide.append((r, c))

        if len(torri_valide) == 0:
            return None
        elif len(torri_valide) > 1:
            raise GE.NotazioneNonValida( 
                "Ci sono due torri candidate per quella posizione, "
                "controlla la notazione"
            )
        return torri_valide[0]
    
    def mosso(self):
        """Segna la torre come mossa."""
        self._mosso = True

    def isMosso(self) -> bool:
        """Controlla se la torre è stata mossa.

        Returns:
            bool: True se la torre è stata mossa, False altrimenti

        """
        return self._mosso
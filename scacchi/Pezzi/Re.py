from typing import TYPE_CHECKING

from scacchi.Giocatore import Giocatore
from scacchi.Pezzi.Pezzo import Pezzo

if TYPE_CHECKING:
    from scacchi.Scacchiera import Scacchiera

class Re(Pezzo):
    """<<Entity>> Classe che rappresenta il re ereditata dalla classe Pezzo.
    
    Il re ha le seguenti caratteristiche:
    - si muove in orizzontale, verticale e diagonale
    - solo se la casella di arrivo non è minacciata da nessun pezzo
    ...
    
    """

    def __init__(self, colore):
        """Inizializza il colore del re.
        
        Args:
            colore: imposta il colore del pezzo (bianco o nero)

        """
        super().__init__(colore)
        self._mosso = False
    
    def simbolo(self) -> str:
        """Restituisce il simbolo del re in accordo con il colore.
        
        Returns:
            char: simbolo del re
        
        """
        return '♔' if self.colore == 'bianco' else '♚'
        
    def __str__(self) -> str:
        """Stampa del pezzo Re.
        
        Returns:
            str: stringa rappresentativa del pezzo
            
        """
        return f"{self.simbolo()} {type(self).__name__}"
    def mosseValide(
        self, posizione_iniziale: tuple[int, int], scacchiera: "Scacchiera"
    ) -> list[tuple[int, int]]:
        """Restituisce tutte le mosse valide per il Re."""
        mosse_valide: list[tuple[int, int]] = []
        riga_iniziale, colonna_iniziale = posizione_iniziale

        direzioni_possibili = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]

        colore_avversario = "nero" if self.colore == "bianco" else "bianco"

        for delta_riga, delta_colonna in direzioni_possibili:
            nuova_riga = riga_iniziale + delta_riga
            nuova_colonna = colonna_iniziale + delta_colonna

            if 0 <= nuova_riga < 8 and 0 <= nuova_colonna < 8:
                pezzo_destinazione = scacchiera.get_pezzo((nuova_riga, nuova_colonna))

                if (
                    pezzo_destinazione is None
                    or pezzo_destinazione.getColore() == colore_avversario
                ):
                    casella_sicura = not scacchiera.casella_sotto_attacco(
                        (nuova_riga, nuova_colonna), colore_avversario
                    )
                    if casella_sicura:
                        mosse_valide.append((nuova_riga, nuova_colonna))

        return mosse_valide

    def mossaValida(
        self,
        posizione_iniziale: tuple[int, int],
        posizione_arrivo: tuple[int, int],
        scacchiera: "Scacchiera",
    ) -> bool:
        """Verifica se una mossa specifica è valida per il Re."""
        return posizione_arrivo in self.mosseValide(posizione_iniziale, scacchiera)

    @staticmethod
    def trovaRe(
        scacchiera: "Scacchiera",
        info_mossa: dict,
        turno: Giocatore
    ) -> tuple[int, int] | None:
        """Restituisce la posizione del Re del giocatore, se può eseguire la mossa.

        Args:
            scacchiera: oggetto scacchiera
            info_mossa: informazioni sulla mossa
            turno: giocatore corrente

        Returns:
            Tuple[int, int] se il re può eseguire la mossa, None altrimenti
        
        """
        r_dest = info_mossa.get("dest_riga")
        c_dest = info_mossa.get("dest_col")
        if r_dest is None or c_dest is None:
            return None

        destinazione = (r_dest, c_dest)
        colore_turno = turno.ottieniColore()

        for riga in range(8):
            for colonna in range(8):
                pezzo_corrente = scacchiera.get_pezzo((riga, colonna))

                if (
                    isinstance(pezzo_corrente, Re)
                    and pezzo_corrente.getColore() == colore_turno
                ):
                    # Verifica distanza 1, non controlla lo scacco
                    dr = abs(destinazione[0] - riga)
                    dc = abs(destinazione[1] - colonna)
                    if (dr <= 1 and dc <= 1) and (dr != 0 or dc != 0):
                        return (riga, colonna)
        
        return None
    
    def mosso(self):
        """Segna il re come mosso."""
        self._mosso = True

    def isMosso(self) -> bool:
        """Controlla se il re è stata mosso.

        Returns:
            bool: True se il re è stata mosso, False altrimenti

        """
        return self._mosso
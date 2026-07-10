from typing import TYPE_CHECKING

from scacchi.Giocatore import Giocatore
from scacchi.Pezzi.Pezzo import Pezzo

if TYPE_CHECKING:
    from scacchi.Scacchiera import Scacchiera


class Regina(Pezzo):
    """<<Entity>> Classe che rappresenta la regina ereditata dalla classe Pezzo.
    
    La regina ha le seguenti caratteristiche:
    - si muove in orizzontale, verticale e diagonale
    """

    def __init__(self, colore):
        """Inizializza il colore della regina.
        
        Args:
            colore: imposta il colore del pezzo (bianco o nero)

        """
        super().__init__(colore)
    
    def simbolo(self) -> str:
        """Restituisce il simbolo della regina in accordo con il colore.
        
        Returns:
            char: simbolo della regina
        
        """
        return '♕' if self.colore == 'bianco' else '♛'

    def __str__(self) -> str:
        """Stampa del pezzo Regina.
        
        Returns:
            str: stringa rappresentativa del pezzo
            
        """
        return f"{self.simbolo()} {type(self).__name__}"
        
    def mosseValide(self, posIniziale: tuple[int, int], 
                    scacchiera: "Scacchiera") -> list[tuple[int, int]]:
        """Calcola e restituisce tutte le mosse valide per la regina.

        Args:
            posIniziale: La posizione corrente della regina (riga, colonna).
            scacchiera: L'oggetto Scacchiera su cui si muovono i pezzi.

        Returns:
            list: Una lista di tuple (riga, colonna) che rappresentano le posizioni
                  valide in cui la regina può muoversi.
                  
        """
        mosse = []
        riga_att, col_att = posIniziale

        direzioni = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # Verticale e Orizzontale
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonale
        ]

        for dr, dc in direzioni:
            for i in range(1, 8): 
                riga_next, col_next = riga_att + dr * i, col_att + dc * i

                if 0 <= riga_next < 8 and 0 <= col_next < 8:
                    pezzo_nella_casella = scacchiera.get_pezzo((riga_next, col_next))

                    if pezzo_nella_casella is None:
                        mosse.append((riga_next, col_next))
                    elif pezzo_nella_casella.getColore() != self.colore:
                        mosse.append((riga_next, col_next))
                        break  
                    else:
                        break
                else:
                    break
        return mosse

    def mossaValida(self, posIniziale: tuple[int, int], posArrivo: tuple[int, int],
                         scacchiera: "Scacchiera") -> bool:
        """Controlla se una specifica mossa è valida per la regina.

        Args:
            posIniziale: La posizione iniziale della regina.
            posArrivo: La posizione di destinazione desiderata.
            scacchiera: L'oggetto Scacchiera.

        Returns:
            bool: True se la mossa è valida, False altrimenti.

        """
        mosse_valide_disponibili = self.mosseValide(posIniziale, scacchiera)
        return posArrivo in mosse_valide_disponibili

    @staticmethod
    def trovaRegina(scacchiera: "Scacchiera", 
                      info_mossa: dict, 
                      turno: Giocatore) -> tuple[int, int] | None:
        """Trova la regina in base alla posizione di destinazione e disambiguazione.
        
        Args:
            scacchiera (Scacchiera): scacchiera su cui si muovono i pezzi
            info_mossa (dict): informazioni sulla mossa (dest_riga, dest_col, disamb_col
                , disamb_riga)
            turno (Giocatore): giocatore corrente
        
        Returns:
            (int, int) posizione della regina (riga, colonna) se trovata
            None: se non trovata nessuna regina valida o la mossa è ambigua senza 
                    disambiguazione

        """
        riga_dest, col_dest = info_mossa["dest_riga"], info_mossa["dest_col"]
        colore_corrente = turno.ottieniColore()

        disamb_col = info_mossa.get("disamb_col")
        disamb_riga = info_mossa.get("disamb_riga")

        candidate_queens = []

        # Scorre tutta la scacchiera per trovare potenziali regine
        for riga_orig in range(8):
            for col_orig in range(8):
                pezzo_alla_origine = scacchiera.get_pezzo((riga_orig, col_orig))

                # Condizione 1: Non è una regina o non è del colore giusto
                if not (isinstance(pezzo_alla_origine, Regina) and
                         pezzo_alla_origine.getColore() == colore_corrente):
                    continue 

                # Condizione 2: La posizione di destinazione non è tra le mosse valide 
                # per questa regina
                if (riga_dest, col_dest) not in pezzo_alla_origine.mosseValide(
                    (riga_orig, col_orig), scacchiera
                ):
                    continue 

                # Condizione 3: Se c'è disambiguazione, controlla che la regina 
                # candidata corrisponda
                if (disamb_col is not None and col_orig != disamb_col) or \
                   (disamb_riga is not None and riga_orig != disamb_riga):
                    continue # Questa regina non corrisponde alla disambiguazione, salta

                # Se tutte le condizioni sopra sono state superate, la regina è una 
                # candidata valida
                candidate_queens.append((riga_orig, col_orig))
        
        if len(candidate_queens) == 1:
            return candidate_queens[0]
        elif len(candidate_queens) > 1:
            return None # Mossa ambigua
        else:
            return None # Nessuna regina trovata che può fare la mossa

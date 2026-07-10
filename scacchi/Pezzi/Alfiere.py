from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scacchi.Scacchiera import Scacchiera

from scacchi.Giocatore import Giocatore
from scacchi.Pezzi.Pezzo import Pezzo


class Alfiere(Pezzo):
    """<<Entity>> Classe che rappresenta l'alfiere ereditata dalla classe Pezzo.
    
    L'alfiere ha le seguenti caratteristiche:
    - si muove solo in diagonale 
    - non può saltare altri pezzi durante la sua traiettoria
    
    """

    def __init__(self, colore):
        """Inizializza il colore dell'alfiere.
        
        Args:
            colore: imposta il colore del pezzo (bianco o nero)

        """
        super().__init__(colore)
    
    def simbolo(self) -> str:
        """Restituisce il simbolo dell'alfiere in accordo con il colore.
        
        Returns:
            char: simbolo dell'alfiere
        
        """
        return '♗' if self.colore == 'bianco' else '♝'

    def __str__(self) -> str:
        """Stampa del pezzo Alfiere.
        
        Returns:
            str: stringa rappresentativa del pezzo
            
        """
        return f"{self.simbolo()} {type(self).__name__}"

    def mosseValide(self, posIniziale: tuple[int, int], 
                    scacchiera: "Scacchiera") -> list[tuple[int, int]]:
        """Calcola e restituisce tutte le mosse valide per l'alfiere.

        Args:
            posIniziale: La posizione corrente dell'alfiere (riga, colonna).
            scacchiera: L'oggetto Scacchiera su cui si muovono i pezzi.

        Returns:
            list: Una lista di tuple (riga, colonna) che rappresentano le posizioni
                  valide in cui l'alfiere può muoversi.

        """
        mosse = []
        riga_att, col_att = posIniziale

        # Direzioni diagonali: su-sx, su-dx, giu-sx, giu-dx
        direzioni = [
            (-1, -1),  # Su-Sinistra
            (-1, 1),   # Su-Destra
            (1, -1),   # Giu-Sinistra
            (1, 1)     # Giu-Destra
        ]

        # Per ogni direzione controlla le caselle finché non incontra un pezzo o bordo
        for dr, dc in direzioni:
            for i in range(1, 8):  # L'alfiere può muoversi per un massimo di 7 caselle
                riga_next, col_next = riga_att + dr * i, col_att + dc * i

                # Controlla se la casella è all'interno della scacchiera
                if 0 <= riga_next < 8 and 0 <= col_next < 8:
                    pezzo_nella_casella = scacchiera.get_pezzo((riga_next, col_next))

                    if pezzo_nella_casella is None:
                        # Casella vuota: la mossa è valida, continua in questa direzione
                        mosse.append((riga_next, col_next))
                    elif pezzo_nella_casella.getColore() != self.colore:
                        # Casella occupata da un pezzo avversario:la mossa è una cattura
                        # Aggiungi la mossa e poi ferma la ricerca in questa direzione
                        mosse.append((riga_next, col_next))
                        break  
                    else:
                        # Casella occupata da un pezzo proprio: la mossa non è valida
                        # Ferma la ricerca in questa direzione
                        break
                else:
                    # Fuori dai bordi della scacchiera
                    break
        return mosse

    def mossaValida(self, posIniziale: tuple[int, int], posArrivo: tuple[int, int], 
                    scacchiera: "Scacchiera") -> bool:
        """Controlla se una specifica mossa è valida per l'alfiere.

        Args:
            posIniziale: La posizione iniziale dell'alfiere.
            posArrivo: La posizione di destinazione desiderata.
            scacchiera: L'oggetto Scacchiera.

        Returns:
            bool: True se la mossa è valida, False altrimenti.

        """
        mosse_valide_disponibili = self.mosseValide(posIniziale, scacchiera)
        return posArrivo in mosse_valide_disponibili

    @staticmethod
    def trovaAlfiere(scacchiera: "Scacchiera",
                      info_mossa: dict,
                      turno: "Giocatore") -> tuple[int, int] | None:
        """Trova l'alfiere che può effettuare la mossa desiderata.

        Args:
            scacchiera: L'oggetto Scacchiera.
            info_mossa: Dizionario con le informazioni sulla mossa (dest_riga, dest_col,
                        disamb_col, disamb_riga).
            turno: L'oggetto Giocatore che rappresenta il turno corrente.

        Returns:
            tuple[int, int]: La posizione (riga, colonna) del pezzo Alfiere trovato.
            None: Se nessun alfiere valido è stato trovato o se la mossa è ambigua 
                    senza disambiguazione sufficiente.

        """
        riga_dest = info_mossa["dest_riga"]
        col_dest = info_mossa["dest_col"]
        disamb_col = info_mossa["disamb_col"]
        disamb_riga = info_mossa["disamb_riga"]
        colore_corrente = turno.ottieniColore()

        candidate_alfieri = []

        for riga_orig in range(8):
            for col_orig in range(8):
                pezzo_alla_origine = scacchiera.get_pezzo((riga_orig, col_orig))

                # Verifica iniziale del tipo e del colore del pezzo
                if not (isinstance(pezzo_alla_origine, Alfiere) and
                        pezzo_alla_origine.getColore() == colore_corrente):
                    continue # Se non è l'alfiere giusto o il colore, salta questo pezzo

                # Calcola le mosse valide per il pezzo trovato
                mosse_valide_pezzo = pezzo_alla_origine.mosseValide(
                    (riga_orig, col_orig), 
                    scacchiera             
                )

                if ((riga_dest, col_dest) in mosse_valide_pezzo and
                    (disamb_col is None or col_orig == disamb_col) and
                    (disamb_riga is None or riga_orig == disamb_riga)):
                    
                    candidate_alfieri.append((riga_orig, col_orig))
        
        if len(candidate_alfieri) == 1:
            return candidate_alfieri[0]
        elif len(candidate_alfieri) > 1:
            return None 
        else:
            return None
from typing import TYPE_CHECKING

from scacchi.Giocatore import Giocatore
from scacchi.Pezzi.Pezzo import Pezzo

if TYPE_CHECKING:
    from scacchi.Scacchiera import Scacchiera


class Pedone(Pezzo):
    """<<Entity>> Classe che rappresenta il pedone ereditata dalla classe Pezzo.

    Il pedone ha le seguenti caratteristiche:
    - avanza di una casella in avanti
    - avanza di due casella in avanti solo se si trova nella posizione iniziale
    - cattura in diagonale
    - non può indietreggiare ne catturare all'indietro
    - se un pezzo è posto subito davanti non può né superarlo né catturarlo
    
    """

    def __init__(self, colore):
        """Inizializza il colore del pedone.
        
        Args:
            colore: colore del pedone
        
        """
        super().__init__(colore)

    def simbolo(self):
        """Restituisce il simbolo del pedone in accordo con il colore.
        
        Returns:
            char: simbolo del pedone
        
        """
        return '♙' if self.colore == 'bianco' else '♟'
   
    def mosseValide(self,
                    posIniziale,
                    scacchiera: "Scacchiera",
                    info_mossa=None) -> list:
        mosse = []
        riga, col = posIniziale
        direzione = -1 if self.colore == 'bianco' else 1
        rigaAvanti = riga + direzione

        # Avanzamento semplice
        if 0 <= rigaAvanti < 8 and scacchiera.get_pezzo((rigaAvanti, col)) is None:
            mosse.append((rigaAvanti, col))

            # Doppio passo iniziale
            rigaDueAvanti = riga + 2 * direzione
            if (
                ((self.colore == 'bianco' and riga == 6) or 
                (self.colore == 'nero' and riga == 1))
                and scacchiera.get_pezzo((rigaDueAvanti, col)) is None
            ):
                mosse.append((rigaDueAvanti, col))

        # Catture diagonali
        for dc in [-1, 1]:
            colDiagonale = col + dc
            if 0 <= colDiagonale < 8 and 0 <= rigaAvanti < 8:
                pezzo = scacchiera.get_pezzo((rigaAvanti, colDiagonale))
                if pezzo is not None and pezzo.getColore() != self.colore:
                    mosse.append((rigaAvanti, colDiagonale))

        # En passant
        if info_mossa and info_mossa.get("en_passant_possibile", False):
            destinazione = info_mossa['en_passant_destinazione']
            vittima = info_mossa['en_passant_vittima']

            if (
                vittima
                and abs(vittima[1] - col) == 1
                and vittima[0] == riga
                and destinazione
            ):
                mosse.append(destinazione)

        return mosse


    def mossaValida(self, posIniziale, posArrivo, scacchiera) -> bool:
        """Restituisce se la mossa è valida per il pedone.

        Args:
            posIniziale: posizione del pedone da muovere
            posArrivo: posizione in cui si vuole che il pedone arrivi
            scacchiera: scacchiera su cui si muovono i pezzi.

        Returns:
            posArrivo (bool): validità o meno della mossa inserita dall'utente
        
        """
        mosse = self.mosseValide(posIniziale, scacchiera)
        return posArrivo in mosse
        
        
    def __str__(self) -> str:
        """Stampa del pezzo Pedone.

        Returns:
            str: stringa rappresentativa del pezzo

        """
        return f"{self.simbolo()} {type(self).__name__}"
    
    @staticmethod
    def trovaPedone(scacchiera: "Scacchiera", 
                    info_mossa: dict, 
                    turno: Giocatore) -> tuple[int, int] | None:
        """Trova il pedone in base alla posizione di destinazione.
        
        Args:
            scacchiera (Scacchiera): scacchiera su cui si muovono i pezzi
            info_mossa (dict): informazioni sulla mossa
            turno (Giocatore): giocatore corrente
        
        Returns:
            (int, int) posizione del pedone (riga, colonna) se trovato
            None: se non trovato nessun pedone valido

        """        
        posizione = (info_mossa["dest_riga"], info_mossa["dest_col"])

        riga_dest, colonna_dest = posizione
        colore = turno.ottieniColore()

        direzione = 1 if colore == 'bianco' else -1

        if info_mossa["cattura"] and info_mossa["disamb_col"] is not None:
            
            if info_mossa["disamb_riga"] is not None and (
                info_mossa["dest_col"] - info_mossa["disamb_col"]) in (-1, 1):
                pezzo = scacchiera.get_pezzo(
                    (info_mossa["disamb_riga"], info_mossa["disamb_col"]))
                if isinstance(pezzo, Pedone) and pezzo.getColore() == colore:
                    return (info_mossa["disamb_riga"], info_mossa["disamb_col"])
            else:
                riga = riga_dest + direzione
                colonna = info_mossa["disamb_col"]
                pezzo = scacchiera.get_pezzo((riga, colonna))
                if isinstance(pezzo, Pedone) and pezzo.getColore() == colore and (
                    info_mossa["dest_col"] - colonna) in (-1, 1):
                    
                    return (riga, colonna)
            return None

        # Movimento di una riga
        una_riga = riga_dest + direzione
        if 0 <= una_riga <= 7:
            pezzo = scacchiera.get_pezzo((una_riga, colonna_dest))
            if (pezzo is not None
                and pezzo.getColore() == colore
                and isinstance(pezzo, Pedone)):
                # Se disambiguazione presente, controlla corrispondenza
                if (
                    info_mossa["disamb_col"] is not None
                    and info_mossa["disamb_col"] != colonna_dest
                ):
                    pass  # non corrisponde la colonna
                elif (
                    info_mossa["disamb_riga"] is not None
                    and info_mossa["disamb_riga"] != una_riga
                ):
                    pass  # non corrisponde la riga
                else:
                    return (una_riga, colonna_dest)

        # Movimento di due righe (solo dalla posizione iniziale 1 o 6)
        due_righe = riga_dest + 2 * direzione
        if 0 <= due_righe <= 7:
            pezzo = scacchiera.get_pezzo((due_righe, colonna_dest))
            casella_intermedia_libera = (scacchiera.get_pezzo((riga_dest + direzione, colonna_dest)) is None)
            if (pezzo is not None
                and pezzo.getColore() == colore
                and isinstance(pezzo, Pedone)
                and due_righe in (1, 6)
                and casella_intermedia_libera):
                # Controllo disambiguazione come sopra
                if (
                    (info_mossa["disamb_col"] is not None
                     and info_mossa["disamb_col"] != colonna_dest)
                    or
                    (info_mossa["disamb_riga"] is not None
                     and info_mossa["disamb_riga"] != due_righe)
                ):
                    pass
                else:
                    return (due_righe, colonna_dest)

        # Nessuna posizione valida trovata
        return None
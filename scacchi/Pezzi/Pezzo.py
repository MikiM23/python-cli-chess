

class Pezzo:
    """<<Entity>> Classe base per rappresentari i pezzi della scacchiera."""

    def __init__(self, colore):
        """Costruttore che inizializza il colore del pezzo.
        
        Args:
            colore (str): indica il colore del pezzo

        """
        self.colore = colore

    def simbolo(self) -> str:
        """Restituisce il simbolo del pezzo in accordo con il colore.
        
        Returns:
            char: ritorna il simbolo del pezzo

        """
        return '?'

    def mosseValide(self, posizione, scacchiera) -> list:
        """Restituisce le mosse che può fare il pezzo.
        
        Args:
            posizione (int, int): posizione nella scacchiera
            scacchiera (Scacchiera): scacchiera di gioco
        
        Returns:
            mosse (list): lista di mosse che il pezzo può effettuare
        
        """
        return []
    
    def mossaValida(self, posIniziale, posArrivo, scacchiera) -> bool:
        """Restituisce se la mossa è valida per il pezzo.
        
        Args:
            posIniziale (int, int): posizione di partenza del pezzo
            posArrivo (int, int): posizione di arrivo del pezzo
            scacchiera (Scacchiera): scacchiera di gioco in cui si trova il pezzo

        Returns:
            bool: ritorna vero se la mossa è valida, falso altrimenti
            
        """
        return False

    def getColore(self) -> str:
        """Ritorna il colore del pezzo.

        Returns:
            str: colore del pezzo (bianco / nero)
            
        """
        return self.colore
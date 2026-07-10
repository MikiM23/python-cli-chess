import re

from scacchi.GestoreEccezioni import GestoreEccezioni as GE
from scacchi.Giocatore import Giocatore
from scacchi.Pezzi.Alfiere import Alfiere
from scacchi.Pezzi.Cavallo import Cavallo
from scacchi.Pezzi.Pedone import Pedone
from scacchi.Pezzi.Re import Re
from scacchi.Pezzi.Regina import Regina
from scacchi.Pezzi.Torre import Torre
from scacchi.Scacchiera import Scacchiera


class Parser:
    """<<Control>> Parser per la notazione algebrica delle mosse."""

    def __init__(self):
        pass

    def riconosciMossa(self, cmd):
        """Riconosce se la stringa cmd è una mossa in notazione Algebrica.

        Args:
            cmd (str): stringa inserita dall'utente in input

        Returns:
            bool: True se la stringa è una mossa, False altrimenti
            
        """
        pattern = re.compile(r"""
            ^(
                [a-h]x[a-h][1-8] |          
                [ATCDR]?[a-h]?[1-8]?x[a-h][1-8][ATCDR]? |
                [ATCDR]?[a-h][1-8] |
                [ATCDR]?[a-h]?[1-8]?[a-h][1-8] |
                [a-h][1-8][ATCD]? |
                0-0 | #arrocco corto
                0-0-0 #arrocco lungo
            )$
        """, re.VERBOSE)
        return bool(pattern.match(cmd))
        
    def trovaPezzi(self, 
                   info_mossa: dict, 
                   scacchiera: Scacchiera,
                   turno: Giocatore) -> tuple[int, int] | None:
        """Chiama la funzione di ricerca del pezzo specifico.

        Args:
            info_mossa (dict): informazioni sulla mossa
            scacchiera (Scacchiera): oggetto scacchiera
            turno (Giocatore): oggetto Giocatore che rappresenta il turno corrente

        Returns:
            (int, int): posizione del pezzo trovato
            None: se il pezzo non viene trovato
        
        """
        trova_funzioni = {
            "P": Pedone.trovaPedone,
            "C": Cavallo.trovaCavallo,
            "D": Regina.trovaRegina,
            "R": Re.trovaRe,
            "A": Alfiere.trovaAlfiere,
            "T": Torre.trovaTorre
        }
        pezzo = info_mossa["pezzo"]

        if pezzo not in trova_funzioni:
            return None
                
        return trova_funzioni[pezzo](scacchiera, info_mossa, turno)
    
    def parsa_mossa_con_cattura(self, mossa: str) -> dict:
        """Parsa una mossa in notazione algebrica con cattura.

        Args:
            mossa (str): mossa in notazione algebrica formato cattura
            
        Returns:
            info (dict): dizionario con le informazioni della mossa
        
        Raise:
            GE.NotazioneNonValida: se la notazione non è valida

        """
        pattern = re.compile(r"""
            ^(?P<pezzo>[ATCDR])?            # tipo del pezzo (facoltativo per pedoni)
            (?P<disamb>[a-h1-8]{0,2})       # colonna/riga di disambiguazione
            x
            (?P<destinazione>[a-h][1-8])    # destinazione
            (?P<promozione>[ATCDRP])?        # promozione (facoltativa)
        $""", re.VERBOSE)

        match = pattern.match(mossa)
        if not match:
            raise GE.NotazioneNonValida(
                "Notazione non valida per la mossa con cattura.")
        
        pezzo = match.group("pezzo") or "P"
        disamb = match.group("disamb")
        destinazione = match.group("destinazione")
        promozione = match.group("promozione")

        if len(destinazione) != 2:
            raise GE.NotazioneNonValida("Le coordinate di destinazione " \
            "del pezzo sono errate.")
        
        dest_col = destinazione[0]
        dest_riga = destinazione[1]

        disamb_col = None
        disamb_riga = None
        for c in disamb:
            if c in "abcdefgh":
                disamb_col = ord(c) - ord('a')
            elif c in "12345678":
                disamb_riga = 8 - int(c)

        if pezzo == "P" and disamb_col is None:
            raise GE.NotazioneNonValida("Notazione errata: " \
            "stai cercando di mangiare con un pedone " \
            "senza specificare la colonna di partenza.")

        
        dest_col = ord(dest_col) - ord('a')

        info = {
            "cattura" : True,
            "pezzo": pezzo,
            "disamb_col": disamb_col,
            "disamb_riga": disamb_riga,
            "dest_col": int(dest_col),
            "dest_riga": 8 - int(dest_riga),
            "promozione": promozione if promozione else None
        }
        return info
    
    def parsa_mossa_senza_cattura(self, mossa: str) -> dict:
        """Parsa una mossa in notazione algebrica senza cattura.

        Args:
            mossa (str): mossa in notazione algebrica senza cattura

        Returns:
            info (dict): dizionario con le informazioni della mossa

        Raise:
            GE.NotazioneNonValida: se la notazione non è valida
            
        """
        pattern = re.compile(r"""
            ^
            (?P<pezzo>[ATCDR])?                # pezzo (opzionale)
            (?P<disamb>[a-h1-8]{0,2})          # disambiguazione o origine completa
            x?                                 # cattura (opzionale)
            (?P<destinazione>[a-h][1-8])       # destinazione
            (?P<promozione>[ATCDRP])?           # promozione (opzionale)
            $
        """, re.VERBOSE)

        match = pattern.match(mossa)
        if not match:
            raise GE.NotazioneNonValida("Notazione non valida per la mossa " \
            "senza cattura.")

        pezzo = match.group("pezzo") or "P"
        disamb = match.group("disamb") or ""
        destinazione = match.group("destinazione")
        promozione = match.group("promozione")

        if len(destinazione) != 2:
            raise GE.NotazioneNonValida("Le coordinate di destinazione " \
            "del pezzo sono errate.")
        
        dest_col = destinazione[0]
        dest_riga = destinazione[1]

        disamb_col = None
        disamb_riga = None
        for c in disamb:
            if c in "abcdefgh":
                disamb_col = ord(c) - ord('a')
            elif c in "12345678":
                disamb_riga = 8 - int(c)
        
        dest_col = ord(dest_col) - ord('a')

        info = {
            "cattura": False,
            "pezzo": pezzo,
            "disamb_col": disamb_col,
            "disamb_riga": disamb_riga,
            "dest_col": int(dest_col),
            "dest_riga": 8 - int(dest_riga),
            "promozione": promozione if promozione else None
        }

        return info
    
    def ottieniInfoMossa(self, mossa: str) -> dict:
        """Ottiene le informazioni della mossa in notazione algebrica.

        Args:
            mossa (str): mossa in notazione algebrica

        Returns:
            dict: informazioni della mossa,
            
        """
        info = {}
        try:
            if "x" in mossa:
                info = self.parsa_mossa_con_cattura(mossa)
            elif mossa == "0-0":
                return {"arrocco": "corto"}
            elif mossa == "0-0-0":
                return {"arrocco": "lungo"}
            else:
                info = self.parsa_mossa_senza_cattura(mossa)
        except Exception as e:
            GE.errore(e)
            return {}

        return info
    
    def controlla_en_passant(self, info_mossa: dict, scacchiera: Scacchiera) -> dict:
        """Controllo se è possibile l'en passant.

        Args:
            info_mossa (dict): informazioni sulla mossa
            scacchiera (Scacchiera): oggetto di tipo scacchiera

        Returns:
            dict: info sulla mossa aggiornate
            
        """
        giocatore: Giocatore = info_mossa['giocatore']
        colore = giocatore.ottieniColore()
        riga_i = info_mossa["pos_pezzo_da_muovere"][0]
        riga_f, colonna_f = info_mossa['dest_riga'], info_mossa['dest_col']
        pezzo = info_mossa['pezzo']

        info_mossa['en_passant_possibile'] = False
        info_mossa['en_passant_vittima'] = None
        info_mossa['en_passant_destinazione'] = None

        # Se un pedone fa la mossa doppia iniziale
        if pezzo == 'P' and abs(riga_f - riga_i) == 2:
            for offset in [-1, 1]:  # Controlla pedoni adiacenti (a sinistra e destra)
                col_lato = colonna_f + offset
                if 0 <= col_lato <= 7:
                    vicino = scacchiera.get_pezzo((riga_f, col_lato))
                    if (vicino and isinstance(vicino, Pedone) and
                            vicino.getColore() != colore):
                        info_mossa['en_passant_possibile'] = True
                        direzione = -1 if colore == 'bianco' else 1
                        info_mossa['en_passant_vittima'] = (riga_f, colonna_f)
                        info_mossa['en_passant_destinazione'] = (
                            riga_f - direzione, colonna_f
                        )

                        break

        return info_mossa
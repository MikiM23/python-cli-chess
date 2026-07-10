import copy

from scacchi.GestoreEccezioni import GestoreEccezioni as GE
from scacchi.GestoreTurni import GestoreTurni
from scacchi.Pezzi.Alfiere import Alfiere
from scacchi.Pezzi.Cavallo import Cavallo
from scacchi.Pezzi.Pedone import Pedone
from scacchi.Pezzi.Pezzo import Pezzo
from scacchi.Pezzi.Re import Re
from scacchi.Pezzi.Regina import Regina
from scacchi.Pezzi.Torre import Torre


class Scacchiera: 
    """<<Entity>> Classe per la Scacchiera di gioco.
    
    Rappresenta una scacchiera con inizializzazione dei pezzi e metodi di stampa.

    Constants:
        LETTERE_COLONNE (str): Stringa contenente le lettere alle colonne ('A','H').
    """

    LETTERE_COLONNE = "ABCDEFGH"


    def __init__(self):
        """Crea la matrice per la scacchiera logica con i pezzi.""" 
        self.griglia = [[None for _ in range(8)] for _ in range(8)]
        self.InizializzaPezzi()
        self.arrocco_permesso = {"bianco": True, "nero": True}        


    def InizializzaPezzi(self):
        """Posiziona i pezzi nella scacchiera."""
        # Inizializzazione pezzi neri.
        
        self.griglia[0] = [
            Torre('nero'), Cavallo('nero'), Alfiere('nero'), Regina('nero'),
            Re('nero'), Alfiere('nero'), Cavallo('nero'), Torre('nero')
        ]

        self.griglia[1] = [Pedone('nero') for _ in range(8)]

        # Inizializzazione pezzi bianchi.
        self .griglia[7] = [
            Torre('bianco'), Cavallo('bianco'), Alfiere('bianco'), Regina('bianco'),
            Re('bianco'), Alfiere('bianco'), Cavallo('bianco'), Torre('bianco')
        ]

        self.griglia[6] = [Pedone('bianco') for _ in range(8)]


    def get_scacchiera(self):
        """Restituisce come output la scacchiera logica.

        Returns:
            scacchiera logica.

        """
        return self.griglia


    def mostraScacchiera(self):
        """Stampa a video della scacchiera logica."""
        print("    " + "   ".join(self.LETTERE_COLONNE)) # lettere colonne superiori
        print("  ┌" + "───┬" * 7 + "───┐") # margini superiori

        for row in range(8):
            numero_riga = 8 - row
            riga_pezzi = f"{numero_riga} │"

            for col in range(8):
                pezzo = self.griglia[row][col]
                simbolo = pezzo.simbolo() if pezzo else ' '
                riga_pezzi += f" {simbolo} │"

            print(riga_pezzi + f" {numero_riga}")

            if row < 7:
                print("  ├" + "───┼" * 7 + "───┤") 

        print("  └" + "───┴" * 7 + "───┘") # margini inferiori
        print("    " + "   ".join(self.LETTERE_COLONNE)) # lettere colonne inferiori
    
    def get_pezzo(self, posizione: tuple[int, int]):
        """Restituisce il pezzo in una determinata posizione della scacchiera.

        Args:
            posizione (int, int): posizione del pezzo (riga, colonna)

        Returns:
            pezzo (Pezzo): oggetto pezzo nella posizione specificata

        """
        riga, colonna = posizione
        return self.griglia[riga][colonna]
    
    def posizioneLibera(self, posizione: tuple[int, int]) -> bool:
        """Controlla se una posizione della scacchiera è libera.

        Args:
            posizione (int, int): posizione da controllare (riga, colonna)

        Returns:
            bool: True se la posizione è libera, False altrimenti
            
        """
        riga, colonna = posizione
        return self.griglia[riga][colonna] is None
    
    def muovi_pezzo(self, 
                    posizione_iniziale: tuple[int, int], 
                    posizione_finale: tuple[int, int]):
        """Muove un pezzo da una posizione iniziale a una finale.

        Args:
            posizione_iniziale (int, int): posizione iniziale del pezzo (riga, colonna)
            posizione_finale (int, int): posizione finale del pezzo (riga, colonna)

        """
        riga_iniziale, colonna_iniziale = posizione_iniziale
        riga_finale, colonna_finale = posizione_finale

        self.griglia[riga_finale][colonna_finale] = (
            self.griglia[riga_iniziale][colonna_iniziale])
        self.griglia[riga_iniziale][colonna_iniziale] = None

    def set_pezzo(self, posizione: tuple[int, int], pezzo: Pezzo):
        """Imposta un pezzo in una determinata posizione della scacchiera.

        Args:
            posizione (int, int): posizione del pezzo (riga, colonna)
            pezzo (Pezzo): oggetto pezzo da posizionare

        """
        riga, colonna = posizione
        self.griglia[riga][colonna] = pezzo

    def rimuoviPezzo(self, posizione: tuple[int, int]):
        """Rimuove un pezzo da una determinata posizione della scacchiera.

        Args:
            posizione (int, int): posizione del pezzo da rimuovere (riga, colonna)

        """
        riga, colonna = posizione
        self.griglia[riga][colonna] = None

    def catturaPezzo(self,
                    posizione_iniziale: tuple[int, int],
                    posizione_finale: tuple[int, int]):
        """Cattura un pezzo da una posizione iniziale a una finale.

        Args:
            posizione_iniziale (int, int): posizione iniziale del pezzo (riga, colonna)
            posizione_finale (int, int): posizione finale del pezzo (riga, colonna)
            
        """
        pezzo = self.get_pezzo(posizione_iniziale)
        self.set_pezzo(posizione_finale, pezzo)
        self.rimuoviPezzo(posizione_iniziale)

    def promozioneValida(self, posizione: tuple[int, int], colore: str) -> bool:
        """Controlla se la promozione di un pedone è valida.

        Args:
            posizione (int, int): posizione di arrivo del pedone (riga, colonna)
            colore (str): colore del pedone ('bianco' o 'nero')

        Returns:
            bool: True se la promozione è valida, False altrimenti
            
        """
        riga, _ = posizione
        
        return (
            (colore == 'bianco' and riga == 0) or
            (colore == 'nero' and riga == 7)
        )

    def generaPezzo(self, pezzo: str, colore: str) -> Pezzo:
        """Genera un pezzo in base al tipo e al colore.

        Args:
            pezzo (str): tipo di pezzo ('T', 'C', 'A', 'R', 'D')
            colore (str): colore del pezzo ('bianco' o 'nero')

        Returns:
            Pezzo: istanza del pezzo generato

        """
        if pezzo == 'T':
            return Torre(colore)
        elif pezzo == 'C':
            return Cavallo(colore)
        elif pezzo == 'A':
            return Alfiere(colore)
        elif pezzo == 'R':
            raise GE.PromozioneNonValida("Non puoi promuovere un pedone a Re.")
        elif pezzo == 'D':
            return Regina(colore)
        elif pezzo == 'P':
            raise GE.PromozioneNonValida("Non puoi promuovere un pedone a Pedone.")
        else:
            raise GE.PromozioneNonValida(f"Tipo di pezzo '{pezzo}' non valido.")
    
    def promuoviPedone(self, pos_pedone: tuple[int, int], pezzo: str, colore: str):
        """Promuove un pedone a un altro pezzo.

        Args:
            pos_pedone (int, int): posizione del pedone da promuovere (riga, colonna)
            pezzo (str): pezzo a cui promuovere il pedone
            colore (str): colore del pezzo ('bianco' o 'nero')
        
        """
        self.set_pezzo(pos_pedone, self.generaPezzo(pezzo, colore))
  
    def casella_sotto_attacco(self, posizione: tuple[int, int], da_colore: str) -> bool:
        """Controlla se la casella specificata è attaccata da parte di pezzi avversari.
            
        Args:
            posizione (tuple[int, int]): casella da controllare (riga, colonna)
            da_colore (str): colore del potenziale attaccante ('bianco' o 'nero')

        Returns:
            bool: True se la casella è sotto attacco, False altrimenti
            
        """
        r, c = posizione
        avversario = da_colore

        # Pedoni
        direzione = 1 if avversario == "bianco" else -1
        for dc in [-1, 1]:
            rp, cp = r + direzione, c + dc
            if 0 <= rp < 8 and 0 <= cp < 8:
                pezzo = self.get_pezzo((rp, cp))
                if (
                    pezzo
                    and pezzo.getColore() == avversario
                    and isinstance(pezzo, Pedone)
                ):
                    return True

        # Cavalli
        cavallo_moves = [
            (-2, -1), (-2, 1),
            (-1, -2), (-1, 2),
            (1, -2),  (1, 2),
            (2, -1),  (2, 1),
        ]
        for dr, dc in cavallo_moves:
            rr, cc = r + dr, c + dc
            if 0 <= rr < 8 and 0 <= cc < 8:
                pezzo = self.get_pezzo((rr, cc))
                if (
                    pezzo
                    and pezzo.getColore() == avversario
                    and isinstance(pezzo, Cavallo)
                ):
                    return True

        # Re
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                rr, cc = r + dr, c + dc
                if 0 <= rr < 8 and 0 <= cc < 8:
                    pezzo = self.get_pezzo((rr, cc))
                    if (
                        pezzo
                        and pezzo.getColore() == avversario
                        and isinstance(pezzo, Re)
                    ):
                        return True

        # Linee per Torre / Regina (orizzontale, verticale)
        direzioni_lineari = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in direzioni_lineari:
            rr, cc = r + dr, c + dc
            while 0 <= rr < 8 and 0 <= cc < 8:
                pezzo = self.get_pezzo((rr, cc))
                if pezzo:
                    if (
                        pezzo.getColore() == avversario
                        and isinstance(pezzo, Torre | Regina)
                    ):
                        return True
                    break
                rr += dr
                cc += dc

        # Diagonali per Alfiere / Regina
        direzioni_diag = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in direzioni_diag:
            rr, cc = r + dr, c + dc
            while 0 <= rr < 8 and 0 <= cc < 8:
                pezzo = self.get_pezzo((rr, cc))
                if pezzo:
                    if (
                        pezzo.getColore() == avversario
                        and isinstance(pezzo, Alfiere | Regina)
                    ):
                        return True
                    break
                rr += dr
                cc += dc

        return False
    
    def pezzi_di_colore(self, colore: str) -> list[tuple[Pezzo, tuple[int, int]]]:
        """Restituisce i pezzi del colore specificato.
        
        Args:
            colore (str): colore dei pezzi da trovare
        
        Returns:
            list (tuple[Pezzo, tuple[int, int]]): lista di coppie (Pezzo, posizione)

        """
        pezzi = []
        for i in range(8):
            for j in range(8):
                pezzo = self.get_pezzo((i, j))
                if pezzo is not None and pezzo.getColore() == colore:
                    pezzi.append((pezzo, (i, j)))
        return pezzi

    def copia_scacchiera(self) -> "Scacchiera":
        """Restituisce una copia profonda della scacchiera attuale.
        
        Returns:
            Scacchiera: copia della scacchiera
            
        """
        return copy.deepcopy(self)
    
    def trova_re(self, colore: str) -> tuple[int, int] | None:
        """Restituisce la poszione del re del colore passato.
        
        Args:
            colore (str): colore del re che si cerca
        
        Returns:
            tuple(int, int): posizione del re nella scacchiera (riga, colonna)
            None: se non trova il re (caso di errore)

        """
        for i in range(8):
            for j in range(8):
                pos = (i,j)
                pezzo: Pezzo = self.get_pezzo(pos)
                if (
                    pezzo is not None
                    and isinstance(pezzo, Re)
                    and pezzo.getColore() == colore
                ):
                    return pos
        return None
        
    def re_sotto_scacco(self, colore: str) -> bool:
        """Restituisce se il re è sotto scacco.
        
        Args:
            colore (str): colore del re (bianco, nero)
        
        Returns:
            bool: True se è sottos scacco, False altrimenti

        """
        pos_re = self.trova_re(colore)
        colore_avversario = "nero" if colore == "bianco" else "bianco"
        return self.casella_sotto_attacco(pos_re, colore_avversario)

    def mosse_salva_re(
        self, colore: str) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """Restituisce la lista delle mosse possibili per togliere il re dallo scacco.

        Args:
            colore (str): colore del giocatore il cui Re è sotto attacco

        Returns:
            list[tuple[tuple[int, int], tuple[int, int]]]: 
                Lista di coppie di posizioni, dove ogni coppia rappresenta 
                (posizione_iniziale, posizione_finale) della mossa legale salva Re.

        """
        mosse_salvanti = []
        
        for pezzo, posizione_iniziale in self.pezzi_di_colore(colore):
            mosse_possibili = pezzo.mosseValide(posizione_iniziale, self)

            for posizione_finale in mosse_possibili:
                scacchiera_simulata = self.copia_scacchiera()
                try:
                    scacchiera_simulata.muovi_pezzo(
                        posizione_iniziale, posizione_finale
                    )
                except Exception:
                    continue
                
                if not scacchiera_simulata.re_sotto_scacco(colore):
                    mosse_salvanti.append((posizione_iniziale, posizione_finale))

        return mosse_salvanti
    
    def is_scacco_matto(self, colore: str) -> bool:
        """Controlla se è scacco matto.
        
        Args:
            colore (str): colore del re da controllare
        
        Returns:
            True se è scacco matto, False altrimenti
            
        """
        if not self.re_sotto_scacco(colore):
            return False

        return len(self.mosse_salva_re(colore)) == 0
    
    def arroccoPossibile(
        self, turno: GestoreTurni, tipo_arrocco: str
    ) -> bool | None | dict:
        """Controlla se l'arrocco è possibile per un determinato colore.

        Args:
            turno (GestoreTurni): giocatore del turno corrente
            tipo_arrocco (str): tipo di arrocco ('corto' o 'lungo')

        Returns:
            bool: True se l'arrocco è possibile, False altrimenti
            
        """
        colore = turno.ottieni_turno().ottieniColore()
        avversario = turno.ottiene_turno_avversario().ottieniColore()
        
        if colore not in ['bianco', 'nero'] or tipo_arrocco not in ['corto', 'lungo']:
            raise GE.ErroreArrocco(
                "Colore o tipo di arrocco non valido. "
                "Colore deve essere 'bianco' o 'nero' e tipo deve essere "
                "'corto' o 'lungo'."
            )
        if tipo_arrocco == "corto" and turno.ottieni_turno().arroccoCorto():
            raise GE.ErroreArrocco(
                "Hai già effetuato l'arrocco corto"
                )
        if tipo_arrocco == "lungo" and turno.ottieni_turno().arroccoLungo():
            raise GE.ErroreArrocco(
                "Hai già effetuato l'arrocco lungo"
                )
        
        if colore == "bianco":
            pos_re = (7, 4)
            if tipo_arrocco == "corto":
                pos_torre = (7, 7)
                pos_intermedie = [(7,6),(7,5)]
                pos_arrivo_re = (7, 6)
                pos_arrivo_torre = (7, 5)
            else:
                pos_torre = (7, 0)
                pos_intermedie = [(7,1),(7,2),(7,3)]
                pos_arrivo_re = (7, 2)
                pos_arrivo_torre = (7, 3)
        else:
            pos_re = (0, 4)
            if tipo_arrocco == "corto":
                pos_torre = (0, 7)
                pos_intermedie = [(0,6),(0,5)]
                pos_arrivo_re = (0, 6)
                pos_arrivo_torre = (0, 5)
            else:
                pos_torre = (0, 0)
                pos_intermedie = [(0,1),(0,2),(0,3)]
                pos_arrivo_re = (0, 2)
                pos_arrivo_torre = (0, 3)
        
        re = self.get_pezzo(pos_re)
        torre = self.get_pezzo(pos_torre)

        if re is None: 
            raise GE.ErroreArrocco("Il Re non è presente nella posizione iniziale.")
        
        if torre is None:
            raise GE.ErroreArrocco("La Torre non è presente nella posizione iniziale.")
        
        if re.isMosso(): 
            raise GE.ErroreArrocco("Il Re è già stato mosso, non puoi arroccare.")
        
        if torre.isMosso():
            raise GE.ErroreArrocco("La Torre è già stata mosso, non puoi arroccare.")
        
        for pos in pos_intermedie:
            if not self.posizioneLibera(pos):
                raise GE.ErroreArrocco(
                    "Una delle caselle utile per l'arrocco è occupata."
                )
        
        if self.casella_sotto_attacco(pos_re, avversario):
            raise GE.ErroreArrocco(
                "Il Re è sotto scacco, non puoi arroccare."
            )

        pos_re_passaggio = pos_intermedie if tipo_arrocco == "corto" else [pos_intermedie[1], pos_intermedie[2]]
        for pos in pos_re_passaggio:
            if self.casella_sotto_attacco(pos, avversario):
                raise GE.ErroreArrocco(
                    "Una delle caselle utile per l'arrocco è sotto attacco."
                )

        return {
            "re": pos_re,
            "torre": pos_torre,
            "arrivo_re": pos_arrivo_re,
            "arrivo_torre": pos_arrivo_torre,
            "tipo_arrocco": tipo_arrocco
        }
    
    def eseguiArrocco(self, info_arrocco: dict):
        """Esegue l'arrocco sulla scacchiera spostando Re e Torre.

        Args:
            info_arrocco (dict): contiene posizioni di partenza e arrivo

        """
        pos_re = info_arrocco['re']
        pos_torre = info_arrocco['torre']
        arrivo_re = info_arrocco['arrivo_re']
        arrivo_torre = info_arrocco['arrivo_torre']

        self.muovi_pezzo(pos_re, arrivo_re)
        self.muovi_pezzo(pos_torre, arrivo_torre)

        torre = self.get_pezzo(arrivo_torre)
        re = self.get_pezzo(arrivo_re)

        torre.mosso()
        re.mosso()
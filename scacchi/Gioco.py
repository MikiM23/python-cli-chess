from scacchi.GestoreTurni import GestoreTurni
from scacchi.Giocatore import Giocatore
from scacchi.Scacchiera import Scacchiera


class Gioco: 
    """<<Entity>> Classe che rappresenta una partita di scacchi."""

    def __init__(self, giocatore_bianco, giocatore_nero):
        """Inizializza una nuova partita a scacchi.

        Crea una nuova scacchiera, assegna i due giocatori,
        imposta il turno iniziale al giocatore bianco e avvia lo stato della partita.

        Args:
            giocatore_bianco (Giocatore): Il giocatore con i pezzi bianchi.
            giocatore_nero (Giocatore): Il giocatore con i pezzi neri.

        """
        self.scacchiera = Scacchiera()
        self.turno = GestoreTurni(giocatore_bianco, giocatore_nero)
        self.vincitore = None
        self.inGioco = True
        self.patta_richiesta = False
        self.avvisoTurno()
        self.mosse = []

    def avvisoTurno(self):
        """Mostra la scacchiera e il nome del giocatore a cui tocca il turno."""
        giocatore_corrente = self.turno.ottieni_turno()
        nome = giocatore_corrente.ottieni_nome()
        simbolo = giocatore_corrente.ottieni_simbolo()
        print(f"\nÈ il turno di {nome} ({simbolo})! Fai la tua mossa 😁\n")
        self.scacchiera.mostraScacchiera()
    
    def registraMossa(self,
                      info_mossa: dict,
                      mossa: str,
                      giocatore: Giocatore,
                      numero_turno: int):
        """Registra una mossa effettuata da un giocatore.
        
        Args:
            info_mossa (dict): Informazioni sulla mossa, come il pezzo e la posizione.
            mossa (str): La mossa effettuata.
            giocatore (Giocatore): Il giocatore che ha effettuato la mossa.
            numero_turno (int): Il numero del turno corrente.

        """
        self.mosse.append(
            {
                "info_mossa": info_mossa, 
                "mossa": mossa, 
                "giocatore": giocatore, 
                "turno": numero_turno
        })
        
    def mostraMosse(self):
        """Mostra tutte le mosse effettuate durante la partita."""
        print("\nMosse effettuate:")

        if len(self.mosse) == 0:
            print("Nessuna mossa effettuata.")
            print("\n")
            return

        giocatori = [m['giocatore'] for m in self.mosse[:2]]
        max_nome_len = max(len(g.ottieni_nome()) for g in giocatori)

        for mossa in self.mosse:
            turno = mossa['turno']
            simbolo = mossa['giocatore'].ottieni_simbolo()
            nome = mossa['giocatore'].ottieni_nome().ljust(max_nome_len)
            print(f"{turno}: {simbolo} {nome} --> {mossa['mossa']}")

        print("\n")
    
    def pattaRichiesta(self):
        """Segna la richiesta di patta da parte del giocatore corrente."""
        self.patta_richiesta = True
    
    def resetPatta(self):
        """Resetta lo stato della richiesta di patta."""
        self.patta_richiesta = False
    
    def getPattaRichiesta(self):
        """Restituisce lo stato della richiesta di patta.
        
        Returns:
            bool: True se una richiesta di patta è stata fatta, False altrimenti.

        """
        return self.patta_richiesta
    
    def scaccoGiocatore(self, giocatore: Giocatore):
        """Mostra il messaggio di scacco al giocatore.
        
        Args:
            giocatore (Giocatore): giocatore sotto scacco
        
        """
        visual_giocatore = f"{giocatore.ottieni_simbolo()} {giocatore.ottieni_nome()}"
        print(f"{visual_giocatore} il tuo Re è sotto scacco!")
    
    def scaccoMatto(self, giocatore: Giocatore) -> None:
        """Mostra il messaggio di scacco matto e di fine partita.
        
        Args:
            giocatore (Giocatore): vincitore
        
        Returns:
            None: partita finita

        """
        visual_giocatore = f"{giocatore.ottieni_simbolo()} {giocatore.ottieni_nome()}"
        print(f"Scacco Matto! {visual_giocatore} complimenti, hai vinto!")

    def stallo(self) -> None:
        """Mostra il messaggio di stallo e di fine partita.
        
        Returns:
            None: partita finita

        """
        print("Stallo! La partita termina in pareggio.")

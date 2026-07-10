import sys

from scacchi.Giocatore import Giocatore
from scacchi.Gioco import Gioco


class Comandi:
    """<<Control>> Classe responsabile della gestione dei comandi dell'applicazione.

    Contiene la lista dei comandi disponibili e i metodi per eseguirli.
    """

    def __init__(self):
        """Inizializza il dizionario dei comandi disponibili con la loro descrizione."""
        self.comandi = {
            "/help": "Mostrare la lista dei comandi",
            "/gioca": "Iniziare la partita",
            "/scacchiera": "Mostrare la scacchiera",
            "/mosse": "Mostrare cronologia mosse",
            "/abbandona": "Abbandonare la partita",
            "/patta": "Richiedere il pareggio",
            "/esci": "Chiudere l'applicazione"
        }

    def mostraComandi(self):
        """Mostra i comandi che l'utente può eseguire."""
        print("Lista comandi disponibili:")
        for cmd, desc in self.comandi.items():
            print(f"   {cmd.ljust(12)} -> {desc}")
        print("")

    def chiediConferma(self, azione) -> bool:
        """Chiede conferma all'utente per un'azione che vuole svolgere.

        Args:
            azione (str): azione che l'utente vuole eseguire

        Returns:
            bool: True se l'utente conferma, False altrimenti

        """
        print(f"{azione}? (s/n)")

        while True:
            conferma = input().strip().lower()
            if conferma in ['s', 'n']:
                return conferma == 's'
            print("!! Errore, input non valido. Inserire s per sì o n per no.")
            
    def gestisciUscita(self):
        """Gestisce il comando /esci con conferma utente.

        La funzione continua a chiedere finché l'input non è valido ('s' o 'n').
        """
        conferma = self.chiediConferma("Sei sicuro di voler uscire dall'applicazione")
        if conferma:
            print("Uscita dall'applicazione. Alla prossima!")
            sys.exit(0)
        else:
            print("Inserire un nuovo tentativo o comando:")

    def gioca(self) -> Gioco:
        """Avvia una nuova partita di scacchi."""
        giocatore_bianco = Giocatore.crea_da_input("bianco")
        giocatore_nero = Giocatore.crea_da_input("nero")
        return Gioco(giocatore_bianco, giocatore_nero)
    
    def abbandonaPartita(self, gioco: Gioco) -> Gioco | None:
        """Chiede conferma all'utente per abbandonare la partita in corso.

        Args:
            gioco (Gioco): Oggetto che rappresenta la partita attualmente in corso.

        Returns:
            gioco (Gioco): aggiornato se l'utente decide di continuare, 
            None: se la partita viene abbandonata o se nessuna partita è in corso.

        """
        if gioco is not None:
            if self.chiediConferma("Sei sicuro di voler abbandonare la partita"):
                gioco.turno.cambia_turno()
                vincitore = gioco.turno.ottieni_turno()
                nome_vincitore = (
                    f"{vincitore.ottieni_nome()} ({vincitore.ottieni_simbolo()})"
                )
                print(
                    "Hai abbandonato la partita. "
                    f"{nome_vincitore} ha vinto per abbandono! 🥳"
                )
                return None
            else:
                print("Hai deciso di continuare la partita.")
                return gioco
        else:
            print("Nessuna partita è in corso.")

    def patta(self, gioco: Gioco) -> None | bool:
        """Metodo per gestire la richiesta di patta.

        Args:
            gioco (Gioco): Oggetto che rappresenta la partita attualmente in corso.

        Returns:
            None | bool: None se la partita non è in corso, 
            bool se la patta è accettata o rifiutata.

        """
        if gioco is None:
            return None
        if gioco.getPattaRichiesta():
            print("!! Hai già richiesto la patta in questo turno.")
            return False
        gioco.pattaRichiesta()
        richiedente_patta = gioco.turno.ottieni_turno()
        accettante_patta = gioco.turno.ottiene_turno_avversario()

        print(
            f"{richiedente_patta.ottieni_nome()} "
            f"({richiedente_patta.ottieni_simbolo()}) ha richiesto la patta."
        )

        richiesta = (
            f"{accettante_patta.ottieni_nome()} "
            f"({accettante_patta.ottieni_simbolo()}), accetti la patta?"
        )
        accetta = self.chiediConferma(richiesta)

        if accetta:
            print("\n=== PARTITA TERMINATA IN PAREGGIO ===\n")
            return True
        else:
            print(
                f"-- {accettante_patta.ottieni_nome()} ha rifiutato la patta."
            )
            return False

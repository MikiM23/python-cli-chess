from scacchi.Giocatore import Giocatore


class GestoreTurni:
    """<<Control>> Classe che gestisce i turni dei giocatori in partita."""

    def __init__(self, giocatore_bianco, giocatore_nero):
        """Inizializza i due giocatori e il turno corrente su giocatore_bianco.

        Args:
            giocatore_bianco (Giocatore): giocatore bianco
            giocatore_nero (Giocatore): giocatore nero

        """
        self.giocatore_bianco = giocatore_bianco
        self.giocatore_nero = giocatore_nero
        self.turno_corrente = giocatore_bianco
        self.n_turno = 1
        self.cambio_turno = 0
        
    def cambia_turno(self):
        """Cambia il turno del giocatore.
        
        Passa il turno dal giocatore corrente al successivo, 
        se entrambi i giocatori hanno effettuato una mossa incrementa n_turno.
        """
        self.turno_corrente = (
            self.giocatore_nero if self.turno_corrente == self.giocatore_bianco 
            else self.giocatore_bianco
        )
        self.cambio_turno = 1 - self.cambio_turno  
        self.n_turno = self.n_turno if self.cambio_turno == 1 else self.n_turno + 1

    def ottieni_turno(self) -> Giocatore:
        """Restituisce il giocatore che deve effettuare il turno.

        Returns:
            turno_corrente (Giocatore): giocatore del turno

        """
        return self.turno_corrente
    
    def ottiene_turno_avversario(self) -> Giocatore:
        """Restituisce il giocatore avversario a quello corrente.

        Returns:
            Giocatore: giocatore avversario

        """
        return (
            self.giocatore_nero 
            if self.turno_corrente == self.giocatore_bianco 
            else self.giocatore_bianco
        )

    def ottieni_numero_turno(self) -> int:
        """Restituisce il numero del turno corrente.
        
        Returns:
            n_turno (int): numero del turno corrente

        """
        return self.n_turno
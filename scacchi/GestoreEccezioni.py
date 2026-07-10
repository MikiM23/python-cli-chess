

class GestoreEccezioni:
    """<<Control>> Classe per gestire le eccezioni.
    
    Ha il compito di gestire le eccezioni e i messaggi per l'tutente.
    """

    class ErroreArgomento(Exception):
        """<<Control>> Sollevata in caso di argomento errato."""

        def __init__(self, msg="Argomento non valido. Usare -h o --help."):
            """Inizializza l'eccezione con il messaggio personalizzato.
            
            Args:
                msg (str): messaggio di errore per l'argomento errato
                
            """
            super().__init__(msg)
    
    class ComandoNonValido(Exception):
        """<<Control>> Sollevata in caso di comando errato."""
        
        def __init__(self, 
                     msg="Comando non valido. Usare /help per la lista dei comandi."):
            """Inizializza l'eccezione con il messaggio personalizzato.
            
            Args:
                msg (str): messaggio di errore per il comando non valido

            """
            super().__init__(msg)
    
    class MossaNonValida(Exception):
        """<<Control>> Eccezione generica per una mossa non valida."""
        
        def __init__(self, msg="Mossa non valida."):
            """Inizializza l'eccezione con il messaggio personalizzato.
            
            Args:
                msg (str): messaggio di errore per la mossa non valida
                
            """
            super().__init__(msg)
    
    class NessunPezzoSelezionato(MossaNonValida):
        """<<Control>> Eccezione per mossa con casella selezionata vuota.

        Sollevata quando l'utente tenta una mossa indicando una casella che non contiene
        un proprio pezzo.
        """

        def __init__(self, msg="Nessun pezzo selezionato."):
            """Inizializza l'eccezione con il messaggio personalizzato.
            
            Args:
                msg (str): messaggio di errore per tentativo di mossa 
                con pezzo non selezionato
                
            """
            super().__init__(msg)
        
    class MossaNonConsentita(MossaNonValida):
        """<<Control>> Sollevata quando l'utente tenta una mossa contro le regole."""

        def __init__(self, pezzo=None):
            """Inizializza l'eccezione con il messaggio personalizzato.
            
            Args:
                pezzo (str): nome del pezzo con cui si sta tentando una mossa
                contro le regole
                
            """
            msg = (
                f"Mossa non consentita per il pezzo {pezzo}." 
                if pezzo
                else "Mossa non consentita.")
            super().__init__(msg)

    class MossaFuoriSccacchiera(MossaNonValida):
        """<<Control>> Sollevata quando si tenta una mossa fuori dalla scacchiera."""

        def __init__(self, msg="Tentata mossa fuori dalla scacchiera."):
            """Inizializza l'eccezione con il messaggio personalizzato.
            
            Args:
                msg (str): messaggio di errore per il tentativo di una mossa 
                la cui destinazione è fuori dalla scacchiera
                
            """
            super().__init__(msg)

    class DestinazioneOccupata(MossaNonValida):
        """<<Control>> Eccezione per mossa con destinazione occupata.
        
        Sollevata quando la casella di destinazione è occupata da un pezzo alleato. 
        """

        def __init__(self,
                     msg="La casella di destinazione è occupata da un pezzo alleato."):
            """Inizializza l'eccezione con il messaggio personalizzato.
            
            Args:
                msg (str): messaggio di errore per il tentativo di una mossa 
                la cui destinazione è occupata da un pezzo dello stesso colore
                
            """
            super().__init__(msg)
    
    class ColoreNonValido(Exception):
        """<<Control>> Sollevata quando il colore del giocatore non è valido."""
        
        def __init__(self, msg="Il colore deve essere 'bianco' o 'nero'."):
            """Inizializza l'eccezione con il messaggio personalizzato.
            
            Args:
                msg (str): messaggio di errore per il colore del pezzo errato,
                può essere o bianco o nero
                
            """
            super().__init__(msg)
    
    class NotazioneNonValida(Exception):
        """<<Control>> Sollevata quando la notazione della mossa non è valida."""
        
        def __init__(self, msg):
            """Inizializza l'eccezione con il messaggio personalizzato.
            
            Args:
                msg (str): messaggio di errore per la notazione della mossa non valida
                
            """
            super().__init__(msg)
        
    class PromozioneNonValida(MossaNonValida):
        """<<Control>> Sollevata quando la promozione del pedone non è valida."""
        
        def __init__(self, msg):
            """Inizializza l'eccezione con il messaggio personalizzato.
            
            Args:
                msg (str): messaggio di errore per la promozione del pedone non valida
                
            """
            super().__init__(msg)
    
    @staticmethod
    def errore(msg):
        """Comunica all'utente un errore.
        
        Args:
            msg (str): errore da comunicare all'utente

        """
        print(f"[ERRORE] {msg}")
    
    @staticmethod
    def warning(msg):
        """Comunica all'utente un avviso importante.
                
        Args:
            msg (str): avviso da comunicare all'utente
            
        """
        print(f"[ATTENZIONE] {msg}")
    
    @staticmethod
    def info(msg):
        """Comunica all'utente un'informazione.
         
        Args:
            msg (str): informazione da comunicare all'utente
        
        """
        print(f"[INFO] {msg}")

    class ErroreArrocco(Exception):
        """<<Control>> Sollevata quando c'è un errore con l'arrocco."""

        def init(self, msg):
            """Inizializza l'eccezione con il messaggio personalizzato.

            Args:
                msg (str): messaggio di errore per l'errore con l'arrocco

            """
            super().init(msg)
from scacchi.GestoreEccezioni import GestoreEccezioni as GE
from scacchi.Pezzi.Pezzo import Pezzo


class Giocatore:
    """<<Entity>> Classe che rappresenta un giocatore di scacchi."""

    def __init__(self, colore: str):
        """Inizializza il giocatore e imposta il colore.

        Args:
            colore (str): Colore del giocatore, deve essere 'bianco' o 'nero'.

        """
        if colore not in ["bianco", "nero"]:
            raise GE.ColoreNonValido()
        self.colore = colore
        self.nome = ""
        self.pezzi_mangiati = []
        self._arrocco_corto = False
        self._arrocco_lungo = False

    def __str__(self) -> str:
        """Visualizza il giocatore.

        Returns:
            str: simbolo e nome del giocatore

        """
        return f"{self.ottieni_simbolo()} {self.ottieni_nome()}"

    def ottieni_simbolo(self) -> str:
        """Restituisce il simbolo associato al colore del giocatore.

        Returns:
            str: Simbolo associato al colore del giocatore.

        """
        return '⚪️' if self.colore == "bianco" else '⚫️'

    def ottieniColore(self) -> str:
        """Restituisce il colore del giocatore.

        Returns:
            colore (str): bianco o nero

        """
        return self.colore

    def imposta_colore(self, colore: str):
        """Imposta il colore del giocatore (bianco o nero)."""
        self.colore = colore

    def imposta_nome(self, nome: str):
        """Imposta il nome del giocatore.

        Args:
            nome (str): nome del giocatre

        """
        self.nome = nome

    def ottieni_nome(self) -> str:
        """Restituisce il nome del giocatore.

        Returns:
            str: nome del giocatore

        """
        return self.nome
    
    @classmethod
    def crea_da_input(cls, colore: str):
        """Crea un nuovo giocatore chiedendo il nome all'utente.

        Args:
            colore (str): Colore del giocatore ('bianco' o 'nero').

        Returns:
            Giocatore: Il giocatore creato.

        """
        try:
            nome = input(f"Inserisci il nome del giocatore {colore}: ").strip()
        except Exception as e:
            GE.errore(f"Errore durante l'inserimento del nome del giocatore: {e}")
            giocatore = cls(colore)
            giocatore.imposta_nome(colore)
            return giocatore
        giocatore = cls(colore)
        giocatore.imposta_nome(nome)
        return giocatore
    
    def aggiungiPezzoMangiato(self, pezzo: Pezzo):
        """Aggiunge un pezzo mangiato dal giocatore alla lista dei pezzi mangiati.

        Args:
            pezzo: Il pezzo mangiato da aggiungere alla lista.

        """
        self.pezzi_mangiati.append(pezzo)
    
    def numeroPezziMangiati(self) -> int:
        """Restituisce il numero di pezzi mangiati dal giocatore.

        Returns:
            int: Numero di pezzi mangiati dal giocatore.

        """
        return len(self.pezzi_mangiati)

    def ottieniPezziMangiati(self) -> list[Pezzo]:
        """Restituisce la lista dei pezzi mangiati dal giocatore.

        Returns:
            list[Pezzo]: Lista dei pezzi mangiati dal giocatore.

        """
        return self.pezzi_mangiati
    
    def arroccoCorto(self) -> bool:
        """Restituisce se il giocatore ha effettuato l'arrocco corto."""
        return self._arrocco_corto
    
    def arroccoLungo(self) -> bool:
        """Restituisce se il giocatore ha effettuato l'arrocco lungo."""
        return self._arrocco_lungo
    
    def arroccoEseguito(self, tipo_arrocco: str):
        """Imposta lo stato dell'arrocco del giocatore.

        Args:
            tipo_arrocco (str): 'corto' o 'lungo'

        """
        if tipo_arrocco == "corto":
            self._arrocco_corto = True
        else:
            self._arrocco_lungo = True
    
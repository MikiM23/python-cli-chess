import sys

from scacchi.Comandi import Comandi
from scacchi.GestoreEccezioni import GestoreEccezioni as GE
from scacchi.Giocatore import Giocatore
from scacchi.Parser import Parser
from scacchi.Pezzi.Re import Re


class Applicazione:
    """<<Boundary>> Classe ciclo vitale dell'applicazione.

    Gestisce l'avvio del programma e controlla gli argomenti passati.
    """

    def __init__(self):
        """Inizializza l'applicazione con gli attributi gioco e comandi."""
        self.gioco = None # attributo per la classe game da implementare
        self.comandi = Comandi()
        self.parser = Parser()
        self.richiestaPattaInCorso = False
        self.richiedenti_patta = (None, None)
    
    def analizzaArgomenti(self) -> str:
        """Verifica se viene passato come argomento -h o --help.
        
        Returns:
            str: stato argomento passato
        
        """
        if len(sys.argv) > 1:
            cmd = sys.argv[1]
            if cmd in ["-h", "--help"]:
                return "help"
            else:
                return "error"
        return "normal"
    
    def gestioneArgomentiAvvio(self):
        """Mostra i comandi se l'argomento è riconosciuto altrimenti esce con errore."""
        stato = self.analizzaArgomenti()
        if stato == "help":
            self.comandi.mostraComandi()
        elif stato == "error":
            GE.errore(
                "!! Errore, argomento non valido. "
                "Usare -h o --help per la lista dei comandi.")

    def avvia(self):    
        """Ciclo per i comandi inseriti dall'utente."""
        while True:
            cmd = self.inputComando()
            self.gestioneComando(cmd)
        
    def inputComando(self) -> str:
        """Riceve il comando in input dall'utente e lo processa.
        
        Returns:
            cmd (str)

        """
        cmd = input("-> ").strip()
        if "/" in cmd:
            return cmd.lower()
        return cmd

    def gestioneComando(self, cmd: str):
        """Controlla se il comando è riconosciuto e lo esegue.

        Args:
            cmd (str): coomando dell'utente

        """
        if cmd == "/help":
            self.comandi.mostraComandi()
        
        elif cmd == "/esci":
            self.comandi.gestisciUscita()
        
        elif cmd == "/gioca":
            if self.gioco is None:
                self.gioco = self.comandi.gioca()
        
        elif cmd == "/scacchiera":
            if self.gioco is None:
                print("!! Errore, partita non iniziata. Digita /gioca per avviarla")
            else:
                self.gioco.scacchiera.mostraScacchiera()   
        elif cmd == "/mosse":
            if not self.gioco:
                GE.errore("Nessuna partita in corso. Digita /gioca per avviarla")
                return
            self.gioco.mostraMosse()   
                   
        elif cmd == "/patta":
            patta = self.comandi.patta(self.gioco)
            if patta is None:
                GE.errore("!! Errore, partita non iniziata. Digita /gioca per avviarla")
                return
            elif patta:
                self.gioco = None
        
        elif cmd == "/abbandona":
            self.gioco = self.comandi.abbandonaPartita(self.gioco)
        
        elif self.parser.riconosciMossa(cmd):
            if not self.gioco:
                GE.errore(
                    "Nessuna partita in corso. "
                    "Usa /gioca per iniziare una nuova partita.")
                return
            
            info_mossa = self.parser.ottieniInfoMossa(cmd)
            if not info_mossa:
                return
            info_mossa["giocatore"] = self.gioco.turno.ottieni_turno()

            if "arrocco" in info_mossa:
                self.tentaMossa(cmd,info_mossa, (0, 0))
                return
        
            """
            self.parser.validaMossa(info_mossa,
                                    self.gioco.scacchiera, 
                                    self.gioco.turno.ottieni_turno())"""
            try:
                posizione_pezzo_da_muovere = self.parser.trovaPezzi(info_mossa, 
                                                                    self.gioco.scacchiera,
                                                                    self.gioco.turno.ottieni_turno())
            except Exception as e:
                GE.errore(e)
                return

            info_mossa["pos_pezzo_da_muovere"] = posizione_pezzo_da_muovere
            

            if posizione_pezzo_da_muovere:
                if self.gioco.scacchiera.get_pezzo(posizione_pezzo_da_muovere) is None:
                    GE.errore("!! Errore, nessun pezzo selezionato.")
                    return
                info_mossa = self.parser.controlla_en_passant(info_mossa, 
                                                          self.gioco.scacchiera)
                colore_giocatore = self.gioco.turno.ottieni_turno().ottieniColore()
                if self.gioco.scacchiera.re_sotto_scacco(colore_giocatore):
                    mosse_salvanti = self.gioco.scacchiera.mosse_salva_re(
                        colore_giocatore
                    )
                    pos_arrivo = (info_mossa["dest_riga"], info_mossa["dest_col"])
                    posizione_tentata = (posizione_pezzo_da_muovere, pos_arrivo)
                    if posizione_tentata not in mosse_salvanti:
                        GE.errore(
                            "Il tuo re è sotto scacco, "
                            "fai una mossa che lo metta in salvo!"
                        )
                        return
                self.tentaMossa(cmd,
                                info_mossa,
                                posizione_pezzo_da_muovere)
            else:
                GE.errore(
                    "Nessun pezzo valido trovato per la mossa. "
                    "Controlla la notazione.")
        else:
            GE.errore(f"!! Errore, {cmd} comando/mossa non valida")

    def tentaMossa(self, 
               mossa: str,
               info_mossa: dict,
               posizione_iniziale: tuple[int, int]):
        """Controlla se la mossa è valida e la esegue.
        
        Args:
            mossa (str): mossa dell'utente
            info_mossa (dict): informazioni sulla mossa
            posizione_iniziale (int, int): posizione iniziale del pezzo

        """
        turno_corrente: Giocatore = self.gioco.turno.ottieni_turno()
        scacchiera = self.gioco.scacchiera
        giocatore: Giocatore = info_mossa["giocatore"]

        if not info_mossa.get("arrocco", False):
            posizione_finale = (info_mossa["dest_riga"], info_mossa["dest_col"])

            pezzo_selezionato = scacchiera.get_pezzo(posizione_iniziale)
            pezzo_destinazione = scacchiera.get_pezzo(posizione_finale)

            if pezzo_selezionato.__class__.__name__ == "Re":
                colore_giocatore = turno_corrente.ottieniColore()
                colore_avversario = "nero" if colore_giocatore == "bianco" else "bianco"
                sotto_attacco = scacchiera.casella_sotto_attacco(
                    posizione_finale,
                    colore_avversario
                    )
                if sotto_attacco:
                    GE.errore("Mossa non valida: il Re finirebbe sotto scacco.")
                    return

            ultima_mossa = (
                self.gioco.mosse[-1]['info_mossa'] if self.gioco.mosse else None
            )
            en_passant = (
                ultima_mossa.get("en_passant_possibile", False)
                if ultima_mossa else False
            )
            en_passant_dest = (
                ultima_mossa.get("en_passant_destinazione")
                if ultima_mossa else None
            )
            en_passant_vittima = (
                ultima_mossa.get("en_passant_vittima")
                if ultima_mossa else None
            )

            if info_mossa["pezzo"] == "P":
                promozioneValida = self.gioco.scacchiera.promozioneValida(
                    posizione_finale,
                    giocatore.ottieniColore())
                    
                if promozioneValida and info_mossa["promozione"] is None:
                    GE.errore(
                        "Non hai specificato la promozione del pedone. "
                        "Usa la notazione algebrica per specificare la promozione "
                        "(es. e8D per promuovere a regina).")
                    return
                    
                if not promozioneValida and info_mossa["promozione"] is not None:
                    GE.errore(
                        "Promozione non valida. "
                        "Il pedone può essere promosso solo all'ultima riga.")
                    return

        # Tentativo di cattura
        if info_mossa.get("cattura", False):
            if pezzo_destinazione is None:
                if not en_passant or tuple(posizione_finale) != tuple(en_passant_dest):
                    GE.errore("!! Errore, nessun pezzo da catturare.")
                    return

                scacchiera_simulata = scacchiera.copia_scacchiera()
                scacchiera_simulata.muovi_pezzo(posizione_iniziale, posizione_finale)
                if en_passant_vittima:
                    scacchiera_simulata.rimuoviPezzo(en_passant_vittima)
                if scacchiera_simulata.re_sotto_scacco(turno_corrente.ottieniColore()):
                    GE.errore("Mossa non valida: il tuo Re finirebbe sotto scacco.")
                    return

                # Esegui en passant
                if en_passant_vittima:
                    pezzo_vittima = scacchiera.get_pezzo(en_passant_vittima)
                    if pezzo_vittima:
                        turno_corrente.aggiungiPezzoMangiato(pezzo_vittima)
                    scacchiera.rimuoviPezzo(en_passant_vittima)
                scacchiera.muovi_pezzo(posizione_iniziale, posizione_finale)
                info_mossa['en_passant_eseguito'] = True

            else:
                if pezzo_destinazione.getColore() == turno_corrente.ottieniColore():
                    GE.errore("!! Errore, non puoi catturare un tuo pezzo.")
                    return
                if isinstance(pezzo_destinazione, Re):
                    GE.errore("!! Errore, non puoi catturare il re.")
                    return

                scacchiera_simulata = scacchiera.copia_scacchiera()
                scacchiera_simulata.catturaPezzo(posizione_iniziale, posizione_finale)
                if scacchiera_simulata.re_sotto_scacco(turno_corrente.ottieniColore()):
                    GE.errore("Mossa non valida: il tuo Re finirebbe sotto scacco.")
                    return

                pezzo_catturato = self.gioco.scacchiera.get_pezzo(posizione_finale)
                if pezzo_catturato:
                    turno_corrente.aggiungiPezzoMangiato(pezzo_catturato)
                scacchiera.catturaPezzo(posizione_iniziale, posizione_finale)

        elif info_mossa.get("arrocco", False):
            try:
                arrocco_possibile = self.gioco.scacchiera.arroccoPossibile(
                self.gioco.turno, info_mossa["arrocco"]
                )
            except Exception as e:
                GE.errore(e)
                return
            if arrocco_possibile:
                self.gioco.scacchiera.eseguiArrocco(arrocco_possibile)
                giocatore.arroccoEseguito(info_mossa["arrocco"])
        else:
                
            if pezzo_destinazione is not None:
                GE.errore("!! Errore, la posizione di destinazione non è libera.")
                return
            
            scacchiera_simulata = scacchiera.copia_scacchiera()
            scacchiera_simulata.muovi_pezzo(posizione_iniziale, posizione_finale)
            if scacchiera_simulata.re_sotto_scacco(turno_corrente.ottieniColore()):
                GE.errore("Mossa non valida: il tuo Re finirebbe sotto scacco.")
                return

            scacchiera.muovi_pezzo(posizione_iniziale, posizione_finale)
        
        if info_mossa.get("promozione") is not None:
            try:
                self.gioco.scacchiera.promuoviPedone(posizione_finale,
                                                info_mossa["promozione"],
                                                giocatore.ottieniColore())
            except Exception as e:
                GE.errore(f"{e}")
                return
            
        if info_mossa.get("pezzo") in ["T", "R"]:
            pezzo_selezionato.mosso()
        
        # Registra mossa e aggiorna il turno
        self.gioco.registraMossa(
            info_mossa,
            mossa,
            turno_corrente,
            self.gioco.turno.ottieni_numero_turno()
        )
        self.gioco.turno.cambia_turno()
        self.gioco.avvisoTurno()
        self.gioco.resetPatta()


        # --- INIZIO controllo scacco/scacco matto ---

        colore_avversario = self.gioco.turno.ottieni_turno().ottieniColore()
        scacchiera = self.gioco.scacchiera

        # Controlla se il re avversario è sotto scacco
        if scacchiera.re_sotto_scacco(colore_avversario):
            # Trova tutte le mosse legali per il colore avversario che salvano il re
            mosse_salvavita = self.gioco.scacchiera.mosse_salva_re(colore_avversario)
            
            if not mosse_salvavita:
                self.gioco = self.gioco.scaccoMatto(
                    self.gioco.turno.ottiene_turno_avversario())  # Termina la partita
                self.gioco.mosse[-1]['mossa'].append("#")
                return
            else:
                self.gioco.scaccoGiocatore(self.gioco.turno.ottieni_turno())
                self.gioco.mosse[-1]['mossa'].append("+")
        else:
            # Controlla stallo (patta per mancanza di mosse legali senza scacco)
            mosse_legali = self.gioco.scacchiera.mosse_salva_re(colore_avversario)
            if not mosse_legali:
                self.gioco = self.gioco.stallo()  # Termina la partita
                return

        # --- FINE controllo scacco/scacco matto ---
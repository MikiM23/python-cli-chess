# MANUALE UTENTE

### 1. Introduzione al Gioco degli Scacchi
Gli scacchi sono un gioco da tavolo strategico per due giocatori. Considerato uno dei giochi più antichi e più profondi al mondo, gli scacchi combinano abilità, tattica, logica e previsione. Ogni partita si gioca su una scacchiera 8x8 e ha l'obiettivo finale di dare "scacco matto" al re avversario, ovvero metterlo sotto attacco in modo tale che non possa sfuggire.

Il gioco degli scacchi ha origini antichissime che risalgono probabilmente all'India del VI secolo, dove era conosciuto come *chaturanga*. Da lì si diffuse in Persia (come *shatranj*) e successivamente nel mondo islamico e in Europa medievale, subendo varie evoluzioni fino alla forma moderna attuale, stabilizzata tra il XV e il XIX secolo.  
Oggi, gli scacchi sono un gioco riconosciuto a livello globale, praticato sia a livello amatoriale sia professionale, con tornei internazionali e una federazione ufficiale: la FIDE (Fédération Internationale des Échecs).

---

### La Scacchiera
<p align="left">
  <img src="img/scacchiera_gioco_scacchi.jpg" alt="Scacchiera" width="400">
</p>

La scacchiera è composta da:

- **8 righe** (numerate da 1 a 8)
- **8 colonne** (indicate con le lettere da a a h)
- In totale **64 caselle** 

Esempio di coordinate: `e4` indica la colonna **e** e la riga **4**.

---

### I Pezzi del Gioco

Ogni giocatore (bianco e nero) inizia con **16 pezzi**, per un totale di **32 pezzi** sulla scacchiera:

- **1 Re**
- **1 Donna (Regina)**
- **2 Alfieri**
- **2 Cavalli**
- **2 Torri**
- **8 Pedoni**

Ogni pezzo ha un tipo di movimento specifico e un valore strategico nel gioco.

---

### Obiettivo del Gioco

L'obiettivo è dare **scacco matto** al re avversario: una condizione in cui il re è sotto attacco e non può effettuare alcuna mossa per mettersi al sicuro.

### Movimento dei Pezzi

- **Re**: si muove di una casella in qualsiasi direzione
- **Donna**: si muove in linea retta in qualsiasi direzione (orizzontale, verticale, diagonale)
- **Torre**: si muove in linea retta solo in orizzontale o verticale
- **Alfiere**: si muove solo in diagonale
- **Cavallo**: si muove a "L" (due caselle in una direzione, poi una perpendicolare) e può saltare sopra altri pezzi
- **Pedone**: si muove in avanti di una casella (due dalla posizione iniziale) e cattura in diagonale

### Notazione Algebrica

Lo standard internazionale per descrivere le mosse nel gioco degli scacchi è la **notazione algebrica**. Essa prevede che la scacchiera sia composta da:

- **8 colonne**, etichettate con le lettere dalla **a** alla **h**
- **8 righe**, numerate dalla **1** alla **8**

<p align="left">
  <img src="img/notazione_algebrica.png" alt="notazione_algebrica" width="400">
</p>

Ogni casella ha un nome univoco: ad esempio, la casella nell’angolo in basso a sinistra è `a1`, mentre quella in alto a destra è `h8`.
Le mosse vengono scritte specificando **la posizione di arrivo** del pezzo:
`e4`

Questo significa che il pezzo si sposta **nella casella e4**.

##### Esempi di mosse

- `e4` → un pedone si muove  per andare in e4
- `Dd4` → un a regina  si muove  per andare in d4
- `Tc1` →  una torre si muove per andare in c1

##### Regole di validità

- Le mosse devono essere **legalmente valide** secondo le regole degli scacchi
- Il formato deve essere sempre caratteri senza separazione (niente spazi o altri caratteri)
- I caratteri devono essere minuscoli e nel formato corretto ([a-h][1-8])
- La mossa deve sempre iniziare con la lettera maiuscola dell'iniziale del pezzo (es. C per cavallo), tranne per il pedone.

| **Pezzo**  | **Iniziale (Notazione Algebrica Italiana)** |
|------------|---------------------------------------------|
| Re         | R                                           |
| Regina     | D                                           |
| Torre      | T                                           |
| Alfiere    | A                                           |
| Cavallo    | C                                           |
| Pedone     | *(nessuna iniziale)*                        |


### 2. Comandi del gioco

All'avvio del gioco viene mostrata una interfaccia ASCII art col menù principale.

<p align="left">
  <img src="img/menu_principale.png" alt="menu_principale" width="400">
</p>

Una volta che l'utente sceglie uno dei comandi visualizzati e preme invio, tale comando verrà eseguito. Se tale comando non fosse valido, verrà mostrato il relativo messaggio d'errore

<p align="left">
  <img src="img/msg_comando_errato.png" alt="msg_comando_errato" width="400">
</p>

#### I comandi dell'applicazione
Vi sono due tipologie di comandi:
* Comandi iniziali (mostrati nel menu principale): /gioca, /help, /esci
* Comandi in gioco (richiamabili in ogni momento quando si sta giocando): /help, /gioca, /scacchiera, /mosse, /abbandona, /patta, /esci

#### Comando /help
Per visualizzare tutti i 7 comandi disponibili con la loro descrizione, l'utente dovrà digitale il comando "/help" e premere invio.

<p align="left">
  <img src="img/comando_help.png" alt="comando_help" width="400">
</p>

#### Comando /gioca
Per cominciare una nuova partita l'utente deve scrivere il comando "/gioca" e premere invio. L'applicazione chiederà il nome dei 2 giocatori (per primo quello con i pezzi bianchi e quello coi pezzi neri) e una volta inseriti, mostrerà l'utente di cui è il turno.

<p align="left">
  <img src="img/comando_gioca.png" alt="comando_gioca" width="400">
</p>

A questo punto l'utente bianco inizierà il gioco con la sua mossa.

#### Comando /scacchiera
Per visualizzare la scacchiera, l'utente potrà immetterà il comando "/scacchiera" e premere invio. Se tale comando viene digitato prima dell'inizio della partita, allora verrà mostrato un messaggio d'errore che indicherà che la partita non è ancora iniziata e inviterà l'utente a inserire comando "/gioca".

<p align="left">
  <img src="img/comando_scacchiera.png" alt="comando_scacciera" width="400">
</p>

#### Comando /mosse
Per visualizzare tutte le mosse effettuate da entrambi i giocatori, l'utente deve digitare il comando "/mosse" e premere invio. Verrà mostrato l'elenco delle mosse (in notazione algebrica) del giocatore bianco (indicato con un pallino bianco) e del nero (indicato con un pallino nero).

<p align="left">
  <img src="img/comando_mosse.png" alt="comando_mosse" width="400">
</p>

#### Comando /abbandona
Per abbandonare la partita in corso, l'utente deve digitare il comando "/abbandona" e premere invio.  Verrà poi richiesta un'ulteriore conferma a cui l'utente può rispondere:
* 's' confermando di abbandonare la partita facendo così vincere il 2^ giocatore per abbandono
* 'n' rimanendo in partita

Qualora questo comando venisse inserito quando non si è in partita, verrà mostrato un messaggio d'errore.

<p align="left">
  <img src="img/comando_abbandona.png" alt="comando_abbandona" width="400">
</p>

#### Comando /patta
Per chiedere la patta l'utente dovrà inserire il comando "/patta" e premere invio, ma solo qualora avesse già effettuato una mossa. Viene poi stampato un messaggio di accettazione della patta all'altro giocatore e alla risposta positiva ('s') di quest'ultimo viene terminanata la partita in pareggio. Se il comando "/patta" viene invocato quando non si è in gioco, viene stampato un relativo messaggio d'errore.

<p align="left">
  <img src="img/comando_patta.png" alt="comando_patta" width="400">
</p>

#### Comando /esci
Al fine di chiudere l'applicazione (sia in gioco che non), l'utente dovrà digitare il comando "/esci" e verrà chiesta conferma a cui l'utente potrà rispondere:
* "s" se vuole confermare la chiusura del gioco
* "n" se vuole annullare l'uscita e ritornare all'applicazione potendo inserire un comando o una mossa (se in gioco)

<p align="left">
  <img src="img/comando_esci.png" alt="comando_esci" width="400">
</p

### Mosse dei pezzi
Ciascun pezzo può muoversi secondo le regole del gioco degli scacchi, che l'utente specificherà in notazione algebrica. Qualora la mossa digitata fosse errata o non disponibile per quel pezzo verrà mostrato un messaggio d'errore.

##### ♙: Pedone 
Il pedone avanza di una sola casella, solamente se la casella di destinazione è libera. Solamente se è la sua prima mossa, può avanzare di 2 caselle. Il pedone cattura solo nelle due celle diagonali di fronte a sè, muovendosi  di una casella. Il pedone non può catturare all'indietro o lateralmente.

<p align="left">
  <img src="img/pedone.jpeg" alt="pedone" width="400">
</p

Per avanzare un pedone, l'utente inserirà una mossa in formato: 
`colonna-riga`
(il trattino non va inserito) dove la colonna è una lettera minuscola compresa tra 'a' ed 'h' e la riga è un numero compreso tra 1 e 8.
es.: b3, f2

Per catturare un pezzo col pedone, l'utente inserirà una mosse in formato:
`colonna1-'x'-colonna2-riga2`
dove la prima colonna (lettera compresa tra 'a' e 'h') è quella di partenza, la seconda è quella di destinazione del pezzo da catturare; invece la riga è quella di destinazione. Il carattere 'x' è un carattere separatore.
es. cxd5, exf3

##### ♖: Torre
La torre si muove in linea retta in verticale o in orizzontale, per un numero qualsiasi di caselle.
Non può saltare sopra altri pezzi: il suo percorso deve essere libero.
Può catturare un pezzo avversario occupando la sua casella.

<p align="left">
  <img src="img/Torre.png" alt="torre" width="400">
</p

Per avanzare una torre, l'utente inserirà una mossa in formato:
`T-colonna-riga` 
(il trattino non va inserito) dove la T indica la torre nella notazione italiana degli scacchi, colonna è una lettera minuscola compresa tra 'a' ed 'h' e la riga è un numero compreso tra 1 e 8. In caso di ambiguità (piu' pezzi che si possono muovere verso tale casella) si deve inserire la mossa in formato completo:
`T-colonna1-riga1-colonna2-riga2`
dove colonna1 e riga1 sono le coordinate di partenza e colonna2 e riga2 quelle di arrivo
es.: Tb3, Tf2, Te4e6

Per catturare un pezzo con la torre, l'utente inserirà una mosse in formato:
`T-'x'-colonna-riga`
,dove colonna e riga sono le coordinate della casella di arrivo. In caso di ambiguità serve sempre il formato completo:
`T-colonna1-riga1-'x'-colonna2-riga2`
es: Txd4

##### ♘: Cavallo
Il cavallo si muove a "L": due caselle in una direzione (orizzontale o verticale) e poi una casella perpendicolare.
È l’unico pezzo che può saltare sopra altri pezzi, siano essi propri o avversari.

<p align="left">
  <img src="img/Cavallo.png" alt="cavallo" width="400">
</p

Per avanzare un cavallo, l'utente inserirà una mossa in formato:
`C-colonna-riga` 
(il trattino non va inserito) dove la C indica il cavallo nella notazione italiana degli scacchi, colonna è una lettera minuscola compresa tra 'a' ed 'h' e la riga è un numero compreso tra 1 e 8. In caso di ambiguità (piu' pezzi che si possono muovere verso tale casella) si deve inserire la mossa in formato completo:
`C-colonna1-riga1-colonna2-riga2`
dove colonna1 e riga1 sono le coordinate di partenza e colonna2 e riga2 quelle di arrivo
es.: Cf3, Cc6, Ce4g4

Per catturare un pezzo con il cavallo, l'utente inserirà una mosse in formato:
`C-'x'-colonna-riga`
,dove colonna e riga sono le coordinate della casella di arrivo. In caso di ambiguità serve sempre il formato completo:
`C-colonna1-riga1-'x'-colonna2-riga2`
es: Cxe5

##### ♗: Alfiere
L'alfiere si muove diagonale per un numero qualsiasi di caselle.
Come la torre, non può saltare sopra altri pezzi e il percorso deve essere libero.

<p align="left">
  <img src="img/Alfiere.png" alt="alfiere" width="400">
</p

Per avanzare un alfiere, l'utente inserirà una mossa in formato:
`A-colonna-riga` 
(il trattino non va inserito) dove la A indica l'alfiere nella notazione italiana degli scacchi, colonna è una lettera minuscola compresa tra 'a' ed 'h' e la riga è un numero compreso tra 1 e 8. In caso di ambiguità (piu' pezzi che si possono muovere verso tale casella) si deve inserire la mossa in formato completo:
`A-colonna1-riga1-colonna2-riga2`
dove colonna1 e riga1 sono le coordinate di partenza e colonna2 e riga2 quelle di arrivo
es.: Ac1, Af4, Ae4g6

Per catturare un pezzo con l'alfiere, l'utente inserirà una mosse in formato:
`A-'x'-colonna-riga`
,dove colonna e riga sono le coordinate della casella di arrivo. In caso di ambiguità serve sempre il formato completo:
`A-colonna1-riga1-'x'-colonna2-riga2`
es: Axc3, Axe6

##### ♕: Donna (Regina)
La donna è il pezzo più potente: può muoversi in qualsiasi direzione (verticale, orizzontale, diagonale), per qualsiasi numero di caselle, fintanto che il percorso è libero.
Non può saltare sopra altri pezzi.

<p align="left">
  <img src="img/Regina.png" alt="regina" width="400">
</p

Per avanzare una donna, l'utente inserirà una mossa in formato:
`D-colonna-riga` 
(il trattino non va inserito) dove la D indica la donna (regina) nella notazione italiana degli scacchi, colonna è una lettera minuscola compresa tra 'a' ed 'h' e la riga è un numero compreso tra 1 e 8. In caso di ambiguità (piu' pezzi che si possono muovere verso tale casella) si deve inserire la mossa in formato completo:
`D-colonna1-riga1-colonna2-riga2`
dove colonna1 e riga1 sono le coordinate di partenza e colonna2 e riga2 quelle di arrivo
es.: Dd1, De4h4

Per catturare un pezzo con la donna, l'utente inserirà una mosse in formato:
`D-'x'-colonna-riga`
,dove colonna e riga sono le coordinate della casella di arrivo. In caso di ambiguità serve sempre il formato completo:
`D-colonna1-riga1-'x'-colonna2-riga2`
es: Dxh7

##### ♔: Re
Il re si muove di una sola casella alla volta, in qualsiasi direzione: verticale, orizzontale o diagonale. Non può muoversi in una casella sotto attacco avversario. Il re è coinvolto anche in una mossa speciale: l’arrocco.

<p align="left">
  <img src="img/Re.png" alt="re" width="400">
</p

Per avanzare un re, l'utente inserirà una mossa in formato:
`R-colonna-riga` 
(il trattino non va inserito) dove la R indica il re nella notazione italiana degli scacchi, colonna è una lettera minuscola compresa tra 'a' ed 'h' e la riga è un numero compreso tra 1 e 8. In caso di ambiguità (piu' pezzi che si possono muovere verso tale casella) si deve inserire la mossa in formato completo:
`R-colonna1-riga1-colonna2-riga2`
dove colonna1 e riga1 sono le coordinate di partenza e colonna2 e riga2 quelle di arrivo
es.: Re1, Rf2

Il re può catturare un pezzo solo se la casella di destinazione non è sotto attacco e non può mettersi, né restare in scacco. Per catturare un pezzo con il re, l'utente inserirà una mosse in formato:
`R-'x'-colonna-riga`
,dove colonna e riga sono le coordinate della casella di arrivo. In caso di ambiguità serve sempre il formato completo:
`R-colonna1-riga1-'x'-colonna2-riga2`
es: Rxf7, Rxd1

---

### Regole Speciali
- **Arrocco**: mossa speciale tra re e torre. Serve a mettere in sicurezza il Re e allo stesso tempo sviluppare la Torre. Il re si sposta di 2 caselle verso una Torre e la Torre "salta" il Re per posizionarsi accanto a lui. Esistono due tipi di arrocco:
    1. Arrocco corto (0-0): il Re si sposta verso la Torre sul lato re (colonna “h”).
    2. Arrocco lungo (0-0-0): il Re si sposta verso la Torre sul lato donna (colonna “a”).
* Le condizioni per l'arrocco sono:
    1. Né il Re né la Torre coinvolta si sono mossi prima.
    2. Non ci sono pezzi tra il Re e la Torre.
    3.  Il Re non è sotto scacco, né passa o finisce su una casella attaccata.
    

- **En passant**: cattura speciale del pedone. Si verifica quando un pedone avversario avanza di due caselle dalla sua posizione iniziale, passando “vicino” al tuo pedone. Il tuo pedone può catturarlo “di passaggio” muovendosi diagonalmente nella casella che il pedone avversario ha “saltato”. La cattura en passant può essere fatta solo immediatamente nel turno successivo all’avanzata di due caselle dell’avversario: se non viene eseguita subito, se ne perde l'opportunità

- **Promozione**: un pedone che raggiunge l’ultima riga (la riga più lontana dalla sua posizione iniziale) può essere promosso, ossia sostituito con un altro pezzo (di solito la donna perché ha la massima mobilità ma può essere anche una torre, alfiere o cavallo). La promozione è obbligatoria: non si può lasciare il pedone sulla riga finale senza promuoverlo. 
Per la promozione di un pedone bisogna specificare un comando nel formato:
`riga-colonna-"Lettera del pezzo"`
, dove riga e colonna solo le coordinate della cella di arrivo e la lettera del pezzo indica in quale lettera lo si vuole promuovere (D,T,A,C)
es. a8D, f1T

---
### Termine della partita

- **Stallo**: il giocatore che deve muovere non è sotto scacco ma non ha mosse legali disponibili. La partita termina immediatamente in patta (pareggio).
es. 
`Re bianco: h1   Donna bianca: g7`
`Re nero: h8`
Il Nero non è in scacco, ma le uniche case in cui potrebbe muovere il Re sono controllate; nessun altro pezzo può muovere → stallo.

<p align="left">
  <img src="img/stallo.png" alt="stallo" width="400">
</p

- **Scacco**: Il Re del giocatore al tratto è minacciato di cattura alla prossima mossa. Il giocatore deve parare lo scacco in uno dei tre modi:
 1. Spostare il Re su una casa sicura;
 2. Catturare il pezzo che dà scacco;
 3. Interporre un pezzo fra l’attaccante e il Re (se lo scacco non è di cavallo). 
 Nel gioco lo scacco ha una notazione normale ma nel registro mosse viene riportato un '+' alla fine come nella notazione algebrica italiana.

<p align="left">
  <img src="img/scacco.png" alt="scacco" width="400">
</p

- **Scacco matto**: vittoria di un giocatore  
  Quando il re avversario è sotto attacco (scacco) e non può sfuggire a nessuna mossa legale. La partita finisce immediatamente e vince chi ha dato scacco matto
 Nel gioco lo scacco ha una notazione normale ma nel registro mosse viene riportato un '#' alla fine come nella notazione algebrica italiana.
 es. Axf7#
<p align="left">
  <img src="img/scacco_matto.jpg" alt="scacco_matto" width="400">
</p





# ♟️ Scacchi Codd - Python CLI Chess Engine

[![Continuous Integration and Continuous Delivery (CI/CD)](https://github.com/softeng2425-inf-uniba/project2-codd/actions/workflows/CI-CD.yml/badge.svg)](https://github.com/softeng2425-inf-uniba/project2-codd/actions/workflows/CI-CD.yml)

Un simulatore completo del gioco degli scacchi per due giocatori da riga di comando (CLI), sviluppato in **Python 3.11**. 

Questo progetto è stato realizzato con l'obiettivo di applicare rigorosamente i principi dell'**Ingegneria del Software**. Il focus principale non è solo sulle meccaniche di gioco, ma sulla creazione di una base di codice scalabile, manutenibile e fortemente modulare, facendo un uso estensivo di architetture standard, Design Pattern e pratiche di Continuous Integration.

---

## 🚀 Tecnologie e Strumenti

* **Linguaggio:** Python 3.11.9
* **Architettura:** Entity-Control-Boundary (ECB), Architettura Layered
* **Testing:** Pytest (Suite di 31 unit test a copertura delle logiche di dominio)
* **DevOps & Qualità:** Docker, GitHub Actions (CI/CD), Ruff (Linting)

---

## 🏗️ Architettura e Ingegneria del Codice

Il motore di gioco è progettato per garantire alta coesione e basso accoppiamento, rispettando i **Principi SOLID** e incapsulando la logica di dominio (regole di validazione, controllo scacco/matto) lontano dalla logica di presentazione (interfaccia terminale).

### Design Pattern Implementati
* **Strategy:** Utilizzato per incapsulare le logiche di ricerca e le strategie di parsing in base alla tipologia di pezzo mosso.
* **Factory Method:** Gestisce la generazione dinamica delle istanze dei pezzi sulla scacchiera, astraendo la logica di creazione.
* **Interpreter:** Cuore del modulo Parser, fondamentale per tradurre la notazione algebrica standard (es. `e4`, `Cxf3`) in coordinate logiche processabili dalla matrice della scacchiera.
* **Command:** Gestisce l'interazione da riga di comando, isolando ogni azione dell'utente in comandi eseguibili autonomamente.
* **Template Method:** Definisce lo scheletro dell'algoritmo di calcolo delle mosse valide nella classe base `Pezzo`, delegando alle sottoclassi (`Torre`, `Cavallo`, ecc.) i comportamenti specifici.
* **Singleton:** Garantisce un punto di accesso globale e univoco per la gestione centralizzata delle eccezioni e del logging degli errori.
* **Facade:** Semplifica le interazioni tra i livelli, fornendo un'interfaccia unificata verso il controller principale del gioco.

---

## 🎮 Funzionalità del Motore

Il sistema gestisce una partita regolamentare completa, implementando tutte le dinamiche del gioco:
* **Meccaniche FIDE:** Calcolo dello scacco, scacco matto e condizioni di stallo.
* **Mosse Speciali:** Pieno supporto per **Arrocco** (corto `0-0` e lungo `0-0-0`), **Cattura En Passant** e **Promozione** del pedone (es. `a8D`).
* **Notazione Algebrica:** Le mosse vengono inserite e storicizzate seguendo lo standard scacchistico internazionale.

---

## 🛠️ Come avviare il progetto

Per garantire la massima compatibilità e isolare l'ambiente di esecuzione (in particolare per la corretta renderizzazione dei caratteri Unicode UTF-8 su tutti i terminali), si raccomanda l'esecuzione tramite **Docker**.

### Opzione 1: Esecuzione con Docker (Raccomandata)
1. Clona la repository:
   ```bash
   git clone https://github.com/softeng2425-inf-uniba/project2-codd.git
   cd project2-codd
   ```

2. Costruisci l'immagine Docker:
   ```bash
   docker build -t scacchi-cli .
   ```

3. Avvia il container in modalità interattiva:
   ```bash
   docker run -it scacchi-cli
   ```

### Opzione 2: Esecuzione Locale (Python)

Assicurati di avere Python 3.11+ installato e un terminale configurato in UTF-8.

1. Clona la repository ed entra nella cartella del progetto:
   ```bash
   git clone https://github.com/softeng2425-inf-uniba/project2-codd.git
   cd project2-codd
   ```

2. (Raccomandato) Crea e attiva un ambiente virtuale:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Su macOS/Linux
   # Oppure su Windows: venv\Scripts\activate
   ```

3. Installa le dipendenze richieste:
   ```bash
   pip install -r requirements.txt
   ```

4. Avvia il gioco come modulo:
   ```bash
   python -m scacchi
   ```


---

## ⌨️ Manuale dei Comandi

L'interazione avviene tramite comandi testuali diretti.

* `/help` - Mostra l'elenco completo dei comandi disponibili.
* `/gioca` - Inizializza la scacchiera e avvia una nuova partita.
* `/scacchiera` - Stampa la disposizione attuale dei pezzi.
* `/mosse` - Mostra il registro completo delle mosse giocate (in notazione algebrica).
* `/patta` - Invia una proposta di pareggio all'avversario.
* `/abbandona` - Concede la vittoria all'avversario.
* `/esci` - Termina l'esecuzione del programma.
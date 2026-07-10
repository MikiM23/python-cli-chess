from rich import print

from scacchi.Applicazione import Applicazione


class UI:
    """Defines the configuration of the game's UI."""

    def __init__(self):
        """Initialize the game's UI with default settings."""
        self._ACCENT_COLOR: str = "red"

    def set_accent_color(self, accent_color: str):
        """Set the accent color for the game's UI.

        List of valid colors supported by the Rich library:
            - `black`
            - `red`
            - `green`
            - `yellow`
            - `blue`
            - `magenta`
            - `cyan`
            - `white`
            - `bright_black`
            - `bright_red`
            - `bright_green`
            - `bright_yellow`
            - `bright_blue`
            - `bright_magenta`
            - `bright_cyan`
            - `bright_white`

        Args:
            accent_color (str): the accent color to be used in the game's UI

        Raises:
            ValueError: if the accent color is not supported by the Rich library

        """
        RICH_COLORS: set[str] = {
            "black",
            "red",
            "green",
            "yellow",
            "blue",
            "magenta",
            "cyan",
            "white",
            "bright_black",
            "bright_red",
            "bright_green",
            "bright_yellow",
            "bright_blue",
            "bright_magenta",
            "bright_cyan",
            "bright_white",
        }

        # If the user provides an accent color, then use it
        if accent_color in RICH_COLORS:
            self._ACCENT_COLOR = accent_color
        else:
            raise ValueError(
                f"Invalid accent color '{self._ACCENT_COLOR}'. "
                "Please choose a color supported by the Rich library."
            )

    def get_accent_color(self) -> str:
        """Get the accent color for the game's UI.

        Returns:
            accent color

        """
        return self._ACCENT_COLOR


def main(): 
    """Run the Scacchi game and activate the GH workflows."""
    ui = UI()
    ui.set_accent_color("blue")

    app = Applicazione()

    # ASCII Art 
    accent = ui.get_accent_color()
    title_art = f"""
    [bold {accent}]
    ███████╗  ██████╗   █████╗   ██████╗  ██████╗  ██╗  ██╗   ██╗
    ██╔════╝ ██╔════╝  ██╔══██╗ ██╔════╝ ██╔════╝  ██║  ██║   ██║
    ███████╗ ██║       ███████║ ██║      ██║       ███████║   ██║
    ╚════██║ ██║       ██╔══██║ ██║      ██║       ██╔══██║   ██║
    ██████╔╝ ╚██████╗  ██║  ██║ ╚██████╗ ╚██████╗  ██║  ██║   ██║
    ╚═════╝   ╚═════╝  ╚═╝  ╚═╝  ╚═════╝  ╚═════╝  ╚═╝  ╚═╝   ╚═╝
    [/bold {accent}]  
       [white]♔ ♕ ♖ ♗ ♘ ♙[/white]   Pensa prima, muovi dopo!\
    [gray]♚ ♛ ♜ ♝ ♞ ♟[/gray]

    [bold green]                  ♔ Menu Principale ♔   [/bold green]
    [white]     ╔═════════════════════════════════════════╗[/white]
    [white]     ║1.[/white][pink]/gioca[/pink] -Inizia una nuova partita   \
    [white]║[/white]
    [white]     ║2.[/white][pink]/help[/pink]  -Mostra comandi disponibili \
    [white]║[/white]
    [white]     ║3.[/white][pink]/esci[/pink]  -Esci dal gioco             \
    [white]║[/white]
    [white]     ╚═════════════════════════════════════════╝[/white]

    """
    print(title_art)

    # Gestione degli argomenti di avvio. In caso di argomento errato chiusura con errore
    app.gestioneArgomentiAvvio() 

    print("Benvenuto in Scacchi! Scegli un comando tra quelli disponibili")

    app.avvia()


if __name__ == "__main__":
    main()

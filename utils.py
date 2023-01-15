import os

def netejar_pantalla() -> None:
    """Neteja la pantalla."""
    os.system("cls") if os.name == "nt" else os.system("clear")

def continuar() -> None:
    """Atura el programa per que l'usuari tingui en compte certa cosa."""
    input("Prem ENTER per continuar.")
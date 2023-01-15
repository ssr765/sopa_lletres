import os
import random
from typing import List, Tuple

from colorama import Fore, Back, Style

from utils import netejar_pantalla


class lletra:
    """A partir d'aquesta crearem totes les caselles del tauler de la sopa de
    lletres i contindrá totes les característiques demanades i algunes més que
    he pensat que serán utils facilitant la cerca de paraules.
    
    He fet una classe en comptes de utilitzar diccionaris perque és una opció
    molt més clara a l'hora de treballar amb les caselles."""
    def __init__(self) -> None:
        self.caracter = "-"
        self.trobat = False
        self.posicio = (-1, -1)
        self.orientacio = None
        self.direccio = None
        self.paraula = None
        self.longitud = 0
    
    def format_caracter(self) -> None:
        """Métode que mostra el caràcter de color verd en cas que s'hagi trobat
        la paraula d'aquest o el mostra normalment en cas que no s'hagi trobat.
        """
        formatat = (Fore.GREEN if self.trobat else "") + self.caracter + (Fore.RESET if self.trobat else "")
        print(formatat.rjust(len(formatat) + 1), end=" ")


# Alias de tipus per fer el codi més clar.
# Com que al codi una llista que conté llistes que contenen instancies de lletra
# sempre será una sopa de lletres fem un alias per referirnos a aquest tipus
# d'estructura.
MatriuSopa = List[List[lletra]]


def seleccio_idioma() -> str:
    """Valida i retorna la selecció de l'idioma."""
    opcio_valida = False
    while not opcio_valida:
        idiomes = [x.capitalize() for x in os.listdir(DIRECTORI_PARAULES)]
        print("Idiomes disponibles:")
        print("  " + ", ".join(idiomes) + "\n")
        opcio = input("Selecciona un idioma: ").capitalize()
        opcio_valida = opcio in idiomes
    
    return opcio

def seleccio_tematica(idioma: str) -> str:
    """Valida i retorna la selecció de la temàtica de les paraules."""
    opcio_valida = False
    while not opcio_valida:
        tematiques = [x[:-4].capitalize() for x in os.listdir(DIRECTORI_PARAULES + idioma)]
        print("Temàtiques disponibles:")
        print("  " + ", ".join(tematiques) + "\n")
        opcio = input("Selecciona una temàtica: ").capitalize()
        opcio_valida = opcio in tematiques
    
    return opcio

def configuracio() -> Tuple[int, int]:
    """Demana i retorna el nombre de paraules i la mida, si no"""
    # Nombre de paraules.
    try:
        num_paraules = int(input("Introdueix el nombre de paraules amb el que vols jugar (10 - 20): "))
        assert num_paraules in range(10, 21)

    except:
        num_paraules = 10
        print(f"Opció no valida, es jugarà amb el valor per defecte: {num_paraules}")

    # Mida del tauler.
    try:
        mida = int(input(f"Introdueix la mida del tauler ({num_paraules + 2} - {num_paraules + 12}): "))
        assert mida in range(num_paraules + 2, num_paraules + 13)

    except:
        mida = num_paraules + 6
        print(f"Opció no valida, es jugarà amb el valor per defecte: {mida}")

    return num_paraules, mida

def escull_paraules(fitxer: str, idioma: str, mida: int, num_paraules: int) -> List[str]:
    """Retorna una llista amb la quantitat especificada de paraules."""
    # Obre el fitxer mitjançant context manager i agafa les paraules del fitxer.
    with open(DIRECTORI_PARAULES + idioma + "/" + fitxer, "r", encoding="UTF-8") as f:
        paraules = [paraula.upper() for paraula in f.read().split("\n")]

    # Filtrem les paraules amb la funció filter, que mitjançant una funció
    # lambda evalua si les paraules no sobrepassen la mida.
    paraules = list(filter(lambda paraula: len(paraula) <= mida, paraules))

    # Barreja les paraules per després retonar les num_paraules primeres.
    random.shuffle(paraules)
    
    return paraules[:num_paraules]

def pos(mida: int) -> Tuple[int, int]:
    """Retorna una tuple amb les cordenades aleatories."""
    return random.randint(0, mida - 1), random.randint(0, mida - 1)

def crea_matriu(mida: int) -> MatriuSopa:
    """Crea i retorna una matriu de mida x mida ficant una instancia de lletra
    a cada fila de la matriu."""
    return [[lletra() for _ in range(mida)] for _ in range(mida)]

def print_sopa(sopa: MatriuSopa, mida: int, tematica: str, idioma: str, palabras_restantes: int) -> None:
    """Funció que mostra la sopa per pantalla."""
    # Capçalera de la sopa.
    if not DEV:
        print(Back.WHITE, Fore.BLACK + "Sopa de lletres".center(3 * mida + 1) + Style.RESET_ALL)
    
    else:
        print(Back.WHITE, Fore.BLACK + "Sopa de lletres - DESENVOLUPAMENT".center(3 * mida + 1) + Style.RESET_ALL)

    print(Back.WHITE, Fore.BLACK + "#" * (3 * mida) + " " + Style.RESET_ALL)
    print(Back.WHITE, Fore.BLACK + f"Temàtica: {tematica} - {idioma}".ljust(3 * mida + 1) + Style.RESET_ALL)
    print(Back.WHITE, Fore.BLACK + f"Paraules restants: {palabras_restantes}".ljust(3 * mida + 1) + Style.RESET_ALL)
    print(Back.WHITE + Fore.BLACK + "   " + " ".join([str(x).rjust(2) for x in range(len(sopa))]) + Style.RESET_ALL)
    # Per cada fila, mostra cada lletra d'aquesta amb el número de la fila al
    # davant.
    for i, fila in enumerate(sopa):
        print(Back.WHITE + Fore.BLACK + str(i).rjust(2) + Style.RESET_ALL +  " ", end="")
        for lletra in fila:
            lletra.format_caracter()
        print()

def hi_cap(mida: int, x: int, y: int, llargada_paraula: int, orientacio: str, direccio: str) -> bool:
    """Comprova si una paraula hi cap tenint en compte la orientació i direcció.
    Retorna un bolean."""
    # Horitzontal.
    if orientacio == "-":
        # Y + la llargada de la paraula no pot superar la mida.
        if direccio == "+" and y + llargada_paraula > mida:
            return False
        
        # Y - la llargada de la paraula no pot ser més petit que 0.
        elif direccio == "-" and y - llargada_paraula < 0:
            return False
    
    # Vertical.
    elif orientacio == "|":
        # X + la llargada de la paraula no pot superar la mida.
        if direccio == "+" and x + llargada_paraula > mida:
            return False
        
        # X - la llargada de la paraula no pot ser més petit que 0.
        elif direccio == "-" and x - llargada_paraula < 0:
            return False
    
    # Diagonal.
    elif orientacio == "/":
        # X - la llargada de la paraula no pot ser més petit que 0.
        # Y + la llargada de la paraula no pot superar la mida.
        if direccio == "+" and (x - llargada_paraula < 0 or y + llargada_paraula > mida):
            return False
        
        # Y - la llargada de la paraula no pot ser més petit que 0.
        # X + la llargada de la paraula no pot superar la mida.
        elif direccio == "-" and (y - llargada_paraula < 0 or x + llargada_paraula > mida):
            return False
    
    # Diagonal inversa.
    elif orientacio == "\\":
        # Y + la llargada de la paraula no pot superar la mida.
        # X + la llargada de la paraula no pot superar la mida.
        if direccio == "+" and (x + llargada_paraula > mida or y + llargada_paraula > mida):
            return False

        # Y - la llargada de la paraula no pot ser més petit que 0.
        # X - la llargada de la paraula no pot ser més petit que 0.
        elif direccio == "-" and (y - llargada_paraula < 0 or x - llargada_paraula < 0):
            return False

    return True

def colocar_paraules(mida, sopa, paraules) -> None:
    """Col·loca les paraules a la sopa aleatoriament. Fa les comprovacions
    necessaries perque hi capiga la paraula i no es superposi amb cap altre
    paraula."""
    # Ordena la llista segons la longitud d'aquestes descendentment.
    paraules.sort(key=len, reverse=True)

    # Per cada paraula comprovará si cap en el tauler i si no hi han lletres
    # ocupades pel mig.
    for p in paraules:
        posicio_valida = False
        while not posicio_valida:
            # Característiques aleatories.
            x, y = pos(mida)
            orientacio = random.choice(ORIENTACIONS)
            direccio = random.choice(DIRECCIONS)

            # Comprovar que hi cap.
            posicio_valida = hi_cap(mida, x, y, len(p), orientacio, direccio)

            # Per cada lletra comprova si la casella NO está ocupada, si troba
            # alguna que si ho está no seguirá comprovant les demés lletres
            # i tornará a provar una altre combinació.
            for i in range(len(p)):

                # En cas que la direcció sigui reversa, ficarà el valor de i en
                # negatiu per fer la direcció contraria.
                i *= DIRECCIONS_NUMS[direccio]

                if posicio_valida:
                    if orientacio == "-":
                        posicio_valida = not ocupada(sopa[x][y + i])

                    elif orientacio == "|":
                        posicio_valida = not ocupada(sopa[x + i][y])

                    elif orientacio == "/":
                        posicio_valida = not ocupada(sopa[x - i][y + i])

                    elif orientacio == "\\":
                        posicio_valida = not ocupada(sopa[x + i][y + i])
        
        # Un cop hagi trobat una posició valida, ficarà les lletres a cada lloc.
        for i, ll in enumerate(p):

            # Tornem a ficar i en negatiu en cas que la direcció sigui reversa.
            i *= DIRECCIONS_NUMS[direccio]

            if orientacio == "-":
                colocar_lletra(sopa, ll, x, y + i, (x, y), orientacio, direccio, p)

            elif orientacio == "|":
                colocar_lletra(sopa, ll, x + i, y, (x, y), orientacio, direccio, p)

            elif orientacio == "/":
                colocar_lletra(sopa, ll, x - i, y + i, (x, y), orientacio, direccio, p)

            elif orientacio == "\\":
                colocar_lletra(sopa, ll, x + i, y + i, (x, y), orientacio, direccio, p)


def ocupada(casella: lletra) -> bool:
    """Comprova si una casella está ocupada. Retorna False si no ho esta i True
    si ho está."""
    if casella.caracter not in LLETRES:
        return False

    return True

def colocar_lletra(sopa: MatriuSopa, ll: str, x: int, y: int, index: Tuple[int, int], orientacio: str, direccio: str, paraula: str) -> None:
    """Cambia els atributs de la instancia de lletra."""
    sopa[x][y].posicio = index
    sopa[x][y].caracter = ll
    sopa[x][y].orientacio = orientacio
    sopa[x][y].direccio = direccio
    sopa[x][y].paraula = paraula
    sopa[x][y].longitud = len(paraula)

def omple_lletres(sopa: MatriuSopa) -> None:
    """Cambia el caràcter de les caselles buides amb una lletra aleatoria."""
    for fila in sopa:
        for casella in fila:
            if casella.caracter == "-":
                casella.caracter = random.choice(LLETRES)

def intent(mida: int, paraules: List[str]) -> Tuple[int, int, str, str, str]:
    """Demana i retorna els valors necessaris per intentar trobar una paraula.
    """
    # Coordenada Y.
    valor_valid = False
    while not valor_valid:
        try:
            coor_y = int(input(f"Introdueix la coordenada Y de la primera lletra de la paraula trobada (0 - {mida}): "))
        
        except ValueError:
            valor_valid = False
        
        else:
            valor_valid = coor_y in range(mida)

    # Coordenada X.
    valor_valid = False
    while not valor_valid:
        try:
            coor_x = int(input(f"Introdueix la coordenada X de la primera lletra de la paraula trobada (0 - {mida}): "))
        
        except ValueError:
            valor_valid = False
        
        else:
            valor_valid = coor_x in range(mida)

    # Orientació.
    valor_valid = False
    while not valor_valid:
        orientacio = input(f"Introdueix l'orientació de la paraula trobada ({', '.join(ORIENTACIONS)}): ")
        valor_valid = orientacio in ORIENTACIONS
    
    # Direcció.
    valor_valid = False
    while not valor_valid:
        direccio = input("Introdueix la direcció de la paraula trobada (+ per direcció normal, - per direcció reversa): ")
        valor_valid = direccio in DIRECCIONS

    # Paraula.
    valor_valid = False
    while not valor_valid:
        paraula = input("Introdueix la paraula trobada: ").upper()
        valor_valid = paraula in paraules
    
    return coor_x, coor_y, orientacio, direccio, paraula

def comprovar_intent(sopa: MatriuSopa, coor_x: int, coor_y: int, orientacio: str, direccio: str, paraula: str) -> bool:
    """Comprova si les característiques de l'intent coincideixen amb les
    característiques de la paraula a la sopa. Retorna True si té èxit la
    comparació."""
    # Localítza la casella.
    casella_escollida = sopa[coor_x][coor_y]

    # Fa les comparacions.
    if casella_escollida.posicio != (coor_x, coor_y):
        return False
    
    if casella_escollida.orientacio != orientacio:
        return False
    
    if casella_escollida.direccio != direccio:
        return False
    
    if casella_escollida.paraula != paraula:
        return False
    
    return True

def marcar_paraula(sopa: MatriuSopa, coor_x: int, coor_y: int, orientacio: str, direccio: str, paraula: str) -> None:
    """Cambia l'atribut trobat a True de cada instancia de la classe lletra de
    cada lletra de la paraula a la sopa"""
    for i in range(len(paraula)):
        i *= DIRECCIONS_NUMS[direccio]
        if orientacio == "-":
            sopa[coor_x][coor_y + i].trobat = True

        elif orientacio == "|":
            sopa[coor_x + i][coor_y].trobat = True

        elif orientacio == "/":
            sopa[coor_x - i][coor_y + i].trobat = True

        elif orientacio == "\\":
            sopa[coor_x + i][coor_y + i].trobat = True

def comprovar_terminal(mida: int) -> None:
    """Comprova l'alçada i l'amplada de la terminal i dona un avís en cas que  alguna 
    sigui massa petita."""

    netejar_pantalla()
    # Comprovar alçada (mínim 15 línies de les dades del joc + mida del tauler).
    if os.get_terminal_size().lines < mida + 15:
        print(Fore.YELLOW + "L'alçada de la teva terminal es massa petita per veure el joc correctament." + Fore.RESET)
        print(f"És recomenable que l'ampliïs {mida + 15 - os.get_terminal_size().lines} línies.")
        input("Prem ENTER per continuar.")

    netejar_pantalla()
    # Comprovar amplada (mínim 82 el missatge més llarg amb el input més llarg
    # posible).
    if os.get_terminal_size().columns < 82:
        print(Fore.YELLOW + "L'amplada de la teva terminal es massa petita per veure el joc correctament." + Fore.RESET)
        print(f"És recomenable que l'ampliïs {82 - os.get_terminal_size().lines} línies.")
        input("Prem ENTER per continuar.")

def main() -> None:
    """Funció principal del programa."""
    # Configuració del joc.
    idioma = seleccio_idioma()
    netejar_pantalla()
    tematica = seleccio_tematica(idioma)
    netejar_pantalla()
    print(f"Idioma: {idioma}")
    print(f"Temàtica: {tematica}")
    num_paraules, mida = configuracio()

    # Crear la matriu, la llista de paraules i colocar aquestes.
    sopa = crea_matriu(mida)
    paraules = escull_paraules(tematica + ".txt", idioma, mida, num_paraules)
    colocar_paraules(mida, sopa, paraules)

    comprovar_terminal(mida)

    # Oplenar el tauler amb lletres aleatories en cas que no estigui activat el 
    # mode de desenvolupament.
    if not DEV:
        omple_lletres(sopa)

    joc = True
    paraula_trobada = None
    incorrecte = False
    # Bucle del joc, el joc acaba quan no hi queden paraules a la llista.
    while joc:
        netejar_pantalla()
        # Informació de la partida.
        print_sopa(sopa, mida, tematica, idioma, len(paraules))
        print(f"\nEncara has de trobar les següents paraules:\n  {', '.join(paraules)}\n")

        # Informa de la anterior paraula trobada.
        if paraula_trobada != None:
            print(Fore.GREEN + f"Has trobat la paraula {paraula_trobada}!" + Fore.RESET)
            paraula_trobada = None

        # Informa de l'anterior intent sense éxit.
        if incorrecte:
            print(Fore.RED + "T'has equivocat." + Fore.RESET)
            incorrecte = False

        # Intent i comprovació d'aquest.
        coor_x, coor_y, orientacio, direccio, paraula = intent(mida, paraules)
        if comprovar_intent(sopa, coor_x, coor_y, orientacio, direccio, paraula):
            # Marca la paraula, la guarda per informar-ho després de netejar la
            # pantalla i treu la paraula de la llista.
            marcar_paraula(sopa, coor_x, coor_y, orientacio, direccio, paraula)
            paraula_trobada = paraula
            paraules.remove(paraula)
            joc = len(paraules) != 0

        else:
            incorrecte = True

    netejar_pantalla()
    print_sopa(sopa, mida, tematica, idioma, len(paraules))
    print(Back.WHITE, Fore.BLACK + "Has trobat totes les paraules!!!".center(3 * mida + 1) + Style.RESET_ALL)


LLETRES = "QWERTYUIOPASDFGHJKLZXCVBNM"
ORIENTACIONS = ["-", "|", "/", "\\"]
DIRECCIONS = ["+", "-"]
DIRECCIONS_NUMS = {"+": 1, "-": -1}
DIRECTORI_PARAULES = r"./paraules/"
DEV = False


if __name__ == "__main__":
    netejar_pantalla()
    main()
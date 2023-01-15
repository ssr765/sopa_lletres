import os
import random
from typing import List, Tuple

from colorama import Fore, Back, Style

from utils import netejar_pantalla, continuar


# Àlies de tipus per fer el codi més clar.
# Com que al codi una llista que conté llistes que contenen diccionaris sempre
# serà una sopa de lletres fem un àlies per referir-nos a aquest tipus
# d'estructura.
MatriuSopa = List[List[dict]]

LLETRES = "QWERTYUIOPASDFGHJKLZXCVBNM"
ORIENTACIONS = ["-", "|", "/", "\\"]
DIRECCIONS = ["+", "-"]
DIRECCIONS_NUMS = {"+": 1, "-": -1}
DIRECTORI_PARAULES = r"./paraules/"
DEV = True


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
    """Demana i retorna el nombre de paraules i la mida, si no s'especifica res
    o s'especifica un valor incorrecte, utilitzarà els valors per defecte."""
    # Nombre de paraules.
    try:
        num_paraules = int(input("Introdueix el nombre de paraules amb el que vols jugar (10 - 20): "))
        assert num_paraules in range(10, 21)

    except:
        num_paraules = 10
        print(f"Opció no valida, es jugarà amb el valor per defecte: {num_paraules}")
        continuar()

    # Mida del tauler.
    try:
        mida = int(input(f"Introdueix la mida del tauler ({num_paraules + 2} - {num_paraules + 12}): "))
        assert mida in range(num_paraules + 2, num_paraules + 13)

    except:
        mida = num_paraules + 6
        print(f"Opció no valida, es jugarà amb el valor per defecte: {mida}")
        continuar()

    return num_paraules, mida


def escull_paraules(fitxer: str, idioma: str, mida: int, num_paraules: int) -> List[str]:
    """Retorna una llista amb la quantitat especificada de paraules."""
    # Obre el fitxer mitjançant context manager i agafa les paraules del fitxer.
    with open(DIRECTORI_PARAULES + idioma + "/" + fitxer, "r", encoding="UTF-8") as f:
        paraules = [paraula.upper() for paraula in f.read().split("\n")]

    # Filtrem les paraules amb la funció filter, que mitjançant una funció
    # lambda avalua si les paraules no sobrepassen la mida.
    paraules = list(filter(lambda paraula: len(paraula) <= mida, paraules))

    # Barreja les paraules per a després retornar les num_paraules primeres.
    random.shuffle(paraules)
    
    return paraules[:num_paraules]


def pos(mida: int) -> Tuple[int, int]:
    """Retorna una tupla amb les coordenades aleatòries."""
    return random.randint(0, mida - 1), random.randint(0, mida - 1)


def crea_matriu(mida: int) -> MatriuSopa:
    """Crea i retorna una matriu de mida x mida ficant un diccionari amb les
    dades de la lletra a cada casella de cada fila de la matriu."""
    return [[{"c": "-", "e": False} for _ in range(mida)] for _ in range(mida)]


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
            print((Fore.GREEN if lletra["e"] else "") + lletra["c"].rjust(2) + (Fore.RESET if lletra["e"] else "") + " ", end="")
        print()


def hi_cap(mida: int, x: int, y: int, llargada_paraula: int, orientacio: str, direccio: str) -> bool:
    """Comprova si una paraula hi cap tenint en compte la orientació i direcció.
    Retorna un boolean."""
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


def colocar_paraules(mida: int, sopa: MatriuSopa, paraules: List[str]) -> None:
    """Col·loca les paraules a la sopa aleatòriament. Fa les comprovacions
    necessàries perqué hi càpiga la paraula i no se superposi amb cap altra
    paraula."""
    # Ordena la llista segons la longitud d'aquestes descendentment.
    paraules.sort(key=len, reverse=True)

    # Per cada paraula comprovarà si cap en el tauler i si no hi han lletres
    # ocupades pel mig.
    for p in paraules:
        posicio_valida = False
        while not posicio_valida:
            # Característiques aleatòries.
            x, y = pos(mida)
            orientacio = random.choice(ORIENTACIONS)
            direccio = random.choice(DIRECCIONS)

            # Comprovar que hi cap i que el segment està buit.
            posicio_valida = (hi_cap(mida, x, y, len(p), orientacio, direccio) 
                and esta_buit(segment_paraula(sopa, len(p), x, y, orientacio, direccio)))
        
        # Un cop hagi trobat una posició valida, ficarà les lletres a cada lloc.
        for i, ll in enumerate(p):

            # En cas que la direcció sigui inversa, ficarà el valor de i en
            # negatiu per fer la direcció contrària.
            i *= DIRECCIONS_NUMS[direccio]

            if orientacio == "-":
                colocar_lletra(sopa, ll, x, y + i, (x, y), orientacio, direccio, p)

            elif orientacio == "|":
                colocar_lletra(sopa, ll, x + i, y, (x, y), orientacio, direccio, p)

            elif orientacio == "/":
                colocar_lletra(sopa, ll, x - i, y + i, (x, y), orientacio, direccio, p)

            elif orientacio == "\\":
                colocar_lletra(sopa, ll, x + i, y + i, (x, y), orientacio, direccio, p)


def segment_paraula(sopa: MatriuSopa, llargada_paraula: int, x: int, y: int, orientacio: str, direccio: str) -> List[dict]:
    """Agafa un segment de la sopa segons els paràmetres passats. Mitjançant
    list comprehension crea una llista de diccionaris (no nous diccionaris sinó
    referències a aquests) i retorna la llista."""

    # Amb i*DIRECCIONS_NUMS[direccio] novament evita ficar if-else addicionals.
    if orientacio == "-":
        segment = [sopa[x][y + i*DIRECCIONS_NUMS[direccio]] for i in range(llargada_paraula)]
    
    elif orientacio == "|":
        segment = [sopa[x + i*DIRECCIONS_NUMS[direccio]][y] for i in range(llargada_paraula)]
    
    elif orientacio == "/":
        segment = [sopa[x - i*DIRECCIONS_NUMS[direccio]][y + i*DIRECCIONS_NUMS[direccio]] for i in range(llargada_paraula)]
    
    elif orientacio == "\\":
        segment = [sopa[x + i*DIRECCIONS_NUMS[direccio]][y + i*DIRECCIONS_NUMS[direccio]] for i in range(llargada_paraula)]
    
    return segment


def esta_buit(segment: List[dict]) -> bool:
    """Comprova un segment i retorna un boolean depenent si està completament
    buit o no."""
    return all([True if not ocupada(casella) else False for casella in segment])


def ocupada(casella: dict) -> bool:
    """Comprova si una casella está ocupada. Retorna False si no ho està i True
    si ho està."""
    if casella["c"] not in LLETRES:
        return False

    return True


def colocar_lletra(sopa: MatriuSopa, ll: str, x: int, y: int, index: Tuple[int, int], orientacio: str, direccio: str, paraula: str) -> None:
    """Canvia el caràcter del diccionari de la lletra."""
    sopa[x][y]["c"] = ll


def omple_lletres(sopa: MatriuSopa) -> None:
    """Canvia el caràcter de les caselles buides amb una lletra aleatòria."""
    for fila in sopa:
        for casella in fila:
            if casella["c"] == "-":
                casella["c"] = random.choice(LLETRES)


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
    """Crea un segment mitjançant la funció segment_paraula i compara el segment
    amb la paraula. Retorna un boolean segons sigui igual o no."""
    segment = segment_paraula(sopa, len(paraula), coor_x, coor_y, orientacio, direccio)
    segment = "".join([x["c"] for x in segment])

    return segment == paraula


def marcar_paraula(sopa: MatriuSopa, coor_x: int, coor_y: int, orientacio: str, direccio: str, paraula: str) -> None:
    """Canvia la clau "e" a True de cada diccionari de cada lletra de la paraula
    a la sopa. Modifica la referència del diccionari de la sopa amb la llista
    que ha retornat la funció segment_paraula."""
    segment = segment_paraula(sopa, len(paraula), coor_x, coor_y, orientacio, direccio)

    for lletra in segment:
        lletra["e"] = True


def comprovar_terminal(mida: int) -> None:
    """Comprova l'alçada i l'amplada de la terminal i dona un avís en cas que  alguna 
    sigui massa petita."""

    netejar_pantalla()
    # Comprovar alçada (mínim 15 línies de les dades del joc + mida del tauler).
    if os.get_terminal_size().lines < mida + 15:
        print(Fore.YELLOW + "L'alçada de la teva terminal es massa petita per veure el joc correctament." + Fore.RESET)
        print(f"És recomenable que l'ampliïs {mida + 15 - os.get_terminal_size().lines} línies.")
        continuar()

    netejar_pantalla()
    # Comprovar amplada (mínim 82 el missatge més llarg amb l'input més llarg
    # possible).
    if os.get_terminal_size().columns < 82:
        print(Fore.YELLOW + "L'amplada de la teva terminal es massa petita per veure el joc correctament." + Fore.RESET)
        print(f"És recomenable que l'ampliïs {82 - os.get_terminal_size().lines} línies.")
        continuar()


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

    # Crear la matriu, la llista de paraules i col·locar aquestes.
    sopa = crea_matriu(mida)
    paraules = escull_paraules(tematica + ".txt", idioma, mida, num_paraules)
    colocar_paraules(mida, sopa, paraules)

    comprovar_terminal(mida)

    # Emplenar el tauler amb lletres aleatòries en cas que no estigui activat el 
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

        # Informa de l'anterior paraula trobada.
        if paraula_trobada != None:
            print(Fore.GREEN + f"Has trobat la paraula {paraula_trobada}!" + Fore.RESET)
            paraula_trobada = None

        # Informa de l'anterior intent sense èxit.
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


if __name__ == "__main__":
    netejar_pantalla()
    main()

# Sergi Serra Reinoso
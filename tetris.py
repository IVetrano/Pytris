import random
ANCHO_JUEGO, ALTO_JUEGO = 9, 18
IZQUIERDA, DERECHA = -1, 1
CUBO = 0
Z = 1
S = 2
I = 3
L = 4
L_INV = 5
T = 6

PIEZAS = ()


def determinar_piezas(ruta_del_archivo):
    res = []
    with open(ruta_del_archivo, "r") as f:
        for linea in f:
            pieza = []
            orientaciones, _ = linea.rstrip("\n").split(" # ")
            orientaciones = orientaciones.split(" ")
            for orientacion in orientaciones:
                orien = []
                posiciones = orientacion.split(";")
                for posicion in posiciones:
                    pos_X, pos_Y = posicion.split(",")
                    pos_X, pos_Y = int(pos_X), int(pos_Y)
                    orien.append((pos_X, pos_Y))
                pieza.append(tuple(sorted(orien)))
            res.append(pieza)
    global PIEZAS 
    PIEZAS = res



def rotar(juego):
    pos_pieza, superficie, termino = juego
    #Ordeno la pieza
    pieza_ordenada = sorted(pos_pieza)
    pos_1_X, pos_1_Y = pieza_ordenada[0]
    pieza_en_el_origen = trasladar_pieza(pieza_ordenada, - pos_1_X, - pos_1_Y)
    for pieza in PIEZAS:
        if pieza_en_el_origen in pieza:
            ind_rot_siguiente = pieza.index(pieza_en_el_origen) + 1
            if ind_rot_siguiente >= len(pieza):
                juego_nuevo = trasladar_pieza(pieza[0], pos_1_X, pos_1_Y), superficie, termino
            else:
                juego_nuevo = trasladar_pieza(pieza[ind_rot_siguiente], pos_1_X, pos_1_Y), superficie, termino
            break
    if validar_posicion(juego_nuevo):
        return juego_nuevo
    return juego


def descenso_rapido(juego):
    pos_pieza, superficie, termino = juego
    nueva_pos_pieza = pos_pieza
    while validar_posicion((nueva_pos_pieza, superficie, terminado)):
        nueva_pos_pieza = trasladar_pieza(nueva_pos_pieza, 0, 1)
    return trasladar_pieza(nueva_pos_pieza,0, -1), superficie, termino





def generar_pieza(pieza=None):
    """
    Genera una nueva pieza de entre PIEZAS al azar. Si se especifica el parámetro pieza
    se generará una pieza del tipo indicado. Los tipos de pieza posibles
    están dados por las constantes CUBO, Z, S, I, L, L_INV, T.

    El valor retornado es una tupla donde cada elemento es una posición
    ocupada por la pieza, ubicada en (0, 0). Por ejemplo, para la pieza
    I se devolverá: ( (0, 0), (0, 1), (0, 2), (0, 3) ), indicando que 
    ocupa las posiciones (x = 0, y = 0), (x = 0, y = 1), ..., etc.
    """
    if pieza:
        return PIEZAS[pieza][0]
    return PIEZAS[random.randrange(len(PIEZAS))][0]

def trasladar_pieza(pieza, dx, dy):
    """
    Traslada la pieza de su posición actual a (posicion + (dx, dy)).

    La pieza está representada como una tupla de posiciones ocupadas,
    donde cada posición ocupada es una tupla (x, y). 
    Por ejemplo para la pieza ( (0, 0), (0, 1), (0, 2), (0, 3) ) y
    el desplazamiento dx=2, dy=3 se devolverá la pieza 
    ( (2, 3), (2, 4), (2, 5), (2, 6) ).
    """
    pieza_trasladada = []
    for pos in pieza:
        pieza_trasladada.append((pos[0] + dx, pos[1] + dy))

    return tuple(pieza_trasladada)

def crear_juego(pieza_inicial):
    """
    Crea un nuevo juego de Tetris.

    El parámetro pieza_inicial es una pieza obtenida mediante 
    pieza.generar_pieza. Ver documentación de esa función para más información.

    El juego creado debe cumplir con lo siguiente:
    - La grilla está vacía: hay_superficie da False para todas las ubicaciones
    - La pieza actual está arriba de todo, en el centro de la pantalla.
    - El juego no está terminado: terminado(juego) da False

    Que la pieza actual esté arriba de todo significa que la coordenada Y de 
    sus posiciones superiores es 0 (cero).
    """

    #Posiciones ocupadas por la superficie, si no hay superficie => la grilla esta vacia:
    superficie = ()

    termino = False

    return trasladar_pieza(pieza_inicial, ANCHO_JUEGO // 2, 0), superficie, termino
def dimensiones(juego):
    """
    Devuelve las dimensiones de la grilla del juego como una tupla (ancho, alto).
    """
    return ANCHO_JUEGO, ALTO_JUEGO
def pieza_actual(juego):
    """
    Devuelve una tupla de tuplas (x, y) con todas las posiciones de la
    grilla ocupadas por la pieza actual.

    Se entiende por pieza actual a la pieza que está cayendo y todavía no
    fue consolidada con la superficie.

    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    pos_pieza = juego[0]
    return pos_pieza
def hay_superficie(juego, x, y):
    """
    Devuelve True si la celda (x, y) está ocupada por la superficie consolidada.
    
    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    return (x, y) in juego[1]

def mover(juego, direccion):
    """
    Mueve la pieza actual hacia la derecha o izquierda, si es posible.
    Devuelve un nuevo estado de juego con la pieza movida o el mismo estado 
    recibido si el movimiento no se puede realizar.

    El parámetro direccion debe ser una de las constantes DERECHA o IZQUIERDA.
    """
    pos_pieza, superficie, termino = juego
    nueva_pos_pieza = trasladar_pieza(pos_pieza, direccion, 0)

    if validar_posicion((nueva_pos_pieza, superficie, termino)):
        return nueva_pos_pieza, superficie, termino
    return juego

def avanzar(juego, siguiente_pieza):
    """
    Avanza al siguiente estado de juego a partir del estado actual.
    
    Devuelve una tupla (juego_nuevo, cambiar_pieza) donde el primer valor
    es el nuevo estado del juego y el segundo valor es un booleano que indica
    si se debe cambiar la siguiente_pieza (es decir, se consolidó la pieza
    actual con la superficie).
    
    Avanzar el estado del juego significa:
     - Descender una posición la pieza actual.
     - Si al descender la pieza no colisiona con la superficie, simplemente
       devolver el nuevo juego con la pieza en la nueva ubicación.
     - En caso contrario, se debe
       - Consolidar la pieza actual con la superficie.
       - Eliminar las líneas que se hayan completado.
       - Cambiar la pieza actual por siguiente_pieza.

    Si se debe agregar una nueva pieza, se utilizará la pieza indicada en
    el parámetro siguiente_pieza. El valor del parámetro es una pieza obtenida 
    llamando a generar_pieza().

    **NOTA:** Hay una simplificación respecto del Tetris real a tener en
    consideración en esta función: la próxima pieza a agregar debe entrar 
    completamente en la grilla para poder seguir jugando, si al intentar 
    incorporar la nueva pieza arriba de todo en el medio de la grilla se
    pisara la superficie, se considerará que el juego está terminado.

    Si el juego está terminado (no se pueden agregar más piezas), la funcion no hace nada, 
    se debe devolver el mismo juego que se recibió.
    """

    #Si el juego está terminado => devuelvo el mismo juego
    if terminado(juego):
        return juego, False


    posicion_pieza_actual, superficie, termino = juego

    #Traslado la pieza 1 posicion hacia abajo:
    #   Si es una posicion valida => la pieza sigue siendo la misma 1 posicion mas abajo.
    #   Si es una posicion no valida => *agrego la pieza a la superficie.
    #                                   *cambio a la nueva pieza.
    #                                   *Si la posicion de la nueva pieza no es valida => termino juego
    #                                   *elimino las filas completas.
    nueva_pos_pieza = trasladar_pieza(posicion_pieza_actual, 0, 1)

    if validar_posicion((nueva_pos_pieza, superficie, termino)):
        return (nueva_pos_pieza, superficie, termino), False
    else:
        superficie += posicion_pieza_actual
        nueva_pos_pieza = trasladar_pieza(siguiente_pieza, ANCHO_JUEGO // 2, 0)

        if not validar_posicion((nueva_pos_pieza, superficie, termino)):
            return (posicion_pieza_actual, superficie, True), False

        #Detecto y remuevo las filas completas
        
        filas_llenas = detectar_filas_completas(superficie)
        for i in range(len(filas_llenas)):
            superficie = Remover_fila_completa(superficie, filas_llenas[i])

        return (nueva_pos_pieza, superficie, termino), True

def terminado(juego):
    """
    Devuelve True si el juego terminó, es decir no se pueden agregar
    nuevas piezas, o False si se puede seguir jugando.
    """

    return juego[2]


    
#----------------------------Funciones agregadas por mi----------------------------



def detectar_filas_completas(superficie):
    """
    Recibe la superficie y devuelve una tupla con las filas completas
    """

    en_fila = 0

    filas_llenas = []

    for i in range(ALTO_JUEGO):
        for pos in superficie:
            if pos[1] == i:
                en_fila += 1
        if en_fila == ANCHO_JUEGO:
            filas_llenas.append(i)
        en_fila = 0

    return tuple(filas_llenas)



def Remover_fila_completa(superficie, fila):
    """
    Recibe como parametro la superficie y la fila que se completó, luego elimina la fila completa,
    baja 1 posición la parte de la superficie que estaba sobre la fila y devuelve la nueva superficie.
    """

    superficie = list(superficie)

    #Borro todas las posiciones de la superficie que se encuentren en esa fila:

    for i in reversed(range(len(superficie))):
        if superficie[i][1] == fila:
            superficie.pop(i)

    #Recorro todas las posiciones de la superficie, si alguna estaba arriba de la fila borrada, la bajo 1 posicion

    for i in range(len(superficie)):
        if superficie[i][1] < fila:
            superficie[i] = list(superficie[i])
            superficie[i][1] += 1
            superficie[i] = tuple(superficie[i])

    return tuple(superficie)


def validar_posicion(juego):
    """
    Recibe como parametro un nuevo estado de juego y analiza si es 
    valido devolviendo un booleano que es True si es valida y False si no lo es.
    """
    #Para que sea valido:
    #   Ninguna posicion de la pieza debe estar incluida tambien en la superficie
    #   Ninguna posicion de la pieza debe pasarse de los extremos
    pos_pieza, superficie, termino = juego

    for pos in pos_pieza:
        if any ((pos in superficie, pos[0] < 0, pos[0] > ANCHO_JUEGO - 1, pos[1] > ALTO_JUEGO - 1)):
            return False
    return True


determinar_piezas("piezas.txt")


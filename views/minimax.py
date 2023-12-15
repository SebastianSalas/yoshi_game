from copy import deepcopy

# Definición de la clase Juego
class Juego:
    def __init__(self, pos_jugador1, pos_jugador2, tablero, puntaje_jugador1, puntaje_jugador2):
        self.tablero = tablero
        self.pos_jugador1 = pos_jugador1
        self.pos_jugador2 = pos_jugador2
        self.puntaje_jugador1 = puntaje_jugador1
        self.puntaje_jugador2 = puntaje_jugador2

# Definición de la clase Nodo
class Nodo:
    def __init__(self, juego, tipo, profundidad=0, padre=None, hijos=None):
        self.juego = juego
        self.padre = padre
        self.tipo = tipo
        self.hijos = hijos if hijos is not None else []
        self.profundidad = profundidad
        self.puntaje = -100000 if tipo == 'max' else 100000

# Función Minimax
def minimax(juego, profundidad):
    raiz = Nodo(juego, 'max')
    crear_arbol(raiz, profundidad)
    actualizar_minimax_arbol(raiz)

    for hijo in raiz.hijos:
        if hijo.puntaje == raiz.puntaje and hijo.profundidad == 1:
            return hijo.juego.pos_jugador1

# Función para crear el árbol de búsqueda
def crear_arbol(nodo, profundidad):
    if profundidad == 0:
        return

    movimientos = obtener_movimientos(nodo.juego.pos_jugador1, nodo.juego.pos_jugador2) if nodo.tipo == 'max' else \
                   obtener_movimientos(nodo.juego.pos_jugador2, nodo.juego.pos_jugador1)

    for movimiento in movimientos:
        tablero_copia = deepcopy(nodo.juego.tablero)
        puntos_movimiento = verificar_movimiento(tablero_copia, movimiento)

        nuevo_juego = estado_nuevo(nodo, movimiento, puntos_movimiento)

        nuevo_nodo = Nodo(nuevo_juego, 'min' if nodo.tipo == 'max' else 'max', nodo.profundidad + 1, nodo)
        nodo.hijos.append(nuevo_nodo)
        crear_arbol(nuevo_nodo, profundidad - 1)

# Función para crear un nuevo estado del juego después de un movimiento
def estado_nuevo(nodo, movimiento, puntos_movimiento):
    tablero_copia = deepcopy(nodo.juego.tablero)

    if puntos_movimiento is not None:
        tablero_copia[puntos_movimiento] = 0
        return Juego(movimiento,
                     nodo.juego.pos_jugador2 if nodo.tipo == 'max' else nodo.juego.pos_jugador1,
                     tablero_copia,
                     int(nodo.juego.puntaje_jugador1) + escalar_puntos(puntos_movimiento + 1, nodo.profundidad + 1),
                     nodo.juego.puntaje_jugador2 if nodo.tipo == 'max' else nodo.juego.puntaje_jugador1)
    else:
        return Juego(movimiento,
                     nodo.juego.pos_jugador2 if nodo.tipo == 'max' else nodo.juego.pos_jugador1,
                     nodo.juego.tablero,
                     nodo.juego.puntaje_jugador1,
                     nodo.juego.puntaje_jugador2)

# Función para convertir el árbol en una lista
def arbol_a_lista(node):
    tree_list = []
    for child in node.hijos:
        tree_list.append(child)
        tree_list += arbol_a_lista(child)
    return tree_list

# Función para actualizar los valores minimax en el árbol
def actualizar_minimax_arbol(nodo):
    children = arbol_a_lista(nodo)
    max_depth = 0

    for child in children:
        if child.profundidad > max_depth:
            max_depth = child.profundidad

        child.puntaje = int(child.juego.puntaje_jugador1) - int(child.juego.puntaje_jugador2) + \
                        funcion_utilidad(child.juego.pos_jugador1,
                                         child.juego.pos_jugador2, child.juego.tablero)

    while max_depth > 0:
        for child in children:
            if child.profundidad == max_depth:
                if child.padre.tipo == 'max':
                    child.padre.puntaje = max(child.padre.puntaje, child.puntaje)
                elif child.padre.tipo == 'min':
                    child.padre.puntaje = min(child.padre.puntaje, child.puntaje)

        max_depth -= 1

# Función para verificar el movimiento en el tablero
def verificar_movimiento(tablero, movimiento):
    for indice, punto in enumerate(tablero):
        if punto == movimiento:
            return indice
    return None

# Función para obtener los movimientos posibles
def obtener_movimientos(posicion, posicion2):
    x, y = posicion

    def agregar_movimiento(dx, dy):
        nuevo_x, nuevo_y = x + dx, y + dy
        if 0 <= nuevo_x <= 7 and 0 <= nuevo_y <= 7 and posicion2 != (nuevo_x, nuevo_y):
            movimientos.append((nuevo_x, nuevo_y))

    movimientos = []

    for dx, dy in [(-1, -2), (-1, 2), (1, -2), (1, 2), (-2, -1), (-2, 1), (2, -1), (2, 1)]:
        agregar_movimiento(dx, dy)

    return movimientos

# Función para escalar los puntos según la profundidad
def escalar_puntos(puntos, profundidad):
    if profundidad == 0:
        return puntos * 0
    if profundidad in [1, 2]:
        return puntos
    if profundidad in [3, 4]:
        return puntos * 0.7
    if profundidad in [5, 6]:
        return puntos * 0.4
    return puntos

# Función de utilidad que calcula la diferencia en distancias entre jugadores y el tablero
def funcion_utilidad(posicion1, posicion2, tablero):
    distancia_jugador1 = calcular_distancias(posicion1, tablero)
    distancia_jugador2 = calcular_distancias(posicion2, tablero)

    return sum([(i + 1) / obtener_escala(distancia) if distancia != 0 else 0 for i, distancia in enumerate(distancia_jugador1)]) - \
           sum([(i + 1) / obtener_escala(distancia) if distancia != 0 else 0 for i, distancia in enumerate(distancia_jugador2)])

# Función para calcular las distancias Manhattan desde una posición dada en el tablero
def calcular_distancias(posicion, tablero):
    distancias = []
    for punto in tablero:
        if punto != 0:
            manhattan = distancia_manhattan(punto, posicion)
            if manhattan == 3:
                movimientos = obtener_movimientos(posicion, tablero)
                if punto in movimientos:
                    distancias.append(-1)
                else:
                    distancias.append(manhattan)
            elif posicion in [(0, 0), (7, 0), (0, 7), (7, 7)] and manhattan == 2:
                distancias.append(4)
            else:
                distancias.append(manhattan)
        else:
            distancias.append(0)
    return distancias

# Función para calcular la distancia Manhattan entre dos puntos
def distancia_manhattan(posicion1, posicion2):
    return abs(posicion1[0] - posicion2[0]) + abs(posicion1[1] - posicion2[1])

# Función para obtener la escala de puntos según la distancia
def obtener_escala(distancia):
    escalas = (1, 1, 3, 2, 3, 4, 3, 4, 5, 4, 5, 4, 5, 4, 6)
    return escalas[min(abs(distancia), len(escalas) - 1)]
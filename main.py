import tetris
import gamelib


ESPERA_DESCENDER = 8
DURACION_CANCION = 1110
								#Relacion de aspecto 17/20
ANCHO_PANTALLA = 510			#(17x30)
ALTO_PANTALLA = 600				#(20x30)
DIM_CASILLA = ANCHO_PANTALLA // 17


def establecer_teclas(ruta_del_archivo):
	"""
	Recibe la ruta del archivo donde se guardan las teclas y devuelve un diccionario las teclas
	como claves y su accion asociada como valor
	"""
	funciones = {"DERECHA": DERECHA, "IZQUIERDA": IZQUIERDA, "ROTAR": ROTAR,
				"DESCENDER": DESCENDER, "GUARDAR": GUARDAR, "CARGAR": CARGAR, "SALIR": "SALIR"}
	res = {}
	with open(ruta_del_archivo, "r") as teclas:
		for linea in teclas:
			try:
				tecla, accion = linea.rstrip("\n").split(" = ")
				res[tecla] = funciones[accion]
			except ValueError:
				continue
	return res


#Funciones para las teclas:
def DERECHA(juego):
	"""
	Recibe el estado de juego actual y devuelve un nuevo estado de juego
	con la pieza movida una casilla hacia la derecha
	"""
	return tetris.mover(juego, tetris.DERECHA)

def IZQUIERDA(juego):
	"""
	Recibe el estado de juego actual y devuelve un nuevo estado de juego
	con la pieza movida una casilla hacia la izquierda
	"""
	return tetris.mover(juego, tetris.IZQUIERDA)

def ROTAR(juego):
	"""
	Recibe el estado de juego actual y devuelve un nuevo estado de juego
	con la pieza rotada, ademas reproduce un sonido
	"""
	gamelib.play_sound("whoosh.wav")
	return tetris.rotar(juego)

def DESCENDER(juego):
	"""
	Recibe el estado de juego actual y devuelve un nuevo estado de juego
	con la pieza movida a la posicion mas baja posible, ademas reproduce un sonido
	"""
	gamelib.play_sound("Click.wav")
	return tetris.descenso_rapido(juego)

def GUARDAR(juego):
	"""
	Guarda el estado de juego actual en el archivo 'partida_guardada.txt'
	"""
	with open("partida_guardada.txt", "w") as f:
		for e in juego:
			f.writelines(str(e) + ";")
	return juego

def CARGAR(juego):
	"""
	Carga el estado de juego guardado en el archivo 'partida_guardada.txt'
	"""
	pieza_cargada = []
	superficie_cargada = []
	termino_cargado = False
	with open("partida_guardada.txt", "r") as f:

		pieza, superficie, termino = f.readline().rstrip(";").split(";")

		#Cargo la pieza
		for posicion in pieza.lstrip("(").rstrip(")").split("), ("):
			posicion = posicion.lstrip("(")
			pos_x, pos_y = posicion.split(", ")
			pieza_cargada.append((int(pos_x), int(pos_y)))

		#Cargo la superficie
		print(superficie)
		if superficie != "()":
			for posicion in superficie.lstrip("(").rstrip(")").split("), ("):
				posicion = posicion.lstrip("(")
				pos_x, pos_y = posicion.split(", ")
				superficie_cargada.append((int(pos_x), int(pos_y)))
		else:
			superficie_cargada = ()

		#Cargo termino
		termino_cargado = termino == "True"

	return tuple(pieza_cargada), tuple(superficie_cargada), termino_cargado



def pos_en_pantalla(posicion):
	"""
	Recibe una posicion en la grilla y devuelve la posicion en la pantalla
	"""
	x, y = posicion

	medio_casilla = DIM_CASILLA//2
	ancho_grilla_fin = (tetris.ANCHO_JUEGO + 1) * DIM_CASILLA
	alto_grilla_fin = (tetris.ALTO_JUEGO + 1) * DIM_CASILLA

	return (DIM_CASILLA + x * DIM_CASILLA, DIM_CASILLA + y * DIM_CASILLA)



def pantalla_menu():
	"""
	Muestra el menu del juego
	"""
	gamelib.draw_rectangle(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA, outline='gray70', fill='gray9')
	gamelib.draw_text("PYTRIS", ANCHO_PANTALLA//2, DIM_CASILLA, size=30, fill='orange2')
	gamelib.draw_text("Presiona ROTAR para comenzar", ANCHO_PANTALLA//2, DIM_CASILLA * 5, size=15, fill='orange2')
	gamelib.draw_text("Presiona DESCENDER para ver puntuaciones", ANCHO_PANTALLA//2, DIM_CASILLA * 6, size=15, fill='orange2')
	gamelib.draw_text("Presiona SALIR para cerrar la ventana", ANCHO_PANTALLA//2, DIM_CASILLA * 7, size=15, fill='orange2')



def pantalla_scores():
	"""
	Muestra los 10 mejores scores en pantalla
	"""
	gamelib.draw_rectangle(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA, outline='gray70', fill='gray9')
	gamelib.draw_text("SCORES", ANCHO_PANTALLA//2, DIM_CASILLA, size=30, fill='orange2')
	with open("puntajes.txt", "r") as f:
		aux = 3
		for linea in f:
			gamelib.draw_text(linea, ANCHO_PANTALLA//2, DIM_CASILLA * aux, size=20, fill='orange2')
			aux += 1
		aux += 1
	gamelib.draw_text("Presiona ROTAR para ir al menu", ANCHO_PANTALLA//2, DIM_CASILLA * aux, size=22, fill='orange2')



def pantalla_juego(juego, proxima_pieza, puntos):
	"""
	Recibe el estado de juego actual, la proxima pieza y los puntos y los grafica
	"""

	#Dibujo la grilla
	pos_pieza, superficie, _ = juego

	ancho_grilla_fin = (tetris.ANCHO_JUEGO + 1) * DIM_CASILLA
	alto_grilla_fin = (tetris.ALTO_JUEGO + 1) * DIM_CASILLA

	gamelib.draw_rectangle(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA, outline='gray70', fill='gray9')

	for v in range(DIM_CASILLA, DIM_CASILLA * (tetris.ALTO_JUEGO + 2), DIM_CASILLA):
		for h in range(DIM_CASILLA, DIM_CASILLA * (tetris.ANCHO_JUEGO + 2), DIM_CASILLA):
			gamelib.draw_line(h, v,ancho_grilla_fin, v, fill='gray70')
			gamelib.draw_line(h, v, h, alto_grilla_fin, fill='gray70')

	#Dibujo superficie
	for pos in superficie:
		pos_x, pos_y = pos_en_pantalla(pos)
		gamelib.draw_rectangle(pos_x, pos_y, pos_x + DIM_CASILLA, pos_y + DIM_CASILLA, outline='gray30', fill='gray48')


	#Dibujo pieza fantasma
	pieza_fantasma, _, _ = tetris.descenso_rapido(juego)

	for pos in pieza_fantasma:
		pos_x, pos_y = pos_en_pantalla(pos)
		gamelib.draw_rectangle(pos_x, pos_y, pos_x + DIM_CASILLA, pos_y + DIM_CASILLA, outline='orange2', fill='gray9', width = 2)


	#Dibujo la pieza
	for pos in pos_pieza:
		pos_x, pos_y = pos_en_pantalla(pos)
		gamelib.draw_rectangle(pos_x, pos_y, pos_x + DIM_CASILLA, pos_y + DIM_CASILLA, outline='orange4', fill='orange2')

	#Dibujo puntos
	ancho_cuadros_ini = ancho_grilla_fin + DIM_CASILLA
	ancho_cuadros_fin = ancho_grilla_fin + DIM_CASILLA * 6

	gamelib.draw_rectangle(ancho_cuadros_ini, DIM_CASILLA, ancho_cuadros_fin, DIM_CASILLA * 3, outline='gray70', fill='gray9')
	gamelib.draw_text("Puntos", ancho_grilla_fin + DIM_CASILLA * (7/2), DIM_CASILLA * (3/2))
	gamelib.draw_text(str(puntos), ancho_grilla_fin + DIM_CASILLA * (7/2), DIM_CASILLA * (5/2))


	#Dibujo sigiente pieza
	gamelib.draw_rectangle(ancho_cuadros_ini, DIM_CASILLA * 4, ancho_cuadros_fin, DIM_CASILLA * 11, outline='gray70', fill='gray9')
	gamelib.draw_text("Siguiente", ancho_grilla_fin + DIM_CASILLA * (7/2), DIM_CASILLA * (9/2))
	for x, y in proxima_pieza:
		pos_x, pos_y = DIM_CASILLA * 12 + x * DIM_CASILLA, DIM_CASILLA * 6 + y * DIM_CASILLA
		gamelib.draw_rectangle(pos_x, pos_y, pos_x + DIM_CASILLA, pos_y + DIM_CASILLA, outline='orange4', fill='orange2')



def main():
	# Inicializar el estado del juego
	gamelib.resize(ANCHO_PANTALLA, ALTO_PANTALLA)
	gamelib.title("Pytris")
	juego = tetris.crear_juego(tetris.generar_pieza())
	proxima_pieza = tetris.generar_pieza()
	teclas = establecer_teclas("teclas.txt")

	timer_bajar = ESPERA_DESCENDER
	pantalla = "menu"
	timer_cancion = DURACION_CANCION
	timer_puntos = 30
	puntos = 0
	gamelib.play_sound('Cancion.wav')
	while gamelib.loop(fps=30):
	
		#Funcionamiento pantalla de menu
		if pantalla == "menu":
			gamelib.draw_begin()
			pantalla_menu()
			gamelib.draw_end()
	
			for event in gamelib.get_events():
				if not event:
					break
				if event.type == gamelib.EventType.KeyPress:
					tecla = event.key
					if teclas.get(tecla, "") == ROTAR:
						pantalla = "juego"
					if teclas.get(tecla, "") == DESCENDER:
						pantalla = "score"
					if teclas.get(tecla, "") == "SALIR":
						return

		#Funcionamiento pantalla de scores
		elif pantalla == "score":
			gamelib.draw_begin()
			pantalla_scores()
			gamelib.draw_end()
	
			for event in gamelib.get_events():
				if not event:
					break
				if event.type == gamelib.EventType.KeyPress:
					tecla = event.key
					if teclas.get(tecla, "") == ROTAR:
						pantalla = "menu"
					if teclas.get(tecla, "") == "SALIR":
						return


		#Funcionamiento pantalla de juego
		elif pantalla == "juego":
			gamelib.draw_begin()
			pantalla_juego(juego, proxima_pieza, puntos)
			gamelib.draw_end()
	
			_, _, termino = juego
	
			for event in gamelib.get_events():
				if not event:
					break
				if event.type == gamelib.EventType.KeyPress:
					tecla = event.key
					if tecla not in teclas:
						break
					if teclas[tecla] != "SALIR":
						juego = teclas[tecla](juego)
					else:
						return
	
			timer_bajar -= 1
			if timer_bajar == 0:
				timer_bajar = ESPERA_DESCENDER
				juego, cambio = tetris.avanzar(juego, proxima_pieza)
				if cambio:
					proxima_pieza = tetris.generar_pieza()
	
			timer_puntos -= 1
			if timer_puntos == 0:
				timer_puntos = 30
				puntos += 1
	
			if termino:

				puntajes = []
				with open("puntajes.txt", "r") as f1:
					for linea in f1:
						nombre, puntaje = linea.split(": ")
						puntaje = int(puntaje)
						puntajes.append((nombre, puntaje))

				if len(puntajes) < 10:
					nombre_jugador = gamelib.input("Inserte nombre por favor")
					puntajes.append((nombre_jugador, puntos))
					puntajes.sort(reverse= True, key=lambda x: x[1])
				else:
					puntajes.sort(reverse= True, key=lambda x: x[1])
					for i in range(len(puntajes)):
						jugador, puntaje = puntajes[i]
						if puntos >= puntaje:
							nombre_jugador = gamelib.input("Inserte nombre por favor")
							puntajes.insert(i, (nombre_jugador, puntos))
							puntajes.pop()
							break

				with open("puntajes.txt", "w") as f:
					for nombre, puntaje in puntajes:
						f.write(f"{nombre}: {puntaje}\n")

				juego = tetris.crear_juego(tetris.generar_pieza())
				puntos = 0
				pantalla = "menu"


		timer_cancion -= 1
		if timer_cancion == 0:
			timer_cancion = DURACION_CANCION
			gamelib.play_sound('Cancion.wav')


gamelib.init(main)
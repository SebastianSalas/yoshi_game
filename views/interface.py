import os
import tkinter as tk
import numpy as np
import uuid
from PIL import Image, ImageTk
from minimax import *

class mainInterface(tk.Tk):

  global initial_matriz, matriz, movements_matriz, rows, columns

  initial_matriz = np.array([
    [1, 1, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 1, 1]])

  matriz = np.copy(initial_matriz)
  movements_matriz = np.copy(initial_matriz)

  # Número de filas y columnas en la matriz
  rows, columns = matriz.shape
  
  def __init__(self): # Función que crea la ventana principal

    super().__init__()

    # Obtener las dimensiones de la pantalla
    screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
  
    # Calcular las dimensiones y posición de la ventana
    windowWidth, windowHeight = round(screen_width / 1.6), round(screen_height / 1.6)
    x, y = round((screen_width - windowWidth) / 2), round((screen_height - windowHeight) / 2) 
    self.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")
    
    # Propiedades de la ventana
    self.config(bg="white")
    self.title("IA - Proyecto #2: Yoshi’s battle")
    self.resizable(True, True)
    self.image_dict = {}
    self.ubicate_yoshis()

    self.turno_yoshi_verde = True

    # Crear el contenedor izquierdo
    self.left_frame = tk.Frame(self, padx=10, pady=10, bg="white")
    self.left_frame.pack(side="left", fill="y")
    self.left_frame.place(relx=0, rely=0, relwidth=0.65, relheight=1)

    # Crear el contenedor derecho
    self.right_frame = tk.Frame(self, padx=10, pady=10, bg="white")
    self.right_frame.pack(side="right", fill="y")
    self.right_frame.place(relx=0.64, rely=0, relwidth=0.35, relheight=1)
    
    # Canvas para representar la matríz en el contenedor izquierdo
    self.canvas_matriz = tk.Canvas(self.left_frame, bg="white", bd=2, relief="solid", highlightbackground="#8EEA6F")
    self.canvas_matriz.pack(expand=True, fill="both")
    self.canvas_matriz.bind("<Button-1>", self.matriz_click)
    self.canvas_matriz.bind("<Configure>", self.dibujar_matriz)

    # Canvas en el contenedor derecho
    self.right_canvas = tk.Canvas(self.right_frame, bg="white", bd=2, relief="solid", highlightbackground="#8EEA6F")
    self.right_canvas.pack(expand=True, fill="both")
    self.right_canvas.bind("<Configure>", self.right_canvas_resize)

    # Primera imagen en el contenedor derecho
    first_image = Image.open("resources/images/yoshigame.png")
    self.photo = ImageTk.PhotoImage(first_image)
    self.first_label = tk.Label(self.right_canvas, image = self.photo)
    self.first_label.config(bg="white")
    self.first_label.pack(padx= 10, pady=10, fill="x")

    # Etiqueta con el título del programa
    self.title_label = tk.Label(self.right_canvas, text="Yoshi's battle", fg="#8EEA6F", font=("Helvetica", 36, "bold"))
    self.title_label.config(bg="white")
    self.title_label.pack(pady="5", padx="10", fill="x")

    # Etiqueta de selección de dificultad
    self.score_label = tk.Label(self.right_canvas, text="Seleccione la dificultad de juego:", fg="black", font=("Helvetica", 12), anchor="w", justify="left")
    self.score_label.config(bg="white")
    self.score_label.pack(pady="5", padx="10", fill="x")

    # Selector de dificultad
    difficulty_options = ["Seleccionar...", "Principiante", "Intermedio", "Experto"]
    selected_difficulty = tk.StringVar(self)
    selected_difficulty.set(difficulty_options[0])
    select_difficulty = tk.OptionMenu(self.right_canvas, selected_difficulty, *difficulty_options)
    select_difficulty.config(font=('Helvetica', 11), bg="#8EEA6F", fg="black")
    select_difficulty.pack(padx="10", fill="x")

    # Crear un frame para contener las puntuaciones
    self.score_frame = tk.Frame(self.right_canvas, bg="white")
    self.score_frame.pack(fill="both", padx=10, pady=10)

    # Etiqueta de puntuaciones
    self.score_label = tk.Label(self.score_frame, text="Puntuaciones:", fg="black", font=("Helvetica", 12), anchor="w", justify="left")
    self.score_label.config(bg="white")
    self.score_label.pack(side="top", fill="both", expand=True)

    # Etiqueta de puntuación Yoshi verde
    self.green_score_label = tk.Label(self.score_frame, text="0", fg="#8EEA6F", font=("Helvetica", 36), anchor="center")
    self.green_score_label.config(bg="white")
    self.green_score_label.pack(side="left", fill="both", expand=True, padx=(10, 10))

    # Etiqueta de puntuación Yoshi rojo
    self.red_score_label = tk.Label(self.score_frame, text="0", fg="red", font=("Helvetica", 36), anchor="center")
    self.red_score_label.config(bg="white")
    self.red_score_label.pack(side="left", fill="both", expand=True, padx=(10, 10))

    # Crear un frame para contener los botones inferiores
    self.buttons_frame = tk.Frame(self.right_canvas, bg="white")
    self.buttons_frame.pack(side=tk.BOTTOM, fill="x", padx=10, pady=10)

    def start_algorithm(): # Función del botón de inicio
      if (selected_difficulty.get() != "Seleccionar..."):
        # Bloquear el uso del botón de inicio
        self.start_button.config(state=tk.DISABLED)
        # Bloquear el uso del selector de dificultad
        select_difficulty.config(state=tk.DISABLED)
        # Llamar a la jugada de Yoshi verde
        self.green_yoshi_turn()

    # Botón para iniciar la partida
    self.start_button = tk.Button(self.buttons_frame, text="Iniciar", bg="#8EEA6F", fg="black", command=start_algorithm)
    self.start_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    self.start_button.config(font=('Helvetica', 12))

    def restart(): # Función para reiniciar la partida
      global movements_matriz
      self.start_button.config(state=tk.ACTIVE)
      select_difficulty.config(state=tk.ACTIVE)
      selected_difficulty.set(difficulty_options[0])
      self.red_score_label.config(text="0")
      self.green_score_label.config(text="0")
      movements_matriz = np.copy(initial_matriz)
      app.ubicate_yoshis()
      app.dibujar_matriz(None)
    
    # Botón para reiniciar la partida
    restart_button = tk.Button(self.buttons_frame, text="Reiniciar", bg="#8EEA6F", fg="black", command=restart)
    restart_button.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
    restart_button.config(font=('Helvetica', 12))

    def credits(): # Función que crea ventana con los créditos
      credits_window = tk.Toplevel(self)
      credits_window.title("Proyecto #2: Yoshi´s battle - Inteligencia artificial")
      credits_window.geometry(f"{round(windowWidth * 0.5)}x{round(windowHeight * 0.5)}+{x}+{y}")
      credits_window.config(bg="#8EEA6F")
      # Etiqueta para mostrar los créditos
      credits_label = tk.Label(credits_window, text="HECHO POR:\n\nDIEGO FERNANDO VICTORIA - 202125877\nDIEGO.VICTORIA@CORREOUNIVALLE.EDU.CO\n\nJANIERT SEBASTIÁN SALAS - 201941265\nJANIERT.SALAS@CORREOUNIVALLE.EDU.CO\n\nJHON ALEXANDER VALENCIA - 202042426\nJHON.HILAMO@CORREOUNIVALLE.EDU.CO")
      credits_label.config(font=('Helvetica', 11), bg="white", bd=3, relief="solid")
      credits_label.place(relx=0.5, rely=0.5, anchor="center")
      credits_window.transient(self)
      credits_window.wait_window()

    # Botón de créditos
    credits_button = tk.Button(self.buttons_frame, text="Créditos", bg="#8EEA6F", fg="black", command=credits)
    credits_button.grid(row=1, column=0, sticky="ew", padx=5, pady=5, columnspan=2)
    credits_button.config(font=('Helvetica', 12))

    # Distribuir uniformemente el espacio en X entre los botones
    self.buttons_frame.columnconfigure(0, weight=1)
    self.buttons_frame.columnconfigure(1, weight=1)
    
  def resize_first_image(self, image, size): # Cálculo de las dimensiones que tendrá la imagen principal de Yoshi
    return ImageTk.PhotoImage(image.resize(size, Image.LANCZOS))
  
  def right_canvas_resize(self, event): # Manejar el evento de redimensionar el Canvas derecho y la imagen
    self.photo = self.resize_first_image(Image.open("resources/images/yoshigame.png"), (self.right_canvas.winfo_width(), round(self.right_canvas.winfo_height() * 0.4)))
    self.first_label.config(image=self.photo)

  def ubicate_yoshis(self): # Genera posiciones aleatorias en el mapa para ubicar ambos yoshi's
    global matriz
    matriz = np.copy(initial_matriz)
    # Yoshi verde 
    zeros = np.argwhere(matriz == 0)
    random_pos = zeros[np.random.choice(len(zeros))]
    matriz[random_pos[0], random_pos[1]] = 3
    # Yoshi rojo
    zeros = np.delete(zeros, np.where((zeros == random_pos).all(axis=1)), axis=0)
    random_pos = zeros[np.random.choice(len(zeros))]
    matriz[random_pos[0], random_pos[1]] = 4

  def green_yoshi_turn(self):
    global matriz, movements_matriz
    green_position, red_position = np.where(matriz == 3), np.where(matriz == 4)
    green_coordinates, red_coordinates = list(zip(green_position[0], green_position[1])), list(zip(red_position[0], red_position[1]))
    gameminimax = Juego(green_coordinates[0], red_coordinates[0], [(row, column) for row, values in enumerate(matriz) for column, value in enumerate(values) if value in [1, 2]], self.green_score_label.cget("text"), self.red_score_label.cget("text"))
    # Actualizar la matriz y las coordenadas del Yoshi verde
    yoshi_y, yoshi_x = green_coordinates[0]
    matriz[yoshi_y, yoshi_x] = 0
    green_y, green_x = minimax(gameminimax, 4)
    self.check_coin("green", matriz[green_y, green_x], self.green_score_label.cget("text"))
    matriz[green_y, green_x] = 3
    # Actualizar la interfaz gráfica
    self.dibujar_matriz(None)
    

  def matriz_click(self, event): # Manejar evento de clic en el Canvas izquierdo
    global matriz, movements_matriz
    # Obtener la posición del clic
    mouse_x, mouse_y = event.x, event.y
    # Tamaño de cada rectángulo en el Canvas
    rectangle_width, rectangle_height = self.canvas_matriz.winfo_width() // columns, self.canvas_matriz.winfo_height() // rows
    # Calcular la fila y columna del clic
    click_row, click_column = mouse_y // rectangle_height, mouse_x // rectangle_width
    # Obtener las coordenadas actuales del Yoshi rojo
    red_position = np.where(matriz == 4)
    red_coordinates = list(zip(red_position[0], red_position[1]))
    red_y, red_x = red_coordinates[0]
    
    if hasattr(self, 'start_button') and self.start_button.cget("state") == "disabled": # Comprueba que se haya iniciado el juego
      if (matriz[click_row, click_column] == 4): # Comprueba que se haya hecho click en el Yoshi rojo
        app.possible_movements("red")
      if (movements_matriz[click_row, click_column] == 6): # Comprueba si hay una casillas disponibles
        matriz[red_y, red_x] = 0
        if (matriz[click_row, click_column] in [1, 2]): # Comprueba si se toma una moneda
          self.check_coin("red", matriz[click_row, click_column], self.red_score_label.cget("text"))
        movements_matriz = np.copy(initial_matriz)
        matriz[click_row, click_column] = 4
        self.leaving_coin(red_y, red_x)
        self.green_yoshi_turn()
    
    app.dibujar_matriz(None)

  def possible_movements(self, yoshi): # Coordenadas (Y, X)
    global matriz, movements_matriz
    green_position, red_position = np.where(matriz == 3), np.where(matriz == 4)
    green_coordinates, red_coordinates = list(zip(green_position[0], green_position[1])), list(zip(red_position[0], red_position[1]))
    yoshi_coordinates = {"red": red_coordinates[0], "green": green_coordinates[0]}
    yoshi_y, yoshi_x = yoshi_coordinates[yoshi]
    
    movements = [ # Posibles direcciones de movimiento
      (-2, -1), (-2, 1), # Movimiento superior izquierdo y derecho
      (2, 1), (2, -1), # Movimiento inferior derecho e izquierdo
      (-1, 2), (1, 2), # Movimiento derecho superior e inferior
      (1, -2), (-1, -2)] # Movimiento izquierdo inferior y superior

    for dy, dx in movements: # Se comprueba que sea posible el movimiento y que no esté el otro yoshi en la casilla...
      next_y, next_x = yoshi_y + dy, yoshi_x + dx
      if 0 <= next_y < rows and 0 <= next_x < columns and matriz[next_y, next_x] not in [3, 4, 5]: # Verificar límites y obstáculos
        movements_matriz[next_y, next_x] = 6

  def check_coin(self, yoshi, value, score): # Comprueba si un yoshi está sobre una moneda
    score_label = self.red_score_label if yoshi == "red" else self.green_score_label
    score_label.config(text=str(int(score) + 1 if value == 1 else int(score) + 3 if value == 2 else int(score)))
    
  def leaving_coin(self, yoshi_y, yoshi_x): # Comprueba si un yoshi deja una casilla donde había una moneda
    if (initial_matriz[yoshi_y, yoshi_x] in [1, 2] and matriz[yoshi_y, yoshi_x] not in [3, 4]):
      matriz[yoshi_y, yoshi_x] = 5

  def dibujar_matriz(self, event):
    # Eliminar dibujos anteriores
    self.canvas_matriz.delete("all")
    # Tamaño de cada rectángulo en el Canvas
    rectangle_width, rectangle_height = self.canvas_matriz.winfo_width() // columns, self.canvas_matriz.winfo_height() // rows

    for row in range(rows):
      for column in range(columns):

        # Calcular coordenadas de la celda
        x1 = column * rectangle_width # Esquina superior izquierda 
        y1 = row * rectangle_height # Esquina superior izquierda
        x2 = x1 + rectangle_width # Esquina inferior derecha
        y2 = y1 + rectangle_height # Esquina inferior derecha
        x_center, y_center = (x1 + x2) // 2, (y1 + y2) // 2

        # Color, texto, borde e imagen para el rectángulo
        color, color_border, border, image_path = "white", "black", 1, None

        if matriz[row][column] == 0: # Casilla libre
          pass
        elif matriz[row][column] == 1: # Casilla con estrella simple
          color, image_path = "#4F80BD", "resources/images/basic_Coin.gif"
        elif matriz[row][column] == 2: # Casilla con estrella especial
          color, image_path = "#4F80BD","resources/images/star_Coin.gif"
        elif matriz[row][column] == 3: # Casilla con Yoshi verde operado por el computador
          image_path = "resources/images/yoshi_Green.png"
        elif matriz[row][column] == 4: # Casilla con Yoshi rojo operado por el jugador
          image_path = "resources/images/yoshi_Red.png"
        elif matriz[row][column] == 5: # Casilla inhabilitada
          image_path = "resources/images/wall.png"
        if movements_matriz[row][column] == 6: # Casilla disponible para movimiento
          color_border, border = "#8B0000", 5
       
        # Dibujar rectángulos en el Canvas
        self.canvas_matriz.create_rectangle(x1, y1, x2, y2, fill=color, outline=color_border, width=border)

        if image_path: # Se agrega imagen a los rectángulos que requieran
          unique_id = str(uuid.uuid4())  # Generar un identificador único para el rectángulo
          image = ImageTk.PhotoImage(Image.open(image_path).resize((round(rectangle_width * 0.9), round(rectangle_height * 0.9)), Image.LANCZOS))
          self.image_dict[unique_id] = image  # Almacenar la imagen en el diccionario
          self.canvas_matriz.create_image(x_center, y_center, anchor=tk.CENTER, image=image)

if __name__ == "__main__": # Método principal
  app = mainInterface()
  app.mainloop()
  #os.system('cls') # Limpia la terminal
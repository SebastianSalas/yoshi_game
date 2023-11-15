import os
import tkinter as tk
import numpy as np
import uuid
from PIL import Image, ImageTk

class mainInterface(tk.Tk):

  global matriz

  matriz = np.array([
    [1, 1, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 1, 1]])
  
  #First yoshi
  zeros = np.argwhere(matriz == 0)
  random_pos = zeros[np.random.choice(len(zeros))]
  matriz[random_pos[0], random_pos[1]] = 3
  #Second yoshi
  zeros = np.delete(zeros, np.where((zeros == random_pos).all(axis=1)), axis=0)
  random_pos = zeros[np.random.choice(len(zeros))]
  matriz[random_pos[0], random_pos[1]] = 4

  def __init__(self):

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
    self.title_label = tk.Label(self.right_canvas, text="Yoshi's battle", fg="#8EEA6F", font=("Helvetica", 20, "bold"))
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

    # Etiqueta de selección de próximo movimiento
    self.select_movement_label = tk.Label(self.right_canvas, text="Seleccione el algoritmo:", fg="black", font=("Helvetica", 12), anchor="w", justify="left")
    self.select_movement_label.config(bg="white")
    self.select_movement_label.pack(pady="5", padx="10", fill="x")

    # Selector del próximo movimiento
    movements_options = ["Seleccionar...", "Superior-Izquierdo", "Superior-Derecho", "Inferior-Izquierdo", "Inferior derecho"]
    selected_movement = tk.StringVar(self.right_canvas)
    selected_movement.set(movements_options[0])
    movements_menu = tk.OptionMenu(self.right_canvas, selected_movement, *movements_options)
    movements_menu.config(font=('Helvetica', 11), bg="#8EEA6F", fg="black")
    movements_menu.pack(padx="10", fill="x")
    movements_menu.config(state=tk.DISABLED)

    # Crear un frame para contener las puntuaciones
    self.score_frame = tk.Frame(self.right_canvas, bg="white")
    self.score_frame.pack(fill="x", padx=10, pady=10)

    # Etiqueta de puntuaciones
    self.score_label = tk.Label(self.score_frame, text="Puntuación:", fg="black", font=("Helvetica", 12), anchor="w", justify="left")
    self.score_label.config(bg="white")
    self.score_label.grid(row=0, column=0, pady=5, padx=0, sticky="w")

    # Etiqueta de puntuación de la máquina
    self.green_score_label = tk.Label(self.score_frame, text="Máquina", fg="#8EEA6F", font=("Helvetica", 12), anchor="w", justify="left")
    self.green_score_label.config(bg="white")
    self.green_score_label.grid(row=0, column=1, pady=0, padx=10, sticky="w")

    # Etiqueta de puntuación del jugador
    self.red_score_label = tk.Label(self.score_frame, text="Jugador", fg="red", font=("Helvetica", 12), anchor="w", justify="left")
    self.red_score_label.config(bg="white")
    self.red_score_label.grid(row=0, column=2, pady=0, padx=10, sticky="w")

    # Crear un frame para contener los botones inferiores
    self.buttons_frame = tk.Frame(self.right_canvas, bg="white")
    self.buttons_frame.pack(side=tk.BOTTOM, fill="x", padx=10, pady=10)

    # Función del botón de inicio del algoritmo
    def start_algorithm():
      if (selected_difficulty.get() != "Seleccionar..."):
        # Bloquear el uso del botón de inicio
        start_button.config(state=tk.DISABLED)
        # Bloquear el uso del selector de dificultad
        select_difficulty.config(state=tk.DISABLED)
        # Activar el selector de movimiento
        movements_menu.config(state=tk.ACTIVE)


    # Botón para iniciar la partida
    start_button = tk.Button(self.buttons_frame, text="Iniciar", bg="#8EEA6F", fg="black", command=start_algorithm)
    start_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    start_button.config(font=('Helvetica', 12))

    # Función para reiniciar la partida
    def restart():
      start_button.config(state=tk.ACTIVE)
      select_difficulty.config(state=tk.ACTIVE)
      movements_menu.config(state=tk.DISABLED)
      selected_difficulty.set(difficulty_options[0])
      selected_movement.set(movements_options[0])
    # Botón para reiniciar la partida
    restart_button = tk.Button(self.buttons_frame, text="Reiniciar", bg="#8EEA6F", fg="black", command=restart)
    restart_button.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
    restart_button.config(font=('Helvetica', 12))

    # Crear ventana con los créditos
    def credits():
      pass

    # Botón de créditos
    credits_button = tk.Button(self.buttons_frame, text="Créditos", bg="#8EEA6F", fg="black", command=credits)
    credits_button.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
    credits_button.config(font=('Helvetica', 12))

    # Distribuir uniformemente el espacio en X entre los botones
    self.buttons_frame.columnconfigure(0, weight=1)
    self.buttons_frame.columnconfigure(1, weight=1)

    def possible_movements(orientation): # Coordenadas (Y, X)
      red_position = np.where(matriz == 4)
      green_position = np.where(matriz == 3)
      red_coordinates = list(zip(red_position[0], red_position[1]))
      green_coordinates = list(zip(green_position[0], green_position[1]))
      red_y, red_x = red_coordinates[0]
      green_y, green_x = green_coordinates[0]
      print(f"Posiciones de red: {red_coordinates}")
      #print(f"Valor Y: {red_y}")
      #print(f"Valor X: {red_x}")
      #print(f"Posiciones de green: {green_coordinates}")
      #print(f"Valor Y: {green_y}")
      #print(f"Valor X: {green_x}")
      
      # Se comprueba que sea posible el movimiento, que no esté el yoshi verde en la casilla...
      # Movimiento superior izquierdo
      if (red_y - 2 >= 0 and red_x - 1 >= 0 and (red_y - 2, red_x - 1) != (green_y, green_x) and orientation == "7"):
        print("Sup-Izq")
        matriz[red_y, red_x] = 0
        matriz[red_y - 2, red_x - 1] = 4
      # Movimiento superior derecho
      if (red_y - 2 >= 0 and red_x + 1 <= 7 and (red_y - 2, red_x + 1) != (green_y, green_x) and orientation == "9"):
        print("Sup-Der")
        matriz[red_y, red_x] = 0
        matriz[red_y - 2, red_x + 1] = 4
      # Movimiento inferior derecho
      if (red_y + 2 <= 7 and red_x + 1 <= 7 and (red_y + 2, red_x + 1) != (green_y, green_x) and orientation == "3"):
        print("Inf-Der")
        matriz[red_y, red_x] = 0
        matriz[red_y + 2, red_x + 1] = 4
      # Movimiento inferior izquierdo
      if (red_y + 2 <= 7 and red_x - 1 >= 0 and (red_y + 2, red_x - 1) != (green_y, green_x) and orientation == "1"):
        print("Inf-Izq")
        matriz[red_y, red_x] = 0
        matriz[red_y + 2, red_x - 1] = 4
    
    def on_arrow_key(event):
      # Imprimir la tecla presionada
      #print(f"Tecla presionada: {event.keysym}")
      possible_movements(event.keysym)

      app.dibujar_matriz(None)

    self.bind("<Key>", on_arrow_key)

  # Cálculo de las dimensiones que tendrá la imagen principal de Yoshi
  def resize_first_image(self, image, size):
    return ImageTk.PhotoImage(image.resize(size, Image.LANCZOS))
  
  # Manejar el evento de redimensionar el Canvas derecho y la imagen
  def right_canvas_resize(self, event):
    self.photo = self.resize_first_image(Image.open("resources/images/yoshigame.png"), (self.right_canvas.winfo_width(), round(self.right_canvas.winfo_height() * 0.4)))
    self.first_label.config(image=self.photo)

  def dibujar_matriz(self, event):

    # Eliminar dibujos anteriores
    self.canvas_matriz.delete("all")
    # Número de filas y columnas en la matriz
    rows = 8
    columns = 8
    # Tamaño de cada rectángulo en el Canvas
    rectangle_width = self.canvas_matriz.winfo_width() // columns
    rectangle_height = self.canvas_matriz.winfo_height() // rows
    print("Llamada dibujar")
    for row in range(rows):
      for column in range(columns):

        # Calcular coordenadas de la celda
        x1 = column * rectangle_width # Esquina superior izquierda 
        y1 = row * rectangle_height # Esquina superior izquierda
        x2 = x1 + rectangle_width # Esquina inferior derecha
        y2 = y1 + rectangle_height # Esquina inferior derecha
        x_center, y_center = (x1 + x2) // 2, (y1 + y2) // 2

        # Color y texto para el rectángulo
        color = "white"
        image_path = None
        if matriz[row][column] == 0: # Casilla libre
          pass
        elif matriz[row][column] == 1: # Casilla con estrella simple
          color = "#4F80BD"
          image_path = "resources/images/basic_Coin.gif"
        elif matriz[row][column] == 2: # Casilla con estrella especial
          color = "#4F80BD"
          image_path = "resources/images/star_Coin.gif"
        elif matriz[row][column] == 3: # Casilla con Yoshi verde operado por el computador
          image_path = "resources/images/yoshi_Green.png"
        elif matriz[row][column] == 4: # Casilla con Yoshi rojo operado por el jugador
          image_path = "resources/images/yoshi_Red.png"
        elif matriz[row][column] == 5: # Punto de inicio
          image_path = "resources/images/fire_truck.png"
          
          if (x1 == 0 and y1 != 0): # Posición cuando X=0 y Y!=0
            self.label_agent_icon.place(x = x1 + (rectangle_width * 0.15), y = y1 + round(y1 ** 0.35))
          elif (x1 != 0 and y1 == 0): # Posición cuando X!=0 y Y=0
            self.label_agent_icon.place(x = x1 + (rectangle_width * 0.15), y = y1 + round(rectangle_height ** 0.55))
          elif (x1 == 0 and y1 == 0): # Posición cuando X=0 y Y=0
            self.label_agent_icon.place(x=x1 + (rectangle_width * 0.15), y=y1 + round(rectangle_height ** 0.55))
          else: # Posición en cualquier otro caso
            self.label_agent_icon.place(x=x1 + round(x1 ** 0.35), y=y1 + round(y1 ** 0.35))

        # Dibujar rectángulos en el Canvas
        self.canvas_matriz.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

        if image_path:
          unique_id = str(uuid.uuid4())  # Generar un identificador único
          image = ImageTk.PhotoImage(Image.open(image_path).resize((round(rectangle_width * 0.9), round(rectangle_height * 0.9)), Image.LANCZOS))
          self.image_dict[unique_id] = image  # Almacenar la imagen en el diccionario
          self.canvas_matriz.create_image(x_center, y_center, anchor=tk.CENTER, image=image)

# Método principal
if __name__ == "__main__":
  app = mainInterface()
  app.mainloop()
  #os.system('cls') # Limpia la terminal
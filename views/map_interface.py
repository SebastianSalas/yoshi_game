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
    [3, 0, 0, 2, 2, 0, 0, 0],
    [0, 0, 0, 2, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 4, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 1, 1]])

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
    self.select_difficulty_label = tk.Label(self.right_canvas, text="Seleccione la dificultad de juego:", fg="black", font=("Helvetica", 12), anchor="w", justify="left")
    self.select_difficulty_label.config(bg="white")
    self.select_difficulty_label.pack(pady="5", padx="10", fill="x")

    # Selector de dificultad
    difficulty_options = ["Seleccionar...", "Principiante", "Intermedio", "Experto"]
    selected_difficulty = tk.StringVar(self)
    selected_difficulty.set(difficulty_options[0])
    select_difficulty = tk.OptionMenu(self.right_canvas, selected_difficulty, *difficulty_options)
    select_difficulty.pack(padx="10", fill="x")
    select_difficulty.config(font=('Helvetica', 11), bg="#8EEA6F", fg="black")

    

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
    if hasattr(self, 'label_agent_icon') and self.label_agent_icon:self.label_agent_icon.destroy()
    # Número de filas y columnas en la matriz
    rows = 8
    columns = 8
    # Tamaño de cada rectángulo en el Canvas
    rectangle_width = self.canvas_matriz.winfo_width() // columns
    rectangle_height = self.canvas_matriz.winfo_height() // rows

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
  os.system('cls') # Limpia la terminal
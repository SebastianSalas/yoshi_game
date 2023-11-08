import tkinter as tk
import numpy as np
from PIL import Image, ImageTk

class mainInterface(tk.Tk):

  global matriz

  matriz = np.array([
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 1, 0, 1, 1, 0, 1, 1],
    [0, 1, 0, 2, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 1, 1, 1],
    [5, 0, 0, 6, 4, 0, 0, 1],
    [0, 1, 1, 1, 1, 1, 0, 1],
    [3, 0, 0, 0, 2, 0, 0, 1],
    [0, 1, 0, 1, 1, 1, 1, 1]])

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

    #self.canvas_matriz.bind("<Configure>", self.dibujar_matriz)

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

  # Cálculo de las dimensiones que tendrá la imagen principal de Yoshi
  def resize_first_image(self, image, size):
    return ImageTk.PhotoImage(image.resize(size, Image.LANCZOS))
  
  # Manejar el evento de redimensionar el Canvas derecho y la imagen
  def right_canvas_resize(self, event):
    self.photo = self.resize_first_image(Image.open("resources/images/yoshigame.png"), (self.right_canvas.winfo_width(), round(self.right_canvas.winfo_height() * 0.4)))
    self.first_label.config(image=self.photo)

# Método principal
if __name__ == "__main__":
  app = mainInterface()
  app.mainloop()
  #os.system('cls') # Limpia la terminal
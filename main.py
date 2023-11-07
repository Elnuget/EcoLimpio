import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Crear la ventana principal
root = tk.Tk()
root.title("EcoLimpio: Juntos por un Mundo más Limpio")

# Cargar la imagen de fondo
background_image = Image.open("logo.jpeg")
background_photo = ImageTk.PhotoImage(background_image)

# Ajustar el tamaño de la ventana al tamaño de la imagen
root.geometry(f'{background_photo.width()}x{background_photo.height()}')

# Crear un label que tendrá la imagen de fondo
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Crear dos botones y colocarlos sobre la imagen de fondo
# Nota: Puedes ajustar los valores 'x' e 'y' según necesites para colocar los botones
button_ecosalto = tk.Button(root, text="Ecosalto", bg='white', fg='black')
button_ecosalto.place(x=50, y=250, width=120, height=30)  # Ejemplo de posición y tamaño

button_oceanopuro = tk.Button(root, text="Oceanopuro", bg='white', fg='black')
button_oceanopuro.place(x=200, y=250, width=120, height=30)  # Ejemplo de posición y tamaño

# Iniciar el bucle principal de Tkinter
root.mainloop()

import tkinter as tk
from tkinter import ttk
# Crear la ventana principal
root = tk.Tk()
root.title("EcoLimpio: Juntos por un Mundo más Limpio")

# Obtener las dimensiones de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Definir las dimensiones de la ventana
window_width = 800
window_height = 500

# Calcular la posición x e y para centrar la ventana
center_x = int((screen_width - window_width) / 2)
center_y = int((screen_height - window_height) / 2)

# Configurar la posición de la ventana en el centro de la pantalla
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# Crear un marco para contener los botones
frame = ttk.Frame(root)
frame.pack(expand=True)

# Crear dos botones dentro del marco con los textos solicitados
button_ecosalto = ttk.Button(frame, text="ecosalto")
button_ecosalto.pack(side=tk.LEFT, padx=10, pady=10)

button_oceanopuro = ttk.Button(frame, text="oceanopuro")
button_oceanopuro.pack(side=tk.RIGHT, padx=10, pady=10)

# Iniciar el bucle principal de Tkinter
root.mainloop()

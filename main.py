import tkinter as tk
from PIL import Image, ImageTk

# Crear la ventana principal
root = tk.Tk()
root.title("EcoLimpio: Juntos por un Mundo más Limpio")

# Función que inicia el juego
def start_game():
    # Crear una nueva ventana para el juego
    game_window = tk.Toplevel(root)
    game_window.title("EcoSalto")

    # Configurar el canvas del juego
    game_canvas = tk.Canvas(game_window, width=600, height=400, bg='white')
    game_canvas.pack()

    # Cargar y mostrar la imagen del dinosaurio y las bolsas de basura
    dino_image = ImageTk.PhotoImage(Image.open("dino.png"))  # Asegúrate de tener una imagen 'dino.png'
    trash_image = ImageTk.PhotoImage(Image.open("trash.png"))  # Asegúrate de tener una imagen 'trash.png'
    
    # Dibujar el dinosaurio y una bolsa de basura
    dino = game_canvas.create_image(50, 350, image=dino_image)
    trash = game_canvas.create_image(550, 350, image=trash_image)

    # Función para mover la bolsa de basura y reiniciarla una vez que salga del canvas
    def move_trash():
        game_canvas.move(trash, -10, 0)
        if game_canvas.coords(trash)[0] < 0:
            game_canvas.coords(trash, 550, 350)
        game_window.after(100, move_trash)

    move_trash()  # Iniciar el movimiento de la bolsa de basura

    # Función para hacer que el dinosaurio 'salte'
    def jump(event):
        # Coordenadas actuales del dinosaurio
        pos = game_canvas.coords(dino)
        # Comenzar salto solo si el dinosaurio está en el suelo
        if pos[1] >= 350:
            # Mover el dinosaurio hacia arriba
            game_canvas.move(dino, 0, -50)
            # Esperar un poco y luego mover el dinosaurio hacia abajo
            game_canvas.after(200, lambda: game_canvas.move(dino, 0, 50))

    game_window.bind('<space>', jump)  # Asignar la tecla Espacio para saltar

    # Mantener una referencia a las imágenes para evitar la recolección de basura
    game_canvas.images = {'dino': dino_image, 'trash': trash_image}

# Cargar la imagen de fondo y ajustar el tamaño de la ventana al tamaño de la imagen
background_image = Image.open("logo.jpeg")
background_photo = ImageTk.PhotoImage(background_image)
root.geometry(f'{background_photo.width()}x{background_photo.height()}')

# Crear un label para la imagen de fondo
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Cargar las imágenes para los botones
ecosalto_icon = ImageTk.PhotoImage(Image.open("ecosalto_button_image_resized.png"))
oceanopuro_icon = ImageTk.PhotoImage(Image.open("oceanopuro_button_image_resized.png"))

# Crear botón Ecosalto que inicia el juego y colocarlo sobre la imagen de fondo
button_ecosalto = tk.Button(root, text="Ecosalto", image=ecosalto_icon, compound="left", bg='white', fg='black', command=start_game)
button_ecosalto.place(x=50, y=250, width=120, height=30)
button_ecosalto.image = ecosalto_icon  # Mantener una referencia a la imagen

# Crear botón Oceanopuro y colocarlo sobre la imagen de fondo
button_oceanopuro = tk.Button(root, text="Oceanopuro", image=oceanopuro_icon, compound="left", bg='white', fg='black')
button_oceanopuro.place(x=200, y=250, width=120, height=30)
button_oceanopuro.image = oceanopuro_icon  # Mantener una referencia a la imagen

# Iniciar el bucle principal de Tkinter
root.mainloop()

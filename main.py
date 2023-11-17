from tkinter import *
import tkinter as tk 
from PIL import Image, ImageTk
import pygame
import math
from pygame import mixer

# Crear la ventana principal
root = tk.Tk()
root.title("EcoLimpio: Juntos por un Mundo más Limpio")

# esto remueve el botón maximizar
root.resizable(0,0)

# Obtener el ancho y alto de la pantalla
ancho_pantalla = root.winfo_screenwidth()
alto_pantalla = root.winfo_screenheight()

# Calcular las coordenadas para centrar la ventana
x_coordenada = int((ancho_pantalla - root.winfo_reqwidth()) / 2)
y_coordenada = int((alto_pantalla - root.winfo_reqheight()) / 2)

# Establecer las coordenadas de la ventana principal
root.geometry("+{}+{}".format(x_coordenada-80, y_coordenada-150))

# Antes de iniciar el juego
pygame.mixer.init()
jump_sound = pygame.mixer.Sound("jumpSound.mp3")  # Reemplaza "jump_sound.wav" con tu archivo de sonido
jump_sound.set_volume(0.5)  # Ajusta el volumen según sea necesario

# Función que inicia el juego
def start_game():
    # Inicializar Pygame antes de cualquier operación de sonido o música
    # Crear una nueva ventana para el juego
    game_window = tk.Toplevel(root)
    game_window.title("EcoSalto")
    # esto remueve el botón maximizar
    game_window.resizable(0,0)

    # Establecer las coordenadas de la ventana principal
    game_window.geometry("+{}+{}".format(x_coordenada-200, y_coordenada-150))

    # Configurar el canvas del juego
    game_canvas = tk.Canvas(game_window, width=600, height=400)
    game_canvas.pack()
  
     # Añadir fondo
    background_image_jump = ImageTk.PhotoImage(
        Image.open("paisaje.png").resize((1200, 400))
    )
    
    background = game_canvas.create_image(300, 200, image=background_image_jump)
    # Cargar y mostrar la imagen del dinosaurio y las bolsas de basura
    dino_image = ImageTk.PhotoImage(
        Image.open("dino-BEST.png")
    )  # Asegúrate de tener una imagen 'dino.png'
    trash_image = ImageTk.PhotoImage(
        Image.open("trash-BEST.png")
    )  # Asegúrate de tener una imagen 'trash.png'

    # Cargar la imagen de la bolsa de basura y ajustar su tamaño
    trash_original_image = Image.open("trash-BEST.png")
    trash_resized_image = trash_original_image.resize((50, 50))
    trash_image = ImageTk.PhotoImage(trash_resized_image)
    
    # Dibujar el dinosaurio y una bolsa de basura
    dino = game_canvas.create_image(65, 350, image=dino_image)
    trash = game_canvas.create_image(550, 365, image=trash_image)
    # Inicializar Pygame antes de cualquier operación de sonido o música
    pygame.mixer.init()
    # Iniciar la música del nivel del juego
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.load("forest.mp3")
    pygame.mixer.music.play(loops=-1) 
    # Variable de estado del juego
    global game_progress
    game_progress = False
    
    # Etiqueta para el mensaje de inicio
    
    global message_start
    global message_end
    global message_reset
    message_start = game_canvas.create_text(300, 200, text="Presiona la barra espaciadora para iniciar el juego",font=("Arial", 12, "bold"), fill="black", )

    #etiqueta puntaje
    #message_score = game_canvas.create_text(200, 50, text="MR.CHANGO ",font=("Arial", 12, "bold"), fill="black", )
    message_score = game_canvas.create_text(50, 50, text="Puntaje: ",font=("Arial", 12, "bold"), fill="black", )
    global score
    score = 0
    global text_score
    text_score = game_canvas.create_text(100, 50, text=score,font=("Arial", 12, "bold"), fill="black", )
    message_score = game_canvas.create_text(50, 50, text="Puntaje: ",font=("Arial", 12, "bold"), fill="black", )
    #Highscore
    global high_score
    high_score = 0
    global texth_score
    texth_score = game_canvas.create_text(500, 50, text=high_score,font=("Arial", 12, "bold"), fill="black", )
    message_score = game_canvas.create_text(400, 50, text="Maximo Puntaje: ",font=("Arial", 12, "bold"), fill="black", )
    global distance
    def hay_colision(x_1, y_1, x_2, y_2):
        global distance
        distance = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
        #Hitbox de la basura
        if distance <  39:
            return True
        else:
            return False
        
   
            
            
        
    # Función para mover la bolsa de basura y reiniciarla una vez que salga del canvas
    
    def move_trash():
        global game_progress
        game_canvas.move(trash, -10, 0)
        if game_canvas.coords(trash)[0] < 0:
            game_canvas.coords(trash, 550, 365)
            global score
            score = score + 1
            global text_score
            game_canvas.delete(text_score)
            text_score = game_canvas.create_text(100, 50, text=score,font=("Arial", 12, "bold"), fill="black", )
        if game_canvas.coords(trash)[0] < 0:
            game_canvas.coords(trash, 550, 365)
            global high_score
            high_score = high_score + 1
            global texth_score
            game_canvas.itemconfig(text_score)
        if game_progress:
            game_canvas.delete(message_start)
            game_window.after(30, move_trash)
        #funcion high
             # Coordenadas actuales del dinosaurio
            dino_pos = game_canvas.coords(dino)
            # Coordenadas actuales de la bolsa de basura
            trash_pos = game_canvas.coords(trash)  
            
             # Verificar colisión al inicio del salto
            colision = hay_colision(dino_pos[0], dino_pos[1], trash_pos[0], trash_pos[1])
            
            if colision:
                game_progress = False
                
                global message_end, message_reset
                message_end = game_canvas.create_text(300, 200, text="Game Over",font=("Helvetica", 24), fill="red" )
                message_reset = game_canvas.create_text(300, 230, text="(Presiona la barra espaciadora para reiniciar el juego)",font=("Arial", 12, "bold"), fill="black", )
                # Esperar a que el jugador presione la barra espaciadora para reiniciar
                game_window.bind("<space>", reset_game)
                
    def jump(event):
        global game_progress
        if not game_progress:
                game_progress = True
                move_trash()  # Iniciar el movimiento de la bolsa de basura
                
        # Coordenadas actuales del dinosaurio
        pos = game_canvas.coords(dino)
        
        # Comenzar salto solo si el dinosaurio está en el suelo
        if pos[1] >= 350:
            #Sonido de salto
            jump_sound.play()
            # Mover el dinosaurio hacia arriba de manera gradual
            for i in range(10):
                game_canvas.move(dino, 0, -20)
                game_canvas.update()
                game_canvas.after(12)
            
            # Esperar un poco antes de bajar
            game_canvas.after(100, lambda: down())
            

    def down():
        # Mover el dinosaurio hacia abajo de manera gradual
        for i in range(10):
            game_canvas.move(dino, 0, 20)
            game_canvas.update()
            game_canvas.after(20)
    #funciona reset todo
    def reset_game(event):
        global game_progress, score,message_start
        #detener musica
        pygame.mixer.music.stop()

        score = 0
        # Reiniciar posición del dinosaurio
        game_canvas.coords(dino, 65, 350)
        # Reiniciar posición de la bolsa de basura
        game_canvas.coords(trash, 550, 365)
        message_start = game_canvas.create_text(300, 200, text="Presiona la barra espaciadora para iniciar el juego",font=("Arial", 12, "bold"), fill="black", )
        game_window.bind("<space>", jump)
        game_canvas.delete(message_end)
        game_canvas.delete(message_reset)
         # Reiniciar puntaje
        game_canvas.itemconfig(text_score, text=score)
        game_canvas.itemconfig(texth_score, text=high_score)
         # Iniciar la música del nivel del juego
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.load("forest.mp3")
        pygame.mixer.music.play(loops=-1)

    # Asignar la tecla Espacio para saltar e iniciar
    
    game_window.bind("<space>", jump)  
    
    # Mantener una referencia a las imágenes para evitar la recolección de basura
    background.images = {"dino": dino_image, "trash": trash_image}

     

# Cargar la imagen de fondo y ajustar el tamaño de la ventana al tamaño de la imagen
background_image = Image.open("logo.jpeg")
background_photo = ImageTk.PhotoImage(background_image)
root.geometry(f"{background_photo.width()}x{background_photo.height()}")

# Crear un label para la imagen de fondo
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Cargar las imágenes para los botones
ecosalto_icon = ImageTk.PhotoImage(Image.open("ecosalto_button_image_resized.png"))
oceanopuro_icon = ImageTk.PhotoImage(Image.open("oceanopuro_button_image_resized.png"))

# Crear botón Ecosalto que inicia el juego y colocarlo sobre la imagen de fondo
button_ecosalto = tk.Button(
    root,
    text="Ecosalto",
    image=ecosalto_icon,
    compound="left",
    bg="white",
    fg="black",
    command=start_game,
)
button_ecosalto.place(x=50, y=250, width=120, height=30)
button_ecosalto.image = ecosalto_icon  # Mantener una referencia a la imagen

# Crear botón Oceanopuro y colocarlo sobre la imagen de fondo
button_oceanopuro = tk.Button(
    root,
    text="Oceanopuro",
    image=oceanopuro_icon,
    compound="left",
    bg="white",
    fg="black",
)
button_oceanopuro.place(x=200, y=250, width=120, height=30)
button_oceanopuro.image = oceanopuro_icon  # Mantener una referencia a la imagen

# Iniciar el bucle principal de Tkinter
root.mainloop()
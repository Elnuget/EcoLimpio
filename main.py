from tkinter import *
import tkinter as tk 
from PIL import Image, ImageTk
import pygame
import math
from pygame import mixer
import random

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
pygame.mixer.music.stop() 


def play_music(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    

    
# Función que inicia el juego
def start_game():
    # Iniciar la música del nivel del juego
    play_music("forest.mp3")
    
    # Crear una nueva ventana para el juego
    game_window = tk.Toplevel(root)
    game_window.title("EcoSalto")
    # esto remueve el botón maximizar
    game_window.resizable(0,0)

    # Establecer las coordenadas de la ventana principal
    game_window.geometry("+{}+{}".format(x_coordenada-200, y_coordenada-150))

    #focus a la pantalla
    game_window.focus_set()
    # Configurar el canvas del juego
    game_canvas = tk.Canvas(game_window, width=600, height=400)
    game_canvas.pack()
    
   
    
    def close_window():
            game_window.destroy()
            play_music("Forest.mp3")       

    # Configurar el evento para cerrar la ventana
    game_window.protocol("WM_DELETE_WINDOW", close_window)
    
     # Añadir fondo
    background_image_jump = ImageTk.PhotoImage(
        Image.open("paisaje.png").resize((650, 450))
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
    
    
    
    # Cargar la imagen de la bolsa de basura y ajustar su tamaño
    dino_original_image = Image.open("dino-BEST.png")
    dino_resized_image = dino_original_image.resize((70, 100))
    dino_image = ImageTk.PhotoImage(dino_resized_image)
    
    # Dibujar el dinosaurio y una bolsa de basura
    dino = game_canvas.create_image(65, 350, image=dino_image)
    trash = game_canvas.create_image(550, 365, image=trash_image)

    # Variable de estado del juego
    global game_progress,message_start,message_end,message_reset
    game_progress = False
    
    # Etiqueta para el mensaje de inicio
    message_start = game_canvas.create_text(300, 200, text="Presiona la barra espaciadora para iniciar el juego",font=("Arial", 12, "bold"), fill="black", )
    #etiqueta puntaje
    message_score = game_canvas.create_text(50, 50, text="Puntaje: ",font=("Arial", 12, "bold"), fill="black", )
    global score
    score = 0
    global text_score
    text_score = game_canvas.create_text(100, 50, text=score,font=("Arial", 12, "bold"), fill="black", )
    global distance
    
    def hay_colision(x_1, y_1, x_2, y_2):
        global distance
        distance = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
        if distance < 60:
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
            score = score+1
            global text_score
            game_canvas.delete(text_score)
            text_score = game_canvas.create_text(100, 50, text=score,font=("Arial", 12, "bold"), fill="black", )
        if game_progress:
            game_canvas.delete(message_start)
            game_window.after(30, move_trash)
             # Coordenadas actuales del dinosaurio
            dino_pos = game_canvas.coords(dino)
            # Coordenadas actuales de la bolsa de basura
            trash_pos = game_canvas.coords(trash)  
            
             # Verificar colisión al inicio del salto
            colision = hay_colision(dino_pos[0], dino_pos[1], trash_pos[0], trash_pos[1])
            
            if colision:
                game_progress = False
                
                global message_end, message_reset
                message_end = game_canvas.create_text(300, 200, text="Fin del juego",font=("Arial", 12, "bold"), fill="black" )
                message_reset = game_canvas.create_text(300, 230, text="(Presiona la barra espaciadora para reiniciar el juego)",font=("Arial", 12, "bold"), fill="black", )
                # Esperar a que el jugador presione la barra espaciadora para reiniciar
                game_window.bind("<space>", reset_game)
                
    def jump(event):
        jump_sound = pygame.mixer.Sound("jumpSound.mp3")  # Reemplaza "jump_sound.wav" con tu archivo de sonido
        jump_sound.set_volume(0.5)  # Ajusta el volumen según sea necesario
        jump_sound.play()
        global game_progress
        if not game_progress:
                game_progress = True
                move_trash()  # Iniciar el movimiento de la bolsa de basura
                
        # Coordenadas actuales del dinosaurio
        pos = game_canvas.coords(dino)
        
        # Comenzar salto solo si el dinosaurio está en el suelo
        if pos[1] >= 350:
            # Mover el dinosaurio hacia arriba de manera gradual
            for i in range(10):
                game_canvas.move(dino, 0, -20)
                game_canvas.update()
                game_canvas.after(20)
            
            # Esperar un poco antes de bajar
            game_canvas.after(100, lambda: down())
            

    def down():
        # Mover el dinosaurio hacia abajo de manera gradual
        for i in range(10):
            game_canvas.move(dino, 0, 20)
            game_canvas.update()
            game_canvas.after(30)
       
    #funciona resetear todo
    def reset_game(event):
        global game_progress, score,message_start
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

    # Asignar la tecla Espacio para saltar e iniciar
    
    game_window.bind("<space>", jump)  
    
    # Mantener una referencia a las imágenes para evitar la recolección de basura
    background.images = {"dino": dino_image, "trash": trash_image}


#JUEGO DEL MAR#####################################################

def start_game2(): 
    # Iniciar la música del nivel del juego
    play_music("mar.mp3")
    # Crear una nueva ventana para el juego
    game_window = tk.Toplevel(root)
    game_window.title("OceanoPuro")
    # esto remueve el botón maximizar
    game_window.resizable(0,0)
    
    def close_window():
        game_window.destroy()
        play_music("mar.mp3")       

    # Configurar el evento para cerrar la ventana
    game_window.protocol("WM_DELETE_WINDOW", close_window)


    # Establecer las coordenadas de la ventana principal
    game_window.geometry("+{}+{}".format(x_coordenada-200, y_coordenada-150))

    #focus a la pantalla
    game_window.focus_set()
    
    # Configurar el canvas del juego
    game_canvas = tk.Canvas(game_window, width=600, height=400)
    game_canvas.pack()
  
     # Añadir fondo
    background_image_jump = ImageTk.PhotoImage(
        Image.open("mar.jpg").resize((650, 400))
    )
    
    #crear fondo
    background = game_canvas.create_image(300, 200, image=background_image_jump)
    
    
    global fish_original_image,fish_resized_image,fish_image
    # Cargar y mostrar la imagen del dinosaurio y las bolsas de basura
    fish_image = ImageTk.PhotoImage(
        Image.open("pez.png")
    )  # Asegúrate de tener una imagen 'dino.png'
    trash_image = ImageTk.PhotoImage(
        Image.open("trash-BEST.png")
    )  # Asegúrate de tener una imagen 'trash.png'
    
    # Cargar la imagen de la bolsa de basura y ajustar su tamaño
    trash_original_image = Image.open("trash-BEST.png")
    trash_resized_image = trash_original_image.resize((50, 50))
    trash_image = ImageTk.PhotoImage(trash_resized_image)
   
     # Cargar la imagen de la pez de basura y ajustar su tamaño
    fish_original_image = Image.open("pez.png")
    fish_resized_image = fish_original_image.resize((100, 100))
    fish_image = ImageTk.PhotoImage(fish_resized_image)
    
    
    # Cargar las imágenes por adelantado
    fish_images = {
        "Up": ImageTk.PhotoImage(Image.open("pez4.png").resize((100, 100))),
        "Down": ImageTk.PhotoImage(Image.open("pez2.png").resize((100, 100))),
        "Left": ImageTk.PhotoImage(Image.open("pez3.png").resize((100, 100))),
        "Right": ImageTk.PhotoImage(Image.open("pez.png").resize((100, 100)))
    }
    
    # Cambiar la posición de la basura de forma aleatoria dentro de los bordes
    trash_x = random.randint(0, 600 - 100)
    trash_y = random.randint(0, 400 - 100)
    
    # Dibujar el dinosaurio y una bolsa de basura
    global fish,trash,game_progress,message_start,message_end,message_reset,score,text_score,distance,reset_fish
    fish = game_canvas.create_image(65, 350, image=fish_images["Right"])
    trash = game_canvas.create_image(trash_x, trash_y, image=trash_image)
    
    ##boolean o estado de juego
    game_progress = False
    reset_fish = True
    
    # Etiqueta para el mensaje de inicio
    message_reset = game_canvas.create_text(300, 20, text="Presiona las ESC para reiniciar el juego",font=("Arial", 12, "bold"), fill="black", )
    message_start = game_canvas.create_text(300, 200, text="Presiona las flechas para iniciar el juego",font=("Arial", 12, "bold"), fill="black", )

    #etiqueta puntaje
    message_score = game_canvas.create_text(50, 50, text="Puntaje: ",font=("Arial", 12, "bold"), fill="black", )
    score = 0
    text_score = game_canvas.create_text(100, 50, text=score,font=("Arial", 12, "bold"), fill="black", )
    
    def pos_trash():
        global trash
         # Eliminar la bolsa de basura anterior
        game_canvas.delete(trash)

        # Cambiar la posición de la basura de forma aleatoria dentro de los bordes
        trash_x = random.randint(20, 600 - 120)
        trash_y = random.randint(20, 400 - 120)
        
        # Dibujar el dinosaurio y una bolsa de basura
        trash = game_canvas.create_image(trash_x, trash_y, image=trash_image)
    
    def hay_colision(x_1, y_1, x_2, y_2):
        global distance
        distance = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
        if distance < 60:
            return True
        else:
            return False        
    
    global direccion_x_trash,direccion_y_trash,velocidad_trash,factor_tiempo_trash
    direccion_x_trash = -1
    direccion_y_trash = -1
    velocidad_trash = 5
    factor_tiempo_trash = 0.4
    # Función para mover la basura
    def move_trash():
        global game_progress, score,text_score,trash,direccion_x_trash,direccion_y_trash,velocidad_trash,factor_tiempo_trash
        if game_progress:
            game_canvas.delete(message_start)
            game_window.after(30, move_trash)
            
            # Coordenadas actuales de la basura
            trash_pos = game_canvas.coords(trash)
            
            # Dirección actual de la basura (inicialmente hacia la derecha)
            # Dirección aleatoria solo cuando la basura toca el borde
            if trash_pos[1] - 40 <= 0 or trash_pos[1] + 40 >= 400 or trash_pos[0] - 60 <= 0 or trash_pos[0] + 40 >= 600:
                opciones = [(1, 0), (-1, 0), (-1, -1),(1, 1)]
                direccion_x_trash, direccion_y_trash = random.choice(opciones)

            # Mover la basura en la dirección actual
            game_canvas.coords(trash, trash_pos[0] + direccion_x_trash * velocidad_trash * factor_tiempo_trash, trash_pos[1] + direccion_y_trash * velocidad_trash * factor_tiempo_trash)
            
            # Coordenadas actuales del pez
            fish_pos = game_canvas.coords(fish)

            # Verificar colisión al inicio del salto
            colision = hay_colision(fish_pos[0], fish_pos[1], trash_pos[0], trash_pos[1])

            if colision:
                eat = pygame.mixer.Sound("comer.mp3") 
                eat.set_volume(0.5)  # Ajusta el volumen según sea necesario
                eat.play()
                game_progress = False
                score = score+1
                game_canvas.delete(text_score)
                text_score = game_canvas.create_text(100, 50, text=score,font=("Arial", 12, "bold"), fill="black")
                pos_trash()

    #funcion mover fish          
    def move_fish(event):
        
        global current_fish_image,fish,game_progress,reset_fish
        
        if not game_progress:
                game_progress = True
                move_trash()  # Iniciar el movimiento de la bolsa de basura
               
        # Coordenadas actuales del dinosaurio
        pos = game_canvas.coords(fish)
        
        # Definir la velocidad del movimiento y el factor de tiempo
        velocidad = 1
        factor_tiempo = 0.1  # Puedes ajustar este valor según sea necesario

        # Inicializar la dirección del movimiento
        direccion_x = 0
        direccion_y = 0
         
        # Verificar qué tecla de flecha se presionó y actualizar la dirección del movimiento
        if event.keysym in {"Up", "w"}:
            if pos[1] - 40 >= 0:
                direccion_y = -20
                direccion_x = 0
                current_fish_image = fish_images["Right"]
        elif event.keysym in {"Down", "s"}:
            if pos[1] + 40 <= 400: 
                direccion_y = 20
                direccion_x = 0
                current_fish_image = fish_images["Right"]
        elif event.keysym in {"Left", "a"}:
             if pos[0] - 60 >= 0:
                direccion_x = -20
                direccion_y = 0
                current_fish_image = fish_images["Left"]
        elif event.keysym in {"Right", "d"}:
              if pos[0] + 40 <= 600:
                 direccion_x = 20
                 direccion_y = 0
                 current_fish_image = fish_images["Right"]
        

         # Cambiar la imagen del pez sin recrear el objeto en el lienzo
        game_canvas.itemconfig(fish, image=current_fish_image)
        
         # Mover el pez solo si el juego está en progreso
        if game_progress and reset_fish:
            # Mover el dinosaurio en la dirección actual con la velocidad ajustada por el factor de tiempo
            game_canvas.coords(fish, pos[0] + direccion_x * velocidad * factor_tiempo, pos[1] + direccion_y * velocidad * factor_tiempo)
            # movimiento o recorrido fluido que vaya seguido
            game_canvas.after(5, lambda: move_fish(event))
            
          
    #funciona resetear todo
    def reset_game(event):
        global game_progress, score, text_score, message_start, message_reset,reset_fish
        # Detener el movimiento del pez
        game_progress = False
        reset_fish = False
        # Reiniciar posición del pez
        game_canvas.coords(fish, 65, 350)
    
        # Reiniciar posición de la basura
        pos_trash()

        # Reiniciar puntaje
        score = 0
        game_canvas.itemconfig(text_score, text=score)

        # Mostrar el mensaje de inicio
        message_start = game_canvas.create_text(300, 200, text="Presiona las flechas para iniciar el juego", font=("Arial", 12, "bold"), fill="black")
       
        game_canvas.after(5, lambda: resetFish(event))

     
    def resetFish(event):
        global reset_fish
        reset_fish = True   
        

    # Asociar la función move_fish con el evento de tecla
    game_canvas.focus_set()
    
    game_canvas.bind("<Up>", move_fish)
    game_canvas.bind("<Down>", move_fish)
    game_canvas.bind("<Left>", move_fish)
    game_canvas.bind("<Right>", move_fish)
    
    
    game_canvas.bind("<w>", move_fish)
    game_canvas.bind("<s>", move_fish)
    game_canvas.bind("<a>", move_fish)
    game_canvas.bind("<d>", move_fish)
    
    #salir juego 
    game_canvas.bind("<Escape>", reset_game)
    # Mantener una referencia a las imágenes para evitar la recolección de basura
    background.images = {"fish": fish_image, "trash": trash_image}

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
    command=start_game2,
)
button_oceanopuro.place(x=200, y=250, width=120, height=30)
button_oceanopuro.image = oceanopuro_icon  # Mantener una referencia a la imagen

play_music("forest.mp3")

# Iniciar el bucle principal de Tkinter
root.mainloop()

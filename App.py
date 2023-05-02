import pygame
import sys
import math
import time
import random

pygame.init()
pygame.font.init()
pygame.mixer.init()

"""
Variables and configurations. 
"""
Button_High = 30  # Button to start de Game 
Image_Size = 200  # Image size in pixeles

# behind the card
memory_Image = "pictures/Memory.png"
hidding_Image = pygame.image.load(memory_Image)
Show_Image = 2  # Seconds to Hide Image

#The class represents the square. 
class Square:
    def __init__(self, image_source):
        self.show = True
        self.uncovered = False
        self.image_source = image_source
        self.imagen_real = pygame.image.load(image_source)

#Images 
squares = [
    [Square("pictures/Bombona.png"), Square("pictures/Bombona.png"),
        Square("pictures/Eric-kaa.png"), Square("pictures/Eric-kaa.png")],
    [Square("pictures/Fache.png"), Square("pictures/Fache.png"),
        Square("pictures/Gentle-Miasma.png"), Square("pictures/Gentle-Miasma.png")],
    [Square("pictures/Joi-Wu.png"), Square("pictures/Joi-Wu.png"),
        Square("pictures/Kim-Rey.png"), Square("pictures/Kim-Rey.png")],
    [Square("pictures/Mari-Pee.png"), Square("pictures/Mari-Pee.png"),
        Square("pictures/Regina.png"), Square("pictures/Regina.png")],
]

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
grey = (206, 206, 206)
blue = (30, 136, 229)

# screen size
screen_width = len(squares[0]) * Image_Size
screen_height = (len(squares) * Image_Size) + Button_High + 105
button_width = screen_width

# Font on the button
font_size = 20
fuente = pygame.font.SysFont("Arial", font_size)
font_title_game = pygame.font.SysFont("Arial", 28)
xFont = int((button_width / 2) - (font_size / 2))
yFont = int(screen_height - Button_High)

button = pygame.Rect(0, screen_height - Button_High,
    button_width, screen_height)

last_Seconds = None
play = True  
start_game = False

x1 = None
y1 = None

x2 = None
y2 = None

# Hide all the squares
def hide_All_Squares():
    for row in squares:
        for square in row:
            square.show = False
            square.uncovered = False

def random_squares():
    # Choose random X and Y, swap them.
    rows_quantity = len(squares)
    columns_quantity = len(squares[0])
    for y in range(rows_quantity):
        for x in range(columns_quantity):
            x_random = random.randint(0, columns_quantity - 1)
            y_random = random.randint(0, rows_quantity - 1)
            temporal_square = squares[y][x]
            squares[y][x] = squares[y_random][x_random]
            squares[y_random][x_random] = temporal_square

def check_Win():
    if win():
        restart_game()

# Back false in case one of the squares is uncovered, and true when all the squares are uncovered.
def win():
    for row in squares:
        for square in row:
            if not square.uncovered:
                return False
    return True

def restart_game():
    global start_game
    start_game = False

def start_game_flag():
    global start_game
    for i in range(3):
        random_squares()
    hide_All_Squares()
    start_game = True

# set up the screen and write a title.
game_screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Memory Game')

#text_surface = fuente.render("¡Hola, mundo!", True, (0, 0, 0))

while True:
    # Listen to the Enevts, they repeat a few times per second.
    for event in pygame.event.get():
        # If the exit to the game, they quit.
        if event.type == pygame.QUIT:
            sys.exit()
        # If they did Click, they can play.
        elif event.type == pygame.MOUSEBUTTONDOWN and play:
            """
            xAbsolute and yAbsolute are the coordinates of the screen 
            where the click was made. 
            """
            xAbsolute, yAbsolute = event.pos
            print(yAbsolute)
            if button.collidepoint(event.pos):
                if not start_game:
                    start_game_flag()
            else:
                if not start_game:
                    continue
                x = math.floor(xAbsolute / Image_Size)
                y = math.floor((yAbsolute - 100) / Image_Size) 
                print(y)
                # If the square is uncover, we don't do anything. 
                square = squares[y][x]
                if square.show or square.uncovered:
                    continue
                if x1 is None and y1 is None:
                    x1 = x
                    y1 = y
                    squares[y1][x1].show = True
                else:
                    x2 = x
                    y2 = y
                    squares[y2][x2].show = True
                    square1 = squares[y1][x1]
                    square2 = squares[y2][x2]
                    # If both of the squares are the same.
                    if square1.image_source == square2.image_source:
                        squares[y1][x1].uncovered = True
                        squares[y2][x2].uncovered = True
                        x1 = None
                        x2 = None
                        y1 = None
                        y2 = None
                    else:
                        # If they don't match, we have to hide them
                        last_Seconds = int(time.time())
                        play = False
                check_Win()
    now = int(time.time())
    if last_Seconds is not None and now - last_Seconds >= Show_Image:
        squares[y1][x1].show = False
        squares[y2][x2].show = False
        x1 = None
        y1 = None
        x2 = None
        y2 = None
        last_Seconds = None
        # At this point the user can do click, because the Image are cover. 
        play = True
    # White Screen 
    game_screen.fill(white)

    x = 0
    y = 100
    # Go thru the Squares
    for row in squares:
        x = 0
        for square in row:
            if square.uncovered or square.show:
                game_screen.blit(square.imagen_real, (x, y))
            else:
                game_screen.blit(hidding_Image, (x, y))
            x += Image_Size
        y += Image_Size

    #Title
    game_screen.blit(font_title_game.render(
        "Grace-Hopper Pets", True, black), (320, 30))
    
    # Draw the button
    if start_game:
        pygame.draw.rect(game_screen, white, button)
        game_screen.blit(fuente.render(
            "Start Game", True, grey), (xFont, yFont))
    else:
        pygame.draw.rect(game_screen, blue, button)
        game_screen.blit(fuente.render(
            "Start Game", True, white), (xFont, yFont))

    # Update display
    pygame.display.update()
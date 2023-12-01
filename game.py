"""
Tommy Ju
A01347715

Matthew
A01373290
"""
from make_character import make_character
from make_board import make_board
from get_user_choice import get_user_choice
from move_character import move_character
from describe_current_location import describe_current_location
# GUI Modules
import tkinter as tk
from PIL import Image, ImageTk
from get_user_interface_data import get_user_interface_data
from user_interface import user_interface
from make_enemy import make_enemy
import threading




def game():



    rows = 10
    columns = 10
    end_point = (4, 4)
    board = make_board(rows, columns)
    character = make_character()
    enemies = make_enemy(board)
    achieved_goal = True
    # GUI

    GUI_HEIGHT = 600
    GUI_WIDTH = 1000
    CELL_SIZE = 50

    # Configure the root window
    root = tk.Tk()
    root.title("RPS Ninja")
    root.geometry(f"{GUI_WIDTH}x{GUI_HEIGHT}")
    root.configure(background='black')
    # Root window comprised of 2 vertical columns for map and information
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=2)

    canvas = tk.Canvas(root)
    canvas.grid(row=0, column=0, sticky="nsew")

    # Configure a grid and add data to cells
    for row in range(rows):
        # Configure even rows
        canvas.grid_rowconfigure(row, minsize=CELL_SIZE)
        for column in range(columns):
            # Configure even columns
            canvas.grid_columnconfigure(column, minsize=CELL_SIZE)
            # Add the frame container widget to each cell to create border effect
            frame = tk.Frame(canvas, background="green", borderwidth=3, relief="raised")
            frame.grid(row=row, column=column, sticky="nsew", padx=2, pady=2)

    # Images
    global ninja_image
    ninja_image_file = Image.open("./assets/ninja.png")
    ninja_image = ImageTk.PhotoImage(ninja_image_file.resize((30, 30)))
    level_one_image_file = Image.open("./assets/forest_level_background.jpeg")
    level_one_image = ImageTk.PhotoImage(level_one_image_file.resize((2000, 2000)))

    #widgets
    all_game_widgets = []
    ninja_widget = tk.Label(canvas, image=ninja_image, background="white")
    all_game_widgets.append(ninja_widget)
    for index in range(len(enemies)):
        enemy_widget = tk.Label(canvas, image=ninja_image, background="white")
        all_game_widgets.append(enemy_widget)

    # Initial game board update
    data = get_user_interface_data(character, end_point, [(2, 2), (1, 1)])
    update_widgets(data, canvas, level_one_image, enemies, all_game_widgets)


    # Add background image to canvas
    canvas.create_image(0, 0, image=level_one_image)
    # Create a separate thread for the game loop
    threading.Thread(target=game_instance, args=(character, achieved_goal, board, end_point, canvas, level_one_image, enemies, all_game_widgets)).start()
    root.mainloop()


def game_instance(character, achieved_goal, board, end_point, canvas, level_one_image, enemies, all_game_widgets):
    while achieved_goal:
        direction = get_user_choice()
        move_character(character, direction)
        describe_current_location(board, character)
        data = get_user_interface_data(character, end_point, [(2, 2), (1, 1)])
        update_widgets(data, canvas, level_one_image, enemies, all_game_widgets)


def update_widgets(user_interface_data, canvas, level_one_image, enemies, all_game_widgets):
    canvas.create_image(0, 0, image=level_one_image)
    all_game_widgets[0].grid(row=user_interface_data["character"][1], column=user_interface_data["character"][0])
    for index in range(len(enemies)):
        all_game_widgets[index + 1].grid(row=enemies[index][1], column=enemies[index][0])


def main():
    game()


if __name__ == "__main__":
    main()

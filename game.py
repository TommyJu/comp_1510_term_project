"""
Tommy Ju
A01347715

Matthew
A01373290
"""
# Modules created by Matthew and Tommy
from character.make_character import make_character
from map.make_board import make_board
from movement.get_user_choice import get_user_choice
from movement.move_character import move_character
from map.describe_current_location import describe_current_location
from map.get_user_interface_data import get_user_interface_data
from enemy.make_enemy import make_enemy
from movement.enemies_move import enemies_move
from enemy.make_vision_cones import make_vision_cones
from enemy.enemy_detection import enemy_detection
from enemy.delete_enemy import delete_enemy
from combat.engage_combat import engage_combat
from map.check_if_endpoint_reached import check_if_endpoint_reached
from character.is_alive import is_alive
from movement.validate_move import validate_move
from combat.get_choice_combat import get_choice_combat

import sys
import io

# GUI Modules
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


def main():
    rows = 10
    columns = 10
    end_point = (9, 9)
    board = make_board(rows, columns)
    character = make_character()
    enemies = make_enemy(board)
    vision_cones = make_vision_cones(enemies, board)
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

    # The column on the right will have 9 rows for each widget
    canvas_right = tk.Canvas(root, bg="black")
    canvas_right.grid(row=0, column=1, sticky="nsew")
    canvas_right.grid_columnconfigure(0)
    for row in range(9):
        canvas_right.grid_rowconfigure(row)

    title_widget = tk.Label(canvas_right, text="RPS NINJA", background="white", fg="white", bg="black", font="40")
    title_widget.grid(row=0, column=0, sticky="nsew")
    title_widget.configure(font=("system", 32))

    level_widget = tk.Label(canvas_right, text="LEVEL 1", background="white", fg="white", bg="black")
    level_widget.grid(row=1, column=0, sticky="nsew")
    level_widget.configure(font=("system", 24))

    health_text_widget = tk.Label(canvas_right, text="Current HP:", background="white", fg="white", bg="black")
    health_text_widget.grid(row=2, column=0, sticky="nsew")
    health_text_widget.configure(font=("system", 12))

    health_widget = ttk.Progressbar(canvas_right, length=200)
    health_widget["value"] = 100
    health_widget.grid(row=3, column=1, sticky="nsew")

    stat_widget = tk.Label(canvas_right, text="PLAYER ACTION: 10", background="white", fg="white", bg="black")
    stat_widget.grid(row=4, column=0, sticky="nsew")
    stat_widget.configure(font=("system", 12))

    # output_string_variable = tk.StringVar()
    # output_widget = tk.Label(canvas_right, textvariable=output_string_variable, background="white", fg="white", bg="black")
    output_widget = tk.Text(canvas_right, background="black", foreground="white")
    output_widget.grid(row=5, column=0, sticky="nsew")
    output_widget.configure(font=("system", 12))

    scroll_widget = tk.Scrollbar(canvas_right, command=output_widget.yview)
    scroll_widget.grid(row=6, column=0, sticky="nsew")
    output_widget["yscrollcommand"] = scroll_widget.set

    input_widget_value = tk.StringVar()
    input_widget = ttk.Entry(canvas_right, textvariable=input_widget_value)
    input_widget.grid(row=7, column=0, sticky="nsew")


    # Images
    ninja_image_file = Image.open("./assets/ninja-heroic-stance.png")
    ninja_image = ImageTk.PhotoImage(ninja_image_file.resize((30, 30)))
    enemy_image_file = Image.open("./assets/oni.png")
    enemy_image = ImageTk.PhotoImage(enemy_image_file.resize((30, 30)))
    vision_cone_image_file = Image.open("./assets/eye-target.png")
    vision_cone_image = ImageTk.PhotoImage(vision_cone_image_file.resize((30, 30)))
    level_one_image_file = Image.open("./assets/forest_level_background.jpeg")
    level_one_image = ImageTk.PhotoImage(level_one_image_file.resize((2000, 2000)))
    end_point_image_file = Image.open("./assets/exit-door.png")
    end_point_image = ImageTk.PhotoImage(end_point_image_file.resize((30, 30)))

    # game board widgets
    ninja_widget = tk.Label(canvas, image=ninja_image, background="white")
    enemy_widgets = []
    vision_cone_widgets = []
    end_point_widget = tk.Label(canvas, image=end_point_image, background="white")
    end_point_widget.grid(row=end_point[0], column=end_point[1])

    # Create widget lists
    for index in range(len(enemies)):
        enemy_widget = tk.Label(canvas, image=enemy_image, background="white")
        enemy_widget.lift()
        enemy_widgets.append(enemy_widget)
    for index in range(len(vision_cones)):
        vision_cone_widget = tk.Label(canvas, image=vision_cone_image, background="white")
        vision_cone_widgets.append(vision_cone_widget)

    # Initial game board update
    data = get_user_interface_data(character, end_point, [(2, 2), (1, 1)])
    # Add background image to canvas
    canvas.create_image(0, 0, image=level_one_image)

    def update_widgets(user_interface_data):
        canvas.create_image(0, 0, image=level_one_image)
        ninja_widget.grid(row=user_interface_data["character"][1], column=user_interface_data["character"][0])
        for index in range(len(vision_cones)):
            if vision_cones[index] == None:
                vision_cone_widgets[index].grid_forget()
            else:
                vision_cone_widgets[index].grid(row=vision_cones[index][1], column=vision_cones[index][0])
        for index in range(len(enemies)):
            enemy_widgets[index].grid(row=enemies[index][1], column=enemies[index][0])
            enemy_widgets[index].lift()

    update_widgets(data)


    # assign the console output to buffer
    sys.stdout = buffer = io.StringIO()

    def update_output_widget():
        # Set the system output to the output_widget after clearing with end-1c
        output_widget.delete(1.0, "end")
        output_widget.insert("end", buffer.getvalue())
        # Scroll to the bottom of the text widget
        output_widget.see("end")

    def game_instance():

        # Get user input, then clear entry widget
        user_input = input_widget_value.get()
        input_widget.delete(0, "end")

        # Check for combat, then update GUI after combat
        enemy_detected_by_index = enemy_detection(character, enemies, vision_cones)
        # If there is an enemy present:
        if enemy_detected_by_index != None:
            # validate attack input
            attack_choice = get_choice_combat(user_input)
            update_output_widget()
            # None represents an invalid choice, exit the game instance
            if attack_choice == None:
                return
            else:
                is_combat_won = engage_combat(character, attack_choice)
                # delete the enemy and update if player wins
                if is_combat_won:
                    delete_enemy(enemies, enemy_widgets, vision_cones, vision_cone_widgets, enemy_detected_by_index)
                    instance_data = get_user_interface_data(character, end_point, [(2, 2), (1, 1)])
                    update_widgets(instance_data)
                # break out of the game instance to initiate the next phase of combat on user input
                else:
                    return

        # Move character
        direction = get_user_choice(character, board, user_input)
        # Add validation here and return out of game instance if invalid move
        if not validate_move(board, character, direction):
            print("\nPlease enter a direction to move within the game board.\n"
                  "To move north: type 'north', 'w', or '1'\n"
                  "hint: W, A, S, or D are valid inputs for direction\n")
            update_output_widget()
            return
        move_character(character, direction)

        # Move enemies and update GUI
        enemies_move(enemies, vision_cones, board)
        describe_current_location(board, character)
        instance_data = get_user_interface_data(character, end_point, [(2, 2), (1, 1)])
        update_widgets(instance_data)

        # Check if endpoint reached or character is dead before proceeding with next game instance
        achieved_goal = check_if_endpoint_reached(character, board)
        character_still_alive = is_alive(character)
        # Load new level if you reach the end point
        if achieved_goal:
            enemies.clear()
            vision_cones.clear()
            for enemy_widget, vision_cone_widget in zip(enemy_widgets, vision_cone_widgets):
                enemy_widget.destroy()
                vision_cone_widget.destroy()
            enemy_widgets.clear()
            vision_cone_widgets.clear()

            # Create new widgets
            enemies.extend(make_enemy(board))
            vision_cones.extend(make_vision_cones(enemies, board))

            for index in range(len(enemies)):
                enemy_widget = tk.Label(canvas, image=enemy_image, background="white")
                enemy_widget.lift()
                enemy_widgets.append(enemy_widget)
            for index in range(len(vision_cones)):
                vision_cone_widget = tk.Label(canvas, image=vision_cone_image, background="white")
                vision_cone_widgets.append(vision_cone_widget)

            # Reset character position
            character["X-coordinate"] = 0
            character["Y-coordinate"] = 0

            new_level_data = get_user_interface_data(character, end_point, enemies)
            update_widgets(new_level_data)

        elif not character_still_alive:
            print("Game end")
            update_output_widget()
            return

        # Set the system output to the output_widget
        if enemy_detected_by_index != None:
            print("Choose your weapon to defeat the enemy\n"
                  "1. (R)ock\n"
                  "2. (P)aper\n"
                  "3. (S)cissor\n")

        update_output_widget()

    # The enter widget initiates a game instance on click
    enter_widget = ttk.Button(canvas_right, text="ENTER", command=game_instance)
    enter_widget.grid(row=8, column=0, sticky="nsew")
    root.bind('<Return>', lambda e: enter_widget.invoke())


    root.mainloop()


if __name__ == "__main__":
    main()

"""
Tommy Ju
A01347715
Matthew Yoon
A01373290
"""
import random
from combat.get_choice_combat import get_choice_combat
from combat.random_enemy_action import random_enemy_action
from combat.does_player_win import does_player_win


def engage_combat(character: dict, enemy_coordinates: list, vision_cones: list, index: int):
    """
    run combat encounter

    player will be locked into combat until victory or player HP is 0. removes enemy engaged in combat in victory

    :param character: dictionary representing the users' character
    :param enemy_coordinates: list of lists representing coordinates of enemies
    :param vision_cones: list of lists or none representing coordinates of vision cones
    :param index: integer representing the index of the enemy engaged in combat
    :precondition: character is a dictionary with key "Current HP" with values being integer
                   character "Current HP" value is greater than 0 at beginning of engage combat
                   enemy_coordinates list of list representing the enemy current location
                   vision_cones list of lists representing the enemy detection or none if enemy is looking at location
                   not on board
                   index is integer associated with enemy currently engaged in combat
    :postcondition: remove enemy coordinate in combat and lantern associated with enemy in combat using the index
                    character value in key "Current HP" may change if player loses a round of RPS
    """
    print("an enemy approaches")
    still_fighting = True
    while still_fighting and (character["Current HP"] > 0):
        print("You have:" + str(character["Current HP"]) + "HP")
        player_action = (get_choice_combat(), (random.randint(0, 10) + character["Attack Level"]))
        print(player_action)
        enemy_action = random_enemy_action()
        print(enemy_action)
        if does_player_win(player_action, enemy_action):
            print("you won")
            still_fighting = False
        else:
            if (enemy_action[1] - player_action[1]) > 0:
                character["Current HP"] -= (enemy_action[1] - player_action[1])
                print('you took ' + str(enemy_action[1] - player_action[1])+' dmg')
            else:
                character["Current HP"] -= 1
    enemy_coordinates.pop(index)

    vision_cones.pop(index)



def main():
   pass


if __name__ == "__main__":
    main()

"""
Tommy Ju
A01347715
Matthew Yoon
A01373290
"""
import random


def random_enemy_action():
    """
    create randomly decided action enemy will take

    :precondition: enemy is alive
                   player character is alive
                   enemy and player are currently in combat
    :postcondition:enemy action is randomly determined
    :return: tuple representing the action of enemy
    """
    style_choice = random.choice(['rock', 'paper', 'scissor'])
    power = random.randint(0, 10)
    enemy_tuple = (style_choice, power)
    return enemy_tuple


def main():
    enemy_action()


if __name__ == "__main__":
    main()

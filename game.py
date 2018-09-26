#Python Text RPG
#Made by Kurisu Lim

import cmd
import textwrap
import sys
import os
import time
import random

screen_width = 100;

#### Player Setup ####
class player:
    def __init__(self):
        self.name =""
        self.job =""
        self.hp = 0
        self.mp = 0
        self.status_effects = []
        self.location = "b2"
        self.game_over = False
        self.attack = 0
myPlayer = player()

### Title Screen ###
def title_screen_selections():
    option = input("> ")

    if option.lower() == ("play"):
        setup_game() #placeholder until written
    elif option.lower() == ("help"):
        help_menu()
    elif option.lower() == ("quit"):
        sys.exit()
        
    while option.lower() not in ["play", "help", "quit"]:
        print("Please enter a valid command.")
        option = input("> ")
        if option.lower() == ("play"):
            setup_game() #placeholder until written
        elif option.lower() == ("help"):
            help_menu()
        elif option.lower() == ("quit"):
            sys.exit()

def title_screen():
    os.system("clear")
    print("""
            ##########################
            # Welcome to the gRexPG! #
            ##########################

                    - Play -
                    - Help -
                    - Quit -
                    
""")
    title_screen_selections()

def help_menu():
    print("""
            ##########################
            # Welcome to the gRexPG! #
            ##########################

        - Use up, down, left, right to move -
        - Type your commands to do them -
        - Use "look" to inspect something -
        - Good luck and have fun! -
                    
""")
    title_screen_selections()

### Game Functionality ###

#def start_game():

### Map ###
 #a1   b1  c1  d1 
#-----------------
#|   |   |   |   | 1
#-----------------
#|   |   |   |   | 2
#-----------------
#|   |   |   |   | 3
#-----------------
#|   |   |   |   | 4
#-----------------
#Player Starts at B2

ZONENAME = ""
DESCRIPTION = "description"
EXAMINATION = "examine"
SOLVED = False
UP = "up", "north"
DOWN = "down", "south"
LEFT = "left", "west"
RIGHT = "right", "east"

solved_places = {"a1": False, "a2": False, "a3": False, "a4": False,
                 "b1": False, "b2": False, "b3": False, "b4": False,
                 "c1": False, "c2": False, "c3": False, "c4": False,
                 "d1": False, "d2": False, "d3": False, "d4": False,
                 }

zonemap = {
    "a1": {
        ZONENAME: "Town Market",
        DESCRIPTION: "description",
        EXAMINATION: "examine",
        SOLVED:False,
        UP: "a4",
        DOWN: "a2",
        LEFT: "d1",
        RIGHT: "b1",
        },
    "a2": {
            ZONENAME: "Town Hall",
            DESCRIPTION: "description",
            EXAMINATION: "examine",
            SOLVED: False,
            UP: "a1",
            DOWN: "a3",
            LEFT: "d2",
            RIGHT: "b2",
        },
    "a3": {
            ZONENAME: "Black Smith",
            DESCRIPTION: "description",
            EXAMINATION: "examine",
            SOLVED: False,
            UP: "a2",
            DOWN: "a4",
            LEFT: "d3",
            RIGHT: "b3",
        },
    "a4": {
            ZONENAME: "Tavern",
            DESCRIPTION: "description",
            EXAMINATION: "examine",
            SOLVED: False,
            UP: "a3",
            DOWN: "a1",
            LEFT: "d4",
            RIGHT: "b4",
        },
    "b1": {
            ZONENAME: "Slumps",
            DESCRIPTION: "description",
            EXAMINATION: "examine",
            SOLVED: False,
            UP: "b4",
            DOWN: "b2",
            LEFT: "a1",
            RIGHT: "c1",
        },
    "b2": {
            ZONENAME: "HOME",
            DESCRIPTION: "This is your home!",
            EXAMINATION: "Your home looks the same - nothing change",
            SOLVED: False,
            UP: "b1",
            DOWN: "b3",
            LEFT: "a2",
            RIGHT: "c2",
        },
    "b3": {
            ZONENAME: "B3",
            DESCRIPTION: "description",
            EXAMINATION: "examine",
            SOLVED: False,
            UP: "b2",
            DOWN: "b4",
            LEFT: "a3",
            RIGHT: "c3",
        },
    "b4": {
            ZONENAME: "B4",
            DESCRIPTION: "description",
            EXAMINATION: "examine",
            SOLVED: False,
            UP: "b3",
            DOWN: "b1",
            LEFT: "a4",
            RIGHT: "c4",
        },
    "c1": {
            ZONENAME: "C1",
            DESCRIPTION: "description",
            EXAMINATION: "examine",
            SOLVED: False,
            UP: "c4",
            DOWN: "c2",
            LEFT: "b1",
            RIGHT: "d1",
        },
    "c2": {
            ZONENAME: "C2",
            DESCRIPTION: "description",
            EXAMINATION: "examine",
            SOLVED : False,
            UP: "c1",
            DOWN: "c3",
            LEFT: "b2",
            RIGHT: "b3",
        },
    "c3": {
            ZONENAME: "C3",
            DESCRIPTION: "description",
            EXAMINATION: "examine",
            SOLVED: False,
            UP: "c2",
            DOWN: "c4",
            LEFT: "b3",
            RIGHT: "d3",
        },
    "c4": {
            ZONENAME: "C4",
            DESCRIPTION: "description",
            EXAMINATION: "examine",
            SOLVED: False,
            UP: "c3",
            DOWN: "c1",
            LEFT: "b4",
            RIGHT: "d4",
        },
    "d1": {
            ZONENAME: "D1",
            DESCRIPTION: "description",
            EXAMINATION: "examine",
            SOLVED: False,
            UP: "d4",
            DOWN: "d2",
            LEFT: "c1",
            RIGHT: "a1",
        },
    "d2": {
            ZONENAME: "D2",
            DESCRIPTION: "description",
            EXAMINATION: "examine",
            SOLVED: False,
            UP: "d1",
            DOWN: "d3",
            LEFT: "c2",
            RIGHT: "a2",
        },
    "d3": {
            ZONENAME: "D3",
            DESCRIPTION: "description",
            EXAMINATION: "examine",
            SOLVED: False,
            UP: "a2",
            DOWN: "d4",
            LEFT: "c3",
            RIGHT: "a3",
        },
    "d4": {
            ZONENAME: "D4",
            DESCRIPTION: "description",
            EXAMINATION: "examine",
            SOLVED: False,
            UP: "d3",
            DOWN: "d1",
            LEFT: "c4",
            RIGHT: "a4",
        },

    }


### Game Interactivity ###
def print_location():
    print("\n" + ("#" * (4 + len(myPlayer.location))))
    print("# " + myPlayer.location.upper() + " #")
    print("# " + zonemap[myPlayer.location][DESCRIPTION] + " #")
    print("\n" + ("#" * (4 + len(myPlayer.location))))

def prompt():
    print("\n" + "====================================")
    print("What would you like to do?")
    print("Move, Inspect or Quit")
    action = input("> ")
    acceptable_actions = ["move", "go", "travel", "walk", "quit", "inspect", "interact", "look"]
    while action.lower() not in acceptable_actions:
        print("Unknown action, try again.\n")
        action = input("> ")
    if action.lower() == "quit":
        sys.exit()
    elif action.lower() in ["move", "go", "travel", "walk"]:
        player_move(action.lower())
    elif action.lower() in ["inspect", "interact", "look"]:
        player_examine(action.lower())

def player_move(myAction):
    ask = "Where would you like to move to?\n"
    dest = input(ask)
    print("UP,DOWN,LEFT,RIGHT")
    if dest in ["up", "north"]:
        destination = zonemap[myPlayer.location][UP]
        movement_handler(destination)
    elif dest in ["down", "south"]:
        destination = zonemap[myPlayer.location][DOWN]
        movement_handler(destination)
    elif dest in ["left", "west"]:
        destination = zonemap[myPlayer.location][LEFT]
        movement_handler(destination)
    elif dest in ["right", "east"]:
        destination = zonemap[myPlayer.location][RIGHT]
        movement_handler(destination)

def movement_handler(destination):
    print("\n" + "You have move to the " + destination + ".")
    myPlayer.location = destination
    print_location()


def player_examine(action):
    if zonemap[myPlayer.location][SOLVED]:
        print("You already checked this zone.")
    else:
        print("You just trigger an event here.")
  
### Game function ####
# def start_game():
#     return

def main_game_loop():
    while myPlayer.game_over is False:
        prompt()
    #here handle if puzzle is solved or find a key




def setup_game():
    os.system("clear")

    question1 ="Hello, what's your name?\n"
    for character in question1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    player_name = input("> ")
    myPlayer.name = player_name


    ## Job Handling
    question2 = "Hello, what class do you want to play?\n"
    question2added = "(You can play as a warrior, mage, or a rouge)\n"
    for character in question2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)

    for character in question2added:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.01)
    player_job = input("> ")
    valid_jobs = ["warrior", "mage", "rouge"]
    if player_job.lower() in valid_jobs:
        myPlayer.job = player_job
        print("You are now a " + player_job + "!\n")
    while player_job.lower() not in valid_jobs:
        player_job = input("> ")
        if player_job.lower() in valid_jobs:
            myPlayer.job = player_job
            print("You are now a " + player_job + "!\n")

    ##Player Stats
    if myPlayer.job is "warrior":
        self.hp = 120
        self.mp = 20
    elif myPlayer.job is "mage":
        self.hp = 50
        self.mp = 100
    elif myPlayer.job is "rouge":
        self.hp = 80
        self.mp = 50


    ##Introduction
    question3 = "Welcome, " + player_name + " the " + player_job + ".\n"
    for character in question3:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)

    speech1 = "Welcome to this fantasy world!\n"
    speech2 = "I hope it greets you well!\n"
    speech3 = "Just make sure you have fun!\n"
    speech4 = "*winks..winks..winks*\n"
    for character in speech1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.03)
    for character in speech2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.03)
    for character in speech3:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.03)
    for character in speech4:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.02)

    os.system("clear")
    print("########################")
    print("#   Let's Start now!   #")
    print("########################")
    main_game_loop()
        
title_screen()




















































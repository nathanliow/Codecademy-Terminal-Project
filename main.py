# idea:
# Text-based adventure game with a player and enemies (LOTR / GOT themes)
# use randint from random to generate damage numbers
# have leveling system like rpg
# random environments (enemy territory or village appears)

# To Do: (7-5-23)
# - set up a finite environment list, will make this infinite later on
# - set up random name gen for villagers and enemies
# - finish giving different type of enemies different characteristics
# - finish player class rob and trade function
# - allow villagers to help player fight or to fight player themselves
# - allow player to go to different places instead of just going thru environment list

# - fix random enemy fight player thing
# - finish implementing worth/money for players, villagers, and items

from random import *
from classes import *
from environments import *

# -- GAME SETUP --
active_environment_index = 0

# -- START OF THE GAME --
# creating player
name = input("What is your name traveler? \n")
player = Player(name)
print("Welcome", name + "! I wish you safe travels!")

# player choosing first class
choice = input("Choose a class: \n  (1) Barbarian \n  (2) Sharpshooter \n  (3) Mage \n  (4) Tank\n")
while choice not in ["1", "2", "3", "4"]:
    print("That is not a class choice!")
    choice = input("Choose a class: \n  (1) Barbarian \n  (2) Sharpshooter \n  (3) Mage \n  (4) Tank\n")
if choice == "1":
    player.add_item(Item("Sword"))
    player.add_item(Item("Potion"), 3)
    player.add_item(Item("Potion", "UNCOMMON"), 1)
elif choice == "2":
    player.add_item(Item("Bow"))
    player.add_item(Item("Potion"), 3)
    player.add_item(Item("Potion", "UNCOMMON"), 1)
elif choice == "3":
    player.add_item(Item("Wand"))
    player.add_item(Item("Potion"), 3)
    player.add_item(Item("Potion", "UNCOMMON"), 1)
elif choice == "4":
    player.add_item(Item("Sledgehammer"))
    player.add_item(Item("Potion"), 3)
    player.add_item(Item("Potion", "UNCOMMON"), 1)

# -- ENTERING GAME --
while True:
    # quick information about active environment
    active_environment = environment_list[active_environment_index]
    print("\nYou are in", active_environment.name + "!")
    if len(active_environment.entity_list) > 0:
        active_environment.view_entity_list()
    if len(active_environment.item_list) > 0:
        active_environment.view_item_list()
    
    # actions within active environment
    if active_environment.type == "Village":
        choice = input("What would you like to do? \n  (1) Train for XP \n  (2) Trade with a villager \n  (3) Leave this place\n")
        while choice not in ["1", "2", "3"]:
            print("That's not a choice!")
            choice = input("What would you like to do? \n  (1) Train for XP \n  (2) Trade with a villager \n  (3) Leave this place\n")
        if choice == "1":
            xp = randint(0,10)
            player.xp += xp
            if player.xp >= 100:
                player.level += 1
                player.xp -= 100
                print("You leveled up to level", player.level + "!")
            print("You trained for several hours and got", xp, "XP!")
        elif choice == "2":
            # WIP
            continue
        elif choice == "3":
            # Move to the next environment, % ensures that the index wraps around to 0 when it reaches the end of the environment_list
            active_environment_index = (active_environment_index + 1) % len(environment_list)
    elif active_environment.type == "Enemy Outpost":
        choice = input("What would you like to do? \n  (1) Fight \n  (2) Heal \n  (3) Leave this place\n")
        while choice not in ["1", "2", "3"]:
            print("That's not a choice!")
            choice = input("What would you like to do? \n  (1) Fight \n  (2) Heal \n  (3) Leave this place\n")
        if choice == "1":
            active_environment.view_entity_list()
            opponent = input("Who would you like to fight? (Name)\n")
            player.fight(opponent, active_environment)
            # WIP random choice of oppoennt to fight player isn't working
            # opponent = random.choice(active_environment.entity_list)
            # opponent.fight(player)
        elif choice == "2":
            choice = input("What rarity of potion would you like to use? \n  (1) COMMON \n  (2) UNCOMMON \n  (3) RARE \n  (4) LEGENDARY \n  (5) MYTHICAL\n")
            while choice not in ["1", "2", "3", "4", "5"]:
                print("That's not a choice!")
                choice = input("What rarity of potion would you like to use? \n  (1) COMMON \n  (2) UNCOMMON \n  (3) RARE \n  (4) LEGENDARY \n  (5) MYTHICAL\n")
            if choice == "1":
                player.heal("COMMON")
            elif choice == "2":
                player.heal("UNCOMMON")
            elif choice == "3":
                player.heal("RARE")
            elif choice == "4":
                player.heal("LEGENDARY")
            elif choice == "5":
                player.heal("MYTHICAL")
        elif choice == "3":
            active_environment_index = (active_environment_index + 1) % len(environment_list)
    elif active_environment.type == "Dungeon":
        choice = input("What would you like to do? \n  (1) Fight \n  (2) Heal \n  (3) Loot \n  (4) Leave this place\n")
        while choice not in ["1", "2", "3", "4"]:
            print("That's not a choice!")
            choice = input("What would you like to do? \n  (1) Fight \n  (2) Heal \n  (3) Loot \n  (4) Leave this place\n")
        if choice == "1":
            # WIP - figure out how to convert input into who to fight
            player.fight("NULL")
        elif choice == "2":
            choice = input("What rarity of potion would you like to use? \n  (1) COMMON \n  (2) UNCOMMON \n  (3) RARE \n  (4) LEGENDARY \n  (5) MYTHICAL\n")
            while choice not in ["1", "2", "3", "4", "5"]:
                print("That's not a choice!")
                choice = input("What rarity of potion would you like to use? \n  (1) COMMON \n  (2) UNCOMMON \n  (3) RARE \n  (4) LEGENDARY \n  (5) MYTHICAL\n")
            if choice == "1":
                player.heal("COMMON")
            elif choice == "2":
                player.heal("UNCOMMON")
            elif choice == "3":
                player.heal("RARE")
            elif choice == "4":
                player.heal("LEGENDARY")
            elif choice == "5":
                player.heal("MYTHICAL")
        elif choice == "3":
            player.loot(active_environment)
            player.view_inv()
            if len(active_environment.item_list) > 0:
                active_environment.view_item_list()
            else:
                print("This place has been fully looted...")
        elif choice == "4":
            active_environment_index = (active_environment_index + 1) % len(environment_list)
    elif active_environment.type == "Boss Room":
        choice = input("What would you like to do? \n  (1) Fight \n  (2) Heal \n  (3) Leave this place\n")
        while choice not in ["1", "2", "3"]:
            print("That's not a choice!")
            choice = input("What would you like to do? \n  (1) Fight \n  (2) Heal \n  (3) Leave this place\n")
        if choice == "1":
            # WIP - figure out how to convert input into who to fight
            player.fight("NULL")
        elif choice == "2":
            choice = input("What rarity of potion would you like to use? \n  (1) COMMON \n  (2) UNCOMMON \n  (3) RARE \n  (4) LEGENDARY \n  (5) MYTHICAL\n")
            while choice not in ["1", "2", "3", "4", "5"]:
                print("That's not a choice!")
                choice = input("What rarity of potion would you like to use? \n  (1) COMMON \n  (2) UNCOMMON \n  (3) RARE \n  (4) LEGENDARY \n  (5) MYTHICAL\n")
            if choice == "1":
                player.heal("COMMON")
            elif choice == "2":
                player.heal("UNCOMMON")
            elif choice == "3":
                player.heal("RARE")
            elif choice == "4":
                player.heal("LEGENDARY")
            elif choice == "5":
                player.heal("MYTHICAL")
        elif choice == "3":
            active_environment_index = (active_environment_index + 1) % len(environment_list)

    # check for game end
    if player.health <= 0:
        print("You died!")
        break
# idea:
# Text-based adventure game with a player and enemies (LOTR / GOT themes)
# use randint from random to generate damage numbers
# have leveling system like rpg
# random environments (enemy territory or village appears)

# To Do: (7-5-23)
# - set up a finite environment list, will make this infinite later on
# - set up random name gen for villagers and enemies
# - finish giving different type of enemies different characteristics
# - allow villagers to help player fight or to fight player themselves
# - allow player to go to different places instead of just going thru environment list

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
    player.add_money(1000)
elif choice == "2":
    player.add_item(Item("Bow"))
    player.add_item(Item("Potion"), 3)
    player.add_item(Item("Potion", "UNCOMMON"), 1)
    player.add_money(1000)
elif choice == "3":
    player.add_item(Item("Wand"))
    player.add_item(Item("Potion"), 3)
    player.add_item(Item("Potion", "UNCOMMON"), 1)
    player.add_money(1000)
elif choice == "4":
    player.add_item(Item("Sledgehammer"))
    player.add_item(Item("Potion"), 3)
    player.add_item(Item("Potion", "UNCOMMON"), 1)
    player.add_money(1000)

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
        choice = input("What would you like to do? \n  (1) Train for XP \n  (2) Trade with a villager \n  (3) Rob a villager \n  (4) Leave this place\n")
        while choice not in ["1", "2", "3", "4"]:
            print("That's not a choice!")
            choice = input("What would you like to do? \n  (1) Train for XP \n  (2) Trade with a villager \n  (3) Rob a villager \n  (4) Leave this place\n")
        if choice == "1":
            xp = randint(1,25)
            player.xp += xp
            # if player has enough xp to level up
            if player.xp >= 100:
                player.level += 1
                player.xp -= 100
                print("You leveled up to level", str(player.level) + "!")
            print("You trained for several hours and got", xp, "XP!")
        elif choice == "2":
            if len(active_environment.entity_list) > 0:
                for i, entity in enumerate(active_environment.entity_list, start=1):
                    print(f"({i}) {entity.name} the {entity.type} (Level: {entity.level})")
                trade_villager_num = input("Who would you like to trade with?\n")
                while not trade_villager_num.isnumeric() or not int(trade_villager_num) <= len(active_environment.entity_list):
                    print("That is not a choice!")
                    trade_villager_num = input("Who would you like to trade with?\n")
                trade_villager = active_environment.entity_list[int(trade_villager_num)-1]
                player.trade(trade_villager.name, active_environment)
                player.view_inv()
            else:
                print("There is nobody to trade with!")
        elif choice == "3":
            if len(active_environment.entity_list) > 0:
                for i, entity in enumerate(active_environment.entity_list, start=1):
                    print(f"({i}) {entity.name} the {entity.type} (Level: {entity.level})")
                rob_villager_num = input("Who would you like to rob?\n")
                while not rob_villager_num.isnumeric() or not int(rob_villager_num) <= len(active_environment.entity_list):
                    print("That is not a choice!")
                    rob_villager_num = input("Who would you like to rob?\n")
                rob_villager = active_environment.entity_list[int(rob_villager_num)-1]
                player.rob(rob_villager.name, active_environment)
            else:
                print("There is nobody to rob!")
        elif choice == "4":
            # Move to the next environment, % ensures that the index wraps around to 0 when it reaches the end of the environment_list
            active_environment_index = (active_environment_index + 1) % len(environment_list)
    elif active_environment.type == "Enemy Outpost":
        choice = input("What would you like to do? \n  (1) Fight \n  (2) Heal \n  (3) Leave this place\n")
        while choice not in ["1", "2", "3"]:
            print("That's not a choice!")
            choice = input("What would you like to do? \n  (1) Fight \n  (2) Heal \n  (3) Leave this place\n")
        if choice == "1":
            if len(active_environment.entity_list) > 0:
                for i, entity in enumerate(active_environment.entity_list, start=1):
                    print(f"({i}) {entity.name} the {entity.type} (Level: {entity.level})")
                opponent_num = input("Who would you like to fight?\n")
                while not opponent_num.isnumeric() or not int(opponent_num) <= len(active_environment.entity_list):
                    print("That is not a choice!")
                    opponent_num = input("Who would you like to fight?\n")
                opponent = active_environment.entity_list[int(opponent_num)-1]
                player.fight(opponent.name, active_environment)
                opponent_list = [entity for entity in active_environment.entity_list]
                opponent = opponent_list[randint(0,len(active_environment.entity_list)-1)]
                opponent.fight(player)
            else:
                print("There are no enemies!")
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
            if len(active_environment.entity_list) > 0:
                for i, entity in enumerate(active_environment.entity_list, start=1):
                    print(f"({i}) {entity.name} the {entity.type} (Level: {entity.level})")
                opponent_num = input("Who would you like to fight?\n")
                while not opponent_num.isnumeric() or not int(opponent_num) <= len(active_environment.entity_list):
                    print("That is not a choice!")
                    opponent_num = input("Who would you like to fight?\n")
                opponent = active_environment.entity_list[int(opponent_num)-1]
                player.fight(opponent.name, active_environment)
                opponent_list = [entity for entity in active_environment.entity_list]
                opponent = opponent_list[randint(0,len(active_environment.entity_list)-1)]
                opponent.fight(player)
            else:
                print("There are no enemies!")
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
            if len(active_environment.entity_list) > 0:
                for i, entity in enumerate(active_environment.entity_list, start=1):
                    print(f"({i}) {entity.name} the {entity.type} (Level: {entity.level})")
                opponent_num = input("Who would you like to fight?\n")
                while not opponent_num.isnumeric() or not int(opponent_num) <= len(active_environment.entity_list):
                    print("That is not a choice!")
                    opponent_num = input("Who would you like to fight?\n")
                opponent = active_environment.entity_list[int(opponent_num)-1]
                player.fight(opponent.name, active_environment)
                opponent_list = [entity for entity in active_environment.entity_list]
                opponent = opponent_list[randint(0,len(active_environment.entity_list)-1)]
                opponent.fight(player)
            else:
                print("There are no enemies!")
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
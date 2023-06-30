# idea:
# Text-based adventure game with a player and enemies (LOTR / GOT themes)
# use randint from random to generate damage numbers
# have leveling system like rpg
# random environments (enemy territory or village appears)

# To Do: (6-30-23)
# - set up a finite environment list, will make this infinite later on
# - set up random name gen for villagers and enemies
# - finish giving different type of enemies different characteristics
# - finish player class rob and trade function
# - allow villagers to help player fight or to fight player themselves
# - figure out fighting choice from input
# - figure out looting option
# - allow player to go to different places instead of just going thru environment list

from random import randint

class Player:
    def __init__(self, name="Traveler", health=100, level=1, inventory=None):
        self.name = name
        self.health = health
        self.xp = 0
        self.level = level
        self.inventory = inventory if inventory is not None else []
        self.max_health = 100 + 5*(self.level-1)

    def __repr__(self):
        return self.name + " is level " + str(self.level) + " and has " + str(self.health) + " health remaining."

    def add_item(self, item, quantity=1):
        # checks if item is already in inventory
        for inventory_item in self.inventory:
            if inventory_item.type == item.type and inventory_item.rarity == item.rarity:
                # item already exists, update quantity
                inventory_item.quantity += quantity
                print("Added", quantity, inventory_item.rarity, inventory_item.type)
                return
        # add new item to inventory if not already present 
        item.quantity = quantity
        self.inventory.append(item)
        print("Added", quantity, item.rarity, item.type)

    def remove_item(self, item, quantity=1):
        # checks if item is in inventory
        for inventory_item in self.inventory:
            if inventory_item.type == item:
                inventory_item.quantity -= quantity
                if inventory_item.quantity <= 0:
                    print("Removed", str(inventory_item.quantity+quantity), inventory_item.rarity, inventory_item.type)
                    self.inventory.remove(inventory_item)
                else:
                    print("Removed", quantity, inventory_item.rarity, inventory_item.type)
                return
        print(item, "not found in the inventory.")

    def fight(self, enemy_name):
        # checks if enemy is in the active environment
        for entity in active_environment.entity_list:
            if entity.name == enemy_name:
                damage = abs((self.level + 1) - entity.level) * randint(0,50)
                entity.health -= damage
                print(entity.name, "the", entity.type, "was hit for", str(damage), "health! They have", str(entity.health), "health left!")
                break
        else:
            print(enemy_name, "isn't in the area!")

    # WIP
    def trade(self, villager_name):
        for entity in active_environment.entity_list:
            if entity.name == villager_name and isinstance(entity, Villager):
                # Trading logic
                # print(entity.name, "the", entity.type, "was hit for", str(damage), "health! They have", str(entity.health), "health left!")
                break
        else:
            print(villager_name, "isn't in the area!")

    # WIP
    def rob(self, villager_name):
        for entity in active_environment.entity_list:
            if entity.name == villager_name and isinstance(entity, Villager):
                # Robbing logic
                # print(entity.name, "the", entity.type, "was hit for", str(damage), "health! They have", str(entity.health), "health left!")
                break
        else:
            print(villager_name, "isn't in the area!")

    def heal(self, rarity="COMMON"):
        potion_found = False
        for inventory_item in self.inventory:
            if inventory_item.type == "Potion" and inventory_item.rarity == rarity:
                inventory_item.quantity -= 1
                potion_found = True
                if rarity == "COMMON":
                    # heals by 20 health
                    self.health += 20
                    print("You used a COMMON potion!")
                elif rarity == "UNCOMMON":
                    # heals by 50 health
                    self.health += 50
                    print("You used an UNCOMMON potion!")
                elif rarity == "RARE":
                    # heals by 20% of your max health
                    self.health += self.max_health*0.2
                    print("You used a RARE potion!")
                elif rarity == "LEGENDARY":
                    # heals by 50% of your max health
                    self.health += self.max_health*0.5
                    print("You used a LEGENDARY potion!")
                elif rarity == "MYTHICAL":
                    self.health = self.max_health
                    print("You used a MYTHICAL potion!")
                if self.health > self.max_health:
                    self.health = self.max_health
                    print("You now have full health at", self.max_health, "health!")
                else:
                    print("You now have", self.health, "health!")
                break 
        if not potion_found:  
            if rarity != "UNCOMMON":
                print("You don't have a", rarity, "potion!")
            else:
                print("You don't have an", rarity, "potion!")

    def view_inv(self):
        item_names = [item.rarity + " " + item.type + " (" + str(item.quantity) + ")" for item in self.inventory]
        final = "You have " + ", ".join(item_names)
        if item_names:
            final = final.rstrip(", ")  # Remove the trailing comma and space
        print(final)

class Enemy:
    def __init__(self, type, name, health=100, level=1):
        self.type = type
        self.name = name
        self.health = health
        self.level = level
        self.damage_multiplier = 1

        # WIP - give different characteristics to common type of enemies
        if self.type == "Orc":
            self.health *= 1
            self.damage_multiplier = 0.9
        elif self.type == "Ogre":
            self.health *= 1.1
            self.damage_multiplier = 1.2
        elif self.type == "Snake":
            self.health *= 0.5
            self.damage_multiplier = 0.9
        elif self.type == "Goblin":
            self.health *= 0.25
            self.damage_multiplier = 0.5
        elif self.type == "Savages":
            self.health *= 1
            self.damage_multiplier = 1.5
        elif self.type == "Bandits":
            self.health *= 1
            self.damage_multiplier = 0.5
        elif self.type == "Dragon":
            self.health *= 10
            self.damage_multiplier = 10
        
    def fight(self, player):
        damage = (abs((self.level + 1) - player.level) * randint(0,50)) * self.damage_multiplier
        player.health -= damage
    
    def __repr__(self):
        return "This " + self.type + " is level " + str(self.level) + " and has " + str(self.health) + " health remaining."

class Villager:
    def __init__(self, type, name, health=100, level=1, inventory=None):
        self.type = type
        self.name = name
        self.health = health
        self.level = level
        self.inventory = inventory if inventory is not None else []

    def __repr__(self):
        return self.name + " the " + self.type + " is level " + str(self.level) + " and has " + str(self.health) + " health remaining."

    def view_inv(self):
        item_names = [item.rarity + " " + item.type + " (" + str(item.quantity) + ")" for item in self.inventory]
        final = self.name, " has " + ", ".join(item_names)
        if item_names:
            final = final.rstrip(", ")  # Remove the trailing comma and space
        print(final)

class Item:
    def __init__(self, type, rarity="COMMON", description="It seems usable...", level=1, quantity=1):
        self.type = type
        self.rarity = rarity
        self.description = description
        self.level = level
        self.quantity = quantity
    
    def __repr__(self):
        return "This level", str(self.level), self.rarity, self.type, "has '" + self.description + "' etched into it. You have", str(self.quantity), "of these."

class Environment:
    def __init__(self, name, level, type, description, entity_list):
        self.name = name
        self.level = level
        self.type = type
        self.description = description
        self.entity_list = entity_list
    
    def __repr__(self):
        return self.name + " is a level " + str(self.level) + " environment. Description: " + self.description

    def view_entity_list(self):
        entity_list = [entity.name + " the " + entity.type + " (Level: " + str(entity.level) + ")" for entity in self.entity_list]
        final = "Enemies: " + ", ".join(entity_list)
        if entity_list:
            final = final.rstrip(", ")  # Remove the trailing comma and space
        print(final)      

# -- GAME SETUP --
environment_list = [
    Environment("Dallas", 1, "Village", "A bustling village at the center of the world, great for trading and training.", [Villager("Librarian", "Joe"), Villager("Blacksmith", "Aaron"), Villager("Magician", "John")]),
    Environment("Ogre Camp", 5, "Enemy Outpost", "A congregation of green grumpy ogres.", [Enemy("Ogre", "Eric"), Enemy("Ogre", "Eel"), Enemy("Ogre", "Erica")]),
    Environment("Snake Dungeon", 10, "Dungeon", "A den of dangerous and venomous snakes may hold great treasures.", [Enemy("Snake", "Moma"), Enemy("Snake", "Mama"), Enemy("Snake", "Memo")]),
    Environment("The Dragon's Lair", 20, "Boss Room", "ENTER AT YOUR OWN RISK...", [Enemy("Dragon", "Drakor")])
]
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
    active_environment = environment_list[active_environment_index]
    print("You are in ", active_environment.name + "!")
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
            # WIP
            continue
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
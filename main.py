# idea:
# Text-based adventure game with a player and enemies (LOTR / GOT themes)
# use randint from random to generate damage numbers
# have leveling system like rpg
# random environments (enemy territory or village appears)

from random import randint

class Player:
    def __init__(self, name="Traveler", health=100, level=1, inventory=None):
        self.name = name
        self.health = health
        self.xp = 0
        self.level = level
        self.inventory = inventory if inventory is not None else []

    def __repr__(self):
        return self.name + " is level " + str(self.level) + " and has " + str(self.health )+ " health remaining."

    # PROBLEM: quantity value isn't overriden, 2nd print statement runs with "player.add_item(Item("Potion", quantity=3))" --> Added 1 COMMON Potion instead of Added 3 COMMON Potion
    # def add_item(self, item, quantity=1):
    #     for inventory_item in self.inventory:
    #         if inventory_item.type == item.type and inventory_item.rarity == item.rarity:
    #             inventory_item.quantity += quantity
    #             print("Added", quantity, inventory_item.rarity, inventory_item.type)
    #             return
    #     self.inventory.append(item)
    #     print("Added", quantity, item.rarity, item.type)

    def remove_item(self, item, quantity=1):
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

    def fight(self, enemy):
        damage = abs(self.level - enemy.level) * randint(0,50)
        enemy.health -= damage
        print("The " + enemy.type + " was hit for " + str(damage) + " health! They have " + str(enemy.health) + " health left!")
    
    # def heal(self):
    #     if self.type == "Potion" not in self.inventory:
    #         print("You don't have a potion!")
    #     else:
    #         self.inventory.remove_item("Potion")
    #         self.health = 100

    def view_inv(self):
        item_names = [item.rarity + " " + item.type + " (" + str(item.quantity) + ")" for item in self.inventory]
        final = "You have " + ", ".join(item_names)
        if item_names:
            final = final.rstrip(", ")  # Remove the trailing comma and space
        print(final)

class Enemy:
    def __init__(self, type, health=100, level=1):
        self.type = type
        self.health = health
        self.level = level
    
    def __repr__(self):
        return "This " + self.type + " is level " + str(self.level) + " and has " + str(self.health) + " health remaining."

    def fight(self, player):
        damage = abs(self.level - player.level) * randint(0,50)
        player.health -= damage

class Item:
    def __init__(self, type, rarity="COMMON", description="It seems usable...", level=1, quantity=1):
        self.type = type
        self.rarity = rarity
        self.description = description
        self.level = level
        self.quantity = quantity
    
    def __repr__(self):
        return "This level " + str(self.level) + " " + self.rarity + " " + self.type + " has '" + self.description + "' etched into it. You have " + str(self.quantity) + " of these."


# -- START OF THE GAME --

# creating player
name = input("What is your name traveler? ")
player = Player(name)

# giving player first weapon
choice = input("Choose a weapon: Sword (1) // Bow (2) ")
if choice == "1":
    player.add_item(Item("Sword"))
    player.add_item(Item("Potion", quantity=3))
elif choice == "2":
    player.add_item(Item("Bow"))

# test statements
player.view_inv()
player.remove_item("Potion", 2)
player.view_inv()


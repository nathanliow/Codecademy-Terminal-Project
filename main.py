# idea:
# Text-based adventure game with a player and enemies (LOTR / GOT themes)
# use randint from random to generate damage numbers
# have leveling system like rpg
# random environments (enemy territory or village appears)

from random import randint

class Player:
    def __init__(self, name="Traveler", health=100, level=1, inventory=[]):
        self.name = name
        self.health = health
        self.level = level
        self.inventory = inventory

    def __repr__(self):
        return self.name + " is level " + self.level + " and has " + self.health + " health remaining."

class Enemy:
    def __init__(self, type, health=100, level=1):
        self.type = type
        self.health = health
        self.level = level
    
    def __repr__(self):
        return "This " + self.type + " is level " + self.level + " and has " + self.health + " health remaining."


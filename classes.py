from random import *

class Player:
    def __init__(self, name="Traveler", health=100, level=1, inventory=None, money=0):
        self.name = name
        self.health = health
        self.xp = 0
        self.level = level
        self.inventory = inventory if inventory is not None else []
        self.money = money
        self.max_health = 100 + 5*(self.level-1)

    def __repr__(self):
        return self.name + " is level " + str(self.level) + " and has " + str(self.health) + " health remaining." + self.name + " has $" + str(self.money) + "."

    def add_item(self, item, quantity=1):
        # checks if item is already in inventory
        for inventory_item in self.inventory:
            if inventory_item.type == item.type and inventory_item.rarity == item.rarity:
                # item already exists, update quantity
                inventory_item.quantity += quantity
                print("Added", quantity, inventory_item.rarity, inventory_item.type + "!")
                return
        # add new item to inventory if not already present 
        item.quantity = quantity
        self.inventory.append(item)
        print("Added", quantity, item.rarity, item.type + "!")

    def remove_item(self, item, quantity=1):
        # checks if item is in inventory
        for inventory_item in self.inventory:
            if inventory_item.type == item.type and inventory_item.rarity == item.rarity:
                inventory_item.quantity -= quantity
                if inventory_item.quantity <= 0:
                    print("Removed", str(inventory_item.quantity+quantity), inventory_item.rarity, inventory_item.type + "!")
                    self.inventory.remove(inventory_item)
                else:
                    print("Removed", quantity, inventory_item.rarity, inventory_item.type + "!")
                return
        if item not in self.inventory:
            print(inventory_item.rarity, inventory_item.type, "not found in the inventory.")

    # WIP
    def fight(self, enemy_name, active_environment):
        # checks if enemy is in the active environment
        for entity in active_environment.entity_list:
            if entity.name == enemy_name:
                damage = abs((self.level + 1) - entity.level) * randint(0,50)
                entity.health -= damage
                print(entity.name, "the", entity.type, "was hit for", str(damage), "health! They have", str(int(entity.health)), "health left!")
                if entity.health <= 0:
                    active_environment.entity_list.remove(entity)
                    print(entity.name, "the", entity.type, "has died!")
                break
        else:
            print(enemy_name, "isn't in the area!")

    # WIP
    def trade(self, villager_name, active_environment):
        for entity in active_environment.entity_list:
            if entity.name == villager_name and isinstance(entity, Villager):
                # Trading logic
                # print(entity.name, "the", entity.type, "was hit for", str(damage), "health! They have", str(entity.health), "health left!")
                break
            else:
                print(villager_name, "isn't in the area!")

    # WIP
    def rob(self, villager_name, active_environment):
        for entity in active_environment.entity_list:
            if entity.name == villager_name and isinstance(entity, Villager):
                # Robbing logic
                # print(entity.name, "the", entity.type, "was hit for", str(damage), "health! They have", str(entity.health), "health left!")
                break
            else:
                print(villager_name, "isn't in the area!")

    def loot(self, active_environment):
        rarity_chances = {
            "COMMON": 90,
            "UNCOMMON": 80,
            "RARE": 60,
            "LEGENDARY": 30,
            "MYTHICAL": 10
        }
        if len(active_environment.item_list) > 0:
            for item in active_environment.item_list:
                if item.rarity in rarity_chances:
                    loot_chance = rarity_chances[item.rarity]
                    randnum = randint(1, 100)
                    if randnum <= loot_chance:
                        temp_quantity = item.quantity
                        active_environment.remove_item(item, quantity=item.quantity)
                        self.add_item(item, quantity=temp_quantity)
                        print("You successfully looted", item.rarity, item.type, "(" + str(temp_quantity) + ")!")
                    else:
                        print("You failed to loot", item.rarity, item.type, "(" + str(item.quantity) + ")!")

    def add_money(self, amount):
        self.money += amount
        print("You have gained $" + amount + "!")

    def remove_money(self, amount):
        self.money -= amount
        print("You have lost $" + amount + "!")

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
        print(self.name, "the", self.type, "hit you for", str(damage), "health! You have", str(int(player.health)), "health left!")

    
    def __repr__(self):
        return "This " + self.type + " is level " + str(self.level) + " and has " + str(self.health) + " health remaining."

class Villager:
    def __init__(self, type, name, health=100, level=1, inventory=None, money=0):
        self.type = type
        self.name = name
        self.health = health
        self.level = level
        self.inventory = inventory if inventory is not None else []
        self.money = money

    def __repr__(self):
        return self.name + " the " + self.type + " is level " + str(self.level) + " and has " + str(self.health) + " health remaining." + self.name + " has $" + str(self.money) + "."

    def add_money(self, amount):
        self.money += amount
        print(self.name, "the", self.type, "has gained $" + amount + "!")

    def remove_money(self, amount):
        self.money -= amount
        print(self.name, "the", self.type, "has lost $" + amount + "!")

    def view_inv(self):
        item_names = [item.rarity + " " + item.type + " (" + str(item.quantity) + ")" for item in self.inventory]
        final = self.name, " has " + ", ".join(item_names)
        if item_names:
            final = final.rstrip(", ")  # Remove the trailing comma and space
        print(final)

class Item:
    def __init__(self, type, rarity="COMMON", description="It seems usable...", level=1, quantity=1, value=100):
        self.type = type
        self.rarity = rarity
        self.description = description
        self.level = level
        self.quantity = quantity
        self.value = value
    
    def __repr__(self):
        return "This level " + str(self.level) + self.rarity, self.type + "has '" + self.description + "' etched into it. There are " + str(self.quantity) + " of these. It is worth " + str(self.value) + "."

class Environment:
    def __init__(self, name, level, type, description, entity_list=None, item_list=None):
        self.name = name
        self.level = level
        self.type = type
        self.description = description
        self.entity_list = entity_list if entity_list is not None else []
        self.item_list = item_list if item_list is not None else []
    
    def __repr__(self):
        return self.name + " is a level " + str(self.level) + " environment. Description: " + self.description

    def view_entity_list(self):
        entity_list = [entity.name + " the " + entity.type + " (Level: " + str(entity.level) + ")" for entity in self.entity_list]
        final = "Entities: " + ", ".join(entity_list)
        if entity_list:
            final = final.rstrip(", ")  # Remove the trailing comma and space
        print(final)   

    def view_item_list(self):
        item_list = [item.rarity + " " + item.type + " (" + str(item.quantity) + ")" for item in self.item_list]
        final = "This place contains " + ", ".join(item_list)
        if item_list:
            final = final.rstrip(", ")  # Remove the trailing comma and space
        print(final)  

    def remove_item(self, item, quantity=1):
        # checks if item is in inventory
        for env_item in self.item_list:
            if env_item.type == item.type and env_item.rarity == item.rarity:
                env_item.quantity -= quantity
                if env_item.quantity <= 0:
                    print("Removed", str(env_item.quantity+quantity), env_item.rarity, env_item.type, "from this place!")
                    self.item_list.remove(env_item)
                else:
                    print("Removed", quantity, env_item.rarity, env_item.type, "from this place!")
                return
        if item not in self.item_list:
            print(env_item.rarity, env_item.type, "is not here.")

    def remove_entity(self, entity_removed):
        # checks if item is in inventory
        for entity in self.entity_list:
            if entity.type == entity_removed.type and entity.name == entity_removed.name:
                self.entity_list.remove(entity_removed)
                print(entity_removed.name, "the", entity_removed.type, "has died!")
            return
        if entity_removed not in self.entity_list:
            print(entity_removed.name, "the", entity_removed.type, "is not here.")
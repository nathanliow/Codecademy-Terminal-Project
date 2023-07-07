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
                # print("Added", quantity, inventory_item.rarity, inventory_item.type + "!")
                return
        # add new item to inventory if not already present 
        item.quantity = quantity
        # print("Added", quantity, item.rarity, item.type + "!")
        self.inventory.append(item)

    def remove_item(self, item, quantity=1):
        # checks if item is in inventory
        for inventory_item in self.inventory:
            if inventory_item.type == item.type and inventory_item.rarity == item.rarity:
                inventory_item.quantity -= quantity
                if inventory_item.quantity <= 0:
                    # print("Removed", str(inventory_item.quantity+quantity), inventory_item.rarity, inventory_item.type + "!")
                    self.inventory.remove(inventory_item)
                # else:
                    # print("Removed", quantity, inventory_item.rarity, inventory_item.type + "!")
                return
        if item not in self.inventory:
            print(inventory_item.rarity, inventory_item.type, "not found in the inventory.")

    def fight(self, enemy_name, active_environment):
        # checks if enemy is in the active environment
        for entity in active_environment.entity_list:
            if entity.name == enemy_name:
                damage = abs((self.level + 1) - entity.level) * randint(0,50)
                entity.health -= damage
                if entity.health <= 0:
                    active_environment.entity_list.remove(entity)
                    print(entity.name, "the", entity.type, "was hit for", str(damage), "health! They have 0 health left!")
                    print(entity.name, "the", entity.type, "has died!")
                else:
                    print(entity.name, "the", entity.type, "was hit for", str(damage), "health! They have", str(int(entity.health)), "health left!")
                break
        else:
            print(enemy_name, "isn't in the area!")

    def trade(self, villager_name, active_environment):
        for entity in active_environment.entity_list:
            if entity.name == villager_name and isinstance(entity, Villager):
                if len(entity.inventory) > 0:
                    # lists out all the villager's items
                    for i, item in enumerate(entity.inventory, start=1):
                        print(f"({i}) {item.rarity} {item.type} ({item.quantity}) -- Value: {item.value}")
                    # asking what item is desired
                    want_item_num = input("What would you like to trade for?\n")
                    while not want_item_num.isnumeric() or not int(want_item_num) <= len(entity.inventory):
                        print("That is not a choice!")
                        want_item_num = input("What would you like to trade for?\n")
                    want_item = entity.inventory[int(want_item_num)-1]    
                    # trading logic
                    payment_method = input("How would you like to trade? \n  (1) With money \n  (2) With an item\n")
                    while payment_method not in ["1", "2"]:
                        print("That's not a choice!")
                        payment_method = input("How would you like to trade? \n  (1) With money \n  (2) With an item\n")
                    # trading with money
                    if payment_method == "1":
                        randnum = randint(1,10)
                        if randnum <= 2:
                            discount = randint(5,30)
                            amount_paid = int(want_item.value * ((100-discount)/100))
                            if self.money - amount_paid >= 0:
                                self.money -= amount_paid
                                self.add_item(want_item, quantity=want_item.quantity)
                                entity.inventory.remove(want_item)
                                print("You were able to bargain and buy", want_item.rarity, want_item.type, "(" + str(want_item.level) + ") for $" + str(amount_paid) + "!")
                                print("You now have $" + str(self.money) + "!")
                                break
                            else:
                                print("You don't have enough money!")
                                break
                        elif randnum >= 8:
                            overcharge = randint(5,30)
                            amount_paid = int(want_item.value * ((100+overcharge)/100))
                            if self.money - amount_paid >= 0:
                                self.money -= amount_paid
                                self.add_item(want_item, quantity=want_item.quantity)
                                entity.inventory.remove(want_item)
                                print("You tried bargaining but", villager_name, "got mad and added more fees! You bought", want_item.rarity, want_item.type, "(" + str(want_item.level) + ") for $" + str(amount_paid) + "!")
                                print("You now have $" + str(self.money) + "!")
                                break
                            else:
                                print("You don't have enough money!")
                                break
                        else:
                            amount_paid = want_item.value
                            if self.money - amount_paid >= 0:
                                self.money -= amount_paid
                                self.add_item(want_item, quantity=want_item.quantity)
                                entity.inventory.remove(want_item)
                                print("You bought", want_item.rarity, want_item.type, "(" + str(want_item.level) + ") for $" + str(amount_paid) + "!")
                                print("You now have $" + str(self.money) + "!")
                                break
                            else:
                                print("You don't have enough money!")
                                break
                    # trading with player items
                    if payment_method == "2":
                        # lists out player items
                        for i, item in enumerate(self.inventory, start=1):
                            print(f"({i}) {item.rarity} {item.type} ({item.quantity}) -- Value: {item.value}")
                        # asking what item wants to be traded away
                        give_item_num = input("What would you like to trade away?\n")
                        while not give_item_num.isnumeric() or not int(give_item_num) <= len(self.inventory):
                            print("That is not a choice!")
                            give_item_num = input("What would you like to trade away?\n")
                        give_item = self.inventory[int(give_item_num)-1]
                        value_diff = abs(give_item.value - want_item.value)
                        # player item more valuable than desired item
                        # trade success chances increase as difference in value increases
                        if give_item.value >= want_item.value:
                            randnum = randint(1,100)
                            if value_diff <= 50:
                                # trade success 50%
                                if randnum <= 50:
                                    self.add_item(want_item, quantity=want_item.quantity)
                                    entity.inventory.remove(want_item)
                                    entity.add_item(give_item, quantity=give_item.quantity)
                                    self.inventory.remove(give_item)
                                    print(villager_name, "was interested in your item! You traded", give_item.rarity, give_item.type, "(" + str(give_item.level) + ") for", want_item.rarity, want_item.type, "(" + str(want_item.level) + ")!")
                                # trade fail
                                else:
                                    print(villager_name, "isn't interested in this item!")
                            elif value_diff > 50 and value_diff <= 200:
                                if randnum <= 65:
                                    self.add_item(want_item, quantity=want_item.quantity)
                                    entity.inventory.remove(want_item)
                                    entity.add_item(give_item, quantity=give_item.quantity)
                                    self.inventory.remove(give_item)
                                    print(villager_name, "was interested in your item! You traded", give_item.rarity, give_item.type, "(" + str(give_item.level) + ") for", want_item.rarity, want_item.type, "(" + str(want_item.level) + ")!")
                                else:
                                    print(villager_name, "isn't interested in this item!")
                            elif value_diff > 200 and value_diff <= 500:
                                if randnum <= 75:
                                    self.add_item(want_item, quantity=want_item.quantity)
                                    entity.inventory.remove(want_item)
                                    entity.add_item(give_item, quantity=give_item.quantity)
                                    self.inventory.remove(give_item)
                                    print(villager_name, "was interested in your item! You traded", give_item.rarity, give_item.type, "(" + str(give_item.level) + ") for", want_item.rarity, want_item.type, "(" + str(want_item.level) + ")!")
                                else:
                                    print(villager_name, "isn't interested in this item!")
                            elif value_diff > 500 and value_diff <= 1000:
                                if randnum <= 90:
                                    self.add_item(want_item, quantity=want_item.quantity)
                                    entity.inventory.remove(want_item)
                                    entity.add_item(give_item, quantity=give_item.quantity)
                                    self.inventory.remove(give_item)
                                    print(villager_name, "was interested in your item! You traded", give_item.rarity, give_item.type, "(" + str(give_item.level) + ") for", want_item.rarity, want_item.type, "(" + str(want_item.level) + ")!")
                                else:
                                    print(villager_name, "isn't interested in this item!")
                            else:
                                if randnum <= 95:
                                    self.add_item(want_item, quantity=want_item.quantity)
                                    entity.inventory.remove(want_item)
                                    entity.add_item(give_item, quantity=give_item.quantity)
                                    self.inventory.remove(give_item)
                                    print(villager_name, "was interested in your item! You traded", give_item.rarity, give_item.type, "(" + str(give_item.level) + ") for", want_item.rarity, want_item.type, "(" + str(want_item.level) + ")!")
                                else:
                                    print(villager_name, "isn't interested in this item!")
                        # player item less valuable than desired item
                        # trade success chances decrease as difference in value increases
                        elif give_item.value < want_item.value:
                            randnum = randint(1,100)
                            if value_diff <= 50:
                                if randnum <= 50:
                                    self.add_item(want_item, quantity=want_item.quantity)
                                    entity.inventory.remove(want_item)
                                    entity.add_item(give_item, quantity=give_item.quantity)
                                    self.inventory.remove(give_item)
                                    print(villager_name, "was interested in your item! You traded", give_item.rarity, give_item.type, "(" + str(give_item.level) + ") for", want_item.rarity, want_item.type, "(" + str(want_item.level) + ")!")
                                else:
                                    print(villager_name, "isn't interested in this item!")
                            elif value_diff > 50 and value_diff <= 200:
                                if randnum <= 35:
                                    self.add_item(want_item, quantity=want_item.quantity)
                                    entity.inventory.remove(want_item)
                                    entity.add_item(give_item, quantity=give_item.quantity)
                                    self.inventory.remove(give_item)
                                    print(villager_name, "was interested in your item! You traded", give_item.rarity, give_item.type, "(" + str(give_item.level) + ") for", want_item.rarity, want_item.type, "(" + str(want_item.level) + ")!")
                                else:
                                    print(villager_name, "isn't interested in this item!")
                            elif value_diff > 200 and value_diff <= 500:
                                if randnum <= 25:
                                    self.add_item(want_item, quantity=want_item.quantity)
                                    entity.inventory.remove(want_item)
                                    entity.add_item(give_item, quantity=give_item.quantity)
                                    self.inventory.remove(give_item)
                                    print(villager_name, "was interested in your item! You traded", give_item.rarity, give_item.type, "(" + str(give_item.level) + ") for", want_item.rarity, want_item.type, "(" + str(want_item.level) + ")!")
                                else:
                                    print(villager_name, "isn't interested in this item!")
                            elif value_diff > 500 and value_diff <= 1000:
                                if randnum <= 10:
                                    self.add_item(want_item, quantity=want_item.quantity)
                                    entity.inventory.remove(want_item)
                                    entity.add_item(give_item, quantity=give_item.quantity)
                                    self.inventory.remove(give_item)
                                    print(villager_name, "was interested in your item! You traded", give_item.rarity, give_item.type, "(" + str(give_item.level) + ") for", want_item.rarity, want_item.type, "(" + str(want_item.level) + ")!")
                                else:
                                    print(villager_name, "isn't interested in this item!")
                            else:
                                if randnum <= 5:
                                    self.add_item(want_item, quantity=want_item.quantity)
                                    entity.inventory.remove(want_item)
                                    entity.add_item(give_item, quantity=give_item.quantity)
                                    self.inventory.remove(give_item)
                                    print(villager_name, "was interested in your item! You traded", give_item.rarity, give_item.type, "(" + str(give_item.level) + ") for", want_item.rarity, want_item.type, "(" + str(want_item.level) + ")!")
                                else:
                                    print(villager_name, "isn't interested in this item!")
                    break
                else:
                    print(villager_name, "doesn't have anything to trade!")
            elif entity.name == villager_name and not isinstance(villager_name, Villager):
                print(villager_name, "isn't a villager!")
                break

    def rob(self, villager_name, active_environment):
        rob_chances = {
            "COMMON": 60,
            "UNCOMMON": 40,
            "RARE": 30,
            "LEGENDARY": 10,
            "MYTHICAL": 5
        }
        for entity in active_environment.entity_list:
            if entity.name == villager_name and isinstance(entity, Villager):
                if len(entity.inventory) > 0:
                    for item in entity.inventory:
                        if item.rarity in rob_chances:
                            rob_chance = rob_chances[item.rarity]
                            randnum = randint(1,100)
                            if randnum <= rob_chance:
                                entity.inventory.remove(item)
                                self.add_item(item, quantity=item.quantity)
                                print("You successfully robbed", item.rarity, item.type, "(" + str(item.quantity) + ")!")
                            else:
                                print("You failed to rob", item.rarity, item.type, "(" + str(item.quantity) + ")!")
                    break
                else:
                    print(villager_name, "doesn't have anything!")
            elif entity.name == villager_name and not isinstance(villager_name, Villager):
                print(villager_name, "isn't a villager!")
                break
        self.view_inv()

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
        print("You have gained $" + str(amount) + "!")

    def remove_money(self, amount):
        self.money -= amount
        print("You have lost $" + str(amount) + "!")

    def view_money(self):
        print("You have $" + str(self.money) + "!")

    def heal(self, rarity="COMMON"):
        potion_found = False
        for inventory_item in self.inventory:
            if inventory_item.type == "Potion" and inventory_item.rarity == rarity:
                inventory_item.quantity -= 1
                if inventory_item.quantity <= 0:
                    # print("Removed", str(inventory_item.quantity+quantity), inventory_item.rarity, inventory_item.type + "!")
                    self.inventory.remove(inventory_item)
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
        enemy_characteristics = {
            "Orc": (1, 0.9),
            "Ogre": (1.1, 1.2),
            "Snake": (0.5, 0.9),
            "Goblin": (0.25, 0.5),
            "Savages": (1, 1.5),
            "Bandits": (1, 0.5),
            "Dragon": (10, 10)
        }

        if self.type in enemy_characteristics:
            self.health *= enemy_characteristics[self.type][0]
            self.damage_multiplier = enemy_characteristics[self.type][1]
        
    def fight(self, player):
        damage = int((abs((self.level + 1) - player.level) * randint(0,50)) * self.damage_multiplier)
        player.health -= damage
        if player.health <= 0:
            print(self.name, "the", self.type, "hit you for", str(damage), "health! You have 0 health left!")
        else:
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
        return self.name + " the " + self.type + " is level " + str(self.level) + " and has " + str(self.health) + " health remaining. " + self.name + " has $" + str(self.money) + "."

    def add_money(self, amount):
        self.money += amount
        print(self.name, "the", self.type, "has gained $" + amount + "!")

    def remove_money(self, amount):
        self.money -= amount
        print(self.name, "the", self.type, "has lost $" + amount + "!")

    def add_item(self, item, quantity=1):
        # checks if item is already in inventory
        for inventory_item in self.inventory:
            if inventory_item.type == item.type and inventory_item.rarity == item.rarity:
                # item already exists, update quantity
                inventory_item.quantity += quantity
                # print("Added", quantity, inventory_item.rarity, inventory_item.type + "!")
                return
        # add new item to inventory if not already present 
        item.quantity = quantity
        # print("Added", quantity, item.rarity, item.type + "!")
        self.inventory.append(item)

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

        rarity_value_multiplier = {
            "COMMON": 1,
            "UNCOMMON": 3,
            "RARE": 5,
            "LEGENDARY": 10,
            "MYTHICAL": 25
        }
        if self.rarity in rarity_value_multiplier:
            if self.type == "Potion":
                item_value = rarity_value_multiplier[self.rarity] * 100
            else:
                # min value = 50, max value = 4000
                item_value = randint(50,150) * rarity_value_multiplier[self.rarity] + randint(0,250)
        self.value = item_value
    
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
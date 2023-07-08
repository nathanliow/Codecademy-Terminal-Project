from classes import *
import random

village_name_list = [
    "Dallas",
    "Chicago",
    "San Francisco",
    "Los Angeles",
    "Boston",
    "Denver",
    "Michigan",
    "Austin",
    "Miami",
    "Seattle",
    "Fairyland"
]

enemy_outpost_name_list = [
    "Abandoned Camp",
    "Dusty Railroad",
    "Ruined Temple",
    "Abandoned House",
    "Destroyed Village"
]

dungeon_name_list = [
    "Jungle Dungeon",
    "Desert Dungeon",
    "Fire Dungeon",
    "Lava Dungeon",
    "Earth Dungeon",
    "Crystal Dungeon",
    "Corrupted Dungeon"
]
    
boss_room_name_list = [
    "Dark Lair",
    "The Lair of Monsters",
    "Lair of Chaos",
    "Lair of Madness",
    "Lair of Revenge",
    "Lair of Darkness",
    "Lair of Ache"
]

villager_name_list = [
    "John",
    "Bob",
    "Alice",
    "Merlin",
    "Jane",
    "Jill",
    "Eric",
    "Jon",
    "Nathan",
    "Paul",
    "David",
    "Jonah",
    "Elijah",
    "Jose",
    "Khan",
    "Diana",
    "Moe"
]

item_type_list = [
    "Potion",
    "Stone Sword",
    "Metal Sword",
    "Crystal Sword",
    "Platinum Sword",
    "Obsidian Sword",
    "Diamond Sword",
    "Bow",
    "Battleaxe",
    "Pickaxe",
    "Crossbow",
    "Machete",
    "Scimitar",
    "Katana",
    "Axe",
    "Hatchet",
    "Longbow",
    "Compound Bow",
    "Pike",
    "Stick",
    "Baton",
    "Crowbar",
    "Hammer"
]

enemy_type_list = [
    "Rat",
    "Crow",
    "Orc",
    "Ogre",
    "Golem",
    "Snake",
    "Goblin",
    "Savage",
    "Bandit",
    "Ravager",
    "Dragon"
]
    
enemy_name_list = [
    "Grimshadow",
    "Vilestrike",
    "Doombringer",
    "Dreadfang",
    "Grimjaw",
    "Bloodthorn",
    "Darkheart",
    "Venomspine",
    "Blackthorn",
    "Ironhide",
    "Ghostwalker",
    "Nightshade",
    "Destroyer",
    "Spineless",
    "Reaper",
    "Soulreaper",
    "Bonecrusher",
    "Deathshroud",
    "Crawler",
    "Stormfury",
    "Doomclaw",
    "Wailer",
    "Blightbane"
]

village_description_list = [
    "Tranquil haven nestled amidst rolling hills and lush meadows.",
    "Idyllic village known for its warm hospitality and charming cottages.",
    "Picturesque hamlet with colorful flower gardens and quaint cobblestone streets.",
    "Serene retreat with a babbling brook and peaceful countryside.",
    "Welcoming community surrounded by verdant forests and crystal-clear lakes.",
    "Quaint village brimming with cheerful locals and a bustling marketplace.",
    "Charming settlement renowned for its festive celebrations and lively folk music.",
    "Peaceful enclave where time seems to stand still, offering respite from the outside world.",
    "Harmonious village where everyone knows each other, fostering a strong sense of community.",
    "Rustic haven filled with cozy cottages, where the aroma of freshly baked bread wafts through the air."
]

enemy_description_list = [
    "Perilous domain shrouded in darkness, where danger lurks at every turn.",
    "Forsaken wasteland haunted by malevolent forces, devoid of any signs of life.",
    "Desolate stronghold teeming with hostile warriors, their eyes filled with malice.",
    "Savage realm ruled by a ruthless warlord, with fear and oppression gripping its inhabitants.",
    "Treacherous territory infested with cunning bandits and merciless mercenaries.",
    "Blighted land ravaged by constant warfare, its landscape scarred by the echoes of battle.",
    "DO NOT ENTER...",
    "Cursed Domain Cursed Domain Cursed Domain Cursed Domain Cursed Domain Cursed Domain",
    "Grim fortress standing tall amidst the desolation, guarded by ruthless sentinels.",
    "Harsh wilderness overrun by feral creatures, their menacing growls echoing through the air.",
    "Tangled thicket harboring vile beasts, their eyes gleaming with hunger and aggression.",
    "Blistering badlands where only the most hardened survive, its barren landscape devoid of mercy.",
    "ENTER AT YOUR OWN RISK...",
    "WARNING: DANGEROUS",
    "Many do not come out alive..."
]

environment_list = []

# Generate random environments
for i in range(randint(20,50)):
    environment_types = ["Village", "Enemy Outpost", "Dungeon", "Boss Room"]
    environment_weights = (10, 5, 4, 1)
    environment_type = random.choices(environment_types, weights=environment_weights, k=1)[0]
    if environment_type == "Village":
        environment_name = random.choice(village_name_list)
    elif environment_type == "Enemy Outpost":
        environment_name = random.choice(enemy_outpost_name_list)
    elif environment_type == "Dungeon":
        environment_name = random.choice(dungeon_name_list)
    elif environment_type == "Boss Room":
        environment_name = random.choice(boss_room_name_list)
    environment_level = random.randint(1, 20)
    if environment_type == "Village":
        environment_description = random.choice(village_description_list)
    else:
        environment_description = random.choice(enemy_description_list)
    entities = []
    items = []

    if environment_type == "Village":
        # Generate random villagers
        num_villagers = random.randint(1, 4)
        for i in range(num_villagers):
            villager_name = random.choice(villager_name_list) 
            villager_inventory = []
            villager_money = randint(0,500)
            
            # Generate random items for each villager
            num_items = random.randint(0, 3)
            for i in range(num_items):
                item_type = random.choice(item_type_list)  
                rarities = ["COMMON", "UNCOMMON", "RARE", "LEGENDARY", "MYTHICAL"]
                rarity_weights = (40, 30, 15, 10, 5)
                item_rarity = random.choices(rarities, weights=rarity_weights, k=1)[0]
                item_level = random.randint(1, 5)
                item_quantity = random.randint(1, 3)
                item = Item(item_type, item_rarity, item_level, item_quantity)
                villager_inventory.append(item)
            villager = Villager("Villager", villager_name, inventory=villager_inventory, level=environment_level+randint(0,2), money=villager_money)
            entities.append(villager)

    if environment_type != "Village":
        if environment_type == "Boss Room":
            # Generate random enemies
            num_enemies = random.randint(1, 3)
            for i in range(num_enemies):
                enemy_type = "Dragon"
                enemy_name = random.choice(enemy_name_list)
                enemy = Enemy(enemy_type, enemy_name, level=environment_level+randint(0,2))
                entities.append(enemy)
        else:
            # Generate random enemies
            num_enemies = random.randint(1, 3)
            for i in range(num_enemies):
                enemy_type = random.choice(enemy_type_list)
                enemy_name = random.choice(enemy_name_list)
                enemy = Enemy(enemy_type, enemy_name, level=environment_level+randint(0,2))
                entities.append(enemy)

    if environment_type == "Dungeon":
        # Generate random items in the dungeon environment
        num_items_in_environment = random.randint(0, 5)
        for i in range(num_items_in_environment):
            item_type = random.choice(item_type_list)
            rarities = ["COMMON", "UNCOMMON", "RARE", "LEGENDARY", "MYTHICAL"]
            rarity_weights = (40, 30, 15, 10, 5)
            item_rarity = random.choices(rarities, weights=rarity_weights, k=1)[0]
            item_level = random.randint(1, 5)
            item_quantity = random.randint(1, 3)
            item = Item(item_type, item_rarity, item_level, item_quantity)
            items.append(item)

    environment = Environment(environment_name, environment_level, environment_type, environment_description, entities, items)
    environment_list.append(environment)
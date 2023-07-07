from classes import *

environment_list = [
    Environment(
        "Dallas", 
        1, 
        "Village", 
        "A bustling village at the center of the world, great for trading and training.", 
        [Villager("Librarian", "Joe", inventory=[Item("Battleaxe", "COMMON", level=1, quantity=1), Item("Bow", "COMMON", level=1, quantity=1), Item("Potion", "COMMON", level=1, quantity=1)]), Villager("Blacksmith", "Aaron"), Villager("Magician", "John"), Enemy("Ogre", "EEE")]
        ),
    
    Environment(
        "Ogre Camp", 
        5, 
        "Enemy Outpost", 
        "A congregation of green grumpy ogres.", 
        [Enemy("Ogre", "Eric"), Enemy("Ogre", "Eel"), Enemy("Ogre", "Erica")]
        ),
    
    Environment(
        "Snake Dungeon", 
        10, 
        "Dungeon", 
        "A den of dangerous and venomous snakes may hold great treasures.", 
        [Enemy("Snake", "Moma"), Enemy("Snake", "Mama"), Enemy("Snake", "Memo")], 
        [Item("Sword", "COMMON", level=1, quantity=5), Item("Bow", "RARE", level=1, quantity=3), Item("Pickaxe", "COMMON", level=4)]
        ),
    
    Environment(
        "The Dragon's Lair", 
        20, 
        "Boss Room", 
        "ENTER AT YOUR OWN RISK...", 
        [Enemy("Dragon", "Drakor")]
        )
]
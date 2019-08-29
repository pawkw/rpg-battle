import colorama
from classes.characters import Character
from classes.monsters import *
from classes.colours import Colours
from classes.controllers import Controller
from classes.magic import *
from classes.items import *

spell_book = [fire_ball, flame, heal, heal_all]

# Player characters
player1 = Character("user", "Valos", True, 12, 0, 5, 5, 5, 0, 2, 0, [Inventory_entry(healing_potion, 1)])
player2 = Character("user", "Gimli", True, 14, 0, 4, 7, 5, 0, 1, 0, [Inventory_entry(mana_shard, 1)])
player3 = Character("user", "Jay", True, 10, 12, 2, 3, 3, 2, 1, 0,[], {}, spell_book)

players = [player3, player1, player2]

# NPCs
enemy1 = Hobgoblin()
enemy2 = Ice_goblin()
enemy3 = Fire_goblin()
# enemy2 = Goblin()
# enemy3 = Goblin()

enemies = [enemy1, enemy2, enemy3]

if __name__ == "__main__":
    # Initiate terminal colours for Windows
    colorama.init()
    print("Hello "+Colours.RED+"THERE"+Colours.END+"!")

    running = True
    while running:
        # Print out status
        print("\n"+"="*25)
        print("Name                       HP                                  MP")
        for player in players:
            player.print_status(Colours.YELLOW, Colours.GREEN)
        for enemy in enemies:
            enemy.print_status(Colours.RED, Colours.RED, True)

        for player in players:
            player.move(players, enemies)

        print("\n"+"-"*25)
        for enemy in enemies:
            enemy.move(enemies, players)
        
        if not enemies or not players:
            running = False
    
    if not enemies:
        print(Colours.GREEN+"You have overcome your enemies!"+Colours.END)
    else:
        print(Colours.RED+"You have been defeated!"+Colours.END)


    # Return terminal colours to normal for Windows
    colorama.deinit()
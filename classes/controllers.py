import random
from classes.colours import Colours
from classes.helpers import get_choice, stop_on_error

class Controller:
    def __init__(self, character, controller_type):
        self.character = character
        self.controller_type = controller_type

    def run(self, allies, enemies):
        if self.controller_type == "user":
            self.user(allies, enemies)
        elif self.controller_type == "thug boss":
            self.thug_boss(allies, enemies)
        elif self.controller_type == "thug":
            self.thug(allies, enemies)
        else:
            stop_on_error("Controller type does not exist: "+self.controller_type)

    def user(self, allies, enemies):
        self.character.reset_defending()
        action_list = ["Attack", "Defend"]
        if self.character.get_max_magic_points() > 0:
            action_list.append("Cast spell")
        if self.character.get_inventory():
            action_list.append("Use item")
        choice = -1
        while choice == -1 and enemies:
            choice = get_choice(self.character.get_name()+" actions", action_list)
            choice = action_list[choice]
            names = [x.name for x in enemies]
            if choice == "Attack":
                choice = get_choice("Target", names, True)
                if choice == -1:
                    continue
                target = enemies[choice]
                self.character.attack_weapon(target)
                if target.is_dead():
                    print(Colours.RED+target.get_The_name()+" has been killed by "+self.character.get_the_name()+"!"+Colours.END)
                    enemies.remove(target)
            elif choice == "Defend":
                self.character.set_defending()
            elif choice == "Cast spell":
                names = [x.name+" - "+str(x.cost)+": "+x.description for x in self.character.spell_book]
                choice = get_choice("Spell", names, True)
                if choice == -1:
                    continue
                spell = self.character.spell_book[choice]
                success = spell.cast(self.character, allies, enemies)
                if not success:
                    choice = -1
                    continue

                # Some spells affect multiple targets.
                for target in enemies:
                    if target.is_dead():
                        print()
                        print(Colours.RED+target.get_The_name()+" has been killed by "+self.character.get_the_name()+"!"+Colours.END)
                        enemies.remove(target)
            elif choice == "Use item":
                names = [x.item.name+" (x"+str(x.quantity)+") : "+x.item.description for x in self.character.inventory]
                choice = get_choice("Item", names, True)
                if choice == -1:
                    continue
                item = self.character.inventory[choice].item
                success = item.use(self.character, allies, enemies)
                if not success:
                    choice = -1
                    continue
                self.character.inventory[choice].quantity -= 1
                if self.character.inventory[choice].quantity == 0:
                    self.character.inventory.remove(self.character.inventory[choice])
                
            else:
                stop_on_error("Choice: "+choice+" does not exist.")


    # Thug boss may have extra inventory items.
    def thug_boss(self, allies, enemies):
        if not enemies:
            return
        target = enemies[random.randrange(0, len(enemies))]
        self.character.attack_weapon(target)
        if target.is_dead():
            print(Colours.RED+target.get_The_name()+" has been killed!"+Colours.END)
            enemies.remove(target)

    # Thugs do not have extra inventory items.
    def thug(self, allies, enemies):
        if not enemies:
            return
        target = enemies[random.randrange(0, len(enemies))]
        self.character.attack_weapon(target)
        if target.is_dead():
            print(Colours.RED+target.get_The_name()+" has been killed!"+Colours.END)
            enemies.remove(target)
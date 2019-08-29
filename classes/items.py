# Item type can be:
# - heal - heals target
# - mana - increases magic points
# - restore - restores magic and hit points to full
# - attack

from classes.helpers import get_choice

class Item:
    def __init__(self, name, description, item_type, element, prop, targets):
        self.name = name
        self.description = description
        self.item_type = item_type
        self.targets = targets
        self.element = element
        self.prop = prop
    
    def use(self, user, allies, enemies):
        if self.item_type == "heal" or self.item_type == "mana":
            if self.targets == "ally":
                names = [x.get_The_name()+" - HP: "+x.get_hp_status_string()+" MP: "+x.get_mp_status_string() for x in allies]
                choice = get_choice("Target", names, True)
                if choice == -1:
                    return False
                target = allies[choice]
                user.attack_item(target, self.name, self.prop, self.element)
                return True

class Inventory_entry:
    def __init__(self, item, quantity):
        self.item = item
        self.quantity = quantity

    def use(self, user, allies, enemies):
        if self.quantity < 1:
            return False
        result = self.item.use(user, allies, enemies)
        return result

healing_potion = Item("Healing potion", "Heals 6 points to one ally.", "heal", "heal", 6, "ally")
mana_chrystal = Item("Mana chrystal", "Adds 6 magic points to all allies.", "mana", "mana", 6, "allies")
mana_shard = Item("Mana shard", "Adds 4 magic points to one ally.", "mana", "mana", 4, "ally")

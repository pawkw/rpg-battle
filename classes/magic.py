# Elements
# - Earth
# - Wind
# - Fire
# - Ice
# - Water
# - Electricity
# - Metamorph
# - Time

from classes.helpers import get_choice, stop_on_error

class Spell:
    def __init__(self, name, description, element, cost, damage, targets):
        self.name = name
        self.description = description
        self.element = element
        self.cost = cost
        self.damage = damage
        self.targets = targets

    def cast(self, caster, allies, enemies, report = True):
        if self.cost > caster.get_magic_points():
            print("Not enough magic points!")
            return False
        if self.targets == "ally":
            names = [x.get_The_name()+" - "+x.get_hp_status_string() for x in allies]
            choice = get_choice("Target", names, True)
            if choice == -1:
                return False
            target = allies[choice]
            caster.attack_magic(target, self.name, self.cost, self.damage, self.element)
        elif self.targets == "enemy":
            names = [x.get_The_name()+" - "+x.get_hp_status_string() for x in enemies]
            choice = get_choice("Target", names, True)
            if choice == -1:
                return False
            target = enemies[choice]
            caster.attack_magic(target, self.name, self.cost, self.damage, self.element)
        elif self.targets == "allies":
            for target in allies:
                caster.attack_magic(target, self.name, self.cost, self.damage, self.element)
        elif self.targets == "enemies":
            for target in enemies:
                caster.attack_magic(target, self.name, self.cost, self.damage, self.element)
        elif self.targets == "self":
            caster.attack_magic(caster, self.name, self.cost, self.damage, self.element)
        else:
            stop_on_error("Failed in magic.py Spell.cast - "+caster.get_The_name()+" "+self.name)
        caster.reduce_magic_points(self.cost)
        return True

# Spells
fire_ball = Spell("Fire ball", "Hits one enemy with a fire ball.", "fire", 2, 10, "enemy")
flame = Spell("Flame", "Hit all enemies with fire.", "fire", 4, 6, "enemies")
heal = Spell("Heal", "Heal one person for 6 hit points.", "heal", 2, 6, "ally")
heal_all = Spell("Heal all", "Heal all allies 4 hit points.", "heal", 4, 4, "allies")
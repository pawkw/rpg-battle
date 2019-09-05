import random
from classes.colours import Colours
from classes.controllers import Controller

class Character:
    def __init__(self, controller_type, name, proper_name, hit_points, magic_points, attack, attack_damage, defense, magic_resistance, speed, experience, inventory = [], elemental_resistance = {}, spell_book = []):
        self.name = name
        self.controller_type = controller_type
        self.proper_name = proper_name
        self.hit_points = hit_points
        self.max_hit_points = hit_points
        self.magic_points = magic_points
        self.max_magic_points = magic_points
        self.attack = attack
        self.attack_damage = attack_damage
        self.defense = defense
        self.magic_resistance = magic_resistance
        self.speed = speed
        self.experience = experience
        self.elemental_resistance = elemental_resistance
        self.spell_book = spell_book
        self.inventory = inventory
        self.defending = False
        self.controller = Controller(self, self.controller_type)

    def set_controller(self, controller):
        self.controller = controller

    def move(self, player_party, enemies):
        self.controller.run(player_party, enemies)

    # Return damage from 90% to 110% of attack damage.
    def generate_damage(self):
        return random.randrange(int(self.attack_damage*.9), int(self.attack_damage*1.1))

    def attack_weapon(self, target, report = True):
        if report:
            print("\n"+Colours.YELLOW+self.get_The_name()+" attacks "+target.get_the_name()+"."+Colours.END)
        outcome = target.receive_attack(self, self.get_attack(), self.generate_damage(), "weapon", False, report)
        if outcome:
            self.experience += outcome

    def attack_magic(self, target, spell_name, magic_points, damage, element, report = True):
        if report:
            print("\n"+Colours.BLUE+self.get_The_name()+" casts "+spell_name+" on "+target.get_the_name()+"."+Colours.END)
        outcome = target.receive_attack(self, magic_points, damage, "magic", element, report)
        if outcome:
            self.experience += outcome

    def attack_item(self, target, item_name, damage, element, report = True):
        if report:
            print("\n"+Colours.YELLOW+self.get_The_name()+" uses the "+item_name.lower()+" on "+target.get_the_name()+"."+Colours.END)
        outcome = target.receive_attack(self, self.get_attack(), damage, "item", element, report)
        if outcome:
            self.experience += outcome

    def receive_attack(self, attacker, attack_strength, attack_damage, attack_type, element = False, report = True):
        if attack_type == "weapon":
            # Compare attack strength against self.defense.
            # Elemental dammage won't occur unless there is a hit first.
            outcome = random.randrange(0, self.defense+attack_strength+1)
            # print("Attack:",attack, "Defense:", self.defense, "Outcome:", outcome)
            if outcome <= self.defense:
                if report:
                    print(Colours.YELLOW+self.get_The_name()+" successfully defends against "+attacker.get_the_name()+"."+Colours.END)
                return False
            else:
                damage = 0

                # If the character is defending, it does not affect elemental damage.
                if element:
                    resistance = 0 if element not in self.elemental_resistance else self.elemental_resistance[element]
                    if resistance > 0:
                        damage += int(attack_damage/(resistance+1))
                    elif resistance < 0:
                        damage += attack_damage*-resistance
                    else:
                        damage += attack_damage

                # If the character is defending, weapon damage is halved.
                damage += attack_damage//2 if self.defending else attack_damage

                if report:
                    print(Colours.RED+attacker.get_The_name()+" hits "+self.get_the_name()+" for "+str(damage)+" damage!"+Colours.END)
                self.take_damage(damage)
                return damage

        elif attack_type == "magic" or attack_type == "item":
            # Do not resist healing spells
            if element == "heal":
                self.heal(attack_damage)
                if report:
                    print(Colours.GREEN+self.get_The_name()+" is healed "+str(attack_damage)+" points."+Colours.END)
                return attack_damage

            # Do not resist mana spells
            if element == "mana":
                self.increase_magic_points(attack_damage)
                if report:
                    print(Colours.BLUE+self.get_The_name()+" receives "+str(attack_damage)+" magic points."+Colours.END)
                return attack_damage

            resistance = self.magic_resistance if element not in self.elemental_resistance else self.elemental_resistance[element]

            # Compare attack strength against self.defense.
            # Elemental dammage won't occur unless there is a hit first.
            outcome = 1
            if resistance > 0:
                outcome = random.randrange(0, resistance+attack_strength+1)
            # print("Attack:",attack_strength, "Resistance:", resistance, "Outcome:", outcome)
            if outcome <= resistance:
                if report:
                    print(Colours.YELLOW+self.get_The_name()+" resists the spell."+Colours.END)
                return False

            if resistance > 0:
                damage = int(attack_damage/(resistance+1))
            elif resistance < 0:
                damage = attack_damage*-resistance
            else:
                damage = attack_damage

            self.take_damage(damage)
            if report:
                print(Colours.RED+self.get_The_name()+" is hit for "+str(damage)+" points "+element+" damage!"+Colours.END)
            return damage

    def take_damage(self, damage):
        self.hit_points -= damage
        if self.hit_points < 0:
            self.hit_points = 0

    def heal(self, damage):
        self.hit_points += damage
        if self.hit_points > self.max_hit_points:
            self.hit_points = self.max_hit_points

    def restore(self):
        self.hit_points = self.max_hit_points
        self.magic_points = self.max_magic_points

    def increase_magic_points(self, magic_points):
        self.magic_points += magic_points
        if self.magic_points > self.max_magic_points:
            self.magic_points = self.max_magic_points

    def reduce_magic_points(self, magic_points):
        self.magic_points -= magic_points
        if self.magic_points < 0:
            self.magic_points = 0

    def set_defending(self, report = True):
        self.defending = True
        if report:
            print(Colours.YELLOW+self.get_name()+" is defending."+Colours.END)

    def reset_defending(self):
        self.defending = False

    def get_hp_status_string(self):
        return str(self.get_hit_points())+"/"+str(self.get_max_hit_points())

    def get_mp_status_string(self):
        return str(self.get_magic_points())+"/"+str(self.get_max_magic_points())

    def print_status(self, name_colour, bar_colour, hide_magic_points = False):
        hp_bar_length = 61 if hide_magic_points else 25
        hp_bar = "█"*int(self.get_hit_points()/self.get_max_hit_points()*hp_bar_length)
        name = self.get_name()+":"

        mp_bar = " "*25
        mp_num = "      0/0"

        output = name_colour + name.ljust(15) + Colours.END + " " + self.get_hp_status_string().rjust(9) + " |" + bar_colour + hp_bar.ljust(hp_bar_length) + Colours.END + "|"

        if self.get_max_magic_points() != 0 and not hide_magic_points:
            mp_bar = "█"*int(self.get_magic_points()/self.get_max_magic_points()*25)
            output += self.get_mp_status_string().rjust(8) + " |" + Colours.BLUE + mp_bar.ljust(25) + Colours.END + "|"
        print(output)

    def is_dead(self):
        return self.hit_points == 0

    def get_attack(self):
        return self.attack

    def get_name(self):
        return self.name

    def get_The_name(self):
        if self.proper_name:
            return self.get_name()
        return "The "+self.get_name().lower()

    def get_the_name(self):
        if self.proper_name:
            return self.get_name()
        return "the "+self.get_name().lower()

    def get_hit_points(self):
        return self.hit_points

    def get_max_hit_points(self):
        return self.max_hit_points

    def get_magic_points(self):
        return self.magic_points

    def get_max_magic_points(self):
        return self.max_magic_points

    def get_experience(self):
        return self.experience

    # Return false if there is no inventory, otherwise the inventory list.
    def get_inventory(self):
        if not self.inventory:
            return False
        return self.inventory

from classes.characters import Character

class Hobgoblin(Character):
    def __init__(self):
        super().__init__("thug boss","Hobgoblin", False, 20, 0, 5, 5, 5, 0, 1, 0)

class Goblin(Character):
    def __init__(self):
        super().__init__("thug", "Goblin", False, 10, 0, 3, 3, 2, 0, 3, 0)

class Fire_goblin(Character):
    def __init__(self):
        super().__init__("thug", "Fire goblin", False, 20, 0, 3, 3, 2, 0, 3, 0, [], {"fire": 8})

class Ice_goblin(Character):
    def __init__(self):
        super().__init__("thug", "Ice goblin", False, 40, 0, 3, 3, 2, 0, 3, 0, [], {"fire": -8})
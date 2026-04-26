import random

class Player:
    def __init__(self, name):
        self.points = 0
        self.alive = True
        self.active_instructions = {"w": False,
                                    "a": False,
                                    "s": False,
                                    "d": False,
                                    "shoot": False}
        
    def update(self, w, a, s, d, shoot):
        self.active_instructions = {"w": w,
                                    "a": a,
                                    "s": s,
                                    "d": d,
                                    "shoot": shoot}
        
    def get_instructions(self):
        return self.active_instructions
    
    def is_bot(self):
        return False
    

class BotPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
    
    def update(self):
        self.active_instructions = {"w": random.choice([True, False]),
                                    "a": random.choice([True, False]),
                                    "s": random.choice([True, False]),
                                    "d": random.choice([True, False]),
                                    "shoot": random.choice([True, False])}
    def is_bot(self):
        return True
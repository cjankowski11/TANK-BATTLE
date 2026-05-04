import random
import pygame
import stable_baselines3

class Player:
    def __init__(self, name):
        self.name = name
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
    
    def add_point(self):
        self.points += 1
    
    

class BotPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.walls = []
        self.bullets = []
        self.players = {}

    
    def update(self):
        self.active_instructions = {"w": random.choice([True, False]),
                                    "a": random.choice([True, False]),
                                    "s": random.choice([True, False]),
                                    "d": random.choice([True, False]),
                                    "shoot": random.choice([True, False])}
    def is_bot(self):
        return True
    
    def update_walls(self, walls):
        self.walls = walls

    def update_players(self, players):
        self.players = players

    def update_bullets(self, bullets):
        self.bullets = bullets

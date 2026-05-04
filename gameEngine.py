import pygame
import random
from tank.tankEngine import TankEngine
import struct
import math


class GameEngine:
    def __init__(self, players_names, game_map, ticks_per_sec):
        self.ticks_per_sec = ticks_per_sec
        self.walls = []
        self.screen_width = 800
        self.screen_height = 450
        self.tank_amunition = 8
        with open(game_map, "r") as f:
            for line in f:
                wall = line.strip().split(",")
                self.walls.append(pygame.Rect(int(wall[0]), int(wall[1]), int(wall[2]), int(wall[3])))
                self.players = {}
        for name in players_names:
            start_pos = self.get_start_pos(self.screen_width, self.screen_height)
            self.players[name] = TankEngine(start_pos, random.randint(0, 360), self.tank_amunition, ticks_per_sec)
        self.bullets = []

    def is_finished(self):
        alive_count = 0
        for tank in self.players.values():
            if tank.is_alive():
                alive_count += 1
        return True if alive_count < 2 else False

    def update_player(self, player, w, a, s, d, shoot):
        tank = self.players[player]
        if not tank.is_alive():
            return False
        old_angle = tank.angle
        old_pos = tank.position.copy()

        if self.check_tank_bullets_collision(tank):
            tank.alive = False

        tank.update_reload_cooldown()
        tank.update_shoot_cooldown()

        if tank.is_able_to_reload():
            tank.reload_bullet()
        if a:
            tank.angle += 2
        if d:
            tank.angle -= 2

        tank.angle %= 360

        if self.check_collision(tank):
            tank.angle = old_angle 

        move_x = 0
        move_y = 0
        rad = math.radians(tank.angle)

        if w:
            move_x -= math.sin(rad) * 1
            move_y -= math.cos(rad) * 1
        if s:
            move_x += math.sin(rad) * 1
            move_y += math.cos(rad) * 1

        tank.position.x += move_x
        if self.check_collision(tank):
            tank.position.x = old_pos.x 

        tank.position.y += move_y
        if self.check_collision(tank):
            tank.position.y = old_pos.y 

        if shoot and tank.is_able_to_shoot():
            bullet = tank.shoot()
            self.bullets.append(bullet)

    def update_bullets(self):
        bullets_to_remove = []
        for bullet in self.bullets:
            bullet.update_exst_time()
            if not bullet.is_existing() or self.check_bullet_walls_collision(bullet):
                bullets_to_remove.append(bullet)
        for bullet in bullets_to_remove:
            self.bullets.remove(bullet)
        
        for bullet in self.bullets:

            rad = math.radians(bullet.angle)
            bullet.position.x -= math.sin(rad) * 1.5
            bullet.position.y -= math.cos(rad) * 1.5


    def get_players(self, binary=False):
        if binary:
            buffor = struct.pack("B", len(self.players))
            for name, tank in self.players.items():
                buffor += struct.pack("20s", name.encode())
                buffor += struct.pack("fffB", tank.position.x, tank.position.y, tank.angle, tank.bullets_left)
            return buffor
        return self.players

    def get_walls(self, binary=False):
        if binary:
            buffor = struct.pack("B", len(self.walls))
            for wall in self.walls:
                buffor += struct.pack("<HHHH", wall.left, wall.top, wall.width, wall.height)
            return buffor
        return self.walls
    
    def get_start_pos(self, screen_w, screen_h):  # TO DO: prevent from spawning in walls

        while True:
            x = random.randint(50, screen_w - 50)
            y = random.randint(100, screen_h)
            if not self.check_starting_collision(x, y):
                return pygame.Vector2(x, y)

    
    def get_bullets(self, binary=False):
        if binary:
            buffor = struct.pack("B", len(self.bullets))
            for bullet in self.bullets:
                buffor += struct.pack("ffH", bullet.position.x,
                                      bullet.position.y, bullet.existence_time)
            return buffor
        return self.bullets
    
    def check_starting_collision(self, x, y): #horrible sollution. Only for now
        tank_rect = pygame.Rect(0, 0, 20, 20)
        tank_rect.center = (int(x), int(y))
        for wall in self.walls:
            if wall.colliderect(tank_rect):
                return True
        return False


    def check_collision(self, tank):          # there is for sure a better way to write it than
        tank_rect = pygame.Rect(0, 0, 20, 20)   # mulitiplicate function for every collisoin
        tank_rect.center = (int(tank.position.x), int(tank.position.y))

        for wall in self.walls:
            if wall.colliderect(tank_rect):
                return True
        return False
    
    def check_bullet_walls_collision(self, bullet):
        bullet_rect = pygame.Rect(0, 0, 5, 5)
        bullet_rect.center = (int(bullet.position.x), int(bullet.position.y))
        for wall in self.walls:
            if wall.colliderect(bullet_rect):
                return True
        return False
    
    def check_tank_bullets_collision(self, tank):
        tank_rect = pygame.Rect(0, 0, 20, 20)
        tank_rect.center = (int(tank.position.x), int(tank.position.y))
        for bullet in self.bullets:
            bullet_rect = pygame.Rect(0, 0, 5, 5)
            bullet_rect.center = (int(bullet.position.x), int(bullet.position.y))
            if tank_rect.colliderect(bullet_rect):
                return True
        return False
    
    def get_winner(self):
        winner = None
        for player, tank in self.players.items():
            if tank.is_alive():
                winner = player
        return winner



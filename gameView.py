import pygame
from tank.tankView import TankView
from bullet.BulletView import BulletView
class GameView:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 450))
        self.walls = []
        self.players = {}
        self.tank_images = [
            pygame.transform.scale_by(pygame.image.load("graphics/tank_1/tank_9x9.png").convert_alpha(), 4),
            pygame.transform.scale_by(pygame.image.load("graphics/tank_1/tank_1.png").convert_alpha(), 4),
            pygame.transform.scale_by(pygame.image.load("graphics/tank_1/tank_1.png").convert_alpha(), 4),
            pygame.transform.scale_by(pygame.image.load("graphics/tank_1/tank_1.png").convert_alpha(), 4)
        ]
        self.bullet_images = [pygame.transform.scale_by(pygame.image.load("graphics/bullet.png").convert_alpha(), 4)]
        self.bullets = []


    def draw_game(self):
        self.screen.fill("white")
        for wall in self.walls:
            pygame.draw.rect(self.screen, "black", wall)
        for tank in self.players.values():
            # print(tank.position)
            tank.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        pygame.display.update()
    
    def update_player(self, name, x, y, angle, bullets):
        self.players[name].position.x = x
        self.players[name].position.y = y
        self.players[name].angle = angle
        self.players[name].bullets = bullets

    def update_walls(self, walls):
        self.walls = walls

    def initialize_players(self, players):
        for i, (name, stats) in enumerate(players.items()):
            x, y, angle, bullets = stats
            self.players[name] = TankView(pygame.Vector2(x, y), angle, bullets, self.tank_images[i])

    def update_bullets(self, bullets):
        new_bullets = []
        for bullet in bullets:
            x, y, time = bullet
            new_bullets.append(BulletView(pygame.Vector2(x, y), time, self.bullet_images[0]))
        self.bullets = new_bullets

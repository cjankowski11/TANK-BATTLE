from bullet.bullet import Bullet
import pygame

class BulletView(Bullet):
    def __init__(self, position, time_of_existence, img):
        super().__init__(position)
        self.image = img
        self.time_of_existence = time_of_existence


    def draw(self, screen):
        screen.blit(self.image, self.position)
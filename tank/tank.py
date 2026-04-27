from bullet.bulletEngine import BulletEngine
import time


class Tank:
    def __init__(self, start_pos, angle, bullets):
        self.position = start_pos
        self.angle = angle
        self.bullets_left = bullets
        self.alive = True

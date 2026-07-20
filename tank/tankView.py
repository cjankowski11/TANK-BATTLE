from tank.tank import Tank
import pygame


class TankView(Tank):
    def __init__(self, start_pos, angle, bullets, img):
        super().__init__(start_pos, angle, bullets)
        self.image = img
    
    @classmethod
    def from_tank_engine_object(cls, tank_engine, img):
        return cls(
            start_pos=tank_engine.position.copy(),
            angle=tank_engine.angle,
            bullets=tank_engine.bullets_left,
            img=img
        )

    def draw(self, screen):
        rotated_tank = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_tank.get_rect(center=self.position)
        screen.blit(rotated_tank, new_rect)
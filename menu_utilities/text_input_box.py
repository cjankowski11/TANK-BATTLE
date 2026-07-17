import pygame
from menu_utilities.text import Text

INACTIVE_COLOR = (100, 100, 100)
ACTIVE_COLOR = (255, 255, 255)


class TextInputBox:
    def __init__(self, x, y, width, height, font_name="ka1.ttf", font_size=30, max_letters=15):
        self.rect = pygame.Rect(x, y, width, height)
        self.active = False
        self.color = INACTIVE_COLOR
        self.max_letters = max_letters
        self.font_name = font_name
        self.font_size = font_size
        
        self.text_x = x + 10
        self.text_y = y + (height - font_size) // 2
        
        self.text_obj = Text(
            text="",
            x=self.text_x,
            y=self.text_y,
            color=ACTIVE_COLOR,
            font_name=font_name,
            font_size=font_size
        )

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, width=2, border_radius=12)
        self.text_obj.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            self.color = ACTIVE_COLOR if self.active else INACTIVE_COLOR

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                new_text = self.text_obj.text[:-1]
                self.text_obj.change_text(new_text)
            elif event.key == pygame.K_RETURN:
                self.active = False
                self.color = INACTIVE_COLOR
            else:
                if (self.text_obj.text_surf.get_width() < self.rect.width - 30 
                    and len(self.text_obj.text) < self.max_letters):
                    new_text = self.text_obj.text + event.unicode
                    self.text_obj.change_text(new_text)
                    
    def change_to_sysfont(self, font="arial", font_size=30):
        self.text_y = self.rect.y + (self.rect.height - font_size) // 2
        self.text_obj.pos = (self.text_x, self.text_y)
        
        self.text_obj.change_to_sysfont(font, font_size)

    def get_text(self):
        return self.text_obj.text
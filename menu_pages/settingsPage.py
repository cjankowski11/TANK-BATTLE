from menu_utilities.button import Button


class SettingsPage:
    def __init__(self):
        self.back_button = Button("BACK", 100, 100, 100, 100, 30)

    def draw_page(self, screen):
        self.back_button.draw(screen)

    def is_page_changed(self, event):
        if self.back_button.is_clicked(event):
            return "MENU"
        return None
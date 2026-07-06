from menu_utilities.button import Button
from menu_utilities.text import Text
from menu_utilities.text_input_box import TextInputBox


class GetNamePage:
    def __init__(self, info, socket):
        self.info = info
        self.back_button = Button("BACK", 100, 100, 100, 100,
                                  (50, 50, 200), (80, 80, 250), 30)
        self.submit_button = Button("SUBMIT", 600, 330, 150, 100,
                                    (50, 50, 200), (80, 80, 250), 30)
        self.name_text = TextInputBox(300, 200, 400, 100)
        self.instruction_text = Text("Write your nickname", 300, 150)

        self.socket = socket

    def draw_page(self, screen):
        self.back_button.draw(screen)
        self.instruction_text.draw(screen)
        self.submit_button.draw(screen)
        self.name_text.draw(screen)

    def is_page_changed(self, event):
        if self.back_button.is_clicked(event):
            return "PLAY"
        if self.submit_button.is_clicked(event):
            name = self.name_text.text_obj.text
            self.is_name_taken(name)
            self.info.name = self.name_text.text_obj.text
            return "ONLINE_LOBBY"
        self.name_text.handle_event(event)
        return None
    
    def is_name_taken(self, name):
        pass

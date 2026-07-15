from menu_utilities.button import Button
from menu_utilities.text import Text
from menu_utilities.text_input_box import TextInputBox
import struct

class GetNamePage:
    def __init__(self, info, socket, host, port):
        self.info = info
        self.back_button = Button("BACK", 100, 100, 100, 100,
                                  (50, 50, 200), (80, 80, 250), 30)
        self.submit_button = Button("SUBMIT", 600, 330, 150, 100,
                                    (50, 50, 200), (80, 80, 250), 30)
        self.name_text = TextInputBox(300, 200, 400, 100)
        self.instruction_text = Text("Write your nickname", 300, 150)

        self.socket = socket
        self.host = host
        self.port = port

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
            if self.is_name_taken(name):
                print("name is taken")
                return "PLAY"
            else:
                self.info.name = self.name_text.text_obj.text
                return "ONLINE_LOBBY"
        self.name_text.handle_event(event)
        return None
    
    def is_name_taken(self, name):
        name_length = len(name)
        message = struct.pack(f"BB{name_length}s", 0, name_length, name.encode())
        self.socket.sendto(message, (self.host, self.port))
        running = True
        while running:
            msg, _ = self.socket.recvfrom(2048)
            msg_type = int(msg[0])
            if msg_type == 5:
                is_taken = msg[1]
                print(is_taken)
                return is_taken
                    
        return False

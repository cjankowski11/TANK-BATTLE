from menu_utilities.button import Button
from menu_utilities.text import Text
import pygame


class LocalLobbyPage:

    def __init__(self, info):
        self.info = info
        self.back_button = Button("BACK", 20, 100, 100, 100, (50, 50, 200),
                                  (80, 80, 250), 30)
        add_player = Button("+", 125, 300, 100, 100, (50, 50, 200), (80, 80, 250))
        add_player.change_to_sysfont("arial", 50)
        self.add_player_button = add_player
        sub_player = Button("-", 250, 300, 100, 100, (50, 50, 200), (80, 80, 250))
        sub_player.change_to_sysfont("arial", 50)
        self.subtract_player_button = sub_player

        self.player_text = Text(f"PLAYERS {self.info.number_of_players}", 125, 245)

        add_bot = Button("+", 500, 300, 100, 100, (50, 50, 200), (80, 80, 250))
        add_bot.change_to_sysfont("arial", 50)
        self.add_bot_button = add_bot
        sub_bot = Button("-", 625, 300, 100, 100, (50, 50, 200), (80, 80, 250))
        sub_bot.change_to_sysfont("arial", 50)
        self.subtract_bot_button = sub_bot

        self.rounds_text = Text(f"ROUNDS {self.info.number_of_rounds}", 150, 50)
        add_round = Button("+", 125, 90, 100, 100, (50, 50, 200), (80, 80, 250))
        add_round.change_to_sysfont("arial", 50)
        self.add_round_button = add_round
        sub_round = Button("-", 250, 90, 100, 100, (50, 50, 200), (80, 80, 250))
        sub_round.change_to_sysfont("arial", 50)
        self.subtract_round_button = sub_round

        self.bot_text = Text(f"BOTS {self.info.number_of_bots}", 550, 245)

        self.play_buton = Button("PLAY", 400, 100, 300, 100, (50, 50, 200),
                                 (80, 80, 250), 50)

    def draw_page(self, screen):
        self.back_button.draw(screen)
        self.add_player_button.draw(screen)
        self.subtract_player_button.draw(screen)
        self.add_bot_button.draw(screen)
        self.subtract_bot_button.draw(screen)
        self.player_text.draw(screen)
        self.bot_text.draw(screen)
        self.rounds_text.draw(screen)
        self.add_round_button.draw(screen)
        self.subtract_round_button.draw(screen)
        self.play_buton.draw(screen)
        

    def is_page_changed(self, event):
        if self.back_button.is_clicked(event):
            self.info.online = None
            return "PLAY"
        
        if (self.add_player_button.is_clicked(event) and
                self.info.number_of_players + self.info.number_of_bots < self.info.max_players):
            self.info.number_of_players += 1
            self.player_text.change_text(f"PLAYERS {self.info.number_of_players}")
        
        if self.subtract_player_button.is_clicked(event) and self.info.number_of_players > 0:
            self.info.number_of_players -= 1
            self.player_text.change_text(f"PLAYERS {self.info.number_of_players}")

        if (self.add_bot_button.is_clicked(event) and
                self.info.number_of_players + self.info.number_of_bots < self.info.max_players):
            self.info.number_of_bots += 1
            self.bot_text.change_text(f"BOTS {self.info.number_of_bots}")
        
        if self.subtract_bot_button.is_clicked(event) and self.info.number_of_bots > 0:
            self.info.number_of_bots -= 1
            self.bot_text.change_text(f"BOTS {self.info.number_of_bots}")
        
        if (self.add_round_button.is_clicked(event) and
                self.info.number_of_rounds < self.info.max_rounds):
            self.info.number_of_rounds += 1
            self.rounds_text.change_text(f"ROUNDS {self.info.number_of_rounds}")
        
        if (self.subtract_round_button.is_clicked(event) and
                self.info.number_of_rounds > self.info.min_rounds):
            self.info.number_of_rounds -= 1
            self.rounds_text.change_text(f"ROUNDS {self.info.number_of_rounds}")

        if self.play_buton.is_clicked(event):
            self.info.game_running = True
            return "QUIT"

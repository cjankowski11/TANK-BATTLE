import socket
import threading
import struct
import pygame
import random
import math
import time
from gameView import GameView

class OnlineGame:
    def __init__(self, bots_number, rounds_number, socket, host="127.0.0.1", port=12345):
        self.host = host
        self.port = port
        self.rounds = rounds_number
        self.socket = socket
        self.gameView = None
        self.running = True
        self.action_list = {"w": False,
                            "a": False,
                            "s": False,
                            "d": False,
                            "shoot": False}

    def update(self):
        pass
    
    def run(self):
        self.gameView = GameView()

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return False

                    
            keys = pygame.key.get_pressed()
            self.action_list["w"] = keys[pygame.K_w]
            self.action_list["a"] = keys[pygame.K_a]
            self.action_list["s"] = keys[pygame.K_s]
            self.action_list["d"] = keys[pygame.K_d]
            self.action_list["shoot"] = keys[pygame.K_SPACE]                
            
            self.gameView.draw_game()
        

    def listener(self):
        actions = {
            2: self.initialize_map,
            3: self.update_game,
            4: self.game_finished
        }
        while self.running:
            try:
                msg, _ = self.socket.recvfrom(2048)
                number = msg[0]
                actions[number](msg)

            except socket.timeout:
                continue
            except Exception as e:
                print(e)
            # time.sleep(0.01)
    
    def broadcasting(self):
        while self.running:
            if any(self.action_list):
                msg = struct.pack("BBBBBB", 7, self.action_list["w"], self.action_list["a"],
                                self.action_list["s"], self.action_list["d"],
                                self.action_list["shoot"])
                try:
                    self.socket.sendto(msg, (self.host, self.port))
                except Exception as e:
                    print(e)
            time.sleep(0.01)
    


    def start_connection(self):
        threading.Thread(target=self.listener, daemon=True).start()
        threading.Thread(target=self.broadcasting, daemon=True).start()

    def initialize_map(self, msg):
        
        number_of_walls = msg[1]
        offset = 2
        walls = []
        players = {}
        for _ in range(number_of_walls):
            left, top, width, height = struct.unpack("<HHHH", msg[offset:offset+8])
            walls.append(pygame.Rect(left, top, width, height))
            offset += 8
        number_of_players = msg[offset]
        offset += 1
       
        for _ in range(number_of_players):
            name = struct.unpack("20s", msg[offset:offset+20])
            offset += 20
            x, y, angle, bullets = struct.unpack("fffB", msg[offset:offset+13])
            offset += 13
            
            players[name] = (x, y, angle, bullets)

        self.gameView.update_walls(walls)
        self.gameView.initialize_players(players)
    
    def update_game(self, msg):
        number_of_players = msg[1]
        offset = 2
        for _ in range(number_of_players):
            name = struct.unpack("20s", msg[offset:offset+20])
            offset += 20
            x, y, angle, bullets= struct.unpack("fffB", msg[offset:offset+13])
            offset += 13
            self.gameView.update_player(name, x, y, angle, bullets, True)
        number_of_bullets = msg[offset]

        offset += 1
        bullets = []
        for _ in range(number_of_bullets):
            x, y, time_of_existence = struct.unpack("ffH", msg[offset:offset+10])
            offset += 10
            bullets.append((x, y, time_of_existence))
        self.gameView.update_bullets(bullets)
    
    def game_finished(self, msg):
        self.running = False

    def is_game_finished(self):
        return not self.running





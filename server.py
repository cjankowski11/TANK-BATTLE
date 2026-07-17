import socket
import threading
import time
import struct
from gameEngine import GameEngine
from dotenv import load_dotenv
import os
from player import Player, BotPlayer
load_dotenv()
server_ip = os.getenv("IP")
port = os.getenv("PORT")


class Server:
    def __init__(self, host='127.0.0.1', port=34567):
        self.host = host
        self.port = port
        self.start_game = False
        self.kill = False
        self.thread_count = 0
        self.menu_players = {}
        self.max_players = 4
        self.bots_number = 0
        self.rounds_number = 1
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.socket.bind((self.host, self.port))
        self.socket.settimeout(1)
        self.lock = threading.Lock()
        self.players = {} # zrobic moze klase graczy gdzie beda te akcje i moze ilosc punktow i to czy gracz zyje igig

    def handle_data(self, data, addr):
        try:
            if len(data):
                msg_type = struct.unpack("B", data[:1])[0]
                now = time.time()
                decoded_name = None
                ready_status = False
                if msg_type == 1:
                    name_length, ready_status = struct.unpack("B?", data[1:3])
                    name_raw = struct.unpack(f"{name_length}s", data[3:name_length+3])[0]
                    decoded_name = name_raw.decode()

                with self.lock:
                    if addr in self.menu_players:
                        self.menu_players[addr]["time"] = now

                    if msg_type == 0:
                        name_is_used = False
                        name_length = struct.unpack("B", data[1:2])[0]
                        print(name_length)
                        new_name = struct.unpack(f"{name_length}s", data[2:int(name_length)+2])[0]
                        new_name = new_name.decode()
                        for player in self.menu_players.values():
                            if new_name == player["name"]:
                                name_is_used = True
                                self.socket.sendto(struct.pack("B?", 5, True), addr)
                        if not name_is_used:
                            self.socket.sendto(struct.pack("B?", 5, False), addr)
                        print(new_name)
                
                    elif msg_type == 1:        
                        all_players = self.get_menu_players_number() + self.bots_number
                        addrs = self.get_menu_players_addrs()
                        if all_players < 4 or addr in addrs:
                            self.menu_players[addr] = {"name": decoded_name,
                                                       "time": now,
                                                       "ready": ready_status}

                    elif msg_type == 2:
                        if self.bots_number + self.get_menu_players_number() < 4:
                            self.bots_number += 1

                    elif msg_type == 3:
                        if self.bots_number > 0:
                            self.bots_number -= 1

                    elif msg_type == 4 and not self.start_game:
                        self.start_game = (bool(self.menu_players) and
                                           all(p["ready"]
                                           for p in self.menu_players.values()))
                        self.initialize_players()
                    elif msg_type == 5:
                        if self.rounds_number < 20:
                            self.rounds_number += 1
                    
                    elif msg_type == 6:
                        if self.rounds_number > 1:
                            self.rounds_number -= 1
                    
                    elif msg_type == 7:
                        name = self.get_player_name(addr)
                        w, a, s, d, shoot = struct.unpack("BBBBB", data[1:])
                        self.players[name].update(w, a, s, d, shoot)
                        
                        
        except Exception as e:
            print(f"error {e}")

    def listen_loop(self):
        self.thread_count += 1
        print("Server working")
        while not self.kill:
            try:
                data, addr = self.socket.recvfrom(2048)
                self.handle_data(data, addr)   # handle_menu_data and handle game_data
            except socket.timeout:
                continue
            except Exception as e:
                print(e)
            # time.sleep(0.01)
        self.thread_count -= 1

    def broadcasting(self):
        game_initialized = False
        ticks_per_sec = 60
        tick_duration = 1.0 / ticks_per_sec
        current_round = 0
        self.thread_count += 1
        next_tick = time.time()
        
        while not self.kill:
            now = time.time()
            
            with self.lock:
                active_game = self.start_game
                current_players = list(self.menu_players.keys())

            if not active_game:
                self.resending_active_players()
                time.sleep(0.1)

                next_tick = time.time() 
                current_round = 0
                continue

            if not game_initialized:   
                self.initialize_game(ticks_per_sec)
                self.update_bot_walls()
                current_round += 1
                if current_round > self.rounds_number:
                    self.start_game = False
                    continue
                for addr in current_players:      
                    self.socket.sendto(struct.pack("B", 1), addr)
                game_initialized = True
                
                time.sleep(0.1)
                for _ in range(5):
                    self.send_starting_info()
                    time.sleep(0.5)

                next_tick = time.time() + tick_duration 

            if now >= next_tick:
                if self.gameEngine.is_finished():
                    game_initialized = False
                    winner = self.gameEngine.get_winner()
                    self.players[winner].add_point()
                    for player, values in self.players.items():
                        print(f"player {player} has {values.points} points")
                    
                    if current_round == self.rounds_number:
                        for addr in current_players:
                            self.socket.sendto(struct.pack("B", 4), addr)
                        self.menu_players = {}
                        self.players = {}
                self.update_game_logic()  
                self.broadcast_game_state() 
                next_tick += tick_duration
            else:

                time.sleep(0.001)
        self.thread_count -= 1

    def await_kill(self):
        self.kill = True
        while self.thread_count:
            time.sleep(0.01)
        print("killed")

    def run(self):
        threading.Thread(target=self.listen_loop).start()
        threading.Thread(target=self.broadcasting).start()
        try:
            while not self.kill:
                time.sleep(0.05)
                
        except KeyboardInterrupt:
            self.await_kill()

    
    def delete_not_active(self):
        addr_to_delete = []
        for addr, _ in self.menu_players.items():
            if time.time() - self.menu_players[addr]["time"] > 5:
                addr_to_delete.append(addr)
        for addr in addr_to_delete:
            self.menu_players.pop(addr)

    def get_menu_players_number(self):
        return len(self.menu_players)
    
    def get_menu_players_addrs(self):
        return list(self.menu_players.keys())

    def get_menu_players_values(self):
        return list(self.menu_players.values())
    
    def get_player_name(self, addr):
        return self.menu_players[addr]["name"]
    
    def resending_active_players(self):
        with self.lock:
            self.delete_not_active()
            current_players = self.get_menu_players_values()
            num_players = self.get_menu_players_number()
            current_bots = self.bots_number
            rounds = self.rounds_number
        buffor = struct.pack("BBBB", 0, num_players, current_bots, rounds)
        for value in current_players:
            encoded_name = value["name"].encode()
            name_length = len(encoded_name)
            buffor += struct.pack(f"B?{name_length}s", name_length, value["ready"], encoded_name)
        with self.lock:
            addrs = self.get_menu_players_addrs()

        for addr in addrs:
            try:
                self.socket.sendto(buffor, addr)
            except Exception as e:
                print(e)
            
    def initialize_game(self, tps): 
        with self.lock:
            names = []
            for name, player in self.players.items():
                names.append(name)
                player.alive = True

        self.gameEngine = GameEngine(names, tps)
        self.gameEngine.change_map("maps/map3.txt")
                
    def initialize_players(self):

        for value in self.menu_players.values():
            name = value["name"]
            self.players[name] = Player(name)
        for i in range(self.bots_number):
            bot_name = f"BOT{i}"
            self.players[bot_name] = BotPlayer(bot_name)

    def update_game_logic(self):
        self.gameEngine.update_bullets()
        bullets_info = self.gameEngine.get_bullets()
        players_info = self.gameEngine.get_players()
        for name, player in self.players.items():
            if player.is_bot():
                player.update_bullets(bullets_info)
                player.update_players(players_info)
                player.update()
            instructions = player.get_instructions()
            
            self.gameEngine.update_player(name, instructions["w"], 
                                          instructions["a"],
                                          instructions["s"],
                                          instructions["d"],
                                          instructions["shoot"])
            
        

    def broadcast_game_state(self):
        players = self.gameEngine.get_players(binary=True)
        bullets = self.gameEngine.get_bullets(binary=True)
        msg = struct.pack("B", 3) + players + bullets

        with self.lock:
            addrs = self.get_menu_players_addrs()
        for addr in addrs:
            self.socket.sendto(msg, addr)

    def send_starting_info(self):
        # send walls to players
        walls = self.gameEngine.get_walls(binary=True)
        players = self.gameEngine.get_players(binary=True)
        msg = struct.pack("B", 2) + walls + players
        with self.lock:
            addrs = self.get_menu_players_addrs()
        for addr in addrs:
            self.socket.sendto(msg, addr)
    
    def update_bot_walls(self):
        walls = self.gameEngine.get_walls()
        for player in self.players.values():
            if player.is_bot():
                player.update_walls(walls)


server = Server(server_ip, int(port))
server.run()
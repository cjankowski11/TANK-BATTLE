from mainMenu import MainMenu
from localGame import LocalGame
from onlineGame import OnlineGame
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    server_ip = os.getenv("IP")
    port = os.getenv("PORT")
    while True:
        menu = MainMenu()
        game = None
        menu_info = menu.run()
        if menu_info.online:
            game = OnlineGame(menu_info.number_of_bots,
                              menu_info.number_of_rounds, menu_info.socket,
                              server_ip, int(port))
            game.start_connection()
        elif menu_info.online is False:
            game = LocalGame(
                menu_info.number_of_players, menu_info.number_of_bots,
                menu_info.number_of_rounds)
        if game is None:
            break
        else:
            game_running = game.run()
            if game_running is False:
                break
    
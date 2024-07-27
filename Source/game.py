"#> GAME: "
# This file will be the main file of the game.
# It will communicate with the <initiator.py> to interact with the rest of the code base.

# > Imports:
import os
import sys
import json

PATH = sys.path[0]
sys.path.append(
    PATH + r"\CodeFiles"
)  # This is for enabling the usage of our <CodeFiles> dir as a module.


# > Importing the <initiator> to interact with the rest of the code base.
from CodeFiles.initiator import clear, cursor, CentralDogma, StartMenu, home_screen

# Create a folder to store all the "Lives", if it doesn't exist already.
if not os.path.exists(PATH + r"\Lives"):
    os.makedirs(PATH + r"\Lives")


# > Defining a <main> func to handle the game and its interactions with the <initiator>:
def main():  # The <main()> func that initiates the game.

    try:

        menu = StartMenu(PATH=PATH)
        clear()
        cursor(False)

        if menu.choice in [
            "RandomLife",
            "CustomLife",
        ]:  # If a new life is started, this will be executed.

            player_folder = "{} {}".format(
                menu.data["first_name"], menu.data["last_name"]
            )

            event_logs_file = "\\{}_{}_event_logs.txt".format(
                menu.data["first_name"].lower(), menu.data["last_name"].lower()
            ).replace(" ", "_")

            data_file = "\\{}_{}_data.json".format(
                menu.data["first_name"].lower(), menu.data["last_name"].lower()
            ).replace(" ", "_")

            player_path = PATH + r"\Lives" + f"\\{player_folder}"

            if not os.path.exists(player_path):
                os.makedirs(player_path)

            log_path = player_path + event_logs_file
            data_path = player_path + data_file
            open(log_path, "x", encoding="utf-8")
            # A new data <.json> file will be created for the player, if it doesn't exist.

            with open(data_path, "x", encoding="utf-8") as data_file:
                json.dump(menu.data, data_file, indent=4)
                datapath = data_file.name

            os.path.normpath(datapath)

            with open(
                datapath,
                "r",
                encoding="utf-8",
            ) as data_file:
                data = json.load(data_file)

            home_screen(
                PATH=PATH, main=main, data=data, datapath=datapath, logpath=log_path
            )

        elif (
            menu.choice == "LoadLife"
        ):  
            # Else, it will go onto load a file from the 'Lives' folder.
            with open(menu.data, "r", encoding="utf-8") as new_file:
                load = json.load(new_file)

            log_path = str(menu.data).replace("data.json", "event_logs.txt")
            os.path.normpath(log_path)
            # The <log_path> is and logs, in general, are going to be explained in <event_handler.py>

            CentralDogma(load)
            # This func handles the sub-min and par-max attribute values of the player.

            home_screen(
                PATH=PATH, main=main, data=load, datapath=menu.data, logpath=log_path
            )

    except:
        pass  # change to <raise> for debugging.


if __name__ == "__main__":
    main()

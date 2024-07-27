"#> GAME: "
# This file will be the main file of the game.
# It will be handling all the interactions between different game modules.
# Also, some of the important game-based decisions will take place here.


# * Imports:

# > Importing Legacy:
import os  # For <path> manipulation.
import sys  # For <path> manipulation, as well.
import json  # For getting our <.json> data.
import random  # For all the <random()> funcs inculding <choice()>, <randint()>, etc.
from numpy.random import choice as npchoice, triangular as tri  # For randoms, as well.

# Also, the <triangular()> or <tri()> helps in generating traingular randoms (with min, mode and max values)
# It will help in generating a weighted random float within a specified range, which can be rounded off to get a clean int.

# This <PATH> var will store the path of the game directory, regardless of whose (Windows) PC it's running on.
# This will ensure that the game doesn't stop working if the directories change, or if the users change.
PATH = sys.path[0]
sys.path.append(
    PATH + r"\CodeFiles"
)  # This is for enabling the usage of our <CodeFiles> dir as a module.


# > Importing custom modules:
# All modules are described in their respective files, briefly. <Ctrl+click> (for VS Code) to open.
from CodeFiles.career import Career
from CodeFiles.menu_screen import Menu
from CodeFiles.home_screen import Home
from CodeFiles.lifestyle import Lifestyle
from CodeFiles.event_handler import Event
from CodeFiles.activities import Activities
from CodeFiles.profile_screen import Profile
from CodeFiles.death_screen import Deathscreen
from CodeFiles.relations import Relations, NewBorn
from CodeFiles.modules import cursor, clear, update, CentralDogma


# Create a folder to store all the "Lives", if it doesn't exist already.
if not os.path.exists(PATH + r"\Lives"):
    os.makedirs(PATH + r"\Lives")


with open(
    PATH + r"\jsonFiles\events_data.json",
    "r",
    encoding="utf-8",
) as file:
    evdata = json.load(
        file
    )  # This is the <events_data> file with all the data about events.


# > Define a <job> func for the parents:
def get_job():  # This func will be used to generate jobs for parents (upon randomising).

    jobs = evdata["life"]["jobs"]
    jobtyp = random.choice(
        list(jobs.keys())[2:]
    )  # To ensure that parents only get jobs of mid level and above (index 2 and above on the <.json> file).
    job = random.choice(list(jobs[jobtyp].keys()))

    if job[0] in list("AEIOU"):  # Aligning the jobs into sentences, gramatically.
        job = "an " + job
    else:
        job = "a " + job

    return job


# > Define the 'Start Menu' of the game:
class StartMenu:  # The Start Menu is the first thing to show up on the screen.

    def __init__(self):

        menu = Menu(PATH)  # Menu will use PATH, as already discussed.
        character_data = menu[0]
        choice = menu[1]

        # * Add attributes to the character data:

        if choice in ["RandomLife", "CustomLife"]:

            # Randomising attribute values for the player, upon generation.
            attributes = ["health", "happiness", "smarts", "looks", "physique"]

            for attribute in attributes:

                if attribute == "health":
                    character_data[attribute] = round(
                        tri(15, 75, 100)
                    )  # Triangular: Returns a random float, closer to the mode. Round it off for an int.
                else:
                    character_data[attribute] = round(tri(30, 60, 90))

            character_data["discipline"] = random.randint(30, 60)

            # Now, randomising attributes for the parents.
            if "mother" in character_data["relations"]["parents"]:
                character_data["relations"]["parents"]["mother"]["health"] = (
                    random.randint(50, 100)
                )
                character_data["relations"]["parents"]["mother"]["relationship"] = (
                    random.randint(50, 100)
                )
                character_data["relations"]["parents"]["mother"]["job"] = get_job()

            if "father" in character_data["relations"]["parents"]:
                character_data["relations"]["parents"]["father"]["health"] = (
                    random.randint(50, 100)
                )
                character_data["relations"]["parents"]["father"]["relationship"] = (
                    random.randint(50, 100)
                )
                character_data["relations"]["parents"]["father"]["job"] = get_job()

        self.data = character_data
        self.choice = choice


# > Define a 'Home Screen' for the game:
class HomeScreen:  # The main game screen, Home screen. Where the events and other gameplay takes place.

    def __init__(self, data, event):

        # The Home Screen will store some of the player's data, the data that it needs to show.
        home = Home(
            (data["first_name"], data["last_name"]),
            data["emojis"],
            data["age"],
            data["gender"],
            (data["location"].split(", ")),
            data["job"],
            data["fortune"]["money"],
            data["fortune"]["salary"],
            data["health"],
            data["happiness"],
            data["smarts"],
            data["looks"],
            data["physique"],
            data["discipline"],
            event,
            PATH=PATH,
        )

        self.choice = home.action


# Now the Home screen will be put into a function, which will actually do all the backend work.
def home_screen(data, datapath, logpath, action=None):

    def Death(data):  # Defining the Death of the pLayer, beforehand.

        fatality = None  # Fatality refers to the final disease  (i.e. The one that kills the player), if any.

        if (
            len(data["diseases"]) > 0
        ):  # Checking for diseases, and if yes, Death can be made more probable for the player.
            diseases = data["diseases"]

            for dis in diseases:
                if (
                    dis in evdata["life"]["diseases"]["fatal_birth_defects"]
                    or dis in evdata["life"]["diseases"]["fatal"]
                ):
                    fatality = dis

        if fatality != None:
            death = f"died due to the complications posed by [red]{fatality}[/red] -- at the age of"

        else:

            if (
                data["age"] >= 75
            ):  # If there's no fatality, we need another reason for the player's death.

                if data["discipline"] >= 50:
                    death = "died in a [green]peaceful sleep[/green] -- at the ripe old age of"
                else:
                    death = "died de to a [red]stroke[/red] -- at the age of"

            else:

                # A list of probable causes, in absence of a fatality and in presence of low discipline (and thus, low karma).
                deaths = [
                    "succumbed to death after being [red]mauled by a bear[/red] -- at the age of",
                    "died remorsefully after being [red]ran over by a truck[/red] -- at the age of",
                    "declared defeat to fatal burns after being [red]thrown into fire[/red] -- alive -- at the age of",
                    "died miserably after being [red]eaten by a Lion[/red] -- while on a safari -- at the age of",
                    "was [red]murdered by a few thugs[/red] -- at the age of",
                ]

                if data["discipline"] < 30:
                    death = random.choice(deaths)

                elif data["happiness"] < 50:
                    death = "died due to the burden of heavy [red]depression[/red] in their life -- at the age of"

                else:
                    death = "died unexpectedly -- at the age of"

        # Now, setting up the <gravemsg> or, the message to be shown on the 'grave'-ish last screen.

        name = f"{data['first_name']} {data['last_name']}"
        age = data["age"]
        karma = round(
            (
                data["discipline"]
                + ((100 - data["health"]) / 2)
                + ((100 - data["happiness"]) / 2)
            )
            / 2.5
        )

        if data["discipline"] >= 60:
            discipline = "[green]a great character[/green]"
        elif data["discipline"] >= 40:
            discipline = "[yellow]a nice persona[/yellow]"
        else:
            discipline = "[red]a questionable character[/red]"

        if data["gender"] == "male":
            pron = ["he", "his"]
            gen = "man"
        else:
            pron = ["she", "her"]
            gen = "woman"

        if len(data["relations"]["partner"]) > 0:
            partner = "{} {} -- {}".format(
                pron[1],
                data["relations"]["partner"]["type"].lower(),
                data["relations"]["partner"]["name"],
            )
        else:
            partner = None

        if len(data["relations"]["children"]) > 0:
            children = "{} of {} children".format(
                len(data["relations"]["children"]), pron[1]
            )
        else:
            children = None

        if partner != None and children != None:
            family = f"{partner} and {children}"
        elif partner != None and children == None:
            family = partner
        elif partner == None and children != None:
            family = children
        else:
            family = "some of {} neighbours, and partly by the local government".format(
                pron[1]
            )

        job = data["job"].replace("Retired ", "")

        if job in ["Doctor", "Lawyer", "Professor"]:
            colleagues = (
                " {} funeral was attended by {} colleagues at {} job as {}.".format(
                    pron[1].capitalize(), pron[1], pron[1], job
                )
            )

            if data["discipline"] >= 75:
                juniors = " Moreover, some of {} juniors were also present at {} funeral, remembering {} dearly.".format(
                    pron[1], pron[1], name.split(" ")[0]
                )

                if job == "Doctor":
                    juniors = juniors.replace("juniors", "patients")
                elif job == "Lawyer":
                    juniors = juniors.replace("juniors", "clients")
                elif job == "Professor":
                    juniors = juniors.replace("juniors", "students")

            else:
                juniors = ""

        else:
            colleagues = ""
            juniors = ""

        if data["gravemsg"] == None:
            gravemsg = """[yellow]{}[/yellow] [white]{} {}. {} was remembered as a {} of {}, on this day.
            
{} funeral was planned by {}.{}{}[/white]
""".format(
                name,
                death,
                age,
                pron[0].capitalize(),
                gen,
                discipline,
                pron[1].capitalize(),
                family,
                colleagues,
                juniors,
            )

            data["alive"] = False
            data["gravemsg"] = gravemsg
            data["karma"] = karma

        else:
            gravemsg = data["gravemsg"]
            karma = data["karma"]

        # Once the <gravemsg> is completed, the message is to be dumped into the player's data file.
        with open(datapath, "w", encoding="utf-8") as new_file:
            json.dump(data, new_file, indent=4)

        clear()
        Deathscreen(gravemsg, karma)
        main()

        return data

    if (
        data["alive"] == True
    ):  # If the player is alive, we will keep continuing the game.

        Event(data, evdata, logpath, PATH, action)

        with open(
            logpath,
            "r",
            encoding="utf-8",
        ) as log_file:
            event_log = log_file.read().split("\n")

        if len(event_log) > 5:
            event_log = event_log[-5:]

        event = ""

        for log in event_log:
            event += str(log + "\n")

        home = HomeScreen(data, event)

        def home_action(action, data, PATH=None):

            if PATH is None:
                action = action(data)
            else:
                action = action(data, PATH)

            with open(datapath, "w", encoding="utf-8") as new_file:
                json.dump(data, new_file, indent=4)

            with open(datapath, "r", encoding="utf-8") as read_file:
                data = json.load(read_file)

            if "Action: " in action or action in ["profile", "career"]:
                Event(data, evdata, logpath, PATH, action)

            update()
            home_screen(data, datapath, logpath, "loaded")

            return action

        if home.choice == "main_menu":
            main()

        elif home.choice == "age_up":

            # Death probability is handled here.

            death_prob = [0.0, 1.0]
            yes = death_prob[0]
            no = death_prob[1]

            if data["age"] >= 60 and data["health"] <= 30:
                death_prob = [yes + 0.25, no - 0.25]
            elif data["age"] >= 75 and data["health"] <= 40:
                death_prob = [yes + 0.5, no - 0.5]
            elif data["age"] >= 90:
                death_prob = [yes + 0.75, no - 0.75]

            yes = death_prob[0]
            no = death_prob[1]

            if len(data["diseases"]) >= 3:
                death_prob = [yes + 0.25, no - 0.25]

            death = npchoice(["yes", "no"], p=death_prob)

            if death == "yes":
                Death(data)

            data["age"] += 1

            # Updating attributes for each of the player's relations.
            for relationtype in data["relations"]:
                if relationtype != "partner":
                    for relation in data["relations"][relationtype]:

                        data["relations"][relationtype][relation]["age"] += 1

                        if data["relations"][relationtype][relation]["age"] >= 60:
                            chance = npchoice(["plus", "minus"], p=[0.35, 0.65])
                        elif data["relations"][relationtype][relation]["age"] < 60:
                            chance = npchoice(["plus", "minus"], p=[0.35, 0.65])

                        if chance == "plus":
                            data["relations"][relationtype][relation][
                                "health"
                            ] += random.randint(0, 12)
                        else:
                            data["relations"][relationtype][relation][
                                "health"
                            ] -= random.randint(0, 12)

                        data["relations"][relationtype][relation][
                            "relationship"
                        ] += random.randint(-18, 6)

                        CentralDogma(data)

                elif (
                    relationtype == "partner"
                    and len(data["relations"][relationtype]) != 0
                ):

                    data["relations"][relationtype]["age"] += 1

                    if data["relations"][relationtype]["age"] >= 60:
                        chance = npchoice(["plus", "minus"], p=[0.35, 0.65])
                    elif data["relations"][relationtype]["age"] < 60:
                        chance = npchoice(["plus", "minus"], p=[0.35, 0.65])

                    if chance == "plus":
                        data["relations"][relationtype]["health"] += random.randint(
                            0, 12
                        )

                    else:
                        data["relations"][relationtype]["health"] -= random.randint(
                            0, 12
                        )

                    data["relations"][relationtype]["relationship"] += random.randint(
                        -18, 6
                    )

                    CentralDogma(data)

            # Updating player's salary (if any).
            salary = data["fortune"]["salary"]

            if data["age"] <= 18:
                tax = 0  # The player won't be taxed for allowance.
            elif data["age"] > 18:
                tax = round((31 / 100) * salary)  # The salary will be taxed at 31%.

            if data["age"] == 19:
                data["fortune"]["salary"] = 0  # Disable allowance money at age 19.

            profit = (
                salary - tax
            )  # The player will get only 69% of their salary after tax.
            if salary > 0:
                data["fortune"]["money"] += profit

            # Further, randomly handling the player's attributes at "Age up" event.
            attrs = [
                "health",
                "happiness",
                "smarts",
                "looks",
                "physique",
                "discipline",
            ]

            for attr in attrs:

                if 90 <= data[attr]:
                    prob = [0.05, 0.95]
                    minP, maxP = 0, 3
                    minM, maxM = 6, 18
                elif 85 <= data[attr] < 90:
                    prob = [0.15, 0.85]
                    minP, maxP = 0, 6
                    minM, maxM = 6, 12
                elif 50 <= data[attr] < 85:
                    prob = [0.25, 0.75]
                    minP, maxP = 3, 6
                    minM, maxM = 3, 6
                elif 20 <= data[attr] < 50:
                    prob = [0.35, 0.65]
                    minP, maxP = 3, 6
                    minM, maxM = 0, 6
                elif 0 <= data[attr] < 20:
                    prob = [0.5, 0.5]
                    minP, maxP = 6, 12
                    minM, maxM = 0, 12

                choice = npchoice(["plus", "minus"], p=prob)

                if attr not in ["looks", "discipline", "smarts"]:
                    if choice == "plus":
                        data[attr] += random.randint(minP, maxP)
                    elif choice == "minus":
                        data[attr] -= random.randint(minM, maxM)
                else:
                    if choice == "plus":
                        data[attr] += random.randint(minP, maxP)
                    elif choice == "minus":
                        data[attr] -= random.randint(minM, maxM)

            if (
                dict(data["relations"]["partner"])
                and data["relations"]["partner"]["expecting"] == True
            ):
                action = home_action(NewBorn, data, PATH)

            CentralDogma(data, ageup=True)

            # Dumping the new data into the <.json> file that has the player's old data.
            with open(datapath, "w", encoding="utf-8") as new_file:
                json.dump(data, new_file, indent=4)

            with open(datapath, "r", encoding="utf-8") as read_file:
                data = json.load(read_file)

            home = home_screen(data, datapath, logpath, "age_up")

        # Or, handling other <home.choice> choices.

        elif home.choice == "profile":
            clear()
            home_action(Profile, data, PATH)

        elif home.choice == "activties":
            action = home_action(Activities, data, PATH)

        elif home.choice == "career":
            action = home_action(Career, data, PATH)

        elif home.choice == "relations":
            action = home_action(Relations, data, PATH)

        elif home.choice == "lifestyle":
            action = home_action(Lifestyle, data, PATH)

    else:  # Else, the death screen is to be shown.
        Death(data)


def main():  # The <main()> func that initiates the game.

    try:

        menu = StartMenu()
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

            home_screen(data, data_path, log_path)

        elif (
            menu.choice == "LoadLife"
        ):  # Else, it will go onto load a file from the 'Lives' folder.

            with open(menu.data, "r", encoding="utf-8") as new_file:
                load = json.load(new_file)

            log_path = str(menu.data).replace("data.json", "event_logs.txt")
            os.path.normpath(
                log_path
            )  # The <log_path> is and logs, in general, are going to be explained in <event_handler.py>

            CentralDogma(
                load
            )  # The <CentralDogma()> just handles the sub-min and par-max attribute values of the player. More ecplaination by <Ctrl+click> (for VS Code) on the func.

            home_screen(load, menu.data, log_path)

    except:
        # raise # (disabled for now)
        pass


if __name__ == "__main__":
    main()

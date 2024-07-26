"#> MENU SCREEN "

# * Imports:
import os
import re
import shutil
from modules import clear, cursor, goto, Entry
import inquirer as inq
import json
import random
from numpy.random import choice as npchoice
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.align import Align
from rich import print

cursor(False)

clear()
print(
    Panel.fit(
        "[green]Initializing the game...[/green]\n[gray30]Press the [i][yellow]Enter[/yellow][/i] button to start[/gray30]"
    )
)
input()


display = Console(height=20).print
menuscreen = Layout()


# * Define the Menu:
# Defining the Main Menu and all its components.
# All the options (viz. New Life, Load Life, etc) will be accessed from here.
def Menu(PATH):

    with open(
        PATH + r"\jsonFiles\game_screen_data.json",
        "r",
        encoding="utf-8",
    ) as file:
        menu_screen_data = json.load(file)

    menu_title = "".join(f"{line}\n" for line in menu_screen_data["menu_title"])

    clear()
    cursor(False)

    # * Set up the choices for the Menu:
    choices = ["New Life", "Load Life", "Quit"]

    load_path = PATH + r"\Lives"
    directory = os.listdir(load_path)

    if len(directory) == 0:
        choices.remove("Load Life")

    menuscreen.update(Align.center((menu_title), vertical="bottom"))
    display(menuscreen)

    # * Enable the Menu:
    # ? The < menu > variable will be used to enable a Menu for the game.
    # Here, the python module <inquirer> is being used to generate a Menu.

    menu = [inq.List("choice", "Main Menu", choices)]
    choice = inq.prompt(menu)["choice"]

    if choice == "New Life":
        clear()
        return NewLife(PATH)
    
    elif choice == "Load Life":
        clear()
        return LoadLife(load_path, directory, PATH)
    
    elif choice == "Quit":
        clear()
        inquiry = [inq.List("choice", "Quit the game", ["Yes", "No"])]
        choice = inq.prompt(inquiry)["choice"]

        if choice == "Yes":
            quit()
        else:
            return Menu(PATH)


# * Define the 'New Life' choice:
def NewLife(PATH):

    cursor(False)

    # * Ask if the user wants to create a random life or start afresh.
    # ? The <asker> will ask the user to select wether they want to create a random life or a custom one.
    asker = [
        inq.List(
            "choice",
            "Choose an option",
            ["Create a Random Life", "Create a Custom Life", "Back"],
        )
    ]
    choice = inq.prompt(asker)["choice"]

    # * Load the <.json> file that contains the data for various demographics:
    # This data will be used to generate the random and custom attributes (name, location, etc.) from.
    with open(
        PATH + r"\jsonFiles\demographics.json",
        "r",
        encoding="utf-8",
    ) as file:
        demographics = json.load(file)

    # * Initiate the choices:
    if choice == "Create a Random Life":
        clear()
        result = RandomLife(demographics)
    elif choice == "Create a Custom Life":
        clear()
        result = CustomLife(demographics)
    elif choice == "Back":
        result = Menu(PATH)

    return result


# * Define the 'Random Life' choice:
def RandomLife(demographics):
    # ? In the <RandomLife> func, first and last names will be fetched from the datafile.
    # ? The final name will be paired with attributes (viz. Health, Smarts, etc) with random values
    # ? Other options such as parentage, location, etc. shall be randomized as well.

    # * Set up the variables for random attributes:
    # ? Firstly, the gender will be randomized. This will also help us in name generation.
    gender = random.choice(("male", "female"))  # two boolean choices.

    # ? Next, the location shall be randomized as - country > city.
    country = random.choice(list(demographics["countries"].keys()))
    city = random.choice(demographics["countries"][country]["cities"])

    # ? Now, the funcs that are to be used, should be defined.
    # ? A set of emojis will be generated for the characters that have been created.
    # For that, a func <get_emoji> is defined.
    def get_emoji(gender):

        light_countries = [
            "Canada",
            "Denmark",
            "France",
            "Germany",
            "Japan",
            "United Kingdom",
        ]

        medium_countries = ["Argentina", "Brazil", "Greece", "Italy", "Mexico"]

        dark_countries = ["Egypt", "India", "Nigeria"]

        if country in light_countries:
            emojis_list = list(demographics["people"][f"{gender}"].values())[:1]
        elif country in medium_countries:
            emojis_list = list(demographics["people"][f"{gender}"].values())[:2]
        elif country in dark_countries:
            emojis_list = list(demographics["people"][f"{gender}"].values())[0:]
        else:
            emojis_list = list(demographics["people"][f"{gender}"].values())[:-1]

        emojis = random.choice(emojis_list)

        return emojis

    # ? Then, a random name will be generated for the player.
    first_name = random.choice(
        demographics["countries"][country][f"{gender}_first_names"]
    )
    last_name = random.choice(demographics["countries"][country]["last_names"])

    # ? Now, the player will be assigned an emoji list.
    emojis = get_emoji(gender)  # Emojis are based on the gender of the player.

    # ? Further, the filial status (i.e. parentage) shall be randomized.
    # The <choice> func of the <numpy> module, imported as <npchoice> shall be used for bias.
    parentage = npchoice(
        ["mother", "father", "both"], p=[0.15, 0.15, 0.7]
    )  # The bias is shown here as <p>.
    # Now, the info for the parents shall be generated.
    while True:  # <while> used to repeat the process until the names are unique.
        mother_name = random.choice(
            demographics["countries"][country]["female_first_names"]
        )
        father_name = random.choice(
            demographics["countries"][country]["male_first_names"]
        )
        if mother_name != first_name and father_name != first_name:
            break
    parents_info = {}
    # The names will be assigned on the basis of parentage (both or single parent).
    # A list of emojis will also be assigned to the parents, respectively.
    # Further, the age of the parents will be randomized as well.
    if parentage == "both":  # If both parents are alive/present.
        parents_info["mother"], parents_info["father"] = (
            {
                "name": f"{mother_name} {last_name}",
                "emojis": get_emoji("female"),
                "age": random.randint(20, 45),
                "gender": "female",
            },
            {
                "name": f"{father_name} {last_name}",
                "emojis": get_emoji("male"),
                "age": random.randint(20, 45),
                "gender": "male",
            },
        )
    elif parentage == "mother":  # If the parent is a single mother.
        parents_info["mother"] = {
            "name": f"{mother_name} {last_name}",
            "emojis": get_emoji("female"),
            "age": random.randint(20, 45),
            "gender": "female",
        }
    elif parentage == "father":  # if the parent is a single father.
        parents_info["father"] = {
            "name": f"{father_name} {last_name}",
            "emojis": get_emoji("male"),
            "age": random.randint(20, 45),
            "gender": "male",
        }

    # ? A birthday will be generated for the player.
    # The <random.choice()> and <random.randint()> funcs shall be used again.
    months = list(demographics["dates"].keys())
    month = random.choice(months)
    dates = demographics["dates"][month]  # Months with varied (31-30-29-28) days.
    date = random.randint(1, dates)  # Choose a date from the given range.
    # Lastly, the birthday shall be created.
    suffix = ""  # The suffix will be put against the date (e.g. 20 July -> 20th July).
    # This will be handled by a few <if> <else> statements.
    if str(date).endswith("1") and date != 11:
        suffix = "st"
    elif str(date).endswith("2") and date != 12:
        suffix = "nd"
    elif str(date).endswith("3") and date != 13:
        suffix = "rd"
    else:
        suffix = "th"
    # The final birthday.
    birthday = f"{date}{suffix} {month}"

    # ? Finally, the <information> dict will store all this information about the player.
    random_information = {
        "alive": True,
        "first_name": first_name,
        "last_name": last_name,
        "emojis": emojis,
        "gender": gender,
        "age": 0,
        "relations": {"parents": parents_info, "partner": {}, "children": {}},
        "location": f"{city}, {country}",
        "birthday": birthday,
        "health": 0,
        "happiness": 0,
        "smarts": 0,
        "looks": 0,
        "physique": 0,
        "discipline": 0,
        "education": [],
        "job": None,
        "fortune": {"money": 0, "salary": 0},
        "lifestyle": None,
        "diseases": [],
        "caps": {"hlt": 6, "hap": 6, "smr": 6, "lks": 6, "phy": 6, "dis": 6},
        "gravemsg": None,
        "karma": None,
    }

    choice = "RandomLife"
    return random_information, choice


# * Define the 'Custom Life' choice:
def CustomLife(demographics):
    # ? In the <CustomLife> func, the player will be asked to fill a few 'entries'.
    # ? These 'entries' are just our custom <Entry> class from the <modules.py> file.
    # ? <Entry> is a modified input widget, that can enforce a length limit on the input while typing.

    width = os.get_terminal_size().columns
    entry_size = 30

    startpoint = round(width / 2) - entry_size

    # A func <get_entry> will be defined to ease the repetitive process of getting entries.
    def get_entry(coords, message):
        x, y = coords
        message = message
        goto(x + 1, y)
        print(message)
        result = Entry(entry_size, (x, y + 15), "yellow", "cyan", "╭╮╰╯│─")

        return result

    # Multiple <Entry> widgets will be used to gather information about the character.
    first_name = get_entry((1, startpoint), "First Name ")
    last_name = get_entry((4, startpoint), "Last Name ")
    mother_name = get_entry((7, startpoint), "Mother's Name ")
    father_name = get_entry((10, startpoint), "Father's Name ")

    # In cases where required, <inquirer> widgets are to be used for inquiry.
    cursor(False)

    goto(14, startpoint)
    gender_inquiry = [inq.List("gender", "Choose your Gender", ["Male", "Female"])]
    gender = inq.prompt(gender_inquiry)["gender"].lower()

    goto(14, startpoint)
    country_inquiry = [
        inq.List("country", "Choose your Country", list(demographics["countries"]))
    ]
    country = inq.prompt(country_inquiry)["country"]

    goto(14, startpoint)
    city_inquiry = [
        inq.List(
            "city",
            "Choose your city",
            list(demographics["countries"][country]["cities"]),
        )
    ]
    city = inq.prompt(city_inquiry)["city"]

    goto(14, startpoint)
    month_inquiry = [
        inq.List("month", "Choose your month of birth", list(demographics["dates"]))
    ]
    month = inq.prompt(month_inquiry)["month"]

    goto(14, startpoint)
    date_inquiry = [
        inq.List(
            "date",
            "Choose your date of birth",
            list(range(1, (demographics["dates"][month] + 1))),
        )
    ]
    date = inq.prompt(date_inquiry)["date"]

    try:
        # The birthday shall be created.
        suffix = (
            ""  # The suffix will be put against the date (e.g. 20 July -> 20th July).
        )
        # This will be handled by a few <if> <else> statements.
        if str(date).endswith("1") and date != 11:
            suffix = "st"
        elif str(date).endswith("2") and date != 12:
            suffix = "nd"
        elif str(date).endswith("3") and date != 13:
            suffix = "rd"
        else:
            suffix = "th"
        # The final birthday.
        birthday = f"{date}{suffix} {month}"

        # Lastly, 'skin tone' is to be chosen by the player.
        goto(14, startpoint)
        emojis_inquiry = [
            inq.List(
                "emojis_choice",
                "Choose your skin tone",
                list(demographics["people"][gender]),
            )
        ]
        emojis_choice = inq.prompt(emojis_inquiry)["emojis_choice"]
        emojis = demographics["people"][gender][emojis_choice]

        # Then, setting up the emojis for parents.
        skin_tones = {"light": 2, "medium": 0, "dark": 0}
        # A <for> loop to be used for this algorithm (to randomize parent skin tones).
        for tone in skin_tones:
            if emojis_choice == tone:
                idx = list(skin_tones.keys()).index(tone)

                if idx == 0:
                    idx = 2
                elif idx == 1:
                    idx = 0
                elif idx == 2:
                    idx = 0

                mother_emojis_choices = list(demographics["people"]["female"].values())
                father_emojis_choices = list(demographics["people"]["male"].values())
                mother_emojis_choices.pop(idx)
                father_emojis_choices.pop(idx)

        # Finalizing info for the parents.

        if (
            len(mother_name.replace(" ", "")) > 0
            and len(father_name.replace(" ", "")) > 0
        ):
            parentage = "both"
        elif (
            len(mother_name.replace(" ", "")) > 0
            and len(father_name.replace(" ", "")) == 0
        ):
            parentage = "mother"
        elif (
            len(mother_name.replace(" ", "")) == 0
            and len(father_name.replace(" ", "")) > 0
        ):
            parentage = "father"

        parents_info = {}
        if parentage == "both":  # If both parents are alive/present.
            parents_info["mother"], parents_info["father"] = (
                {
                    "name": f"{mother_name} {last_name}",
                    "emojis": random.choice(father_emojis_choices),
                    "age": random.randint(20, 45),
                    "gender": "female",
                },
                {
                    "name": f"{father_name} {last_name}",
                    "emojis": random.choice(father_emojis_choices),
                    "age": random.randint(20, 45),
                    "gender": "male",
                },
            )
        elif parentage == "mother":  # If the parent is a single mother.
            parents_info["mother"] = {
                "name": f"{mother_name} {last_name}",
                "emojis": random.choice(father_emojis_choices),
                "age": random.randint(20, 45),
                "gender": "female",
            }
        elif parentage == "father":  # if the parent is a single father.
            parents_info["father"] = {
                "name": f"{father_name} {last_name}",
                "emojis": random.choice(father_emojis_choices),
                "age": random.randint(20, 45),
                "gender": "male",
            }

        first_name = re.sub(r"[\s\t]*", "", first_name)
        last_name = re.sub(r"[\s\t]*", "", last_name)
        mother_name = re.sub(r"[\s\t]*", "", mother_name)
        father_name = re.sub(r"[\s\t]*", "", father_name)

        clear()

        if (
            first_name != ""
            and last_name != ""
            and mother_name != ""
            and father_name != ""
        ):
            parentage = "both"
            parentage_info = f"{mother_name} {last_name} [white](Mother)[/white], {father_name} {last_name} [white](Father)"
        elif (
            first_name != ""
            and last_name != ""
            and father_name == ""
            and mother_name != ""
        ):
            parentage = "mother"
            parentage_info = f"{mother_name} {last_name} [white](Mother)"
        elif (
            first_name != ""
            and last_name != ""
            and mother_name == ""
            and father_name != ""
        ):
            parentage = "father"
            parentage_info = f"{father_name} {last_name} [white](Father)"
        elif first_name == "" or last_name == "":
            print("First Name and Last name is necessary.")
            input("Press <enter> key to restart the character creation.")
            CustomLife(demographics)
        elif (
            first_name != ""
            and last_name != ""
            and mother_name == ""
            and father_name == ""
        ):
            print("At least one parent is needed.")
            input("Press <enter> key to restart the character creation.")
            CustomLife(demographics)

        options = f"""
    [yellow]Name: [green]{first_name} {last_name}
    [yellow]Gender: [green]{gender}
    [yellow]Parentage: [green]{parentage_info}
    [yellow]Location: [green]{city}, {country}
    [yellow]Birthday: [green]{birthday}
    """
        # Finally, declaring the <information> var and returning it through this func.

        custom_information = {
            "alive": True,
            "first_name": first_name,
            "last_name": last_name,
            "emojis": emojis,
            "gender": gender,
            "age": 0,
            "relations": {"parents": parents_info, "partner": {}, "children": {}},
            "location": f"{city}, {country}",
            "birthday": birthday,
            "health": 0,
            "happiness": 0,
            "smarts": 0,
            "looks": 0,
            "physique": 0,
            "discipline": 0,
            "education": [],
            "job": None,
            "fortune": {
                "money": 0,
                "salary": 0,
            },
            "lifestyle": None,
            "diseases": [],
            "caps": {"hlt": 6, "hap": 6, "smr": 6, "lks": 6, "phy": 6, "dis": 6},
            "gravemsg": None,
            "karma": None,
        }

        goto(1, 1)
        print(Panel.fit(options), "\n")
        confirmation = [
            inq.List("confirm", "Do you want to confirm your options?", ["Yes", "No"])
        ]
        confirm = inq.prompt(confirmation)["confirm"]

        if confirm == "No":
            clear()
            input("Redirecting you to the Main Menu, press the <Enter> key.")
            clear()
            custom_information = CustomLife(demographics)[0]

        elif confirm == "Yes":
            pass

        choice = "CustomLife"
        return custom_information, choice

    except:
        clear()
        print("It looks like some of the required information wasn't provided.")
        input("Press <Enter> key to try again.")
        clear()

        result = CustomLife(demographics)

    return result


# * Define the 'Load Life' choice:
# The <LoadLife()> func will handle the process of loading different folders.
# It will communicate with the <Menu()> and return a 'result' to it.
# The 'result' will be forwarded to the <game.py> file.
def LoadLife(path, directory, PATH):

    cursor(False)

    directory.append("Back")

    files = [inq.List("file", "Choose a Life to load", directory)]
    folder = inq.prompt(files)["file"]
    filename = str(folder).lower().replace(" ", "_") + "_data.json"

    loaded_file = path + f"\\{folder}" + f"\\{filename}"
    os.path.normpath(loaded_file)

    if folder == "Back":
        result = Menu(PATH)
    else:
        clear()
        inquiry = [
            inq.List("choice", f"Life: {folder}", ["Load Life", "Delete Life", "Back"])
        ]
        option = inq.prompt(inquiry)["choice"]

        if "Load" in option:
            loaded_information = loaded_file
            choice = "LoadLife"
            result = (loaded_information, choice)
        elif "Delete" in option:
            clear()
            inquiry = [inq.List("choice", f"Delete the Life: {folder}", ["Yes", "No"])]
            option = inq.prompt(inquiry)["choice"]

            if option == "Yes":
                shutil.rmtree(PATH + f"\\Lives\\{folder}")
                result = Menu(PATH)
            else:
                result = Menu(PATH)

        else:
            result = Menu(PATH)

    return result

"#> HOME SCREEN "

# * Imports:
import os
import json
import inquirer as inq
from modules import update, cursor, Bar
from event_handler import PopUp
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.align import Align
from rich.table import Table
from rich import box


# * Define the <home_screen> that is to be displayed:
class Home:

    def __init__(
        self,
        name,
        emojis,
        age,
        gender,
        location,
        job,
        money,
        salary,
        health,
        happiness,
        smarts,
        looks,
        physique,
        discipline,
        event,
        PATH,
    ):

        cursor(False)
        update()

        self.screen(
            name=name,
            emojis=emojis,
            age=age,
            gender=gender,
            location=location,
            job=job,
            money=money,
            salary=salary,
            health=health,
            happiness=happiness,
            smarts=smarts,
            looks=looks,
            physique=physique,
            discipline=discipline,
            event=event,
            PATH=PATH,
        )

    def screen(
        self,
        name,
        emojis,
        age,
        gender,
        location,
        job,
        money,
        salary,
        health,
        happiness,
        smarts,
        looks,
        physique,
        discipline,
        event,
        PATH,
    ):

        # * Fetch the data:
        # ? Load the <.json> file into the program and extract data from it.
        with open(
            PATH + r"\jsonFiles\game_screen_data.json",
            "r",
            encoding="utf-8",
        ) as file:
            game_screen_data = json.load(file)
        # Here we get the graphics for our title, to be shown on screen.
        title = "".join(f"{line}\n" for line in game_screen_data["title"])

        # * Get the terminal size (no. of lines):
        # ? Initiate the <Console().print> function as <cprint>
        lines = os.get_terminal_size().lines
        display = Console(height=round(lines / 1.5)).print

        # * Initiate the screen < window > and style its layout:
        # ? Split the < window > into different sections as per need.
        window = Layout()  # Main window, which will be split into layouts.
        window.split_column(Layout(name="topwin"), Layout(name="events_screen"))
        window["topwin"].split_column(Layout(name="titlewin"), Layout(name="HUD"))
        window["titlewin"].split_row(
            Layout(name="info"), Layout(name="title"), Layout(name="professional_info")
        )
        window["info"].split_column(
            Layout(name="name_plate", ratio=1), Layout(name="location", ratio=1)
        )
        window["professional_info"].split_column(
            Layout(name="money", ratio=1), Layout(name="profession", ratio=1)
        )
        window["money"].split_row(
            Layout(name="funds", ratio=1), Layout(name="salary", ratio=1)
        )
        window["location"].split_row(Layout(name="city"), Layout(name="country"))

        # * Assign graphics to all the layouts of the window:
        # The player's age group shall be decided:
        if 0 <= age < 5:
            age_group = 0
        elif 5 <= age < 16:
            age_group = 1
        elif 15 <= age < 30:
            age_group = 2
        elif 30 <= age < 60:
            age_group = 3
        elif age >= 60:
            age_group = 4
        # Emojis shall be assigned based on the age group.
        emoji = emojis[age_group]
        # ? The UI elements like 'info', 'fortune', etc. are to be displayed respectively.
        titlewin_style = "yellow"  # Colour of the <title_win> elements.
        # This will show the game title:
        window["title"].update(Align.center(title, vertical="middle"))
        # This will show the player's name and gender:
        if gender == "male":
            symbol = "[cyan]:male_sign:"
        elif gender == "female":
            symbol = "[hot_pink]:female_sign:"

        window["name_plate"].update(
            Panel(
                Align.center(f"[white]{name[0]} {name[1]} {symbol}"),
                title="[purple]Person",
                style=titlewin_style,
            )
        )
        # This will show the player's location:
        window["city"].update(
            Panel(
                Align.center(f"[white]{location[0]}", vertical="middle"),
                title="[purple]City",
                style=titlewin_style,
            )
        )
        # This will show the player's gender:
        window["country"].update(
            Panel(
                Align.center(f"[white]{location[1]}", vertical="middle"),
                title=f"[purple]Country",
                style=titlewin_style,
            )
        )
        # This will show the amount of money that the player has (if any):
        window["funds"].update(
            Panel(
                Align.center(f"[white]$[green]{money}", vertical="middle"),
                title="[purple]Money",
                style=titlewin_style,
            )
        )
        # This will show the salary of the player (if any):
        window["salary"].update(
            Panel(
                Align.center(f"[white]$[green]{salary} [white]p.a.", vertical="middle"),
                title="[purple]Salary",
                style=titlewin_style,
            )
        )
        window["profession"].update(
            Panel(
                Align.center(f"[white]{job}[/white]", vertical="middle"),
                title="[purple]Professional Status",
                style=titlewin_style,
            )
        )

        # * Initialize different status bars:
        # ? Status bars like for attributes like 'Health', 'Smarts', etc, are to be initialized.
        # ? A <Bar> class from the custom <modules.py> file is to be used here.

        attrs = {
            "health": health,
            "happiness": happiness,
            "smarts": smarts,
            "looks": looks,
            "physique": physique,
            "discipline": discipline,
        }

        for attr in attrs:
            val = attrs[attr]

            if 100 >= val >= 80:
                attrs[attr] = 0
            elif 80 >= val >= 60:
                attrs[attr] = 1
            elif 60 >= val >= 40:
                attrs[attr] = 2
            elif 40 >= val >= 20:
                attrs[attr] = 3
            elif 20 >= val >= 0:
                attrs[attr] = 4

        HUD_style, HUD_text = "cyan", "white"  # Colour of the < HUD > elements.
        bar_cols = game_screen_data["bar_colours"]
        graphics = game_screen_data["bar_graphics"]
        full = 20  # Maximum value that an attribute can have.
        health_bar = Panel(
            graphics["health"][attrs["health"]]
            + " "
            + Bar((health, full), "█", (bar_cols[attrs["health"]], "gray15")),
            title=f"[{HUD_text}]Health",
            style=HUD_style,
        )
        happiness_bar = Panel(
            graphics["happiness"][attrs["happiness"]]
            + " "
            + Bar((happiness, full), "█", (bar_cols[attrs["happiness"]], "gray15")),
            title=f"[{HUD_text}]Happiness",
            style=HUD_style,
        )
        smarts_bar = Panel(
            graphics["smarts"][attrs["smarts"]]
            + " "
            + Bar((smarts, full), "█", (bar_cols[attrs["smarts"]], "gray15")),
            title=f"[{HUD_text}]Smarts",
            style=HUD_style,
        )
        looks_bar = Panel(
            graphics["looks"][attrs["looks"]]
            + " "
            + Bar((looks, full), "█", (bar_cols[attrs["looks"]], "gray15")),
            title=f"[{HUD_text}]Looks",
            style=HUD_style,
        )
        physique_bar = Panel(
            graphics["physique"][attrs["physique"]]
            + " "
            + Bar((physique, full), "█", (bar_cols[attrs["physique"]], "gray15")),
            title=f"[{HUD_text}]Physique",
            style=HUD_style,
        )
        discipline_bar = Panel(
            graphics["discipline"][attrs["discipline"]]
            + " "
            + Bar((discipline, full), "█", (bar_cols[attrs["discipline"]], "gray15")),
            title=f"[{HUD_text}]Discipline",
            style=HUD_style,
        )

        # * Put the status bars onto the < HUD > layout:
        # ? The status bars are now going to be placed onto the <HUD> layout of the <window>, respectively
        # ? A <rich.table --> Table()> class will be used for this.
        status_table = Table(box=box.SIMPLE, show_header=False)
        status_table.add_row(health_bar, happiness_bar, smarts_bar)
        status_table.add_row(looks_bar, physique_bar, discipline_bar)
        window["HUD"].update(Align.center(status_table))

        # * Events screen:
        # ? The Events screen is going to be used to display all the in-game events.
        window["events_screen"].update(
            Panel(
                event,
                title=f"[white]( Age: {age} )",
                style="white",
                border_style="purple",
                padding=(1, 3),
                subtitle_align="left",
            )
        )

        # * Display the window onto the screen:
        display(window)

        options = [
            "|{:^20}|".format("🎂 Age up"),
            "|{:^19}|".format(f"{emoji}Profile"),
            "|{:^20}|".format("💞 Relations"),
            "|{:^20}|".format("📋 Activities"),
            "|{:^21}|".format("☰  Main Menu"),
        ]

        if age > 18:
            options.insert(4, "|{:^20}|".format("💼 Career"))
            options.insert(5, "|{:^20}|".format("🏠 Lifestyle"))

        actions = [inq.List("action", "Options", options)]
        action = inq.prompt(actions)["action"]

        self.action = ""

        if "Age up" in action:
            self.action = "age_up"

        elif "Profile" in action:
            self.action = "profile"

        elif "Relations" in action:
            self.action = "relations"

        elif "Activities" in action:
            self.action = "activties"

        elif "Career" in action:
            self.action = "career"

        elif "Lifestyle" in action:
            self.action = "lifestyle"

        elif "Main Menu" in action:
            self.action = "main_menu"

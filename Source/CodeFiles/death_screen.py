"#> DEATH SCREEN: "
"""The Death Screen is just the UI part of the actual Death scenario.
The backend is written, back in the <game.py> file.

Pretty easy code here:
- An ASCII text art title to be displayed on top of the 'grave'.
- Information about the player, like:
    - Name
    - Age
    - Cause of death
    - Funeral host
    - Attendees
    - Karma
    is to be displayed on the 'gravestone' (i.e. <gravemsg>)
"""


# * Imports:
import os
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.align import Align
from modules import goto, cursor, Bar


size = os.get_terminal_size().lines

display = Console(height=size - 1).print

title = """[red]
▓█████▄ ▓█████ ▄▄▄     ▄▄▄█████▓ ██░ ██ 
▒██▀ ██▌▓█   ▀▒████▄   ▓  ██▒ ▓▒▓██░ ██▒
░██   █▌▒███  ▒██  ▀█▄ ▒ ▓██░ ▒░▒██▀▀██░
░▓█▄   ▌▒▓█  ▄░██▄▄▄▄██░ ▓██▓ ░ ░▓█ ░██ 
░▒████▓ ░▒████▒▓█   ▓██▒ ▒██▒ ░ ░▓█▒░██▓
 ▒▒▓  ▒ ░░ ▒░ ░▒▒   ▓▒█░ ▒ ░░    ▒ ░░▒░▒
 ░ ▒  ▒  ░ ░  ░ ▒   ▒▒ ░   ░     ▒ ░▒░ ░
 ░ ░  ░    ░    ░   ▒    ░       ░  ░░ ░
   ░       ░  ░     ░  ░         ░  ░  ░
 ░                                     
[/red] 
"""


# * Establishing the Deathscreen:
class Deathscreen:

    def __new__(cls, gravemsg, karma):

        karma = "Karma " + Bar((karma, 50), "█", ("purple", "gray15"))

        cursor(False)
        cls.death_screen(cls, gravemsg, karma)
        goto(1, 1)
        input()

    def death_screen(cls, gravemsg, karma):

        window = Layout()
        window.split_column(
            Layout(name="top", ratio=2),
            Layout(name="mid", ratio=6),
            Layout(name="bot", ratio=2),
        )
        window["mid"].split_row(
            Layout(name="lef", ratio=2),
            Layout(name="main", ratio=6),
            Layout(name="rig", ratio=2),
        )

        for win in ["top", "lef", "rig"]:
            window[win].update("")

        window["main"].split_column(
            Layout(name="head", ratio=4), Layout(name="foot", ratio=6)
        )

        window["bot"].update(Align.center(Panel.fit(f"{karma}"), vertical="middle"))

        window["head"].update(Align.center(title, vertical="middle"))
        window["foot"].update(
            Panel(
                Align.center(gravemsg, vertical="top"),
                padding=(1, 2),
                title="💀💀💀",
                subtitle="[gray50]Press [i][yellow]Enter[/yellow][/i] to return to the Menu",
                subtitle_align="center",
            )
        )

        display(window)

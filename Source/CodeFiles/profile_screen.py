"#> PROFILE:"
"""Notes:
The profile is quite simple.
It will be a screen that shows our player's attributes, including:
- Name
- Age
- Location ...
- Money, - Salary... and so on.
"""

# * Imports:
import os
from modules import cursor
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.align import Align
from rich.table import Table
import inquirer as inq

cursor(False)

lines = os.get_terminal_size().lines
display = Console(height=round(lines / 1.6)).print


# * Establishing the Profile:
class Profile:

    def __new__(cls, data, PATH):
        cursor(False)
        cls.profile(cls, data)
        return "profile"

    def profile(cls, data):

        person = """
     ████████═╗
    ██████████╚╗
   ███ ████ ███║
   ████████████║
    ███▀▀▀▀███═╝
     ▀██████▀
          
       ████═══╗
    ██████████╚═╗
  ██████████████║ 
  ██████████████╝
"""

        ZooCard = """
[blue]▀█ █▀█ █▀█ [green]█▀▀ ▄▀█ █▀█ █▀▄
[blue]█▄ █▄█ █▄█ [green]█▄▄ █▀█ █▀▄ █▄▀
"""

        name = "{} {}".format(data["first_name"], data["last_name"])
        age = data["age"]
        gender = str(data["gender"]).capitalize()
        location = data["location"]

        if gender == "Male":
            person = "[blue]" + person + "[/blue]"
        elif gender == "Female":
            person = "[hot_pink]" + person + "[/hot_pink]"

        money = data["fortune"]["money"]
        salary = data["fortune"]["salary"]
        education = data["education"]
        lifestyle = data["lifestyle"]

        diseases = (
            str(data["diseases"])
            .replace("'", "")
            .replace('"', "")
            .replace("[", "")
            .replace("]", "")
        )

        if diseases == "":
            diseases = "[green]None[/green]"
        else:
            diseases = f"[red]{diseases}[/red]"

        education = (
            str(data["education"])
            .replace("'", "")
            .replace('"', "")
            .replace("[", "")
            .replace("]", "")
        )

        if len(education) == 0:
            education = "[red]None[/red]"
        else:
            education = f"{education}"

        if len(data["relations"]["partner"]) != 0:
            marriage = "{} ({})".format(
                data["relations"]["partner"]["name"],
                data["relations"]["partner"]["type"],
            )
        else:
            marriage = None

        if len(data["relations"]["children"]) == 0:
            children = None
        else:
            children = len(data["relations"]["children"])

        if data["job"] == None:
            job = "[red]None[/red]"
        else:
            job = data["job"]

        parentage = [
            (parent, name)
            for parent, name in zip(
                (str(par).capitalize() for par in data["relations"]["parents"]),
                (
                    data["relations"]["parents"][par]["name"]
                    for par in data["relations"]["parents"]
                ),
            )
        ]

        if len(parentage) == 1:
            parents = "".join("({}) {}".format(parentage[0][0], parentage[0][1]))
        elif len(parentage) == 2:
            parents = "".join(
                "({}) {}, ({}) {}".format(
                    parentage[0][0],
                    parentage[0][1],
                    parentage[1][0],
                    parentage[1][1],
                )
            )

        window = Layout()

        window.split_row(Layout(name="left", ratio=3), Layout(name="right", ratio=7))

        profile = Table.grid(expand=True)
        profile.add_row(f"[yellow]Name:[/yellow] {name}")
        profile.add_row(f"[yellow]Age:[/yellow] {age}")
        profile.add_row(f"[yellow]Gender:[/yellow] {gender}")
        profile.add_row(f"[yellow]Location:[/yellow] {location}")
        profile.add_row(f"[yellow]Parent(s):[/yellow] {parents}"),
        profile.add_row(f"[yellow]Partner:[/yellow] {marriage}"),
        profile.add_row(f"[yellow]Children:[/yellow] {children}")
        profile.add_row(f"[yellow]Education:[/yellow] {education}"),
        profile.add_row(f"[yellow]Profession:[/yellow] {job}")
        profile.add_row(f"[yellow]Money:[/yellow] $[green]{money}[/green]")
        profile.add_row(f"[yellow]Salary:[/yellow] $[green]{salary}[/green] per annum")
        profile.add_row(f"[yellow]Lifestyle:[/yellow] {lifestyle}")
        profile.add_row(f"[yellow]Diseases:[/yellow] {diseases}")

        window["right"].update(
            Panel(
                Panel(
                    profile,
                    border_style="purple",
                    title="[yellow]Profile",
                ),
                border_style="purple",
            )
        )

        window["left"].split_column(
            Layout(name="picture", minimum_size=16), Layout(name="bottom")
        )
        window["picture"].update(
            Panel(
                Panel(
                    Align.center(person),
                    title="[purple]Photograph",
                    border_style="yellow",
                ),
                border_style="yellow",
            )
        )
        window["bottom"].update(Panel(Align.center(ZooCard)))

        display(window)

        options = [inq.List("option", "Options", ["Back"])]
        inq.prompt(options)

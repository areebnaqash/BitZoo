"#> LIFESTYLE: "
"""Really simple.
This module handles the 'Lifestyle' option of the <home_screen.py> module.
Lifestyle works as follows:

- Player gets list of lifestyles:
    - None
    - Basic
    - Middle
    - Upper
    - Deluxe

- Player chooses any of these:
    - If player has the money:
        - Player gets the lifestyle (it's subscribtion based, btw).
        - If the money is not sufficient for the lifestyle in the subsequent years:
            - Lifestyle gets cancelled.
    - Else:
        - Player does not get the choice.

- Lifestyles come with perks like:
    - Health + / Health ++
    - Happiness + / Happiness ++ 
    etc
    for the player, and their immediate family as well.
"""


# * Imports:
import inquirer as inq
from event_handler import PopUp


# * Establishing the Lifestyle:
class Lifestyle:

    def __new__(cls, data, PATH):

        PopUp(
            "Lifestyle",
            "[white]I should probably start thinking about my lifestyle...[/white]",
            inp=True,
        )

        lifestyles = {
            "No Lifestyle -- Vibe with those streets, bro.": 0,
            "Basic Lifestyle -- Government ration for 1 person + Low tier apartment (1 Bedroom, 1 Bathroom & 1 Kitchen)": 10000,
            "Middle Class Lifestyle -- Food for 2 people + Mid tier apartment (1 Bedroom, 1 Bathroom, 1 Living Room & 1 Kitchen)": 50000,
            "Upper Class Lifestyle -- Middle Class Lifestyle + 2 children accomodation + Basic Healthcare": 200000,
            "Deluxe Lifestyle -- Food from top vendors + Villa + Advanced Healthcare + Entertainment": 1000000,
        }

        options = list(lifestyles.keys())
        options.append("Back")

        inquiry = [inq.List("choice", "I want to choose a", options)]
        lifestyle = inq.prompt(inquiry)["choice"]

        if lifestyle == "Back":
            return "profile"

        else:

            style = lifestyle.split(" -- ")[0]
            perks = lifestyle.split(" -- ")[1]
            cost = lifestyles[lifestyle]

            PopUp(
                style,
                f"[white]This lifestyle will cost me around $[red]{cost} [white]in cash. It comes with: [green]{perks}[/green]",
                inp=True,
            )

            inquiry = [
                inq.List("choice", "Let me see", ["Hell yeah!", "No, low on cash!"])
            ]
            choice = inq.prompt(inquiry)["choice"]

            if "yeah" in choice:

                if data["fortune"]["money"] >= cost:
                    data["fortune"]["money"] -= cost
                    event = f"[white]I have opted for {style}.[/white]"
                    PopUp("New Life!", event, inp=False)
                    data["lifestyle"] = lifestyle
                else:
                    PopUp(
                        "Knew it...",
                        "[white]It was all going fine until the payment. I didn't have enough money. [red]The agency told me to not waste their time...[/red]",
                        inp=False,
                    )
                    return "profile"

                if "No" in lifestyle:
                    data["lifestyle"] = None

                return "Action: " + event

            else:
                return "profile"

"#> ACTIVITIES: "
"""This module will handle all the player's activities, like -- Fun, Mischeif, etc.
Again, the <PATH> will help us with connecting to the events_data for fetching information.

Other than that, the code here is pretty self-explainatory.
Each action has its separate func.

Some actions will result in change of the values of the player's attributes.
Others will result in modifying the player's data (e.g. 'Visit a Doctor' can remove certain diseases).
"""


# * Imports:
from event_handler import PopUp
from modules import CentralDogma
import inquirer as inq
import random
from numpy.random import choice as npchoice
import json


# * Establishing the <Activities> class:
class Activities:

    def __new__(cls, data, PATH):

        with open(
            PATH + r"\jsonFiles\events_data.json",
            "r",
            encoding="utf-8",
        ) as file:
            evdata = json.load(file)

        action = cls.activity(cls, data, evdata)

        return action

    def activity(cls, data, evdata):

        PopUp("Activities", "[white]Hmm... what should I do today?[/white]", inp=True)

        if data["age"] < 19:
            cls.age = "toddler"

            choices = ["Fun", "Mischief"]

            if data["age"] > 4:
                cls.age = "child"
                choices = [
                    "Mind and Body",
                    "Visit a Doctor",
                    "Fun",
                    "Mischief",
                ]

        elif data["age"] >= 19:
            cls.age = "grown"
            choices = [
                "Mind and Body",
                "Visit a Doctor",
                "Fun",
                "Mischief",
            ]

        choices.append("Back")

        inquiry = [inq.List("choice", "Options", choices)]
        choice = inq.prompt(inquiry)["choice"]

        if "Fun" in choice:
            choice = cls.Fun(cls, data)
        elif "Mischief" in choice:
            choice = cls.Mischief(cls, data)
        elif "Doctor" in choice:
            choice = cls.Doctor(cls, data, evdata)
        elif "Mind" in choice:
            choice = cls.MindBody(cls, data)

        return choice

    def Fun(cls, data):

        PopUp(
            "I want to have some FUN!",
            "[white]What can I do for fun, though?[/white]",
            inp=True,
        )

        if cls.age == "toddler":
            choices = [
                "play with Lego blocks.",
                "play with dirt.",
                "laugh out loud!",
            ]

        elif cls.age == "child":
            choices = [
                "doodle in my notebook.",
                "play with my friends.",
                "play a videogame!",
                "watch an animated movie!",
            ]

        elif cls.age == "grown":
            choices = [
                "play football!",
                "play cricket!",
                "watch some TV.",
                "do some cycling.",
                "throw a good videogame onto the station!",
                "meet with my friends.",
                "go out for a movie!",
                "eat out!",
                "meet my grandparents!",
                "go to an adventure park.",
                "pick up a hobby!",
            ]

        choices.append("Back")

        inquiry = [inq.List("choice", "Options", choices)]
        choice = inq.prompt(inquiry)["choice"]
        choice = f"[white]I decided to {choice}[/white]"

        if data["caps"]["hap"] != 0 and "Back" not in choice:
            data["happiness"] += random.randint(3, 6)
            data["smarts"] -= random.randint(3, 6)
            CentralDogma(data)
            PopUp("I love it!", choice, inp=False)
            data["caps"]["hap"] -= 1

        elif "Back" in choice:
            choice = ""

        return "Action: " + choice

    def Mischief(cls, data):

        PopUp(
            "Mischeif eh? Mhmm let's see...",
            "[white]What can I do for fun, though?[/white]",
            inp=True,
        )

        if cls.age == "toddler":
            choices = [
                "start crying at night.",
                "poop on the brand new sofa.",
                "break a kitchen appliance.",
            ]

        elif cls.age == "child":
            choices = [
                "prank my elderly neighbour.",
                "throw stones at stray dogs.",
                "fly the birds away from water while they're drinking.",
                "burn some ants using a magnifying glass.",
            ]

        elif cls.age == "grown":
            choices = [
                "prank my elderly neighbour.",
                "throw stones at stray dogs.",
                "fly the birds away from water while they're drinking.",
                "burn some ants using a magnifying glass.",
                "lie to my friend about their mother's death.",
                "push a kid down the stairs.",
                "set a cat on fire.",
                "steal my friend's gaming set.",
            ]

        if data["age"] > 18:
            choices = [
                "prank my elderly neighbour.",
                "throw stones at stray dogs.",
                "fly the birds away from water while they're drinking.",
                "burn some ants using a magnifying glass.",
                "lie to my friend about their mother's death.",
                "push a kid down the stairs.",
                "set a cat on fire.",
                "steal my friend's gaming set.",
                "help a friend cheat on their partner.",
                "leave a blind person in the middle of a busy road.",
            ]

        choices.append("Back")

        inquiry = [inq.List("choice", "Options", choices)]
        choice = inq.prompt(inquiry)["choice"]
        choice = f"[white]I decided to {choice}[/white]"

        if data["caps"]["hap"] != 0 and "Back" not in choice:
            data["happiness"] += random.randint(6, 12)
            data["discipline"] -= random.randint(6, 12)
            CentralDogma(data)
            PopUp("Mwahahahaha!", choice, inp=False)
            data["caps"]["hap"] -= 1

        elif "Back" in choice:
            choice = ""

        return "Action: " + choice

    def Doctor(cls, data, evdata):

        if len(data["diseases"]) == 0:

            event = "[white]I visited the Doctor. [green]The Reports said that there's nothing to worry about.[/green]"

            PopUp(
                "Fit and Fine!",
                event,
                inp=False,
            )

            return "Action: " + event

        else:

            diseases = ""
            for disease in data["diseases"]:
                diseases += f"{disease}, "

            diseases = diseases[:-2]

            event = f"[white]I visited the Doctor. Turns out that I'm suffering from [red]{diseases}.[/red]"

            PopUp("Bad news!", event, inp=True)

            treat = [inq.List("choice", "I want to get rid of", data["diseases"])]
            choice = inq.prompt(treat)["choice"]

            if (
                choice in evdata["life"]["diseases"]["mild"]
                or choice in evdata["life"]["diseases"]["mild_birth_defects"]
            ):
                cost = random.randint(10000, 25000)
            else:
                cost = random.randint(50000, 200000)

            PopUp(
                "Let's hope for good...",
                f"[white]I think I should do something about my [red]{choice}[/red]. The expenses will be around $[red]{cost}[/red].",
                inp=True,
            )

            if data["age"] < 18:
                paychoices = [
                    "Yes. (Guardian will pay)",
                    "Nah... It doesn't really bother me.",
                ]
                pay = "guard"

            else:
                paychoices = [
                    "Yes, I'll pay.",
                    "Hard pass!",
                ]
                pay = "self"

            payment = [inq.List("choice", "Should I go with it?", paychoices)]
            paychoice = inq.prompt(payment)["choice"]

            if paychoice == paychoices[1]:
                event += f" I wanted to treat my [red]{choice}[/red], but then I decided to let it go."

            elif paychoice == paychoices[0]:

                def heal():

                    chance = npchoice(["yes", "no"], p=[0.75, 0.25])
                    if chance == "yes":
                        cure = f"[green]I have been cured of {choice}![/green]"
                        PopUp(
                            "Finally!",
                            cure,
                            inp=False,
                        )

                        event = f" I decided to treat my [red]{choice}[/red]. {cure}"

                        data["diseases"].remove(choice)
                        return event

                    else:
                        cure = f"[red]I continue to suffer from {choice}...[/red]"
                        PopUp(
                            "Tough Luck!",
                            cure,
                            inp=False,
                        )
                        return ""

                if (
                    choice in evdata["life"]["diseases"]["mild_birth_defects"]
                    or choice in evdata["life"]["diseases"]["mild"]
                ):
                    if pay == "guard":
                        event += heal()

                    elif pay == "self":
                        if data["fortune"]["money"] >= cost:
                            event += heal()
                            data["fortune"]["money"] -= cost
                        else:
                            cure = f"[red]I don't have enough money for that...[/red]"
                            PopUp(
                                "Poor, poor me...",
                                cure,
                                inp=False,
                            )
                            event += f" I decided to treat my [red]{choice}[/red], but {cure}"

                else:
                    cure = f"[red]I continue to suffer from {choice}...[/red]"
                    PopUp(
                        "Tough Luck!",
                        cure,
                        inp=False,
                    )
                    event += f" I decided to treat my [red]{choice}[/red], but {cure}"

        return "Action: " + event

    def MindBody(cls, data):

        PopUp(
            "Self Improvement? Hell yeah!",
            "[white]A healthy mind in a healthy body... What should I do for that?[/white]",
            inp=True,
        )

        choices = ["read a book.", "watch an educational video!"]

        if data["age"] > 9:
            choices += [
                "exercise.",
                "join a sports club!",
                "solve some puzzles!",
                "practice some Mathematics.",
            ]

        if data["age"] > 18:
            choices += [
                "join a gym!",
                "practice fasting.",
                "watch a biography.",
                "read some History.",
                "learn something new!",
            ]

        choices.append("Back")

        inquiry = [inq.List("choice", "Options", choices)]
        choice = inq.prompt(inquiry)["choice"]

        if "exercise" in choice or "join" in choice or "fast" in choice:
            if data["caps"]["hlt"] != 0 and "Back" not in choice:
                data["health"] += random.randint(3, 12)
                data["physique"] += random.randint(3, 12)
                data["looks"] += random.randint(3, 12)
                data["happiness"] -= random.randint(3, 6)
                data["discipline"] += random.randint(3, 6)
                CentralDogma(data)
                choice = f"[white]I decided to {choice}[/white]"
                PopUp("That's what I'm talking about!", choice, inp=False)
                data["caps"]["hlt"] -= 1

        elif "Back" in choice:
            choice = ""

        else:
            if data["caps"]["smr"] != 0 and "Back" not in choice:
                data["smarts"] += random.randint(3, 12)
                data["happiness"] -= random.randint(3, 6)
                data["discipline"] += random.randint(3, 6)
                CentralDogma(data)
                choice = f"[white]I decided to {choice}[/white]"
                PopUp("That's what I'm talking about!", choice, inp=False)
                data["caps"]["smr"] -= 1

        return "Action: " + choice

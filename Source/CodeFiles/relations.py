"#> RELATIONS: "
"""Simple, yet again.
The player's relations will be handled through this module.
The player will be able to:

- View their relations (viz. Parents, Partner, Children).
- Interact with each of these.
- Change the respective relationship attribute values with each of these.
- Ask for money from the parents.
- Make love to the partner

And... so on.
"""

import inquirer as inq
import random
from numpy.random import choice as npchoice
from event_handler import PopUp
from modules import cursor, CentralDogma, Entry, Bar


# * Establishing the Relations:
class Relations:

    def __new__(cls, data, PATH):

        rels = list(data["relations"].keys())
        reltypes = []

        for rel in rels:
            if len(data["relations"][rel]) != 0:
                reltypes.append(rel)

        reltypes.append("Back")

        PopUp(
            "Relations:",
            "[white]Yeah, I should check on my family regularly![/white]",
            inp=True,
        )

        inquiry = [inq.List("choice", "I want to interact with my", reltypes)]
        choice = inq.prompt(inquiry)["choice"]

        PopUp(f"{choice.capitalize()}:", "[white]Let's meet up![/white]", inp=True)

        if choice == "Back":
            pass

        elif choice != "partner":

            PopUp(
                f"{choice.capitalize()}:",
                f"[white]I wanna interact with...[white]",
                inp=True,
            )

            rel = list(data["relations"][choice].keys())
            rel.append("Back")

            inquiry = [inq.List("choice", f"{choice}", rel)]
            person = inq.prompt(inquiry)["choice"]

            PopUp(f"{choice.capitalize()}", "[white]Of course![white]", inp=True)

            if person == "Back":
                pass

            elif person in ["mother", "father"]:
                rel = data["relations"]["parents"][person]

                name = data["relations"]["parents"][person]["name"]
                age = data["relations"]["parents"][person]["age"]
                health = data["relations"]["parents"][person]["health"]
                relship = data["relations"]["parents"][person]["relationship"]

                health = Bar(
                    ratio=(health, 20), graphics="█", colours=("cyan", "gray15")
                )
                relship = Bar(
                    ratio=(relship, 20), graphics="█", colours=("cyan", "gray15")
                )

                if data["age"] < 6:
                    choices = ["spend time", "Back"]
                else:
                    choices = ["spend time", "ask for money", "insult", "Back"]

                PopUp(
                    f"{person.capitalize()}",
                    f"[yellow]Name: [white]{name}\n[yellow]Age: [white]{age}\n\n[yellow]Health[/yellow] {health}\n\n[yellow]Relationship[/yellow] {relship}",
                    inp=True,
                )

                inquiry = [inq.List("choice", f"I wanna", choices)]
                choice = inq.prompt(inquiry)["choice"]

                if "spend time" in choice:
                    event = f"[white]I spent time with my {person}.[/white]"
                    PopUp("Let's go!", event, inp=False)
                    data["relations"]["parents"][person][
                        "relationship"
                    ] += random.randint(12, 24)
                    data["happiness"] += random.randint(0, 6)
                    CentralDogma(data)

                    return "Action: " + event

                elif "money" in choice:
                    if data["relations"]["parents"][person]["relationship"] >= 75:
                        money = random.randint(1, 1000)
                        event = f"[white]I asked my {person} for some money. They gave me $[green]{money}[white] in cash![/white]"
                        data["fortune"]["money"] += money
                        data["happiness"] += random.randint(0, 6)
                        data["relations"]["parents"][person]["relationship"] -= 10
                    else:
                        event = f"[white]I asked my {person} for some money. [red]They refused to give me anything...[/red]"
                        data["relations"]["parents"][person]["relationship"] -= 15
                        data["happiness"] -= random.randint(0, 6)

                    PopUp("Wow...", event, inp=False)

                    CentralDogma(data)
                    return "Action: " + event

                elif "insult" in choice:
                    event = (
                        f"I insulted my {person}. [red]I was grounded for a week![/red]"
                    )
                    PopUp("Terrible!", event, inp=False)
                    data["relations"]["parents"][person]["relationship"] -= 35
                    data["happiness"] -= random.randint(3, 12)

                    CentralDogma(data)
                    return "Action: " + event

                else:
                    return "profile"

            else:

                age = data["relations"]["children"][person]["age"]
                health = data["relations"]["children"][person]["health"]
                relship = data["relations"]["children"][person]["relationship"]
                reltype = data["relations"]["children"][person]["type"]

                health = Bar(
                    ratio=(health, 20), graphics="█", colours=("cyan", "gray15")
                )
                relship = Bar(
                    ratio=(relship, 20), graphics="█", colours=("cyan", "gray15")
                )

                PopUp(
                    "Child",
                    f"[yellow]Name: [white]{person} ({reltype})\n[yellow]Age: [white]{age}\n\n[yellow]Health {health}\n\n[yellow]Relationship: {relship}",
                    inp=True,
                )

                choices = ["spend time", "Back"]

                inquiry = [inq.List("choice", f"I wanna", choices)]
                choice = inq.prompt(inquiry)["choice"]

                if choice == "spend time":

                    event = f"[white]I decided to {choice} with my {reltype}.[/white]"
                    PopUp("Let's go!", event, inp=False)

                    data["relations"]["children"][person][
                        "relationship"
                    ] += random.randint(12, 24)
                    data["happiness"] += 5

                    CentralDogma(data)

                    return "Action: " + event

                else:
                    pass

        else:

            name = data["relations"]["partner"]["name"]
            age = data["relations"]["partner"]["age"]
            partype = data["relations"]["partner"]["type"]
            health = data["relations"]["partner"]["health"]
            relship = data["relations"]["partner"]["relationship"]

            health = Bar(ratio=(health, 20), graphics="█", colours=("cyan", "gray15"))
            relship = Bar(ratio=(relship, 20), graphics="█", colours=("cyan", "gray15"))

            PopUp(
                f"{choice.capitalize()}:",
                f"[yellow]Name: [white]{name} ({partype})\n[yellow]Age: [white]{age}\n\n[yellow]Health {health}\n\n[yellow]Relationship: {relship}",
                inp=True,
            )

            choices = [
                "spend time",
                "make love",
                "part ways",
                "Back",
            ]

            inquiry = [inq.List("choice", "Let's", choices)]
            choice = inq.prompt(inquiry)["choice"]

            event = ""

            if choice == "Back":
                pass

            elif "part" not in choice:
                event = f"[white]I decided to {choice} with my {partype}.[/white]"

                PopUp("Let's go!", event, inp=False)

                if "time" in choice:
                    data["relations"]["partner"]["relationship"] += random.randint(
                        12, 24
                    )
                    data["happiness"] += 5

                    CentralDogma(data)

                elif "love" in choice:
                    data["relations"]["partner"]["relationship"] += random.randint(
                        24, 32
                    )
                    data["happiness"] += random.randint(6, 18)

                    ready = False

                    if not dict(data["relations"]["children"]):
                        ready = True

                    elif dict(data["relations"]["children"]):
                        childrenlist = list(data["relations"]["children"].keys())
                        if (
                            data["relations"]["children"][childrenlist[0]]["age"] > 3
                            and data["relations"]["partner"]["age"] <= 45
                            and ready == False
                        ):
                            ready = True

                    if ready == True:

                        chance = "yes"

                        if chance == "yes":
                            data["relations"]["partner"]["expecting"] = True
                            expecting = (
                                f"[green]Me and my {partype} are expecting![/green]"
                            )
                            PopUp("Good news!!!", expecting, inp=False)
                            data["happiness"] += 15

                        event += "\n" + expecting

                    CentralDogma(data)

            elif "part" in choice:
                PopUp(
                    "Thoughts...",
                    f"[white]I'm thinking about divorcing my {partype}...",
                    inp=True,
                )
                inquiry = [
                    inq.List(
                        "choice",
                        "If I'm so sure",
                        ["Yes, it's over!", "No... what was I thinking?"],
                    )
                ]
                choice = inq.prompt(inquiry)["choice"]

                if "Yes" in choice:
                    divorce = f"[red]I divorced my {partype}, {name}.[/red]"
                    PopUp("Sigh...", divorce, inp=False)
                    data["happiness"] -= 35
                    data["relations"]["partner"] = {}
                    event = divorce

            CentralDogma(data)

            return "Action: " + event

        return "profile"


# * Establishing the NewBorn:
"""The NewBorn class:
- Handles the birth of player's child.
- Handles its attribute allocation, as:
    - Naming (through an Entry widget).
    - Stats randomization.
    
Finally, throws a pop-up on the screen.
"""


class NewBorn:

    def __new__(cls, data, PATH):

        if data["age"] <= 35 and data["relations"]["partner"]["age"] <= 35:
            prob = [0.85, 0.15]
        elif data["age"] <= 45 and data["relations"]["partner"]["age"] <= 45:
            prob = [0.5, 0.5]
        else:
            prob = [0.0, 1.0]

        chance = npchoice(["yes", "no"], p=prob)

        if chance == "yes":

            gender = random.choice(["boy", "girl"])
            event = f"[green]I welcomed my new-born into this world![/green] It's a baby {gender}! I want a beautiful name!"

            def naming():

                PopUp("Good news!", event, inp=True)

                def getentry():

                    cursor(True)

                    name = Entry(
                        size=20,
                        coords=(20, 3),
                        border="green",
                        colour="cyan",
                        graphics="╭╮╰╯│─",
                    )

                    cursor(False)

                    name.replace(" ", "")

                    if len(name) == 0:
                        getentry()
                    else:
                        return name

                name = getentry()

                if name in data["relations"]["children"]:
                    PopUp(
                        "Error!",
                        "[yellow]You already have a child with that name! [white]Try again.",
                        inp=False,
                    )
                    naming()

                return name

            name = naming()
            if gender == "boy":
                gen = "son"
            else:
                gen = "daughter"

            child = {
                "age": 0,
                "type": gen,
                "health": random.randint(70, 100),
                "relationship": random.randint(70, 100),
            }

            event += f"\n[cyan]I named my baby {gender} '{name}' and I love it![/cyan]"
            data["relations"]["children"][name] = child
            data["relations"]["partner"]["expecting"] = False

            return "Action: " + event

        else:

            event = "[red]We lost the baby due to a miscarriage...[/red]"
            PopUp("God..?", event, inp=False)

            data["relations"]["partner"]["expecting"] = False
            data["happiness"] -= 50
            CentralDogma(data)

            return "Action: " + event

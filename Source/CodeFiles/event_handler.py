"#> EVENT HANDLER: "
"""The Event handler, as the name suggests, handles all the in-game events, like:
- Birth
- Childhood
- Youth
    - University
    - Graduation
    - Job
- Adulthood
    - Marriage
    - Childbirth
- Old age
- Death

As well as pop-ups and interactive events.
"""

import json
import random
from numpy.random import choice as npchoice
from modules import CentralDogma, goto, update
from rich import print
from rich.panel import Panel
import inquirer as inq


# * Create a <PopUp> class to handle all the pop-up events:
class PopUp:

    def __init__(self, head, foot, inp):

        if inp == False:
            endmessage = "\n\n\n[i][grey50]Press [yellow][i]Enter[/i][/yellow] to continue...[/i][/grey50]"
        else:
            endmessage = ""

        event = f"[b][u]{head}[/b][/u]\n\n{foot}{endmessage}"

        goto(15, 1)
        print(Panel(event, height=10, width=60, border_style="yellow", style="purple"))

        if inp == False:
            input()


# * Create an <Event> class to handle all the in-game events:
# ? This class is going to handle all the events that happen in the game.
"""The <Event> class will handle events, age by age.
Not only that, it will be working from the initiation (birth) itself.
Generating the birth events, carrying onto all the life event and finally -- Death.

The code is a bit lengthy, yet self-explainatory. Each age-event call is almost the same...
Most of this could've been packed into much, much shorter code (i.e. a simple func or class), but...
I didn't want to risk whatever stability the code has, as of now (IF ANY).
"""


class Event:

    def __init__(self, data, evdata, evpath, PATH, action=None):

        with open(
            PATH + r"\jsonFiles\demographics.json",
            "r",
            encoding="utf-8",
        ) as demfile:
            demographics = json.load(demfile)

        age = data["age"]

        # ? Deciding the parentage status of the character:
        if (
            "mother" in data["relations"]["parents"]
            and "father" in data["relations"]["parents"]
        ):
            parentage = "both"
            parents = "my mother, {} ({}), who works as {}; and my father, {} ({}), who works as {}".format(
                data["relations"]["parents"]["mother"]["name"],
                data["relations"]["parents"]["mother"]["age"],
                data["relations"]["parents"]["mother"]["job"],
                data["relations"]["parents"]["father"]["name"],
                data["relations"]["parents"]["father"]["age"],
                data["relations"]["parents"]["father"]["job"],
            )
        elif (
            "mother" in data["relations"]["parents"]
            and "father" not in data["relations"]["parents"]
        ):
            parentage = "mother"
            parents = "my mother, {} ({}), who works as {}".format(
                data["relations"]["parents"]["mother"]["name"],
                data["relations"]["parents"]["mother"]["age"],
                data["relations"]["parents"]["mother"]["job"],
            )
        elif (
            "father" in data["relations"]["parents"]
            and "mother" not in data["relations"]["parents"]
        ):
            parentage = "father"
            parents = "my father, {} ({}), who works as {}".format(
                data["relations"]["parents"]["father"]["name"],
                data["relations"]["parents"]["father"]["age"],
                data["relations"]["parents"]["father"]["job"],
            )

        self.parentage = parentage
        self.parents = parents

        def proposal():

            if (
                21 <= age < 50
                and len(data["relations"]["partner"]) == 0
                and data["looks"] > 40
                and age % 6 == 0
            ):

                country = data["location"].split(", ")[1]

                if data["gender"] == "male":
                    prop_first_name = random.choice(
                        demographics["countries"][country]["female_first_names"]
                    )
                    prop_last_name = random.choice(
                        demographics["countries"][country]["last_names"]
                    )
                    propname = f"{prop_first_name} {prop_last_name}"
                    propgender = "female"
                    propage = random.randint(age - 3, age + 3)
                    if propage < 30:
                        mesgen = "girl"
                    else:
                        mesgen = "woman"
                if data["gender"] == "female":
                    prop_first_name = random.choice(
                        demographics["countries"][country]["male_first_names"]
                    )
                    prop_last_name = random.choice(
                        demographics["countries"][country]["last_names"]
                    )
                    propname = f"{prop_first_name} {prop_last_name}"
                    propgender = "male"
                    propage = random.randint(age - 3, age + 3)
                    if propage < 30:
                        mesgen = "boy"
                    else:
                        mesgen = "man"

                PopUp(
                    "Love at last sight...?",
                    f"[white]A {mesgen} named [yellow]{propname} [white]({propage}) proposed you for marriage.[/white]",
                    inp=True,
                )
                inquiry = [
                    inq.List(
                        "choice",
                        "I think I will",
                        ["accept their proposal!", "reject them."],
                    )
                ]
                choice = inq.prompt(inquiry)["choice"]

                if "accept" in choice:

                    if propgender == "female":
                        proptype = "Wife"
                    elif propgender == "male":
                        proptype = "Husband"

                    partner = {
                        "name": propname,
                        "age": int(propage),
                        "gender": propgender,
                        "type": proptype,
                        "health": random.randint(50, 90),
                        "relationship": 50,
                        "expecting": False,
                    }

                    data["relations"]["partner"] = partner
                    event = f"\n[green]I've married a {propage} years old {mesgen} named {propname}![/green]"

                else:
                    event = f"\n[white]A {mesgen} named {propname} proposed me. I [red]rejected[white] the proposal![/white]"

            else:
                event = ""

            return event

        def getill(p1, p2):
            """Attributes:
            p1: Probability of getting a disease.
            p2: Mild-Fatal probability"""

            chance = npchoice(["yes", "no"], p=p1)

            if chance == "yes":
                if len(data["diseases"]) >= 2:
                    p1 = [0.25, 0.75]
                elif len(data["diseases"]) >= 4:
                    p1 = [0.01, 0.99]

            chance = npchoice(["yes", "no"], p=p1)

            if chance == "yes":
                chance = npchoice(["mild", "fatal"], p=p2)
                disease = random.choice(evdata["life"]["diseases"][chance])

                if disease not in data["diseases"]:
                    event = f"[white]I was diagnosed with [red]{disease} [white]today![/white]"
                    PopUp("Arghhh!!!", event, inp=False)
                    data["diseases"] += [disease]
                else:
                    event = f"[red]My {disease} is getting worse...[/red]"
                    PopUp("Oh no...", event, inp=False)

                return "\n" + event

            else:
                return ""

        if age == 0:
            event_log = (
                f"[yellow][Age: [white]{data['age']}[yellow]][/yellow] "
                + self.birth_events(data, evdata)
            )
            with open(
                evpath,
                "r+",
                encoding="utf-8",
            ) as log_file:
                read_file = log_file.read()
                if "[born]" not in read_file:
                    log_file.write(f"[born]\n{event_log}\n")

        if action == "age_up":

            if age == 60:

                if data["job"] != "Unemployed":

                    event = PopUp(
                        "Oldie!",
                        f"[yellow]I have retired from my job as {data['job']}.[/yellow]",
                        inp=False,
                    )

                    if data["job"] in ["Doctor", "Lawyer", "Professor"]:
                        data["job"] = "Retired " + data["job"]
                        data["fortune"]["salary"] = round(data["fortune"]["salary"] / 4)

                    else:
                        data["job"] = "Retired " + data["job"]
                        data["fortune"]["salary"] = 10000

                    event_log = (
                        f"[yellow][Age: [white]{data['age']}[yellow]][/yellow] {event}"
                    )

            for disease in data["diseases"]:
                if disease in evdata["life"]["diseases"]["fatal"]:
                    data["health"] -= 6
                    data["happiness"] -= 3
                else:
                    data["health"] -= 3
                    data["happiness"] -= 1

                CentralDogma(data)

            if 1 <= age < 5:
                event_log = (
                    f"[yellow][Age: [white]{data['age']}[yellow]][/yellow] "
                    + self.events("toddler_events", evdata)
                )

                if age % 3 == 0:
                    event = self.interactive("age3", data, evdata)
                    event_log = (
                        f"[yellow][Age: [white]{data['age']}[yellow]][/yellow] "
                        + self.events("toddler_events", evdata)
                        + "\n"
                        + event[0]
                    )

            elif 5 <= age < 13:

                event = self.events("child_events", evdata)
                event_log = (
                    f"[yellow][Age: [white]{data['age']}[yellow]][/yellow] " + event
                )

                if age % 3 == 0:
                    event = self.interactive("child", data, evdata)
                    event_log = (
                        f"[yellow][Age: [white]{data['age']}[yellow]][/yellow] "
                        + self.events("child_events", evdata)
                        + "\n"
                        + event[0]
                    )

                if age == 5:

                    popup = evdata["popups"]["age5"]

                    header = random.choice(popup["header"])
                    message = random.choice(popup["message"])

                    update()
                    PopUp(header, message, False)

                    event_log = (
                        f"[yellow][Age: [white]{data['age']}[yellow]][/yellow] "
                        + message
                        + "\n"
                        + event
                    )

                    data["job"] = "Elementary School student"

                if age == 10:

                    popup = evdata["popups"]["age10"]

                    header = random.choice(popup["header"])
                    message = random.choice(popup["message"])

                    update()
                    PopUp(header, message, False)

                    event_log = (
                        f"[yellow][Age: [white]{data['age']}[yellow]][/yellow] "
                        + message
                        + "\n"
                        + event
                    )

                    data["job"] = "Middle School student"
                    data["education"].insert(0, ["Elementary School"])

            elif 13 <= age < 16:

                if age == 13:
                    amount = random.randint(1000, 2000)
                    data["fortune"]["salary"] = amount
                    allowance = f"[white]I have started recieving allowance. The amount is going to be $[green]{amount}[/green] per year. I will get it upto age 19 only, I should use it wisely..."
                    event = self.events("young_teen_events", evdata)

                    PopUp("YEAH!!!", allowance, inp=False)

                    event_log = (
                        f"[yellow][Age: [white]{data['age']}[yellow]][/yellow] "
                        + event
                        + "\n"
                        + allowance
                    )

                else:
                    event = self.events("young_teen_events", evdata)
                    event_log = (
                        f"[yellow][Age: [white]{data['age']}[yellow]][/yellow] " + event
                    )

                if age == 14:

                    popup = evdata["popups"]["age15"]

                    header = random.choice(popup["header"])
                    message = random.choice(popup["message"])

                    update()
                    PopUp(header, message, False)

                    event_log = (
                        f"[yellow][Age: [white]{data['age']}[yellow]][/yellow] "
                        + message
                        + "\n"
                        + event
                    )

                    data["job"] = "High School student"
                    data["education"].insert(0, ["Middle School"])

                if age % 3 == 0:
                    event = self.interactive("young_teen", data, evdata)
                    event_log += (
                        "\n" + self.events("child_events", evdata) + "\n" + event[0]
                    )

            elif 16 <= age < 19:

                event = self.events("teen_events", evdata)
                event_log = (
                    f"[yellow][Age: [white]{data['age']}[yellow]][/yellow] " + event
                )

                if age % 3 == 0:
                    event = self.interactive("teen", data, evdata)
                    event_log += (
                        "\n" + self.events("child_events", evdata) + "\n" + event[0]
                    )

            elif 19 <= age < 25:

                event = self.events("youth_events", evdata)
                event_log = (
                    f"[yellow][Age: [white]{data['age']}[yellow]][/yellow] " + event
                )

                event_log += proposal()

                if age == 19:

                    if data["smarts"] >= 60:
                        event = self.interactive("university", data, evdata)
                        event_log = (
                            f"[yellow][Age: [white]{data['age']}[yellow]][/yellow] "
                            + self.events("youth_events", evdata)
                            + "\n"
                            + event[0]
                        )

                        majors = [
                            "Mathematics",
                            "Physics",
                            "Biology",
                            "Chemistry",
                            "Computer Science",
                            "Engineering",
                            "Language",
                            "Political Science",
                        ]

                        for major in majors:
                            if major in event[1]:
                                data["job"] = f"Undergrad student ({major} Major)"
                                break

                            else:
                                data["job"] = "Unemployed"

                        data["education"].insert(0, ["High School"])
                        data["happiness"] += 20
                        CentralDogma(data)

                    elif 40 <= data["smarts"] < 60:

                        event = "[white]I graduated from school, but couldn't clear the entrance exams. So... no University, I guess...[/white]"

                        PopUp("Sheesh!", event, inp=False)

                        event_log = (
                            f"[yellow][Age: [white]{data['age']}[yellow]][/yellow] "
                            + self.events("youth_events", evdata)
                            + "\n"
                            + event
                        )

                        data["education"].insert(0, ["High School"])
                        data["job"] = "Unemployed"
                        data["happiness"] -= 40
                        CentralDogma(data)

                    else:

                        event = "[white]I couldn't graduate from High School...[/white]"

                        PopUp("The hell???", event, inp=False)

                        event_log = (
                            f"[yellow][Age: [white]{data['age']}[yellow]][/yellow] "
                            + self.events("youth_events", evdata)
                            + "\n"
                            + event
                        )

                        data["job"] = "Unemployed"
                        data["happiness"] -= 60
                        CentralDogma(data)

                major = (
                    data["job"]
                    .replace("Undergrad ", "")
                    .replace(" Major", "")
                    .replace("student ", "")
                    .replace("(", "")
                    .replace(")", "")
                )

                if age == 23 and "Undergrad" in data["job"]:

                    def graduate():
                        event = self.events("youth_events", evdata)
                        event_now = f"[white]I graduated from the University with a {major} degree![/white]"
                        event_log = (
                            f"[yellow][Age: [white]{data['age']}[yellow]][/yellow] "
                            + event_now
                            + "\n"
                            + event
                        )

                        PopUp(
                            "Moving Ahead!",
                            event_now,
                            False,
                        )

                        data["job"] = "Unemployed"
                        data["education"].insert(0, f"Bachelors in {major}")
                        data["happiness"] += 20
                        CentralDogma(data)

                        return event_log

                    if data["smarts"] >= 75:
                        grad_event = graduate()
                        event_now = ""

                        if major not in ["Computer Science", "Engineering"]:
                            event_now = f"[white]Should I try for Graduate School?"
                            PopUp("What to do?", event_now, inp=True)

                            choices = [
                                f"apply as a Ph.D. candidate for {major}!",
                                "let it go...",
                            ]

                            if major in ["Biology", "Chemistry"]:
                                choices.insert(1, "apply to a Medical School.")
                            elif major == "Political Science":
                                choices.insert(1, "apply to a Law School.")

                            inquiry = [inq.List("choice", "I think I should", choices)]
                            choice = inq.prompt(inquiry)["choice"]

                            if data["smarts"] > 85:
                                prob = [0.95, 0.05]
                            else:
                                prob = [0.65, 0.35]

                            chance = npchoice(["yes", "no"], p=prob)

                            if chance == "no":
                                event_now = "[red]My application was rejected![/red]"
                                PopUp(
                                    "Tough luck!",
                                    event_now,
                                    inp=False,
                                )
                                data["happiness"] -= 30
                                CentralDogma(data)

                            elif chance == "yes":
                                if (
                                    major in ["Biology", "Chemistry"]
                                    and "Medical" in choice
                                ):
                                    event_now = "[green]I've been accepted into Medical School![/green]"
                                    PopUp(
                                        "That's right!",
                                        event_now,
                                        inp=False,
                                    )
                                    data["job"] = "Medical student"
                                elif major == "Political Science" and "Law" in choice:
                                    event_now = "[green]I've been accepted into Law School![/green]"
                                    PopUp(
                                        "That's right!",
                                        event_now,
                                        inp=False,
                                    )
                                    data["job"] = "Law student"
                                else:
                                    stipend = random.randint(25000, 50000)
                                    event_now = f"[white]I have been accepted as a Ph.D. candidate for {major}! I will be recieving a stipend of $[green]{stipend}[/green] per year![/white]"
                                    PopUp(
                                        "Well... nice!",
                                        event_now,
                                        inp=False,
                                    )
                                    data["job"] = f"Ph.D. {major} student"
                                    data["fortune"]["salary"] = stipend

                                data["happiness"] += 30
                                CentralDogma(data)

                        event_log = grad_event + "\n" + event_now

                    elif 60 <= data["smarts"] < 75:

                        event_log = graduate()

                    else:

                        event = "[red]I was expelled from University due to bad performance...[/red]"

                        PopUp("What am I gonna do now???", event, inp=False)

                        event_log = (
                            f"[yellow][Age: [white]{data['age']}[yellow]][/yellow] "
                            + self.events("youth_events", evdata)
                            + "\n"
                            + event
                        )

                        data["job"] = "Unemployed"
                        data["happiness"] = 10
                        CentralDogma(data)

                if age % 3 == 0:
                    event = self.interactive("youth", data, evdata)
                    event_log += (
                        "\n" + self.events("youth_events", evdata) + "\n" + event[0]
                    )

            elif 25 <= age < 45:

                if data["physique"] <= 20:
                    data["health"] -= 1

                CentralDogma(data)

                event = self.events("adult_events", evdata)
                event_log = (
                    f"[yellow][Age: [white]{data['age']}[yellow]][/yellow] " + event
                )

                event_log += proposal()

                if age == 27 and "Medical" in data["job"]:
                    if data["smarts"] > 80:
                        grad_event = "[green]I have completed Medical School![/green]"
                        PopUp("Yeahhh!", grad_event, inp=False)
                        data["job"] = "Unemployed"
                        data["education"].insert(0, "M.D. (Doctor of Medicine)")
                    else:
                        grad_event = "[red]I had to leave my Medical education because of poor performance...[/red]"
                        PopUp("I wanna die...", grad_event, inp=False)
                        data["job"] = "Unemployed"
                    event_log = f"[yellow][Age: [white]{data['age']}[yellow]][/yellow] {grad_event}"

                elif age == 26 and "Law" in data["job"]:
                    if data["smarts"] > 80:
                        grad_event = "[green]I have completed Law School![/green]"
                        PopUp("Yeahhh!", grad_event, inp=False)
                        data["job"] = "Unemployed"
                        data["education"].insert(0, "J.D. (Juris Doctor)")
                    else:
                        grad_event = "[red]I had to leave my Law education because of poor performance...[/red]"
                        PopUp("I wanna die...", grad_event, inp=False)
                        data["job"] = "Unemployed"
                    event_log = f"[yellow][Age: [white]{data['age']}[yellow]][/yellow] {grad_event}"

                elif age == 27 and "Ph.D." in data["job"]:

                    major = data["job"].replace("Ph.D. ", "").replace(" student", "")

                    if data["smarts"] > 80:
                        grad_event = (
                            f"[green]I have completed my Ph.D. in {major}![/green]"
                        )
                        PopUp("Yeahhh!", grad_event, inp=False)
                        data["job"] = "Unemployed"
                        data["education"].insert(
                            0, f"Ph.D. (Doctor of Philosophy) in {major}"
                        )
                    else:
                        grad_event = "[red]I had to give up on a Ph.D. because of poor performance...[/red]"
                        PopUp("I wanna die...", grad_event, inp=False)
                        data["job"] = "Unemployed"
                    event_log = f"[yellow][Age: [white]{data['age']}[yellow]][/yellow] {grad_event}"

                if data["health"] <= 10:
                    event_log += getill([0.75, 0.25], [0.85, 0.15])

                if age % 5 == 0:
                    event = self.interactive("adult", data, evdata)
                    event_log += (
                        "\n" + self.events("adult_events", evdata) + "\n" + event[0]
                    )

            elif 45 <= age < 60:

                event = self.events("mid_age_events", evdata)
                event_log = (
                    f"[yellow][Age: [white]{data['age']}[yellow]][/yellow] " + event
                )

                data["health"] -= 3

                CentralDogma(data)

                if data["health"] <= 10:
                    event_log += getill([0.85, 0.15], [0.5, 0.5])

                if age % 5 == 0:
                    event = self.interactive("mid_age", data, evdata)
                    event_log += (
                        "\n" + self.events("mid_age_events", evdata) + "\n" + event[0]
                    )

            elif age >= 60:

                event = self.events("old_age_events", evdata)
                event_log = (
                    f"[yellow][Age: [white]{data['age']}[yellow]][/yellow] " + event
                )

                data["health"] -= 6

                CentralDogma(data)

                if data["health"] <= 10:
                    event_log += getill([0.95, 0.05], [0.75, 0.25])

                if age % 5 == 0:
                    event = self.interactive("old_age", data, evdata)
                    event_log += (
                        "\n" + self.events("old_age_events", evdata) + "\n" + event[0]
                    )

            else:
                event_log = f"[yellow][Age: [white]{data['age']}[yellow]][/yellow] Nothing interesting us happening nowadays..."

            if data["lifestyle"] != None:
                cost = evdata["life"]["lifestyles"][data["lifestyle"]]
                data["fortune"]["money"] -= cost

                if "Basic" in data["lifestyle"]:
                    data["happiness"] += 1
                    data["health"] += 1

                elif "Middle" in data["lifestyle"]:
                    data["happiness"] += 3
                    data["health"] += 3
                    data["physique"] += 1

                elif "Upper" in data["lifestyle"]:
                    data["happiness"] += 6
                    data["health"] += 12
                    data["physique"] += 3

                    if dict(data["partner"]) is True:
                        data["partner"]["health"] += 3
                        data["partner"]["relationship"] += 6

                    if dict(data["children"]) is True:
                        for child in data["children"]:
                            data["children"][child]["health"] += 3
                            data["children"][child]["relationship"] += 6

                elif "Deluxe" in data["lifestyle"]:
                    data["happiness"] += 12
                    data["health"] += 24
                    data["physique"] += 6

                    if dict(data["partner"]) is True:
                        data["partner"]["health"] += 6
                        data["partner"]["relationship"] += 12

                    if dict(data["children"]) is True:
                        for child in data["children"]:
                            data["children"][child]["health"] += 6
                            data["children"][child]["relationship"] += 12

                if data["fortune"]["money"] < cost:
                    event = "[red]My Lifestyle has been cancelled due to insufficient funds...[/red]"
                    data["lifestyle"] = None
                    PopUp("Sheesh!", event, inp=False)
                    event_log += "\n" + event

            with open(
                evpath,
                "a",
                encoding="utf-8",
            ) as log_file:
                log_file.write(f"{event_log}\n")

        elif action is not None and "Action: " in action:

            event_log = action.replace("Action: ", "")

            if event_log == "":
                pass

            else:
                with open(
                    evpath,
                    "a",
                    encoding="utf-8",
                ) as log_file:
                    log_file.write(f"{event_log}\n")

    # * Create birth events to be displayed on the birth of the main character:
    # ? The events that are to be assigned right at the birth of the character, are decided here.
    def birth_events(self, data, evdata):

        age = data["age"]

        keys = evdata["birth_events"]["keys"]

        # ? Preparing the birth event:
        intro = str(random.choice(evdata["birth_events"]["intro"]))

        for key in keys:
            new_key = key.replace("{", "").replace("}", "")
            if new_key in data:
                value = data[new_key]
                intro = intro.replace(key, value)
            elif new_key in evdata["birth_events"]:
                value = random.choice(evdata["birth_events"][new_key])
                intro = intro.replace(key, value)
            elif new_key == "parents":
                intro = intro.replace(key, self.parents)

        # ? Preparing the health info:
        shortcoming = None
        if 30 <= data["health"] < 40:
            shortcoming = "mild"
            data["physique"] = data["physique"] - (40 - (40 - data["health"]))
        elif 20 <= data["health"] < 30:
            shortcoming = "severe"
            data["physique"] = data["physique"] - (40 - (40 - data["health"]))
        elif 0 <= data["health"] < 20:
            shortcoming = "fatal"
            data["physique"] = data["physique"] - (80 - (40 - data["health"]))

        # The <CentralDogma> cleans up the sub-minimum and par-maximum attribute values.
        CentralDogma(data)

        if shortcoming is not None:
            health = str(random.choice(evdata["birth_events"]["health"][shortcoming]))

            if "{diseases}" in health:
                if shortcoming == "severe":
                    disease = random.choice(
                        list(evdata["life"]["diseases"]["mild_birth_defects"])
                    )
                    if disease not in data["diseases"] and age == 0:
                        data["diseases"].append(disease)
                        if len(data["diseases"]) > 1:
                            data["diseases"] = [data["diseases"][0]]

                elif shortcoming == "fatal":
                    disease = random.choice(
                        list(evdata["life"]["diseases"]["fatal_birth_defects"])
                    )
                    if disease not in data["diseases"] and age < 2:
                        data["diseases"].append(disease)
                        if len(data["diseases"]) > 1:
                            data["diseases"] = [data["diseases"][0]]

                health = health.replace("{diseases}", disease)

            health = " " + health

        else:
            health = ""

        return intro + health

    def events(self, event_type, evdata):
        keys = evdata[event_type]["keys"]

        event = str(random.choice(evdata[event_type]["events"]))

        for key in keys:
            new_key = key.replace("{", "").replace("}", "")
            value = random.choice(evdata[event_type][new_key])
            event = event.replace(key, value)

        if self.parentage == "both":
            value = random.choice(("mother", "father"))
        else:
            value = self.parentage

        event = event.replace("{parent}", value)

        return event

    # * Create interactive events:

    def interactive(self, event_type, data, evdata):

        popup = evdata["interactive"][event_type]

        header = random.choice(popup["head"])
        message = random.choice(list(popup["message"].keys()))

        def blank_replace(sentence):

            keys = evdata["interactive"][event_type]["keys"]
            result = sentence

            for key in keys:
                if key != "{parent}":
                    new_key = key.replace("{", "").replace("}", "")
                    value = random.choice(evdata["interactive"][event_type][new_key])
                    result = result.replace(key, value)

                if key == "{parent}":
                    if self.parentage == "both":
                        value = random.choice(("mother", "father"))
                    else:
                        value = self.parentage
                    result = result.replace(key, value)

            return result

        new_message = blank_replace(message)

        raw_choices = list(popup["message"][message]["options"].keys())
        random.shuffle(raw_choices)
        choices = []

        for choice in raw_choices:

            choices.append(blank_replace(choice))

        update()
        PopUp(header, new_message, True)

        inquiry = [inq.List("choice", "I decided", choices=choices)]
        choice = inq.prompt(inquiry)["choice"]
        reaction = random.choice(
            popup["message"][message]["options"][
                f"{list(raw_choices)[choices.index(choice)]}"
            ]
        )

        reaction = blank_replace(reaction)
        event = new_message

        turnouts = {
            "[+hlt]": "health",
            "[-hlt]": "health",
            "[+hap]": "happiness",
            "[-hap]": "happiness",
            "[+smr]": "smarts",
            "[-smr]": "smarts",
            "[+lks]": "looks",
            "[-lks]": "looks",
            "[+phy]": "physique",
            "[-phy]": "physique",
            "[+dis]": "discipline",
            "[-dis]": "discipline",
        }

        for turnout in turnouts:
            if turnout in reaction:
                if "+" in turnout:
                    data[turnouts[turnout]] += random.randint(5, 15)
                elif "-" in turnout:
                    data[turnouts[turnout]] -= random.randint(5, 15)

                reaction = reaction.replace(turnout, "")
            CentralDogma(data)

        event_log = event + " " + f"I decided {choice} " + reaction

        return event_log, choice

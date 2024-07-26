"#> CAREER: "
"""This module handles the player's career.

- Various jobs are fetched from the <.json> data file.
- Then the jobs are presented against their educational requirements and pay ranges.
- The eligibility of the player is checked.
- Finally, the player gets the job, if eligible (with subtle selection randomization, for fun).

Rest... nothing fancy, self-explainatory code.
"""


# * Imports:
from event_handler import PopUp
from modules import CentralDogma
import inquirer as inq
import json
import random


# * Establishing a <Career> class:
class Career:

    def __new__(cls, data, PATH):

        with open(
            PATH + r"\jsonFiles\events_data.json",
            "r",
            encoding="utf-8",
        ) as file:
            evdata = json.load(file)

        if "student" in data["job"]:
            PopUp(
                "Oops!",
                "[yellow]Can't have a career as a full-time student.[/yellow]",
                inp=False,
            )

            return "career"

        else:
            PopUp(
                "I think a job would be nice...",
                "[white]What should I do tho? Am I eligible for some good jobs or would I have to try my luck with an entry level? [yellow]Would I even get one?[/yellow]",
                inp=True,
            )

            levels = list(evdata["life"]["jobs"].keys())
            levels.remove("Top")
            levels.append("Back")
            inquiry = [inq.List("choice", "I'm looking for", levels)]
            jobtype = inq.prompt(inquiry)["choice"]

            if jobtype == "Back":
                return "career"

            PopUp(
                "Decision...",
                f"[white]I'm thinking of some {jobtype} level jobs...[/white]",
                inp=True,
            )

            jobs = list(evdata["life"]["jobs"][jobtype].keys())
            jobs.append("Back")
            inquiry = [inq.List("choice", "I want to try for", jobs)]
            job = inq.prompt(inquiry)["choice"]

            if job == "Back":
                return "career"

            education = evdata["life"]["jobs"][jobtype][job]["req"]
            pay = evdata["life"]["jobs"][jobtype][job]["pay"]
            requirements = f"[yellow]Educational Requirements for this job: [white]{education}\n[yellow]Average pay: [white]$[green]{pay[0]} [white]- [green]{pay[1]}[/green]"

            PopUp(f"Job: {job}", f"Requirements:\n{requirements}", inp=True)
            inquiry = [
                inq.List(
                    "choice",
                    "I should try for it",
                    ["Yes, of course!", "Nah, I deserve better..."],
                )
            ]
            choice = inq.prompt(inquiry)["choice"]

            if "Yes" in choice:
                salary = None
                if education not in ["Ph.D.", "M.D.", "J.D.", "Bachelors", "None"]:
                    if education in data["education"]:
                        salary = random.randint(pay[0], pay[1])
                        PopUp(
                            "Sweet Money!",
                            f"[white]I got a position as {job}! My salary will be $[green]{salary}[white] all in cash!",
                            inp=False,
                        )
                elif education == "M.D.":
                    if "M.D." in data["education"][0]:
                        salary = random.randint(pay[0], pay[1])
                        PopUp(
                            "Sweet Money!",
                            f"[white]I got a position as {job}! My salary will be $[green]{salary}[white] all in cash!",
                            inp=False,
                        )
                elif education == "J.D.":
                    if "J.D." in data["education"][0]:
                        salary = random.randint(pay[0], pay[1])
                        PopUp(
                            "Sweet Money!",
                            f"[white]I got a position as {job}! My salary will be $[green]{salary}[white] all in cash!",
                            inp=False,
                        )
                elif education == "Ph.D.":
                    if "Ph.D." in data["education"][0]:
                        salary = random.randint(pay[0], pay[1])
                        PopUp(
                            "Sweet Money!",
                            f"[white]I got a position as {job}! My salary will be $[green]{salary}[white] all in cash!",
                            inp=False,
                        )
                elif (
                    education == "Bachelors"
                    and "Bachelors" in data["education"][0]
                    or "Bachelors" in data["education"][1]
                ):
                    salary = random.randint(pay[0], pay[1])
                    PopUp(
                        "Sweet Money!",
                        f"[white]I got a position as {job}! My salary will be $[green]{salary}[white] all in cash!",
                        inp=False,
                    )
                elif education == "None":
                    salary = random.randint(pay[0], pay[1])
                    PopUp(
                        "Sweet Money!",
                        f"[white]I got a position as {job}! My salary will be $[green]{salary}[white] all in cash!",
                        inp=False,
                    )

                if salary is not None:
                    event = f"[green]I started working as [white]{job}[green] from today![/green]"
                    data["job"] = job
                    data["fortune"]["salary"] = salary
                    data["happiness"] += 20
                    CentralDogma(data)

                else:
                    PopUp(
                        "Tough Luck!",
                        f"[red]They threw my resume in the trash! How rude!?[red]",
                        inp=False,
                    )
                    data["happiness"] -= 20
                    CentralDogma(data)

                    event = f"[red]I applied for a position as [white]{job}[red], but couldn't get it...[/red]"

                return "Action: " + event

            else:
                return "career"

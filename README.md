# BitZoo
**A Life Simulator game written in Python.**

<sup>*An example image from a gameplay is also provided below.*</sup>

## About
**BitZoo** is fun project that I created over the span of (almost) six days. It is quite basic, raw and a lot lenient as far as the coding style goes. Well, I've intended it to be that way -- a fun project, from a beginner.

Before diving deep into the whatabouts of the program, I'll firstly like to share the meaning behind the game's name.
The name *BitZoo* can be etymologically described as follows:
* **Bit**: The usual digital *bit* (Binary Digit).
* **Zoo**: The **Kashmiri** word for *life* (*Zuw*) -- just like the **Greek** *Zoi*.

Now, with that out of the way, let's move onto the actual project.

## Features
<sub>*An example image from a gameplay session:*</sub>

![BitZoo_screenshot](https://github.com/user-attachments/assets/177b79e3-a3df-4339-a223-da7dea79b6dd)

The project, and thus, the game itself is inspired from the plethora of *life simulators* out there. The name of my project might unequivocally point towards such a possibility. I've tried to implement the utmost basic mechanics of an average *life simulator* into my humble project. These include:
* **Menu**
	* A menu is basically needed in every game. It has various navigation options.
  * A new game can be started, or we can load a saved game from the system.
  * The saved games can also be deleted.
* **Home Screen**
  * The screen where most of the gameplay happens. It consists of various UI elements, such as:
    * Player's name.
    * Location.
    * Money and salary.
    * Status bars for health, happiness, smarts, etc.
    * The events log screen (sort of a journal, where the player's life events are displayed).
    * Navigation menu with various options, like:
      	* Profile.
      	* Relations.
      	* Activities.
      	* Career.
      	* Lifestyle.
* **Profile**
  * A profile that shows information about the player. Such as the name, age, location, so on and so forth.
* **Relations**
  * The player can interact with their *relatives* as in most of the *lifesims*.
* **Activities**
  * The Activities tab provides the player with a set of activities. Nothing fancy, just regular *lifesim* gameplay options.
* **Career**
  * An option which enables the player to seek a job and earn money.
* **Lifestyle**
  * From money earnt to money spent! This option provides the player with some use of their *salary* in the form of a tier based list of lifestyles, from which, a suitable lifestyle can be chosen to avail its perks.

As it can be seen. The game is presented as a TUI (Terminal User Interface) program. Thus, it's lightweight, but it comes with its own set of dependencies, which we'll be discussing below.

## Installation
**This project is built keeping the Windows Operating System in mind.**
As usual, download or clone this repository and follow along!
### Getting Python
This project has been created in **Python** - *version: 3.11.9* (the latest version would work just fine -- I'm working with an older version for a different use case) and therefore, if you don't already have Python, you'll have to get it from the following link:

[The official Python website](https://www.python.org/)

### Installing all the dependencies
This project uses the following libraries, as specified in the `requirements.txt` in the Source file.
* Python - `inquirer` ver: 3.3.0
*	Python - `numpy` ver: 2.0.1
*	Python - `rich` ver: 13.7.1

To install these dependencies, you'll have to open the `cmd` (Command Prompt) on your Windows OS, or just open the Windows Terminal (if installed from the store). Then, you have to navigate to the path of the `\BitZoo` directory stored on your system and type the following command:

`pip install -r requirements.txt`

Alternatively, the following command:

`python -m pip install -r requirements.txt`

If this doesn't work, then try the following command:

`py -m pip install -r requirements.txt`

Assuming that the installation has been successful for you, we can move onto the next step.

## Initializing the game
### From the File Explorer
Head over to the folder where you have downloaded the `\BitZoo` repo. Open it. Go inside the `\Source` repo and then run the `\game.py` file.

### From the Console
Open up `cmd` or Windows Terminal. With the help of the `cd` commands, locate the directory in which the `\BitZoo` repo is present on your system. Navigate to `\Source` using the `cd` command and then type the command `python game.py` or alternatively, `py game.py` to start the game.

*Pertaining to personal experience, it is suggested that you install the [**Windows Terminal**](https://apps.microsoft.com/detail/9n0dx20hk701?hl=en-US&gl=US) -- purely for aesthetic reasons, here. Also, as a side note, if you want your game to look exactly like the one in the example image, then you should try out the **One Half Dark** Windows Terminal colour scheme.*

## Conclusion
Well, that's all. I hope you enjoy this little game! Check out the source-code if possible. Play around with the `.json` files and have your custom places and scenarios playable, as per your taste. Play around with the code if you want. Let me know if you come across any errors or akin. Although I do not plan to work further on this project, since it was for fun, I am open to discussions about the code, and tweaks in it as well. So, let me know and I'll try to come up with a solution, or better, we could work on it together!

**If you plan on modifying and/or distributing this project or any significant code from it, please read the `LICENSE.md` file of the `\BitZoo` repository, as well as the `LICENSE.md` files of each source repository, thoroughly. Be sure that you're in line with the GPL-3 License while doing this.**

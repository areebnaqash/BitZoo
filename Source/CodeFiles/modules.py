"#> MODULES: "
"""All my custom funcs, classes for the game, have been written here.
These include:

    - update()
        - used to update the screen, with ANSI Escape codes. Hence, no flicker.

    - clear()
        - clears the screen with 'cls' command. Has flickering.

    - Entry()
        - A length imited, TUI Entry widget that I created.

    - CentralDogma()
        - A 'dogma' to handle in-game character attributes.
"""

import sys
from msvcrt import getch

styles = {
    "black": 30,
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
}


def cursor(toggle=True):
    if toggle == True:
        sys.stdout.write("\033[?25h")
    elif toggle == False:
        sys.stdout.write("\033[?25l")


def update():
    """A function to clear the terminal screen."""
    sys.stdout.write("\033[1;1f")


def clear():
    sys.stdout.write("\033c")


def goto(x, y):
    """A function to move the cursor within the terminal.

    x: Number of characters to traverse (horizontal axis).
    y: Number of lines to traverse (vertical axis).
    """

    sys.stdout.write(f"\033[{x};{y}f")


def getinput(limit):
    """A modified version of the input() function of Python, with length limit.

    limit: Maximum length of the input."""

    input_text = ""

    while True:
        try:
            char = getch()
            if char == b"\r":
                print()
                return input_text
                break
            elif char == b"\x08":
                if input_text:
                    input_text = input_text[:-1]

                    print("\b \b", end="", flush=True)
            elif len(input_text) < limit:
                input_text += char.decode()
                print(char.decode(), end="", flush=True)

        except:
            pass


class Entry:
    """An Entry widget for the terminal.

    Attributes:
    size: Maximun length of the input to be taken.
    coords: Coordinates of the widget on the screen.
    border: Colour of the borders of the widget.
    colour: Colour of the input text.
    graphics: A string containing the shapes used to make the borders of the widget.
    """

    def __new__(cls, size, coords=None, border=None, colour=None, graphics=None):
        cls.size = size
        cls.coords = coords
        cls.border = border
        cls.colour = colour
        result = cls.build_entry(
            cls,
            size=cls.size,
            coords=cls.coords,
            border=cls.border,
            colour=cls.colour,
            graphics=graphics,
        )
        return result

    def build_entry(cls, size, coords, border, colour, graphics):

        if graphics is None:
            corners = ["+", "+", "+", "+"]
            vertical = "|"
            horizontal = "-"
        elif graphics is not None:
            graphics = list(graphics)
            corners = graphics[:4]
            vertical = graphics[4]
            horizontal = graphics[5]

        if coords is not None:
            x, y = coords
            goto(x, y)

        if border is not None:
            sys.stdout.write(f"\033[{styles[border]}m")

        print("%s%s%s" % (corners[0], (horizontal[0] * size), corners[1]))
        if coords is not None:
            goto(x + 1, y)
        print("%s%s%s" % (vertical, (" " * size), vertical[0]))
        if coords is not None:
            goto(x + 2, y)
        print("%s%s%s" % (corners[2], (horizontal[0] * size), corners[3]))

        sys.stdout.write("\033[0m")

        if coords is not None:
            goto(x + 1, y + 1)
        else:
            sys.stdout.write("\033[A\033[A\033[C")

        if colour is not None:
            sys.stdout.write(f"\033[{styles[colour]}m")

        inp = getinput(size)

        sys.stdout.write("\033[0m")

        if coords is not None:
            goto(x + 2, 1)
        else:
            sys.stdout.write("\033[B")

        return inp


class Bar:
    """A Bar widget for the terminal. [Needs the <rich> library for desired performance]

    Attributes:
    ratio: (x, y) where x is the percentage (rounded) and y is the Bar length.
    graphics: A string containing the Bar placeholder.
    colours: Colours of the current and missing bar values.
    """

    def __new__(cls, ratio, graphics, colours):
        percent, maxi = ratio
        mini = round((maxi * percent) / 100)
        return cls.build_bar(cls, mini, maxi, graphics, colours, percent)

    def build_bar(cls, mini, maxi, graphics, colours, percent):
        c1 = f"[{colours[0]}]"
        c2 = f"[{colours[1]}]"
        return "%s%s%s%s [white]%s[/white]" % (
            c1,
            graphics * mini,
            c2,
            graphics * (maxi - mini),
            str(percent) + "%",
        )


# * Now, let's define a few funcs that will be used in-game.


def CentralDogma(data, ageup=None):
    """The CentralDogma is set up in order to ensure that:

    - The sub-minimum (less than the lowest point of the range) and...
        the par-maximum (more than the highest point of the range) values
        of the different (character) attributes aren't crossed.

    - The values are in between 0 and 100, and do not subceed or exceed this range.
    """

    attrs = [
        "health",
        "happiness",
        "smarts",
        "looks",
        "physique",
        "discipline",
    ]

    for attr in attrs:

        if data[attr] > 100:
            data[attr] = 100
        elif data[attr] < 0:
            data[attr] = 0

    relattrs = ["health", "relationship"]

    for attr in relattrs:
        for reltype in data["relations"]:
            if reltype != "partner":
                for rel in data["relations"][reltype]:
                    if data["relations"][reltype][rel][attr] > 100:
                        data["relations"][reltype][rel][attr] = 100
                    elif data["relations"][reltype][rel][attr] < 0:
                        data["relations"][reltype][rel][attr] = 0
            elif reltype == "partner":
                if dict(data["relations"][reltype]):
                    if data["relations"][reltype][attr] > 100:
                        data["relations"][reltype][attr] = 100
                    elif data["relations"][reltype][attr] < 0:
                        data["relations"][reltype][attr] = 0

    if ageup == True:

        attrs2 = ["hlt", "hap", "smr", "lks", "phy", "dis"]

        for attr in attrs2:
            data["caps"][attr] = 6

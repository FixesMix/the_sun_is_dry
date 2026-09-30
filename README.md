![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Status](https://img.shields.io/badge/status-in--progress-yellow)
# The Sun is Dry

A terminal-based visual novel engine written in Python. Stories are written in a custom
keyword format inside a `.docx` file, parsed into branching nodes, then played back
in the terminal with 24-bit color images, save/load, and branching.

*The Sun is Dry* is a story about the world
existing once the sun has left, as well as a small demonstration of the engine's features. 

![Terminal gameplay showing colored ASCII rendering](EXAMPLES/EXAMPLE%20the_sun_is_dry_GIFTerm.gif)

## Table of Contents

- [Features](#features)
- [To Run](#to-run)
- [Story Format](#story-format)
- [Technical Highlights](#technical-highlights)
- [Assets](#assets)
- [Status](#status)

## Features

- **Custom `.docx` story format** — chapters, nodes, choices, and branching written in plain
  keyword syntax (`CHAPTER:`, `NODE:`, `CHOICE:`, `NEXT:`, `NEXT_CHAPTER:`) inside a Word
  document, parsed into a nested chapter/node graph at runtime.
- **Branching & reconverging paths** — choices can lead to distinct nodes or converge back
  into a shared node, with auto-continue (`NEXT:`) nodes for non-choices.
- **Save & load** — Checkpoints with save/overwrite confirmation.
- **Full 24-bit color terminal images** — images render as true-RGB ASCII art. The art is sized
  to fit the player's terminal window. See [Technical Highlights](#technical-highlights)
  for how this actually works.

## To Run

```
pip install -r requirements.txt
python CYOA_Logic.py
```

Story content lives in `The_Sun.docx`. Images referenced by `IMAGE:` lines are not
included in this repo (see [Assets](#assets) below), so the game will run and display all
text/choices correctly, but will show a placeholder message where images would normally
appear.

## Story format

Stories are plain `.docx` files using a small keyword syntax:

```
CHAPTER: 1
TITLE: The Sun
START: Basement

NODE: Basement
NARRATOR: Es looks up and can't tell if she actually is.
CHOICE: Think -> Thoughts
CHOICE: Switch on the lights -> Basement_Lit

NODE: Basement_Lit
IMAGE: dist/images/Sun.png
NARRATOR: Es pulls the string and a stream of light floods through the open space.
NEXT_CHAPTER: 2
```
- `CHAPTER:` / `TITLE:` / `START:` open a chapter and name its first node. `START:` must
  always come after `CHAPTER:`, never before.
- `NODE:` marks a position change. It is required at the start of every chapter and at any
  choice that moves the player somewhere new.
- `CHOICE: label -> target` gives the player a decision; `NEXT: target` continues
  automatically with no choice required. A choice's target can be any node defined in the
  same chapter, including the node the player is already in (e.g. `CHOICE: Stay -> Forest`
  from inside `NODE: Forest` is valid, and simply re-plays that node).
- `NEXT_CHAPTER: n` signals where to go next. The destination chapter still needs its own
  `CHAPTER:` header to actually exist.
- `IMAGE: path` displays an image that persists on screen until the next `IMAGE:` line.
- Any other `SPEAKER: line` becomes a line of dialogue, printed in order.

## Technical Highlights

**Full-color terminal rendering**

Terminal ASCII art from this library renders in fewer colors than its browser output, because
[`ascii_magic`](https://github.com/LeandroBarone/python-ascii_magic) library's
terminal API (`to_terminal()`) takes every character's color to its nearest match in
an ANSI 8-color palette (`constants.py`). 

The source code showed that it actually computes full RGB color
for every character internally using (`full_hex_color`). But this was only for HTML export mode, and
never for the terminal. This engine bypasses `to_terminal()` and instead calls `_img_to_art()`
with `modes=Modes.OBJECT`, which returns each cell's `full-hex-color` in the raw per-character grid.
Next, the library's own color-snapping step runs. That data is then handed
to `rich.text.Text` for rendering. 

This gives 24-bit color output in the terminal using
the exact same character mapping `ascii_magic` produces, with none of the color loss.

![Terminal gameplay showing colored ASCII rendering](EXAMPLES/EXAMPLE%20the_sun_is_dry_SSTerminal.png)

![Terminal gameplay showing colored ASCII rendering](EXAMPLES/EXAMPLE%20the_sun_is_dry_SSTerminal_2.png)


Image sizing is computed by the renderer, which reads the
current size of the terminal (`shutil.get_terminal_size()`) and the source image's aspect
ratio. This means tall images never scroll out of view. 

## Assets

Image files referenced by `IMAGE:` lines in `The_Sun.docx` are not included in this repo.
The engine handles missing images by printing a message instead and will continue to run
normally. 

## Status

This is a work in progress, built for learning Python and
terminal rendering. The story ends after a few passes. Additional chapters and assets are staged for the future

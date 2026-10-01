from rich import print
from rich.console import Console
from ascii_magic import AsciiArt
from docx import Document
from json_parser import parse_story
import questionary, time, logging, sys, json, os
from truecolor_ascii import render_truecolor_ascii



console = Console()
logger = logging.getLogger(__name__)


document = Document("The_Sun.docx")
lines = [p.text.replace("\xa0", " ").strip() for p in document.paragraphs if p.text.strip()]
SAVE_FILE = "save.json"


def seperateWithBorder(): #a border that wraps around text when called
  border = console.print(f"[sky_blue1]==========[/sky_blue1]")
  time.sleep(1)
  return border


def save_exists():
  return os.path.exists(SAVE_FILE)


def write_save(chapter_id, node_id, flags_set):
  data = {"chapter": chapter_id, "node": node_id, "flags": list(flags_set)}
  with open(SAVE_FILE, "w") as f:
    json.dump(data, f)


def read_save():
  with open(SAVE_FILE, "r") as f:
    return json.load(f)


def loadTitleScreen():
  print("The Sun is Dry")
  while True:
    user_title_screen_choice = questionary.select("", choices=["New game", "Load", "End"]).ask()

    if user_title_screen_choice == "New game":
      print("starting new game...")
      time.sleep(2.5)
      gameLoop()

    elif(user_title_screen_choice == "Load"): #check for save file. save should stay regardless if game closed
      print("Loading game...")
      time.sleep(2.5)
      if save_exists():
        print("Loading save file")
        save_data = read_save()
        gameLoop(
          start_chapter=str(save_data["chapter"]),
          start_node=save_data["node"],
          flags_set=set(save_data.get("flags", []))
        )
      else:
        print("No previous save")


    elif(user_title_screen_choice == "End"):
      print("Closing...")
      sys.exit()
      return


def saveGame(current_chapter_id, current_node_id, flags_set):
  save_file = save_exists()

  save_game = questionary.confirm("Would you like to save?").ask()
  if save_game and save_file: #if they want to save, and save exists
    overwrite_save = questionary.select("There is already a save in the slot. Would you still like to overwrite" \
    " the save?", choices=["Overwrite", "Do not overwrite"]
    ).ask()
    #final confirmation
    if overwrite_save == "Overwrite":
      final_overwrite_confirm = questionary.confirm("Overwrite save?").ask()
      if final_overwrite_confirm:
        write_save(current_chapter_id, current_node_id, flags_set)
        console.print("[chartreuse1]Save overwritten. Success![/chartreuse1]")
        return True
      else:
        console.print("returning debug case")
        return False
    else:
      return False
  elif save_game and not save_file:
    write_save(current_chapter_id, current_node_id, flags_set)
    console.print("[chartreuse1]Game saved successfuly![/chartreuse1]")
    return True
  else:
    console.print("Returning...")
    return False


def resolve_branches(node, flags_set):
  """Given a node with a 'branches' list, return the target of the first
  BRANCH_IF_FLAG whose flag is in flags_set, or the BRANCH_ELSE target
  (flag=None) if none matched. Returns None if there are no branches."""
  fallback = None
  for branch in node.get("branches", []):
    if branch["flag"] is None:
      fallback = branch["target"]
    elif branch["flag"] in flags_set:
      return branch["target"]
  return fallback


def gameLoop(start_chapter="1", start_node=None, flags_set=None):
  story = parse_story(lines)
  current_chapter_id = start_chapter
  flags_set = flags_set if flags_set is not None else set()

  first_pass = True
  while True:
    chapter = story[current_chapter_id]
    if first_pass and start_node:
      current_node_id = start_node
    else:
      current_node_id = chapter["start_node"]
    first_pass = False


    seperateWithBorder()
    console.print(f"Chapter {current_chapter_id} - {chapter["title"]}")
    seperateWithBorder()

    while True:
      node = chapter["nodes"][current_node_id]

      # A node made purely of BRANCH_IF_FLAG/BRANCH_ELSE lines routes
      # immediately to another node based on flags_set, with no dialogue
      # or choices of its own.
      if node.get("branches"):
        current_node_id = resolve_branches(node, flags_set)
        continue

      current_image = None

      for entry in node["dialogue"]:
          if entry.get("type") == "image":
            current_image = entry["path"]
            continue

          console.clear()
          if current_image:
              try:
                  art = render_truecolor_ascii(current_image, max_columns=100)
                  print(art)
              except Exception as e:
                  console.print(f"[red]Could not load image: {current_image} ({e})[/red]")

          if entry["speaker"] == "NARRATOR":
              console.print(entry["line"])
          else:
              console.print(f"[bold]{entry['speaker']}:[/bold] {entry['line']}")
          input("(>)")

      if "next" in node:
        seperateWithBorder()
        current_node_id = node["next"]


      elif "next_chapter" in node:
        current_chapter_id = node["next_chapter"]
        break

      elif node["choices"]:
        choice = questionary.select("",
            choices=list(node["choices"].keys()) + ["Save and quit"]
        ).ask()

        if choice == "Save and quit":
          quit_confirmed = saveGame(current_chapter_id, current_node_id, flags_set)
          if quit_confirmed:
            return
          seperateWithBorder()
          continue

        chosen = node["choices"][choice]
        if chosen["sets_flag"]:
          flags_set.add(chosen["sets_flag"])

        seperateWithBorder()
        current_node_id = chosen["target"]

      else:
        console.print("[sky_blue1]--- END ---[/sky_blue1]")
        return


loadTitleScreen()
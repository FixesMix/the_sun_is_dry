from rich import print
from rich.console import Console
from ascii_magic import AsciiArt, from_image, Back
from PIL import ImageEnhance
from docx import Document
from json_parser import parse_story
import questionary, time, logging, sys


console = Console()
logger = logging.getLogger(__name__)


document = Document("The_Sun.docx")
lines = [p.text.replace("\xa0", " ").strip() for p in document.paragraphs if p.text.strip()]


def seperateWithBorder(): #a border that wraps around text when called
  border = console.print(f"[sky_blue1]==========[/sky_blue1]")
  time.sleep(1)
  return border

def loadTitleScreen():
  print("Our New (Every)day")
  while True:
    user_title_screen_choice = questionary.select("", choices=["New game", "Load", "End"]).ask()

    if user_title_screen_choice == "New game":
      print("starting new game...")
      time.sleep(2.5)
      gameLoop()

    elif(user_title_screen_choice == "Load"): #check for save file. save should stay regardless if game closed
      print("Loading game...")
      time.sleep(2.5)
      if(#the_hypothetical_save_file is True
        ):
        print("Loading save file")
      else:
        print("No previous save")
      

    elif(user_title_screen_choice == "End"):
      print("Closing...")
      sys.exit()
      return
  

def saveGame():#this is all working. need to get actual save file to check
  save_file = True

  save_game = questionary.confirm("Would you like to save?").ask()
  if save_game and save_file: #if they want to save, and save exists
    overwrite_save = questionary.select("There is already a save in the slot. Would you still like to overwrite" \
    " the save?", choices=["Overwrite", "Do not overwrite"]
    ).ask() 
    #final confirmation
    if overwrite_save == "Overwrite":
      final_overwrite_confirm = questionary.confirm("Overwrite save?").ask()
      if final_overwrite_confirm :
        console.print("[chartreuse1]Save overwritten. Success![/chartreuse1]")
        return
      else: 
        console.print("returning debug case")
        return
    else:
      return
  elif save_game and not save_file:
    console.print("[chartreuse1]Game saved successfuly![/chartreuse1]")
  else:
    console.print("Returning...")
    return
  

def gameLoop():
  story = parse_story(lines) 
  current_chapter_id = "1"         

  while True:
    chapter = story[current_chapter_id]
    current_node_id = chapter["start_node"]
    
    
    seperateWithBorder()
    console.print(f"Chapter {current_chapter_id} - {chapter["title"]}")  
    seperateWithBorder()
    
    while True:
      node = chapter["nodes"][current_node_id]

      for entry in node["dialogue"]:
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
            choices=list(node["choices"].keys())
        ).ask()
        seperateWithBorder()
        current_node_id = node["choices"][choice]

      else:
        console.print("[sky_blue1]--- END ---[/sky_blue1]")
        return

  # if userChoice.saveGame == "Yes":
  #   #check for save file   
  #   if saveFile is not None:
  #     userChoice.overwriteSave.ask()
  #   else:
  #     print("No save found. Saving game...")
  #     time.sleep(2)
  # else:
  #   return
  
  # if userChoice.overwriteSave == "Overwrite":
  #   print("Overwriting save...")
  #   time.sleep(2)
  # else:
    # print(userChoice)
  
  #save file in variable. if variable is taken, ask if wants to 
  #be overwritten. if so, overwrite variable at pos x. Else return.


loadTitleScreen()

result = parse_story(lines)
print(result)

# chapter = "1. The [yellow]Sun[/yellow]"
# seperateWithBorder(chapter)


# console.print("**Our New (Every)day**\n\n\nNew game \tLoad \tEnd")

# loadTitleScreen()

# try:
#   displayed_art = from_image(f"dist/images/the_sun.jpg")
#   displayed_art.to_terminal(columns=200)
#   input("Press Enter to exit...")

# except Exception as e:
#   print(f"Unexpected error: {e}")
#   input("Press Enter to exit...")

# AsciiArt.print_palette()
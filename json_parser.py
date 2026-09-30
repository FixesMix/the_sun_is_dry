from docx import Document

def parse_story(lines):
    chapters = {}
    current_chapter_id = None
    current_node_id = None

    for line in lines:
        if line.startswith("CHAPTER:"): #Signals the start of a chapter
            current_chapter_id = line.replace("CHAPTER:", "").strip()
            chapters[current_chapter_id] = {"nodes": {}} 

        elif line.startswith("TITLE:"):
            chapters[current_chapter_id]["title"] = line.replace("TITLE:", "").strip()

        elif line.startswith("START:"):
            chapters[current_chapter_id]["start_node"] = line.replace("START:", "").strip()

        elif line.startswith("NODE:"): #Position change
            current_node_id = line.replace("NODE:", "").strip()
            chapters[current_chapter_id]["nodes"][current_node_id] = {"dialogue": [], "choices": {}}

        elif line.startswith("CHOICE:"): #Prompt
            choice_part = line.replace("CHOICE:", "").strip()
            label, target = choice_part.split("->")
            chapters[current_chapter_id]["nodes"][current_node_id]["choices"][label.strip()] = target.strip()

        elif line.startswith("NEXT:"): #Continue without giving a choice
          chapters[current_chapter_id]["nodes"][current_node_id]["next"] = line.replace("NEXT:", "").strip()

        elif line.startswith("SETS_FLAG:"): #A choice to be remembered
            chapters[current_chapter_id]["nodes"][current_node_id]["sets_flag"] = line.replace("SETS_FLAG:", "").strip()

        elif line.startswith("NEXT_CHAPTER:"): #Signals the end of a chapter
            chapters[current_chapter_id]["nodes"][current_node_id]["next_chapter"] = line.replace("NEXT_CHAPTER:", "").strip()
        
        elif line.startswith("IMAGE:"): #An image to be displayed
            image_path = line.replace("IMAGE:", "").strip()
            chapters[current_chapter_id]["nodes"][current_node_id]["dialogue"].append({
                "type": "image",
                "path": image_path
            })
            
        elif ":" in line: #A speaking character
            speaker, spoken_line = line.split(":", 1)
            chapters[current_chapter_id]["nodes"][current_node_id]["dialogue"].append({
                "speaker": speaker.strip(),
                "line": spoken_line.strip()
            })

    return chapters


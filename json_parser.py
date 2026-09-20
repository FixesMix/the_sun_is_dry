from docx import Document

def parse_story_docx(path):
    doc = Document(path)
    lines = [paragraph.text.strip() for paragraph in doc.paragraphs if paragraph.text.strip()]

    chapters = {}
    current_chapter_id = None
    current_node_id = None

    for line in lines:
        if line.startswith("CHAPTER:"):
            current_chapter_id = line.replace("CHAPTER:", "").strip()
            chapters[current_chapter_id] = {"nodes": {}}

        elif line.startswith("NODE:"):
            current_node_id = line.replace("NODE:", "").strip()
            chapters[current_chapter_id]["nodes"][current_node_id] = {"dialogue": [], "choices": {}}

        elif line.startswith("CHOICE:"):
            choice_part = line.replace("CHOICE:", "").strip()
            label, target = choice_part.split("->")
            chapters[current_chapter_id]["nodes"][current_node_id]["choices"][label.strip()] = target.strip()

        elif line.startswith("SETS_FLAG:"):
            chapters[current_chapter_id]["nodes"][current_node_id]["sets_flag"] = line.replace("SETS_FLAG:", "").strip()

        elif line.startswith("NEXT_CHAPTER:"):
            chapters[current_chapter_id]["nodes"][current_node_id]["next_chapter"] = line.replace("NEXT_CHAPTER:", "").strip()
        
        elif ":" in line:
            speaker, spoken_line = line.split(":", 1)
            chapters[current_chapter_id]["nodes"][current_node_id]["dialogue"].append({
                "speaker": speaker.strip(),
                "line": spoken_line.strip()
            })

    return chapters
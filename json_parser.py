from docx import Document

def get_lines_from_docx(path):
  doc = Document(path)
  lines = []

  for paragraph in doc.paragraphs:
    text = paragraph.text.strip()
    if text:
      lines.append(text)

  return lines


def remove_empty(input):
  word_list = []

  for word in input:
    pure_text = word.strip()
    if pure_text:
      word_list.append(pure_text)
  return word_list

line = "START: The Meadow"

if line.startswith("TITLE:"):
  new_phrase = line.replace("TITLE:", "").strip()
  print(new_phrase)
elif line.startswith("START:"):
  new_phrase = line.replace("START:", "").strip()
  print(new_phrase)
elif line.startswith("CHAPTER:"):
  new_phrase = line.replace("CHAPTER:", "").strip()
  print(new_phrase)
else: 
  print("Does not start with keyword.")

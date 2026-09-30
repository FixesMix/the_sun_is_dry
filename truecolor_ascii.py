import shutil
from PIL import Image
from ascii_magic import AsciiArt
from ascii_magic.constants import Modes
from rich.text import Text


def render_truecolor_ascii(image_path, max_columns=140, width_ratio=2.2, height_fraction=0.75):
    """Renders an image as ASCII art using full 24-bit RGB terminal color,
    sized so the image's height fits within a safe fraction of the current
    terminal window, instead of always using a fixed column count that can
    produce an image taller than the visible terminal."""

    terminal_size = shutil.get_terminal_size()
    max_lines_for_image = int(terminal_size.lines * height_fraction)

    img = Image.open(image_path)
    aspect_ratio = img.height / img.width


    columns_for_height = int(max_lines_for_image / aspect_ratio * width_ratio)

    columns = min(max_columns, columns_for_height, terminal_size.columns)
    columns = max(columns, 10)  # keep a  floor so smallerterminals don't crash the render

    art = AsciiArt.from_image(image_path)
    grid = art._img_to_art(columns=columns, width_ratio=width_ratio, mode=Modes.OBJECT)

    text = Text()
    for row in grid:
        for cell in row:
            text.append(cell.character, style=cell.full_hex_color)
        text.append("\n")

    return text
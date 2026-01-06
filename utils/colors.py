import json
from pathlib import Path


# load json into variable
def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

# create variables for main, secondry, and text color  
def get_school_colors(school):
    return {
        "primary": load_json("data/colors/school_colors.json").get(school, "#000000"),
        "secondary": load_json("data/colors/secondary_school_colors.json").get(school, "#CCCCCC"),
        "secondary_text": load_json("data/colors/secondary_text_colors.json").get(school, "#000000")
    }


# helper function to create rgb value out of hex
def hex_to_rgb(hex_color):
    # Remove the '#' character if present
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]

    # Ensure the hex string is the correct length (6 characters)
    if len(hex_color) != 6:
        raise ValueError("Invalid hex color code length")

    # Use int() with base 16 for conversion
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return (r, g, b)


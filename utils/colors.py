import json
from pathlib import Path

def load_colors(path):
    with open(path, "r") as f:
        return json.load(f)
    
def get_school_colors(school):
    return {
        "primary": load_colors("data/school_colors.json").get(school, "#000000"),
        "secondary": load_colors("data/secondary_school_colors.json").get(school, "#CCCCCC")
    }


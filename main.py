# IMPORTS
import os
import json
from knife_point_horror import Story

# Create story objects
stories = []
synopses_dir = "./Synopses"
synopses = [f for f in os.listdir(f"{synopses_dir}") if f[0] != "_"]
for synopsis in synopses:
    stories.append(Story(synopsis_filename=f"{synopses_dir}/{synopsis}"))

# Do cool stuff
for story in stories:
    for character in story.synopsis["characters"]:

        # Create a character sheet if none exists
        character_sheet_filename = character.lower().replace(" ", "_")
        cs_default_data = {
            "name": character,
            "age": None,
            "summary": None,
            "mentions": []
        }
        cs_file_dir = os.path.join("Character_Sheets", character_sheet_filename + ".json")
        if not os.path.isfile(cs_file_dir):
            with open(cs_file_dir, "w") as cs_file:
                json.dump(cs_default_data, cs_file, indent=4)

        with open(cs_file_dir, "r+") as cs_file:
            cs_data = json.load(cs_file)
            cs_data["mentions"].append(story.synopsis["title"])
            cs_file.seek(0)
            json.dump(cs_data, cs_file, indent=4)
            cs_file.truncate()

pass

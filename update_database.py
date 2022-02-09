# IMPORTS
import json

# Decode data from master JSON file
with open("stories.json", "r") as stories_file:
    stories = json.load(stories_file)

# Decode data from master JSON characters file
with open("characters.json", "r") as characters_file:
    characters = json.load(characters_file)

# Build/update character sheets
for story in stories:

    # Add narrator to characters list if not already there
    if story["narrator"] not in story["characters"] and story["narrator"] != "":
        story["characters"].append(story["narrator"])

    # Create character entry if none exists
    logged_characters = [char["name"] for char in characters]
    for story_character in story["characters"]:
        if story_character not in logged_characters:
            new_character_info = {"name": story_character, "age": 0, "summary": "", "mentions": [story["title"]]}
            characters.append(new_character_info)

    # Update story mentions for each character
    for character in characters:
        if character["name"] in story["characters"] and story["title"] not in character["mentions"]:
            character["mentions"].append(story["title"])
        elif character["name"] not in story["characters"] and story["title"] in character["mentions"]:
            character["mentions"].remove(story["title"])

# Encode data to master JSON stories file
with open("stories.json", "w") as stories_file:
    json.dump(stories, stories_file, indent=4)

# Encode data to master JSON characters file
with open("characters.json", "w") as characters_file:
    json.dump(characters, characters_file, indent=4)

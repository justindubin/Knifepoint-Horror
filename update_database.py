# IMPORTS
import json


# MAIN
def main():

    # Decode story data from master JSON file
    with open("stories.json", "r") as stories_file:
        stories = json.load(stories_file)

    # Decode character data from master JSON file
    with open("characters.json", "r") as characters_file:
        characters = json.load(characters_file)

    # Build/update character sheets
    for story in stories:

        # Add narrator to characters list if not already there
        if story["narrator"] not in story["characters"] and story["narrator"] != "":
            story["characters"].append(story["narrator"])

        # Remove duplicate characters in stories file
        story["characters"] = list(set([char.lower() for char in story["characters"]]))

        # Alphabetize characters and themes in story data sheet
        story["characters"].sort()
        story["themes"].sort()

        # Create character entry if none exists
        logged_characters = [char["name"].lower() for char in characters]
        for story_character in story["characters"]:
            if story_character.lower() not in logged_characters:
                new_character_info = {
                    "name": story_character.lower(),
                    "age": "unknown",
                    "description": "",
                    "mentions": [story["title"]]
                }
                characters.append(new_character_info)

        # Update story mentions for each character
        for character in characters:

            if character["name"] in story["characters"] and story["title"] not in character["mentions"]:
                character["mentions"].append(story["title"])
            elif character["name"] not in story["characters"] and story["title"] in character["mentions"]:
                character["mentions"].remove(story["title"])

        # Alphabetize character entries in character data sheet
        characters = sorted(characters, key=lambda d: d["name"])

    # Encode story data to master JSON file
    with open("stories.json", "w") as stories_file:
        json.dump(stories, stories_file, indent=4)

    # Encode character data to master JSON file
    with open("characters.json", "w") as characters_file:
        json.dump(characters, characters_file, indent=4)


# ENTRY POINT
if __name__ == '__main__':
    main()

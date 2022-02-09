# IMPORTS
import sys
import json


# FUNCTIONS
def load_dump_json(filename: str, action: str, dump_data=None, indent=2):
    if action.lower() == "load":
        with open(filename, "r") as file_obj:
            data_out = json.load(file_obj)
            return data_out
    elif action.lower() == "dump":
        with open(filename, "w") as file_obj:
            json.dump(dump_data, file_obj, indent=indent)
    else:
        raise NameError(f"Unable to handle JSON load/dump request!"
                        f"\nUser-input '{action}' is not an accepted action input argument."
                        f"\nPlease ensure 'action' is set to either 'load' or 'dump'.")


# MAIN
def main():

    # Decode JSON data
    stories = load_dump_json(filename="stories.json", action="load")
    characters = load_dump_json(filename="characters.json", action="load")

    # Build/update character sheets
    all_story_characters = []
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
            all_story_characters.append(story_character)
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

    # Remove character objects not present in any story object
    characters = [c for c in characters if c["name"] in all_story_characters]

    # Encode JSON data
    load_dump_json(filename="stories.json", action="dump", dump_data=stories, indent=4)
    load_dump_json(filename="characters.json", action="dump", dump_data=characters, indent=4)


# ENTRY POINT
if __name__ == '__main__':
    main()

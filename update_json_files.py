# IMPORTS
import os
import copy
import json


# FUNCTIONS
def load_dump_json(filename: str, action: str, dump_data=None, indent=2):

    # Create file if none exists
    if not os.path.isfile(filename):
        print(f"\nNo file '{filename}' exists\n > Creating empty JSON array...")
        with open(filename, "w") as file_obj:
            json.dump([], file_obj, indent=indent)

    # Dynamically load/dump data
    if action.lower() == "load":
        with open(filename, "r") as file_obj:
            data_out = json.load(file_obj)
            return data_out
    elif action.lower() == "dump":
        with open(filename, "w") as file_obj:
            json.dump(dump_data, file_obj, indent=indent)
    else:
        # Throw name error if user enters invalid action
        raise NameError(f"Invalid input: '{action}'. Ensure action = 'load' or 'dump'.")


def conform_naming(name: str):
    compatible_name = name.lower().replace(" ", "_").replace(".", "").replace("'", "")
    return compatible_name


# MAIN
def main():

    # Decode JSON data
    stories = load_dump_json(filename="stories.json", action="load")
    characters = load_dump_json(filename="characters.json", action="load")
    print("\nJSON data loaded into memory...")

    # Build/update character sheets
    all_story_characters = []
    for story in stories:

        # Add narrator to characters list if not already there
        if story["narrator"] not in story["characters"] and story["narrator"] != "":
            story["characters"].append(story["narrator"])

        # Remove duplicate characters and themes in stories file
        story["characters"] = list(set([char for char in story["characters"]]))
        story["themes"] = list(set([theme.lower() for theme in story["themes"]]))

        # Alphabetize characters and themes in story data sheet
        story["characters"].sort()
        story["themes"].sort()

        # Check character information
        logged_characters = [char["name"].lower() for char in characters]
        character_descriptions = []
        near_duplicates = []
        for story_character in story["characters"]:
            all_story_characters.append(story_character)

            # Check for near-duplicates
            check_bin = copy.copy(story["characters"])
            check_bin.remove(story_character)
            check_bin = [c.lower() for c in check_bin]
            if story_character.lower() in check_bin:
                near_duplicates.append(story_character)

            # Create character entry if none exists
            if story_character.lower() not in logged_characters:
                new_character = {
                    "name": story_character,
                    "age": "unknown",
                    "description": "",
                    "mentions": [story["title"]]
                }
                characters.append(new_character)

            # Create a new character description file if none exists
            char_fname = conform_naming(story_character)
            char_desc_dir = f"char_desc/{char_fname}.txt"
            if not os.path.isfile(char_desc_dir):
                default_text = f"Replace this text with a description of {story_character}"
                with open(char_desc_dir, "w") as char_desc:
                    char_desc.write(default_text)

            # Add description from char_desc file
            with open(char_desc_dir, "r") as char_desc:
                character_descriptions.append((story_character, char_desc.read()))

        # Alert near-duplicates
        if len(near_duplicates) > 0:
            desc_string = "The following characters are listed more than once in their story object:"
            title_string = "! NEAR-DUPLICATE(S) DETECTED !"
            print()
            print("-" * len(desc_string))
            print(title_string.center(len(desc_string)))
            print("-" * len(desc_string))
            print(desc_string)
            for near_duplicate in near_duplicates:
                print(f"  + {near_duplicate}")

        # Update character information
        for character in characters:
            if len(character_descriptions) > 0:
                for char_name, char_desc in character_descriptions:
                    if char_name == character["name"]:
                        character["description"] = char_desc
                        continue
            if character["name"] in story["characters"] and story["title"] not in character["mentions"]:
                character["mentions"].append(story["title"])
            elif character["name"] not in story["characters"] and story["title"] in character["mentions"]:
                character["mentions"].remove(story["title"])

        # Alphabetize character entries in character data sheet  ToDo: Also by episode number (link to title)
        characters = sorted(characters, key=lambda d: d["name"])

    # Alert character objects not present in any story object
    unmentioned_characters = [c["name"] for c in characters if c["name"] not in all_story_characters]
    if len(unmentioned_characters) > 0:
        desc_string = "The following characters don't belong to any story object:"
        title_string = "! UNMENTIONED CHARACTER(S) DETECTED !"
        print()
        print("-"*len(desc_string))
        print(title_string.center(len(desc_string)))
        print("-"*len(desc_string))
        print(desc_string)
        for unmentioned_character in unmentioned_characters:
            print(f"  + {unmentioned_character}")
        delete_extras = input("\nDelete unmentioned characters? (y/n): ")
        if delete_extras.lower() == "y":
            characters = [c for c in characters if c["name"] not in unmentioned_characters]
            print(" --- Deleted all unmentioned characters")
        else:
            print(" --- No characters deleted")

    # Encode JSON data
    load_dump_json(filename="stories.json", action="dump", dump_data=stories, indent=4)
    load_dump_json(filename="characters.json", action="dump", dump_data=characters, indent=4)

    print("\nJSON data files updated successfully...")


# ENTRY POINT
if __name__ == '__main__':
    main()

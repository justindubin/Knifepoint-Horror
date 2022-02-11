# IMPORTS
import os
import copy
import json


# FUNCTIONS
def load_dump_json(filename: str, action: str, dump_data=None, indent=2):

    # Create file if none exists
    if not os.path.isfile(filename) and action == "load":
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


def throw_alert(title_string, info_string):
    print()
    print("-" * len(info_string))
    print(title_string.center(len(info_string)))
    print("-" * len(info_string))
    print(info_string)


# MAIN
def main():

    # Welcome message
    print("\n--- RUNNING THE KPH JSON FILE UPDATE SCRIPT ---")

    # Decode JSON data
    stories = load_dump_json(filename="stories.json", action="load")
    characters = load_dump_json(filename="characters.json", action="load")
    print("\n > JSON data loaded into memory")

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
        character_datapack = []
        near_duplicates = []
        for story_character in story["characters"]:
            all_story_characters.append(story_character)

            # Check for near-duplicates
            check_bin = copy.copy(story["characters"])
            check_bin.remove(story_character)
            check_bin = [c.lower() for c in check_bin]
            if story_character.lower() in check_bin:
                near_duplicates.append(story_character)

            # Create character object if none exists
            if story_character.lower() not in logged_characters:
                new_character = {
                    "name": story_character,
                    "age": "unknown",
                    "description": "",
                    "mentions": [story["title"]]
                }
                characters.append(new_character)

            # Create a new character description text file if none exists
            char_filename = conform_naming(story_character)
            char_file_dir = f"char_desc/{char_filename}.txt"
            if not os.path.isfile(char_file_dir):
                default_text = f"Replace this text with a description of {story_character}"
                with open(char_file_dir, "w") as char_file:
                    char_file.write(default_text)

            # Read descriptions from char_desc files
            with open(char_file_dir, "r") as char_file:
                character_datapack.append((story_character, char_file.read(), char_file_dir))

        # Alert for near-duplicates
        if len(near_duplicates) > 0:
            title_string = "! NEAR-DUPLICATE(S) DETECTED !"
            info_string = "The following characters are listed more than once in their story object:"
            throw_alert(title_string=title_string, info_string=info_string)
            for near_duplicate in near_duplicates:
                print(f"  + {near_duplicate}")

        # Update character information
        for character in characters:

            # Character descriptions
            if len(character_datapack) > 0:
                for char_name, char_file_desc, char_file_dir in character_datapack:
                    if char_name == character["name"]:
                        if character["description"].split(" ")[0] == "Replace" or character["description"] == "":
                            # Safe to overwrite JSON file
                            character["description"] = char_file_desc
                        elif char_file_desc.split(" ")[0] == "Replace" or char_file_desc == "":
                            # Safe to overwrite TXT file
                            with open(char_file_dir, "w") as char_file:
                                char_file.write(character["description"])
                        elif character["description"] != char_file_desc:
                            # Warn of potential data loss
                            title_string = "! DATA LOSS WARNING !"
                            info_string = "Description clash detected between JSON and TXT files"
                            throw_alert(title_string=title_string, info_string=info_string)
                            json_text = character["description"]
                            txt_text = char_file_desc
                            print(f"\nCHARACTER: {character['name']}\nMENTIONS: {', '.join(character['mentions'])}")
                            print("~"*40)
                            print(f"JSON description: '{json_text}'")
                            print(f"TXT description: '{txt_text}'")
                            overwrite = input("\nWhich description is correct? (json/txt): ")
                            if overwrite.lower() == "json":
                                with open(char_file_dir, "w") as char_file:
                                    char_file.write(json_text)
                                print(f" --- {char_file_dir} updated")
                            elif overwrite.lower() == "txt":
                                character["description"] = txt_text
                                print(f" --- JSON object updated")
                            else:
                                print(f" --- No changes made")
                        else:
                            # No need for update
                            pass
                        continue

            # Story mentions
            if character["name"] in story["characters"] and story["title"] not in character["mentions"]:
                character["mentions"].append(story["title"])
            elif character["name"] not in story["characters"] and story["title"] in character["mentions"]:
                character["mentions"].remove(story["title"])

        # Alphabetize character entries in character data sheet
        characters = sorted(characters, key=lambda d: d["name"])

    # Alert for character objects not present in any story object
    unmentioned_characters = [c["name"] for c in characters if c["name"] not in all_story_characters]
    if len(unmentioned_characters) > 0:
        title_string = "! UNMENTIONED CHARACTER(S) DETECTED !"
        info_string = "The following characters don't belong to any story object:"
        throw_alert(title_string=title_string, info_string=info_string)
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

    print("\n > JSON data files updated successfully")


# ENTRY POINT
if __name__ == '__main__':
    main()

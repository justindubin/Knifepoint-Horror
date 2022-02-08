# CLASSES
class KnifePointHorror:
    def __init__(self):
        self.author = "Soren Narnia"


class Story(KnifePointHorror):
    def __init__(self, synopsis_filename):
        super().__init__()
        self.synopsis_filename = synopsis_filename
        self.title = None
        self.episode_number = None
        self.release_date = None
        self.length = None
        self.read_by = None
        self.description = None
        self.narrator = None
        self.story_date = None
        self.location = None
        self.characters = None
        self.themes = None
        self.parse_synopsis(self.synopsis_filename)

    def parse_synopsis(self, filename):
        with open(f"Synopses/{filename}", mode="r") as f:
            file_contents = [line.rstrip("\n") for line in f.readlines()]
            param_dict = {}
            split_key = " ~ "
            for item in file_contents:
                param = item.split(split_key)[0]
                value = item.split(split_key)[1]
                if param not in param_dict:
                    param_dict[param] = value
            self.title = param_dict["TITLE"]
            self.episode_number = int(param_dict["EPISODENUMBER"])
            self.release_date = param_dict["RELEASEDATE"]
            self.length = param_dict["LENGTH"]
            self.read_by = param_dict["READBY"].title()
            self.description = param_dict["DESCRIPTION"]
            self.narrator = param_dict["NARRATOR"].title()
            self.story_date = param_dict["STORYDATE"]  # ToDo: Mimic release_date?
            self.location = param_dict["LOCATION"]  # ToDo: Expand?
            self.characters = [char.strip().title() for char in param_dict["CHARACTERS"].split(",")]
            if self.narrator not in self.characters:
                self.characters.append(self.narrator)
            self.characters = set(self.characters)
            self.themes = [theme.lstrip().rstrip().lower() for theme in param_dict["THEMES"].split(",")]


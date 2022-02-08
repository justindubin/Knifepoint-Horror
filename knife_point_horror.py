import string
import json


class KnifePointHorror:
    def __init__(self):
        self.author = "Soren Narnia"


class Story(KnifePointHorror):
    def __init__(self, synopsis_filename):
        super().__init__()
        with open(synopsis_filename, "r") as synopsis_file:
            self.synopsis = json.load(synopsis_file)



class KnifePointHorror:
    def __init__(self):
        self.author = "Soren Narnia"


class Story(KnifePointHorror):
    def __init__(self, title, release_date, audio_length, read_by):
        super().__init__()

        # Meta Data
        self.title = title
        self.release_date = release_date
        self.audio_length = audio_length
        self.read_by = read_by


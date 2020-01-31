# class for snacks

class Snack():
    track_id = 1

    def __init__(self, name, kind):
        self.name = name
        self.kind = kind
        self.ID = Snack.track_id
        Snack.track_id += 1

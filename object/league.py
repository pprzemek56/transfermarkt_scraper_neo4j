class League:
    def __init__(self, name, nationality, is_top_5):
        self.name = name
        self.nationality = nationality
        self.is_top_5 = is_top_5

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def nationality(self):
        return self._nationality

    @nationality.setter
    def nationality(self, nationality):
        self._nationality = nationality

    @property
    def is_top_5(self):
        return self._is_top_5

    @is_top_5.setter
    def is_top_5(self, is_top_5):
        self._is_top_5 = is_top_5

class League:
    def __init__(self, name, nationality, url):
        self.name = name
        self.nationality = nationality
        self.url = url

    def __str__(self) -> str:
        return super().__str__()

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
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

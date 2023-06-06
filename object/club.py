class Club:
    def __init__(self, name, url):
        self.name = name
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
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

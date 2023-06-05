class Club:
    def __init__(self, name, league):
        self.name = name
        self.league = league

    def __str__(self) -> str:
        return super().__str__()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def league(self):
        return self._league

    @league.setter
    def league(self, league):
        self._league = league

class Player:
    def __init__(self, name, current_club, previous_clubs):
        self.name = name
        self.current_club = current_club
        self.previous_clubs = previous_clubs

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def current_club(self):
        return self._current_club

    @current_club.setter
    def current_club(self, current_club):
        self._current_club = current_club

    @property
    def previous_clubs(self):
        return self._previous_clubs

    @previous_clubs.setter
    def previous_clubs(self, previous_clubs):
        self._previous_clubs = previous_clubs

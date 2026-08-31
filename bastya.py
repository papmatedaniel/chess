from babu import Babu


class Bastya(Babu):
    """Tartalmazza a bástya tulajdonságait, metódusait."""

    def __init__(self, szin, nev, jelenlegi_koordinata, el_e):
        super().__init__(szin, nev, jelenlegi_koordinata, el_e)


    def lepes(self):
        """Hagyományos mozgása a lónak."""
        return self.ortogonalis_lepes()

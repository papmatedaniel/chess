from babu import Babu


class Futo(Babu):
    """Tartalmazza a futó tulajdonságait, metódusait."""

    def __init__(self, szin, nev, jelenlegi_koordinata, el_e):
        super().__init__(szin, nev, jelenlegi_koordinata, el_e)


    def lepes(self):
        """Hagyományos mozgása a futónak."""
        return self.diagonalis_lepes()

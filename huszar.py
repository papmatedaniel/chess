from babu import Babu


class Huszar(Babu):
    """Tartalmazza a huszér tulajdonságait, metódusait."""

    def __init__(self, szin, nev, jelenlegi_koordinata, el_e):
        super().__init__(szin, nev, jelenlegi_koordinata, el_e)


    def lepes(self):
        """Hagyományos mozgása a lónak."""
        lepesek = [(1,2), (2,1), (-1, 2), (2, -1), (1, -2), (-2, 1), (-1,-2), (-2,-1)]
        return self.hozzad(lepesek)

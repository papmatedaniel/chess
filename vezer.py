from babu import Babu


class Vezer(Babu):
    """Tartalmazza a vezér tulajdonságait, metódusait."""

    def __init__(self, szin, nev, jelenlegi_koordinata, el_e):
        super().__init__(szin, nev, jelenlegi_koordinata, el_e)


    def lepes(self):
        """Hagyományos mozgása a vezérnek."""
        lepesek = []
        lepesek.extend(self.ortogonalis_lepes())
        lepesek.extend(self.diagonalis_lepes())
        return lepesek

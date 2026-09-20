from chess.babuk.babu import Babu
from chess.dataclassok.lepestipusok import Pozicio


class Kiraly(Babu):
    nev = "Király"

    def lepes(self) -> list[Pozicio]:
        """Hagyományos mozgása a királynak."""
        lepesek = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        return self.hozzad(lepesek)

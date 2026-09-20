from chess.babuk.babu import Babu
from chess.dataclassok.lepestipusok import Pozicio


class Futo(Babu):
    nev = "Futó"

    def lepes(self) -> list[list[Pozicio]]:
        """Hagyományos mozgása a futónak."""
        return self.diagonalis_lepes()

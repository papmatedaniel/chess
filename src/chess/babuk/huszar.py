from chess.babuk.babu import Babu
from chess.dataclassok.lepestipusok import Pozicio


class Huszar(Babu):
    nev = "Huszár"

    def lepes(self) -> list[Pozicio]:
        """Hagyományos mozgása a lónak."""
        return self.huszar_lepes()

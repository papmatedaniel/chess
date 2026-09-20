from chess.babuk.babu import Babu
from chess.dataclassok.lepestipusok import Pozicio


class Vezer(Babu):
    nev = "Vezér"

    def lepes(self) -> list[list[Pozicio]]:
        """Hagyományos mozgása a vezérnek."""
        lepesek = []
        lepesek.extend(self.ortogonalis_lepes())
        lepesek.extend(self.diagonalis_lepes())
        return lepesek

from filok.babuk.babu import Babu
from filok.dataclassok.lepestipusok import Pozicio


class Vezer(Babu):

    def __init__(self) -> None:
        super().__init__(nev="Vezér")

    def lepes(self) -> list[list[Pozicio]]:
        """Hagyományos mozgása a vezérnek."""
        lepesek = []
        lepesek.extend(self.ortogonalis_lepes())
        lepesek.extend(self.diagonalis_lepes())
        return lepesek

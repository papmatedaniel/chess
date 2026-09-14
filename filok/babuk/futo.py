from filok.babuk.babu import Babu
from filok.dataclassok.lepestipusok import Pozicio

class Futo(Babu):

    def __init__(self) -> None:
        super().__init__(nev="Futó")

    def lepes(self) -> list[list[Pozicio]]:
        """Hagyományos mozgása a futónak."""
        return self.diagonalis_lepes()

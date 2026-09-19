from filok.babuk.babu import Babu
from filok.dataclassok.lepestipusok import Pozicio


class Huszar(Babu):
    nev = "Huszár"

    def lepes(self) -> list[Pozicio]:
        """Hagyományos mozgása a lónak."""
        return self.huszar_lepes()

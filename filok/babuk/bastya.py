from filok.babuk.babu import Babu
from filok.dataclassok.lepestipusok import Pozicio


class Bastya(Babu):
    nev = "Bástya"

    def lepes(self) -> list[list[Pozicio]]:
        """Hagyományos ortogonális mozgása a bástyának."""
        return self.ortogonalis_lepes()

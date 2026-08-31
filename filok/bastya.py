from filok.babu import Babu


class Bastya(Babu):
    """Tartalmazza a bástya tulajdonságait, metódusait."""

    def __init__(self) -> None:
        super().__init__(nev="Bástya")


    def lepes(self) -> list[list[tuple[int, int]]]:
        """Hagyományos mozgása a lónak."""
        return self.ortogonalis_lepes()

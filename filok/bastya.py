from filok.babu import Babu


class Bastya(Babu):

    def __init__(self) -> None:
        super().__init__(nev="Bástya")

    def lepes(self) -> list[list[tuple[int, int]]]:
        """Hagyományos mozgása a lónak."""
        return self.ortogonalis_lepes()

from filok.babu import Babu


class Huszar(Babu):

    def __init__(self) -> None:
        super().__init__(nev="Huszár")

    def lepes(self) -> list[tuple[int, int]]:
        """Hagyományos mozgása a lónak."""
        return self.huszar_lepes()

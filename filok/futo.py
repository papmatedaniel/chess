from filok.babu import Babu


class Futo(Babu):

    def __init__(self) -> None:
        super().__init__(nev="Futó")

    def lepes(self) -> list[list[tuple[int, int]]]:
        """Hagyományos mozgása a futónak."""
        return self.diagonalis_lepes()

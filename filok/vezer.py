from filok.babu import Babu


class Vezer(Babu):

    def __init__(self) -> None:
        super().__init__(nev="Vezér")


    def lepes(self) -> list[list[tuple[int, int]]]:
        """Hagyományos mozgása a vezérnek."""
        lepesek = []
        lepesek.extend(self.ortogonalis_lepes())
        lepesek.extend(self.diagonalis_lepes())
        return lepesek

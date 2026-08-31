from babu import Babu


class Kiraly(Babu):

    def __init__(self) -> None:
        super().__init__(nev="Király")


    def lepes(self) -> list[tuple[int, int]]:
        """Hagyományos mozgása a királynak."""
        lepesek = [(1, 0), (0,1), (-1, 0), (0,-1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        return self.hozzad(lepesek)

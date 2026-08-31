from babu import Babu


class Huszar(Babu):

    def __init__(self) -> None:
        super().__init__(nev="Huszár")


    def lepes(self) -> list[tuple[int, int]]:
        """Hagyományos mozgása a lónak."""
        lepesek = [(1,2), (2,1), (-1, 2), (2, -1), (1, -2), (-2, 1), (-1,-2), (-2,-1)]
        return self.hozzad(lepesek)

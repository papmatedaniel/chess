from filok.babuk.babu import Babu
from filok.dataclassok.lepestipusok import Pozicio


class Gyalog(Babu):
    def __init__(self) -> None:
        super().__init__(nev="Gyalog")

    def utes(self) -> list[Pozicio]:
        """Hagyományos ütés"""
        lepesek = [
            (self.szinek[self.szin], self.szinek[self.szin]),
            (-self.szinek[self.szin], self.szinek[self.szin]),
        ]
        return self.hozzad(lepesek)

    def lepes(self) -> list[Pozicio]:
        """Hagyományos lépés"""
        lepesek = [(0, self.szinek[self.szin])]
        return self.hozzad(lepesek)

    def elso_lepes(self) -> list[Pozicio]:
        """Első lépés, ami lehet dupla is"""
        lepesek = [(0, self.szinek[self.szin]), (0, 2 * self.szinek[self.szin])]
        return self.hozzad(lepesek)

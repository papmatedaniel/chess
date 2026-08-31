from filok.babu import Babu


class Gyalog(Babu):
 
    def __init__(self) -> None:
        super().__init__(nev="Gyalog")


    def utes(self) -> list[tuple[int, int]]:
        """Hagyományos ütést"""
        lepesek = [(self.szinek[self.szin], self.szinek[self.szin]), (-self.szinek[self.szin], self.szinek[self.szin])]
        return self.hozzad(lepesek)

    def lepes(self) -> list[tuple[int, int]]:
        """Hagyományos lépés"""
        lepesek = [(0,  self.szinek[self.szin])]
        return self.hozzad(lepesek)

    def elso_lepes(self) -> list[tuple[int, int]]:
        """Első lépés, ami lehet dupla is"""
        lepesek = [(0,  self.szinek[self.szin]), (0, 2 * self.szinek[self.szin])]
        return self.hozzad(lepesek)


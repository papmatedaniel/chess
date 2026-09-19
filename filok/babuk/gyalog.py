from filok.babuk.babu import Babu
from filok.dataclassok.lepestipusok import Pozicio


class Gyalog(Babu):
    nev = "Gyalog"

    def utes(self) -> list[Pozicio]:
        """Hagyományos ütés"""
        lepesek = [
            (self.gyalog_irany[self.szin], self.gyalog_irany[self.szin]),
            (-self.gyalog_irany[self.szin], self.gyalog_irany[self.szin]),
        ]
        return self.hozzad(lepesek)

    def lepes(self) -> list[Pozicio]:
        """Hagyományos lépés"""
        lepesek = [(0, self.gyalog_irany[self.szin])]
        return self.hozzad(lepesek)

    def elso_lepes(self) -> list[Pozicio]:
        """Első lépés, ami lehet dupla is"""
        lepesek = [
            (0, self.gyalog_irany[self.szin]),
            (0, 2 * self.gyalog_irany[self.szin]),
        ]
        return self.hozzad(lepesek)

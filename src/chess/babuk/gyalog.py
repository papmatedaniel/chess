from typing import ClassVar

from chess.babuk.babu import Babu
from chess.dataclassok.lepestipusok import Pozicio


class Gyalog(Babu):
    nev = "Gyalog"
    gyalog_irany: ClassVar[dict[str, int]] = {"Fehér": -1, "Fekete": 1}

    def lepes(self) -> list[list[Pozicio]]:
        """Hagyományos lépés"""
        lepesek = [(0, self.gyalog_irany[self.szin])]
        return self.hozzad(lepesek)

    def utes(self) -> list[list[Pozicio]]:
        """Hagyományos ütés"""
        dy = self.gyalog_irany.get(self.szin, 0)
        lepesek = [(-1, dy), (1, dy)]
        return self.hozzad(lepesek)

    def elso_lepes(self) -> list[list[Pozicio]]:
        """Első lépés, ami lehet dupla is"""
        dy = self.gyalog_irany.get(self.szin, 0)
        lepesek = [(0, dy), (0, 2 * dy)]
        return self.hozzad(lepesek)

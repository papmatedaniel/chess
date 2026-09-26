from collections.abc import Sequence
from typing import ClassVar

from chess.dataclassok.lepestipusok import Pozicio


class Babu:
    nev: ClassVar[str] = "nincs"

    def __init__(
        self,
        szin: str = "nincs",
        jelenlegi_pozicio: Pozicio | None = None,
    ) -> None:
        self.szin = szin
        kezdo_pozicio = (
            jelenlegi_pozicio if jelenlegi_pozicio is not None else Pozicio(-1, -1)
        )
        self.koordinatak = [kezdo_pozicio]

    @property
    def utolsokoord(self) -> Pozicio:
        return self.koordinatak[-1]

    def hozzad(self, eltolasok: Sequence[tuple[int, int]]) -> list[list[Pozicio]]:
        aktualis = self.utolsokoord
        return [
            [Pozicio(sor=aktualis.sor + dy, oszlop=aktualis.oszlop + dx)]
            for dx, dy in eltolasok
        ]

    def lepes_hozzad(self, iranyok: Sequence[tuple[int, int]]) -> list[list[Pozicio]]:
        aktualis = self.utolsokoord
        folista = []
        for dx, dy in iranyok:
            allista = []
            sor = aktualis.sor
            oszlop = aktualis.oszlop
            for _ in range(8):
                sor += dy
                oszlop += dx
                allista.append(Pozicio(sor=sor, oszlop=oszlop))
            folista.append(allista)

        return folista

    def ortogonalis_lepes(self) -> list[list[Pozicio]]:
        lepesek = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        return self.lepes_hozzad(lepesek)

    def diagonalis_lepes(self) -> list[list[Pozicio]]:
        lepesek = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        return self.lepes_hozzad(lepesek)

    def huszar_lepes(self) -> list[list[Pozicio]]:
        lepesek = [
            (1, 2),
            (2, 1),
            (-1, 2),
            (2, -1),
            (1, -2),
            (-2, 1),
            (-1, -2),
            (-2, -1),
        ]
        return self.hozzad(lepesek)

    def lepes(self) -> list[list[Pozicio]]:
        return []

    def utes(self) -> list[list[Pozicio]]:
        """Alapértelmezetten a bábu oda üthet, ahova léphet."""
        return self.lepes()

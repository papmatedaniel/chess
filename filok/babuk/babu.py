from filok.dataclassok.lepestipusok import Pozicio
from collections.abc import Sequence

class Babu:

    def __init__(
        self,
        szin: str = "nincs",
        nev: str = "nincs",
        jelenlegi_pozicio: Pozicio = Pozicio(-1, -1),
    ) -> None:
        self.szin = szin
        self.nev = nev
        self.koordinatak: list[Pozicio] = [jelenlegi_pozicio]
        self.el_e = True
        self.szinek = {"Fehér": -1, "Fekete": 1}

    @property
    def utolsokoord(self) -> Pozicio:
        return self.koordinatak[-1]

    def hozzad(self, eltolasok: Sequence[tuple[int, int]]) -> list[Pozicio]:
            aktualis = self.utolsokoord
            return [
                Pozicio(sor=aktualis.sor + dy, oszlop=aktualis.oszlop + dx)
                for dx, dy in eltolasok
            ]
        
    def lepes_hozzad(
            self, iranyok: Sequence[tuple[int, int]]
        ) -> list[list[Pozicio]]:
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

    def huszar_lepes(self) -> list[Pozicio]:
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

    def lepes(self) -> list:
        return []

    def __getattr__(self, name):
        if name == "utes":
            return self.lepes

        raise AttributeError(
            f"'{type(self).__name__}' objektumnak nincs '{name}' attribútuma"
        )
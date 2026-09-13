class Babu:

    def __init__(
        self, szin="nincs", nev="nincs", jelenlegi_koordinata=(-1, -1)
    ) -> None:
        self.szin = szin
        self.nev = nev
        self.koordinatak = [jelenlegi_koordinata]
        self.el_e = True
        self.szinek = {"Fehér": -1, "Fekete": 1}

    @property
    def utolsokoord(self) -> tuple[int, int]:
        return self.koordinatak[-1]

    def hozzad(self, lepesek) -> list[tuple[int, int]]:
        x1, y1 = self.utolsokoord
        return [(x1 + x2, y1 + y2) for x2, y2 in lepesek]

    def lepes_hozzad(self, lepesek) -> list[list[tuple[int, int]]]:
        x, y = self.utolsokoord
        folista = []
        for x1, y1 in lepesek:
            allista = []
            aktualisx, akutalisy = (x, y)
            for _ in range(8):
                aktualisx += x1
                akutalisy += y1
                allista.append((aktualisx, akutalisy))
            folista.append(allista)

        return folista

    def ortogonalis_lepes(self) -> list[list[tuple[int, int]]]:
        """Vizszintes és függőleges"""
        lepesek = [(0, 1), (1, 0), (-1, 0), (0, -1)]
        return self.lepes_hozzad(lepesek)

    def diagonalis_lepes(self) -> list[list[tuple[int, int]]]:
        """Átlós"""
        lepesek = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        return self.lepes_hozzad(lepesek)

    def huszar_lepes(self):
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

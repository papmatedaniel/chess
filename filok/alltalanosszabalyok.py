from filok.dataclassok.lepestipusok import Pozicio


class Altalanosszabalyok:

    def hova_lephet(
        self, tabla, poziciok: list[Pozicio]
    ) -> list[Pozicio]:
        jo_poziciok: list[Pozicio] = []

        for pos in poziciok:
            if tabla.bentvane(pos) and tabla.urese(pos):
                jo_poziciok.append(pos)

        return jo_poziciok

    def hova_uthet(
        self, tabla, poziciok: list[Pozicio], szin: str
    ) -> list[Pozicio]:
        jo_poziciok: list[Pozicio] = []

        for pos in poziciok:
            if (
                tabla.bentvane(pos)
                and not tabla.urese(pos)
                and tabla.mezo_lekerdezese(pos).szin != szin
            ):
                jo_poziciok.append(pos)

        return jo_poziciok

    def hova_lephet_sor(
        self, tabla, iranyok: list[list[Pozicio]]
    ) -> list[Pozicio]:
        """Egyenes lépéssorozat üres mezőkre: bástya, futó, vezér."""
        jo_poziciok: list[Pozicio] = []

        for irany in iranyok:
            for pos in irany:
                if tabla.bentvane(pos) and tabla.urese(pos):
                    jo_poziciok.append(pos)
                else:
                    break

        return jo_poziciok

    def hova_uthet_sor(
        self, tabla, iranyok: list[list[Pozicio]], szin: str
    ) -> list[Pozicio]:
        """Egyenes ütési sorozat: bástya, futó, vezér."""
        jo_poziciok: list[Pozicio] = []

        for irany in iranyok:
            for pos in irany:
                if not tabla.bentvane(pos):
                    break

                if not tabla.urese(pos):
                    cel_babu = tabla.mezo_lekerdezese(pos)
                    if cel_babu.szin != szin:
                        jo_poziciok.append(pos)
                    # Ha bármilyen bábu áll az úton (akár saját, akár ellenség), a sugár megtörik
                    break

        return jo_poziciok
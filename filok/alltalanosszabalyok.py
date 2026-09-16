from filok.dataclassok.lepestipusok import Pozicio


class Altalanosszabalyok:
    def hova_lephet(self, tabla, poziciok: list[Pozicio]) -> list[Pozicio]:
        jo_poziciok: list[Pozicio] = []

        for poz in poziciok:
            if tabla.bentvane(poz) and tabla.urese(poz):
                jo_poziciok.append(poz)

        return jo_poziciok

    def hova_uthet(self, tabla, poziciok: list[Pozicio], szin: str) -> list[Pozicio]:
        jo_poziciok: list[Pozicio] = []

        for poz in poziciok:
            if (
                tabla.bentvane(poz)
                and not tabla.urese(poz)
                and tabla.mezo_lekerdezese(poz).szin != szin
            ):
                jo_poziciok.append(poz)

        return jo_poziciok

    def hova_lephet_sor(self, tabla, iranyok: list[list[Pozicio]]) -> list[Pozicio]:
        """Egyenes lépéssorozat üres mezőkre: bástya, futó, vezér."""
        jo_poziciok: list[Pozicio] = []

        for irany in iranyok:
            for poz in irany:
                if tabla.bentvane(poz) and tabla.urese(poz):
                    jo_poziciok.append(poz)
                else:
                    break

        return jo_poziciok

    def hova_uthet_sor(
        self, tabla, iranyok: list[list[Pozicio]], szin: str
    ) -> list[Pozicio]:
        """Egyenes ütési sorozat: bástya, futó, vezér."""
        jo_poziciok: list[Pozicio] = []

        for irany in iranyok:
            for poz in irany:
                if not tabla.bentvane(poz):
                    break

                if not tabla.urese(poz):
                    cel_babu = tabla.mezo_lekerdezese(poz)
                    if cel_babu.szin != szin:
                        jo_poziciok.append(poz)
                    # Ha bármilyen bábu áll az úton (akár saját, akár ellenség), a sugár megtörik
                    break

        return jo_poziciok

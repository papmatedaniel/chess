from filok.babuk.babu import Babu
from filok.dataclassok.lepestipusok import Pozicio


class Sakkkezeles:

    def __init__(self, tabla, babu, szin: str) -> None:
        self.tabla = tabla
        self.babu = babu
        self.szin = szin

    def kiralyvegrehajt(self, szin: str) -> bool:
        holvan = self.kiralyvalaszto(szin)
        return self.kiraly_sakkban_vane(holvan)

    def kiralyvalaszto(self, szin: str) -> Pozicio:
        for sor in self.tabla.tabla:
            for babu in sor:
                if babu.nev == "Király" and babu.szin == szin:
                    return babu.utolsokoord
        return Pozicio(-1, -1)

    def lebont(self, koordinatalista) -> list[Pozicio]:
        lista: list[Pozicio] = []
        for elemek in koordinatalista:
            if isinstance(elemek, list):
                lista.extend(elemek)
            else:
                lista.append(elemek)
        return lista

    def kiraly_sakkban_vane(self, kiraly_pozicio: Pozicio) -> bool:
        # Ideiglenes király objektum a sugárirányú mezők felderítéséhez
        ideiglenes_kiraly = Babu(
            szin=self.szin,
            nev="Király",
            jelenlegi_pozicio=kiraly_pozicio,
        )

        nagylista: list[Pozicio] = []

        lebont1 = self.lebont(
            self.babu.hova_uthet_sor(
                self.tabla, ideiglenes_kiraly.ortogonalis_lepes(), self.szin
            )
        )
        nagylista.extend(lebont1)

        lebont2 = self.lebont(
            self.babu.hova_uthet_sor(
                self.tabla, ideiglenes_kiraly.diagonalis_lepes(), self.szin
            )
        )
        nagylista.extend(lebont2)

        lovak = self.lebont(
            self.babu.hova_uthet(
                self.tabla, ideiglenes_kiraly.huszar_lepes(), self.szin
            )
        )
        nagylista.extend(lovak)

        for elem_pos in nagylista:
            tamado_babu = self.tabla.mezo_lekerdezese(elem_pos)
            kozos: list[Pozicio] = []
            kozos.extend(self.lebont(tamado_babu.utes()))
            kozos.extend(self.lebont(tamado_babu.lepes()))

            if kiraly_pozicio in kozos:
                return True

        return False
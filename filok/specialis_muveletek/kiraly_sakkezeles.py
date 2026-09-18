from filok.babuk.babu import Babu
from filok.dataclassok.lepestipusok import Pozicio


class Sakkkezeles:
    def __init__(self, tabla, babu) -> None:
        self.tabla = tabla
        self.babu = babu

    def sakkbanvane_vezerlo(self, szin: str) -> bool:

        holvan = self.kiralykeresoo(szin)
        return self.kiraly_sakkban_vane(holvan, szin)

    def kiralykeresoo(self, szin: str) -> Pozicio:
        """Szín alapján kikeresi a király koordinátáját."""
        for sor in self.tabla.tabla:
            for babu in sor:
                if babu.nev == "Király" and babu.szin == szin:
                    return babu.utolsokoord
        return Pozicio(-1, -1)

    def lebont(self, koordinatalista) -> list[Pozicio]:
        """1 vagy 2 dimenziós listákat egységesít"""
        lista: list[Pozicio] = []
        for elemek in koordinatalista:
            if isinstance(elemek, list):
                lista.extend(elemek)
            else:
                lista.append(elemek)
        return lista

    def kiraly_sakkban_vane(self, kiraly_pozicio: Pozicio, szin: str) -> bool:
        # Ideiglenes király objektum a sugárirányú mezők felderítéséhez
        ideiglenes_kiraly = Babu(
            szin=szin,
            nev="Király",
            jelenlegi_pozicio=kiraly_pozicio,
        )

        nagylista: list[Pozicio] = []

        lebont1 = self.lebont(
            self.babu.hova_uthet_sor(
                self.tabla, ideiglenes_kiraly.ortogonalis_lepes(), szin
            )
        )
        nagylista.extend(lebont1)

        lebont2 = self.lebont(
            self.babu.hova_uthet_sor(
                self.tabla, ideiglenes_kiraly.diagonalis_lepes(), szin
            )
        )
        nagylista.extend(lebont2)

        lovak = self.lebont(
            self.babu.hova_uthet(self.tabla, ideiglenes_kiraly.huszar_lepes(), szin)
        )
        nagylista.extend(lovak)

        for elem_poz in nagylista:
            tamado_babu = self.tabla.mezo_lekerdezese(elem_poz)
            kozos: list[Pozicio] = []
            kozos.extend(self.lebont(tamado_babu.utes()))
            kozos.extend(self.lebont(tamado_babu.lepes()))

            if kiraly_pozicio in kozos:
                return True

        return False

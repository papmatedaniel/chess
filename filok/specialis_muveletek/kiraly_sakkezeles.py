from filok.babuk.babu import Babu
from filok.dataclassok.lepestipusok import Pozicio


class Sakkkezeles:
    def __init__(self, tabla, altalanosszabalyok) -> None:
        self.tabla = tabla
        self.altalanosszabalyok = altalanosszabalyok

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
            jelenlegi_pozicio=kiraly_pozicio,
        )

        nagylista: list[Pozicio] = []

        nagylista.extend(
            self.altalanosszabalyok.hova_uthet_sor(
                self.tabla, ideiglenes_kiraly.ortogonalis_lepes(), szin
            )
        )

        nagylista.extend(
            self.altalanosszabalyok.hova_uthet_sor(
                self.tabla, ideiglenes_kiraly.diagonalis_lepes(), szin
            )
        )

        nagylista.extend(
            self.altalanosszabalyok.hova_uthet(
                self.tabla, ideiglenes_kiraly.huszar_lepes(), szin
            )
        )

        for elem_poz in nagylista:
            tamado_babu = self.tabla.mezo_lekerdezese(elem_poz)
            if kiraly_pozicio in self.lebont(tamado_babu.utes()):
                return True

        return False

from filok.babu import Babu


class Sakkkezeles:

    def __init__(self, tabla, babu, szin):
        self.tabla = tabla
        self.babu = babu
        self.szin = szin

    def kiralyvegrehajt(self, szin) -> bool:
        holvan = self.kiralyvalaszto(szin)
        return self.kiraly_sakkban_vane(holvan)

    def kiralyvalaszto(self, szin) -> tuple[int, int]:
        # szin=Fehér/Fekete
        # Két koncepció:
        # Mindig megadjuk, hogy melyik szinűt keressük
        # Ezt hasznalhatju ugy, hogy minden allasnal lefuttatjuk
        # Megadjuk manualisan a szint
        # Vagy a lepeslistabol az utolso szint
        for sor in self.tabla.tabla:
            for oszlop_elem in sor:
                x, y = oszlop_elem.utolsokoord
                aktualis_babu = self.tabla.tabla[y][x]
                if aktualis_babu.nev == "Király" and aktualis_babu.szin == szin:
                    return (x, y)
        return (-1, -1)

    def lebont(self, koordinatalista) -> list[tuple[int, int]]:
        lista = []
        for elemek in koordinatalista:
            if type(elemek) == list:
                lista.extend(elemek)
            else:
                lista.append(elemek)
        return lista

    def kiraly_sakkban_vane(self, kiraly_koordinata) -> bool:
        x, y = kiraly_koordinata

        # ideiglenes király objektum
        ideiglenes_kiraly = Babu(
            szin=self.szin, nev="Király", jelenlegi_koordinata=kiraly_koordinata
        )

        nagylista = []

        lebont1 = self.lebont(
            self.babu.hova_uthet_sor(ideiglenes_kiraly.ortogonalis_lepes(), self.szin)
        )
        nagylista.extend(lebont1)

        lebont2 = self.lebont(
            self.babu.hova_uthet_sor(ideiglenes_kiraly.diagonalis_lepes(), self.szin)
        )
        nagylista.extend(lebont2)

        lovak = self.lebont(
            self.babu.hova_uthet(ideiglenes_kiraly.huszar_lepes(), self.szin)
        )
        nagylista.extend(lovak)

        for elem in nagylista:
            x, y = elem
            kozos = []
            kozos.extend(self.lebont(self.tabla.tabla[y][x].utes()))
            kozos.extend(self.lebont(self.tabla.tabla[y][x].lepes()))
            kozos = list(tuple(kozos))

            if kiraly_koordinata in kozos:
                return True

        return False

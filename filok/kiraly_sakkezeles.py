class Sakkkezeles:

    def __init__(self, tabla, babu):
        self.tabla = tabla
        self.babu = babu

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
        # if kiraly_koordinata is None:
        #     kiraly_koordinata = self.babu.utolsokoord

        nagylista = []
        x, y = kiraly_koordinata
        kiralyelem = self.tabla.tabla[y][x]
        lebont1 = self.lebont(
            self.babu.hova_uthet_sor(kiralyelem.ortogonalis_lepes(), "Fehér")
        )
        nagylista.extend(lebont1)
        lebont2 = self.lebont(
            self.babu.hova_uthet_sor(kiralyelem.diagonalis_lepes(), "Fehér")
        )
        nagylista.extend(lebont2)
        lovak = self.lebont(self.babu.hova_uthet(kiralyelem.huszar_lepes(), "Fehér"))
        nagylista.extend(lovak)
        for elem in nagylista:
            x, y = elem
            print(f"{self.tabla.tabla[y][x].utes() = }")
            if kiraly_koordinata in self.lebont(self.tabla.tabla[y][x].utes()):
                return True  # sakkban van, talalt egyet aminek az utesebe van benne

        return False

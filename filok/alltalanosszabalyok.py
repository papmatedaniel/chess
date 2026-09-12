# ide jöhetnek majd a sor_lepes, stb
class Altalanosszabalyok:

    def __init__(self, tabla):
        self.tabla = tabla

    def hova_lephet(self, koordinatak) -> list[tuple[int, int]]:
        jo_koordinatak = []

        for i in koordinatak:
            if self.tabla.bentvane(i) and self.tabla.urese(i):
                jo_koordinatak.append(i)

        return jo_koordinatak

    def hova_uthet(self, koordinatak, szin) -> list[tuple[int, int]]:
        jo_koordinatak = []

        for i in koordinatak:
            if (
                self.tabla.bentvane(i)
                and not self.tabla.urese(i)
                and self.tabla.tabla[i[1]][i[0]].szin != szin
            ):
                jo_koordinatak.append(i)

        return jo_koordinatak

    def hova_lephet_sor(self, koordinatak) -> list[tuple[int, int]]:
        """Egyenes lépssorozat, bástya, futó, vezér"""
        jo_koordinatak = []

        for i in koordinatak:
            for j in i:
                if self.tabla.bentvane(j) and self.tabla.urese(j):
                    jo_koordinatak.append(j)
                else:
                    break

        return jo_koordinatak

    def hova_uthet_sor(self, koordinatak, szin) -> list[tuple[int, int]]:
        """egyenes lépssorozat, bástya, futó"""
        jo_koordinatak = []

        for i in koordinatak:
            for j in i:
                if (
                    self.tabla.bentvane(j)
                    and not self.tabla.urese(j)
                    and self.tabla.tabla[j[1]][j[0]].szin != szin
                ):
                    jo_koordinatak.append(j)
                    break
                if (
                    not self.tabla.bentvane(j)
                    or self.tabla.tabla[j[1]][j[0]].szin == szin
                ):
                    break

        return jo_koordinatak

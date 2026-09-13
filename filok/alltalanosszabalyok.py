class Altalanosszabalyok:

    def hova_lephet(self, tabla, koordinatak) -> list[tuple[int, int]]:
        jo_koordinatak = []

        for i in koordinatak:
            if tabla.bentvane(i) and tabla.urese(i):
                jo_koordinatak.append(i)

        return jo_koordinatak

    def hova_uthet(self, tabla, koordinatak, szin) -> list[tuple[int, int]]:
        jo_koordinatak = []

        for i in koordinatak:
            if (
                tabla.bentvane(i)
                and not tabla.urese(i)
                and tabla.tabla[i[1]][i[0]].szin != szin
            ):
                jo_koordinatak.append(i)

        return jo_koordinatak

    def hova_lephet_sor(self, tabla, koordinatak) -> list[tuple[int, int]]:
        """Egyenes lépssorozat, bástya, futó, vezér"""
        jo_koordinatak = []

        for i in koordinatak:
            for j in i:
                if tabla.bentvane(j) and tabla.urese(j):
                    jo_koordinatak.append(j)
                else:
                    break

        return jo_koordinatak

    def hova_uthet_sor(self, tabla, koordinatak, szin) -> list[tuple[int, int]]:
        """egyenes lépssorozat, bástya, futó"""
        jo_koordinatak = []

        for i in koordinatak:
            for j in i:
                if (
                    tabla.bentvane(j)
                    and not tabla.urese(j)
                    and tabla.tabla[j[1]][j[0]].szin != szin
                ):
                    jo_koordinatak.append(j)
                    break
                if not tabla.bentvane(j) or tabla.tabla[j[1]][j[0]].szin == szin:
                    break

        return jo_koordinatak

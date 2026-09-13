class Gyaloglepes:
    def __init__(self, altalanosszabalyok) -> None:
        self.altalanosszabalyok = altalanosszabalyok

    def gyalog_duplalepese(self, koordinatak) -> bool:
        if len(koordinatak) == 2:
            x1, y1 = koordinatak[0]
            x2, y2 = koordinatak[1]
            return x1 == x2 and abs(y2 - y1) == 2
        return False

    def gyalog_hova_lephet_enpassant(self, tabla, babu) -> dict:

        alap_valasz: dict[str, list[tuple[int, int]] | tuple[int, int] | None] = {
            "vegkoordinata": [],
            "leveheto_koordinata": None,
        }

        if len(tabla.lepesek) == 0:  # nem_lepett
            return alap_valasz

        utolso = tabla.lepesek[-1]
        if utolso.babutipus1 != "Gyalog":
            return alap_valasz

        x1, y1 = utolso.hova1
        x2, y2 = babu.utolsokoord

        if not self.gyalog_duplalepese(tabla.tabla[y1][x1].koordinatak):
            return alap_valasz

        if y2 != y1 or abs(x2 - x1) != 1:
            return alap_valasz

        jo_koordinatak = []
        leveheto_koordinata = None

        for i in babu.utes():
            x = i[0]
            if tabla.bentvane(i) and tabla.urese(i) and x == x1:
                leveheto_koordinata = utolso.hova1
                jo_koordinatak.append(i)

        return {
            "vegkoordinata": jo_koordinatak,
            "leveheto_koordinata": leveheto_koordinata,
        }

    def gyalog_hova_lephet(self, tabla, babu) -> list[tuple[int, int]]:
        # Ha előre 1 lépés engedélyezett, 2-t próbálunk
        if (
            len(babu.koordinatak) == 1
            and len(self.altalanosszabalyok.hova_lephet(tabla, babu.lepes())) == 1
        ):
            if babu.utolsokoord[-1] in [1, 6]:  # második soros gyalogok
                return babu.elso_lepes()

        return self.altalanosszabalyok.hova_lephet(tabla, babu.lepes())

    def gyalog_atvaltozhat_e(self, babu):
        return babu.utolsokoord[1] in [1, 6] and len(babu.koordinatak) > 1

    def gyalog_atvaltozas(self) -> str:
        szotar = {"v": "Vezér", "b": "Bástya", "h": "Huszár", "f": "Futó"}
        while True:
            bemenet = input("Milyen bábuvá változnál?(V, B, H, F): ").lower()
            if bemenet in ["v", "b", "h", "f"]:
                break
            else:
                print("probald ujra")
        return szotar[bemenet]

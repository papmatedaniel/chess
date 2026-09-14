from filok.dataclassok.lepestipusok import Pozicio


class Gyaloglepes:
    def __init__(self, altalanosszabalyok) -> None:
        self.altalanosszabalyok = altalanosszabalyok

    def gyalog_duplalepese(self, koordinatak: list[Pozicio]) -> bool:
        if len(koordinatak) >= 2:
            p1 = koordinatak[-2]
            p2 = koordinatak[-1]
            return p1.oszlop == p2.oszlop and abs(p2.sor - p1.sor) == 2
        return False

    def gyalog_hova_lephet_enpassant(self, tabla, babu) -> dict:
        alap_valasz: dict[str, list[Pozicio] | Pozicio | None] = {
            "vegkoordinata": [],
            "leveheto_koordinata": None,
        }

        if len(tabla.lepesek) == 0:
            return alap_valasz

        utolso = tabla.lepesek[-1]
        utolso_babu = tabla.mezo_lekerdezese(utolso.hova)
        if utolso_babu.nev != "Gyalog":
            return alap_valasz

        pos1 = utolso.hova
        pos2 = babu.utolsokoord

        if not self.gyalog_duplalepese(utolso_babu.koordinatak):
            return alap_valasz

        # Csak közvetlenül egymás mellett álló gyalogok esetén lehetséges
        if pos2.sor != pos1.sor or abs(pos2.oszlop - pos1.oszlop) != 1:
            return alap_valasz

        jo_koordinatak: list[Pozicio] = []
        leveheto_koordinata: Pozicio | None = None

        for cel_pos in babu.utes():
            if (
                tabla.bentvane(cel_pos)
                and tabla.urese(cel_pos)
                and cel_pos.oszlop == pos1.oszlop
            ):
                leveheto_koordinata = utolso.hova
                jo_koordinatak.append(cel_pos)

        return {
            "vegkoordinata": jo_koordinatak,
            "leveheto_koordinata": leveheto_koordinata,
        }

    def gyalog_hova_lephet(self, tabla, babu) -> list[Pozicio]:
        # Ha a kezdő mezőjén van és az 1 mezős előrelépés szabad
        szabad_egyes = self.altalanosszabalyok.hova_lephet(tabla, babu.lepes())
        if len(babu.koordinatak) == 1 and len(szabad_egyes) == 1:
            # Csak a szabad mezőket engedélyezzük a dupla lépésnél is
            return self.altalanosszabalyok.hova_lephet(tabla, babu.elso_lepes())

        return szabad_egyes

    def gyalog_atvaltozhat_e(self, babu) -> bool:
        # Fehér a sor == 0, Fekete a sor == 7 alapsorra érve változik át
        cel_sor = 0 if babu.szin == "Fehér" else 7
        # Ha a következő lépésével eléri a túloldalt
        kovetkezo_sor = babu.utolsokoord.sor + babu.szinek[babu.szin]
        return kovetkezo_sor == cel_sor

    def gyalog_atvaltozas(self) -> str:
        szotar = {"v": "Vezér", "b": "Bástya", "h": "Huszár", "f": "Futó"}
        while True:
            bemenet = input("Milyen bábuvá változnál?(V, B, H, F): ").lower()
            if bemenet in szotar:
                return szotar[bemenet]
            print("Hibás bábutípus! Választható: V, B, H, F")
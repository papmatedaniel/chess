from typing import Any

from chess.babuszabaly import BabuSzabaly
from chess.dataclassok.lepestipusok import Lepes, Pozicio
from chess.specialis_muveletek.kiraly_sakkezeles import Sakkkezeles
from chess.specialis_muveletek.sancszabaly import SancSzabaly
from chess.tabla import Tabla


class Szimulacio:
    def __init__(
        self, tabla: Tabla, sakkezeles: Sakkkezeles, babuszabaly: BabuSzabaly
    ) -> None:
        self.tabla = tabla
        self.sakkezeles = sakkezeles
        self.babuszabaly = babuszabaly

    def lepes_tesztelo(self, lepes: Lepes, szin: str) -> bool:
        """True-t ad vissza, ha a lépés szabályos (a saját király NINCS sakkban utána)."""
        self.tabla.lepes_vegrehajtas(lepes)
        sakkban_maradt = self.sakkezeles.sakkbanvane_vezerlo(szin)
        self.tabla.lepes_visszavonas()

        return not sakkban_maradt

    def validlepesek(self, szin: str) -> dict[Pozicio, list[Pozicio]]:
        szotar: dict[Pozicio, list[Pozicio]] = {}
        for sor in self.tabla.tabla:
            for babu in sor:
                if babu.szin != szin:
                    continue

                osszes_kordinata = self.babuszabaly.elerheto_mezok_lekerese(
                    self.tabla, babu
                )
                gyujt: list[Pozicio] = []
                gyujt.extend(osszes_kordinata.get("lephet", []))
                gyujt.extend(osszes_kordinata.get("uthet", []))

                enpassant = osszes_kordinata.get("enpassant", {})
                if isinstance(enpassant, dict):
                    gyujt.extend(enpassant.get("vegkoordinata", []))

                jo_lepesek: list[Pozicio] = []
                for elem in gyujt:
                    lepestipus = self.babuszabaly.babu_valaszto(
                        self.tabla,
                        babu,
                        babu.utolsokoord,
                        elem,
                    )
                    if not lepestipus.siker or lepestipus.objektum is None:
                        continue
                    if self.lepes_tesztelo(lepestipus.objektum, szin):
                        jo_lepesek.append(elem)
                if len(jo_lepesek) > 0:
                    szotar[babu.utolsokoord] = jo_lepesek

        return szotar

    def valid_sancok(self, szin: str) -> list[str]:
        """Adott színhez tartozó szabályos sáncolási lehetőségek."""
        lista: list[str] = []
        sancszabaly = SancSzabaly(self.tabla, szin, self.sakkezeles)

        for sanc_tipus in ["0-0", "0-0-0"]:
            eredmeny = sancszabaly.sanc_valaszto(sanc_tipus)
            if eredmeny.siker:
                lista.append(sanc_tipus)

        return lista

    def szimulacio_ertekelo(self, szin: str) -> dict[str, Any]:
        valid_lepesek_szotar = self.validlepesek(szin)
        valid_sanc_lista = self.valid_sancok(szin)
        osszes_lepes_szama = sum(
            len(hova) for hova in valid_lepesek_szotar.values()
        ) + len(valid_sanc_lista)
        jatekmehettovabb = osszes_lepes_szama > 0

        allapot = "mehettovabb"
        if not jatekmehettovabb:
            if self.sakkezeles.sakkbanvane_vezerlo(szin):
                allapot = "matt"
            else:
                allapot = "patt"

        return {
            "szabalyos_lepesek_szama": osszes_lepes_szama,
            "lepesek": valid_lepesek_szotar,
            "sancok": valid_sanc_lista,
            "allapot": allapot,
            "jatekmehettovabb": jatekmehettovabb,
        }

    def kiirat(self, szin: str, szotarja: dict[Pozicio, list[Pozicio]]) -> None:
        print(f"A {szin} színhez tartozó összes lehetséges lépése: ")

        for k, v in szotarja.items():
            print(f"Honnan: {k}, hova: {v}")

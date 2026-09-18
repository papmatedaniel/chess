from filok.specialis_muveletek.sancszabaly import SancSzabaly


class Szimulacio:
    def __init__(self, tabla, sakkezeles, babuszabaly):
        self.tabla = tabla
        self.sakkezeles = sakkezeles
        self.babuszabaly = babuszabaly

    def lepes_tesztelo(self, lepes, szin) -> bool:
        """True-t ad vissza, ha a lépés szabályos (a saját király NINCS sakkban utána)."""

        self.tabla.lepes_vegrehajtas(lepes)
        sakkban_maradt = self.sakkezeles.sakkbanvane_vezerlo(szin)
        self.tabla.lepes_visszavonas()

        return not sakkban_maradt

    def validlepesek(self, szin) -> dict:
        szotar = {}
        for sor in self.tabla.tabla:
            for babu in sor:
                if babu.szin != szin:
                    continue

                self.babuszabaly.szimilacio_kapcsolo()
                osszes_kordinata = self.babuszabaly.elerheto_mezok_lekerese(
                    self.tabla, babu
                )
                gyujt = []
                gyujt.extend(osszes_kordinata.get("lephet", []))
                gyujt.extend(osszes_kordinata.get("uthet", []))

                enpassant = osszes_kordinata.get("enpassant", {})
                if isinstance(enpassant, dict):
                    gyujt.extend(enpassant.get("vegkoordinata", []))

                jo_lepesek = []
                for elem in gyujt:
                    lepestipus = self.babuszabaly.babu_valaszto(
                        self.tabla,
                        babu,
                        babu.utolsokoord,
                        elem,
                    )
                    if not lepestipus.siker:
                        continue
                    if self.lepes_tesztelo(lepestipus.objektum, szin):
                        jo_lepesek.append(elem)
                if len(jo_lepesek) > 0:
                    szotar[babu.utolsokoord] = jo_lepesek
        return szotar

    def valid_sancok(self, szin) -> list:
        """Adott színhez tartozó szabályos sáncolási lehetőségek."""
        lista = []
        sancszabaly = SancSzabaly(self.tabla, szin, self.sakkezeles)

        for sanc_tipus in ["0-0", "0-0-0"]:
            eredmeny = sancszabaly.sanc_valaszto(sanc_tipus)
            if eredmeny.siker and self.lepes_tesztelo(eredmeny.objektum, szin):
                lista.append(sanc_tipus)

        return lista

    def szimulacio_ertekelo(self, szin) -> dict:
        osszes_lepes_szama = len(self.validlepesek(szin)) + len(self.valid_sancok(szin))
        jatekmehettovabb = osszes_lepes_szama > 0

        allapot = "mehettovabb"
        if not jatekmehettovabb:
            if self.sakkezeles.sakkbanvane_vezerlo(szin):
                allapot = "matt"
            else:
                allapot = "patt"

        return {
            "szabalyos_lepesek_szama": osszes_lepes_szama,
            "allapot": allapot,
            "jatekmehettovabb": jatekmehettovabb,
        }

    def kiirat(self, szin, szotarja):
        print(f"A {szin} színhez tartozó összes lehetséges lépése: ")

        for k, v in szotarja.items():
            print(f"Honnan: {k}, hova: {v}")

from chess.dataclassok.lepeseredmeny import LepesEredmeny
from chess.dataclassok.lepestipusok import Lepes, LepesTipus, Pozicio


class BabuSzabaly:
    def __init__(self, altalanosszabalyok, gyalogszabalyok) -> None:
        self.altalanosszabalyok = altalanosszabalyok
        self.gyalog = gyalogszabalyok

        self.szabaly_generatorok = {
            "Gyalog": self.gyalog_generator,
            "Huszár": self.generator,
            "Király": self.generator,
            "Futó": self.generator,
            "Bástya": self.generator,
            "Vezér": self.generator,
        }

    def generator(self, tabla, babu) -> dict:
        return {
            "lephet": self.altalanosszabalyok.hova_lephet(tabla, babu.lepes()),
            "uthet": self.altalanosszabalyok.hova_uthet(tabla, babu.utes(), babu.szin),
        }

    def gyalog_generator(
        self,
        tabla,
        babu,
    ) -> dict:

        return {
            "lephet": self.gyalog.gyalog_hova_lephet(tabla, babu),
            "uthet": self.altalanosszabalyok.hova_uthet(tabla, babu.utes(), babu.szin),
            "enpassant": self.gyalog.gyalog_hova_lephet_enpassant(tabla, babu),
            "atvaltozhat": self.gyalog.gyalog_atvaltozhat_e(babu),
        }

    def elerheto_mezok_lekerese(self, tabla, babu) -> dict:
        generator = self.szabaly_generatorok.get(babu.nev)
        if not generator:
            return {"lephet": [], "uthet": []}
        return generator(tabla, babu)

    def lepes_ellenorzo(
        self,
        tabla,
        kezdopozicio: Pozicio,
        sajatszin: str,
        vegpozicio: Pozicio,
    ) -> LepesEredmeny:
        if not tabla.bentvane(kezdopozicio):
            return LepesEredmeny(False, "A kezdő koordináta a pályán kívül van")

        if not tabla.bentvane(vegpozicio):
            return LepesEredmeny(False, "A célkoordináta a pályán kívül van")

        if tabla.urese(kezdopozicio):
            return LepesEredmeny(False, "A kezdő koordinátán nincs bábu")

        babu = tabla.mezo_lekerdezese(kezdopozicio)
        if sajatszin != babu.szin:
            return LepesEredmeny(False, "Az ellenfél bábujához nyúltál")

        return LepesEredmeny(True, "Minden feltétel megfelel")

    def babu_valaszto(
        self,
        tabla,
        babu,
        kezdopozicio: Pozicio,
        vegpozicio: Pozicio,
        valasztott_tiszt: str = "Vezér",
    ) -> LepesEredmeny:
        if babu.nev not in self.szabaly_generatorok:
            return LepesEredmeny(False, "Nincs ilyen bábu")

        adatok = self.szabaly_generatorok[babu.nev](tabla, babu)

        # Ha átváltozhat, a megadott típust használjuk (szimulációnál alapértelmezetten Vezér)
        atvaltozas_tipus = valasztott_tiszt if adatok.get("atvaltozhat") else None

        return self.altalanos_lepes_ellenorzo(
            tabla=tabla,
            kezdopozicio=kezdopozicio,
            vegpozicio=vegpozicio,
            lephet=adatok.get("lephet", []),
            uthet=adatok.get("uthet", []),
            enpassant=adatok.get("enpassant"),
            atvaltozott_babu_tipusa=atvaltozas_tipus,
        )

    def altalanos_lepes_ellenorzo(
        self,
        tabla,
        kezdopozicio: Pozicio,
        vegpozicio: Pozicio,
        lephet: list[Pozicio],
        uthet: list[Pozicio],
        enpassant: dict | None = None,
        atvaltozott_babu_tipusa: str | None = None,
    ) -> LepesEredmeny:
        # 1. Lépés üres mezőre
        if vegpozicio in lephet:
            tipus = (
                LepesTipus.ATVALTOZAS if atvaltozott_babu_tipusa else LepesTipus.SIMA
            )
            lepes = Lepes(
                tipus=tipus,
                honnan=kezdopozicio,
                hova=vegpozicio,
                uj_babu_tipus=atvaltozott_babu_tipusa,
            )
            return LepesEredmeny(True, "Lépés végrehajtható", lepes)

        # 2. Ütés
        if vegpozicio in uthet:
            tipus = (
                LepesTipus.ATVALTOZAS_UTESSEL
                if atvaltozott_babu_tipusa
                else LepesTipus.UTES
            )
            lepes = Lepes(
                tipus=tipus,
                honnan=kezdopozicio,
                hova=vegpozicio,
                levett_babu=tabla.mezo_lekerdezese(vegpozicio),
                levett_babu_pozicio=vegpozicio,
                uj_babu_tipus=atvaltozott_babu_tipusa,
            )
            return LepesEredmeny(True, "Ütés végrehajtható", lepes)

        # 3. En passant lépés
        if enpassant is not None and vegpozicio in enpassant["vegkoordinata"]:
            leutendo_pozicio = enpassant["leveheto_koordinata"]
            lepes = Lepes(
                tipus=LepesTipus.EN_PASSANT,
                honnan=kezdopozicio,
                hova=vegpozicio,
                levett_babu=tabla.mezo_lekerdezese(leutendo_pozicio),
                levett_babu_pozicio=leutendo_pozicio,
            )
            return LepesEredmeny(True, "En passant végrehajtható", lepes)

        return LepesEredmeny(
            False, "A célkoordináta nem egyezik a bábu szabályos lépésével"
        )

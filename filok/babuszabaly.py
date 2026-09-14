from filok.dataclassok.lepeseredmeny import LepesEredmeny
from filok.dataclassok.lepestipusok import Lepes, LepesTipus, Pozicio


class BabuSzabaly:
    def __init__(
        self,
        altalanosszabalyok,
    ) -> None:
        self.altalanosszabalyok = altalanosszabalyok

    def lepes_ellenorzo(
        self,
        tabla,
        kezdopozicio: Pozicio,
        sajatszin: str,
        vegpozicio: Pozicio,
    ) -> LepesEredmeny:
        if not tabla.bentvane(kezdopozicio):
            return LepesEredmeny(False, "A kezdő koordináta a pályán kívül van", None)

        if not tabla.bentvane(vegpozicio):
            return LepesEredmeny(False, "A célkoordináta a pályán kívül van", None)

        if tabla.urese(kezdopozicio):
            return LepesEredmeny(False, "A kezdő koordinátán nincs bábu", None)

        babu = tabla.mezo_lekerdezese(kezdopozicio)
        if sajatszin != babu.szin:
            return LepesEredmeny(False, "Az ellenfél bábujához nyúltál", None)

        return LepesEredmeny(True, "Minden feltétel megfelel", None)

    def babu_valaszto(
        self,
        tabla,
        babu,
        gyalog,
        kezdopozicio: Pozicio,
        vegpozicio: Pozicio,
    ) -> LepesEredmeny:
        match babu.nev:
            case "Gyalog":
                return self.gyalog_lepes_ellenorzo(
                    tabla, babu, gyalog, kezdopozicio, vegpozicio
                )
            case "Huszár":
                return self.huszar_lepes_ellenorzo(
                    tabla, babu, kezdopozicio, vegpozicio
                )
            case "Futó":
                return self.futo_lepes_ellenorzo(
                    tabla, babu, kezdopozicio, vegpozicio
                )
            case "Bástya":
                return self.bastya_lepes_ellenorzo(
                    tabla, babu, kezdopozicio, vegpozicio
                )
            case "Vezér":
                return self.vezer_lepes_ellenorzo(
                    tabla, babu, kezdopozicio, vegpozicio
                )
            case "Király":
                return self.kiraly_lepes_ellenorzo(
                    tabla, babu, kezdopozicio, vegpozicio
                )
            case _:
                return LepesEredmeny(False, "Nincs ilyen bábu", None)

    def altalanos_lepes_ellenorzo(
        self,
        tabla,
        babu,
        kezdopozicio: Pozicio,
        vegpozicio: Pozicio,
        lephet: list[Pozicio],
        uthet: list[Pozicio],
        enpassant: dict | None = None,
        atvaltozott_babu_tipusa: str | None = None,
    ) -> LepesEredmeny:
        # 1. Lépés üres mezőre (sima vagy gyalogátváltozás)
        if vegpozicio in lephet:
            tipus = (
                LepesTipus.ATVALTOZAS
                if atvaltozott_babu_tipusa
                else LepesTipus.SIMA
            )
            lepes = Lepes(
                tipus=tipus,
                honnan=kezdopozicio,
                hova=vegpozicio,
                uj_babu_tipus=atvaltozott_babu_tipusa,
            )
            return LepesEredmeny(True, "Lépés végrehajtható", lepes)

        # 2. Ütés (sima ütés vagy ütéssel egybekötött átváltozás)
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
            False,
            "A célkoordináta nem egyezik a bábu szabályos lépésével",
            None,
        )

    def gyalog_lepes_ellenorzo(
        self, tabla, babu, gyalog, kezdopozicio: Pozicio, vegpozicio: Pozicio
    ) -> LepesEredmeny:
        lephet = gyalog.gyalog_hova_lephet(tabla, babu)
        uthet = self.altalanosszabalyok.hova_uthet(tabla, babu.utes(), babu.szin)
        enpassant = gyalog.gyalog_hova_lephet_enpassant(tabla, babu)
        atvaltozott_babu_tipusa = None
        if gyalog.gyalog_atvaltozhat_e(babu):
            atvaltozott_babu_tipusa = gyalog.gyalog_atvaltozas()

        return self.altalanos_lepes_ellenorzo(
            tabla,
            babu,
            kezdopozicio,
            vegpozicio,
            lephet,
            uthet,
            enpassant,
            atvaltozott_babu_tipusa,
        )

    def huszar_lepes_ellenorzo(
        self, tabla, babu, kezdopozicio: Pozicio, vegpozicio: Pozicio
    ) -> LepesEredmeny:
        lephet = self.altalanosszabalyok.hova_lephet(tabla, babu.lepes())
        uthet = self.altalanosszabalyok.hova_uthet(tabla, babu.utes(), babu.szin)

        return self.altalanos_lepes_ellenorzo(
            tabla, babu, kezdopozicio, vegpozicio, lephet, uthet, None
        )

    def bastya_lepes_ellenorzo(
        self, tabla, babu, kezdopozicio: Pozicio, vegpozicio: Pozicio
    ) -> LepesEredmeny:
        lephet = self.altalanosszabalyok.hova_lephet_sor(tabla, babu.lepes())
        uthet = self.altalanosszabalyok.hova_uthet_sor(tabla, babu.utes(), babu.szin)

        return self.altalanos_lepes_ellenorzo(
            tabla, babu, kezdopozicio, vegpozicio, lephet, uthet, None
        )

    def futo_lepes_ellenorzo(
        self, tabla, babu, kezdopozicio: Pozicio, vegpozicio: Pozicio
    ) -> LepesEredmeny:
        lephet = self.altalanosszabalyok.hova_lephet_sor(tabla, babu.lepes())
        uthet = self.altalanosszabalyok.hova_uthet_sor(tabla, babu.utes(), babu.szin)

        return self.altalanos_lepes_ellenorzo(
            tabla, babu, kezdopozicio, vegpozicio, lephet, uthet, None
        )

    def vezer_lepes_ellenorzo(
        self, tabla, babu, kezdopozicio: Pozicio, vegpozicio: Pozicio
    ) -> LepesEredmeny:
        lephet = self.altalanosszabalyok.hova_lephet_sor(tabla, babu.lepes())
        uthet = self.altalanosszabalyok.hova_uthet_sor(tabla, babu.utes(), babu.szin)

        return self.altalanos_lepes_ellenorzo(
            tabla, babu, kezdopozicio, vegpozicio, lephet, uthet, None
        )

    def kiraly_lepes_ellenorzo(
        self, tabla, babu, kezdopozicio: Pozicio, vegpozicio: Pozicio
    ) -> LepesEredmeny:
        lephet = self.altalanosszabalyok.hova_lephet(tabla, babu.lepes())
        uthet = self.altalanosszabalyok.hova_uthet(tabla, babu.utes(), babu.szin)

        return self.altalanos_lepes_ellenorzo(
            tabla, babu, kezdopozicio, vegpozicio, lephet, uthet, None
        )
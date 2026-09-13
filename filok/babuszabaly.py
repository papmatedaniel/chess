from filok.dataclassok.lepeseredmeny import LepesEredmeny


class BabuSzabaly:
    def __init__(
        self,
        lepestipusok,
        altalanosszabalyok,
    ) -> None:
        self.lepestipusok = lepestipusok
        self.altalanosszabalyok = altalanosszabalyok

    def lepes_ellenorzo(
        self, tabla, kezdokoordinata, sajatszin, vegkoordinata
    ) -> LepesEredmeny:
        if tabla.urese(kezdokoordinata):
            return LepesEredmeny(False, "A kezdő koordinátán nincs bábu", None)
        if not tabla.bentvane(kezdokoordinata):
            return LepesEredmeny(False, "A kezdő koordináta a pályán kívül van", None)

        if not tabla.bentvane(vegkoordinata):
            return LepesEredmeny(False, "A célkoordináta a pályán kívül van", None)

        x, y = kezdokoordinata
        if not tabla.urese(kezdokoordinata) and sajatszin != tabla.tabla[y][x].szin:
            return LepesEredmeny(False, "Az ellenfél bábujához nyúltál", None)

        return LepesEredmeny(True, "Minden feltétel megfelel", None)

    def babu_valaszto(
        self, tabla, babu, gyalog, kezdokordinata, vegkordinata
    ) -> LepesEredmeny:

        match babu.nev:
            case "Gyalog":
                return self.gyalog_lepes_ellenorzo(
                    tabla, babu, gyalog, kezdokordinata, vegkordinata
                )

            case "Huszár":
                return self.huszar_lepes_ellenorzo(
                    tabla, babu, kezdokordinata, vegkordinata
                )
            case "Futó":
                return self.futo_lepes_ellenorzo(
                    tabla, babu, kezdokordinata, vegkordinata
                )

            case "Bástya":
                return self.bastya_lepes_ellenorzo(
                    tabla, babu, kezdokordinata, vegkordinata
                )

            case "Vezér":
                return self.vezer_lepes_ellenorzo(
                    tabla, babu, kezdokordinata, vegkordinata
                )
            case "Király":
                return self.kiraly_lepes_ellenorzo(
                    tabla, babu, kezdokordinata, vegkordinata
                )
            case _:
                return LepesEredmeny(False, "Nincs ilyen bábu", None)

    def altalanos_lepes_ellenorzo(
        self,
        tabla,
        babu,
        kezdokoordinata,
        vegkoordinata,
        lephet,
        uthet,
        enpassant=None,
        atvaltozott_babu_tipusa=None,
    ) -> LepesEredmeny:
        x, y = vegkoordinata
        if vegkoordinata in lephet:
            lepesobjektum = self.lepestipusok(
                muvelet="lepes",
                honnan1=kezdokoordinata,
                hova1=vegkoordinata,
                babutipus1=babu.nev,
                babuszin=babu.szin,
                atvaltozott_babu_tipusa=atvaltozott_babu_tipusa,
            )
            self.altalanos_lepes_vegrehajtas(tabla, lepesobjektum)
            return LepesEredmeny(True, "Lépés végrehajtva", lepesobjektum)

        if vegkoordinata in uthet:
            lepesobjektum = self.lepestipusok(
                muvelet="utes",
                honnan1=kezdokoordinata,
                hova1=vegkoordinata,
                babutipus1=babu.nev,
                babuszin=babu.szin,
                levett_babutipus=tabla.tabla[y][x].nev,
                levett_babukoordinataja=vegkoordinata,
                atvaltozott_babu_tipusa=atvaltozott_babu_tipusa,
            )
            self.altalanos_lepes_vegrehajtas(tabla, lepesobjektum)
            return LepesEredmeny(True, "Ütés végrehajtva", lepesobjektum)

        if enpassant is not None and vegkoordinata in enpassant["vegkoordinata"]:
            lepesobjektum = self.lepestipusok(
                muvelet="enpassant",
                honnan1=kezdokoordinata,
                hova1=vegkoordinata,
                babutipus1=babu.nev,
                babuszin=babu.szin,
                levett_babutipus=tabla.tabla[y][x].nev,
                levett_babukoordinataja=enpassant["leveheto_koordinata"],
            )

            self.altalanos_lepes_vegrehajtas(tabla, lepesobjektum)

            return LepesEredmeny(True, "En passant végrehajtva", lepesobjektum)

        return LepesEredmeny(
            False,
            "A célkoordináta nem egyezik a bábu szabályos lépésével",
            None,
        )

    def altalanos_lepes_vegrehajtas(self, tabla, lepesobjektum):
        tabla.lepes_mentes(lepesobjektum)
        tabla.tablamodosit()

    def gyalog_lepes_ellenorzo(
        self, tabla, babu, gyalog, kezdokoordinata, vegkoordinata
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
            kezdokoordinata,
            vegkoordinata,
            lephet,
            uthet,
            enpassant,
            atvaltozott_babu_tipusa,
        )

    def huszar_lepes_ellenorzo(
        self, tabla, babu, kezdokoordinata, vegkoordinata
    ) -> LepesEredmeny:
        lephet = self.altalanosszabalyok.hova_lephet(tabla, babu.lepes())
        uthet = self.altalanosszabalyok.hova_uthet(tabla, babu.utes(), babu.szin)

        return self.altalanos_lepes_ellenorzo(
            tabla, babu, kezdokoordinata, vegkoordinata, lephet, uthet, None
        )

    def bastya_lepes_ellenorzo(
        self, tabla, babu, kezdokoordinata, vegkoordinata
    ) -> LepesEredmeny:
        lephet = self.altalanosszabalyok.hova_lephet_sor(tabla, babu.lepes())
        uthet = self.altalanosszabalyok.hova_uthet_sor(tabla, babu.utes(), babu.szin)

        return self.altalanos_lepes_ellenorzo(
            tabla, babu, kezdokoordinata, vegkoordinata, lephet, uthet, None
        )

    def futo_lepes_ellenorzo(
        self, tabla, babu, kezdokoordinata, vegkoordinata
    ) -> LepesEredmeny:
        lephet = self.altalanosszabalyok.hova_lephet_sor(tabla, babu.lepes())
        uthet = self.altalanosszabalyok.hova_uthet_sor(tabla, babu.utes(), babu.szin)

        return self.altalanos_lepes_ellenorzo(
            tabla, babu, kezdokoordinata, vegkoordinata, lephet, uthet, None
        )

    def vezer_lepes_ellenorzo(
        self, tabla, babu, kezdokoordinata, vegkoordinata
    ) -> LepesEredmeny:
        lephet = self.altalanosszabalyok.hova_lephet_sor(tabla, babu.lepes())
        uthet = self.altalanosszabalyok.hova_uthet_sor(tabla, babu.utes(), babu.szin)

        return self.altalanos_lepes_ellenorzo(
            tabla, babu, kezdokoordinata, vegkoordinata, lephet, uthet, None
        )

    def kiraly_lepes_ellenorzo(
        self, tabla, babu, kezdokoordinata, vegkoordinata
    ) -> LepesEredmeny:
        lephet = self.altalanosszabalyok.hova_lephet(tabla, babu.lepes())
        uthet = self.altalanosszabalyok.hova_uthet(tabla, babu.utes(), babu.szin)

        return self.altalanos_lepes_ellenorzo(
            tabla, babu, kezdokoordinata, vegkoordinata, lephet, uthet, None
        )

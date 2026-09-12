from filok.lepeseredmeny import LepesEredmeny


class BabuSzabaly:
    def __init__(
        self,
        tabla,
        lepestipusok,
        sajatszin,
        babu,
        babu_oslepesek,
        altalanosszabalyok,
        gyalog,
    ) -> None:
        self.babu = babu
        self.babu_oslepesek = babu_oslepesek
        self.lepestipusok = lepestipusok
        self.tabla = tabla
        self.sajatszin = sajatszin
        self.altalanosszabalyok = altalanosszabalyok
        self.gyalog = gyalog

    def lepes_ellenorzo(self, kezdokoordinata, vegkoordinata) -> LepesEredmeny:
        if self.tabla.urese(kezdokoordinata):
            return LepesEredmeny(False, "A kezdő koordinátán nincs bábu")
        if not self.tabla.bentvane(kezdokoordinata):
            return LepesEredmeny(False, "A kezdő koordináta a pályán kívül van")

        if not self.tabla.bentvane(vegkoordinata):
            return LepesEredmeny(False, "A célkoordináta a pályán kívül van")

        x, y = kezdokoordinata
        if (
            not self.tabla.urese(kezdokoordinata)
            and self.sajatszin != self.tabla.tabla[y][x].szin
        ):
            return LepesEredmeny(False, "Az ellenfél bábujához nyúltál")

        return LepesEredmeny(True, "Minden feltétel megfelel")

    def babu_valaszto(self, kezdokordinata, vegkordinata) -> LepesEredmeny:

        match self.babu.nev:
            case "Gyalog":
                return self.gyalog_lepes_ellenorzo(kezdokordinata, vegkordinata)

            case "Huszár":
                return self.huszar_lepes_ellenorzo(kezdokordinata, vegkordinata)
            case "Futó":
                return self.futo_lepes_ellenorzo(kezdokordinata, vegkordinata)

            case "Bástya":
                return self.bastya_lepes_ellenorzo(kezdokordinata, vegkordinata)

            case "Vezér":
                return self.vezer_lepes_ellenorzo(kezdokordinata, vegkordinata)
            case "Király":
                return self.kiraly_lepes_ellenorzo(kezdokordinata, vegkordinata)
            case _:
                return LepesEredmeny(False, "Nincs ilyen bábu")

    def altalanos_lepes_ellenorzo(
        self,
        kezdokoordinata,
        vegkoordinata,
        lephet,
        uthet,
        enpassant=None,
        atvaltozott_babu_tipusa=None,
    ) -> LepesEredmeny:
        x, y = vegkoordinata
        if vegkoordinata in lephet:
            self.tabla.lepes_mentes(
                self.lepestipusok(
                    muvelet="lepes",
                    honnan1=kezdokoordinata,
                    hova1=vegkoordinata,
                    babutipus1=self.babu.nev,
                    babuszin=self.babu.szin,
                    atvaltozott_babu_tipusa=atvaltozott_babu_tipusa,
                )
            )
            self.tabla.tablamodosit()
            return LepesEredmeny(True, "Lépés végrehajtva")

        if vegkoordinata in uthet:
            self.tabla.lepes_mentes(
                self.lepestipusok(
                    muvelet="utes",
                    honnan1=kezdokoordinata,
                    hova1=vegkoordinata,
                    babutipus1=self.babu.nev,
                    babuszin=self.babu.szin,
                    levett_babutipus=self.tabla.tabla[y][x].nev,
                    levett_babukoordinataja=vegkoordinata,
                    atvaltozott_babu_tipusa=atvaltozott_babu_tipusa,
                )
            )
            self.tabla.tablamodosit()
            return LepesEredmeny(True, "Ütés végrehajtva")

        if enpassant is not None and vegkoordinata in enpassant["vegkoordinata"]:
            self.tabla.lepes_mentes(
                self.lepestipusok(
                    muvelet="enpassant",
                    honnan1=kezdokoordinata,
                    hova1=vegkoordinata,
                    babutipus1=self.babu.nev,
                    babuszin=self.babu.szin,
                    levett_babutipus=self.tabla.tabla[y][x].nev,
                    levett_babukoordinataja=enpassant["leveheto_koordinata"],
                )
            )
            self.tabla.tablamodosit()
            return LepesEredmeny(True, "En passant végrehajtva")

        return LepesEredmeny(
            False, "A célkoordináta nem egyezik a bábu szabályos lépésével"
        )

    def gyalog_lepes_ellenorzo(self, kezdokoordinata, vegkoordinata) -> LepesEredmeny:
        lephet = self.gyalog.gyalog_hova_lephet()
        uthet = self.altalanosszabalyok.hova_uthet(self.babu.utes(), self.babu.szin)
        enpassant = self.gyalog.gyalog_hova_lephet_enpassant()
        atvaltozott_babu_tipusa = None
        if self.gyalog.gyalog_atvaltozhat_e():
            atvaltozott_babu_tipusa = self.gyalog.gyalog_atvaltozas()

        return self.altalanos_lepes_ellenorzo(
            kezdokoordinata,
            vegkoordinata,
            lephet,
            uthet,
            enpassant,
            atvaltozott_babu_tipusa,
        )

    def huszar_lepes_ellenorzo(self, kezdokoordinata, vegkoordinata) -> LepesEredmeny:
        lephet = self.altalanosszabalyok.hova_lephet(self.babu.lepes())
        uthet = self.altalanosszabalyok.hova_uthet(self.babu.utes(), self.babu.szin)

        return self.altalanos_lepes_ellenorzo(
            kezdokoordinata, vegkoordinata, lephet, uthet, None
        )

    def bastya_lepes_ellenorzo(self, kezdokoordinata, vegkoordinata) -> LepesEredmeny:
        lephet = self.altalanosszabalyok.hova_lephet_sor(self.babu.lepes())
        uthet = self.altalanosszabalyok.hova_uthet_sor(self.babu.utes(), self.babu.szin)

        return self.altalanos_lepes_ellenorzo(
            kezdokoordinata, vegkoordinata, lephet, uthet, None
        )

    def futo_lepes_ellenorzo(self, kezdokoordinata, vegkoordinata) -> LepesEredmeny:
        lephet = self.altalanosszabalyok.hova_lephet_sor(self.babu.lepes())
        uthet = self.altalanosszabalyok.hova_uthet_sor(self.babu.utes(), self.babu.szin)

        return self.altalanos_lepes_ellenorzo(
            kezdokoordinata, vegkoordinata, lephet, uthet, None
        )

    def vezer_lepes_ellenorzo(self, kezdokoordinata, vegkoordinata) -> LepesEredmeny:
        lephet = self.altalanosszabalyok.hova_lephet_sor(self.babu.lepes())
        uthet = self.altalanosszabalyok.hova_uthet_sor(self.babu.utes(), self.babu.szin)

        return self.altalanos_lepes_ellenorzo(
            kezdokoordinata, vegkoordinata, lephet, uthet, None
        )

    def kiraly_lepes_ellenorzo(self, kezdokoordinata, vegkoordinata) -> LepesEredmeny:
        lephet = self.altalanosszabalyok.hova_lephet(self.babu.lepes())
        uthet = self.altalanosszabalyok.hova_uthet(self.babu.utes(), self.babu.szin)

        return self.altalanos_lepes_ellenorzo(
            kezdokoordinata, vegkoordinata, lephet, uthet, None
        )

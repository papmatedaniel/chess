

        
from mypy.typeops import false_only


class Szabaly:
    def __init__(self, lepestipusok, tabla, babu):
        self.lepestipusok = lepestipusok
        self.tabla = tabla
        self.babu = babu

    def babu_valaszto(self, babutipus, kezdokordinata, vegkordinata):
        match babutipus:
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
                pass



    def lepes_ellenorzo(self, kezdokoordinata, vegkoordinata) -> str | None:
        if self.tabla.urese(kezdokoordinata):
            return "A kezdő koordinátán nincs bábu"

        if not self.tabla.bentvane(kezdokoordinata):
            return "A kezdő koordináta a pályán kívül van"
        
        if not self.tabla.bentvane(vegkoordinata):
            return "A célkoordináta a pályán kívül van"

        return None


    def hova_lephet(self):
        jo_koordinatak = []

        for i in self.babu.lepes():
            if self.tabla.bentvane(i) and self.tabla.urese(i):
                jo_koordinatak.append(i)

        return jo_koordinatak
    

    def hova_uthet(self) -> list[int]:
        jo_koordinatak = []

        for i in self.babu.utes():
            if self.tabla.bentvane(i) and not self.tabla.urese(i) and self.tabla.tabla[i[1]][i[0]].szin != self.babu.szin:
                jo_koordinatak.append(i)

        return jo_koordinatak

    def hova_lephet_sor(self):
        """egyenes lépssorozat, bástya, futó"""
        jo_koordinatak = []

        for i in self.babu.lepes():
            for j in i:
                if self.tabla.bentvane(j) and self.tabla.urese(j):
                    jo_koordinatak.append(j)
                else:
                    break

        return jo_koordinatak

    def hova_uthet_sor(self):
        """egyenes lépssorozat, bástya, futó"""
        jo_koordinatak = []

        for i in self.babu.utes():
            for j in i:
                if self.tabla.bentvane(j) and not self.tabla.urese(j) and self.tabla.tabla[j[1]][j[0]].szin != self.babu.szin:
                    jo_koordinatak.append(j)
                    break
                if not self.tabla.bentvane(j) or self.tabla.tabla[j[1]][j[0]].szin == self.babu.szin:
                    break

        return jo_koordinatak

    def gyalog_duplalepese(self, koordinatak) -> bool:
        if len(koordinatak) == 2:
            x1, y1 = koordinatak[0]
            x2, y2 = koordinatak[1]
            return x1 == x2 and abs(y2 - y1) == 2
        return False

    def gyalog_hova_lephet_enpassant(self):
        
        jo_koordinatak = []
        leveheto_koordinata = (0,0)
        if len(self.tabla.lepesek) > 0:
            utolso = self.tabla.lepesek[-1]
            if utolso.babutipus1 == "Gyalog":
                x1, y1 = utolso.hova1
                x2, y2 = self.babu.koordinatak[-1]
                if self.gyalog_duplalepese(self.tabla.tabla[y1][x1].koordinatak):
                    if y2 == y1 and abs(x2 - x1) == 1:
                        for i in self.babu.utes():
                            x = i[0]
                            if self.tabla.bentvane(i) and self.tabla.urese(i) and x == x1:
                                leveheto_koordinata = utolso.hova1
                                jo_koordinatak.append(i)

        return {"vegkoordinata": jo_koordinatak, "leveheto_koordinata" : leveheto_koordinata}


    def gyalog_hova_lephet(self) -> list[int]:

        if len(self.babu.koordinatak) == 1 and len(self.hova_lephet()) == 1: # Ha előre 1 lépés engedélyezett, 2-t próbálunk
            if self.babu.koordinatak[-1][-1] in [1,6]: # második soros gyalogok
                return self.babu.elso_lepes()

        return self.hova_lephet()

    def altalanos_lepes_ellenorzo(self, kezdokoordinata, vegkoordinata, lephet, uthet, enpassant=None):
        x,y = vegkoordinata
        if vegkoordinata in lephet: 
            print("Lépés")
            self.tabla.lepes_mentes(self.lepestipusok(muvelet = "lepes",
                                                      honnan1 = kezdokoordinata,
                                                      hova1 = vegkoordinata,
                                                      babutipus1 = self.babu.nev,
                                                      babuszin = self.babu.szin))
            self.tabla.tablamodosit(kezdokoordinata, vegkoordinata, "csere")
            return "Lépés végrehajtva"
            
        if vegkoordinata in uthet: 
            print("Ütés")
            self.tabla.lepes_mentes(self.lepestipusok(muvelet = "utes",
                                                      honnan1 = kezdokoordinata,
                                                      hova1 = vegkoordinata,
                                                      babutipus1 = self.babu.nev,
                                                      babuszin = self.babu.szin,
                                                      levett_babutipus = self.tabla.tabla[y][x].nev
                                                      )) 
            self.tabla.tablamodosit(kezdokoordinata, vegkoordinata, "utes")
            return "Lépés végrehajtva"


        if enpassant is not None and vegkoordinata in enpassant["vegkoordinata"]:
            print("Enpassant")
            self.tabla.lepes_mentes(self.lepestipusok(muvelet = "enpassant",
                                                      honnan1 = kezdokoordinata,
                                                      hova1 = vegkoordinata,
                                                      babutipus1 = self.babu.nev,
                                                      babuszin = self.babu.szin,
                                                      levett_babutipus = self.tabla.tabla[y][x].nev,
                                                      levett_babukoordinataja = enpassant["leveheto_koordinata"]
                                                      )) 
            self.tabla.tablamodosit(kezdokoordinata, vegkoordinata, "enpassant", enpassant["leveheto_koordinata"])
            return "Lépés végrehajtva"

        return "A megadott célkoordináta nem egyezik a bábu szabályos lépésével"


    def gyalog_lepes_ellenorzo(self, kezdokoordinata, vegkoordinata) -> str:
        lephet = self.gyalog_hova_lephet()
        uthet = self.hova_uthet()
        enpassant = self.gyalog_hova_lephet_enpassant()

        return self.altalanos_lepes_ellenorzo(
            kezdokoordinata,
            vegkoordinata,
            lephet,
            uthet,
            enpassant
        )        




    def huszar_lepes_ellenorzo(self, kezdokoordinata, vegkoordinata) -> str:
        lephet = self.hova_lephet()
        uthet = self.hova_uthet()

        return self.altalanos_lepes_ellenorzo(
            kezdokoordinata,
            vegkoordinata,
            lephet,
            uthet,
            None
        )

    def bastya_lepes_ellenorzo(self, kezdokoordinata, vegkoordinata) -> str:
        lephet = self.hova_lephet_sor()
        uthet = self.hova_uthet_sor()

        return self.altalanos_lepes_ellenorzo(
            kezdokoordinata,
            vegkoordinata,
            lephet,
            uthet,
            None
        )


    def futo_lepes_ellenorzo(self, kezdokoordinata, vegkoordinata) -> str:
        lephet = self.hova_lephet_sor()
        uthet = self.hova_uthet_sor()

        return self.altalanos_lepes_ellenorzo(
            kezdokoordinata,
            vegkoordinata,
            lephet,
            uthet,
            None
        )

    def vezer_lepes_ellenorzo(self, kezdokoordinata, vegkoordinata) -> str:
        lephet = self.hova_lephet_sor()
        uthet = self.hova_uthet_sor()

        return self.altalanos_lepes_ellenorzo(
            kezdokoordinata,
            vegkoordinata,
            lephet,
            uthet,
            None
        )
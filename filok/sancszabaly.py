
from filok.lepeseredmeny import LepesEredmeny
from filok.sanc import Sanc


class SancSzabaly:

    def __init__(self, tabla, lepestipusok, sanc, szin) -> None:
        self.tabla = tabla
        self.lepestipusok = lepestipusok
        self.sanc = sanc
        self.szin = szin
        self.sor = Sanc.szinek[self.szin]

    def kettokozottikoordinatak(self, egy, ketto) -> list[tuple[int, int]]:
        """Csak vízszintben"""
        y = egy[1]
        x1, x2 = sorted([egy[0], ketto[0]])
        return [(i, y) for i in range(x1 + 1, x2)]

    def teruletszabad(self, lista) -> bool:
        """Megkapja a területet, és vissza adja, hogy van e ott bábu"""
        return all(self.tabla.urese(i) for i in lista)

    def sanc_lephet_e(self) -> LepesEredmeny:

        if not self.sanc in ["0-0", "0-0-0"]:
            return LepesEredmeny(False, "Nem létező sánc típus")

        egeszsor = self.tabla.tabla[self.sor]
        kiraly = egeszsor[Sanc.kiraly_honnan]
        bastya = egeszsor[Sanc.sancvalaszto[self.sanc]["bastya_honnan"]]
        if kiraly.nev != "Király" or bastya.nev != "Bástya":
            return LepesEredmeny(False, "Hiámyzó bábu")

        if len(kiraly.koordinatak) != 1 or len(bastya.koordinatak) != 1:
            return LepesEredmeny(False, "Korábbi lépés miatt nem sáncolhatsz")

        if not self.teruletszabad(
            self.kettokozottikoordinatak(kiraly.koordinatak[-1], bastya.koordinatak[-1])
        ):
            return LepesEredmeny(False, "Útban van más bábu")

        return LepesEredmeny(True, "Sáncolás végrehajtható")

    def sanc_valaszto(self) -> LepesEredmeny:
        eredmeny = self.sanc_lephet_e()
        print(eredmeny.uzenet)

        if not eredmeny.siker:
            return eredmeny

        return self.sanc_lepes()

    def sanc_lepes(self) -> LepesEredmeny:
        kiraly_honnan = (Sanc.kiraly_honnan, self.sor)
        bastya_honnan = (Sanc.sancvalaszto[self.sanc]["bastya_honnan"], self.sor)
        kiraly_hova = (Sanc.sancvalaszto[self.sanc]["kiraly_hova"], self.sor)
        bastya_hova = (Sanc.sancvalaszto[self.sanc]["bastya_hova"], self.sor)

        self.tabla.lepes_mentes(
            self.lepestipusok(
                muvelet="sánc",
                honnan1=kiraly_honnan,
                hova1=kiraly_hova,
                babutipus1=Sanc.babu1,
                honnan2=bastya_honnan,
                hova2=bastya_hova,
                babutipus2=Sanc.babu2,  # sanctipus atadasa
            )
        )
        self.tabla.tablamodosit()
        return LepesEredmeny(True, "Sánc végrehajtva")

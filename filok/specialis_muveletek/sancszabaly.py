from filok.dataclassok.lepeseredmeny import LepesEredmeny
from filok.dataclassok.lepestipusok import Lepes, LepesTipus, Pozicio
from filok.dataclassok.sanc import Sanc


class SancSzabaly:
    def __init__(self, tabla, szin, sakkezeles) -> None:
        self.tabla = tabla
        self.szin = szin
        self.sor = Sanc.szinek[self.szin]
        self.sakkezeles = sakkezeles

    def kettokozottikoordinatak(self, egy: Pozicio, ketto: Pozicio) -> list[Pozicio]:
        """A király és bástya közötti üresnek kötelező mezők listája."""
        sor = egy.sor
        oszlop1, oszlop2 = sorted([egy.oszlop, ketto.oszlop])
        return [Pozicio(sor=sor, oszlop=i) for i in range(oszlop1 + 1, oszlop2)]

    def teruletszabad(self, poziciok: list[Pozicio]) -> bool:
        """Megadja, hogy az adott mezők mindegyike üres-e."""
        return all(self.tabla.urese(poz) for poz in poziciok)

    def sanc_lephet_e(self, sanc) -> LepesEredmeny:
        if sanc not in ["0-0", "0-0-0"]:
            return LepesEredmeny(False, "Nem létező sánc típus", None)

        kiraly_oszlop = Sanc.kiraly_honnan
        bastya_oszlop = Sanc.sancvalaszto[sanc]["bastya_honnan"]

        kiraly_poz = Pozicio(sor=self.sor, oszlop=kiraly_oszlop)
        bastya_poz = Pozicio(sor=self.sor, oszlop=bastya_oszlop)

        kiraly = self.tabla.mezo_lekerdezese(kiraly_poz)
        bastya = self.tabla.mezo_lekerdezese(bastya_poz)

        if kiraly.nev != "Király" or bastya.nev != "Bástya":
            return LepesEredmeny(False, "Hiányzó bábu", None)

        if len(kiraly.koordinatak) != 1 or len(bastya.koordinatak) != 1:
            return LepesEredmeny(False, "Korábbi lépés miatt nem sáncolhatsz", None)

        kettokozott = self.kettokozottikoordinatak(kiraly_poz, bastya_poz)
        if not self.teruletszabad(kettokozott):
            return LepesEredmeny(False, "Útban van más bábu", None)

        # A király által érintett mezők ellenőrzése (kezdő, áthaladó, érkező mező nem lehet sakkban)
        kiraly_cel_oszlop = Sanc.sancvalaszto[sanc]["kiraly_hova"]
        lepes_irany = 1 if kiraly_cel_oszlop > kiraly_oszlop else -1

        kiraly_utvonala = [
            kiraly_poz,
            Pozicio(sor=self.sor, oszlop=kiraly_oszlop + lepes_irany),
            Pozicio(sor=self.sor, oszlop=kiraly_cel_oszlop),
        ]

        if any(
            self.sakkezeles.kiraly_sakkban_vane(poz, self.szin)
            for poz in kiraly_utvonala
        ):
            return LepesEredmeny(False, "Támadott a király/mozgástere", None)

        return LepesEredmeny(True, "Sáncolás végrehajtható", None)

    def sanc_koordinatak(self, sanc) -> tuple[Pozicio, Pozicio, Pozicio, Pozicio]:
        kiraly_honnan = Pozicio(sor=self.sor, oszlop=Sanc.kiraly_honnan)
        bastya_honnan = Pozicio(
            sor=self.sor,
            oszlop=Sanc.sancvalaszto[sanc]["bastya_honnan"],
        )
        kiraly_hova = Pozicio(
            sor=self.sor,
            oszlop=Sanc.sancvalaszto[sanc]["kiraly_hova"],
        )
        bastya_hova = Pozicio(
            sor=self.sor,
            oszlop=Sanc.sancvalaszto[sanc]["bastya_hova"],
        )

        return kiraly_honnan, bastya_honnan, kiraly_hova, bastya_hova

    def sanc_valaszto(self, sanc) -> LepesEredmeny:
        eredmeny = self.sanc_lephet_e(sanc)

        if not eredmeny.siker:
            return eredmeny

        kiraly_honnan, bastya_honnan, kiraly_hova, bastya_hova = self.sanc_koordinatak(
            sanc
        )

        lepesobj = Lepes(
            tipus=LepesTipus.SANC,
            honnan=kiraly_honnan,
            hova=kiraly_hova,
            bastya_honnan=bastya_honnan,
            bastya_hova=bastya_hova,
        )

        return LepesEredmeny(True, "Sánc végrehajtható", lepesobj)

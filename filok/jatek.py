from filok.babuszabaly import BabuSzabaly
from filok.sancszabaly import SancSzabaly
from filok.babu import Babu
from filok.gyalog_lepes import Gyaloglepes
from filok.alltalanosszabalyok import Altalanosszabalyok
from filok.kiraly_sakkezeles import Sakkkezeles

class Jatek:
    """Felhasználói interface. Ez lép közvetlen kapcsolatba a felhasználóval."""

    def __init__(self, tablaobj, lepestipusok) -> None:
        self.nev1 = ""
        self.nev2 = ""
        self.tablaobj = tablaobj
        self.lepestipusok = lepestipusok

    def nev_beker(self) -> None:
        """Bekéri a neveket a játékosoktól"""
        nevek = [self.nev1, self.nev2]
        for i in range(2):
            while nevek[i] == "":
                nev = input("Add meg a neved. (2-7) karakter hosszúságban: ")
                if 2 > len(nev) or len(nev) > 7:
                    print("2-7 karakter hossszú nevet válassz!")
                elif nevek[i] == nev or nevek[i - 1] == nev:
                    print("Ne ugyanazt a nevet add meg mint a másik játékos")
                else:
                    nevek[i] = nev

    def koordinata_beker(self, bemenet) -> list[int]:
        """Bekéri a koordinátákat a játékosoktól"""
        szoveg = "abcdefgh"
        honnan, hova = bemenet.split(" ")
        x1, y1 = honnan
        x2, y2 = hova
        return [szoveg.index(x1), 8 - int(y1), szoveg.index(x2), 8 - int(y2)]

    def lepesek(self) -> None:
        szinek = ["Fehér", "Fekete"]

        while True:
            print(szinek[0])
            try:
                self.tablaobj.tablakiirat()
                bemenet = input("Add meg a koordinátákat(honnan hová): a2 a3: ").lower()

                try:
                    x1, y1, x2, y2 = self.koordinata_beker(bemenet)

                    szabaly = BabuSzabaly(
                        self.tablaobj,
                        self.lepestipusok,
                        szinek[0],
                        self.tablaobj.tabla[y1][x1],
                        Babu(),
                        Altalanosszabalyok(self.tablaobj),
                        Gyaloglepes(self.tablaobj,
                                    self.tablaobj.tabla[y1][x1],
                                    Altalanosszabalyok(self.tablaobj)
                                    )
                    )

                    ellenorzes = szabaly.lepes_ellenorzo((x1, y1), (x2, y2))
                    print(ellenorzes.uzenet)

                    if not ellenorzes.siker:
                        continue

                    vegrehajtas = szabaly.babu_valaszto((x1, y1), (x2, y2))
                    print(vegrehajtas.uzenet)

                    if vegrehajtas.siker:
                        szinek = szinek[::-1]
                        print(Sakkkezeles(self.tablaobj, Altalanosszabalyok(self.tablaobj)).kiralyvegrehajt("Fehér"))

                except (ValueError, IndexError , KeyError):
                    try:
                        szabaly2 = SancSzabaly(
                            self.tablaobj, self.lepestipusok, bemenet, szinek[0]
                        )
                        eredmeny2 = szabaly2.sanc_valaszto()
                        print(eredmeny2.uzenet)

                        if eredmeny2.siker:
                            szinek = szinek[::-1]

                    except (KeyError , ValueError, IndexError):
                        print("Hibás input")
                        continue

            except KeyboardInterrupt:
                print("\nKilépés")
                break

    def jatekmenet(self) -> None:
        # self.nev_beker()
        self.tablaobj.tablageneralas()
        self.lepesek()

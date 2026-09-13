from filok.alltalanosszabalyok import Altalanosszabalyok
from filok.babuszabaly import BabuSzabaly
from filok.specialis_muveletek.gyalog_lepes import Gyaloglepes
from filok.specialis_muveletek.kiraly_sakkezeles import Sakkkezeles
from filok.specialis_muveletek.sancszabaly import SancSzabaly


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

                    # 1. BabuSzabaly példányosítás (helyes konstruktor)
                    szabaly = BabuSzabaly(
                        self.lepestipusok,
                        Altalanosszabalyok()
                    )

                    # 2. Általános ellenőrzés
                    ellenorzes = szabaly.lepes_ellenorzo(
                        self.tablaobj,
                        (x1, y1),
                        szinek[0],
                        (x2, y2)
                    )
                    print(ellenorzes.uzenet)

                    if not ellenorzes.siker:
                        continue

                    # 3. Bábuspecifikus ellenőrzés
                    babu = self.tablaobj.tabla[y1][x1]
                    gyalog = Gyaloglepes(Altalanosszabalyok())

                    vegrehajtas = szabaly.babu_valaszto(
                        self.tablaobj,
                        babu,
                        gyalog,
                        (x1, y1),
                        (x2, y2)
                    )
                    print(vegrehajtas.uzenet)

                    # 4. Ha szabályos → végrehajtás
                    if vegrehajtas.siker:
                        szabaly.altalanos_lepes_vegrehajtas(
                            self.tablaobj,
                            vegrehajtas.objektum
                        )

                        szinek = szinek[::-1]

                        print(
                            f"{Sakkkezeles(self.tablaobj, szabaly, szinek[0]).kiralyvegrehajt('Fehér') = }"
                        )

                except (ValueError, IndexError, KeyError):
                    # 5. SÁNC KEZELÉSE (javított verzió)
                    try:
                        szabaly = BabuSzabaly(self.lepestipusok, Altalanosszabalyok())
                        szabaly2 = SancSzabaly(
                            self.tablaobj,
                            self.lepestipusok,
                            bemenet,
                            szinek[0],
                            Sakkkezeles(self.tablaobj, szabaly, szinek[0])
                        )

                        # 5/a. Sánc ellenőrzés + lépésobjektum létrehozása
                        eredmeny2 = szabaly2.sanc_valaszto()
                        print(eredmeny2.uzenet)

                        # 5/b. Ha szabályos → SÁNC VÉGREHAJTÁSA
                        if eredmeny2.siker:
                            szabaly2.sanc_lepes(self.tablaobj, eredmeny2.objektum)
                            szinek = szinek[::-1]

                    except (KeyError, ValueError, IndexError):
                        print("Hibás input")
                        continue

            except KeyboardInterrupt:
                print("\nKilépés")
                break



    def jatekmenet(self) -> None:
        # self.nev_beker()
        self.tablaobj.tablageneralas()
        self.lepesek()

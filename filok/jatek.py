from filok.babuszabaly import BabuSzabaly
from filok.sancszabaly import SancSzabaly


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
        szinek = ["fehér", "fekete"]
        while True:
            print(szinek[0])
            try:
                self.tablaobj.tablakiirat()
                bemenet = input("Add meg a koordinátákat(honnan hová): a2 a3: ").lower()

                try:
                    # Megpróbáljuk normál lépésként feldolgozni
                    x1, y1, x2, y2 = self.koordinata_beker(bemenet)
                    szabaly = BabuSzabaly(
                        self.tablaobj, self.lepestipusok, self.tablaobj.tabla[y1][x1]
                    )
                    eredmeny = szabaly.lepes_ellenorzo((x1, y1), (x2, y2))
                    print(eredmeny.uzenet)
                    if eredmeny.siker:
                        print(szabaly.babu_valaszto((x1, y1), (x2, y2)))
                        szinek = szinek[::-1]

                except ValueError:
                    try:
                        szabaly2 = SancSzabaly(
                            self.tablaobj, self.lepestipusok, bemenet, szinek[0]
                        )
                        eredmeny2 = szabaly2.sanc_valaszto()
                        print(eredmeny2.uzenet)
                        if eredmeny2.siker:
                            szinek = szinek[::-1]

                    except (
                        KeyError,
                        ValueError,
                        IndexError,
                    ):  # Csak a sima hibákat kapja el, a kilépést NEM!
                        print("Hibás input")
                        szinek = szinek[::-1]

            except KeyboardInterrupt:
                # Ez most már biztosan elkapja a Ctrl+C-t vagy a leállítást
                print("\nKilépés")
                break

    def jatekmenet(self) -> None:
        # self.nev_beker()
        self.tablaobj.tablageneralas()
        self.lepesek()

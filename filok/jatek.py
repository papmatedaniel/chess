from filok.szabaly import Szabaly


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
                elif nevek[i] == nev or nevek[i-1] == nev:
                    print("Ne ugyanazt a nevet add meg mint a másik játékos")
                else:
                    nevek[i] = nev

    def koordinata_beker(self, bemenet) -> list[int]:
        """Bekéri a koordinátákat a játékosoktól"""
        szoveg = "abcdefgh"
        honnan, hova = bemenet.split(" ")
        x1,y1 = honnan
        x2,y2 = hova
        return [szoveg.index(x1), 8-int(y1), szoveg.index(x2), 8-int(y2)]



    def lepesek(self) -> None:
        while True:
            self.tablaobj.tablakiirat()
            try: 
                bemenet = input("Add meg a koordinátákat(honnan hová): a2 a3: ").lower()
                x1,y1,x2,y2 = self.koordinata_beker(bemenet)
                szabaly = Szabaly(self.lepestipusok, self.tablaobj, self.tablaobj.tabla[y1][x1])
                hiba = szabaly.lepes_ellenorzo((x1,y1), (x2,y2))
                if hiba != None:
                    print(hiba)
                else:
                    babutipus = self.tablaobj.tabla[y1][x1].nev
                    print(szabaly.babu_valaszto(babutipus, (x1,y1), (x2,y2)))

            except ValueError:
                print("Hibás input")

            except KeyboardInterrupt:
                print("Kilépés")
                break

    def jatekmenet(self) -> None:
        # self.nev_beker()
        self.tablaobj.tablageneralas()
        self.lepesek()




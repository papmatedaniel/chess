from filok.alltalanosszabalyok import Altalanosszabalyok
from filok.babuszabaly import BabuSzabaly
from filok.dataclassok.lepestipusok import Pozicio
from filok.specialis_muveletek.gyalog_lepes import Gyaloglepes
from filok.specialis_muveletek.kiraly_sakkezeles import Sakkkezeles
from filok.specialis_muveletek.sancszabaly import SancSzabaly


class Jatek:
    """Felhasználói interface. Ez lép közvetlen kapcsolatba a felhasználóval."""

    def __init__(self, tablaobj, lepestipusok=None) -> None:
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

    def koordinata_beker(self, bemenet: str) -> tuple[Pozicio, Pozicio]:
        """Bekéri és Pozíció objektumokká alakítja a koordinátákat."""
        oszlop_betuk = "abcdefgh"
        honnan_str, hova_str = bemenet.strip().split(" ")

        honnan = Pozicio(
            sor=8 - int(honnan_str[1]),
            oszlop=oszlop_betuk.index(honnan_str[0]),
        )
        hova = Pozicio(
            sor=8 - int(hova_str[1]),
            oszlop=oszlop_betuk.index(hova_str[0]),
        )
        return honnan, hova

    def lepesek(self) -> None:
        szinek = ["Fehér", "Fekete"]

        while True:
            print(szinek[0])
            try:
                self.tablaobj.tablakiirat()
                bemenet = input("Add meg a koordinátákat(honnan hová): a2 a3: ").lower()

                try:
                    honnan_pos, hova_pos = self.koordinata_beker(bemenet)

                    # 1. BabuSzabaly példányosítás
                    szabaly = BabuSzabaly(Altalanosszabalyok())

                    # 2. Általános ellenőrzés Pozicio típusokkal
                    ellenorzes = szabaly.lepes_ellenorzo(
                        self.tablaobj, honnan_pos, szinek[0], hova_pos
                    )
                    print(ellenorzes.uzenet)

                    if not ellenorzes.siker:
                        continue

                    # 3. Bábuspecifikus ellenőrzés
                    babu = self.tablaobj.mezo_lekerdezese(honnan_pos)
                    gyalog = Gyaloglepes(Altalanosszabalyok())

                    vegrehajtas = szabaly.babu_valaszto(
                        self.tablaobj, babu, gyalog, honnan_pos, hova_pos
                    )
                    print(vegrehajtas.uzenet)

                    # 4. Ha szabályos → végrehajtás
                    if vegrehajtas.siker:
                        self.tablaobj.lepes_vegrehajtas(vegrehajtas.objektum)
                        szinek = szinek[::-1]

                except (ValueError, IndexError, KeyError):
                    # 5. SÁNC KEZELÉSE
                    try:
                        szabaly2 = SancSzabaly(
                            self.tablaobj,
                            self.lepestipusok,
                            bemenet,
                            szinek[0],
                            Sakkkezeles(self.tablaobj, Altalanosszabalyok(), szinek[0]),
                        )

                        # 5/a. Sánc ellenőrzés
                        eredmeny2 = szabaly2.sanc_valaszto()
                        print(eredmeny2.uzenet)

                        # 5/b. Ha szabályos → végrehajtás
                        if eredmeny2.siker:
                            self.tablaobj.lepes_vegrehajtas(eredmeny2.objektum)
                            szinek = szinek[::-1]

                    except (ValueError, IndexError, KeyError):
                        print("Hibás input")
                        continue

            except KeyboardInterrupt:
                print("\nKilépés")
                break

    def jatekmenet(self) -> None:
        # self.nev_beker()
        self.tablaobj.tablageneralas()
        self.lepesek()
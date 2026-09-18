from filok.alltalanosszabalyok import Altalanosszabalyok
from filok.babuszabaly import BabuSzabaly
from filok.dataclassok.lepestipusok import Pozicio
from filok.specialis_muveletek.gyalog_lepes import Gyaloglepes
from filok.specialis_muveletek.kiraly_sakkezeles import Sakkkezeles
from filok.specialis_muveletek.sancszabaly import SancSzabaly
from filok.szimulacio import Szimulacio


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

        alt_szabaly = Altalanosszabalyok()
        gyalog_szabaly = Gyaloglepes(alt_szabaly)
        babu_szabaly = BabuSzabaly(alt_szabaly, gyalog_szabaly)
        sakkezeles = Sakkkezeles(self.tablaobj, alt_szabaly)

        szimulacio = Szimulacio(self.tablaobj, sakkezeles, babu_szabaly)

        while True:
            soron_kovetkezo = szinek[0]
            print(f"\n--- {soron_kovetkezo} köre ---")

            try:
                self.tablaobj.tablakiirat()

                valid_lepesek = szimulacio.validlepesek(soron_kovetkezo)
                valid_sanc_lehetosegek = szimulacio.valid_sancok(soron_kovetkezo)

                # Játék vége ellenőrzés
                szimulacio_ertekelo = szimulacio.szimulacio_ertekelo(soron_kovetkezo)
                if not szimulacio_ertekelo["jatekmehettovabb"]:
                    print("Játék vége")
                    if szimulacio_ertekelo["allapot"] != "patt":
                        print(f"Sakk-matt! A {soron_kovetkezo} vesztett.")
                    else:
                        print("Patt! A játék döntetlen.")
                    break

                bemenet = (
                    input("Lépés (pl. e2 e4) vagy sánc (0-0 / 0-0-0): ").strip().lower()
                )

                # --- Sáncolás ága ---
                if bemenet in ["0-0", "0-0-0"]:
                    if bemenet in valid_sanc_lehetosegek:
                        sanc_szabaly = SancSzabaly(
                            self.tablaobj, soron_kovetkezo, sakkezeles
                        )
                        sanc_eredmeny = sanc_szabaly.sanc_valaszto(bemenet)
                        self.tablaobj.lepes_vegrehajtas(sanc_eredmeny.objektum)
                        szinek = szinek[::-1]
                    else:
                        print("A sáncolás nem hajtható végre!")
                    continue

                # --- Hagyományos lépés ága ---
                try:
                    honnan_poz, hova_poz = self.koordinata_beker(bemenet)
                except (ValueError, IndexError):
                    print("Hibás koordináta formátum! Használat: 'e2 e4'")
                    continue

                ellenorzes = babu_szabaly.lepes_ellenorzo(
                    self.tablaobj, honnan_poz, soron_kovetkezo, hova_poz
                )
                if not ellenorzes.siker:
                    print(ellenorzes.uzenet)
                    continue

                babu = self.tablaobj.mezo_lekerdezese(honnan_poz)
                vegrehajtas = babu_szabaly.babu_valaszto(
                    self.tablaobj, babu, honnan_poz, hova_poz
                )
                if not vegrehajtas.siker:
                    print(vegrehajtas.uzenet)
                    continue

                if (
                    honnan_poz in valid_lepesek
                    and hova_poz in valid_lepesek[honnan_poz]
                ):
                    self.tablaobj.lepes_vegrehajtas(vegrehajtas.objektum)
                    szinek = szinek[::-1]
                else:
                    print(
                        "Szabálytalan lépés: a lépés után a királyod sakkban maradna!"
                    )

            except KeyboardInterrupt:
                print("\nKilépés a játékból.")
                break

    def jatekmenet(self) -> None:
        # self.nev_beker()
        self.tablaobj.tablageneralas()
        self.lepesek()

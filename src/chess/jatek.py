from chess.alltalanosszabalyok import Altalanosszabalyok
from chess.babuszabaly import BabuSzabaly
from chess.dataclassok.lepestipusok import Pozicio
from chess.specialis_muveletek.gyalog_lepes import Gyaloglepes
from chess.specialis_muveletek.kiraly_sakkezeles import Sakkkezeles
from chess.specialis_muveletek.sancszabaly import SancSzabaly
from chess.szimulacio import Szimulacio


class Jatek:
    """Felhasználói interfész. Kapcsolatot tart a játékossal és vezérli a körmenetet."""

    def __init__(self, tablaobj) -> None:
        self.tablaobj = tablaobj

    def koordinata_beker(self, bemenet: str) -> tuple[Pozicio, Pozicio]:
        """Bekéri és Pozicio objektumokká alakítja a koordinátákat."""
        honnan_str, hova_str = bemenet.strip().split()
        return Pozicio.alakit(honnan_str), Pozicio.alakit(hova_str)

    def atvaltozas_beker(self) -> str:
        """Konzolos bekérés a felhasználótól gyalog átváltozás esetén."""
        szotar = {"v": "Vezér", "b": "Bástya", "h": "Huszár", "f": "Futó"}
        while True:
            bemenet = input("Milyen bábuvá változnál? (V, B, H, F): ").strip().lower()
            if bemenet in szotar:
                return szotar[bemenet]
            print("Hibás bábutípus! Választható: V, B, H, F")

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

                szimulacio_adatok = szimulacio.szimulacio_ertekelo(soron_kovetkezo)
                valid_lepesek = szimulacio_adatok["lepesek"]
                valid_sanc_lehetosegek = szimulacio_adatok["sancok"]

                # Matt / Patt vizsgálat
                if not szimulacio_adatok["jatekmehettovabb"]:
                    print("Játék vége!")
                    if szimulacio_adatok["allapot"] == "matt":
                        print(f"Sakk-matt! A {soron_kovetkezo} vesztett.")
                    else:
                        print("Patt! A játék döntetlen.")
                    break

                bemenet = (
                    input("Lépés (pl. e2 e4) vagy sánc (0-0 / 0-0-0): ").strip().lower()
                )

                # --- 1. Sáncolás ága ---
                if bemenet in ["0-0", "0-0-0"]:
                    if bemenet in valid_sanc_lehetosegek:
                        sanc_szabaly = SancSzabaly(
                            self.tablaobj, soron_kovetkezo, sakkezeles
                        )
                        sanc_eredmeny = sanc_szabaly.sanc_valaszto(bemenet)
                        if sanc_eredmeny.objektum is not None:
                            self.tablaobj.lepes_vegrehajtas(sanc_eredmeny.objektum)
                            szinek = szinek[::-1]
                    else:
                        print("A sáncolás nem hajtható végre!")
                    continue

                # --- 2. Hagyományos lépés ága ---
                try:
                    honnan_poz, hova_poz = self.koordinata_beker(bemenet)
                except (ValueError, IndexError):
                    print("Hibás koordináta formátum! Használat: 'e2 e4'")
                    continue

                # Alapvető mező- és bábu-ellenőrzés
                ellenorzes = babu_szabaly.lepes_ellenorzo(
                    self.tablaobj, honnan_poz, soron_kovetkezo, hova_poz
                )
                if not ellenorzes.siker:
                    print(ellenorzes.uzenet)
                    continue

                babu = self.tablaobj.mezo_lekerdezese(honnan_poz)

                # Gyalog átváltozás típusának bekérése
                valasztott_tiszt = "Vezér"
                if babu.nev == "Gyalog" and gyalog_szabaly.gyalog_atvaltozhat_e(babu):
                    valasztott_tiszt = self.atvaltozas_beker()

                # Fizikai/geometriai lépéslehetőség ellenőrzése
                vegrehajtas = babu_szabaly.babu_valaszto(
                    self.tablaobj,
                    babu,
                    honnan_poz,
                    hova_poz,
                    valasztott_tiszt=valasztott_tiszt,
                )
                if not vegrehajtas.siker or vegrehajtas.objektum is None:
                    print(vegrehajtas.uzenet)
                    continue

                # Király biztonságának ellenőrzése a legális lépéshalmaz alapján
                if not (
                    honnan_poz in valid_lepesek
                    and hova_poz in valid_lepesek[honnan_poz]
                ):
                    print(
                        "Szabálytalan lépés: a lépés után a királyod sakkban maradna!"
                    )
                    continue

                self.tablaobj.lepes_vegrehajtas(vegrehajtas.objektum)
                szinek = szinek[::-1]

            except KeyboardInterrupt:
                print("\nKilépés a játékból.")
                break

    def jatekmenet(self) -> None:
        self.tablaobj.tablageneralas()
        self.lepesek()

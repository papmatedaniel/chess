import copy
from typing import Any

from chess.dataclassok.lepestipusok import Lepes, LepesTipus, Pozicio


class Tabla:
    def __init__(self, *, mezo, gyalog, huszar, futo, bastya, vezer, kiraly) -> None:
        self.mezo = mezo
        self.gyalog = gyalog
        self.huszar = huszar
        self.futo = futo
        self.bastya = bastya
        self.vezer = vezer
        self.kiraly = kiraly

        self.tabla: list[list[Any]] = []
        self.lepesek: list[Lepes] = []

    def tablageneralas(self) -> None:
        """Teljes sakk kezdőállás legenerálása deklaratív sablon alapján."""
        tiszt_sablon = [
            self.bastya,
            self.huszar,
            self.futo,
            self.vezer,
            self.kiraly,
            self.futo,
            self.huszar,
            self.bastya,
        ]

        for y in range(8):
            sor = []
            for x in range(8):
                poz = Pozicio(sor=y, oszlop=x)

                if y == 0:  # Fekete tisztek
                    babu = copy.deepcopy(tiszt_sablon[x])
                    babu.szin = "Fekete"
                elif y == 1:  # Fekete gyalogok
                    babu = copy.deepcopy(self.gyalog)
                    babu.szin = "Fekete"
                elif y == 6:  # Fehér gyalogok
                    babu = copy.deepcopy(self.gyalog)
                    babu.szin = "Fehér"
                elif y == 7:  # Fehér tisztek
                    babu = copy.deepcopy(tiszt_sablon[x])
                    babu.szin = "Fehér"
                else:  # Üres mező
                    babu = copy.deepcopy(self.mezo)

                babu.koordinatak = [poz]
                sor.append(babu)

            self.tabla.append(sor)

    # ---------------------------------------------------------
    # Pozíció alapú mezőkezelő metódusok
    # ---------------------------------------------------------

    def bentvane(self, pozicio: Pozicio) -> bool:
        """Ellenőrzi, hogy a pozíció a pályán belül van-e."""
        return pozicio.palyan_van()

    def urese(self, pozicio: Pozicio) -> bool:
        """Ellenőrzi, hogy a megadott mező üres-e."""
        return self.tabla[pozicio.sor][pozicio.oszlop].nev == "nincs"

    def mezo_lekerdezese(self, pozicio: Pozicio) -> Any:
        return self.tabla[pozicio.sor][pozicio.oszlop]

    def mezo_beallitasa(self, pozicio: Pozicio, babu: Any) -> None:
        self.tabla[pozicio.sor][pozicio.oszlop] = babu
        if hasattr(babu, "koordinatak") and babu.koordinatak[-1] != pozicio:
            babu.koordinatak.append(pozicio)

    def _uresit_mezo(self, pozicio: Pozicio) -> None:
        uj_ures = copy.deepcopy(self.mezo)
        uj_ures.koordinatak = [pozicio]
        self.tabla[pozicio.sor][pozicio.oszlop] = uj_ures

    def _mozgat_babu(self, honnan: Pozicio, hova: Pozicio) -> None:
        babu = self.mezo_lekerdezese(honnan)
        self.mezo_beallitasa(hova, babu)
        self._uresit_mezo(honnan)

    def _uj_babu_letrehozasa(
        self, pozicio: Pozicio, babutipus: str | None, szin: str
    ) -> None:
        tiszt_prototipusok = {
            "Vezér": self.vezer,
            "Bástya": self.bastya,
            "Huszár": self.huszar,
            "Futó": self.futo,
        }

        if babutipus not in tiszt_prototipusok:
            raise ValueError(f"Ismeretlen átváltozási bábutípus: {babutipus}")

        uj_babu = copy.deepcopy(tiszt_prototipusok[babutipus])
        uj_babu.szin = szin
        uj_babu.koordinatak = [pozicio]
        self.tabla[pozicio.sor][pozicio.oszlop] = uj_babu

    # ---------------------------------------------------------
    # Lépés végrehajtása és visszavonása
    # ---------------------------------------------------------

    def lepes_vegrehajtas(self, lepes: Lepes) -> None:
        """Determinisztikus lépésvégrehajtás a LepesTipus alapján."""
        match lepes.tipus:
            case LepesTipus.SIMA | LepesTipus.UTES:
                self._mozgat_babu(lepes.honnan, lepes.hova)

            case LepesTipus.SANC:
                assert lepes.bastya_honnan is not None and lepes.bastya_hova is not None
                self._mozgat_babu(lepes.honnan, lepes.hova)
                self._mozgat_babu(lepes.bastya_honnan, lepes.bastya_hova)

            case LepesTipus.EN_PASSANT:
                assert lepes.levett_babu_pozicio is not None
                self._uresit_mezo(lepes.levett_babu_pozicio)
                self._mozgat_babu(lepes.honnan, lepes.hova)

            case LepesTipus.ATVALTOZAS:
                szin = self.mezo_lekerdezese(lepes.honnan).szin
                self._uresit_mezo(lepes.honnan)
                self._uj_babu_letrehozasa(lepes.hova, lepes.uj_babu_tipus, szin)

            case LepesTipus.ATVALTOZAS_UTESSEL:
                szin = self.mezo_lekerdezese(lepes.honnan).szin
                self._uresit_mezo(lepes.honnan)
                self._uj_babu_letrehozasa(lepes.hova, lepes.uj_babu_tipus, szin)

        self.lepesek.append(lepes)

    def _visszamozgat_babu(self, honnan_most: Pozicio, hova_vissza: Pozicio) -> None:
        """Bábu visszamozgatása az előző helyére a történet bővítése nélkül."""
        babu = self.mezo_lekerdezese(honnan_most)

        if len(babu.koordinatak) > 1:
            babu.koordinatak.pop()

        # Közvetlenül a mátrixba írjuk vissza, nem hívunk történet-bővítő settert
        self.tabla[hova_vissza.sor][hova_vissza.oszlop] = babu
        self._uresit_mezo(honnan_most)

    def lepes_visszavonas(self) -> None:
        """A legutolsó lépés visszavonása."""
        if not self.lepesek:
            return

        lepes = self.lepesek.pop()

        match lepes.tipus:
            case LepesTipus.SIMA:
                self._visszamozgat_babu(lepes.hova, lepes.honnan)

            case LepesTipus.UTES:
                self._visszamozgat_babu(lepes.hova, lepes.honnan)
                self.tabla[lepes.hova.sor][lepes.hova.oszlop] = lepes.levett_babu

            case LepesTipus.SANC:
                assert lepes.bastya_honnan is not None and lepes.bastya_hova is not None
                self._visszamozgat_babu(lepes.hova, lepes.honnan)
                self._visszamozgat_babu(lepes.bastya_hova, lepes.bastya_honnan)

            case LepesTipus.EN_PASSANT:
                assert lepes.levett_babu_pozicio is not None
                self._visszamozgat_babu(lepes.hova, lepes.honnan)
                self.tabla[lepes.levett_babu_pozicio.sor][
                    lepes.levett_babu_pozicio.oszlop
                ] = lepes.levett_babu

            case LepesTipus.ATVALTOZAS:
                szin = self.mezo_lekerdezese(lepes.hova).szin
                self._uresit_mezo(lepes.hova)
                gyalog = copy.deepcopy(self.gyalog)
                gyalog.szin = szin
                # Legalább 2 pozíciót kap a története, hogy soha ne lehessen újra kezdő/duplalépéses
                gyalog.koordinatak = [Pozicio(-1, -1), lepes.honnan]
                self.tabla[lepes.honnan.sor][lepes.honnan.oszlop] = gyalog

            case LepesTipus.ATVALTOZAS_UTESSEL:
                szin = self.mezo_lekerdezese(lepes.hova).szin
                self.tabla[lepes.hova.sor][lepes.hova.oszlop] = lepes.levett_babu
                gyalog = copy.deepcopy(self.gyalog)
                gyalog.szin = szin
                gyalog.koordinatak = [Pozicio(-1, -1), lepes.honnan]
                self.tabla[lepes.honnan.sor][lepes.honnan.oszlop] = gyalog

    def tablakiirat(self) -> None:
        szotar = {
            "Gyalog": {"Fehér": "♙", "Fekete": "♟"},
            "Bástya": {"Fehér": "♖", "Fekete": "♜"},
            "Huszár": {"Fehér": "♘", "Fekete": "♞"},
            "Futó": {"Fehér": "♗", "Fekete": "♝"},
            "Vezér": {"Fehér": "♕", "Fekete": "♛"},
            "Király": {"Fehér": "♔", "Fekete": "♚"},
            "nincs": {"nincs": " ", "Fehér": " ", "Fekete": " "},
        }

        FEKETE_SZIN = "\033[93m"
        ALAP_SZIN = "\033[0m"

        elvalaszto = "  +" + "---+" * 8
        print(elvalaszto)

        for idx, sor in enumerate(self.tabla):
            sor_szam = len(self.tabla) - idx
            sor_szoveg = f"{sor_szam} |"

            for mezo in sor:
                if mezo.nev == "nincs":
                    sor_szoveg += "   |"
                else:
                    babu = szotar[mezo.nev][mezo.szin]
                    if mezo.szin == "Fekete":
                        sor_szoveg += f" {FEKETE_SZIN}{babu}{ALAP_SZIN} |"
                    else:
                        sor_szoveg += f" {babu} |"

            print(sor_szoveg)
            print(elvalaszto)

        print("    A   B   C   D   E   F   G   H  ")

import copy
from typing import Any, TypeGuard

from filok.lepestipusok import Lepestipusok


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
        self.lepesek: list[Lepestipusok] = []

    def tablageneralas(self) -> None:
        """Teljes sakk kezdőállás legenerálása."""

        for y in range(8):
            sor = []
            for x in range(8):

                # Üres mező alapértelmezésben
                uj_mezo = copy.deepcopy(self.mezo)
                uj_mezo.koordinatak[-1] = (x, y)

                # --- FEKETE FŐBÁBUK (y == 0) ---
                if y == 0:
                    if x in (0, 7):
                        babu = copy.deepcopy(self.bastya)
                    elif x in (1, 6):
                        babu = copy.deepcopy(self.huszar)
                    elif x in (2, 5):
                        babu = copy.deepcopy(self.futo)
                    elif x == 3:
                        babu = copy.deepcopy(self.vezer)
                    elif x == 4:
                        babu = copy.deepcopy(self.kiraly)
                    else:
                        # Pyright kedvéért, bár ide sosem jut el
                        sor.append(uj_mezo)
                        continue

                    babu.szin = "Fekete"
                    babu.koordinatak[-1] = (x, y)
                    sor.append(babu)
                    continue

                # --- FEKETE GYALOGOK (y == 1) ---
                if y == 1:
                    babu = copy.deepcopy(self.gyalog)
                    babu.szin = "Fekete"
                    babu.koordinatak[-1] = (x, y)
                    sor.append(babu)
                    continue

                # --- FEHÉR GYALOGOK (y == 6) ---
                if y == 6:
                    babu = copy.deepcopy(self.gyalog)
                    babu.szin = "Fehér"
                    babu.koordinatak[-1] = (x, y)
                    sor.append(babu)
                    continue

                # --- FEHÉR FŐBÁBUK (y == 7) ---
                if y == 7:
                    if x in (0, 7):
                        babu = copy.deepcopy(self.bastya)
                    elif x in (1, 6):
                        babu = copy.deepcopy(self.huszar)
                    elif x in (2, 5):
                        babu = copy.deepcopy(self.futo)
                    elif x == 3:
                        babu = copy.deepcopy(self.vezer)
                    elif x == 4:
                        babu = copy.deepcopy(self.kiraly)
                    else:
                        sor.append(uj_mezo)
                        continue

                    babu.szin = "Fehér"
                    babu.koordinatak[-1] = (x, y)
                    sor.append(babu)
                    continue

                # --- ÜRES MEZŐ ---
                sor.append(uj_mezo)

            self.tabla.append(sor)

    def valid(self, adat: tuple[int, int] | None) -> TypeGuard[tuple[int, int]]:
        return adat is not None

    def _uresit_mezo(self, x: int, y: int) -> None:
        """Segédfüggvény egy mező kiürítésére."""
        uj_ures = self.mezo() if callable(self.mezo) else self.mezo
        self.tabla[y][x] = uj_ures
        if hasattr(self.tabla[y][x], "koordinatak"):
            self.tabla[y][x].koordinatak = [(x, y)]

    def _mozgat_babu(self, honnan: tuple[int, int], hova: tuple[int, int]) -> None:
        """Segédfüggvény egy figura áthelyezésére és a régi hely kiürítésére."""
        x1, y1 = honnan
        x2, y2 = hova

        # Áttesszük a figurát a célmezőre
        self.tabla[y2][x2] = self.tabla[y1][x1]
        if hasattr(self.tabla[y2][x2], "koordinatak"):
            self.tabla[y2][x2].koordinatak.append((x2, y2))

        # A startmezőt kiürítjük
        self._uresit_mezo(x1, y1)

    def tablamodosit(self) -> None:
        if not self.lepesek:
            return

        utolso = self.lepesek[-1]
        muvelet = utolso.muvelet

        honnan1 = utolso.honnan1
        hova1 = utolso.hova1
        levett_babu_koord = utolso.levett_babukoordinataja
        honnan2 = utolso.honnan2
        hova2 = utolso.hova2
        atvaltozott_babu_tipusa = utolso.atvaltozott_babu_tipusa
        babuszin = utolso.babuszin
        uj_babu: Any | None = None
        match muvelet:

            case "lepes" | "utes":
                if self.valid(honnan1) and self.valid(hova1):
                    self._mozgat_babu(honnan1, hova1)

            case "enpassant":
                if (
                    self.valid(honnan1)
                    and self.valid(hova1)
                    and self.valid(levett_babu_koord)
                ):
                    self._uresit_mezo(*levett_babu_koord)
                    self._mozgat_babu(honnan1, hova1)

            case "sanc":
                if (
                    self.valid(honnan1)
                    and self.valid(hova1)
                    and self.valid(honnan2)
                    and self.valid(hova2)
                ):
                    self._mozgat_babu(honnan1, hova1)
                    self._mozgat_babu(honnan2, hova2)

            case _:
                print(f"Ismeretlen művelet: {muvelet}")

        # -------------------------
        # Gyalog átváltozás (javított)
        # -------------------------
        if atvaltozott_babu_tipusa is not None and self.valid(hova1):
            x, y = hova1

            # Ugyanaz a minta, mint a kezdőtáblánál: deepcopy prototípus báburól
            if atvaltozott_babu_tipusa == "Vezér":
                uj_babu = copy.deepcopy(self.vezer)
            elif atvaltozott_babu_tipusa == "Bástya":
                uj_babu = copy.deepcopy(self.bastya)
            elif atvaltozott_babu_tipusa == "Huszár":
                uj_babu = copy.deepcopy(self.huszar)
            elif atvaltozott_babu_tipusa == "Futó":
                uj_babu = copy.deepcopy(self.futo)

            if uj_babu is None:
                raise ValueError(
                    f"Ismeretlen átváltozási bábutípus: {atvaltozott_babu_tipusa}"
                )

            uj_babu.szin = babuszin
            uj_babu.koordinatak = [(x, y)]

            # A gyalog helyére kerül az új bábu
            self.tabla[y][x] = uj_babu

    def lepes_mentes(self, adat_objektum) -> None:
        self.lepesek.append(adat_objektum)

    def bentvane(self, koordinata) -> bool:
        x, y = koordinata
        return 0 <= x <= 7 and 0 <= y <= 7

    def urese(self, koordinata) -> bool:
        x, y = koordinata
        return self.tabla[y][x].nev == "nincs"

    def tablakiirat(self) -> None:
        # Unicode sakkfigurák (mindegyik pontosan 1 karakter széles)
        szotar = {
            "Gyalog": {"Fehér": "♙", "Fekete": "♟"},
            "Bástya": {"Fehér": "♖", "Fekete": "♜"},
            "Huszár": {"Fehér": "♘", "Fekete": "♞"},
            "Futó": {"Fehér": "♗", "Fekete": "♝"},
            "Vezér": {"Fehér": "♕", "Fekete": "♛"},
            "Király": {"Fehér": "♔", "Fekete": "♚"},
            "nincs": {"Fehér": " ", "Fekete": " "},
        }

        # ANSI színkódok a terminálhoz
        FEKETE_SZIN = "\033[93m"  # Élénksárga/Arany a sötét bábuknak, hogy jól látszódjanak a fekete háttéren
        ALAP_SZIN = "\033[0m"  # Színezés alaphelyzetbe állítása

        elvalaszto = "  +" + "---+" * 8
        print(elvalaszto)

        for idx, j in enumerate(self.tabla):
            sor_szam = len(self.tabla) - idx
            sor_szoveg = f"{sor_szam} |"

            for i in j:
                if i.nev == "nincs":
                    sor_szoveg += "   |"
                else:
                    babu = szotar[i.nev][i.szin]
                    if i.szin == "Fekete":
                        # Csak a karaktert színezzük ki, a szóközök mérete változatlan marad
                        sor_szoveg += f" {FEKETE_SZIN}{babu}{ALAP_SZIN} |"
                    else:
                        sor_szoveg += f" {babu} |"

            print(sor_szoveg)
            print(elvalaszto)

        print("    A   B   C   D   E   F   G   H  ")

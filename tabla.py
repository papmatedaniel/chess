import copy
from dataclasses import dataclass


@dataclass
class Lepestipusok:
    muvelet : str
    honnan1 : tuple[int, int] | None = None
    hova1 : tuple[int, int] | None = None
    babutipus1 : str | None = None
    babuszin : str | None = None
    levett_babutipus : str | None = None
    levett_babukoordinataja : tuple[int, int] | None = None
    atvaltozott_babu_tipusa : str | None = None
    sanctipus : str | None = None
    babutipus2 : str | None = None
    honnan2 : tuple[int, int] | None = None
    hova2 : tuple[int, int] | None = None

class Tabla:

    def __init__(self, *, mezo, gyalog, huszar, futo, bastya, vezer, kiraly) -> None:
        self.mezo = mezo
        self.gyalog = gyalog
        self.huszar = huszar
        self.futo = futo
        self.bastya = bastya
        self.vezer = vezer
        self.kiraly = kiraly

        self.tabla = []  
        self.lepesek : list[Lepestipusok] = []

        
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

        



    def tablamodosit(self, honnan, hova,  muvelet, levettbabukoordinataja=(0,0)) -> None:
        """Művelet alatt ütés, csere, uj babu értendő"""
        x1,y1 = honnan
        x2,y2 = hova
        if muvelet == "csere":
            self.tabla[y1][x1], self.tabla[y2][x2] = self.tabla[y2][x2], self.tabla[y1][x1]
            self.tabla[y1][x1].koordinatak.append((x1, y1))
            self.tabla[y2][x2].koordinatak.append((x2, y2))

        if muvelet == "utes":
            self.tabla[y2][x2] = self.tabla[y1][x1]
            self.tabla[y2][x2].koordinatak.append((x2, y2))
            self.tabla[y1][x1] = self.mezo
            self.tabla[y1][x1].koordinatak.append((x1, x2))

        if muvelet == "enpassant":
            self.tabla[y1][x1], self.tabla[y2][x2] = self.tabla[y2][x2], self.tabla[y1][x1]
            self.tabla[y1][x1].koordinatak.append((x1, y1))
            self.tabla[y2][x2].koordinatak.append((x2, y2))
            x3, y3 = levettbabukoordinataja
            self.tabla[y3][x3] = self.mezo



    def lepes_mentes(self, adat_objektum) -> None:
        self.lepesek.append(adat_objektum)


    def bentvane(self, koordinata) -> bool: 
        x, y = koordinata
        return 0 <= x <= 7 and 0 <= y <= 7

    def urese(self, koordinata) -> bool:
        x,y = koordinata
        return self.tabla[y][x].nev == "nincs"

    def tablakiirat(self) -> None:
        # Unicode sakkfigurák (mindegyik pontosan 1 karakter széles)
        szotar = {
            "Gyalog":  {"Fehér": "♙", "Fekete": "♟"},
            "Bástya":  {"Fehér": "♖", "Fekete": "♜"},
            "Huszár":  {"Fehér": "♘", "Fekete": "♞"},
            "Futó":    {"Fehér": "♗", "Fekete": "♝"},
            "Vezér":   {"Fehér": "♕", "Fekete": "♛"},
            "Király":  {"Fehér": "♔", "Fekete": "♚"},
            "nincs":   {"Fehér": " ", "Fekete": " "}
        }
        
        # ANSI színkódok a terminálhoz
        FEKETE_SZIN = "\033[93m"  # Élénksárga/Arany a sötét bábuknak, hogy jól látszódjanak a fekete háttéren
        ALAP_SZIN = "\033[0m"     # Színezés alaphelyzetbe állítása
        
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

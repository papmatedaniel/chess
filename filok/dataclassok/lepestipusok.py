# filok/dataclassok/lepestipusok.py
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


@dataclass(frozen=True, slots=True)
class Pozicio:
    sor: int  # y index a mátrixban (0..7)
    oszlop: int  # x index a mátrixban (0..7)

    def palyan_van(self) -> bool:
        """Ellenőrzi, hogy a pozíció a 8x8-as sakktáblán belül van-e."""
        return 0 <= self.sor < 8 and 0 <= self.oszlop < 8


class LepesTipus(Enum):
    SIMA = auto()  # Normál lépés üres mezőre
    UTES = auto()  # Ellenfél bábujának leütése
    SANC = auto()  # Kiskirály- vagy nagykirály-sánc
    EN_PASSANT = auto()  # Menet közbeni ütés
    ATVALTOZAS = auto()  # Gyalog átváltozása üres mezőre lépve
    ATVALTOZAS_UTESSEL = auto()  # Gyalog átváltozása ütéssel egybekötve


@dataclass(frozen=True, slots=True)
class Lepes:
    tipus: LepesTipus
    honnan: Pozicio
    hova: Pozicio

    # Sáncolás esetén a bástya koordinátái
    bastya_honnan: Pozicio | None = None
    bastya_hova: Pozicio | None = None

    # Ütés és En Passant esetén (a visszavonáshoz/naplózáshoz a levett bábu példánya és pontos helye)
    levett_babu: Any | None = None
    levett_babu_pozicio: Pozicio | None = None

    # Gyalog átváltozása esetén a választott bábutípus neve ("Vezér", "Bástya", stb.)
    uj_babu_tipus: str | None = None

from dataclasses import dataclass

from filok.dataclassok.lepestipusok import Lepes


@dataclass
class LepesEredmeny:
    siker: bool
    uzenet: str
    objektum: Lepes | None

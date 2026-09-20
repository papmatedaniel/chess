from dataclasses import dataclass

from chess.dataclassok.lepestipusok import Lepes


@dataclass(slots=True)
class LepesEredmeny:
    siker: bool
    uzenet: str
    objektum: Lepes | None = None

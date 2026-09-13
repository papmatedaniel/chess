from dataclasses import dataclass
from filok.dataclassok import lepestipusok


@dataclass
class LepesEredmeny:
    siker: bool
    uzenet: str
    objektum: lepestipusok.Lepestipusok | None

from dataclasses import dataclass


@dataclass
class Lepestipusok:
    muvelet: str
    honnan1: tuple[int, int] | None = None
    hova1: tuple[int, int] | None = None
    babutipus1: str | None = None
    babuszin: str | None = None
    levett_babutipus: str | None = None
    levett_babukoordinataja: tuple[int, int] | None = None
    atvaltozott_babu_tipusa: str | None = None
    sanctipus: str | None = None
    honnan2: tuple[int, int] | None = None
    hova2: tuple[int, int] | None = None
    babutipus2: str | None = None

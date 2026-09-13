from dataclasses import dataclass
from typing import ClassVar


# mehet egybe a sáncszabaly fileval
@dataclass
class Sanc:
    kiraly_honnan = 4
    babu1: ClassVar[str] = "Bástya"
    babu2: ClassVar[str] = "Király"
    sancvalaszto: ClassVar[dict] = {
        "0-0": {
            "kiraly_hova": 6,
            "bastya_honnan": 7,
            "bastya_hova": 5,
        },
        "0-0-0": {
            "kiraly_hova": 2,
            "bastya_honnan": 0,
            "bastya_hova": 3,
        },
    }

    szinek: ClassVar[dict] = {"Fehér": 7, "Fekete": 0}

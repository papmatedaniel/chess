from typing import ClassVar


class Sanc:
    kiraly_honnan: int = 4
    babu1: str = "Bástya"
    babu2: str = "Király"
    szinek: ClassVar[dict[str, int]] = {"Fehér": 7, "Fekete": 0}

    sancvalaszto: ClassVar[dict[str, dict[str, int]]] = {
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

from chess.babuk.bastya import Bastya
from chess.babuk.futo import Futo
from chess.babuk.gyalog import Gyalog
from chess.babuk.huszar import Huszar
from chess.babuk.kiraly import Kiraly
from chess.babuk.ures import UresMezo
from chess.babuk.vezer import Vezer
from chess.jatek import Jatek
from chess.tabla import Tabla


def main() -> None:
    ures = UresMezo()
    gyalog = Gyalog()
    huszar = Huszar()
    bastya = Bastya()
    futo = Futo()
    vezer = Vezer()
    kiraly = Kiraly()

    tabla = Tabla(
        mezo=ures,
        gyalog=gyalog,
        huszar=huszar,
        futo=futo,
        bastya=bastya,
        vezer=vezer,
        kiraly=kiraly,
    )

    jatek = Jatek(tabla)
    jatek.jatekmenet()


if __name__ == "__main__":
    main()
# ctrl shift  b elinditja a terminalt

from filok.babuk.bastya import Bastya
from filok.babuk.futo import Futo
from filok.babuk.gyalog import Gyalog
from filok.babuk.huszar import Huszar
from filok.babuk.kiraly import Kiraly
from filok.babuk.ures import UresMezo
from filok.babuk.vezer import Vezer
from filok.dataclassok.lepestipusok import Lepestipusok
from filok.jatek import Jatek
from filok.tabla import Tabla

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
lepestipus = Lepestipusok
jatek = Jatek(tabla, lepestipus)
jatek.jatekmenet()

# ctrl shift  b elinditja a terminalt

from filok.bastya import Bastya
from filok.futo import Futo
from filok.gyalog import Gyalog
from filok.huszar import Huszar
from filok.jatek import Jatek
from filok.kiraly import Kiraly
from filok.lepestipusok import Lepestipusok
from filok.tabla import Tabla
from filok.ures import UresMezo
from filok.vezer import Vezer

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

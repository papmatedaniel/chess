
from bastya import Bastya
from futo import Futo
from gyalog import Gyalog
from huszar import Huszar
from jatek import Jatek
from tabla import Lepestipusok, Tabla
from ures import UresMezo
from vezer import Vezer

ures = UresMezo()
gyalog = Gyalog()
huszar =  Huszar()
bastya = Bastya()
futo = Futo()
vezer = Vezer()
tabla = Tabla(mezo=ures, gyalog=gyalog, huszar=huszar, futo=futo, bastya=bastya, vezer=vezer)
lepestipus = Lepestipusok
jatek = Jatek(tabla, lepestipus)
jatek.jatekmenet()
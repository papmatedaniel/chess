
from jatek import  Jatek
from tabla import Tabla, Lepestipusok
from gyalog import Gyalog
from ures import UresMezo
from huszar import Huszar
from bastya import Bastya
from futo import Futo
from vezer import Vezer


ures = UresMezo("nincs", "nincs", (-1,-1))
gyalog = Gyalog("nincs", "Gyalog", (-1, -1), None)
huszar =  Huszar("nincs", "Huszár", (-1,-1), None)
bastya = Bastya("nincs", "Bástya", (-1,-1), None)
futo = Futo("nincs", "Futó", (-1,-1), None)
vezer = Vezer("nincs", "Vezér", (-1,-1), None)
tabla = Tabla(ures, gyalog, huszar, bastya, futo, vezer)
lepestipus = Lepestipusok
jatek = Jatek(tabla, lepestipus)
jatek.jatekmenet()
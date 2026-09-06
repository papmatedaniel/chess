from filok.lepeseredmeny import LepesEredmeny


class Szabaly:
    def __init__(self, tabla, lepestipusok, sajatszin) -> None:
        self.lepestipusok = lepestipusok
        self.tabla = tabla
        self.sajatszin = sajatszin

    def lepes_ellenorzo(self, kezdokoordinata, vegkoordinata) -> LepesEredmeny:
        if self.tabla.urese(kezdokoordinata):
            return LepesEredmeny(False, "A kezdő koordinátán nincs bábu")
        if not self.tabla.bentvane(kezdokoordinata):
            return LepesEredmeny(False, "A kezdő koordináta a pályán kívül van")

        if not self.tabla.bentvane(vegkoordinata):
            return LepesEredmeny(False, "A célkoordináta a pályán kívül van")

        x, y = kezdokoordinata
        if (
            not self.tabla.urese(kezdokoordinata)
            and self.sajatszin != self.tabla.tabla[y][x].szin
        ):
            return LepesEredmeny(False, "Az ellenfél bábujához nyúltál")

        return LepesEredmeny(True, "Minden feltétel megfelel")

    def nemlepett(self) -> bool:
        return len(self.tabla.lepesek) == 0

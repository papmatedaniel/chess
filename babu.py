
class Babu:
    """Tartalmazza a bábu tulajdonságait"""
    def __init__(self, szin, nev, jelenlegi_koordinata, el_e):
        self.szin = szin
        self.nev = nev
        self.koordinatak = [jelenlegi_koordinata]
        self.el_e = el_e
        self.szinek = {
            "Fehér" : -1,
            "Fekete" : 1
        }

    def hozzad(self, lepesek):
        x1, y1 = self.koordinatak[-1]
        return [(x1+x2, y1+y2) for x2, y2 in lepesek]

    def lepes_hozzad(self, lepesek):
        x, y = self.koordinatak[-1]
        folista = []
        for x1, y1 in lepesek:
            allista = []
            aktualisx, akutalisy = (x, y)
            for _ in range(8):
                aktualisx += x1
                akutalisy += y1
                allista.append((aktualisx, akutalisy))
            folista.append(allista)

        return folista

    def ortogonalis_lepes(self):
        """Vizszintes és függőleges"""
        lepesek = [(0,1), (1,0), (-1, 0), (0,-1)]
        return self.lepes_hozzad(lepesek)

    def diagonalis_lepes(self):
        """Átlós"""
        lepesek = [(1,1), (1,-1), (-1, -1), (-1,1)]
        return self.lepes_hozzad(lepesek)

    def lepes(self):
        pass

    def __getattr__(self, name):
        if name == 'utes':
            return self.lepes
        
        raise AttributeError(f"'{type(self).__name__}' objektumnak nincs '{name}' attribútuma")

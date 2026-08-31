from babu import Babu


class Gyalog(Babu):
    """Tartalmazza a gyalog tulajdonságait, metódusait."""
 
    def __init__(self, szin, nev, jelenlegi_koordinata, el_e):
        super().__init__(szin, nev, jelenlegi_koordinata, el_e)


    def utes(self):
        """Hagyományos ütést"""
        lepesek = [(self.szinek[self.szin], self.szinek[self.szin]), (-self.szinek[self.szin], self.szinek[self.szin])]
        return self.hozzad(lepesek)

    def lepes(self):
        """Hagyományos lépés"""
        lepesek = [(0,  self.szinek[self.szin])]
        return self.hozzad(lepesek)

    def elso_lepes(self):
        """Első lépés, ami lehet dupla is"""
        lepesek = [(0,  self.szinek[self.szin]), (0, 2 * self.szinek[self.szin])]
        return self.hozzad(lepesek)


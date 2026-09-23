# Sakk Motor & Játék (Tanuló Projekt)

Egy objektumorientált elvekre (OOP) épülő sakk motor és szimulációs keretrendszer Pythonban. A projekt célja a tiszta kód alapelveinek, a felelősségi körök szétválasztásának (Single Responsibility Principle) és a hatékony állapotszimulációnak a gyakorlati elsajátítása volt.

---

## 1. Fejlesztési történet és mérföldkövek

A fejlesztés lépésről lépésre, iteratív módon történt az alábbi fázisokban:

1. **Alapok és a legösszetettebb gyaloglogika:**
   - A sakktábla generálása és az alapvető mezőkezelés kialakítása.
   - `Gyalog` osztály létrehozása: előrelépés, ütések megvalósítása.
   - Az *en passant* (menet közbeni ütés) szabály lefejlesztése, amely megkövetelte az előzmények (lépéstörténet) bevezetését.

2. **További figurák implementálása:**
   - A többi bábu lépéslogikájának fokozatos hozzáadása: `Király` $\rightarrow$ `Huszár` $\rightarrow$ `Bástya` $\rightarrow$ `Futó` $\rightarrow$ `Vezér`.
   - Lokális kétjátékos mód életre hívása és a gyalogátváltozás (*promotion*) kezelése.

3. **Speciális szabályok és szabályrendszer szétválasztása:**
   - A bábuk alapszintű lépéseinek elkülönítése a speciális játékhelyzetektől.
   - Dedikált segédosztályok bevezetése:
     - Király sakk- és mattvizsgálata
     - Sáncolás (kis- és nagysánc) ellenőrzése
     - Gyalogkezelő logika

4. **Adatmodellezés és állapotmentés:**
   - Python `dataclass` struktúrák bevezetése a lépések és állapotok tiszta, típusbiztos tárolására.

5. **Szimuláció és teljesítményoptimalizálás:**
   - Sakkvizsgálat és lépéselemzés megvalósítása költséges táblamásolások (`deepcopy`) nélkül, helyette egyetlen táblán történő lépés- és visszavonás (*make move / unmake move*) logikával.

6. **Refaktorálás és mappa-architektúra:**
   - Moduláris projektstruktúra kialakítása, rétegek logikai szétválasztása.

---

## 2. Mesterséges Intelligencia (AI) Használatának Dokumentációja

A projekt során az AI-t nem kódgeneráló feketedobozként, hanem **architektúrális mentorként, refaktorálási eszközként és konzultációs partnerként** alkalmaztam.

### Főbb tervezési döntések és koncepciók (AI konzultáció alapján)

* **OOP alapelvek és felelősségi körök (SRP):**
  - Az ellenőrzés (validálás), az állapotmódosítás (végrehajtás) és a játékvezérlés szétválasztása külön osztályokba.
  - Öröklődés tudatos alkalmazása kompozícióval szemben (mikor indokolt az alosztályképzés és mikor elegendő az interfész/viselkedés átadása).
* **Függőségek kezelése (Dependency Injection):**
  - Megtanult szabály: a statikus konfigurációt nem injektáljuk; a futásidejű függőségeket és állapotokat injektáljuk az osztályokba.
* **Körkörös függőségek (`circular imports`) feloldása:**
  - Hídosztályok (Bridge pattern) és közvetítő rétegek bevezetése a tábla, a játékvezérlő és a figurák közötti oda-vissza hivatkozások megszüntetésére.
* **Konstruktor vs. egyéb metódusok:**
  - Adatátadási stratégiák tisztázása: mikor inicializáljon a konstruktor, és mikor érdemes állapotbeállító metódusokat (pl. `setup`, `load_state`) használni.
* **Adatreprezentáció (`dataclass`):**
  - Tiszta adatkonténerek használata üzleti logika nélküli struktúrákhoz (különösen a lépések, koordináták és előzmények rögzítésére).
* **Szimuláció optimalizációja:**
  - `copy.deepcopy(tabla)` elvetése a magas memóriaterhelés és lassulás miatt; helyette reverzibilis műveletek (`lepes_vegrehajtas` és `lepes_visszavonas`) kialakítása ugyanazon a táblapéldányon.
* **Üres mező támadottságának vizsgálata:**
  - Mivel az üres mező nem rendelkezik saját ütéslogikával, az AI segítségével dolgoztuk ki a stratégiát: ideiglenes tesztfigura (átmeneti király) elhelyezése vagy a támadott mezők kiszervezése külön logikai rétegbe.

---

### Érintett komponensek és modulok

Az alábbi táblázat pontosan összefoglalja, mely forrásfájlokban milyen mértékben vett részt az AI:

| Fájl | Érintett függvények / osztályok | Feladat jellege | Saját hozzáadott érték és ellenőrzés |
| :--- | :--- | :--- | :--- |
| `tabla.py` | `tablageneralas`, `mezo_lekerdezes`, `mezo_beallitasa`, `_uresit_mezo`, `_mozgat_babu`, `_uj_babu_letrehozasa`, `lepes_vegrehajtas`, `_visszamozgat_babu`, `lepes_visszavonas`, `tablakiirat` | Refaktorálás, kódstrukturálás, output egységesítés | Logikai láncolat felépítése, táblaindexelési konvenciók ellenőrzése és integrálása a játékmenetbe. |
| `jatek.py` | `lepesek` | Refaktorálás, lépésvalidáció tisztítása | Szabályok sorrendiségének felügyelete, hibakeresés peremesetekre. |
| `kiraly_sakkezeles.py` | `kiraly_sakkban_vane` | Algoritmus és refaktorálás | Ideiglenes király használatának ötlete és tesztelése speciális sáncolási és blokkolási szituációkban. |
| `gyalog_lepes.py` | `gyalog_atvaltozhat_e` | Kódgenerálás és refaktorálás | Integrálás a lépésfolyamba és a felhasználói bábuválasztás logikájába. |
| `lepestipusok.py` | Teljes fájl | `dataclass` adatreprezentáció | Adatstruktúra definiálása a lépésvisszavonáshoz és előzménykezeléshez szükséges mezőkkel. |


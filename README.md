# ♟️ Terminal Chess Engine

Egy teljesen moduláris, tiszta architektúrájú konzolos sakkmotor Pythonban. A projekt a **SOLID tervezési elveket**, a modern **`src/` layout** csomagstruktúrát és a szigorú típusbiztonságot (`MyPy`, `Pyright`, `Ruff`) követi külső futásidejű függőségek nélkül.

---

## 📋 Tartalomjegyzék

* [Funkciók](https://www.google.com/search?q=%2523-funkci%25C3%25B3k&utm_source=gemini)
* [Architektúra és Tervezési Minták](https://www.google.com/search?q=%2523-architekt%25C3%25BAra-%25C3%25A9s-tervez%25C3%25A9si-mint%25C3%25A1k&utm_source=gemini)
* [Projektstruktúra](https://www.google.com/search?q=%2523-projektstrukt%25C3%25BAra&utm_source=gemini)
* [Telepítés és Futtatás](https://www.google.com/search?q=%2523-telep%25C3%25ADt%25C3%25A9s-%25C3%25A9s-futtat%25C3%25A1s&utm_source=gemini)
* [Játékmenet és Kezelés](https://www.google.com/search?q=%2523-j%25C3%25A1t%25C3%25A9kmenet-%25C3%25A9s-kezel%25C3%25A9s&utm_source=gemini)
* [Fejlesztés és Minőségellenőrzés](https://www.google.com/search?q=%2523-fejleszt%25C3%25A9s-%25C3%25A9s-min%25C5%2591s%25C3%25A9gellen%25C5%2591rz%25C3%25A9s&utm_source=gemini)

---

## ✨ Funkciók

* **Teljes FIDE sakk-szabályrendszer implementáció:**
* Hagyományos bábuk mozgása és ütése (Gyalog, Bástya, Huszár, Futó, Vezér, Király).
* Gyalog duplalépés a kezdőpozícióból.
* Menet közbeni ütés (**En Passant**) lépéstörténet-alapú érvényesítéssel.
* Kis- és nagysánc (**0-0**, **0-0-0**) mező-ellenőrzéssel és támadott vonalak vizsgálatával.
* Gyalogátváltozás (**Promotion**) konzolos választással (Vezér, Bástya, Huszár, Futó).


* **Tranzakciós játékmotor:**
* Lépés-visszavonási (Rollback / Undo) mechanizmus a szabályos lépések felderítéséhez.
* Király sakkban maradásának szimulációs vizsgálata.
* Automatikus állapotfelismerés: **Sakk**, **Sakk-matt** és **Patt (döntetlen)**.


* **Letisztult CLI megjelenítés:**
* Standard algebrai koordináták (`a1`–`h8`).
* Unicode sakkfigurák és ANSI színkiemelés.



---

## 🏛️ Architektúra és Tervezési Minták

1. **Dependency Injection (Függőség-befecskendezés):**
Az osztályok nem maguk példányosítják a függőségeiket. A geometriai szabályok (`Altalanosszabalyok`), a figuramozgások (`BabuSzabaly`), a táblaállapot (`Tabla`) és az ellenőrzések (`Sakkkezeles`) kívülről, rétegezve kerülnek átadásra.
2. **Prototype Pattern (Prototípus minta):**
A `Tabla` osztály a kezdőállás generálásakor és a gyalogátváltozáskor előre konfigurált bábupéldányokból klónoz (`copy.deepcopy`), így a táblamodell teljesen független a konkrét bábuosztályoktól.
3. **Unit of Work & Rollback (Tranzakciókezelés):**
A szimulációs lépéstesztelő (`lepes_tesztelo`) ideiglenesen végrehajtja a lépést, kiértékeli a király biztonságát, majd mellékhatásmentesen visszaállítja az eredeti állapotot és a bábutörténetet.
4. **Immutabilitás (Megváltoztathatatlanság):**
A `Pozicio` koordináták `@dataclass(frozen=True, slots=True)` formában rögzítettek, hash-elhetők, így megbízható kulcsokként használhatók szótárakban és halmazokban.
5. **Separation of Concerns (Felelősségek szétválasztása):**
A játéklogika, a mezőgeometria és a konzolos I/O (`input()`, `print()`) szigorúan el van különítve.

---

## 📂 Projektstruktúra

```text
chess/
├── .gitignore
├── .python-version
├── pyproject.toml
├── README.md
├── uv.lock
└── src/
    └── chess/
        ├── __init__.py
        ├── main.py                     # Belépési pont (CLI entrypoint)
        ├── jatek.py                    # Játékmenet és I/O vezérlő
        ├── tabla.py                    # Mátrixkezelés, lépésvégrehajtás és rollback
        ├── alltalanosszabalyok.py       # Geometriai és sugárirányú mezővizsgálatok
        ├── babuszabaly.py              # Szabálydiszpécser figuratípusok szerint
        ├── szimulacio.py               # Legális lépések és matt/patt kalkulátor
        ├── babuk/                      # Figuradefiníciók (polimorf eltolások)
        │   ├── babu.py                 # Absztrakt ősosztály
        │   ├── bastya.py
        │   ├── futo.py
        │   ├── gyalog.py
        │   ├── huszar.py
        │   ├── kiraly.py
        │   ├── ures.py
        │   └── vezer.py
        ├── dataclassok/                # Adatmodellek és konfigurációk
        │   ├── lepeseredmeny.py
        │   ├── lepestipusok.py         # Pozicio, Lepes, LepesTipus
        │   └── sanc.py
        └── specialis_muveletek/        # Komplex sakklogikai szervizek
            ├── gyalog_lepes.py         # En passant és kettős lépés logika
            ├── kiraly_sakkezeles.py    # Inverz sugárpásztázás sakkvizsgálathoz
            └── sancszabaly.py          # Sáncolási előfeltételek ellenőrzése

```

---

## 🚀 Telepítés és Futtatás

A játék futtatásához legalább **Python 3.12** szükséges. Válassz az alábbi módszerek közül:

### 1. Futtatás letöltés nélkül (Ajánlott játékosoknak)

Ha rendelkezel [`uv`](https://docs.astral.sh/uv/?utm_source=gemini) vagy [`pipx`](https://www.google.com/search?q=https://pypa.github.io/pipx/&utm_source=gemini) eszközzel, a repó klónozása nélkül, egyetlen paranccsal elindíthatod a játékot egy izolált sandbox környezetből:

**`uvx` használatával:**

```bash
uvx git+https://github.com/FELHASZNALONEV/chess.git

```

**`pipx` használatával:**

```bash
pipx run --spec git+https://github.com/FELHASZNALONEV/chess.git chess

```

---

### 2. Fejlesztői környezet `uv`-val (Ajánlott)

1. **Klónozd a tárolót:**
```bash
git clone https://github.com/FELHASZNALONEV/chess.git
cd chess

```


2. **Futtatás:**
```bash
uv run chess

```


*(Az `uv` automatikusan felépíti a `.venv` környezetet a lockfile alapján, és elindítja a játékot.)*

---

### 3. Hagyományos környezet (`git` + `pip`)

1. **Klónozd a tárolót:**
```bash
git clone https://github.com/FELHASZNALONEV/chess.git
cd chess

```


2. **Virtuális környezet létrehozása és aktiválása:**
* **Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate

```


* **Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1

```




3. **Telepítés szerkeszthető (editable) módban:**
```bash
pip install -e .

```


4. **Indítás:**
```bash
chess

```



---

## 🎮 Játékmenet és Kezelés

A játék körökre osztva fut a terminálban. A lépéseket standard algebrai formátumban kell megadni szóközökkel elválasztva:

* **Normál lépés és ütés:** `honnan hova`
```text
Lépés (pl. e2 e4) vagy sánc (0-0 / 0-0-0): e2 e4
Lépés (pl. e2 e4) vagy sánc (0-0 / 0-0-0): b1 c3

```


* **Kiskirálysánc (Rövid sánc):**
```text
Lépés (pl. e2 e4) vagy sánc (0-0 / 0-0-0): 0-0

```


* **Nagykirálysánc (Hosszú sánc):**
```text
Lépés (pl. e2 e4) vagy sánc (0-0 / 0-0-0): 0-0-0

```


* **Gyalogátváltozás:**
Ha egy gyalog eléri a túlsó alapsort, a terminál bekéri a kívánt tiszt kódját:
```text
Milyen bábuvá változnál? (V, B, H, F): v

```


* **Kilépés:**
A játék bármikor megszakítható a `Ctrl + C` billentyűkombinációval.

---

## 🛠️ Fejlesztés és Minőségellenőrzés

A projekt szigorú statikus ellenőrzést használ. A fejlesztői függőségek telepítése:

```bash
uv sync --group dev

```

### Formázás és Linting (Ruff)

```bash
uv run ruff check .
uv run ruff format --check .

```

### Típusellenőrzés (Pyright & MyPy)

```bash
uv run pyright
uv run mypy src

```
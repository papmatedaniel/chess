# Telepítés és Futtatás

A sakkmotor futtatásához legalább **Python 3.12** szükséges. Válassz az alábbi három módszer közül a céljaidnak megfelelően:

---

## 1. Módszer: Futtatás letöltés nélkül (Egyszeri játékhoz)

Ha rendelkezel [`uv`](https://docs.astral.sh/uv/?utm_source=gemini) vagy [`pipx`](https://www.google.com/search?q=https://pypa.github.io/pipx/&utm_source=gemini) eszközzel, nem szükséges a tárolót klónoznod vagy a gépedet konfigurálnod. Egyetlen paranccsal elindíthatod a játékot egy izolált sandbox környezetből:

### `uvx` használatával (Ajánlott):

```bash
uvx git+https://github.com/papmatedaniel/chess.git

```

### vagy `pipx` használatával:

```bash
pipx run --spec git+https://github.com/papmatedaniel/chess.git chess

```

---

## 2. Módszer: Futtatás `uv`-val (Fejlesztéshez)

Ha klónozni szeretnéd a projektet, vagy módosítanád a forráskódot:

1. **Klónozd a tárolót:**
```bash
git clone https://github.com/papmatedaniel/chess.git
cd chess

```


2. **Indítsd el a játékot közvetlenül:**
```bash
uv run chess

```


*(Az `uv` automatikusan létrehozza a `.venv` környezetet az `uv.lock` alapján, telepíti a belső csomagot, és elindítja a sakktáblát.)*

---

## 3. Módszer: Hagyományos telepítés (`git` + `pip`)

Ha nem használsz `uv`-t, a standard beépített Python eszközökkel is elindíthatod a projektet:

1. **Klónozd a tárolót:**
```bash
git clone https://github.com/papmatedaniel/chess.git
cd chess

```


2. **Hozz létre és aktiválj egy virtuális környezetet:**
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




3. **Telepítsd a csomagot szerkeszthető (editable) módban:**
```bash
pip install -e .

```


4. **Indítsd el a játékot a CLI paranccsal:**
```bash
chess

```
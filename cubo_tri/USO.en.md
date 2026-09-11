# `cubo_tri_pontos_intensidade.py` + `cubo_tri_zonas_intensidade.py` — usage guide

Plotter for a 3-axis space **still only of intensity** (extensity is dealt with
in campo_presenca/) for the gradations of a semiotic value space — fiduciary
trust, veridiction, manipulation or competence —, based on the researcher's own
diagrams (U3/U4–U6), supported by Fontanille & Zilberberg, *Tensão e
Significação*, Zilberberg, *Elementos de Semiótica Tensiva* (2011) and
Zilberberg, *Structures Tensives* (2012).

Three files:

- **`espacos.py`** — the **content** (axis gradations, spaces and example
  paths). This is where you edit/create the gradations — see
  [How to edit gradations](#how-to-edit-gradations--create-a-space) below.
- **`cubo_tri_pontos_intensidade.py`** — the `CuboPontosIntensidade` class and
  the "point" factories: the basic one (`pontos_puro`), the four ready-made
  spaces (fiduciary, veridiction, manipulation, competence) and, for each one,
  the `_conversa` versions (the 4 points of the converse diagonal), `_inversa_1`
  and `_inversa_2` (the two inverse diagonals).
- **`cubo_tri_zonas_intensidade.py`** — `CuboZonasIntensidade
  (CuboPontosIntensidade)`, which adds a 4×4×4 grid, highlighted zones (with
  legend) and paths; it imports `CuboPontosIntensidade` from
  `cubo_tri_pontos_intensidade.py`.

## The three axes

| Axis (hand sketch) | Orientation on screen | Editable? |
|---|---|---|
| **Intensity** | vertical, on the **left** | no — always `demenos → menos → mais → demais` |
| **eixo_z** | rises to the **right** | yes — name + 4 gradations (from `–` to `+`) |
| **eixo_x** | descends to the **right** | yes — name + 4 gradations (from `–` to `+`) |

`eixo_x`/`eixo_z` are the axis name and its 4-degree scale; **intensity** is
the same in every space. The four ready-made spaces:

| Space | eixo_x (descends right) | eixo_z (rises right) |
|---|---|---|
| Fiduciary | trust (S/S): não confia nada → confia totalmente | belief (S/O): não crê nada → crê totalmente |
| Veridictory | seem: não parecer nada → parecer muito | be: não ser de forma alguma → ser exatamente |
| Manipulation | want: não querer de forma alguma → querer muito | must: não dever nada → dever muito |
| Competence | can: não poder nada → poder totalmente | know: não saber nada → saber exatamente |

> **Extensity** is present in campo_presenca/, but is not dealt with here.

Internal matplotlib mapping: `x ← eixo_x`, `y ← eixo_z`, `z ← intensity`.

---

## How to edit gradations / create a space

Everything lives in `espacos.py` — the single source of the content. You don't
need to touch the plotters.

- **Edit the gradations of an axis**: change the labels of one of the lists
  (`CONFIANCA`, `CRENCA`, `PARECER`, `SER`, `QUERER`, `DEVER`, `PODER`,
  `SABER`). Always 4 labels, from `–` to `+`.
- **Create a new space**: add an entry to `ESPACOS` in the same format
  (`eixo_x_nome`/`eixo_x_labels` + `eixo_z_nome`/`eixo_z_labels`). The generic
  factories (`pontos`, `pontos_diagonal`, `pontos_percurso`, `zonas_*`) accept
  it automatically.
- **Example paths**: live in `PERCURSOS` (manual paths).

```python
from espacos import ESPACOS, diagonal, kw_espaco

# diagonals derived automatically from the gradations:
diagonal("fiduciario", "conversa")    # 4 zones, ascending intensity order
diagonal("fiduciario", "inversa_1")   # eixo_x descends
diagonal("fiduciario", "inversa_2")   # eixo_z descends

kw_espaco("competencial")             # ready kwargs for any factory
```

For a one-off custom space, you can still pass `eixo_x_nome`/`eixo_x_labels`
and `eixo_z_nome`/`eixo_z_labels` directly to any factory (see
[Common parameters](#common-parameters)).

---

## How to run

The scripts depend on `numpy`, `matplotlib` and `Pillow` (used only to crop the
excess white margin of the PNG after saving — 3D axes without ticks have a
known matplotlib bug with `bbox_inches="tight"`). Each factory returns a
`CuboPontosIntensidade` object (or `CuboZonasIntensidade`, which is a
`CuboPontosIntensidade`); call `.salvar("file.png")` to generate the image.

```python
from cubo_tri_pontos_intensidade import pontos_puro, pontos_fiduciario
from cubo_tri_zonas_intensidade import zonas_zona_completo
pontos_puro().salvar("puro.png")
pontos_fiduciario().salvar("fiducia.png")
```

- Running `python3 cubo_tri_pontos_intensidade.py` generates the "point" cubes
  at once.
- Running `python3 cubo_tri_zonas_intensidade.py` generates the four grid/zone
  versions of the fiduciary space.
- `python3 gerar_exemplos.py` (re)generates **all reference examples**: the
  points in `exemplos/pontos/` (one subfolder per space, plus `pontos_puro.png`
  at the root) and the 16×4 zones in `exemplos/zonas/<space>/`.
- `gerar_zonas.py` and `gerar_percursos.py` are the entry points to generate
  ONE custom figure at a time (`EDITE AQUI` block at the top).

---

## The twenty commands of `cubo_tri_pontos_intensidade.py`

They all accept the same camera/figure parameters via `**kw` (see
[Common parameters](#common-parameters)).

### `pontos_puro()` — the most basic of all
Only the **intensity** labels (the vertical line) and the `+`/`–` symbols; the
other two (editable) axes show **only the 4 divisions**, with no text or title.
Base for the four spaces below.

```python
pontos_puro().salvar("pontos_puro.png")
```

### Fiduciary space (trust × belief)
```python
pontos_fiduciario().salvar("pontos_fiduciario.png")          # three full axes
pontos_fiduciario_conversa().salvar("pontos_fiduciario_conversa.png")  # + converse diagonal
pontos_fiduciario_inversa_1().salvar("pontos_fiduciario_inversa_1.png")  # 1st inverse (trust descends)
pontos_fiduciario_inversa_2().salvar("pontos_fiduciario_inversa_2.png")  # 2nd inverse (belief descends)
pontos_fiduciario_percurso_tres().salvar("pontos_fiduciario_percurso_tres.png")  # 3-point path
```

### Veridictory space (seem × be)
```python
pontos_veridictorio().salvar("pontos_veridictorio.png")
pontos_veridictorio_conversa().salvar("pontos_veridictorio_conversa.png")
pontos_veridictorio_inversa_1().salvar("pontos_veridictorio_inversa_1.png")
pontos_veridictorio_inversa_2().salvar("pontos_veridictorio_inversa_2.png")
pontos_veridictorio_percurso_dois().salvar("pontos_veridictorio_percurso_dois.png")  # 2-point path
```

### Manipulation space (want × must)
```python
pontos_manipulacao().salvar("pontos_manipulacao.png")
pontos_manipulacao_conversa().salvar("pontos_manipulacao_conversa.png")
pontos_manipulacao_inversa_1().salvar("pontos_manipulacao_inversa_1.png")
pontos_manipulacao_inversa_2().salvar("pontos_manipulacao_inversa_2.png")
pontos_manipulacao_percurso_quatro().salvar("pontos_manipulacao_percurso_quatro.png")  # 4-point path
```

### Competence space (can × know)
```python
pontos_competencial().salvar("pontos_competencial.png")
pontos_competencial_conversa().salvar("pontos_competencial_conversa.png")
pontos_competencial_inversa_1().salvar("pontos_competencial_inversa_1.png")
pontos_competencial_inversa_2().salvar("pontos_competencial_inversa_2.png")
pontos_competencial_percurso_dois().salvar("pontos_competencial_percurso_dois.png")  # 2-point path
```

The three diagonals of each space:

- `_conversa` — the three axes rise together.
- `_inversa_1` — **eixo_x descends** while eixo_z and intensity rise.
- `_inversa_2` — **eixo_z descends** while eixo_x and intensity rise.

Each `_conversa`/`_inversa_1`/`_inversa_2` version carries one colored marker
per point, with **dotted guides** to the three axes (see
[How to mark a point](#how-to-mark-a-point)) — it is not a path: no arrow, no
link from one point to another. The `_percurso_*` versions link the points with
an arrow (see `_add_percurso` in the class).

---

## The six commands of `cubo_tri_zonas_intensidade.py`

They all inherit from `CuboPontosIntensidade` (via `CuboZonasIntensidade`). By
default they work in the fiduciary space; for the other spaces, pass
`eixo_x_nome`/`eixo_x_labels` and `eixo_z_nome`/`eixo_z_labels` (the gradations
are in `cubo_tri_pontos_intensidade.py`: `PARECER`/`SER`, `QUERER`/`DEVER`,
`PODER`/`SABER`):

```python
# the same zone cube, now in the competence space (can × know)
from cubo_tri_pontos_intensidade import PODER, SABER
from cubo_tri_zonas_intensidade import zonas_zona_completo
zonas_zona_completo(("saber exatamente", "poder totalmente", "demais"),
                    eixo_x_nome="poder", eixo_x_labels=PODER,
                    eixo_z_nome="saber", eixo_z_labels=SABER).salvar("z.png")
```

### 1. `zonas_grade()` — full 4×4×4 grid
Dashed grid of all the crossings of the 4 zones on each axis.

```python
zonas_grade().salvar("grade.png")
```

### 2. `zonas_faces_parcial()` — grid only on the 3 visible faces
Dashed grid only on the front (`eixo_x × intensity`), on the right side
(`eixo_z × intensity`) and on the top. Cleaner than the full grid.

```python
zonas_faces_parcial().salvar("zonas_fiduciario_faces_parcial.png")
```

### 3. `zonas_faces_completo()` — full grid on the faces
Equivalent to `zonas_grade()` (full grid at all crossings).

```python
zonas_faces_completo().salvar("zonas_fiduciario_faces_completo.png")
```

### 4. `zonas_zona_parcial(zonas)` — partial faces + highlighted zone(s)
Grid of the 3 visible faces **+** one or several painted zones, with automatic
legend.

```python
# single zone
zonas_zona_parcial(("crê totalmente", "confia totalmente", "demais")).salvar("z.png")
```

### 5. `zonas_zona_completo(zonas)` — full grid + highlighted zone(s)
Same as the previous, but with the full 4×4×4 grid behind.

```python
zonas_zona_completo(("crê totalmente", "confia totalmente", "demais")).salvar("z.png")
```

### 6. `zonas_percurso(percursos, grade=...)` — zones linked by a path
Draws the zones **+** one or several paths: a line that goes from the **middle**
of one zone to the **middle** of the next (never through the vertices), with an
arrow indicating the direction. A path links 2 zones or more and can move along
one or several axes at once.

- **Unidirectional** (`bidirecional=False`, default): arrow `->` shows the sense.
- **Bidirectional** (`bidirecional=True`): arrow `<->` indicates back and forth.
- `grade`: `"completa"` (4×4×4) or `"parcial"` (3 visible faces).

```python
# single (unidirectional) path, given as a list of zones
zonas_percurso([
    ("não crê nada",   "não confia nada",   "demenos"),
    ("crê totalmente", "confia totalmente", "demais"),
]).salvar("percurso.png")

# bidirectional path
zonas_percurso({"zonas": [z1, z2], "bidirecional": True}).salvar("p.png")

# several paths at once
zonas_percurso([
    {"zonas": [z1, z2, z3], "bidirecional": False},
    {"zonas": [za, zb],     "bidirecional": True},
]).salvar("p.png")
```

---

## How to specify a zone

A zone is a cell of the cube, given as the tuple
**`(eixo_z, eixo_x, intensity)`** (in the fiduciary space: `(belief, trust,
intensity)`). Each value can be the text label **or** the `0–3` index on the
scale.

```python
("crê totalmente", "confia totalmente", "demais")   # by text (fiduciary)
(3, 3, 3)                                            # equivalent by index
```

### Color by the "temperature" of the intensity
The color of each zone is defined by its **intensity**, on a fire scale:

| Intensity | Color | Temperature |
|---|---|---|
| `demais`  | red          | more "hot" |
| `mais`    | reddish-orange | |
| `menos`   | orange           | |
| `demenos` | golden-yellow      | more "cold" |

Zones at the same intensity get the **same color** — the distinction between
them comes from the position in the cube and the legend. To force a fixed color
(ignoring the scale), pass `cor="..."`.

### One zone
```python
zonas_zona_completo(("até crê", "quase confia", "mais")).salvar("uma.png")   # reddish-orange
```

### Several zones
```python
zonas = [
    ("crê totalmente", "confia totalmente", "demais"),   # red
    ("até crê",        "confia totalmente", "demais"),   # red (same intensity)
    ("até crê",        "confia totalmente", "mais"),     # reddish-orange
]
zonas_zona_completo(zonas).salvar("varias.png")
```

> **Mind the coordinates.** To place a zone *exactly below* another, keep
> **eixo_z and eixo_x equal** and change only the **intensity**. Changing
> eixo_z/eixo_x together shifts the cube to another column of the space (it ends
> up on the diagonal, not stacked).

The legend is built automatically as a three-column **table**
(`intensity | <eixo_x> | <eixo_z>` — in the fiduciary space, `intensity | trust
| belief`), one line per zone, with each zone's color square to the left of its
line. The lines are stacked **by intensity** (demenos at the bottom → demais at
the top), aligned to the cube's vertical axis. In paths, an arrow on the left
marks the direction of the path (up when ascending, down when descending). The
table sits on the right, centered on the cube's height; that's why the zone
functions use a wider figure by default (`figsize=(13, 8.5)`).

---

## How to mark a point

`_add_ponto(eixo_z, eixo_x, intensity, rotulo=None, cor=None, ...)` marks the
**center** of a zone with a colored point and five dotted reading guides — to
each of the three axes. It is the piece behind the
`_conversa`/`_inversa_1`/`_inversa_2` factories — a method of the
`CuboPontosIntensidade` class, not a factory; to use it in isolation, build the
figure manually:

```python
from cubo_tri_pontos_intensidade import CuboPontosIntensidade, PARECER, SER

c = CuboPontosIntensidade(titulo="Meu ponto", eixo_x_nome="parecer",
                          eixo_x_labels=PARECER, eixo_z_nome="ser", eixo_z_labels=SER)
c._add_titulos()
c._add_ponto("até ser", "parecer pouco", "mais",
             rotulo="um ponto qualquer do espaço veridictório")
c.salvar("ponto.png")
```

Unlike `zonas_percurso()` (in `cubo_tri_zonas_intensidade.py`), there is no
arrow and no link between points — each call marks an isolated point; to mark
several (as in the `_conversa`/`_inversa_1`/`_inversa_2` factories), call
`_add_ponto()` once per point.

---

## Common parameters

Passed as *keyword arguments* to any factory:

| Parameter | Default | What it does |
|---|---|---|
| `figsize` | `(9.5, 8.5)` — or `(13, 8.5)` in the zone functions | figure size in inches |
| `elev` | `18` | camera elevation (degrees) |
| `azim` | `-25` | camera azimuth (degrees) |
| `titulo` | `None` | big title at the top of the figure |
| `subtitulo` | `None` | smaller subtitle just below the title |
| `eixo_x_nome` | `"confiança (S/S)"` | name of the axis that descends to the right |
| `eixo_x_labels` | trust scale | list of 4 labels for that axis, from `–` to `+` |
| `eixo_z_nome` | `"crença (S/O)"` | name of the axis that rises to the right |
| `eixo_z_labels` | belief scale | list of 4 labels for that axis, from `–` to `+` |
| `rotular_lados` | `True` | `False` hides the eixo_x/eixo_z text, only the 4 divisions (used by `pontos_puro()`) |
| `cor` | `"lightblue"` | color of the single zone (ignored with several zones) |
| `alpha` | `0.40` | opacity of the zone fill |

`.salvar(caminho, dpi=300)` saves the PNG and returns the path (for high resolution/articles, use `dpi=600`).

```python
from cubo_tri_zonas_intensidade import zonas_zona_completo
zonas_zona_completo(zonas, elev=25, azim=-60, alpha=0.35).salvar("custom.png")

# a custom space, without going through any of the four ready-made factories
from cubo_tri_pontos_intensidade import CuboPontosIntensidade
c = CuboPontosIntensidade(
    titulo="Meu Espaço",
    eixo_x_nome="querer", eixo_x_labels=["não querer nada", "quase querer", "querer pouco", "querer muito"],
    eixo_z_nome="dever",  eixo_z_labels=["não dever nada", "quase dever", "dever pouco", "dever muito"],
)
c._add_titulos()
c.salvar("meu_espaco.png")
```

---

## Note on zone overlap (not a bug)

When two zones fall in the same projection band, one may end up **behind** the
other and look "cut" or smaller — this is **perspective occlusion**, not a
boundary error. To keep each zone readable, the fill is translucent and the
**outline (the 12 edges) of each cube is drawn on top**, in a more saturated
color, so that the full silhouette of each zone appears even when its fill is
covered.

If you still want to separate the zones visually, rotate the camera with
`azim`/`elev`.

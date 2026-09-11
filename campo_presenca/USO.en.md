# `campo_presenca.py` — usage guide

Plotter for the **field of presence**: a tensive representation of the crossing
between **intensity** (central axis) and **extensity** (side axes), in its two
canonical correlations — **inverse** and **converse**. It follows the same
visual language and architecture (class + factory + `.salvar()`) as the sibling
module `cubo_tri/cubo_tri_pontos_intensidade.py`, but in 2D.

Two factory sources, in the same spirit:

- `campo_presenca.py` — the "clean" versions: simple zones or the full tensive
  cycle (ascendency/descendency + poles).
- `campo_presenca_puro.py` — enriched versions, which add to the cone the
  internal direction of modulation and the density by intensity (see
  [The enriched versions](#the-enriched-versions-campo_presenca_puropy)).

## Reading the diagram

| Element | What it is |
|---|---|
| **Central line** | intensity axis: `+` at the top, `–` at the bottom, with "intensity" written below the `–` |
| **INVERSE cone** (left) | tip on top, base at the bottom — when intensity rises, extensity falls |
| **EXT.** to the left of the inverse | `–` at the top, `+` at the bottom (inverted relative to intensity) |
| **CONVERSE cone** (right) | base on top, tip at the bottom — when intensity rises, extensity rises too |
| **EXT.** to the right of the converse | `+` at the top, `–` at the bottom (same direction as intensity) |
| **S1 – S4** | the 4 slices of the converse cone, from the top (S1) to the tip (S4); each one linked by a dotted guide line to the MIDDLE of its band on the cone's surface |

Each cone has **4 circles**: the base one is solid; the other three (at 1/4, 2/4
and 3/4 of the height) are dotted and divide the cone into 4 equal parts.

### The directions of intensity (brackets beside the central line)

On each side of the central intensity line, two thin brackets mark the two
processes that split the line in half. Each process carries TWO rotated labels
glued to the bracket: the **name** (upright, closer) and its **increment** — the
"more/less × more/less" formula of *Figure 1. Tensive directions for more and
for less* (italic, further out):

| Side | Lower half | Upper half | Movement |
|---|---|---|---|
| Left | re-establishment ← *less less* | recrudescence ← *more more* | **ascendency** ↑ |
| Right | minimization ← *more less* | attenuation ← *less more* | **descendency** ↓ |

A master bracket, further out still, embraces the two process names together
(from the middle of one to the middle of the other); beside it sits
"ascendency" or "descendency" (italic, same register as the labels), with a
small arrow glued to the label indicating the direction of movement (above
"ascendency", below "descendency").

### The two poles of the cycle: event and torpor

Ascendency and descendency are the two arcs of the same tensive cycle, which
begin and end at the same two poles — marked next to the `+` and the `–` of the
central line, each one also with name and increment:

- **event** ← *only more* (top, next to the `+`) — maximum intensity.
- **torpor** ← *only less* (base, next to the `–`) — minimum intensity.

This closes the full cycle of Figure 1 and makes explicit that each label is a
**passage**, not a static zone: torpor (only less) passes through
re-establishment (less less), then recrudescence (more more), up to event (only
more); from there, descendency passes through attenuation (less more), through
minimization (more less) and back to torpor (only less). `_add_polos_ciclo()`
draws only the two poles — use it together with `_add_movimentos_int()`.

---

## How to run

It depends only on `matplotlib`.

```python
from campo_presenca import campo_zonas, campo_direcoes_tensivas
campo_direcoes_tensivas().salvar("campo_presenca_direcoes_tensivas.png")
```

Running `python3 campo_presenca.py` directly generates the images at once (the
ones from `campo_presenca_puro.py`, by running `python3 campo_presenca_puro.py`,
generate the enriched versions).

**Without editing code:** `gerar_campo.py` gathers the twelve versions (the
three from here plus the nine from `campo_presenca_puro.py`) into a single
script — edit the `VERSAO` variable at the top and run `python3 gerar_campo.py`.

---

## The versions

### 1. `campo_zonas()` — "Field of Tensive Presence"

Without brackets: the central line only has the **four intensity zones** marked
with a thin dash and the name beside it — from bottom (`–`) to top (`+`):
`demenos`, `menos`, `mais`, `demais`. Automatic title: "Campo de Presença
Tensivo".

```python
campo_zonas().salvar("campo_presenca_zonas.png")
```

### 2. `campo_valores_zonas()` — "Field of Tensive Presence" / "Tensive Values"

Like `campo_zonas()`, adding a bracket on the outside of each extensity axis,
splitting it in half. Each bracket carries a two-line label, italic/gray
("values of" + the term), growing outward from the bracket (never over it) — the
four **tensive values** of extensity:

| Axis | Upper half | Lower half |
|---|---|---|
| **inverse** (left) | values of absolute | values of universe |
| **converse** (right) | values of apogee | values of abyss |

```python
campo_valores_zonas().salvar("campo_valores_zonas.png")
```

It reuses `_colchete()` (the same piece used by `_add_movimentos_int()` for the
intensity brackets) through the new method
`_add_colchete_valores(x, lado, termo_cima, termo_baixo)` — `lado` defines both
which way the bracket opens and which side the label grows: `"esquerda"`
(bracket slightly to the left of `x`, opening to the right; label grows left) or
`"direita"` (the mirror). Called once per axis (`c.X_EXT_L` with `"esquerda"`,
`c.X_EXT_R` with `"direita"`), but nothing prevents reusing it with other terms
in a new factory.

### 3. `campo_direcoes_tensivas()` — "Field of Tensive Presence" / "Tensive Directions"

The ascendency/descendency brackets, each label with its increment, and the two
poles of the cycle (event/torpor) marked — the full tensive cycle of Figure 1,
showing that each label is a passage between poles. Automatic title + subtitle.

```python
campo_direcoes_tensivas().salvar("campo_presenca_direcoes_tensivas.png")
```

### Accepted parameters (common to both)

| Parameter | Default | What it does |
|---|---|---|
| `figsize` | `(13.0, 6.6)` | figure size in inches |
| `titulo` | `None` (`campo_zonas`/`campo_direcoes_tensivas` already come with one) | big title at the top of the figure |
| `subtitulo` | `None` (`campo_direcoes_tensivas` already comes with one) | subtitle, smaller and italic, just below the title |
| `H` | `3.0` | height of each cone / of the intensity line (also defines the 4 S1–S4 bands) |
| `R` | `1.35` | radius (half-width) of the base of each cone |
| `dist_cones` | `7.4` | distance between the centers of the two cones |
| `gap_ext` | `0.75` | space between the cone edge and the extensity axis beside it |
| `gap_label` | `0.50` | space between the extensity axis and the "extensity" label |
| `gap_s` | `1.05` | space between the right extensity axis and the S1–S4 column |

`_add_movimentos_int()` has its own internal parameters (`gap_colchete`,
`gap_rotulo`, `gap_incremento`, `gap_mestre`, `gap_label_mestre`,
`meia_altura_rotulo`, `gap_seta`) to adjust the spacing of the brackets and of
the name/increment labels, if needed — but they are not exposed in the factory
functions; to customize them, build the figure manually (see the next section).

```python
campo_zonas(titulo="Meu título", R=1.0).salvar("v2.png")
```

`.salvar(caminho, dpi=300)` saves the PNG and returns the path (for high resolution/articles, use `dpi=600`).

---

## The enriched versions (`campo_presenca_puro.py`)

They reuse the `CampoPresenca` class, adding to the clean cone:

- **internal modulation** — an arrow running along the cone's axis, from the
  center of one band to another. In the factories below, always between the two
  poles of the tensive cycle: `direcao="asc"` goes from `S4` to `S1` (extinction
  -> saturation, ascendency); `direcao="desc"` goes from `S1` to `S4`
  (saturation -> extinction, descendency) — the same pair as
  `campo_direcoes_tensivas()`.
- **density by intensity** — the four bands (S1..S4) filled with increasing
  opacity toward S1 (darker = denser), each slice cut in 3D by the arcs of the
  cone's ellipses (includes the full base, with its back, in the converse
  correlation).
- **mobilized extensity labels** — each S1–S4 band of the extensity axis carries
  two italic/gray labels (name + correlate), fixed in the `MOBIL_INVERSA` and
  `MOBIL_CONVERSA` constants:

  | Band | Inverse extensity | Converse extensity |
  |---|---|---|
  | S1 | ephemeral / hermetic | eternal / wide-open |
  | S2 | brief / closed | long / open |
  | S3 | long / open | brief / closed |
  | S4 | eternal / wide-open | ephemeral / hermetic |

- **intensity tendency labels** — the intensity axis always keeps the original
  labels (`S1`/demais, `S2`/mais, `S3`/menos, `S4`/demenos, via `_add_zonas_int()`)
  and adds, just below each one, the process name (italic/gray), according to
  `direcao`:

  | Band | `direcao="asc"` (`TEND_ASC`) | `direcao="desc"` (`TEND_DESC`) |
  |---|---|---|
  | S1 | saturation | moderation |
  | S2 | amplification | diminution |
  | S3 | progression | reduction |
  | S4 | resumption | extenuation |

- **red highlight arrow** — covers the same stretch as the internal modulation
  (`S4`→`S1` or `S1`→`S4`, according to `direcao`), overlaid on the intensity
  axis and on the active extensity(ies).

### 1. `campo_puro(correlacao="inversa", direcao="asc")`

One enriched correlation (internal modulation + density + mobilized labels on
its extensity + tendency labels and red arrow on the intensity); the opposite
one appears **faded** (cone and extensity in light gray, no labels, no arrow).

```python
from campo_presenca_puro import campo_puro
campo_puro("inversa", "asc").salvar("puro_inversa_asc.png")
campo_puro("conversa", "desc").salvar("puro_conversa_desc.png")
```

### 2. `campo_puro_ambas(direcao="asc")`

The two enriched correlations side by side, neither faded — each with the
mobilized labels of its own extensity, the same `direcao` on both cones, and the
red highlight arrow replicated on the intensity and on both extensities.

```python
from campo_presenca_puro import campo_puro_ambas
campo_puro_ambas("desc").salvar("puro_ambas_desc.png")
```

### The six standard examples

`campo_puro`/`campo_puro_ambas` have six ready combinations as named functions
(the same generated by `python3 campo_presenca_puro.py` and listed in
`gerar_campo.py`) — without "puro" in the name, since these six always carry a
modulation arrow, tendency labels and red highlight (they are no longer the
clean cone):

```python
from campo_presenca_puro import (
    campo_ambas_asc, campo_ambas_desc,
    campo_inversa_asc, campo_inversa_desc,
    campo_conversa_asc, campo_conversa_desc,
)
campo_ambas_asc().salvar("ambas_asc.png")
```

### 3. `campo_ampliacao(correlacao="inversa")`

An isolated correlation (the opposite faded, cone and extensity), with the fixed
modulation from `S2` (amplification) to `S1` (saturation) and the mobilized
labels of each band on the active extensity axis (two per band: the name and its
correlate — e.g. "brief"/"closed" in S2, "ephemeral"/"hermetic" in S1 in the
inverse).

```python
from campo_presenca_puro import campo_ampliacao
campo_ampliacao("inversa").salvar("ampliacao_inversa.png")
campo_ampliacao("conversa").salvar("ampliacao_conversa.png")
```

### 4. `campo_direcoes_tensivas_densidade()`

Like `campo_direcoes_tensivas()` (poles + ascendency/descendency brackets,
without the S1–S4 ruler), adding the density of the bands by intensity in both
cones.

```python
from campo_presenca_puro import campo_direcoes_tensivas_densidade
campo_direcoes_tensivas_densidade().salvar("direcoes_densidade.png")
```

All accept the same common parameters from the table above (`figsize`,
`titulo`, `subtitulo`, `H`, `R`, `dist_cones`, `gap_ext`, `gap_label`), plus
`direcao` (`campo_puro`/`campo_puro_ambas`, `"asc"` or `"desc"` — direction of
the internal modulation between `S4` and `S1`).

---

## Extending the module

The `CampoPresenca` class keeps the private methods as independent layers, in
the same spirit as `CuboPontosIntensidade`:

- `_add_eixo_int()` — central intensity line + the "intensity" label
- `_add_zonas_int()` — the four simple zones (demenos/menos/mais/demais), without brackets
- `_add_movimentos_int()` — the ascendency/descendency brackets
- `_add_polos_ciclo()` — the "event"/"torpor" labels at the two poles
- `_add_eixos_ext()` — the two side extensity axes
- `_add_cone(xc, tipo, titulo)` — draws a cone (`tipo="inversa"` or
  `"conversa"`); returns `r_at(y)`, the function giving the cone's radius at
  each height (useful to link new guides/markings to exact points of the cone)
- `_add_regua_s(r_at_conversa)` — the S1–S4 ruler with the dotted guides
- `_add_colchete_valores(x, lado, termo_cima, termo_baixo)` — a pair of brackets
  on the outside of an extensity axis, each with a two-line label ("values of" +
  term)

New versions (for example, with sample markings, highlighted zones or custom
labels) can be added as new factory functions combining these same layers —
without rewriting the geometry of the cones or the axes. E.g. a "campo_zonas +
directions" that combines `_add_zonas_int()` and `_add_movimentos_int()` in the
same figure, if that ever makes sense.

`CampoPresencaPuro` (in `campo_presenca_puro.py`) extends `CampoPresenca` with a
few more layers, in the same logic:

- `_add_densidade_intensidade(xc, tipo)` — the density of the 4 bands
- `_add_modulacao(xc, tipo, s_ini, s_fim)` — the modulation arrow, from the
  center of one band to the center of another
- `_add_cone_fraco(xc, tipo, titulo)` — the "faded" (light gray) version of a
  cone, for the unused correlation
- `_add_tendencias(tend)`, `_add_extensidade_rotulos(mobil, ...)`,
  `_add_destaque_percurso(s_ini, s_fim, ...)`, `_eixo_ext_fraco(x, ...)` —
  support layers used by `campo_ampliacao()`, reusable in new factories that
  need mobilized labels on the extensity or to highlight a traversed stretch

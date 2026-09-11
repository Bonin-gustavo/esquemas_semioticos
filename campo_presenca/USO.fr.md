# `campo_presenca.py` — guide d'utilisation

Traceur du **champ de présence** : représentation tensive du croisement entre
**intensité** (axe central) et **extensité** (axes latéraux), dans ses deux
corrélations canoniques — **inverse** et **converse**. Il suit le même langage
visuel et la même architecture (classe + fabrique + `.salvar()`) que le module
frère `cubo_tri/cubo_tri_pontos_intensidade.py`, mais en 2D.

Deux sources de fabriques, dans le même esprit :

- `campo_presenca.py` — les versions « propres » : zones simples ou le cycle
  tensif complet (ascendance/descendance + pôles).
- `campo_presenca_puro.py` — versions enrichies, qui ajoutent au cône la
  direction interne de modulation et la densification par intensité (voir
  [Les versions enrichies](#les-versions-enrichies-campo_presenca_puropy)).

## La lecture du diagramme

| Élément | Ce que c'est |
|---|---|
| **Ligne centrale** | axe d'intensité : `+` en haut, `–` en bas, avec « intensité » écrit en dessous du `–` |
| **Cône INVERSE** (gauche) | pointe en haut, base en bas — quand l'intensité monte, l'extensité descend |
| **EXT.** à gauche de l'inverse | `–` en haut, `+` en bas (inversé par rapport à l'intensité) |
| **Cône CONVERSE** (droite) | base en haut, pointe en bas — quand l'intensité monte, l'extensité monte aussi |
| **EXT.** à droite de la converse | `+` en haut, `–` en bas (même sens que l'intensité) |
| **S1 – S4** | les 4 tranches du cône de la converse, du haut (S1) jusqu'à la pointe (S4) ; chacune reliée par une ligne-guide en pointillés au MILIEU de sa bande sur la surface du cône |

Chaque cône a **4 cercles** : celui de la base est plein ; les trois autres (à
1/4, 2/4 et 3/4 de la hauteur) sont en pointillés et divisent le cône en 4
parties égales.

### Les directions de l'intensité (crochets à côté de la ligne centrale)

De chaque côté de la ligne centrale d'intensité, deux crochets fins marquent les
deux processus qui coupent la ligne en deux. Chaque processus porte DEUX
étiquettes couchées collées au crochet : le **nom** (droit, plus proche) et son
**incrément** — la formule « plus/moins × plus/moins » de la *Figure 1.
Directions tensives pour plus et pour moins* (italique, plus à l'extérieur) :

| Côté | Moitié du bas | Moitié du haut | Mouvement |
|---|---|---|---|
| Gauche | rétablissement ← *moins moins* | recrudescence ← *plus plus* | **ascendance** ↑ |
| Droite | minimisation ← *plus moins* | atténuation ← *moins plus* | **descendance** ↓ |

Un crochet-maître, encore plus à l'extérieur, embrasse les deux noms de
processus ensemble (du milieu de l'un au milieu de l'autre) ; à côté de lui se
trouve « ascendance » ou « descendance » (italique, même registre que les
étiquettes), avec une petite flèche collée à l'étiquette indiquant le sens du
mouvement (au-dessus d'« ascendance », en dessous de « descendance »).

### Les deux pôles du cycle : événement et torpeur

Ascendance et descendance sont les deux arcs du même cycle tensif, qui
commencent et finissent aux deux mêmes pôles — marqués à côté du `+` et du `–`
de la ligne centrale, chacun aussi avec nom et incrément :

- **événement** ← *seulement plus* (haut, à côté du `+`) — intensité maximale.
- **torpeur** ← *seulement moins* (base, à côté du `–`) — intensité minimale.

Cela ferme le cycle complet de la Figure 1 et rend explicite que chaque
étiquette est un **passage**, pas une zone statique : la torpeur (seulement
moins) passe par le rétablissement (moins moins), puis par la recrudescence
(plus plus), jusqu'à l'événement (seulement plus) ; de là, la descendance passe
par l'atténuation (moins plus), par la minimisation (plus moins) et revient à la
torpeur (seulement moins). `_add_polos_ciclo()` dessine seulement les deux pôles
— utilisez-le avec `_add_movimentos_int()`.

---

## Comment exécuter

Il ne dépend que de `matplotlib`.

```python
from campo_presenca import campo_zonas, campo_direcoes_tensivas
campo_direcoes_tensivas().salvar("campo_presenca_direcoes_tensivas.png")
```

Exécuter `python3 campo_presenca.py` directement génère les images d'un coup
(celles de `campo_presenca_puro.py`, en exécutant `python3 campo_presenca_puro.py`,
génèrent les versions enrichies).

**Sans éditer de code :** `gerar_campo.py` rassemble les douze versions (les
trois d'ici plus les neuf de `campo_presenca_puro.py`) dans un seul script —
éditez la variable `VERSAO` en haut et exécutez `python3 gerar_campo.py`.

---

## Les versions

### 1. `campo_zonas()` — « Champ de Présence Tensif »

Sans crochets : la ligne centrale n'a que les **quatre zones de l'intensité**
marquées d'un trait fin et du nom à côté — de bas (`–`) en haut (`+`) :
`demenos`, `menos`, `mais`, `demais`. Titre automatique : « Campo de Presença
Tensivo ».

```python
campo_zonas().salvar("campo_presenca_zonas.png")
```

### 2. `campo_valores_zonas()` — « Champ de Présence Tensif » / « Valeurs Tensives »

Comme `campo_zonas()`, en ajoutant un crochet à l'extérieur de chaque axe
d'extensité, le coupant en deux. Chaque crochet porte une étiquette sur deux
lignes, italique/gris (« valeurs de » + le terme), croissant vers l'extérieur du
crochet (jamais par-dessus) — les quatre **valeurs tensives** de l'extensité :

| Axe | Moitié du haut | Moitié du bas |
|---|---|---|
| **inverse** (gauche) | valeurs d'absolu | valeurs d'univers |
| **converse** (droite) | valeurs d'apogée | valeurs d'abîme |

```python
campo_valores_zonas().salvar("campo_valores_zonas.png")
```

Il réutilise `_colchete()` (la même pièce utilisée par `_add_movimentos_int()`
pour les crochets de l'intensité) via la nouvelle méthode
`_add_colchete_valores(x, lado, termo_cima, termo_baixo)` — `lado` définit à la
fois vers quelle direction le crochet s'ouvre et de quel côté l'étiquette
croît : `"esquerda"` (crochet un peu à gauche de `x`, s'ouvrant vers la droite ;
l'étiquette croît vers la gauche) ou `"direita"` (le miroir). Appelé une fois
par axe (`c.X_EXT_L` avec `"esquerda"`, `c.X_EXT_R` avec `"direita"`), mais rien
n'empêche de le réutiliser avec d'autres termes dans une nouvelle fabrique.

### 3. `campo_direcoes_tensivas()` — « Champ de Présence Tensif » / « Directions Tensives »

Les crochets d'ascendance/descendance, chaque étiquette avec son incrément, et
les deux pôles du cycle (événement/torpeur) marqués — le cycle tensif complet de
la Figure 1, montrant que chaque étiquette est un passage entre pôles. Titre +
sous-titre automatiques.

```python
campo_direcoes_tensivas().salvar("campo_presenca_direcoes_tensivas.png")
```

### Paramètres acceptés (communs aux deux)

| Paramètre | Défaut | Ce qu'il fait |
|---|---|---|
| `figsize` | `(13.0, 6.6)` | taille de la figure en pouces |
| `titulo` | `None` (`campo_zonas`/`campo_direcoes_tensivas` en ont déjà un) | grand titre en haut de la figure |
| `subtitulo` | `None` (`campo_direcoes_tensivas` en a déjà un) | sous-titre, plus petit et en italique, juste sous le titre |
| `H` | `3.0` | hauteur de chaque cône / de la ligne d'intensité (définit aussi les 4 bandes S1–S4) |
| `R` | `1.35` | rayon (demi-largeur) de la base de chaque cône |
| `dist_cones` | `7.4` | distance entre les centres des deux cônes |
| `gap_ext` | `0.75` | espace entre le bord du cône et l'axe d'extensité à côté |
| `gap_label` | `0.50` | espace entre l'axe d'extensité et l'étiquette « extensité » |
| `gap_s` | `1.05` | espace entre l'axe d'extensité droit et la colonne S1–S4 |

`_add_movimentos_int()` a ses propres paramètres internes (`gap_colchete`,
`gap_rotulo`, `gap_incremento`, `gap_mestre`, `gap_label_mestre`,
`meia_altura_rotulo`, `gap_seta`) pour ajuster l'espacement des crochets et des
étiquettes de nom/incrément, si besoin — mais ils ne sont pas exposés dans les
fonctions de fabrique ; pour les personnaliser, montez la figure manuellement
(voir la section suivante).

```python
campo_zonas(titulo="Meu título", R=1.0).salvar("v2.png")
```

`.salvar(caminho, dpi=300)` enregistre le PNG et renvoie le chemin (pour la haute résolution/les articles, utilisez `dpi=600`).

---

## Les versions enrichies (`campo_presenca_puro.py`)

Elles réutilisent la classe `CampoPresenca`, en ajoutant au cône propre :

- **modulation interne** — une flèche qui court le long de l'axe du cône, du
  centre d'une bande à une autre. Dans les fabriques ci-dessous, toujours entre
  les deux pôles du cycle tensif : `direcao="asc"` va de `S4` à `S1` (extinction
  -> saturation, ascendance) ; `direcao="desc"` va de `S1` à `S4` (saturation ->
  extinction, descendance) — la même paire que `campo_direcoes_tensivas()`.
- **densification par intensité** — les quatre bandes (S1..S4) remplies avec une
  opacité croissante vers S1 (plus foncé = plus dense), chaque tranche découpée
  en 3D par les arcs des ellipses du cône (inclut la base pleine, avec son
  verso, dans la corrélation converse).
- **étiquettes mobilisées de l'extensité** — chaque bande S1–S4 de l'axe
  d'extensité porte deux étiquettes en italique/gris (nom + corrélat), fixées
  dans les constantes `MOBIL_INVERSA` et `MOBIL_CONVERSA` :

  | Bande | Extensité de l'inverse | Extensité de la converse |
  |---|---|---|
  | S1 | éphémère / hermétique | éternel / grand ouvert |
  | S2 | bref / fermé | long / ouvert |
  | S3 | long / ouvert | bref / fermé |
  | S4 | éternel / grand ouvert | éphémère / hermétique |

- **étiquettes de tendance de l'intensité** — l'axe d'intensité garde toujours
  les étiquettes originales (`S1`/demais, `S2`/mais, `S3`/menos, `S4`/demenos,
  via `_add_zonas_int()`) et ajoute, juste en dessous de chacune, le nom du
  processus (italique/gris), selon `direcao` :

  | Bande | `direcao="asc"` (`TEND_ASC`) | `direcao="desc"` (`TEND_DESC`) |
  |---|---|---|
  | S1 | saturation | modération |
  | S2 | amplification | diminution |
  | S3 | progression | réduction |
  | S4 | reprise | extenuation |

- **flèche rouge de mise en évidence** — couvre le même tronçon que la modulation
  interne (`S4`→`S1` ou `S1`→`S4`, selon `direcao`), superposée à l'axe
  d'intensité et à la/aux extensité(s) active(s).

### 1. `campo_puro(correlacao="inversa", direcao="asc")`

Une corrélation enrichie (modulation interne + densification + étiquettes
mobilisées sur son extensité + étiquettes de tendance et flèche rouge sur
l'intensité) ; l'opposée apparaît **estompée** (cône et extensité en gris
clair, sans étiquettes, sans flèche).

```python
from campo_presenca_puro import campo_puro
campo_puro("inversa", "asc").salvar("puro_inversa_asc.png")
campo_puro("conversa", "desc").salvar("puro_conversa_desc.png")
```

### 2. `campo_puro_ambas(direcao="asc")`

Les deux corrélations enrichies côte à côte, aucune estompée — chacune avec les
étiquettes mobilisées de sa propre extensité, la même `direcao` sur les deux
cônes, et la flèche rouge de mise en évidence répliquée sur l'intensité et sur
les deux extensités.

```python
from campo_presenca_puro import campo_puro_ambas
campo_puro_ambas("desc").salvar("puro_ambas_desc.png")
```

### Les six exemples standards

`campo_puro`/`campo_puro_ambas` ont six combinaisons prêtes comme fonctions
nommées (les mêmes générées par `python3 campo_presenca_puro.py` et listées dans
`gerar_campo.py`) — sans « puro » dans le nom, puisque ces six portent toujours
une flèche de modulation, des étiquettes de tendance et une mise en évidence
rouge (ce ne sont plus le cône propre) :

```python
from campo_presenca_puro import (
    campo_ambas_asc, campo_ambas_desc,
    campo_inversa_asc, campo_inversa_desc,
    campo_conversa_asc, campo_conversa_desc,
)
campo_ambas_asc().salvar("ambas_asc.png")
```

### 3. `campo_ampliacao(correlacao="inversa")`

Une corrélation isolée (l'opposée estompée, cône et extensité), avec la
modulation fixe de `S2` (amplification) à `S1` (saturation) et les étiquettes
mobilisées de chaque bande sur l'axe d'extensité actif (deux par bande : le nom
et son corrélat — ex. « bref »/« fermé » en S2, « éphémère »/« hermétique » en
S1 dans l'inverse).

```python
from campo_presenca_puro import campo_ampliacao
campo_ampliacao("inversa").salvar("ampliacao_inversa.png")
campo_ampliacao("conversa").salvar("ampliacao_conversa.png")
```

### 4. `campo_direcoes_tensivas_densidade()`

Comme `campo_direcoes_tensivas()` (pôles + crochets d'ascendance/descendance,
sans la règle S1–S4), en ajoutant la densification des bandes par intensité dans
les deux cônes.

```python
from campo_presenca_puro import campo_direcoes_tensivas_densidade
campo_direcoes_tensivas_densidade().salvar("direcoes_densidade.png")
```

Toutes acceptent les mêmes paramètres communs du tableau ci-dessus (`figsize`,
`titulo`, `subtitulo`, `H`, `R`, `dist_cones`, `gap_ext`, `gap_label`), plus
`direcao` (`campo_puro`/`campo_puro_ambas`, `"asc"` ou `"desc"` — sens de la
modulation interne entre `S4` et `S1`).

---

## Étendre le module

La classe `CampoPresenca` garde les méthodes privées comme des couches
indépendantes, dans le même esprit que `CuboPontosIntensidade` :

- `_add_eixo_int()` — ligne centrale d'intensité + l'étiquette « intensité »
- `_add_zonas_int()` — les quatre zones simples (demenos/menos/mais/demais), sans crochets
- `_add_movimentos_int()` — les crochets d'ascendance/descendance
- `_add_polos_ciclo()` — les étiquettes « événement »/« torpeur » aux deux pôles
- `_add_eixos_ext()` — les deux axes d'extensité latéraux
- `_add_cone(xc, tipo, titulo)` — dessine un cône (`tipo="inversa"` ou
  `"conversa"`) ; renvoie `r_at(y)`, la fonction donnant le rayon du cône à
  chaque hauteur (utile pour relier de nouveaux guides/marquages à des points
  exacts du cône)
- `_add_regua_s(r_at_conversa)` — la règle S1–S4 avec les guides en pointillés
- `_add_colchete_valores(x, lado, termo_cima, termo_baixo)` — une paire de
  crochets à l'extérieur d'un axe d'extensité, chacun avec une étiquette sur
  deux lignes (« valeurs de » + terme)

De nouvelles versions (par exemple, avec des marquages d'exemple, des zones en
évidence ou des étiquettes personnalisées) peuvent être ajoutées comme nouvelles
fonctions de fabrique combinant ces mêmes couches — sans réécrire la géométrie
des cônes ou des axes. Ex. : un « campo_zonas + directions » qui combine
`_add_zonas_int()` et `_add_movimentos_int()` dans la même figure, si cela a un
jour du sens.

`CampoPresencaPuro` (dans `campo_presenca_puro.py`) étend `CampoPresenca` avec
quelques couches de plus, dans la même logique :

- `_add_densidade_intensidade(xc, tipo)` — la densification des 4 bandes
- `_add_modulacao(xc, tipo, s_ini, s_fim)` — la flèche de modulation, du centre
  d'une bande au centre d'une autre
- `_add_cone_fraco(xc, tipo, titulo)` — la version « estompée » (gris clair)
  d'un cône, pour la corrélation non utilisée
- `_add_tendencias(tend)`, `_add_extensidade_rotulos(mobil, ...)`,
  `_add_destaque_percurso(s_ini, s_fim, ...)`, `_eixo_ext_fraco(x, ...)` —
  couches de support utilisées par `campo_ampliacao()`, réutilisables dans de
  nouvelles fabriques qui ont besoin d'étiquettes mobilisées sur l'extensité ou
  de mettre en évidence un tronçon parcouru

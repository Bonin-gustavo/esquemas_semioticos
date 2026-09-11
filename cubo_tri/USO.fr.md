# `cubo_tri_pontos_intensidade.py` + `cubo_tri_zonas_intensidade.py` — guide d'utilisation

Traceur d'un espace à 3 axes **encore uniquement d'intensité** (l'extensité est
traitée dans campo_presenca/) pour les gradations d'un espace de valeur
sémiotique — fiducie, véridiction, manipulation ou compétence —, basé sur les
schémas originaux du chercheur (U3/U4–U6), appuyé sur Fontanille & Zilberberg,
*Tensão e Significação*, Zilberberg, *Elementos de Semiótica Tensiva* (2011) et
Zilberberg, *Structures Tensives* (2012).

Trois fichiers :

- **`espacos.py`** — le **contenu** (gradations des axes, espaces et parcours
  d'exemple). C'est ici que vous éditez/créez les gradations — voir
  [Comment éditer les gradations](#comment-éditer-les-gradations--créer-un-espace)
  ci-dessous.
- **`cubo_tri_pontos_intensidade.py`** — la classe `CuboPontosIntensidade` et
  les fabriques « par point » : la basique (`pontos_puro`), les quatre espaces
  prêts (fiducie, véridiction, manipulation, compétence) et, pour chacun, les
  versions `_conversa` (les 4 points de la diagonale converse), `_inversa_1` et
  `_inversa_2` (les deux diagonales inverses).
- **`cubo_tri_zonas_intensidade.py`** — `CuboZonasIntensidade
  (CuboPontosIntensidade)`, qui ajoute une grille 4×4×4, des zones en évidence
  (avec légende) et des parcours ; il importe `CuboPontosIntensidade` depuis
  `cubo_tri_pontos_intensidade.py`.

## Les trois axes

| Axe (croquis à la main) | Orientation à l'écran | Modifiable ? |
|---|---|---|
| **Intensité** | verticale, à **gauche** | non — toujours `demenos → menos → mais → demais` |
| **eixo_z** | monte à **droite** | oui — nom + 4 gradations (du `–` au `+`) |
| **eixo_x** | descend à **droite** | oui — nom + 4 gradations (du `–` au `+`) |

`eixo_x`/`eixo_z` sont le nom de l'axe et son échelle de 4 degrés ;
l'**intensité** est la même dans tout espace. Les quatre espaces prêts :

| Espace | eixo_x (descend à droite) | eixo_z (monte à droite) |
|---|---|---|
| Fiduciaire | confiance (S/S) : não confia nada → confia totalmente | croyance (S/O) : não crê nada → crê totalmente |
| Véridictoire | paraître : não parecer nada → parecer muito | être : não ser de forma alguma → ser exatamente |
| Manipulation | vouloir : não querer de forma alguma → querer muito | devoir : não dever nada → dever muito |
| Compétence | pouvoir : não poder nada → poder totalmente | savoir : não saber nada → saber exatamente |

> L'**extensité** est présente dans campo_presenca/, mais n'est pas traitée ici.

Correspondance interne pour matplotlib : `x ← eixo_x`, `y ← eixo_z`, `z ← intensité`.

---

## Comment éditer les gradations / créer un espace

Tout vit dans `espacos.py` — la source unique des contenus. Inutile de toucher
aux traceurs.

- **Éditer les gradations d'un axe** : changez les libellés de l'une des listes
  (`CONFIANCA`, `CRENCA`, `PARECER`, `SER`, `QUERER`, `DEVER`, `PODER`,
  `SABER`). Toujours 4 libellés, du `–` au `+`.
- **Créer un nouvel espace** : ajoutez une entrée à `ESPACOS` dans le même
  format (`eixo_x_nome`/`eixo_x_labels` + `eixo_z_nome`/`eixo_z_labels`). Les
  fabriques génériques (`pontos`, `pontos_diagonal`, `pontos_percurso`,
  `zonas_*`) l'acceptent automatiquement.
- **Parcours d'exemple** : vivent dans `PERCURSOS` (chemins manuels).

```python
from espacos import ESPACOS, diagonal, kw_espaco

# diagonales dérivées automatiquement des gradations :
diagonal("fiduciario", "conversa")    # 4 zones, ordre d'intensité ascendant
diagonal("fiduciario", "inversa_1")   # eixo_x descend
diagonal("fiduciario", "inversa_2")   # eixo_z descend

kw_espaco("competencial")             # kwargs prêts pour toute fabrique
```

Pour un espace ponctuel, vous pouvez toujours passer `eixo_x_nome`/
`eixo_x_labels` et `eixo_z_nome`/`eixo_z_labels` directement à toute fabrique
(voir [Paramètres communs](#paramètres-communs)).

---

## Comment exécuter

Les scripts dépendent de `numpy`, `matplotlib` et `Pillow` (utilisé uniquement
pour rogner l'excès de marge blanche du PNG après sauvegarde — les axes 3D sans
ticks ont un bug connu de matplotlib avec `bbox_inches="tight"`). Chaque
fabrique renvoie un objet `CuboPontosIntensidade` (ou `CuboZonasIntensidade`,
qui est un `CuboPontosIntensidade`) ; appelez `.salvar("fichier.png")` pour
générer l'image.

```python
from cubo_tri_pontos_intensidade import pontos_puro, pontos_fiduciario
from cubo_tri_zonas_intensidade import zonas_zona_completo
pontos_puro().salvar("puro.png")
pontos_fiduciario().salvar("fiducia.png")
```

- Exécuter `python3 cubo_tri_pontos_intensidade.py` génère les cubes « par
  point » d'un coup.
- Exécuter `python3 cubo_tri_zonas_intensidade.py` génère les quatre versions
  de grille/zone de la fiducie.
- `python3 gerar_exemplos.py` (re)génère **tous les exemples de référence** :
  les points dans `exemplos/pontos/` (un sous-dossier par espace, plus
  `pontos_puro.png` à la racine) et les 16×4 de zones dans
  `exemplos/zonas/<espace>/`.
- `gerar_zonas.py` et `gerar_percursos.py` sont les points d'entrée pour générer
  UNE figure personnalisée à la fois (bloc `EDITE AQUI` en haut).

---

## Les vingt commandes de `cubo_tri_pontos_intensidade.py`

Toutes acceptent les mêmes paramètres de caméra/figure via `**kw` (voir
[Paramètres communs](#paramètres-communs)).

### `pontos_puro()` — la plus basique de toutes
Seuls les libellés de l'**intensité** (la ligne verticale) et les symboles
`+`/`–` ; les deux autres axes (modifiables) montrent **uniquement les 4
divisions**, sans texte ni titre. Base des quatre espaces ci-dessous.

```python
pontos_puro().salvar("pontos_puro.png")
```

### Espace fiduciaire (confiance × croyance)
```python
pontos_fiduciario().salvar("pontos_fiduciario.png")          # trois axes complets
pontos_fiduciario_conversa().salvar("pontos_fiduciario_conversa.png")  # + diagonale converse
pontos_fiduciario_inversa_1().salvar("pontos_fiduciario_inversa_1.png")  # 1re inverse (la confiance descend)
pontos_fiduciario_inversa_2().salvar("pontos_fiduciario_inversa_2.png")  # 2e inverse (la croyance descend)
pontos_fiduciario_percurso_tres().salvar("pontos_fiduciario_percurso_tres.png")  # parcours de 3 points
```

### Espace véridictoire (paraître × être)
```python
pontos_veridictorio().salvar("pontos_veridictorio.png")
pontos_veridictorio_conversa().salvar("pontos_veridictorio_conversa.png")
pontos_veridictorio_inversa_1().salvar("pontos_veridictorio_inversa_1.png")
pontos_veridictorio_inversa_2().salvar("pontos_veridictorio_inversa_2.png")
pontos_veridictorio_percurso_dois().salvar("pontos_veridictorio_percurso_dois.png")  # parcours de 2 points
```

### Espace de manipulation (vouloir × devoir)
```python
pontos_manipulacao().salvar("pontos_manipulacao.png")
pontos_manipulacao_conversa().salvar("pontos_manipulacao_conversa.png")
pontos_manipulacao_inversa_1().salvar("pontos_manipulacao_inversa_1.png")
pontos_manipulacao_inversa_2().salvar("pontos_manipulacao_inversa_2.png")
pontos_manipulacao_percurso_quatro().salvar("pontos_manipulacao_percurso_quatro.png")  # parcours de 4 points
```

### Espace compétentiel (pouvoir × savoir)
```python
pontos_competencial().salvar("pontos_competencial.png")
pontos_competencial_conversa().salvar("pontos_competencial_conversa.png")
pontos_competencial_inversa_1().salvar("pontos_competencial_inversa_1.png")
pontos_competencial_inversa_2().salvar("pontos_competencial_inversa_2.png")
pontos_competencial_percurso_dois().salvar("pontos_competencial_percurso_dois.png")  # parcours de 2 points
```

Les trois diagonales de chaque espace :

- `_conversa` — les trois axes montent ensemble.
- `_inversa_1` — l'**eixo_x descend** pendant qu'eixo_z et l'intensité montent.
- `_inversa_2` — l'**eixo_z descend** pendant qu'eixo_x et l'intensité montent.

Chaque version `_conversa`/`_inversa_1`/`_inversa_2` porte un marqueur coloré
par point, avec des **guides en pointillés** vers les trois axes (voir
[Comment marquer un point](#comment-marquer-un-point)) — ce n'est pas un
parcours : pas de flèche, pas de lien d'un point à l'autre. Les versions
`_percurso_*` relient les points par une flèche (voir `_add_percurso` dans la
classe).

---

## Les six commandes de `cubo_tri_zonas_intensidade.py`

Toutes héritent de `CuboPontosIntensidade` (via `CuboZonasIntensidade`). Par
défaut elles travaillent dans l'espace fiduciaire ; pour les autres espaces,
passez `eixo_x_nome`/`eixo_x_labels` et `eixo_z_nome`/`eixo_z_labels` (les
gradations sont dans `cubo_tri_pontos_intensidade.py` : `PARECER`/`SER`,
`QUERER`/`DEVER`, `PODER`/`SABER`) :

```python
# le même cube de zones, maintenant dans l'espace compétentiel (pouvoir × savoir)
from cubo_tri_pontos_intensidade import PODER, SABER
from cubo_tri_zonas_intensidade import zonas_zona_completo
zonas_zona_completo(("saber exatamente", "poder totalmente", "demais"),
                    eixo_x_nome="poder", eixo_x_labels=PODER,
                    eixo_z_nome="saber", eixo_z_labels=SABER).salvar("z.png")
```

### 1. `zonas_grade()` — grille 4×4×4 complète
Grille en pointillés de tous les croisements des 4 zones sur chaque axe.

```python
zonas_grade().salvar("grade.png")
```

### 2. `zonas_faces_parcial()` — grille sur les 3 faces visibles seulement
Grille en pointillés uniquement sur le devant (`eixo_x × intensité`), sur le
côté droit (`eixo_z × intensité`) et sur le dessus. Plus propre que la grille
complète.

```python
zonas_faces_parcial().salvar("zonas_fiduciario_faces_parcial.png")
```

### 3. `zonas_faces_completo()` — grille complète sur les faces
Équivalente à `zonas_grade()` (grille complète à tous les croisements).

```python
zonas_faces_completo().salvar("zonas_fiduciario_faces_completo.png")
```

### 4. `zonas_zona_parcial(zonas)` — faces partielles + zone(s) en évidence
Grille des 3 faces visibles **+** une ou plusieurs zones peintes, avec légende
automatique.

```python
# zone unique
zonas_zona_parcial(("crê totalmente", "confia totalmente", "demais")).salvar("z.png")
```

### 5. `zonas_zona_completo(zonas)` — grille complète + zone(s) en évidence
Comme la précédente, mais avec la grille 4×4×4 complète derrière.

```python
zonas_zona_completo(("crê totalmente", "confia totalmente", "demais")).salvar("z.png")
```

### 6. `zonas_percurso(percursos, grade=...)` — zones reliées par un parcours
Dessine les zones **+** un ou plusieurs parcours : une ligne qui va du **milieu**
d'une zone au **milieu** de la suivante (jamais par les sommets), avec une
flèche indiquant la direction. Un parcours relie 2 zones ou plus et peut se
déplacer sur un ou plusieurs axes à la fois.

- **Unidirectionnel** (`bidirecional=False`, défaut) : flèche `->` montre le sens.
- **Bidirectionnel** (`bidirecional=True`) : flèche `<->` indique aller-retour.
- `grade` : `"completa"` (4×4×4) ou `"parcial"` (3 faces visibles).

```python
# parcours unique (unidirectionnel), donné comme liste de zones
zonas_percurso([
    ("não crê nada",   "não confia nada",   "demenos"),
    ("crê totalmente", "confia totalmente", "demais"),
]).salvar("percurso.png")

# parcours bidirectionnel
zonas_percurso({"zonas": [z1, z2], "bidirecional": True}).salvar("p.png")

# plusieurs parcours à la fois
zonas_percurso([
    {"zonas": [z1, z2, z3], "bidirecional": False},
    {"zonas": [za, zb],     "bidirecional": True},
]).salvar("p.png")
```

---

## Comment spécifier une zone

Une zone est une cellule du cube, donnée comme le tuple
**`(eixo_z, eixo_x, intensité)`** (dans la fiducie : `(croyance, confiance,
intensité)`). Chaque valeur peut être le libellé en texte **ou** l'indice `0–3`
sur l'échelle.

```python
("crê totalmente", "confia totalmente", "demais")   # par texte (fiducie)
(3, 3, 3)                                            # équivalent par indice
```

### Couleur par la « température » de l'intensité
La couleur de chaque zone est définie par son **intensité**, sur une échelle de
feu :

| Intensité | Couleur | Température |
|---|---|---|
| `demais`  | rouge          | plus « chaud » |
| `mais`    | rouge-orangé | |
| `menos`   | orange           | |
| `demenos` | jaune-doré      | plus « froid » |

Les zones de même intensité reçoivent la **même couleur** — la distinction
entre elles vient de la position dans le cube et de la légende. Pour forcer une
couleur fixe (en ignorant l'échelle), passez `cor="..."`.

### Une zone
```python
zonas_zona_completo(("até crê", "quase confia", "mais")).salvar("uma.png")   # rouge-orangé
```

### Plusieurs zones
```python
zonas = [
    ("crê totalmente", "confia totalmente", "demais"),   # rouge
    ("até crê",        "confia totalmente", "demais"),   # rouge (même intensité)
    ("até crê",        "confia totalmente", "mais"),     # rouge-orangé
]
zonas_zona_completo(zonas).salvar("varias.png")
```

> **Attention aux coordonnées.** Pour placer une zone *exactement en dessous*
> d'une autre, gardez **eixo_z et eixo_x égaux** et changez seulement
> l'**intensité**. Changer eixo_z/eixo_x ensemble déplace le cube vers une
> autre colonne de l'espace (il finit sur la diagonale, pas empilé).

La légende est construite toute seule comme un **tableau** de trois colonnes
(`intensité | <eixo_x> | <eixo_z>` — dans la fiducie, `intensité | confiance |
croyance`), une ligne par zone, avec le carré de couleur de chaque zone à gauche
de sa ligne. Les lignes sont empilées **par intensité** (demenos en bas → demais
en haut), alignées sur l'axe vertical du cube. Dans les parcours, une flèche à
gauche marque la direction du chemin (monte en ascendance, descend en
descendance). Le tableau se place à droite, centré sur la hauteur du cube ;
c'est pourquoi les fonctions de zone utilisent une figure plus large par défaut
(`figsize=(13, 8.5)`).

---

## Comment marquer un point

`_add_ponto(eixo_z, eixo_x, intensité, rotulo=None, cor=None, ...)` marque le
**centre** d'une zone avec un point coloré et cinq guides en pointillés de
lecture — vers chacun des trois axes. C'est la pièce derrière les fabriques
`_conversa`/`_inversa_1`/`_inversa_2` — une méthode de la classe
`CuboPontosIntensidade`, pas une fabrique ; pour l'utiliser isolément, montez la
figure manuellement :

```python
from cubo_tri_pontos_intensidade import CuboPontosIntensidade, PARECER, SER

c = CuboPontosIntensidade(titulo="Meu ponto", eixo_x_nome="parecer",
                          eixo_x_labels=PARECER, eixo_z_nome="ser", eixo_z_labels=SER)
c._add_titulos()
c._add_ponto("até ser", "parecer pouco", "mais",
             rotulo="um ponto qualquer do espaço veridictório")
c.salvar("ponto.png")
```

Contrairement à `zonas_percurso()` (dans `cubo_tri_zonas_intensidade.py`), il
n'y a ni flèche ni lien entre les points — chaque appel marque un point isolé ;
pour en marquer plusieurs (comme dans les fabriques
`_conversa`/`_inversa_1`/`_inversa_2`), appelez `_add_ponto()` une fois par
point.

---

## Paramètres communs

Passés comme *arguments nommés* à toute fabrique :

| Paramètre | Défaut | Ce qu'il fait |
|---|---|---|
| `figsize` | `(9.5, 8.5)` — ou `(13, 8.5)` dans les fonctions de zone | taille de la figure en pouces |
| `elev` | `18` | élévation de la caméra (degrés) |
| `azim` | `-25` | azimut de la caméra (degrés) |
| `titulo` | `None` | grand titre en haut de la figure |
| `subtitulo` | `None` | sous-titre plus petit juste sous le titre |
| `eixo_x_nome` | `"confiança (S/S)"` | nom de l'axe qui descend à droite |
| `eixo_x_labels` | échelle de la confiance | liste de 4 libellés de cet axe, du `–` au `+` |
| `eixo_z_nome` | `"crença (S/O)"` | nom de l'axe qui monte à droite |
| `eixo_z_labels` | échelle de la croyance | liste de 4 libellés de cet axe, du `–` au `+` |
| `rotular_lados` | `True` | `False` masque le texte d'eixo_x/eixo_z, seulement les 4 divisions (utilisé par `pontos_puro()`) |
| `cor` | `"lightblue"` | couleur de la zone unique (ignorée avec plusieurs zones) |
| `alpha` | `0.40` | opacité du remplissage des zones |

`.salvar(caminho, dpi=300)` enregistre le PNG et renvoie le chemin (pour la haute résolution/les articles, utilisez `dpi=600`).

```python
from cubo_tri_zonas_intensidade import zonas_zona_completo
zonas_zona_completo(zonas, elev=25, azim=-60, alpha=0.35).salvar("custom.png")

# un espace propre, sans passer par aucune des quatre fabriques prêtes
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

## Note sur le chevauchement de zones (ce n'est pas un bug)

Quand deux zones tombent dans la même bande de projection, l'une peut se
retrouver **derrière** l'autre et paraître « coupée » ou plus petite — c'est une
**occlusion de perspective**, pas une erreur de frontière. Pour garder chaque
zone lisible, le remplissage est translucide et le **contour (les 12 arêtes) de
chaque cube est tracé par-dessus**, dans une couleur plus saturée, de sorte que
la silhouette complète de chaque zone apparaisse même quand son remplissage est
recouvert.

Si vous voulez quand même séparer visuellement les zones, tournez la caméra avec
`azim`/`elev`.

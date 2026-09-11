# Schémas Tensifs

**Lire en :** [Português](README.md) · [English](README.en.md) · Français (actuel)

Deux outils Python qui génèrent, à partir de code, les visualisations de deux
schémas basés sur l'approche tensive : Fontanille & Zilberberg, *Tension et 
signification* (1998), Zilberberg, *Eléments de grammaire tensive* (2001) et 
Zilberberg, *Structures Tensives* (2012) :

- **`cubo_tri/`** — l'**espace d'intensité** (sans extensité pour l'instant) :
  deux outils 3D qui croisent une catégorie graduée (comme la **croyance**
  (relation sujet/objet), la **confiance** (relation sujet/sujet)) et une
  mesure graduée d'**intensité** — `cubo_tri_pontos_intensidade.py` (points
  et parcours) et `cubo_tri_zonas_intensidade.py` (grille, zones en évidence
  et parcours).
- **`campo_presenca/`** — le **champ de présence** : le croisement entre
  **intensité** et **extensité** dans les deux corrélations canoniques
  (**inverse** et **converse**), avec le cycle tensif complet (ascendance/
  descendance), les paroxysmes (événement/torpeur) et des versions enrichies
  (direction interne, densification par intensité).

Chaque dossier a son propre guide technique complet dans `USO.md` (en
portugais — voir le [Mode 2](#mode-2--via-ia-sans-programmer) si vous ne
lisez pas le portugais). Ce README couvre la vue d'ensemble et **les deux
façons d'utiliser ce dépôt**.

Aucune programmation n'est strictement nécessaire — voir le
[Mode 2](#mode-2--via-ia-sans-programmer) ci-dessous.

---

## Structure du dépôt

```
cubo_tri/
  espacos.py              # CONTENU modifiable : gradations des axes, espaces et parcours
  cubo_tri_pontos_intensidade.py  # module principal (classe CuboPontosIntensidade + fabriques de points)
  cubo_tri_zonas_intensidade.py   # grille, zones en évidence et parcours (les 4 espaces de valeur)
  gerar_zonas.py         # modifiez une liste de zones en haut du fichier et exécutez
  gerar_percursos.py     # modifiez des parcours (trajectoires) en haut et exécutez
  gerar_exemplos.py      # (re)génère tous les exemples de référence (points et zones)
  USO.md                  # guide complet (portugais) : axes, zones, parcours, paramètres
  exemplos/                # PNG de référence déjà générés (pontos/ et zonas/<espace>/)
campo_presenca/
  campo_presenca.py       # module de base (zones simples, cycle tensif)
  campo_presenca_puro.py  # versions enrichies (direction interne, densification)
  gerar_campo.py           # modifiez la version voulue en haut et exécutez
  USO.md                   # guide complet (portugais) : lecture du diagramme, versions, paramètres
  exemplos/                 # PNG de référence déjà générés
arco_tensivo/                # en construction
Crimson_Pro/                # police utilisée dans les figures (SIL OFL 1.1)
requirements.txt
```

## Exemples

Quelques figures générées (cliquez pour agrandir) :

<table>
  <tr>
    <td><img src="cubo_tri/exemplos/pontos/fiduciario/pontos_fiduciario_conversa.png" alt="Espace fiduciaire — diagonale converse" width="380"></td>
    <td><img src="cubo_tri/exemplos/zonas/fiduciario/zonas_fiduciario_zona_completo.png" alt="Espace fiduciaire — zone en évidence" width="380"></td>
  </tr>
  <tr>
    <td align="center"><i>pontos_fiduciario_conversa</i></td>
    <td align="center"><i>zonas_fiduciario_zona_completo</i></td>
  </tr>
  <tr>
    <td><img src="campo_presenca/exemplos/campo_presenca_direcoes_tensivas.png" alt="Champ de présence — directions tensives" width="380"></td>
    <td><img src="campo_presenca/exemplos/campo_ambas_asc.png" alt="Champ de présence — corrélations enrichies" width="380"></td>
  </tr>
  <tr>
    <td align="center"><i>campo_presenca_direcoes_tensivas</i></td>
    <td align="center"><i>campo_ambas_asc</i></td>
  </tr>
</table>

## Dépendances

- Python 3.9+
- `numpy`, `matplotlib` (installez avec `pip install -r requirements.txt`)

---

## Mode 1 — terminal (pour celles et ceux qui programment)

```bash
git clone https://github.com/Bonin-gustavo/esquemas_semioticos
cd esquemas_semioticos
pip install -r requirements.txt

# espace d'intensité — modifiez ZONAS dans cubo_tri/gerar_zonas.py, puis exécutez :
cd cubo_tri
python3 gerar_zonas.py
python3 gerar_percursos.py
python3 gerar_exemplos.py   # (re)génère tous les exemples de référence

# champ de présence — modifiez VERSAO dans campo_presenca/gerar_campo.py, puis exécutez :
cd ../campo_presenca
python3 gerar_campo.py
```

Les scripts `gerar_*.py` ont un bloc modifiable en haut du fichier (marqué
`EDITE AQUI`, « modifiez ici ») — changez les valeurs (zones, parcours,
version, titre) et relancez. Pour un usage plus avancé (appeler directement
les fonctions fabriques, combiner zones et parcours, ajuster la caméra/la
figure), consultez le `USO.md` de chaque dossier (en portugais ; demandez à
votre assistant IA de le traduire à la volée si besoin).

## Mode 2 — via IA (sans programmer)

Si vous ne programmez pas, vous pouvez demander à un assistant IA ayant
accès aux fichiers et pouvant exécuter du code (OpenCode, Claude Code, Codex
d'OpenAI, ou tout chatbot capable de lire des fichiers et d'exécuter du code)
de générer l'image à votre place.

Le plus simple est de **coller le lien du dépôt** dans la conversation :

1. Envoyez le lien à l'IA :

   > `https://github.com/Bonin-gustavo/esquemas_semioticos`

   L'IA télécharge le projet et lit les fichiers toute seule — vous n'avez
   rien à installer.

2. Décrivez ce que vous voulez en langage courant, en indiquant le bon
   dossier. Par exemple :

   > « Dans le dossier `cubo_tri/`, lis `cubo_tri_pontos_intensidade.py`,
   > `cubo_tri_zonas_intensidade.py` et `USO.md` (le guide d'utilisation en
   > portugais) et génère une image mettant en évidence la zone (crê
   > totalmente, confia totalmente, demais) en rouge, avec la grille
   > complète. »

   > « Dans le dossier `campo_presenca/`, lis `campo_presenca.py`,
   > `campo_presenca_puro.py` et `USO.md`, et génère le champ de présence en
   > ne montrant que la corrélation inverse, enrichie en densité, avec la
   > modulation commençant en S1 et se terminant en S4. »

3. L'IA lit le code et le `USO.md`, écrit (ou réutilise) les bons appels de
   fonction, et exécute le script — le résultat est le fichier `.png`
   généré.

Si l'IA n'a pas accès à Internet (ou si vous préférez télécharger), utilisez
le bouton **Code → Download ZIP** sur GitHub (ou `git clone`), décompressez
le dossier et glissez-le dans la conversation (ou ouvrez-le comme
projet/espace de travail) — le reste est identique.

Plus la demande est précise (quelles zones, quelle corrélation, quel
parcours), meilleur sera le résultat. Si vous ne connaissez pas les termes
techniques, décrivez ce que vous voulez en langage courant (« très intense
et très digne de confiance, mais sans y croire totalement ») — l'IA peut
faire correspondre cela aux bonnes zones à l'aide du `USO.md`.

---

## Cadre théorique

Les deux schémas s'appuient sur la sémiotique tensive de Claude Zilberberg
et Jacques Fontanille (Fontanille & Zilberberg, *Tension et signification* (1998), 
Zilberberg, *Eléments de grammaire tensive* (2001) et Zilberberg, *Structures Tensives* (2012)).

Les gradations des catégories du cube d'intensité s'inspirent de la
proposition de Soares et Mancini (2023) :

SOARES, Vinicius Lisboa; MANCINI, Renata. Uma leitura tensiva das modalidades veridictórias.
Estudos Semióticos, São Paulo, Brasil, v. 19, n. 1, p. 15–29, 2023. DOI: 10.11606/issn.1980-4016.esse.2023.206156.
Disponible sur : https://revistas.usp.br/esse/article/view/206156. Consulté le : 11 sept. 2026.

## Comment citer

```
BONIN, Gustavo. Esquemas Tensivos : espace d'intensité (points et zones) et
champ de présence [logiciel]. Programa de Pós-Graduação em Linguística,
Universidade de São Paulo, 2026. Disponible à :
https://github.com/Bonin-gustavo/esquemas_semioticos
```

## Licence

- **Code** (`.py`) : [MIT](LICENSE)
- **Documentation et images** (`README*.md`, `USO.md`, `exemplos/*.png`) :
  [CC BY 4.0](LICENSE-CONTENT.md)
- **Police Crimson Pro** (`Crimson_Pro/`) : [SIL OFL 1.1](Crimson_Pro/OFL.txt)

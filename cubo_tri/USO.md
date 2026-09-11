# `cubo_tri_pontos_intensidade.py` + `cubo_tri_zonas_intensidade.py` — guia de uso

Plotter de um espaço de 3 eixos **ainda só de intensidade** (a extensidade
é considerada no campo_presenca/) para as gradações de um espaço de valor
semiótico — fidúcia, veridicção, manipulação ou competência —, baseado nos
quadros autorais do pesquisador (U3/U4–U6), apoiados em Fontanille &
Zilberberg, *Tensão e Significação*, Zilberberg, *Elementos de Semiótica 
Tensiva* (2011) e Zilberberg, *Structures Tensives* (2012).

Três arquivos:

- **`espacos.py`** — os **conteúdos** (gradações dos eixos, espaços e
  percursos de exemplo). É aqui que você edita/cria as gradações — veja abaixo
  [Como editar gradações](#como-editar-gradações--criar-um-espaço).
- **`cubo_tri_pontos_intensidade.py`** — a classe `CuboPontosIntensidade` e
  as fábricas "por ponto": o básico (`pontos_puro`), os quatro espaços
  prontos (fidúcia, veridicção, manipulação, competência) e, de cada um, as
  versões `_conversa` (os 4 pontos da diagonal conversa), `_inversa_1` e
  `_inversa_2` (as duas diagonais inversas).
- **`cubo_tri_zonas_intensidade.py`** — `CuboZonasIntensidade
  (CuboPontosIntensidade)`, que acrescenta grade 4×4×4, zonas destacadas
  (com legenda) e percursos; importa `CuboPontosIntensidade` de
  `cubo_tri_pontos_intensidade.py`.

## Os três eixos

| Eixo (esboço à mão) | Orientação na tela | Maleável? |
|---|---|---|
| **Intensidade** | vertical, à **esquerda** | não — sempre `demenos → menos → mais → demais` |
| **eixo_z** | sobe à **direita** | sim — nome + 4 gradações (do `–` ao `+`) |
| **eixo_x** | desce à **direita** | sim — nome + 4 gradações (do `–` ao `+`) |

`eixo_x`/`eixo_z` são o nome do eixo e sua escala de 4 graus; a
**intensidade** é a mesma em qualquer espaço. Os quatro espaços prontos:

| Espaço | eixo_x (desce à direita) | eixo_z (sobe à direita) |
|---|---|---|
| Fiduciário | confiança (S/S): não confia nada → confia totalmente | crença (S/O): não crê nada → crê totalmente |
| Veridictório | parecer: não parecer nada → parecer muito | ser: não ser de forma alguma → ser exatamente |
| Manipulação | querer: não querer de forma alguma → querer muito | dever: não dever nada → dever muito |
| Competencial | poder: não poder nada → poder totalmente | saber: não saber nada → saber exatamente |

> A **extensidade** está presente no campo_presenca/, mas não é considerada aqui.

Mapeamento interno para o matplotlib: `x ← eixo_x`, `y ← eixo_z`, `z ← intensidade`.

---

## Como editar gradações / criar um espaço

Tudo mora em `espacos.py` — a fonte única dos conteúdos. Não precisa mexer
nos plotters.

- **Editar as gradações de um eixo**: troque os rótulos de uma das listas
  (`CONFIANCA`, `CRENCA`, `PARECER`, `SER`, `QUERER`, `DEVER`, `PODER`,
  `SABER`). Sempre 4 rótulos, do `–` ao `+`.
- **Criar um espaço novo**: adicione uma entrada em `ESPACOS` no mesmo
  formato (`eixo_x_nome`/`eixo_x_labels` + `eixo_z_nome`/`eixo_z_labels`).
  As fábricas genéricas (`pontos`, `pontos_diagonal`, `pontos_percurso`,
  `zonas_*`) passam a aceitá-lo automaticamente.
- **Percursos de exemplo**: ficam em `PERCURSOS` (caminhos manuais).

```python
from espacos import ESPACOS, diagonal, kw_espaco

# diagonais derivadas automaticamente das gradações:
diagonal("fiduciario", "conversa")    # 4 zonas, ordem ascendente de intensidade
diagonal("fiduciario", "inversa_1")   # eixo_x desce
diagonal("fiduciario", "inversa_2")   # eixo_z desce

kw_espaco("competencial")             # kwargs prontos p/ qualquer fábrica
```

Para um espaço próprio avulso, ainda dá para passar `eixo_x_nome`/
`eixo_x_labels` e `eixo_z_nome`/`eixo_z_labels` direto a qualquer fábrica
(veja [Parâmetros comuns](#parâmetros-comuns)).

---

## Como rodar

Os scripts dependem de `numpy`, `matplotlib` e `Pillow` (usado só para
recortar o excesso de margem branca do PNG depois de salvo — eixos 3D sem
ticks têm um bug conhecido do matplotlib com `bbox_inches="tight"`). Cada
função de fábrica devolve um objeto `CuboPontosIntensidade` (ou
`CuboZonasIntensidade`, que é um `CuboPontosIntensidade`); chame
`.salvar("arquivo.png")` para gerar a imagem.

```python
from cubo_tri_pontos_intensidade import pontos_puro, pontos_fiduciario
from cubo_tri_zonas_intensidade import zonas_zona_completo
pontos_puro().salvar("puro.png")
pontos_fiduciario().salvar("fiducia.png")
```

- Rodar `python3 cubo_tri_pontos_intensidade.py` gera os cubos "por ponto"
  de uma vez.
- Rodar `python3 cubo_tri_zonas_intensidade.py` gera as quatro versões de
  grade/zona da fidúcia.
- `python3 gerar_exemplos.py` (re)gera **todos os exemplos de referência**:
  os pontos em `exemplos/pontos/` (uma subpasta por espaço, mais o
  `pontos_puro.png` na raiz) e os 16×4 de zonas em `exemplos/zonas/<espaço>/`.
- `gerar_zonas.py` e `gerar_percursos.py` são as portas de entrada para
  gerar UMA figura customizada por vez (bloco `EDITE AQUI` no topo).

---

## Os vinte comandos de `cubo_tri_pontos_intensidade.py`

Todos aceitam os mesmos parâmetros de câmera/figura via `**kw`
(veja [Parâmetros comuns](#parâmetros-comuns)).

### `pontos_puro()` — o mais básico de todos
Só os rótulos da **intensidade** (a linha vertical) e os símbolos `+`/`–`; os
outros dois eixos (maleáveis) mostram **apenas as 4 divisões**, sem texto nem
título. Base para os quatro espaços abaixo.

```python
pontos_puro().salvar("pontos_puro.png")
```

### Espaço Fiduciário (confiança × crença)
```python
pontos_fiduciario().salvar("pontos_fiduciario.png")          # três eixos completos
pontos_fiduciario_conversa().salvar("pontos_fiduciario_conversa.png")  # + diagonal conversa
pontos_fiduciario_inversa_1().salvar("pontos_fiduciario_inversa_1.png")  # 1ª inversa (confiança desce)
pontos_fiduciario_inversa_2().salvar("pontos_fiduciario_inversa_2.png")  # 2ª inversa (crença desce)
pontos_fiduciario_percurso_tres().salvar("pontos_fiduciario_percurso_tres.png")  # percurso de 3 pontos
```

### Espaço Veridictório (parecer × ser)
```python
pontos_veridictorio().salvar("pontos_veridictorio.png")
pontos_veridictorio_conversa().salvar("pontos_veridictorio_conversa.png")
pontos_veridictorio_inversa_1().salvar("pontos_veridictorio_inversa_1.png")
pontos_veridictorio_inversa_2().salvar("pontos_veridictorio_inversa_2.png")
pontos_veridictorio_percurso_dois().salvar("pontos_veridictorio_percurso_dois.png")  # percurso de 2 pontos
```

### Espaço de Manipulação (querer × dever)
```python
pontos_manipulacao().salvar("pontos_manipulacao.png")
pontos_manipulacao_conversa().salvar("pontos_manipulacao_conversa.png")
pontos_manipulacao_inversa_1().salvar("pontos_manipulacao_inversa_1.png")
pontos_manipulacao_inversa_2().salvar("pontos_manipulacao_inversa_2.png")
pontos_manipulacao_percurso_quatro().salvar("pontos_manipulacao_percurso_quatro.png")  # percurso de 4 pontos
```

### Espaço Competencial (poder × saber)
```python
pontos_competencial().salvar("pontos_competencial.png")
pontos_competencial_conversa().salvar("pontos_competencial_conversa.png")
pontos_competencial_inversa_1().salvar("pontos_competencial_inversa_1.png")
pontos_competencial_inversa_2().salvar("pontos_competencial_inversa_2.png")
pontos_competencial_percurso_dois().salvar("pontos_competencial_percurso_dois.png")  # percurso de 2 pontos
```

As três diagonais de cada espaço:

- `_conversa` — os três eixos sobem juntos.
- `_inversa_1` — o **eixo_x desce** enquanto eixo_z e intensidade sobem.
- `_inversa_2` — o **eixo_z desce** enquanto eixo_x e intensidade sobem.

Cada versão `_conversa`/`_inversa_1`/`_inversa_2` leva um marcador colorido
por ponto, com **guias pontilhadas** até os três eixos (ver
[Como marcar um ponto](#como-marcar-um-ponto)) — não é um percurso: sem seta,
sem ligar um ponto a outro. Os `_percurso_*` ligam os pontos por seta (ver
`_add_percurso` na classe).

---

## Os seis comandos de `cubo_tri_zonas_intensidade.py`

Todos herdam de `CuboPontosIntensidade` (via `CuboZonasIntensidade`). Por
padrão trabalham no espaço da fidúcia; para os outros espaços, passe
`eixo_x_nome`/`eixo_x_labels` e `eixo_z_nome`/`eixo_z_labels` (as gradações
estão em `cubo_tri_pontos_intensidade.py`: `PARECER`/`SER`, `QUERER`/`DEVER`,
`PODER`/`SABER`):

```python
# o mesmo cubo de zonas, agora no espaço competencial (poder × saber)
from cubo_tri_pontos_intensidade import PODER, SABER
from cubo_tri_zonas_intensidade import zonas_zona_completo
zonas_zona_completo(("saber exatamente", "poder totalmente", "demais"),
                    eixo_x_nome="poder", eixo_x_labels=PODER,
                    eixo_z_nome="saber", eixo_z_labels=SABER).salvar("z.png")
```

### 1. `zonas_grade()` — grade completa 4×4×4
Grade tracejada de todos os cruzamentos das 4 zonas em cada eixo.

```python
zonas_grade().salvar("grade.png")
```

### 2. `zonas_faces_parcial()` — grade só nas 3 faces visíveis
Grade tracejada apenas na frente (`eixo_x × intensidade`), na lateral direita
(`eixo_z × intensidade`) e no topo. Mais limpo que a grade completa.

```python
zonas_faces_parcial().salvar("zonas_fiduciario_faces_parcial.png")
```

### 3. `zonas_faces_completo()` — grade completa nas faces
Equivalente à `zonas_grade()` (grade completa em todos os cruzamentos).

```python
zonas_faces_completo().salvar("zonas_fiduciario_faces_completo.png")
```

### 4. `zonas_zona_parcial(zonas)` — faces parciais + zona(s) destacada(s)
Grade das 3 faces visíveis **+** uma ou várias zonas pintadas, com legenda automática.

```python
# zona única
zonas_zona_parcial(("crê totalmente", "confia totalmente", "demais")).salvar("z.png")
```

### 5. `zonas_zona_completo(zonas)` — grade completa + zona(s) destacada(s)
Igual à anterior, mas com a grade 4×4×4 completa por trás.

```python
zonas_zona_completo(("crê totalmente", "confia totalmente", "demais")).salvar("z.png")
```

### 6. `zonas_percurso(percursos, grade=...)` — zonas ligadas por percurso
Desenha as zonas **+** um ou vários percursos: uma linha que vai do **meio** de
uma zona ao **meio** da seguinte (nunca pelos vértices), com seta indicando a
direção. Um percurso liga de 2 zonas em diante e pode andar por um ou vários
eixos ao mesmo tempo.

- **Unidirecional** (`bidirecional=False`, padrão): seta `->` mostra o sentido.
- **Bidirecional** (`bidirecional=True`): seta `<->` indica ida e volta.
- `grade`: `"completa"` (4×4×4) ou `"parcial"` (3 faces visíveis).

```python
# percurso único (unidirecional), dado como lista de zonas
zonas_percurso([
    ("não crê nada",   "não confia nada",   "demenos"),
    ("crê totalmente", "confia totalmente", "demais"),
]).salvar("percurso.png")

# percurso bidirecional
zonas_percurso({"zonas": [z1, z2], "bidirecional": True}).salvar("p.png")

# vários percursos de uma vez
zonas_percurso([
    {"zonas": [z1, z2, z3], "bidirecional": False},
    {"zonas": [za, zb],     "bidirecional": True},
]).salvar("p.png")
```

---

## Como especificar uma zona

Uma zona é uma célula do cubo, dada como a tupla **`(eixo_z, eixo_x, intensidade)`**
(na fidúcia: `(crença, confiança, intensidade)`). Cada valor pode ser o rótulo
em texto **ou** o índice `0–3` na escala.

```python
("crê totalmente", "confia totalmente", "demais")   # por texto (fidúcia)
(3, 3, 3)                                            # equivalente por índice
```

### Cor pela "temperatura" da intensidade
A cor de cada zona é definida pela sua **intensidade**, numa escala de fogo:

| Intensidade | Cor | Temperatura |
|---|---|---|
| `demais`  | vermelho          | mais "quente" |
| `mais`    | laranja-avermelhado | |
| `menos`   | laranja           | |
| `demenos` | amarelo-ouro      | mais "frio" |

Zonas na mesma intensidade recebem a **mesma cor** — a distinção entre elas fica
por conta da posição no cubo e da legenda. Para forçar uma cor fixa (ignorando a
escala), passe `cor="..."`.

### Uma zona
```python
zonas_zona_completo(("até crê", "quase confia", "mais")).salvar("uma.png")   # laranja-avermelhado
```

### Várias zonas
```python
zonas = [
    ("crê totalmente", "confia totalmente", "demais"),   # vermelho
    ("até crê",        "confia totalmente", "demais"),   # vermelho (mesma intensidade)
    ("até crê",        "confia totalmente", "mais"),     # laranja-avermelhado
]
zonas_zona_completo(zonas).salvar("varias.png")
```

> **Atenção às coordenadas.** Para colocar uma zona *exatamente abaixo* de outra,
> mantenha **eixo_z e eixo_x iguais** e mude só a **intensidade**. Mudar
> eixo_z/eixo_x junto desloca o cubo para outra coluna do espaço (fica na
> diagonal, e não empilhado).

A legenda é montada sozinha como uma **tabela** de três colunas
(`intensidade | <eixo_x> | <eixo_z>` — na fidúcia, `intensidade | confiança |
crença`), uma linha por zona, com o quadradinho de cor de cada zona à
esquerda da sua linha. As linhas são empilhadas **pela intensidade** (demenos
embaixo → demais em cima), alinhadas ao eixo vertical do cubo. Nos percursos,
uma seta à esquerda marca a direção do caminho (sobe no ascendente, desce no
descendente). A tabela fica à direita, centrada na altura do cubo; por isso as
funções de zona usam uma figura mais larga por padrão (`figsize=(13, 8.5)`).

---

## Como marcar um ponto

`_add_ponto(eixo_z, eixo_x, intensidade, rotulo=None, cor=None, ...)` marca o
**centro** de uma zona com um ponto colorido e cinco guias pontilhadas de
leitura — até cada um dos três eixos. É a peça por trás das fábricas
`_conversa`/`_inversa_1`/`_inversa_2` — método da classe
`CuboPontosIntensidade`, não uma função de fábrica; para usar isolado, monte
a figura manualmente:

```python
from cubo_tri_pontos_intensidade import CuboPontosIntensidade, PARECER, SER

c = CuboPontosIntensidade(titulo="Meu ponto", eixo_x_nome="parecer",
                          eixo_x_labels=PARECER, eixo_z_nome="ser", eixo_z_labels=SER)
c._add_titulos()
c._add_ponto("até ser", "parecer pouco", "mais",
             rotulo="um ponto qualquer do espaço veridictório")
c.salvar("ponto.png")
```

Diferente de `zonas_percurso()` (em `cubo_tri_zonas_intensidade.py`), não há
seta nem ligação entre pontos — cada chamada marca um ponto isolado; para
marcar vários (como nas fábricas `_conversa`/`_inversa_1`/`_inversa_2`),
chame `_add_ponto()` uma vez por ponto.

---

## Parâmetros comuns

Passados como *keyword arguments* para qualquer função de fábrica:

| Parâmetro | Padrão | O que faz |
|---|---|---|
| `figsize` | `(9.5, 8.5)` — ou `(13, 8.5)` nas funções de zona | tamanho da figura em polegadas |
| `elev` | `18` | elevação da câmera (graus) |
| `azim` | `-25` | azimute da câmera (graus) |
| `titulo` | `None` | título grande no topo da figura |
| `subtitulo` | `None` | subtítulo menor logo abaixo do título |
| `eixo_x_nome` | `"confiança (S/S)"` | nome do eixo que desce à direita |
| `eixo_x_labels` | escala da confiança | lista de 4 rótulos desse eixo, do `–` ao `+` |
| `eixo_z_nome` | `"crença (S/O)"` | nome do eixo que sobe à direita |
| `eixo_z_labels` | escala da crença | lista de 4 rótulos desse eixo, do `–` ao `+` |
| `rotular_lados` | `True` | `False` esconde o texto de eixo_x/eixo_z, só as 4 divisões (usado por `pontos_puro()`) |
| `cor` | `"lightblue"` | cor da zona única (ignorado com várias zonas) |
| `alpha` | `0.40` | opacidade do preenchimento das zonas |

`.salvar(caminho, dpi=300)` grava o PNG e devolve o caminho (para alta resolução/artigos, use `dpi=600`).

```python
from cubo_tri_zonas_intensidade import zonas_zona_completo
zonas_zona_completo(zonas, elev=25, azim=-60, alpha=0.35).salvar("custom.png")

# um espaço próprio, sem passar por nenhuma das quatro fábricas prontas
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

## Nota sobre sobreposição de zonas (não é bug)

Quando duas zonas caem na mesma faixa da projeção, uma pode ficar **atrás** da
outra e parecer "cortada" ou menor — isso é **oclusão de perspectiva**, não erro
de fronteira. Para manter cada zona legível, o preenchimento é translúcido e o
**contorno (as 12 arestas) de cada cubo é traçado por cima**, numa cor mais
saturada, de modo que a silhueta completa de cada zona apareça mesmo quando o
preenchimento é encoberto.

Se ainda assim quiser separar visualmente as zonas, gire a câmera com `azim`/`elev`.

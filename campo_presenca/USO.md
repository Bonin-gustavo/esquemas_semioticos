# `campo_presenca.py` — guia de uso

Plotter do **campo de presença**: representação tensiva do cruzamento entre
**intensidade** (eixo central) e **extensidade** (eixos laterais), nas suas
duas correlações canônicas — **inversa** e **conversa**. Segue a mesma
linguagem visual e arquitetura (classe + fábrica + `.salvar()`) do módulo
irmão `cubo_tri/cubo_tri_pontos_intensidade.py`, mas em 2D.

Duas fontes de fábricas, no mesmo espírito:

- `campo_presenca.py` — as versões "limpas": zonas simples ou o ciclo tensivo
  completo (ascendência/descendência + polos).
- `campo_presenca_puro.py` — versões enriquecidas, que acrescentam ao cone a
  direção interna de modulação e o adensamento por intensidade (ver
  [As versões enriquecidas](#as-versões-enriquecidas-campo_presenca_puropy)).

## A leitura do diagrama

| Elemento | O que é |
|---|---|
| **Linha central** | eixo de intensidade: `+` no topo, `–` embaixo, com "intensidade" escrito embaixo do `–` |
| **Cone INVERSA** (esquerda) | ponta em cima, base embaixo — quando a intensidade sobe, a extensidade desce |
| **EXT.** à esquerda da inversa | `–` no topo, `+` embaixo (invertido em relação à intensidade) |
| **Cone CONVERSA** (direita) | base em cima, ponta embaixo — quando a intensidade sobe, a extensidade sobe junto |
| **EXT.** à direita da conversa | `+` no topo, `–` embaixo (no mesmo sentido da intensidade) |
| **S1 – S4** | os 4 recortes do cone da conversa, do topo (S1) até a ponta (S4); cada um ligado por uma linha-guia pontilhada ao MEIO da sua faixa na superfície do cone |

Cada cone tem **4 círculos**: o da base é sólido; os outros três (a 1/4, 2/4
e 3/4 da altura) são pontilhados e dividem o cone em 4 partes iguais.

### As direções da intensidade (colchetes ao lado da linha central)

De cada lado da linha central de intensidade, dois colchetes finos marcam
os dois processos que dividem a linha ao meio. Cada processo leva DOIS
rótulos deitados e colados ao colchete: o **nome** (redondo, mais perto) e o
seu **incremento** — a fórmula "mais/menos × mais/menos" da *Figura 1.
Direções tensivas para mais e para menos* (itálico, mais para fora):

| Lado | Metade de baixo | Metade de cima | Movimento |
|---|---|---|---|
| Esquerda | restabelecimento ← *menos menos* | recrudescimento ← *mais mais* | **ascendência** ↑ |
| Direita | minimização ← *mais menos* | atenuação ← *menos mais* | **descendência** ↓ |

Um colchete-mestre, mais para fora ainda, abraça os dois nomes de processo
juntos (do meio de um ao meio do outro); ao lado dele fica "ascendência" ou
"descendência" (itálico, mesmo registro dos rótulos), com uma setinha bem
colada ao rótulo indicando o sentido do movimento (acima de "ascendência",
abaixo de "descendência").

### Os dois polos do ciclo: acontecimento e torpor

Ascendência e descendência são os dois arcos do mesmo ciclo tensivo, que
começam e terminam nos mesmos dois polos — marcados junto ao `+` e ao `–` da
linha central, cada um também com nome e incremento:

- **acontecimento** ← *somente mais* (topo, junto ao `+`) — intensidade máxima.
- **torpor** ← *somente menos* (base, junto ao `–`) — intensidade mínima.

Isso fecha o ciclo completo da Figura 1 e deixa explícito que cada rótulo é
uma **passagem**, não uma zona estática: o torpor (somente menos) passa
pelo restabelecimento (menos menos), depois pelo recrudescimento (mais mais),
até o acontecimento (somente mais); dali, a descendência passa pela atenuação
(menos mais), pela minimização (mais menos) e volta ao torpor (somente
menos). `_add_polos_ciclo()` desenha só os dois polos — use junto com
`_add_movimentos_int()`.

---

## Como rodar

Depende só de `matplotlib`.

```python
from campo_presenca import campo_zonas, campo_direcoes_tensivas
campo_direcoes_tensivas().salvar("campo_presenca_direcoes_tensivas.png")
```

Rodar `python3 campo_presenca.py` diretamente gera as duas imagens de uma vez
(as de `campo_presenca_puro.py`, rodando `python3 campo_presenca_puro.py`,
geram as versões enriquecidas).

**Sem editar código:** `gerar_campo.py` reúne as doze versões (as três
daqui mais as nove de `campo_presenca_puro.py`) num único script — edite a
variável `VERSAO` no topo e rode `python3 gerar_campo.py`.

---

## As versões

### 1. `campo_zonas()` — "Campo de Presença Tensivo"

Sem colchetes: a linha central só tem as **quatro zonas da intensidade**
marcadas com um traço fino e o nome ao lado — de baixo (`–`) para cima (`+`):
`demenos`, `menos`, `mais`, `demais`. Título automático: "Campo de Presença
Tensivo".

```python
campo_zonas().salvar("campo_presenca_zonas.png")
```

### 2. `campo_valores_zonas()` — "Campo de Presença Tensivo" / "Valores Tensivos"

Como `campo_zonas()`, acrescentando um colchete do lado de fora de cada
eixo de extensidade, dividindo-o ao meio. Cada colchete leva um rótulo em
duas linhas, itálico/cinza ("valores de" + o termo), crescendo pra fora do
colchete (nunca por cima dele) — os quatro **valores tensivos** da
extensidade:

| Eixo | Metade de cima | Metade de baixo |
|---|---|---|
| **inversa** (esquerda) | valores de absoluto | valores de universo |
| **conversa** (direita) | valores de apogeu | valores de abismo |

```python
campo_valores_zonas().salvar("campo_valores_zonas.png")
```

Reaproveita `_colchete()` (a mesma peça usada por `_add_movimentos_int()`
para os colchetes da intensidade) através do método novo
`_add_colchete_valores(x, lado, termo_cima, termo_baixo)` — `lado` define
tanto para que direção o colchete abre quanto para que lado o rótulo
cresce: `"esquerda"` (colchete um pouco à esquerda de `x`, abrindo pra
direita; rótulo cresce pra esquerda) ou `"direita"` (o espelho). Chamado uma
vez por eixo (`c.X_EXT_L` com `"esquerda"`, `c.X_EXT_R` com `"direita"`),
mas nada impede reaproveitá-lo com outros termos numa fábrica nova.

### 3. `campo_direcoes_tensivas()` — "Campo de Presença Tensivo" / "Direções Tensivas"

Os colchetes de ascendência/descendência, cada rótulo com seu incremento, e
os dois polos do ciclo (acontecimento/torpor) marcados — o ciclo tensivo
completo da Figura 1, evidenciando que cada rótulo é uma passagem entre
polos. Título + subtítulo automáticos.

```python
campo_direcoes_tensivas().salvar("campo_presenca_direcoes_tensivas.png")
```

### Parâmetros aceitos (comuns às duas)

| Parâmetro | Padrão | O que faz |
|---|---|---|
| `figsize` | `(13.0, 6.6)` | tamanho da figura em polegadas |
| `titulo` | `None` (`campo_zonas`/`campo_direcoes_tensivas` já vêm com um) | título grande no topo da figura |
| `subtitulo` | `None` (`campo_direcoes_tensivas` já vem com um) | subtítulo, menor e em itálico, logo abaixo do título |
| `H` | `3.0` | altura de cada cone / da linha de intensidade (também define as 4 faixas S1–S4) |
| `R` | `1.35` | raio (meia-largura) da base de cada cone |
| `dist_cones` | `7.4` | distância entre os centros dos dois cones |
| `gap_ext` | `0.75` | espaço entre a borda do cone e o eixo de extensidade ao lado |
| `gap_label` | `0.50` | espaço entre o eixo de extensidade e o rótulo "extensidade" |
| `gap_s` | `1.05` | espaço entre o eixo de extensidade direito e a coluna S1–S4 |

`_add_movimentos_int()` tem seus próprios parâmetros internos
(`gap_colchete`, `gap_rotulo`, `gap_incremento`, `gap_mestre`,
`gap_label_mestre`, `meia_altura_rotulo`, `gap_seta`) para ajustar o
espaçamento dos colchetes e dos rótulos de nome/incremento, caso precise —
mas eles não são expostos nas funções de fábrica; para customizá-los, monte
a figura manualmente (veja a seção seguinte).

```python
campo_zonas(titulo="Meu título", R=1.0).salvar("v2.png")
```

`.salvar(caminho, dpi=300)` grava o PNG e devolve o caminho (para alta resolução/artigos, use `dpi=600`).

---

## As versões enriquecidas (`campo_presenca_puro.py`)

Reaproveitam a classe `CampoPresenca`, acrescentando ao cone limpo:

- **modulação interna** — uma seta que corre pelo eixo do cone, do centro de
  uma faixa a outra. Nas fábricas abaixo, sempre entre os dois polos do ciclo
  tensivo: `direcao="asc"` vai de `S4` a `S1` (extinção -> saturação,
  ascendência); `direcao="desc"` vai de `S1` a `S4` (saturação -> extinção,
  descendência) — a mesma dupla de `campo_direcoes_tensivas()`.
- **adensamento por intensidade** — as quatro faixas (S1..S4) preenchidas com
  opacidade crescente rumo a S1 (mais escuro = mais denso), cada fatia
  recortada em 3D pelos arcos das elipses do cone (inclui a base cheia, com o
  verso, na correlação conversa).
- **rótulos mobilizados da extensidade** — cada faixa S1–S4 do eixo de
  extensidade leva dois rótulos em itálico/cinza (nome + correlato), fixados
  nas constantes `MOBIL_INVERSA` e `MOBIL_CONVERSA`:

  | Faixa | Extensidade da inversa | Extensidade da conversa |
  |---|---|---|
  | S1 | efêmero / hermético | eterno / escancarado |
  | S2 | breve / fechado | longo / aberto |
  | S3 | longo / aberto | breve / fechado |
  | S4 | eterno / escancarado | efêmero / hermético |

- **rótulos de tendência da intensidade** — o eixo de intensidade mantém
  sempre os rótulos originais (`S1`/demais, `S2`/mais, `S3`/menos,
  `S4`/demenos, via `_add_zonas_int()`) e acrescenta, logo abaixo de cada um,
  o nome do processo (itálico/cinza), conforme a `direcao`:

  | Faixa | `direcao="asc"` (`TEND_ASC`) | `direcao="desc"` (`TEND_DESC`) |
  |---|---|---|
  | S1 | saturação | moderação |
  | S2 | ampliação | diminuição |
  | S3 | progressão | redução |
  | S4 | retomada | extenuação |

- **seta vermelha de destaque** — cobre o mesmo trecho da modulação interna
  (`S4`→`S1` ou `S1`→`S4`, conforme `direcao`), sobreposta ao eixo de
  intensidade e à(s) extensidade(s) ativa(s).

### 1. `campo_puro(correlacao="inversa", direcao="asc")`

Uma correlação enriquecida (modulação interna + adensamento + rótulos
mobilizados na sua extensidade + rótulos de tendência e seta vermelha na
intensidade); a oposta aparece **apagada** (cone e extensidade em cinza
claro, sem rótulos, sem seta).

```python
from campo_presenca_puro import campo_puro
campo_puro("inversa", "asc").salvar("puro_inversa_asc.png")
campo_puro("conversa", "desc").salvar("puro_conversa_desc.png")
```

### 2. `campo_puro_ambas(direcao="asc")`

As duas correlações enriquecidas lado a lado, nenhuma apagada — cada uma com
os rótulos mobilizados da própria extensidade, a mesma `direcao` nos dois
cones, e a seta vermelha de destaque replicada na intensidade e nas duas
extensidades.

```python
from campo_presenca_puro import campo_puro_ambas
campo_puro_ambas("desc").salvar("puro_ambas_desc.png")
```

### Os seis exemplos padrão

`campo_puro`/`campo_puro_ambas` têm seis combinações prontas como funções
nomeadas (as mesmas geradas por `python3 campo_presenca_puro.py` e listadas
em `gerar_campo.py`) — sem "puro" no nome, já que essas seis sempre levam
seta de modulação, rótulos de tendência e destaque vermelho (não são mais o
cone limpo):

```python
from campo_presenca_puro import (
    campo_ambas_asc, campo_ambas_desc,
    campo_inversa_asc, campo_inversa_desc,
    campo_conversa_asc, campo_conversa_desc,
)
campo_ambas_asc().salvar("ambas_asc.png")
```

### 3. `campo_ampliacao(correlacao="inversa")`

Uma correlação isolada (a oposta apagada, cone e extensidade), com a
modulação fixa de `S2` (ampliação) a `S1` (saturação) e os rótulos
mobilizados de cada faixa no eixo de extensidade ativo (dois por faixa: o
nome e seu correlato — ex. "breve"/"fechado" em S2, "efêmero"/"hermético" em
S1 na inversa).

```python
from campo_presenca_puro import campo_ampliacao
campo_ampliacao("inversa").salvar("ampliacao_inversa.png")
campo_ampliacao("conversa").salvar("ampliacao_conversa.png")
```

### 4. `campo_direcoes_tensivas_densidade()`

Como `campo_direcoes_tensivas()` (polos + colchetes de ascendência/
descendência, sem a régua S1–S4), acrescentando o adensamento das faixas por
intensidade nos dois cones.

```python
from campo_presenca_puro import campo_direcoes_tensivas_densidade
campo_direcoes_tensivas_densidade().salvar("direcoes_densidade.png")
```

Todas aceitam os mesmos parâmetros comuns da tabela acima (`figsize`,
`titulo`, `subtitulo`, `H`, `R`, `dist_cones`, `gap_ext`, `gap_label`), além
de `direcao` (`campo_puro`/`campo_puro_ambas`, `"asc"` ou `"desc"` — sentido
da modulação interna entre `S4` e `S1`).

---

## Estender o módulo

A classe `CampoPresenca` guarda os métodos privados como camadas
independentes, no mesmo espírito de `CuboPontosIntensidade`:

- `_add_eixo_int()` — linha central de intensidade + o rótulo "intensidade"
- `_add_zonas_int()` — as quatro zonas simples (demenos/menos/mais/demais), sem colchetes
- `_add_movimentos_int()` — os colchetes de ascendência/descendência
- `_add_polos_ciclo()` — os rótulos "acontecimento"/"torpor" nos dois polos
- `_add_eixos_ext()` — os dois eixos de extensidade laterais
- `_add_cone(xc, tipo, titulo)` — desenha um cone (`tipo="inversa"` ou
  `"conversa"`); devolve `r_at(y)`, a função que dá o raio do cone em cada
  altura (útil para ligar novas guias/marcações a pontos exatos do cone)
- `_add_regua_s(r_at_conversa)` — a régua S1–S4 com as guias pontilhadas
- `_add_colchete_valores(x, lado, termo_cima, termo_baixo)` — um par de
  colchetes do lado de fora de um eixo de extensidade, cada um com um
  rótulo de duas linhas ("valores de" + termo)

Novas versões (por exemplo, com marcações de exemplo, zonas destacadas ou
rótulos customizados) podem ser acrescentadas como novas funções de fábrica
que combinam essas mesmas camadas — sem precisar reescrever a geometria dos
cones ou dos eixos. Ex.: um "campo_zonas + direções" que combine
`_add_zonas_int()` e `_add_movimentos_int()` na mesma figura, se um dia fizer
sentido.

`CampoPresencaPuro` (em `campo_presenca_puro.py`) estende `CampoPresenca` com
mais algumas camadas, na mesma lógica:

- `_add_densidade_intensidade(xc, tipo)` — o adensamento das 4 faixas
- `_add_modulacao(xc, tipo, s_ini, s_fim)` — a seta de modulação, do centro
  de uma faixa ao centro de outra
- `_add_cone_fraco(xc, tipo, titulo)` — a versão "apagada" (cinza claro) de
  um cone, para a correlação não usada
- `_add_tendencias(tend)`, `_add_extensidade_rotulos(mobil, ...)`,
  `_add_destaque_percurso(s_ini, s_fim, ...)`, `_eixo_ext_fraco(x, ...)` —
  camadas de apoio usadas por `campo_ampliacao()`, reaproveitáveis em novas
  fábricas que precisem de rótulos mobilizados na extensidade ou de destacar
  um trecho percorrido

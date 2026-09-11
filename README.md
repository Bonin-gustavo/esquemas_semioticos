# Esquemas Tensivos

**Leia em:** Português (atual) · [English](README.en.md) · [Français](README.fr.md)

Duas ferramentas em Python para gerar, a partir de código, as visualizações de
dois esquemas baseados na abordagem tensiva (Fontanille & Zilberberg, *Tensão e
Significação* (2001), Zilberberg, *Elementos de Semiótica Tensiva* (2011) e Zilberberg, *Structures Tensives* (2012):

- **`cubo_tri/`** — o **espaço de intensidade** (ainda sem extensidade): dois
  códigos 3D que cruzam um categoria gradualizada (como de **crença** (relação sujeito/objeto), **confiança**
  (relação sujeito/sujeito)) e uma medida gradualizada de **intensidade** —
  `cubo_tri_pontos_intensidade.py` (pontos e percursos) e
  `cubo_tri_zonas_intensidade.py` (grade, zonas destacadas e percursos).
- **`campo_presenca/`** — o **campo de presença**: o cruzamento entre
  **intensidade** e **extensidade** nas duas correlações canônicas
  (**inversa** e **conversa**), com o ciclo tensivo completo
  (ascendência/descendência), paroxismos (acontecimento/torpor) e versões enriquecidas
  (direção interna, adensamento por intensidade).

Cada pasta tem seu próprio guia técnico completo em `USO.md` — este README
cobre a visão geral e **os dois modos de usar o repositório**.

Nenhuma programação é estritamente necessária: veja o [Modo 2](#modo-2--via-ia-sem-programar) abaixo.

---

## Estrutura do repositório

```
cubo_tri/
  espacos.py              # CONTEÚDO editável: gradações dos eixos, espaços e percursos
  cubo_tri_pontos_intensidade.py  # classe CuboPontosIntensidade + pontos por espaço (fidúcia, veridicção, manipulação, competência)
  cubo_tri_zonas_intensidade.py   # classe CuboZonasIntensidade: grade, zonas destacadas e percursos (4 espaços)
  gerar_zonas.py           # edite uma lista de zonas no topo e rode
  gerar_percursos.py       # edite percursos (trajetórias) no topo e rode
  gerar_exemplos.py        # (re)gera todos os exemplos de referência (pontos e zonas)
  USO.md                    # guia completo: eixos, zonas, percursos, pontos, parâmetros
  exemplos/                  # PNGs de referência já gerados (pontos/ e zonas/<espaço>/)
campo_presenca/
  campo_presenca.py      # módulo base (zonas simples, ciclo tensivo)
  campo_presenca_puro.py # versões enriquecidas (direção interna, adensamento)
  gerar_campo.py          # edite a versão desejada no topo e rode
  USO.md                  # guia completo: leitura do diagrama, versões, parâmetros
  exemplos/                # PNGs de referência já gerados
arco_tensivo/
  em construção
Crimson_Pro/               # fonte usada nas figuras (SIL OFL 1.1)
requirements.txt
```

## Dependências

- Python 3.9+
- `numpy`, `matplotlib` (instale com `pip install -r requirements.txt`)

---

## Modo 1 — terminal (para quem programa)

```bash
git clone https://github.com/Bonin-gustavo/esquemas_semioticos
cd esquemas_semioticos
pip install -r requirements.txt

# espaço de intensidade — edite ZONAS em cubo_tri/gerar_zonas.py e rode:
cd cubo_tri
python3 gerar_zonas.py
python3 gerar_percursos.py
python3 gerar_exemplos.py   # (re)gera todos os exemplos de referência

# campo de presença — edite VERSAO em campo_presenca/gerar_campo.py e rode:
cd ../campo_presenca
python3 gerar_campo.py
```

Os scripts `gerar_*.py` têm um bloco `EDITE AQUI` no topo — troque os valores
(zonas, percursos, versão, título) e rode de novo. Para uso mais avançado
(chamar as funções de fábrica diretamente, combinar zonas e percursos,
ajustar câmera/figura), veja o `USO.md` de cada pasta.

## Modo 2 — via IA (sem programar)

Se você não programa, pode pedir a uma IA com acesso a arquivos e capacidade
de rodar código (OpenCode, Claude Code, Codex do OpenAI, ou qualquer chatbot
que tenha acesso a arquivos) para gerar a imagem por você.

O jeito mais simples é **colar o link do repositório** na conversa:

1. Envie para a IA o link:

   > `https://github.com/Bonin-gustavo/esquemas_semioticos`

   A IA baixa o projeto e lê os arquivos sozinha — você não precisa instalar
   nada.

2. Diga em português o que você quer, apontando a pasta certa. Por exemplo:

   > "Na pasta `cubo_tri/`, leia `cubo_tri_pontos_intensidade.py`,
   > `cubo_tri_zonas_intensidade.py` e `USO.md` e gere uma imagem destacando a
   > zona (crê totalmente, confia totalmente, demais) em vermelho, com a grade
   > completa."

   > "Na pasta `campo_presenca/`, leia `campo_presenca.py`,
   > `campo_presenca_puro.py` e `USO.md` e gere o campo de presença mostrando
   > só a correlação inversa, enriquecida em densidade, com a modulação começando 
   > em S1 e terminando em S4."

3. A IA lê o código e o `USO.md`, escreve (ou reaproveita) as chamadas certas
   e roda o script — o resultado é o arquivo `.png` gerado.

Se a IA não tiver acesso à internet (ou você preferir baixar): use o botão
**Code → Download ZIP** no GitHub (ou `git clone`), descompacte e arraste a
pasta para a conversa (ou abra-a como projeto/workspace) — o resto é igual.

Quanto mais específico o pedido (quais zonas, qual correlação, qual
percurso), melhor o resultado. Se não souber os termos técnicos, descreva o
que quer em linguagem comum ("bem intenso e bem confiável, mas sem crer
totalmente") — a IA consegue mapear isso para as zonas certas usando o
`USO.md`.

---

## Base teórica

Os dois esquemas partem da semiótica tensiva de Claude Zilberberg e Jacques
Fontanille (*Tensão e Significação*), Zilberberg, (*Elementos de Semiótica 
Tensiva* (2011)) e Zilberberg, *Structures Tensives* (2012).

As gradações das categorias do cubo de intensidade são inspiradas
na proposta de Soares e Mancini (2023):

SOARES, Vinicius Lisboa; MANCINI, Renata. Uma leitura tensiva das modalidades veridictórias. 
Estudos Semióticos, São Paulo, Brasil, v. 19, n. 1, p. 15–29, 2023. DOI: 10.11606/issn.1980-4016.esse.2023.206156. 
Disponível em: https://revistas.usp.br/esse/article/view/206156. Acesso em: 11 set. 2026.

## Como citar

```
BONIN, Gustavo. Esquemas Tensivos: espaço de intensidade (pontos e zonas) e
campo de presença [software]. Programa de Pós-Graduação em Linguística,
Universidade de São Paulo, 2026. Disponível em:
https://github.com/Bonin-gustavo/esquemas_semioticos
```

## Licença

- **Código** (`.py`): [MIT](LICENSE)
- **Documentação e imagens** (`README*.md`, `USO.md`, `exemplos/*.png`):
  [CC BY 4.0](LICENSE-CONTENT.md)
- **Fonte Crimson Pro** (`Crimson_Pro/`): [SIL OFL 1.1](Crimson_Pro/OFL.txt)

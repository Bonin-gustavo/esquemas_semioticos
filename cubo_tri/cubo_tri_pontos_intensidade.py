"""
cubo_tri_pontos_intensidade.py — Plotter dos pontos de intensidade
==================================================================
Espaço de 3 eixos (ainda só de INTENSIDADE — a extensidade fica para etapa
posterior) para as gradações — e, em cada espaço, os 4 pontos das diagonais
conversa e inversa — de um espaço de valor semiótico: fidúcia, veridicção,
manipulação ou competência.

Os CONTEÚDOS (gradações dos eixos x/z, espaços e percursos de exemplo) ficam
em `espacos.py` — edite LÁ para mudar as gradações ou criar um espaço novo.
Aqui fica só o plotter (a classe `CuboPontosIntensidade` e as fábricas).

Fábricas genéricas (aceitam o nome de qualquer espaço de espacos.py):
    pontos(nome)                  — três eixos completos, sem pontos
    pontos_diagonal(nome, tipo)   — + os 4 pontos de uma diagonal ("conversa", "inversa_1", "inversa_2")
    pontos_percurso(nome, zonas)  — + um percurso (seta) entre as zonas

Wrappers nomeados (os nomes públicos, um por espaço × variante):
    pontos_fiduciario() / _conversa() / _inversa_1() / _inversa_2() / _percurso_tres()
    pontos_veridictorio() / _conversa() / _inversa_1() / _inversa_2() / _percurso_dois()
    pontos_manipulacao() / _conversa() / _inversa_1() / _inversa_2() / _percurso_quatro()
    pontos_competencial() / _conversa() / _inversa_1() / _inversa_2() / _percurso_dois()
    pontos_puro() — o mais básico (só a intensidade rotulada)

Orientação (como no esboço à mão):
    INTENSIDADE : vertical, à ESQUERDA — a mesma em todo espaço
                  (demenos -> menos -> mais -> demais)
    eixo_z      : sobe à DIREITA  — MALEÁVEL (nome + 4 gradações, do – ao +)
    eixo_x      : desce à DIREITA — MALEÁVEL (nome + 4 gradações, do – ao +)

(A EXTENSIDADE fica reservada para etapa posterior — provável nível tensivo
distinto, mereceria 4º eixo/projeção própria.)

Baseado nos quadros autorais do pesquisador (U3/U4–U6), apoiados em
Fontanille & Zilberberg, *Tensão e Significação*.

Uso rápido
----------
    from cubo_tri_pontos_intensidade import pontos_fiduciario_conversa
    pontos_fiduciario_conversa().salvar("conversa.png")

    # espaço próprio, sem wrapper:
    from cubo_tri_pontos_intensidade import pontos_diagonal
    pontos_diagonal("fiduciario", "inversa_1").salvar("inv1.png")
"""
from __future__ import annotations
import pathlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from mpl_toolkits.mplot3d import proj3d
from PIL import Image

# Conteúdos (gradações, espaços, percursos, diagonais) — edite em espacos.py.
from espacos import (
    INTENSIDADE, CRENCA, CONFIANCA, PARECER, SER, QUERER, DEVER, PODER, SABER,
    ESPACOS, PERCURSOS, kw_espaco, diagonal,
)

# ----------------------------------------------------------------------
# Fonte — Crimson Pro (pasta irmã Crimson_Pro/, na raiz do capítulo),
# a mesma usada em todos os gráficos deste capítulo (ver campo_presenca/).
# ----------------------------------------------------------------------
_FONT_DIR = pathlib.Path(__file__).resolve().parent.parent / "Crimson_Pro" / "static"
for _nome in ("CrimsonPro-Regular.ttf", "CrimsonPro-Italic.ttf",
              "CrimsonPro-Medium.ttf", "CrimsonPro-MediumItalic.ttf",
              "CrimsonPro-SemiBold.ttf", "CrimsonPro-SemiBoldItalic.ttf",
              "CrimsonPro-Bold.ttf", "CrimsonPro-BoldItalic.ttf"):
    _caminho = _FONT_DIR / _nome
    if _caminho.exists():
        font_manager.fontManager.addfont(str(_caminho))
plt.rcParams["font.family"] = "Crimson Pro"

# matplotlib x  <- eixo_x (confiança por padrão)  — desce para a DIREITA
# matplotlib y  <- eixo_z (crença por padrão)     — sobe para a DIREITA
# matplotlib z  <- INTENSIDADE                    — vertical, à ESQUERDA

_COR_EIXO   = "0.15"
_COR_SIM    = "crimson"

# Cor de cada ponto/guia pela "temperatura" da INTENSIDADE (escala de fogo,
# a mesma usada nas zonas de cubo_tri_zonas_intensidade.py, que importa este dicionário):
# demais = vermelho (mais quente) → demenos = amarelo (mais frio). Assim,
# nas fábricas "_conversa"/"_inversa" (4 pontos, um por grau de
# intensidade), cada ponto — e suas guias pontilhadas — sai numa cor
# diferente, o que evita confundir os traçados quando eles se cruzam
# (como acontece nas "_inversa").
_COR_INTENSIDADE = {
    "demenos": "#F7C41F",   # amarelo-ouro (mais frio)
    "menos":   "#F2941A",   # laranja
    "mais":    "#E1571E",   # laranja-avermelhado
    "demais":  "#C4161C",   # vermelho (mais quente)
}


def _cor_por_intensidade(intensidade):
    """Resolve a cor de um ponto pela sua INTENSIDADE (str ou índice 0-3)."""
    label = intensidade if isinstance(intensidade, str) else INTENSIDADE[int(intensidade)]
    return _COR_INTENSIDADE.get(label, _COR_SIM)


def _quebrar_rotulo(texto, max_chars=10):
    """Quebra um rótulo em duas linhas, no espaço mais próximo do meio —
    usado só no rótulo mais longo de cada eixo (o do canto, i=0), pra não
    colidir com o eixo vizinho. Rótulos curtos saem sem quebra."""
    if len(texto) <= max_chars:
        return texto
    palavras = texto.split(" ")
    melhor_i, melhor_dif = 1, float("inf")
    for i in range(1, len(palavras)):
        acumulado = len(" ".join(palavras[:i]))
        dif = abs(acumulado - len(texto) / 2)
        if dif < melhor_dif:
            melhor_dif, melhor_i = dif, i
    return " ".join(palavras[:melhor_i]) + "\n" + " ".join(palavras[melhor_i:])


def _cortar_margem_branca(caminho, pad=20, limiar=250):
    """Recorta a margem branca ao redor do conteúdo de um PNG já salvo.

    Eixos 3D sem ticks (como os deste módulo) fazem `bbox_inches="tight"`
    quebrar no matplotlib (bug do mplot3d: bbox vazio) — em vez disso,
    salva normal e recorta o retrato aqui, direto no arquivo. Usado por
    `CuboPontosIntensidade.salvar()` e herdado por `CuboZonasIntensidade` (cubo_tri_zonas_intensidade.py)."""
    img = Image.open(caminho).convert("RGB")
    arr = np.asarray(img)
    nao_branco = (arr < limiar).any(axis=2)
    linhas = np.where(nao_branco.any(axis=1))[0]
    colunas = np.where(nao_branco.any(axis=0))[0]
    if linhas.size == 0 or colunas.size == 0:
        return
    topo    = max(int(linhas[0]) - pad, 0)
    base    = min(int(linhas[-1]) + pad, arr.shape[0])
    esq     = max(int(colunas[0]) - pad, 0)
    dir_    = min(int(colunas[-1]) + pad, arr.shape[1])
    img.crop((esq, topo, dir_, base)).save(caminho)


class Arrow3D(FancyArrowPatch):
    """Seta reta em 3D (para os percursos entre zonas).

    Recebe os pontos inicial e final em coordenadas de dados 3D e se
    reprojeta a cada desenho. arrowstyle "-|>" = uma ponta; "<|-|>" = duas.
    Usada por `CuboPontosIntensidade._add_percurso()` aqui e por `CuboZonasIntensidade`
    (cubo_tri_zonas_intensidade.py), que a importa deste módulo."""
    def __init__(self, xs, ys, zs, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, _ = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.get_proj())
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        return np.min(zs3d)


class CuboPontosIntensidade:
    def __init__(self, figsize=(9.5, 8.5), elev=18, azim=-25, titulo=None,
                 subtitulo=None,
                 eixo_x_nome="confiança (S/S)", eixo_x_labels=None,
                 eixo_z_nome="crença (S/O)", eixo_z_labels=None,
                 rotular_lados=True):
        """`eixo_x` (desce à direita) e `eixo_z` (sobe à direita) são os
        dois eixos maleáveis — nome do eixo + suas 4 gradações (do – ao +).
        Por padrão são confiança/crença (o cubo da fidúcia); passe outro
        par de nome+gradações pra outro espaço (ver pontos_veridictorio,
        pontos_manipulacao, pontos_competencial). A INTENSIDADE (linha
        vertical) não é maleável — é a mesma em todos os espaços.
        `rotular_lados=False` esconde o texto desses dois eixos, deixando
        só as 4 divisões (ver pontos_puro). `subtitulo`, se dado, sai menor e
        mais claro logo abaixo do `titulo` (usado pelas fábricas
        "_percurso_*", ex.: "Percurso - dois pontos")."""
        self.eixo_x_nome = eixo_x_nome
        self.eixo_x_labels = list(eixo_x_labels) if eixo_x_labels else list(CONFIANCA)
        self.eixo_z_nome = eixo_z_nome
        self.eixo_z_labels = list(eixo_z_labels) if eixo_z_labels else list(CRENCA)
        self.rotular_lados = rotular_lados

        self.fig = plt.figure(figsize=figsize)
        self.ax  = self.fig.add_subplot(111, projection="3d")
        self.ax.view_init(elev=elev, azim=azim)
        self.ax.set_proj_type("ortho")
        # ocupa quase toda a figura — o padrão do matplotlib reserva uma
        # margem grande demais, pensada pra eixos com ticks/rótulos, que
        # este gráfico não tem (ver salvar(): bbox_inches="tight" não
        # funciona com eixos 3D sem ticks). _add_legenda_zonas() (em
        # cubo_tri_zonas_intensidade.py) reajusta essa posição quando há tabela de legenda.
        self.ax.set_position([0.02, 0.02, 0.96, 0.90])
        self._montar_base()
        if titulo:
            # x=0.30, y=0.83 (não o padrão 0.5/0.95): com a câmera padrão
            # (elev=18, azim=-25) o "cubo" (só as 3 arestas a partir da
            # origem) ocupa sobretudo o canto inferior esquerdo da caixa
            # 3D — esse ponto fica logo acima do topo real do desenho
            # (o "+" da intensidade), não no topo/centro da figura inteira.
            self.fig.suptitle(titulo, fontsize=13, x=0.30, y=0.83)
        if subtitulo:
            self.fig.text(0.30, 0.795, subtitulo, fontsize=10, color="0.40",
                          ha="center", va="top")

    # ------------------------------------------------------------------
    # Camada base: eixos, ticks, rótulos das zonas, símbolos +/–
    # ------------------------------------------------------------------
    def _montar_base(self):
        ax = self.ax
        ax.set_xlim(0, 4); ax.set_ylim(0, 4); ax.set_zlim(0, 4)
        ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
        ax.set_xlabel(""); ax.set_ylabel(""); ax.set_zlabel("")
        for pane in (ax.xaxis, ax.yaxis, ax.zaxis):
            pane.pane.set_visible(False)
            pane.line.set_visible(False)
        ax.grid(False)

        # três eixos a partir da origem
        for (dx, dy, dz) in [(4, 0, 0), (0, 4, 0), (0, 0, 4)]:
            ax.plot([0, dx], [0, dy], [0, dz], color=_COR_EIXO, lw=1.6, zorder=1)

        # símbolos +/–
        ax.text(-0.15, -0.15, 0,   "–", fontsize=9, ha="center", va="center",
                color=_COR_SIM, zorder=9)
        ax.text(4.2,  0.0,   0,    "+", fontsize=9, ha="center", va="center",
                color=_COR_SIM, zorder=9)
        ax.text(0,    4.2,   0,    "+", fontsize=9, ha="center", va="center",
                color=_COR_SIM, zorder=9)
        ax.text(-0.15, -0.15, 4.0, "+", fontsize=9, ha="center", va="center",
                color=_COR_SIM, zorder=9)

        # 5 traços por eixo — fronteiras das 4 zonas
        tk = 0.12
        for i in range(5):
            ax.plot([i, i], [0, -tk], [0, 0],  color=_COR_EIXO, lw=1.0, zorder=2)
            ax.plot([0, -tk], [i, i], [0, 0],  color=_COR_EIXO, lw=1.0, zorder=2)
            ax.plot([0, -tk], [0, 0], [i, i],  color=_COR_EIXO, lw=1.0, zorder=2)

        # rótulos das zonas — centrados em i+0.5 (eixo x/z só se rotular_lados)
        if self.rotular_lados:
            for i, lab in enumerate(self.eixo_x_labels):
                txt = _quebrar_rotulo(lab) if i == 0 else lab
                ax.text(i + 0.5, -0.30, 0.06, txt, fontsize=6, ha="center",
                        va="top", zdir="x", zorder=8)
            for i, lab in enumerate(self.eixo_z_labels):
                txt = _quebrar_rotulo(lab) if i == 0 else lab
                ax.text(-0.005, i + 0.3, 0.06, txt, fontsize=6, ha="center",
                        va="bottom", zdir="y", zorder=8)
        for i, lab in enumerate(INTENSIDADE):
            ax.text(-0.12, 0, i + 0.5, lab, fontsize=6, ha="right",
                    va="center", zorder=8)

        try:
            ax.set_box_aspect((1, 1, 1))
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Camada opcional: títulos grandes dos eixos
    # ------------------------------------------------------------------
    def _add_titulos(self):
        ax = self.ax
        ax.text(2.0, -0.85, 0.06, self.eixo_x_nome, fontsize=11, ha="center",
                va="top", zdir="x", zorder=8)
        ax.text(-0.10, 2.0, 0.18, self.eixo_z_nome, fontsize=11, ha="center",
                zdir="y", zorder=8)
        ax.text2D(0.05, 0.50, "intensidade", fontsize=11, ha="center",
                  va="center", rotation=90, transform=ax.transAxes, zorder=8)

    # ------------------------------------------------------------------
    # Zonas: célula (crença/eixo_z × confiança/eixo_x × intensidade) —
    # cantos e centro em coordenadas de dados. Base para _add_ponto() aqui
    # e para grade/zonas/percurso em CuboZonasIntensidade (cubo_tri_zonas_intensidade.py).
    # ------------------------------------------------------------------
    def _cantos_zona(self, crenca, confianca, intensidade):
        """(x0,x1,y0,y1,z0,z1) da célula. Aceita str ou índice 0-3.
        Usa as gradações desta instância (self.eixo_x_labels/eixo_z_labels),
        não as globais — importa se o cubo foi criado com outro par de eixos."""
        def _i(v, escala):
            return escala.index(v) if isinstance(v, str) else int(v)
        x0 = _i(confianca,   self.eixo_x_labels)
        y0 = _i(crenca,      self.eixo_z_labels)
        z0 = _i(intensidade, INTENSIDADE)
        return x0, x0 + 1, y0, y0 + 1, z0, z0 + 1

    def _centro_zona(self, crenca, confianca, intensidade):
        """Ponto central (meio) da célula, em coordenadas de dados."""
        x0, x1, y0, y1, z0, z1 = self._cantos_zona(crenca, confianca, intensidade)
        return ((x0 + x1) / 2.0, (y0 + y1) / 2.0, (z0 + z1) / 2.0)

    # ------------------------------------------------------------------
    # Ponto: marca o centro de UMA célula (zona) + guias de leitura até
    # os três eixos (não é um percurso — sem seta, sem ligar a outro ponto)
    # ------------------------------------------------------------------
    def _add_ponto(self, crenca, confianca, intensidade, rotulo=None, cor=None,
                   desloc=(0.10, 0.10, 0.25), ha="left", va="bottom", fontsize=8.5):
        """Marca o centro da célula (eixo_z=crenca, eixo_x=confianca,
        intensidade) com um ponto e traça as guias pontilhadas de leitura
        até cada um dos três eixos. `rotulo`, se dado, vai ao lado do ponto
        (deslocado por `desloc`). `cor`, se omitida, sai pela "temperatura"
        da intensidade (`_cor_por_intensidade`) — cada um dos 4 pontos das
        fábricas "_conversa"/"_inversa" (um por grau) sai numa cor
        diferente, o que ajuda a não confundir os traçados quando eles se
        cruzam (como nas "_inversa")."""
        ax = self.ax
        ax.computed_zorder = False
        cor = cor or _cor_por_intensidade(intensidade)
        x, y, z = self._centro_zona(crenca, confianca, intensidade)

        guia = dict(color=cor, lw=0.9, ls=":", dashes=(1.5, 2.5), zorder=5, alpha=0.95)
        # até o eixo_x (confiança/parecer/querer/poder):  P -> (x,y,0) -> (x,0,0)
        ax.plot([x, x], [y, y], [z, 0], **guia)
        ax.plot([x, x], [y, 0], [0, 0], **guia)
        # até o eixo_z (crença/ser/dever/saber):           (x,y,0) -> (0,y,0)
        ax.plot([x, 0], [y, y], [0, 0], **guia)
        # até o eixo da intensidade:                       P -> (0,y,z) -> (0,0,z)
        ax.plot([x, 0], [y, y], [z, z], **guia)
        ax.plot([0, 0], [y, 0], [z, z], **guia)

        ax.scatter([x], [y], [z], s=70, color=cor, edgecolor="white",
                   linewidth=0.8, zorder=10, depthshade=False)
        if rotulo:
            dx, dy, dz = desloc
            ax.text(x + dx, y + dy, z + dz, rotulo, fontsize=fontsize,
                    color="0.15", ha=ha, va=va, zorder=11)
        return x, y, z

    # ------------------------------------------------------------------
    # Percurso: liga os CENTROS de 2+ zonas por uma linha com seta(s) —
    # diferente de _add_ponto(), que marca um ponto isolado (sem ligar a
    # outro). Usado pelas fábricas "_percurso_*" aqui e por CuboZonasIntensidade
    # (cubo_tri_zonas_intensidade.py), que soma zonas destacadas + legenda em cima disso.
    # ------------------------------------------------------------------
    def _add_percurso(self, zonas_seq, bidirecional=False, cor_linha="0.12",
                      lw=1.8, escala_seta=13):
        """Traça o percurso: liga os centros das zonas, na ordem dada.

        A linha começa e termina no MEIO de cada zona (nunca nos vértices).
        Uma seta por trecho: unidirecional (->) mostra o sentido; bidirecional
        (<->) indica ida e volta. Aceita de 2 zonas em diante."""
        ax = self.ax
        ax.computed_zorder = False
        centros = [self._centro_zona(cr, co, it) for (cr, co, it) in zonas_seq]
        estilo = "<|-|>" if bidirecional else "-|>"
        for a, b in zip(centros[:-1], centros[1:]):
            seta = Arrow3D([a[0], b[0]], [a[1], b[1]], [a[2], b[2]],
                           arrowstyle=estilo, mutation_scale=escala_seta,
                           lw=lw, color=cor_linha, zorder=8,
                           shrinkA=0, shrinkB=0)
            ax.add_artist(seta)

    # ------------------------------------------------------------------
    def salvar(self, caminho, dpi=300):
        self.fig.savefig(caminho, dpi=dpi)
        _cortar_margem_branca(caminho)
        return caminho


# ----------------------------------------------------------------------
# Fábricas genéricas — o corpo comum; os wrappers nomeados vêm abaixo.
# ----------------------------------------------------------------------
def pontos(nome, **kw) -> CuboPontosIntensidade:
    """Espaço `nome` com os três eixos completos (sem pontos)."""
    kw = {**kw_espaco(nome), **kw}
    c = CuboPontosIntensidade(**kw)
    c._add_titulos()
    return c


def pontos_diagonal(nome, tipo, **kw) -> CuboPontosIntensidade:
    """Espaço `nome` + os 4 pontos da diagonal `tipo` ("conversa",
    "inversa_1" ou "inversa_2"), com guias de leitura até os três eixos."""
    kw = {**kw_espaco(nome), **kw}
    c = CuboPontosIntensidade(**kw)
    c._add_titulos()
    for eixo_z, eixo_x, intensidade in diagonal(nome, tipo):
        c._add_ponto(eixo_z, eixo_x, intensidade)
    return c


def pontos_percurso(nome, zonas, **kw) -> CuboPontosIntensidade:
    """Espaço `nome` + pontos + um percurso ligando os centros de `zonas`
    por seta (ver `_add_percurso`)."""
    kw = {**kw_espaco(nome), **kw}
    c = CuboPontosIntensidade(**kw)
    c._add_titulos()
    for eixo_z, eixo_x, intensidade in zonas:
        c._add_ponto(eixo_z, eixo_x, intensidade)
    c._add_percurso(zonas)
    return c


# ----------------------------------------------------------------------
# Wrappers nomeados — os nomes públicos (um por espaço × variante).
# ----------------------------------------------------------------------
def pontos_puro(**kw) -> CuboPontosIntensidade:
    """O mais básico de todos: só a intensidade rotulada e os símbolos +/–;
    os outros dois eixos mostram apenas as 4 divisões."""
    kw.setdefault("rotular_lados", False)
    c = CuboPontosIntensidade(**kw)
    return c


# Fiduciário — confiança (S/S) × crença (S/O)
def pontos_fiduciario(**kw) -> CuboPontosIntensidade:
    """Espaço fiduciário: confiança (S/S) × crença (S/O) × intensidade."""
    return pontos("fiduciario", **kw)


def pontos_fiduciario_conversa(**kw) -> CuboPontosIntensidade:
    """Espaço fiduciário + os 4 pontos da diagonal conversa."""
    return pontos_diagonal("fiduciario", "conversa", **kw)


def pontos_fiduciario_inversa_1(**kw) -> CuboPontosIntensidade:
    """Espaço fiduciário + a 1ª diagonal inversa (eixo_x desce)."""
    return pontos_diagonal("fiduciario", "inversa_1", **kw)


def pontos_fiduciario_inversa_2(**kw) -> CuboPontosIntensidade:
    """Espaço fiduciário + a 2ª diagonal inversa (eixo_z desce)."""
    return pontos_diagonal("fiduciario", "inversa_2", **kw)


def pontos_fiduciario_percurso_tres(**kw) -> CuboPontosIntensidade:
    """Espaço fiduciário com um percurso de 3 pontos."""
    return pontos_percurso("fiduciario", PERCURSOS["fiduciario"]["percurso_tres"], **kw)


# Veridictório — parecer × ser
def pontos_veridictorio(**kw) -> CuboPontosIntensidade:
    """Espaço veridictório: parecer × ser × intensidade."""
    return pontos("veridictorio", **kw)


def pontos_veridictorio_conversa(**kw) -> CuboPontosIntensidade:
    """Espaço veridictório + os 4 pontos da diagonal conversa."""
    return pontos_diagonal("veridictorio", "conversa", **kw)


def pontos_veridictorio_inversa_1(**kw) -> CuboPontosIntensidade:
    """Espaço veridictório + a 1ª diagonal inversa (eixo_x desce)."""
    return pontos_diagonal("veridictorio", "inversa_1", **kw)


def pontos_veridictorio_inversa_2(**kw) -> CuboPontosIntensidade:
    """Espaço veridictório + a 2ª diagonal inversa (eixo_z desce)."""
    return pontos_diagonal("veridictorio", "inversa_2", **kw)


def pontos_veridictorio_percurso_dois(**kw) -> CuboPontosIntensidade:
    """Espaço veridictório com um percurso de 2 pontos."""
    return pontos_percurso("veridictorio", PERCURSOS["veridictorio"]["percurso_dois"], **kw)


# Manipulação — querer × dever
def pontos_manipulacao(**kw) -> CuboPontosIntensidade:
    """Espaço de manipulação: querer × dever × intensidade."""
    return pontos("manipulacao", **kw)


def pontos_manipulacao_conversa(**kw) -> CuboPontosIntensidade:
    """Espaço de manipulação + os 4 pontos da diagonal conversa."""
    return pontos_diagonal("manipulacao", "conversa", **kw)


def pontos_manipulacao_inversa_1(**kw) -> CuboPontosIntensidade:
    """Espaço de manipulação + a 1ª diagonal inversa (eixo_x desce)."""
    return pontos_diagonal("manipulacao", "inversa_1", **kw)


def pontos_manipulacao_inversa_2(**kw) -> CuboPontosIntensidade:
    """Espaço de manipulação + a 2ª diagonal inversa (eixo_z desce)."""
    return pontos_diagonal("manipulacao", "inversa_2", **kw)


def pontos_manipulacao_percurso_quatro(**kw) -> CuboPontosIntensidade:
    """Espaço de manipulação com um percurso de 4 pontos."""
    return pontos_percurso("manipulacao", PERCURSOS["manipulacao"]["percurso_quatro"], **kw)


# Competencial — poder × saber
def pontos_competencial(**kw) -> CuboPontosIntensidade:
    """Espaço competencial: poder × saber × intensidade."""
    return pontos("competencial", **kw)


def pontos_competencial_conversa(**kw) -> CuboPontosIntensidade:
    """Espaço competencial + os 4 pontos da diagonal conversa."""
    return pontos_diagonal("competencial", "conversa", **kw)


def pontos_competencial_inversa_1(**kw) -> CuboPontosIntensidade:
    """Espaço competencial + a 1ª diagonal inversa (eixo_x desce)."""
    return pontos_diagonal("competencial", "inversa_1", **kw)


def pontos_competencial_inversa_2(**kw) -> CuboPontosIntensidade:
    """Espaço competencial + a 2ª diagonal inversa (eixo_z desce)."""
    return pontos_diagonal("competencial", "inversa_2", **kw)


def pontos_competencial_percurso_dois(**kw) -> CuboPontosIntensidade:
    """Espaço competencial com um percurso de 2 pontos."""
    return pontos_percurso("competencial", PERCURSOS["competencial"]["percurso_dois"], **kw)


# ----------------------------------------------------------------------
if __name__ == "__main__":
    pontos_puro().salvar("pontos_puro.png")
    print("salvo: pontos_puro.png")
    pontos_fiduciario().salvar("pontos_fiduciario.png")
    print("salvo: pontos_fiduciario.png")
    pontos_fiduciario_conversa().salvar("pontos_fiduciario_conversa.png")
    print("salvo: pontos_fiduciario_conversa.png")
    pontos_fiduciario_inversa_1().salvar("pontos_fiduciario_inversa_1.png")
    print("salvo: pontos_fiduciario_inversa_1.png")
    pontos_fiduciario_inversa_2().salvar("pontos_fiduciario_inversa_2.png")
    print("salvo: pontos_fiduciario_inversa_2.png")
    pontos_veridictorio().salvar("pontos_veridictorio.png")
    print("salvo: pontos_veridictorio.png")
    pontos_veridictorio_conversa().salvar("pontos_veridictorio_conversa.png")
    print("salvo: pontos_veridictorio_conversa.png")
    pontos_veridictorio_inversa_1().salvar("pontos_veridictorio_inversa_1.png")
    print("salvo: pontos_veridictorio_inversa_1.png")
    pontos_veridictorio_inversa_2().salvar("pontos_veridictorio_inversa_2.png")
    print("salvo: pontos_veridictorio_inversa_2.png")
    pontos_manipulacao().salvar("pontos_manipulacao.png")
    print("salvo: pontos_manipulacao.png")
    pontos_manipulacao_conversa().salvar("pontos_manipulacao_conversa.png")
    print("salvo: pontos_manipulacao_conversa.png")
    pontos_manipulacao_inversa_1().salvar("pontos_manipulacao_inversa_1.png")
    print("salvo: pontos_manipulacao_inversa_1.png")
    pontos_manipulacao_inversa_2().salvar("pontos_manipulacao_inversa_2.png")
    print("salvo: pontos_manipulacao_inversa_2.png")
    pontos_competencial().salvar("pontos_competencial.png")
    print("salvo: pontos_competencial.png")
    pontos_competencial_conversa().salvar("pontos_competencial_conversa.png")
    print("salvo: pontos_competencial_conversa.png")
    pontos_competencial_inversa_1().salvar("pontos_competencial_inversa_1.png")
    print("salvo: pontos_competencial_inversa_1.png")
    pontos_competencial_inversa_2().salvar("pontos_competencial_inversa_2.png")
    print("salvo: pontos_competencial_inversa_2.png")

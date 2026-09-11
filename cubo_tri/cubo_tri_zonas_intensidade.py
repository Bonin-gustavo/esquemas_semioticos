"""
cubo_tri_zonas_intensidade.py — grades, zonas destacadas e percursos de intensidade
=====================================================
Estende `CuboPontosIntensidade` (cubo_tri_pontos_intensidade.py) com a grade 4×4×4, zonas destacadas
(com legenda em tabela) e percursos entre zonas. Por padrão trabalha no
espaço da fidúcia (confiança × crença × intensidade); passe `eixo_x_nome`/
`eixo_x_labels`/`eixo_z_nome`/`eixo_z_labels` (ver cubo_tri_pontos_intensidade.py) para os
outros espaços: veridicção, manipulação, competência.

Versões disponíveis
-------------------
    zonas_grade()           — grade completa 4×4×4 tracejada
    zonas_faces_parcial()   — grade só nas 3 faces visíveis (frente, lateral dir., topo)
    zonas_faces_completo()  — grade completa em todos os cruzamentos
    zonas_zona_parcial()    — faces parciais + uma ou várias zonas destacadas
    zonas_zona_completo()   — grade completa + uma ou várias zonas destacadas
    zonas_percurso()        — zonas destacadas + um ou vários percursos (com seta)

Uso rápido
----------
    from cubo_tri_zonas_intensidade import zonas_faces_parcial, zonas_zona_parcial
    zonas_faces_parcial().salvar("faces.png")
    zonas_zona_parcial(("crê totalmente", "confia totalmente", "demais")).salvar("zona.png")
"""
from __future__ import annotations
import itertools
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from cubo_tri_pontos_intensidade import CuboPontosIntensidade, Arrow3D, _COR_INTENSIDADE
from espacos import INTENSIDADE

# Paleta de cores claras para múltiplas zonas (cor matplotlib, nome em português)
_PALETA_ZONAS = [
    ("lightblue",   "azul claro"),
    ("lightgreen",  "verde claro"),
    ("lightyellow", "amarelo claro"),
    ("lightpink",   "rosa claro"),
    ("peachpuff",   "pêssego"),
    ("plum",        "lilás"),
    ("lightcyan",   "ciano claro"),
    ("lavender",    "lavanda"),
]

# _COR_INTENSIDADE (cor da zona pela "temperatura" da INTENSIDADE — demais =
# vermelho/mais quente ... demenos = amarelo/mais frio) e Arrow3D (seta reta
# em 3D usada pelos percursos) vêm de cubo_tri_pontos_intensidade.py — a primeira também colore
# os pontos das fábricas "_conversa"/"_inversa"; a segunda também é usada
# por `CuboPontosIntensidade._add_percurso()`, herdado aqui por `CuboZonasIntensidade`.


class CuboZonasIntensidade(CuboPontosIntensidade):
    """CuboPontosIntensidade + grade 4×4×4, zonas destacadas e percursos."""

    # ------------------------------------------------------------------
    # Camada opcional: grade completa 4×4×4 (todos os cruzamentos de zonas)
    # 5 planos por eixo × 5 linhas por plano × 3 direções = 75 linhas
    # ------------------------------------------------------------------
    def _add_grade_cubo(self):
        ax = self.ax
        kw = dict(color="0.72", lw=0.5, ls="--", dashes=(3, 3), zorder=0)
        for s in range(5):       # 0,1,2,3,4
            for t in range(5):
                ax.plot([0, 4], [s, s], [t, t], **kw)   # linhas em x
                ax.plot([s, s], [0, 4], [t, t], **kw)   # linhas em y
                ax.plot([s, s], [t, t], [0, 4], **kw)   # linhas em z

    # ------------------------------------------------------------------
    # Camada opcional: grade apenas nas 3 faces externas visíveis (parcial)
    # Com azim=-25, elev=18: frente (y=0), lateral direita (x=4), topo (z=4)
    # ------------------------------------------------------------------
    def _add_faces_parcial(self):
        ax = self.ax
        kw = dict(color="0.72", lw=0.5, ls="--", dashes=(3, 3), zorder=0)
        v = range(5)   # 0,1,2,3,4
        # face superior (z=4): grade em x e y
        for s in v:
            ax.plot([0, 4], [s, s], [4, 4], **kw)
            ax.plot([s, s], [0, 4], [4, 4], **kw)
        # face lateral direita crença-intensidade (x=4): grade em y e z
        for s in v:
            ax.plot([4, 4], [0, 4], [s, s], **kw)
            ax.plot([4, 4], [s, s], [0, 4], **kw)
        # face frente confiança-intensidade (y=0): grade em x e z
        for s in v:
            ax.plot([0, 4], [0, 0], [s, s], **kw)
            ax.plot([s, s], [0, 0], [0, 4], **kw)

    # ------------------------------------------------------------------
    # Camada opcional: grade completa nas 3 faces (todos os cruzamentos)
    # ------------------------------------------------------------------
    def _add_faces_completo(self):
        self._add_grade_cubo()

    # ------------------------------------------------------------------
    # Camada opcional: pinta UMA ou várias células (zonas) do cubo
    # ------------------------------------------------------------------
    def _faces_zona(self, crenca, confianca, intensidade):
        """Vértices das 6 faces da célula (crença × confiança × intensidade). Aceita str ou índice 0-3."""
        x0, x1, y0, y1, z0, z1 = self._cantos_zona(crenca, confianca, intensidade)
        V = list(itertools.product([x0, x1], [y0, y1], [z0, z1]))
        return [
            [V[0], V[1], V[3], V[2]],
            [V[4], V[5], V[7], V[6]],
            [V[0], V[1], V[5], V[4]],
            [V[2], V[3], V[7], V[6]],
            [V[0], V[2], V[6], V[4]],
            [V[1], V[3], V[7], V[5]],
        ]

    def _arestas_zona(self, crenca, confianca, intensidade):
        """As 12 arestas da célula, cada uma como par de pontos ((x,y,z),(x,y,z))."""
        x0, x1, y0, y1, z0, z1 = self._cantos_zona(crenca, confianca, intensidade)
        xs, ys, zs = (x0, x1), (y0, y1), (z0, z1)
        arestas = []
        # arestas paralelas a cada eixo, variando os outros dois
        for b in ys:
            for c in zs:
                arestas.append(((x0, b, c), (x1, b, c)))   # ao longo de x
        for a in xs:
            for c in zs:
                arestas.append(((a, y0, c), (a, y1, c)))   # ao longo de y
        for a in xs:
            for b in ys:
                arestas.append(((a, b, z0), (a, b, z1)))   # ao longo de z
        return arestas

    @staticmethod
    def _cor_aresta(cor, fator=0.55):
        """Versão mais escura/saturada da cor de preenchimento, p/ o contorno."""
        r, g, b = mcolors.to_rgb(cor)
        return (r * fator, g * fator, b * fator)

    def _add_zonas(self, entradas, alpha=0.40):
        """Desenha as zonas: preenchimento translúcido + contorno sempre visível.

        As zonas podem se ocluir na projeção (uma célula fica atrás de
        outra e some parcialmente — não é erro de fronteira, é a
        perspectiva). Para que a extensão completa de cada zona continue
        legível, o preenchimento vai numa Poly3DCollection translúcida e
        o contorno (12 arestas) é traçado por cima, com zorder alto e
        computed_zorder desligado, de modo que a silhueta de cada cubo
        apareça mesmo quando seu preenchimento é encoberto.
        """
        ax = self.ax
        ax.computed_zorder = False

        todas_faces, cores = [], []
        for cor, crenca, confianca, intensidade in entradas:
            faces = self._faces_zona(crenca, confianca, intensidade)
            todas_faces.extend(faces)
            cores.extend([cor] * len(faces))
        pc = Poly3DCollection(todas_faces, facecolor=cores, edgecolor="none",
                              alpha=alpha, zorder=3)
        ax.add_collection3d(pc)

        for cor, crenca, confianca, intensidade in entradas:
            cor_borda = self._cor_aresta(cor)
            for (p0, p1) in self._arestas_zona(crenca, confianca, intensidade):
                ax.plot([p0[0], p1[0]], [p0[1], p1[1]], [p0[2], p1[2]],
                        color=cor_borda, lw=1.3, zorder=6)

    # ------------------------------------------------------------------
    # _add_percurso() (liga os centros das zonas por uma linha com seta)
    # vem de CuboPontosIntensidade (cubo_tri_pontos_intensidade.py) — usada aqui tal como está.
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # Legenda das zonas — TABELA na lateral direita, alinhada ao cubo
    # ------------------------------------------------------------------
    def _add_legenda_zonas(self, entradas, alpha=0.40, seta=None):
        """Legenda em forma de tabela, colada à direita e centrada no cubo.

        entradas: lista de (cor, crenca, confianca, intensidade)
        Colunas: intensidade | <eixo_x> | <eixo_z> (uma linha por zona), onde
        eixo_x/eixo_z são os nomes curtos dos eixos do espaço em uso
        (confiança/crença na fidúcia, poder/saber no competencial, etc.);
        o quadradinho de cor de cada zona fica à esquerda da sua linha.
        A tabela é centrada verticalmente no conjunto de zonas para que
        cubo e legenda componham um único bloco (não fica acima do cubo).
        As linhas são empilhadas pela INTENSIDADE (demenos embaixo → demais
        em cima), alinhadas ao eixo vertical do cubo.

        seta: None (sem seta) | "uni" (->) | "bi" (<->). Quando dado, traça
        ao lado dos quadradinhos uma seta da 1ª zona do percurso à última —
        para cima se o percurso é ascendente, para baixo se descendente.
        """
        ax  = self.ax
        fig = self.fig

        # comprime o gráfico 3D para a esquerda, abrindo espaço p/ a tabela
        ax.set_position([0.00, 0.00, 0.63, 1.00])
        fig.canvas.draw()   # garante a matriz de projeção atualizada

        # centro do conjunto de zonas → fração da FIGURA (p/ alinhar vertical)
        cs = [self._cantos_zona(cr, co, it) for _, cr, co, it in entradas]
        cx = np.mean([(c[0] + c[1]) / 2 for c in cs])
        cy = np.mean([(c[2] + c[3]) / 2 for c in cs])
        cz = np.mean([(c[4] + c[5]) / 2 for c in cs])
        x2, y2, _ = proj3d.proj_transform(cx, cy, cz, ax.get_proj())
        _, fy = fig.transFigure.inverted().transform(ax.transData.transform((x2, y2)))

        # geometria da tabela (fração da FIGURA)
        # colunas refletem o espaço em uso (fidúcia, veridicção, manipulação
        # ou competência): nome curto de cada eixo, sem o qualificador
        # "(S/S)"/"(S/O)" da fidúcia.
        eixo_x_curto = self.eixo_x_nome.split(" (")[0]
        eixo_z_curto = self.eixo_z_nome.split(" (")[0]
        headers   = ["intensidade", eixo_x_curto, eixo_z_curto]
        col_w     = [0.080, 0.110, 0.090]             # larguras das 3 colunas
        sw_w      = 0.022                             # quadradinho de cor
        row_h     = 0.048
        x0        = 0.705                             # borda esquerda do bloco de texto
        bounds    = [x0]
        for w in col_w:
            bounds.append(bounds[-1] + w)
        x1        = bounds[-1]                        # borda direita

        n         = len(entradas)
        total_h   = (n + 1) * row_h                   # cabeçalho + n linhas
        y_top     = fy + total_h / 2.0                # centrado no cubo
        y_bot     = y_top - total_h

        kw = dict(color="0.45", lw=0.8, transform=fig.transFigure,
                  clip_on=False, zorder=20)

        # linhas horizontais e verticais da tabela (em coords de figura)
        for k in range(n + 2):
            y = y_top - k * row_h
            fig.add_artist(mlines.Line2D([x0, x1], [y, y], **kw))
        for x in bounds:
            fig.add_artist(mlines.Line2D([x, x], [y_top, y_bot], **kw))

        # cabeçalho
        for j, h in enumerate(headers):
            xc = (bounds[j] + bounds[j + 1]) / 2.0
            fig.text(xc, y_top - row_h / 2.0, h, fontsize=8, fontweight="bold",
                     ha="center", va="center", zorder=21)

        # linhas de dados + quadradinho de cor à esquerda de cada linha.
        # As linhas são empilhadas pela INTENSIDADE (demenos embaixo → demais
        # em cima), correspondendo ao eixo vertical do cubo; a direção do
        # percurso fica marcada pela SETA, não pela posição das linhas.
        linhas = sorted(entradas, key=lambda e: _idx_intensidade(e[3]), reverse=True)
        for i, (cor, crenca, confianca, intensidade) in enumerate(linhas):
            yc = y_top - row_h - (i + 0.5) * row_h
            for j, v in enumerate([intensidade, confianca, crenca]):
                xc = (bounds[j] + bounds[j + 1]) / 2.0
                fig.text(xc, yc, v, fontsize=7, ha="center", va="center", zorder=21)
            fig.add_artist(mpatches.Rectangle(
                (x0 - sw_w - 0.008, yc - row_h * 0.32), sw_w, row_h * 0.64,
                facecolor=cor, edgecolor=self._cor_aresta(cor), lw=0.9,
                alpha=alpha, transform=fig.transFigure, clip_on=False, zorder=21))

        # seta do percurso: vai da 1ª zona do percurso à última (à esquerda
        # dos quadradinhos). Ascendente sobe (embaixo → em cima); descendente
        # desce (em cima → embaixo).
        if seta in ("uni", "bi") and n >= 2:
            x_seta = (x0 - sw_w - 0.008) - 0.018
            y_prim  = y_top - 1.5 * row_h            # centro da linha de cima
            y_ult   = y_top - (n + 0.5) * row_h      # centro da linha de baixo
            ascendente = _idx_intensidade(entradas[0][3]) < _idx_intensidade(entradas[-1][3])
            y_ini, y_fim = (y_ult, y_prim) if ascendente else (y_prim, y_ult)
            estilo = "<|-|>" if seta == "bi" else "-|>"
            fig.add_artist(FancyArrowPatch(
                (x_seta, y_ini), (x_seta, y_fim),
                arrowstyle=estilo, mutation_scale=11, lw=1.6, color="0.10",
                transform=fig.transFigure, clip_on=False, zorder=24,
                shrinkA=0, shrinkB=0))


# ----------------------------------------------------------------------
# Helper interno: normaliza zonas e atribui cor pela temperatura da intensidade
# ----------------------------------------------------------------------
def _idx_intensidade(intensidade):
    """Índice 0-3 da intensidade (aceita rótulo ou índice)."""
    return INTENSIDADE.index(intensidade) if isinstance(intensidade, str) else int(intensidade)


def _preparar_zonas(zonas, cor_padrao=None):
    """Retorna lista de (cor, crenca, confianca, intensidade).

    A cor de cada zona é dada pela "temperatura" da sua INTENSIDADE
    (_COR_INTENSIDADE): demais = vermelho ... demenos = amarelo. Zonas na
    mesma intensidade recebem a mesma cor — a distinção entre elas fica por
    conta da posição e da legenda. `cor_padrao`, se dado, sobrepõe o mapa
    (mesma cor para todas as zonas).
    """
    if isinstance(zonas, tuple) and not isinstance(zonas[0], (tuple, list)):
        zonas = [zonas]

    def _cor_de(z):
        if cor_padrao is not None:
            return cor_padrao
        intensidade = z[2]
        return _COR_INTENSIDADE.get(intensidade, "lightblue")

    return [(_cor_de(z), *z) for z in zonas]


# ----------------------------------------------------------------------
# Helper interno: normaliza a especificação de percursos
# ----------------------------------------------------------------------
def _preparar_percursos(percursos):
    """Devolve lista de {"zonas": [...], "bidirecional": bool}.

    Aceita:
      - dict {"zonas": [...], "bidirecional": ...}          → 1 percurso
      - lista de zonas [(cr,co,it), (cr,co,it), ...]         → 1 percurso (uni)
      - lista de percursos (dicts e/ou listas de zonas)      → vários
    """
    def _eh_zona(x):
        return (isinstance(x, tuple) and len(x) == 3
                and all(isinstance(v, str) for v in x))

    if isinstance(percursos, dict):
        percursos = [percursos]
    elif isinstance(percursos, (list, tuple)) and percursos and _eh_zona(percursos[0]):
        percursos = [list(percursos)]          # percurso único dado como lista de zonas

    specs = []
    for p in percursos:
        if isinstance(p, dict):
            specs.append({"zonas": list(p["zonas"]),
                          "bidirecional": bool(p.get("bidirecional", False))})
        else:
            specs.append({"zonas": list(p), "bidirecional": False})
    return specs


# ----------------------------------------------------------------------
# Funções de fábrica — ponto de entrada público
# ----------------------------------------------------------------------
def zonas_grade(**kw) -> CuboZonasIntensidade:
    """Grade completa 4×4×4 tracejada."""
    c = CuboZonasIntensidade(**kw)
    c._add_grade_cubo()
    return c


def zonas_faces_parcial(**kw) -> CuboZonasIntensidade:
    """Grade tracejada apenas nas 3 faces visíveis: frente (y=0), lateral direita (x=4), topo (z=4)."""
    c = CuboZonasIntensidade(**kw)
    c._add_faces_parcial()
    return c


def zonas_faces_completo(**kw) -> CuboZonasIntensidade:
    """Grade tracejada completa em todos os cruzamentos do cubo 4×4×4."""
    c = CuboZonasIntensidade(**kw)
    c._add_faces_completo()
    return c


def zonas_zona_parcial(zonas, cor=None, alpha=0.40, **kw) -> CuboZonasIntensidade:
    """3 faces visíveis (parcial) + uma ou várias zonas destacadas com legenda.

    zonas: tupla (crenca, confianca, intensidade)  — zona única
           lista de tuplas                          — várias zonas
    cor:   None → cor pela temperatura da intensidade; ou força uma cor fixa.

    Exemplos:
        zonas_zona_parcial(("crê totalmente", "confia totalmente", "demais")).salvar("z.png")
        zonas_zona_parcial([("quase crê", "quase confia", "mais"),
                            ("crê totalmente", "confia totalmente", "demais")]).salvar("z.png")
    """
    kw.setdefault("figsize", (13, 8.5))   # largura extra p/ a tabela à direita
    c = CuboZonasIntensidade(**kw)
    c._add_faces_parcial()
    entradas = _preparar_zonas(zonas, cor)
    c._add_zonas(entradas, alpha=alpha)
    c._add_legenda_zonas(entradas, alpha=alpha)
    return c


def zonas_zona_completo(zonas, cor=None, alpha=0.40, **kw) -> CuboZonasIntensidade:
    """Grade completa 4×4×4 + uma ou várias zonas destacadas com legenda.

    zonas: tupla (crenca, confianca, intensidade)  — zona única
           lista de tuplas                          — várias zonas
    cor:   None → cor pela temperatura da intensidade; ou força uma cor fixa.
    """
    kw.setdefault("figsize", (13, 8.5))   # largura extra p/ a tabela à direita
    c = CuboZonasIntensidade(**kw)
    c._add_faces_completo()
    entradas = _preparar_zonas(zonas, cor)
    c._add_zonas(entradas, alpha=alpha)
    c._add_legenda_zonas(entradas, alpha=alpha)
    return c


def zonas_percurso(percursos, grade="completa", cor_linha="0.12",
                   alpha=0.40, **kw) -> CuboZonasIntensidade:
    """Zonas destacadas + percurso(s) ligando os CENTROS das zonas por seta.

    Um percurso é uma sequência ordenada de 2+ zonas. A linha vai do meio de
    uma zona ao meio da seguinte (nunca pelos vértices). Unidirecional mostra
    o sentido (->); bidirecional indica ida e volta (<->). O percurso pode
    andar por um ou vários eixos de uma vez — depende das zonas escolhidas.

    percursos:
        - lista de zonas [(cr,co,it), ...]                → 1 percurso (uni)
        - {"zonas": [...], "bidirecional": True/False}    → 1 percurso
        - lista de percursos (dicts e/ou listas de zonas) → vários
    grade: "completa" (4×4×4) ou "parcial" (3 faces visíveis)

    Exemplos:
        zonas_percurso([("não crê nada","não confia nada","demenos"),
                        ("crê totalmente","confia totalmente","demais")]).salvar("p.png")
        zonas_percurso({"zonas": [...], "bidirecional": True}).salvar("p.png")
    """
    kw.setdefault("figsize", (13, 8.5))
    c = CuboZonasIntensidade(**kw)
    if grade == "parcial":
        c._add_faces_parcial()
    else:
        c._add_faces_completo()

    specs = _preparar_percursos(percursos)
    # zonas únicas, na ordem de aparição → cubos + legenda
    zonas_todas = []
    for sp in specs:
        for z in sp["zonas"]:
            if z not in zonas_todas:
                zonas_todas.append(z)
    entradas = _preparar_zonas(zonas_todas)
    c._add_zonas(entradas, alpha=alpha)
    for sp in specs:
        c._add_percurso(sp["zonas"], bidirecional=sp["bidirecional"],
                        cor_linha=cor_linha)
    # seta na legenda: só faz sentido com um único percurso (ordem = linhas)
    if len(specs) == 1 and len(zonas_todas) == len(specs[0]["zonas"]):
        seta = "bi" if specs[0]["bidirecional"] else "uni"
    else:
        seta = None
    c._add_legenda_zonas(entradas, alpha=alpha, seta=seta)
    return c


# ----------------------------------------------------------------------
if __name__ == "__main__":
    zonas_faces_parcial().salvar("zonas_fiduciario_faces_parcial.png")
    print("salvo: zonas_fiduciario_faces_parcial.png")
    zonas_faces_completo().salvar("zonas_fiduciario_faces_completo.png")
    print("salvo: zonas_fiduciario_faces_completo.png")
    zonas_zona_parcial(("crê totalmente", "confia totalmente", "demais")).salvar("zonas_fiduciario_zona_parcial.png")
    print("salvo: zonas_fiduciario_zona_parcial.png")
    zonas_zona_completo(("crê totalmente", "confia totalmente", "demais")).salvar("zonas_fiduciario_zona_completo.png")
    print("salvo: zonas_fiduciario_zona_completo.png")

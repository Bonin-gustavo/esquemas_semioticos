"""
campo_presenca.py — Plotter do campo de presença (cruzamento inverso/converso
                     de intensidade e extensidade)
==============================================================================
Representação tensiva do cruzamento entre INTENSIDADE (eixo central vertical)
e EXTENSIDADE (eixos laterais), nas suas duas correlações canônicas:

    INVERSA  (esquerda) : quando a intensidade sobe, a extensidade desce.
                           Cone com a PONTA para cima e a BASE para baixo.
    CONVERSA (direita)  : quando a intensidade sobe, a extensidade sobe junto.
                           Cone com a BASE para cima e a PONTA para baixo.

Cada cone é cortado por 4 círculos em alturas igualmente espaçadas (1/4, 2/4,
3/4 e base = 4/4), dividindo-o em 4 recortes iguais — os mesmos 4 recortes
nomeados S1–S4 (do topo para a base) ao lado do cone da conversa, com linhas-
guia pontilhadas e delicadas ligando cada Si ao círculo que abre a sua faixa.

Baseado nos quadros autorais do pesquisador, apoiados em Fontanille &
Zilberberg, *Tensão e Significação*. Segue a mesma linguagem visual (preto/
cinza, sem preenchimento) e a mesma arquitetura (classe + fábricas + .salvar())
do módulo irmão `cubo_tri/cubo_tri_pontos_intensidade.py`.

Versões disponíveis
--------------------
    campo_zonas()               — "Campo de Presença Tensivo": sem colchetes,
                                  só as quatro zonas da intensidade (demenos/
                                  menos/mais/demais) marcadas no eixo central.
    campo_valores_zonas()       — "Campo de Presença Tensivo" / "Valores
                                  Tensivos": como campo_zonas(), acrescentando
                                  um colchete do lado de fora de cada eixo de
                                  extensidade — os quatro valores tensivos:
                                  absoluto/universo na inversa (esquerda),
                                  apogeu/abismo na conversa (direita).
    campo_direcoes_tensivas()   — "Campo de Presença Tensivo" / "Direções
                                  Tensivas": os colchetes de ascendência/
                                  descendência com os dois polos do ciclo
                                  (acontecimento/torpor) marcados, cada passo
                                  com seu incremento (ex.: recrudescimento
                                  via "mais mais") — evidenciando que cada
                                  rótulo é uma passagem entre polos, seguindo
                                  a Figura 1 (Direções tensivas para mais e
                                  para menos).

(Novas versões — com marcações, zonas ou exemplos aplicados — podem ser
acrescentadas depois como novas funções de fábrica, reaproveitando os métodos
privados da classe CampoPresenca.)

Uso rápido
----------
    from campo_presenca import campo_direcoes_tensivas
    campo_direcoes_tensivas().salvar("campo_presenca_direcoes_tensivas.png")
"""
from __future__ import annotations
import pathlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import font_manager

# ----------------------------------------------------------------------
# Fonte — Crimson Pro (pasta irmã Crimson_Pro/, na raiz do capítulo),
# a mesma usada em todos os gráficos deste capítulo.
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

# ----------------------------------------------------------------------
# Paleta / estilo — mesma linguagem do cubo_tri
# ----------------------------------------------------------------------
_COR_EIXO       = "0.15"    # linhas cheias (eixos, contorno do cone, base)
_COR_PONTILHADO = "0.45"    # círculos internos tracejados do cone
_COR_GUIA       = "0.55"    # linhas-guia delicadas (S1–S4 -> círculos)
_COR_CENTRO     = "0.65"    # linha de eixo interna do cone (tracejada, leve)
_COR_SIM        = "crimson" # símbolos + / -

_TRACEJADO_CIRCULO = (0, (2, 2))
_TRACEJADO_CENTRO  = (0, (1, 2))
_TRACEJADO_GUIA    = (0, (1, 2.5))

_ELLIPSE_RATIO = 0.28   # altura/largura das elipses (efeito de perspectiva)
_COR_MOVIMENTO   = "0.32"   # rótulos de processo (restabelecimento, atenuação...) — auxiliares, tom mais leve
_COR_INCREMENTO  = "0.42"   # rótulos de incremento (menos menos, somente mais...) — mais delicados que o nome


class CampoPresenca:
    """Espaço 2D para o cruzamento inverso/converso de intensidade x extensidade.

    Geometria interna (unidades arbitrárias, não são as escalas do cubo):
        H  = altura de cada cone e do eixo INT (0 a H)
        R  = raio (meia-largura) da base de cada cone
        X_INV / X_CONV = centro x dos cones inversa / conversa
    """

    def __init__(self, figsize=(13.0, 6.6), titulo=None, subtitulo=None,
                 H=3.0, R=1.35, dist_cones=7.4,
                 gap_ext=0.75, gap_label=0.50, gap_s=1.05,
                 y_titulo_eixo=-0.62, margem_topo=0.80, margem_base=0.90,
                 regua_s=True):
        self.H, self.R = H, R
        # se a régua S1-S4 do lado da conversa não for usada (campo_zonas),
        # a margem direita da figura não precisa reservar espaço pra ela.
        self._regua_s = regua_s
        # alturas dos 3 círculos internos (pontilhados), a 1/4, 2/4 e 3/4 de H
        self.alturas_internas = (H * 0.25, H * 0.5, H * 0.75)
        self.X_INV  = -dist_cones / 2
        self.X_CONV =  dist_cones / 2
        self.X_EXT_L = self.X_INV - R - gap_ext
        self.X_EXT_R = self.X_CONV + R + gap_ext
        self.X_LABEL_EXT_L = self.X_EXT_L - gap_label
        self.X_LABEL_EXT_R = self.X_EXT_R + gap_label
        self.X_S = self.X_LABEL_EXT_R + gap_s
        # y do título de cada eixo (intensidade/extensidade), logo abaixo do
        # "−"/"+" da base. campo_direcoes_tensivas() empurra isso mais para
        # baixo (via kwarg), para não se misturar com o rótulo do polo
        # "torpor" (_add_polos_ciclo), logo acima dele; campo_zonas() usa
        # o padrão, bem mais perto dos cones.
        self._Y_TITULO_EIXO = y_titulo_eixo
        self._margem_topo = margem_topo
        self._margem_base = margem_base

        self.fig, self.ax = plt.subplots(figsize=figsize)
        self._config_eixos()
        if titulo:
            y_titulo = 0.95 if subtitulo else 0.94
            self.fig.suptitle(titulo, fontsize=16, y=y_titulo, fontweight="bold")
            if subtitulo:
                self.fig.text(0.5, y_titulo - 0.06, subtitulo, fontsize=14,
                             ha="center", color="0.35", style="italic")

    # ------------------------------------------------------------------
    def _config_eixos(self):
        ax = self.ax
        x_max = self.X_S + 0.9 if self._regua_s else self.X_EXT_R + 0.9
        ax.set_xlim(self.X_EXT_L - 0.9, x_max)
        ax.set_ylim(-self._margem_base, self.H + self._margem_topo)
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_facecolor("white")
        self.fig.patch.set_facecolor("white")

    # ------------------------------------------------------------------
    # Um eixo vertical com seta dupla + símbolos +/- nas pontas
    # ------------------------------------------------------------------
    def _eixo_vertical(self, x, cima="+", baixo="−", cor=_COR_EIXO, lw=1.4):
        ax = self.ax
        ax.annotate("", xy=(x, self.H), xytext=(x, 0),
                    arrowprops=dict(arrowstyle="<->", color=cor, lw=lw),
                    zorder=5)
        ax.text(x, self.H + 0.30, cima, fontsize=28, fontweight="bold",
                ha="center", va="bottom", color=_COR_SIM, zorder=9)
        ax.text(x, -0.30, baixo, fontsize=28, fontweight="bold",
                ha="center", va="top", color=_COR_SIM, zorder=9)

    def _rotulo_deitado(self, x, texto, y=None, cor=_COR_EIXO, fontsize=13,
                        style="normal"):
        """Texto rotacionado 90°, 'deitado' ao longo de um eixo vertical.
        Por padrão centrado em y=H/2 (uso: rótulos INT./EXT./ASC./DESC.),
        mas aceita um y customizado (uso: rótulos de processo, centrados
        no meio do seu colchete).

        Leva um fundo branco discreto para não ser cortado por guias que
        cruzem essa altura (ex.: a linha S3, que passa por y=H/2).
        """
        y = self.H / 2 if y is None else y
        self.ax.text(x, y, texto, fontsize=fontsize, rotation=90,
                    ha="center", va="center", color=cor, zorder=8,
                    fontweight="medium", style=style,
                    bbox=dict(facecolor="white", edgecolor="none", pad=2))

    # ------------------------------------------------------------------
    # Título de um eixo (intensidade/extensidade): negrito, um pouco maior
    # que os rótulos de processo/polo — precisa se destacar claramente
    # deles (ex.: "intensidade" não pode se confundir com "torpor", logo
    # acima dela no gráfico das direções tensivas).
    # ------------------------------------------------------------------
    def _titulo_eixo(self, x, texto):
        self.ax.text(x, self._Y_TITULO_EIXO, texto, fontsize=15,
                    fontweight="bold", ha="center", va="top",
                    color=_COR_EIXO, zorder=8)

    # ------------------------------------------------------------------
    # Eixo central de INTENSIDADE — o título "intensidade" fica embaixo,
    # logo abaixo do "−" da seta (não mais deitado ao lado, como EXT.).
    # ------------------------------------------------------------------
    def _add_eixo_int(self):
        self._eixo_vertical(0.0, cima="+", baixo="−")
        self._titulo_eixo(0.0, "intensidade")

    # ------------------------------------------------------------------
    # Os dois polos do ciclo tensivo: acontecimento (intensidade máxima, "só
    # mais") no topo, torpor (intensidade mínima, "só menos") na base —
    # de onde partem/chegam as duas metades (ascendência/descendência) de
    # _add_movimentos_int(). Cada polo leva também o seu incremento (o
    # "somente mais"/"somente menos" da Figura 1), em itálico, mais perto
    # do "+"/"−"; o nome do processo (acontecimento/torpor) vem depois, mais
    # para fora. Ex.: "o restabelecimento é uma saída do torpor" — o
    # torpor precisa estar marcado para essa leitura fazer sentido.
    # ------------------------------------------------------------------
    def _add_polos_ciclo(self):
        ax, H = self.ax, self.H
        kw_nome = dict(fontsize=15.5, ha="center", color=_COR_MOVIMENTO, zorder=8)
        kw_inc  = dict(fontsize=9.5, ha="center", color=_COR_INCREMENTO,
                       style="italic", zorder=8)
        ax.text(0.0, H + 0.70, "somente mais", va="bottom", **kw_inc)
        ax.text(0.0, H + 0.90, "acontecimento", va="bottom", **kw_nome)
        ax.text(0.0, -0.70, "somente menos", va="top", **kw_inc)
        ax.text(0.0, -0.90, "torpor", va="top", **kw_nome)

    # ------------------------------------------------------------------
    # Colchete delicado cobrindo [y0, y1], abrindo para o lado da linha
    # central (abre_para="direita" p/ colchetes à esquerda do x=0, e
    # "esquerda" p/ colchetes à direita). Levemente recuado das duas
    # pontas (não toca 0/meio/H) para ficar sutil, sem competir com a
    # seta principal do INT nem com a seta ASC/DESC mais externa.
    # ------------------------------------------------------------------
    def _colchete(self, x, y0, y1, abre_para, cor=_COR_GUIA, lw=0.8,
                 tick=0.07, recuo=0.10):
        ax = self.ax
        sinal = 1 if abre_para == "direita" else -1
        y0, y1 = y0 + recuo, y1 - recuo
        ax.plot([x, x], [y0, y1], color=cor, lw=lw, zorder=5)
        ax.plot([x, x + sinal * tick], [y0, y0], color=cor, lw=lw, zorder=5)
        ax.plot([x, x + sinal * tick], [y1, y1], color=cor, lw=lw, zorder=5)

    # ------------------------------------------------------------------
    # Pequena seta indicativa de sentido (não é um eixo, só um ícone),
    # usada acima do colchete-mestre para marcar ascendência/descendência.
    # ------------------------------------------------------------------
    def _seta_pequena(self, x, y0, sobe, cor=_COR_EIXO, lw=1.1, comprimento=0.22):
        y1 = y0 + comprimento
        xy, xytext = ((x, y1), (x, y0)) if sobe else ((x, y0), (x, y1))
        self.ax.annotate("", xy=xy, xytext=xytext,
                        arrowprops=dict(arrowstyle="-|>", color=cor, lw=lw), zorder=5)

    # ------------------------------------------------------------------
    # Movimentos do eixo INT: dois colchetes finos e internos (um por
    # metade da linha). Cada metade leva DOIS rótulos deitados: o nome do
    # processo (mais perto do colchete, redondo) e o seu incremento — a
    # fórmula "mais/menos X mais/menos" da Figura 1 (mais para fora,
    # itálico). Mais para fora ainda, um colchete-mestre abraça os dois
    # processos juntos (do meio do de baixo ao meio do de cima); ao lado
    # dele fica "ascendência"/"descendência", com uma setinha colada
    # indicando o sentido do movimento.
    #   esquerda: torpor -[menos menos]-> restabelecimento
    #                     -[mais mais]--> recrudescimento -> acontecimento
    #                     = ascendência
    #   direita : acontecimento -[menos mais]-> atenuação
    #                            -[mais menos]-> minimização -> torpor
    #                            = descendência
    # ------------------------------------------------------------------
    def _add_movimentos_int(self, gap_colchete=0.40, gap_rotulo=0.22,
                            gap_incremento=0.26, gap_mestre=1.20,
                            gap_label_mestre=0.28, meia_altura_rotulo=0.38,
                            gap_seta=0.08):
        """meia_altura_rotulo: metade da extensão vertical aproximada do
        rótulo "ascendência"/"descendência" deitado — usada só para colar a
        setinha de sentido bem perto dele (acima, na ascendência; abaixo,
        na descendência), sem precisar medir a caixa de texto renderizada."""
        H = self.H
        meio = H / 2
        y_lo = meio / 2          # centro do par de baixo (restabelecimento/minimização)
        y_hi = (meio + H) / 2    # centro do par de cima (recrudescimento/atenuação)
        kw_proc = dict(fontsize=13, cor=_COR_MOVIMENTO, style="normal")
        kw_inc  = dict(fontsize=12, cor=_COR_INCREMENTO, style="italic")
        kw_mov  = dict(fontsize=12, cor=_COR_MOVIMENTO, style="italic")

        # -------- esquerda: ascendência --------
        x_col = -gap_colchete
        self._colchete(x_col, 0.0, meio, abre_para="direita")
        self._colchete(x_col, meio, H, abre_para="direita")
        x_proc = x_col - gap_rotulo
        x_inc = x_proc - gap_incremento
        self._rotulo_deitado(x_proc, "restabelecimento", y=y_lo, **kw_proc)
        self._rotulo_deitado(x_inc, "menos menos", y=y_lo, **kw_inc)
        self._rotulo_deitado(x_proc, "recrudescimento", y=y_hi, **kw_proc)
        self._rotulo_deitado(x_inc, "mais mais", y=y_hi, **kw_inc)

        x_mestre = -gap_mestre
        self._colchete(x_mestre, y_lo, y_hi, abre_para="direita",
                       cor=_COR_EIXO, lw=1.0, tick=0.09, recuo=0.0)
        x_mov = x_mestre - gap_label_mestre
        self._rotulo_deitado(x_mov, "ascendência", y=meio, **kw_mov)
        self._seta_pequena(x_mov, meio + meia_altura_rotulo + gap_seta, sobe=True)

        # -------- direita: descendência --------
        x_col = gap_colchete
        self._colchete(x_col, 0.0, meio, abre_para="esquerda")
        self._colchete(x_col, meio, H, abre_para="esquerda")
        x_proc = x_col + gap_rotulo
        x_inc = x_proc + gap_incremento
        self._rotulo_deitado(x_proc, "minimização", y=y_lo, **kw_proc)
        self._rotulo_deitado(x_inc, "mais menos", y=y_lo, **kw_inc)
        self._rotulo_deitado(x_proc, "atenuação", y=y_hi, **kw_proc)
        self._rotulo_deitado(x_inc, "menos mais", y=y_hi, **kw_inc)

        x_mestre = gap_mestre
        self._colchete(x_mestre, y_lo, y_hi, abre_para="esquerda",
                       cor=_COR_EIXO, lw=1.0, tick=0.09, recuo=0.0)
        x_mov = x_mestre + gap_label_mestre
        self._rotulo_deitado(x_mov, "descendência", y=meio, **kw_mov)
        seta_comprimento = 0.22
        self._seta_pequena(x_mov, meio - meia_altura_rotulo - gap_seta - seta_comprimento,
                           sobe=False, comprimento=seta_comprimento)

    # ------------------------------------------------------------------
    # Eixos laterais de EXTENSIDADE
    # (esquerda, ao lado da inversa: + embaixo, - em cima)
    # (direita, ao lado da conversa: + em cima, - embaixo)
    # ------------------------------------------------------------------
    def _add_eixos_ext(self):
        self._eixo_vertical(self.X_EXT_L, cima="−", baixo="+")
        self._titulo_eixo(self.X_EXT_L, "extensidade")

        self._eixo_vertical(self.X_EXT_R, cima="+", baixo="−")
        self._titulo_eixo(self.X_EXT_R, "extensidade")

    # ------------------------------------------------------------------
    # Um cone (inversa: ponta em cima / base embaixo | conversa: o inverso)
    # Devolve r_at(y): raio do cone na altura y — usado p/ as guias S1-S4.
    # ------------------------------------------------------------------
    def _add_cone(self, xc, tipo, titulo):
        ax, H, R = self.ax, self.H, self.R

        if tipo == "inversa":
            apex_y, base_y = H, 0.0
            r_at = lambda y: (H - y) / H * R
        else:  # "conversa"
            apex_y, base_y = 0.0, H
            r_at = lambda y: y / H * R

        # título acima do cone
        ax.text(xc, H + 0.55, titulo, fontsize=15, fontweight="bold",
                ha="center", va="bottom", color=_COR_EIXO, zorder=9)

        # lados do cone (contorno sólido)
        ax.plot([xc, xc - R], [apex_y, base_y], color=_COR_EIXO, lw=1.6, zorder=3)
        ax.plot([xc, xc + R], [apex_y, base_y], color=_COR_EIXO, lw=1.6, zorder=3)

        # eixo central do cone (tracejado, bem leve)
        ax.plot([xc, xc], [apex_y, base_y], color=_COR_CENTRO, lw=0.6,
                ls=_TRACEJADO_CENTRO, zorder=2)

        # 3 círculos internos pontilhados, a 1/4, 2/4 e 3/4 de H (dividem em 4 partes iguais)
        for y in self.alturas_internas:
            r = r_at(y)
            e = mpatches.Ellipse((xc, y), width=2 * r, height=2 * r * _ELLIPSE_RATIO,
                                  fill=False, edgecolor=_COR_PONTILHADO, lw=1.0,
                                  ls=_TRACEJADO_CIRCULO, zorder=4)
            ax.add_patch(e)

        # círculo da base — linha contínua
        e_base = mpatches.Ellipse((xc, base_y), width=2 * R, height=2 * R * _ELLIPSE_RATIO,
                                   fill=False, edgecolor=_COR_EIXO, lw=1.6, zorder=4)
        ax.add_patch(e_base)

        return r_at

    # ------------------------------------------------------------------
    # Régua S1-S4 ao lado da conversa: cada rótulo fica na altura do MEIO
    # do seu recorte (o trecho do cone entre dois círculos consecutivos),
    # com uma guia pontilhada e delicada até esse ponto médio na superfície
    # do cone — não até os círculos que o delimitam.
    # ------------------------------------------------------------------
    def _add_regua_s(self, r_at_conversa):
        ax = self.ax
        H, xc = self.H, self.X_CONV
        h1, h2, h3 = self.alturas_internas
        # fronteiras dos 4 recortes, do topo (base) até a ponta
        fronteiras = [H, h3, h2, h1, 0.0]
        for i, nome in enumerate(("S1", "S2", "S3", "S4")):
            y_meio = (fronteiras[i] + fronteiras[i + 1]) / 2
            x_alvo = xc + r_at_conversa(y_meio)
            ax.plot([self.X_S - 0.22, x_alvo], [y_meio, y_meio],
                    color=_COR_GUIA, lw=0.6, ls=_TRACEJADO_GUIA, zorder=6)
            ax.text(self.X_S, y_meio, nome, fontsize=13, ha="left",
                    va="center", color=_COR_EIXO, fontweight="bold", zorder=9)

    # ------------------------------------------------------------------
    # Quatro zonas simples no eixo de intensidade — sem colchetes, só um
    # traço fino em cada fronteira. O nome da zona (demais/mais/menos/
    # demenos) fica do lado DIREITO, como sempre; o índice Sn (mesma
    # notação do cone da conversa: demais=S1, mais=S2, menos=S3,
    # demenos=S4) fica à parte, do lado ESQUERDO.
    # ------------------------------------------------------------------
    def _add_zonas_int(self):
        ax, H = self.ax, self.H
        h1, h2, h3 = self.alturas_internas
        fronteiras = [0.0, h1, h2, h3, H]
        nomes = ["demenos", "menos", "mais", "demais"]   # de baixo (–) pra cima (+)
        tick = 0.09
        for y in fronteiras:
            ax.plot([-tick, tick], [y, y], color=_COR_GUIA, lw=0.8, zorder=5)
        for i, nome in enumerate(nomes):
            y_meio = (fronteiras[i] + fronteiras[i + 1]) / 2
            s_num = 4 - i   # demenos->S4, menos->S3, mais->S2, demais->S1
            ax.text(0.30, y_meio, nome, fontsize=13, ha="left", va="center",
                    color=_COR_EIXO, fontweight="medium", zorder=8)
            ax.text(-0.30, y_meio, f"S{s_num}", fontsize=13, ha="right",
                    va="center", color=_COR_EIXO, fontweight="bold", zorder=8)

    # ------------------------------------------------------------------
    # Um par de colchetes (metade de cima / metade de baixo) do lado de
    # fora de um eixo de extensidade — mesma lógica de
    # _colchete()/_add_movimentos_int(), mas uma única vez, sem
    # colchete-mestre nem incremento. Cada colchete leva um rótulo de duas
    # linhas ("valores de" + o termo), itálico/cinza, centrado na altura do
    # colchete; o rótulo cresce PRA FORA do colchete (ha="right"/"left"),
    # nunca por cima dele, não importa o tamanho do texto.
    # ------------------------------------------------------------------
    def _add_colchete_valores(self, x, lado, termo_cima, termo_baixo,
                              gap_colchete=0.30, gap_rotulo=0.14):
        H = self.H
        meio = H / 2
        y_lo, y_hi = meio / 2, (meio + H) / 2
        sinal = -1 if lado == "esquerda" else 1
        abre_para = "direita" if lado == "esquerda" else "esquerda"
        ha = "right" if lado == "esquerda" else "left"
        x_col = x + sinal * gap_colchete
        x_rot = x_col + sinal * gap_rotulo
        kw_rot = dict(fontsize=14, ha=ha, va="center", style="italic",
                      color=_COR_INCREMENTO, zorder=8)

        def rotulo(y, termo):
            self.ax.text(x_rot, y + 0.11, "valores de", **kw_rot)
            self.ax.text(x_rot, y - 0.11, termo, **kw_rot)

        self._colchete(x_col, meio, H, abre_para=abre_para)
        self._colchete(x_col, 0.0, meio, abre_para=abre_para)
        rotulo(y_hi, termo_cima)
        rotulo(y_lo, termo_baixo)

    # ------------------------------------------------------------------
    def salvar(self, caminho, dpi=300):
        self.fig.savefig(caminho, dpi=dpi, bbox_inches="tight")
        return caminho


# ----------------------------------------------------------------------
# Funções de fábrica — ponto de entrada público
# ----------------------------------------------------------------------
def campo_zonas(**kw) -> CampoPresenca:
    """"Campo de Presença Tensivo" — sem colchetes: só as quatro zonas da
    intensidade (S1 demais / S2 mais / S3 menos / S4 demenos) marcadas do
    lado esquerdo do eixo central. Sem a régua S1-S4 do lado da conversa
    (esse índice já vive nas próprias zonas aqui)."""
    kw.setdefault("titulo", "Campo de Presença Tensivo")
    kw.setdefault("regua_s", False)
    c = CampoPresenca(**kw)
    c._add_eixo_int()
    c._add_zonas_int()
    c._add_eixos_ext()
    c._add_cone(c.X_INV, "inversa", "INVERSA")
    c._add_cone(c.X_CONV, "conversa", "CONVERSA")
    return c


def campo_valores_zonas(**kw) -> CampoPresenca:
    """Como campo_zonas(), acrescentando um par de colchetes do lado de fora
    de cada eixo de extensidade, dividindo-o ao meio — os quatro VALORES
    TENSIVOS da extensidade, cada colchete com um rótulo de duas linhas
    ("valores de" + termo):

        inversa  (esquerda) — topo: valores de absoluto | base: valores de universo
        conversa (direita)  — topo: valores de apogeu    | base: valores de abismo
    """
    kw.setdefault("titulo", "Campo de Presença Tensivo")
    kw.setdefault("subtitulo", "Valores Tensivos")
    kw.setdefault("regua_s", False)
    c = CampoPresenca(**kw)
    c._add_eixo_int()
    c._add_zonas_int()
    c._add_eixos_ext()
    c._add_cone(c.X_INV, "inversa", "INVERSA")
    c._add_cone(c.X_CONV, "conversa", "CONVERSA")
    c._add_colchete_valores(c.X_EXT_L, "esquerda", "absoluto", "universo")
    c._add_colchete_valores(c.X_EXT_R, "direita", "apogeu", "abismo")
    return c


def campo_direcoes_tensivas(**kw) -> CampoPresenca:
    """"Campo de Presença Tensivo" / "Direções Tensivas" — os colchetes de
    ascendência/descendência COM os dois polos do ciclo marcados: acontecimento
    (topo) e torpor (base). Assim cada rótulo de processo se lê como uma
    passagem entre polos (ex.: o restabelecimento é a saída do torpor,
    rumo ao recrudescimento e ao acontecimento)."""
    kw.setdefault("titulo", "Campo de Presença Tensivo")
    kw.setdefault("subtitulo", "Direções Tensivas")
    # precisa de mais folga que o padrão: os polos acontecimento/torpor (mais
    # o incremento de cada um) ficam acima/abaixo do título de cada eixo.
    kw.setdefault("y_titulo_eixo", -1.30)
    kw.setdefault("margem_topo", 1.30)
    kw.setdefault("margem_base", 1.65)
    kw.setdefault("regua_s", False)
    c = CampoPresenca(**kw)
    c._add_eixo_int()
    c._add_polos_ciclo()
    c._add_movimentos_int()
    c._add_eixos_ext()
    c._add_cone(c.X_INV, "inversa", "INVERSA")
    c._add_cone(c.X_CONV, "conversa", "CONVERSA")
    return c


# ----------------------------------------------------------------------
if __name__ == "__main__":
    campo_zonas().salvar("campo_presenca_zonas.png")
    print("salvo: campo_presenca_zonas.png")
    campo_valores_zonas().salvar("campo_valores_zonas.png")
    print("salvo: campo_valores_zonas.png")
    campo_direcoes_tensivas().salvar("campo_presenca_direcoes_tensivas.png")
    print("salvo: campo_presenca_direcoes_tensivas.png")

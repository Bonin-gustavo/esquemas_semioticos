"""
campo_presenca_puro.py — versão "pura" do campo de presença, enriquecida
========================================================================
Reaproveita a classe CampoPresenca (campo_presenca.py). Sobre o cone limpo:

    i)  DIREÇÃO INTERNA — linha de modulação que corre pelo eixo do cone.
    ii) ADENSAMENTO das faixas S1..S4 orientado pela INTENSIDADE (S1 mais
        escuro, S4 mais claro), cada faixa recortada em 3D pelos arcos das
        elipses (inclui a base cheia, com o verso, na conversa).

Fábricas:
    campo_puro(correlacao, direcao)          — uma correlação; a oposta apagada.
    campo_puro_ambas(direcao)                — as duas correlações.
    campo_ampliacao(correlacao)              — uma correlação, modulação S2->S1,
                                               com rótulos mobilizados na extensidade.
    campo_direcoes_tensivas_densidade()      — ciclo tensivo completo (polos +
                                               ascendência/descendência) com adensamento.

`direcao` é sempre "asc" (S4 -> S1, extinção -> saturação) ou "desc" (S1 ->
S4, saturação -> extinção) — a mesma dupla de polos do ciclo tensivo de
campo_direcoes_tensivas(). Os seis exemplos padrão (ver `if __name__ ==
"__main__"` no fim do arquivo) são as combinações prontas — sem "puro" no
nome, porque já não são o cone limpo (têm seta de modulação, rótulos de
tendência e destaque vermelho):
    campo_ambas_asc / campo_ambas_desc
    campo_inversa_asc / campo_inversa_desc
    campo_conversa_asc / campo_conversa_desc
"""
from __future__ import annotations
import numpy as np
import matplotlib.patches as mpatches
import campo_presenca as cp
from campo_presenca import CampoPresenca

_COR_DIRECAO = "0.18"
_COR_FRACO   = "0.80"
_COR_TEND    = "0.30"    # direções-tendências (itálico, cinza)
_ALPHAS_INTENSIDADE = [0.035, 0.085, 0.150, 0.230]   # S4..S1

# Rótulos mobilizados da extensidade, por correlação (ver USO.md)
MOBIL_INVERSA = {
    "S4": ("eterno", "escancarado"),
    "S3": ("longo", "aberto"),
    "S2": ("breve", "fechado"),
    "S1": ("efêmero", "hermético"),
}
MOBIL_CONVERSA = {
    "S1": ("eterno", "escancarado"),
    "S2": ("longo", "aberto"),
    "S3": ("breve", "fechado"),
    "S4": ("efêmero", "hermético"),
}
# direção da modulação interna: sempre entre os polos do ciclo tensivo
_DIRECOES = {"asc": ("S4", "S1"), "desc": ("S1", "S4")}
# na conversa, S1 fica bem em cima do círculo da base (que ali é no topo);
# em "desc" a modulação parte de S1 — afasta só um pouco a bolinha desse
# círculo (um ajuste maior a deixaria longe demais do ponto onde a mesma
# seta chega em "asc" e da seta vermelha de destaque ao lado, que não leva
# esse ajuste)
_AJUSTE_BOLINHA_BASE = -0.12

# rótulos de tendência (itálico, cinza, abaixo de cada Sn) por direção —
# os rótulos originais S1|demais, S2|mais, S3|menos, S4|demenos (via
# _add_zonas_int) são sempre mantidos junto com estes
TEND_ASC = {"S1": "saturação", "S2": "ampliação", "S3": "progressão", "S4": "retomada"}
TEND_DESC = {"S1": "moderação", "S2": "diminuição", "S3": "redução", "S4": "extenuação"}


class CampoPresencaPuro(CampoPresenca):

    def _r_at(self, tipo):
        H, R = self.H, self.R
        if tipo == "inversa":
            return lambda y: (H - y) / H * R
        return lambda y: y / H * R

    def _arco_inferior(self, xc, y, r, n=48):
        a = np.linspace(np.pi, 2 * np.pi, n)
        return list(zip(xc + r * np.cos(a), y + r * cp._ELLIPSE_RATIO * np.sin(a)))

    def _arco_superior(self, xc, y, r, n=48):
        a = np.linspace(np.pi, 0, n)
        return list(zip(xc + r * np.cos(a), y + r * cp._ELLIPSE_RATIO * np.sin(a)))

    # ------------------------------------------------------------------
    # (ii) adensamento por intensidade, fatias 3D limitadas pelos arcos
    # ------------------------------------------------------------------
    def _add_densidade_intensidade(self, xc, tipo):
        ax, H = self.ax, self.H
        r_at = self._r_at(tipo)
        h1, h2, h3 = self.alturas_internas
        fronteiras = [0.0, h1, h2, h3, H]              # S4, S3, S2, S1
        apex_y = H if tipo == "inversa" else 0.0
        base_y = 0.0 if tipo == "inversa" else H

        def arco(y, r):
            # a base do cone é preenchida por inteiro (verso incluso): usa o
            # arco que se afasta do ápice. Os círculos internos usam o arco
            # frontal (inferior), de modo que as fatias se encaixem.
            if abs(y - base_y) < 1e-9 and base_y > apex_y:
                return self._arco_superior(xc, y, r)
            return self._arco_inferior(xc, y, r)

        for i in range(4):
            y0, y1 = fronteiras[i], fronteiras[i + 1]
            r0, r1 = r_at(y0), r_at(y1)
            poly = arco(y0, r0) + arco(y1, r1)[::-1]
            ax.add_patch(mpatches.Polygon(poly, closed=True, facecolor="0.0",
                                          edgecolor="none",
                                          alpha=_ALPHAS_INTENSIDADE[i], zorder=1.5))

    # ------------------------------------------------------------------
    # direção / modulação internas
    # ------------------------------------------------------------------
    def _centro_faixa(self, s):
        h1, h2, h3 = self.alturas_internas
        return {"S4": (0.0 + h1) / 2, "S3": (h1 + h2) / 2,
                "S2": (h2 + h3) / 2, "S1": (h3 + self.H) / 2}[s]

    def _add_modulacao(self, xc, tipo, s_ini, s_fim, ajuste_bolinha=0.0):
        """Seta da modulação, do centro da faixa inicial ao centro da final.
        `ajuste_bolinha`: desloca o ponto de partida (bolinha + cauda da
        seta) verticalmente — usado só quando a faixa inicial cai bem em
        cima do círculo da base do cone (ex.: S1 na conversa, cujo círculo
        de base fica no topo), pra bolinha não coincidir com esse círculo."""
        y0 = self._centro_faixa(s_ini) + ajuste_bolinha
        y1 = self._centro_faixa(s_fim)
        self.ax.annotate("", xy=(xc, y1), xytext=(xc, y0),
                         arrowprops=dict(arrowstyle="-|>", color=_COR_DIRECAO, lw=1.9),
                         zorder=7)
        self.ax.scatter([xc], [y0], s=20, color=_COR_DIRECAO, zorder=8)

    # ------------------------------------------------------------------
    # cone apagado (oposto "sem uso")
    # ------------------------------------------------------------------
    def _add_cone_fraco(self, xc, tipo, titulo):
        ax, H, R = self.ax, self.H, self.R
        r_at = self._r_at(tipo)
        apex_y, base_y = (H, 0.0) if tipo == "inversa" else (0.0, H)
        ax.text(xc, H + 0.55, titulo, fontsize=15, fontweight="bold",
                ha="center", va="bottom", color=_COR_FRACO, zorder=3)
        ax.plot([xc, xc - R], [apex_y, base_y], color=_COR_FRACO, lw=1.0, zorder=2)
        ax.plot([xc, xc + R], [apex_y, base_y], color=_COR_FRACO, lw=1.0, zorder=2)
        for y in self.alturas_internas:
            r = r_at(y)
            ax.add_patch(mpatches.Ellipse((xc, y), width=2*r, height=2*r*cp._ELLIPSE_RATIO,
                         fill=False, edgecolor=_COR_FRACO, lw=0.8,
                         ls=cp._TRACEJADO_CIRCULO, zorder=2))
        ax.add_patch(mpatches.Ellipse((xc, base_y), width=2*R, height=2*R*cp._ELLIPSE_RATIO,
                     fill=False, edgecolor=_COR_FRACO, lw=1.0, zorder=2))

    # ------------------------------------------------------------------
    # rótulos de direção-tendência (itálico, cinza) abaixo dos S1..S4
    # ------------------------------------------------------------------
    def _add_tendencias(self, tend):
        for s, txt in tend.items():
            y = self._centro_faixa(s)
            self.ax.text(-0.30, y - 0.15, txt, fontsize=14, style="italic",
                         ha="right", va="top", color=_COR_TEND, zorder=8)

    # ------------------------------------------------------------------
    # eixo de extensidade (esquerda) com divisórias + rótulos mobilizados
    # ------------------------------------------------------------------
    def _add_extensidade_rotulos(self, mobil, x=None, lado="esquerda"):
        """Divisórias + rótulos mobilizados no eixo de extensidade (o eixo em
        si já vem de _add_eixos_ext ou de _eixo_vertical). Rótulos em
        itálico/cinza, os dois de cada faixa bem próximos um do outro.
        `x` default X_EXT_L (lado esquerdo, inversa); `lado="direita"` espelha
        os rótulos para fora do eixo direito (conversa)."""
        ax, H = self.ax, self.H
        if x is None:
            x = self.X_EXT_L
        h1, h2, h3 = self.alturas_internas
        tick = 0.09
        for y in (0.0, h1, h2, h3, H):
            ax.plot([x - tick, x + tick], [y, y], color=cp._COR_GUIA, lw=0.8, zorder=5)
        dx = -0.26 if lado == "esquerda" else 0.26
        ha = "right" if lado == "esquerda" else "left"
        for s, (w1, w2) in mobil.items():
            yc = self._centro_faixa(s)
            ax.text(x + dx, yc + 0.11, w1, fontsize=12, ha=ha, va="center",
                    style="italic", color=_COR_TEND, zorder=8)
            ax.text(x + dx, yc - 0.11, w2, fontsize=12, ha=ha, va="center",
                    style="italic", color=_COR_TEND, zorder=8)

    # ------------------------------------------------------------------
    # destaque do trecho percorrido, nos dois eixos (sugestão)
    # ------------------------------------------------------------------
    def _add_destaque_percurso(self, s_ini, s_fim, x_ext=None):
        """Seta de destaque no trecho percorrido, sobre cada eixo (intensidade
        e extensidade), cobrindo o mesmo caminho da modulação interna do cone.
        `x_ext` default X_EXT_L (inversa); passe X_EXT_R para a conversa."""
        y_ini, y_fim = self._centro_faixa(s_ini), self._centro_faixa(s_fim)
        if x_ext is None:
            x_ext = self.X_EXT_L
        for x in (0.0, x_ext):
            self.ax.annotate("", xy=(x, y_fim), xytext=(x, y_ini),
                             arrowprops=dict(arrowstyle="-|>", color=cp._COR_SIM, lw=2.4),
                             zorder=6)

    def _eixo_ext_fraco(self, x, cima="+", baixo="−"):
        """Eixo de extensidade apagado (para a correlação não usada). Por
        padrão na orientação da conversa (cima +, baixo -); passe cima="−",
        baixo="+" para apagar o lado da inversa."""
        ax, H = self.ax, self.H
        ax.annotate("", xy=(x, H), xytext=(x, 0),
                    arrowprops=dict(arrowstyle="<->", color=_COR_FRACO, lw=1.2), zorder=2)
        ax.text(x, H + 0.30, cima, fontsize=28, fontweight="bold", ha="center",
                va="bottom", color=_COR_FRACO, zorder=3)
        ax.text(x, -0.30, baixo, fontsize=28, fontweight="bold", ha="center",
                va="top", color=_COR_FRACO, zorder=3)
        ax.text(x, self._Y_TITULO_EIXO, "extensidade", fontsize=15, fontweight="bold",
                ha="center", va="top", color=_COR_FRACO, zorder=3)


# ----------------------------------------------------------------------
# Fábricas gerais
# ----------------------------------------------------------------------
def campo_puro(correlacao="inversa", direcao="asc", **kw) -> CampoPresencaPuro:
    """Uma correlação enriquecida (adensamento + modulação interna entre os
    polos do ciclo tensivo); a oposta aparece apagada (cone e extensidade).
    Os rótulos mobilizados da extensidade (MOBIL_INVERSA/MOBIL_CONVERSA)
    ficam no eixo de extensidade ativo; o eixo apagado fica sem rótulos.
    Na intensidade, mantém os rótulos originais (S1|demais...S4|demenos) e
    acrescenta, abaixo de cada um, o rótulo de tendência (TEND_ASC/TEND_DESC)
    e a seta vermelha de destaque entre os polos da modulação, tanto na
    intensidade quanto na extensidade ativa."""
    s_ini, s_fim = _DIRECOES[direcao]
    tend = TEND_ASC if direcao == "asc" else TEND_DESC
    sub = {"inversa": "Correlação inversa", "conversa": "Correlação conversa"}[correlacao]
    kw.setdefault("titulo", "Campo de Presença Tensivo")
    kw.setdefault("subtitulo", sub)
    kw.setdefault("regua_s", False)
    c = CampoPresencaPuro(**kw)
    c._add_eixo_int()
    c._add_zonas_int()
    c._add_tendencias(tend)

    if correlacao == "inversa":
        x_cone_ativo, tipo_ativo = c.X_INV, "inversa"
        x_cone_fraco, tipo_fraco = c.X_CONV, "conversa"
        x_ext_ativo, x_ext_fraco = c.X_EXT_L, c.X_EXT_R
        cima_ativo, baixo_ativo = "−", "+"
        cima_fraco, baixo_fraco = "+", "−"
        lado_ativo = "esquerda"
        mobil_ativo = MOBIL_INVERSA
    else:
        x_cone_ativo, tipo_ativo = c.X_CONV, "conversa"
        x_cone_fraco, tipo_fraco = c.X_INV, "inversa"
        x_ext_ativo, x_ext_fraco = c.X_EXT_R, c.X_EXT_L
        cima_ativo, baixo_ativo = "+", "−"
        cima_fraco, baixo_fraco = "−", "+"
        lado_ativo = "direita"
        mobil_ativo = MOBIL_CONVERSA

    c._eixo_vertical(x_ext_ativo, cima=cima_ativo, baixo=baixo_ativo)
    c._titulo_eixo(x_ext_ativo, "extensidade")
    c._add_extensidade_rotulos(mobil_ativo, x=x_ext_ativo, lado=lado_ativo)
    c._eixo_ext_fraco(x_ext_fraco, cima=cima_fraco, baixo=baixo_fraco)
    c._add_destaque_percurso(s_ini, s_fim, x_ext=x_ext_ativo)

    ajuste_bolinha = _AJUSTE_BOLINHA_BASE if (tipo_ativo == "conversa" and direcao == "desc") else 0.0
    c._add_cone_fraco(x_cone_fraco, tipo_fraco, tipo_fraco.upper())
    c._add_cone(x_cone_ativo, tipo_ativo, tipo_ativo.upper())
    c._add_densidade_intensidade(x_cone_ativo, tipo_ativo)
    c._add_modulacao(x_cone_ativo, tipo_ativo, s_ini, s_fim, ajuste_bolinha=ajuste_bolinha)
    return c


def campo_puro_ambas(direcao="asc", **kw) -> CampoPresencaPuro:
    """As duas correlações enriquecidas lado a lado (nenhuma apagada), cada
    uma com os rótulos mobilizados da sua extensidade (MOBIL_INVERSA à
    esquerda, MOBIL_CONVERSA à direita) e a mesma modulação interna
    (`direcao`) nos dois cones. Na intensidade, mantém os rótulos originais
    e acrescenta os rótulos de tendência (TEND_ASC/TEND_DESC) e a seta
    vermelha de destaque, replicada nas duas extensidades."""
    s_ini, s_fim = _DIRECOES[direcao]
    tend = TEND_ASC if direcao == "asc" else TEND_DESC
    kw.setdefault("titulo", "Campo de Presença Tensivo")
    kw.setdefault("regua_s", False)
    c = CampoPresencaPuro(**kw)
    c._add_eixo_int()
    c._add_zonas_int()
    c._add_tendencias(tend)
    c._add_eixos_ext()
    c._add_extensidade_rotulos(MOBIL_INVERSA, x=c.X_EXT_L, lado="esquerda")
    c._add_extensidade_rotulos(MOBIL_CONVERSA, x=c.X_EXT_R, lado="direita")
    c._add_destaque_percurso(s_ini, s_fim, x_ext=c.X_EXT_L)
    c._add_destaque_percurso(s_ini, s_fim, x_ext=c.X_EXT_R)

    c._add_cone(c.X_INV, "inversa", "INVERSA")
    c._add_densidade_intensidade(c.X_INV, "inversa")
    c._add_modulacao(c.X_INV, "inversa", s_ini, s_fim)

    c._add_cone(c.X_CONV, "conversa", "CONVERSA")
    c._add_densidade_intensidade(c.X_CONV, "conversa")
    ajuste_bolinha = _AJUSTE_BOLINHA_BASE if direcao == "desc" else 0.0
    c._add_modulacao(c.X_CONV, "conversa", s_ini, s_fim, ajuste_bolinha=ajuste_bolinha)
    return c


# ----------------------------------------------------------------------
# Exemplos padrão — as seis combinações prontas de campo_puro/campo_puro_ambas.
# Sem "puro" no nome: já levam seta de modulação, rótulos de tendência e
# destaque vermelho, então não são mais o cone limpo.
# ----------------------------------------------------------------------
def campo_ambas_asc(**kw) -> CampoPresencaPuro:
    return campo_puro_ambas("asc", **kw)


def campo_ambas_desc(**kw) -> CampoPresencaPuro:
    return campo_puro_ambas("desc", **kw)


def campo_inversa_asc(**kw) -> CampoPresencaPuro:
    return campo_puro("inversa", "asc", **kw)


def campo_inversa_desc(**kw) -> CampoPresencaPuro:
    return campo_puro("inversa", "desc", **kw)


def campo_conversa_asc(**kw) -> CampoPresencaPuro:
    return campo_puro("conversa", "asc", **kw)


def campo_conversa_desc(**kw) -> CampoPresencaPuro:
    return campo_puro("conversa", "desc", **kw)


def campo_ampliacao(correlacao="inversa", **kw) -> CampoPresencaPuro:
    """Uma correlação isolada (a oposta apagada, cone e extensidade), com a
    modulação de S2 (mais/ampliação) a S1 (demais/saturação):

        inversa  — extensidade: breve/fechado (S2) -> efêmero/hermético (S1)
        conversa — extensidade: aberto/longo (S2) -> escancarado/eterno (S1)

    Na conversa, a extensidade ativa é a da DIREITA (a que sobe junto com a
    intensidade); o cone e a extensidade da inversa ficam apagados, e vice-versa."""
    s_ini, s_fim = "S2", "S1"
    tend = {"S2": "ampliação", "S1": "saturação"}
    if correlacao == "inversa":
        sub = "Correlação inversa (ascendência de S2 a S1)"
        mobil = {"S2": ("breve", "fechado"), "S1": ("efêmero", "hermético")}
    else:
        sub = "Correlação conversa (ascendência de S2 a S1)"
        mobil = {"S2": ("aberto", "longo"), "S1": ("escancarado", "eterno")}

    kw.setdefault("titulo", "Campo de Presença Tensivo")
    kw.setdefault("subtitulo", sub)
    kw.setdefault("regua_s", False)
    c = CampoPresencaPuro(**kw)
    c._add_eixo_int()
    c._add_zonas_int()
    c._add_tendencias(tend)

    if correlacao == "inversa":
        x_ativo, tipo_ativo = c.X_INV, "inversa"
        x_fraco, tipo_fraco = c.X_CONV, "conversa"
        x_ext_ativo, x_ext_fraco = c.X_EXT_L, c.X_EXT_R
        cima_ativo, baixo_ativo = "−", "+"
        cima_fraco, baixo_fraco = "+", "−"
        lado_mobil = "esquerda"
    else:
        x_ativo, tipo_ativo = c.X_CONV, "conversa"
        x_fraco, tipo_fraco = c.X_INV, "inversa"
        x_ext_ativo, x_ext_fraco = c.X_EXT_R, c.X_EXT_L
        cima_ativo, baixo_ativo = "+", "−"
        cima_fraco, baixo_fraco = "−", "+"
        lado_mobil = "direita"

    c._eixo_vertical(x_ext_ativo, cima=cima_ativo, baixo=baixo_ativo)
    c._titulo_eixo(x_ext_ativo, "extensidade")
    c._eixo_ext_fraco(x_ext_fraco, cima=cima_fraco, baixo=baixo_fraco)
    c._add_extensidade_rotulos(mobil, x=x_ext_ativo, lado=lado_mobil)
    c._add_destaque_percurso(s_ini, s_fim, x_ext=x_ext_ativo)
    c._add_cone_fraco(x_fraco, tipo_fraco, tipo_fraco.upper())
    c._add_cone(x_ativo, tipo_ativo, tipo_ativo.upper())
    c._add_densidade_intensidade(x_ativo, tipo_ativo)
    c._add_modulacao(x_ativo, tipo_ativo, s_ini, s_fim)
    return c


def campo_direcoes_tensivas_densidade(**kw) -> CampoPresencaPuro:
    """Como campo_direcoes_tensivas (ciclo tensivo: polos + ascendência/
    descendência, sem régua S1–S4), acrescentando o adensamento das faixas
    por intensidade nos dois cones."""
    kw.setdefault("titulo", "Campo de Presença Tensivo")
    kw.setdefault("subtitulo", "Direções Tensivas")
    kw.setdefault("y_titulo_eixo", -1.30)
    kw.setdefault("margem_topo", 1.30)
    kw.setdefault("margem_base", 1.65)
    kw.setdefault("regua_s", False)
    c = CampoPresencaPuro(**kw)
    c._add_eixo_int()
    c._add_polos_ciclo()
    c._add_movimentos_int()
    c._add_eixos_ext()
    c._add_cone(c.X_INV, "inversa", "INVERSA")
    c._add_densidade_intensidade(c.X_INV, "inversa")
    c._add_cone(c.X_CONV, "conversa", "CONVERSA")
    c._add_densidade_intensidade(c.X_CONV, "conversa")
    return c


if __name__ == "__main__":
    campo_ambas_asc().salvar("campo_ambas_asc.png"); print("salvo: campo_ambas_asc.png")
    campo_ambas_desc().salvar("campo_ambas_desc.png"); print("salvo: campo_ambas_desc.png")
    campo_inversa_asc().salvar("campo_inversa_asc.png"); print("salvo: campo_inversa_asc.png")
    campo_inversa_desc().salvar("campo_inversa_desc.png"); print("salvo: campo_inversa_desc.png")
    campo_conversa_asc().salvar("campo_conversa_asc.png"); print("salvo: campo_conversa_asc.png")
    campo_conversa_desc().salvar("campo_conversa_desc.png"); print("salvo: campo_conversa_desc.png")

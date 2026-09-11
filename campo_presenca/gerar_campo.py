"""
gerar_campo.py — gere o campo de presença que você quiser
===========================================================
Edite APENAS o bloco abaixo e rode:

    python3 gerar_campo.py

Rode a partir da pasta campo_presenca/ (onde está o campo_presenca.py).

Escolha a VERSAO (qual figura gerar) — cada uma corresponde a uma fábrica de
campo_presenca.py ou campo_presenca_puro.py:

    "zonas"                — as quatro zonas simples da intensidade
    "valores_zonas"         — como "zonas", com dois pares de colchetes na
                             extensidade da inversa (absoluto/universo por
                             fora, apogeu/abismo por dentro)
    "direcoes"              — ciclo tensivo completo: polos + ascendência/descendência
    "ambas_asc"              — as duas correlações enriquecidas, modulação S4->S1 (ascendência)
    "ambas_desc"             — idem, modulação S1->S4 (descendência)
    "inversa_asc"            — só a correlação inversa, enriquecida, modulação S4->S1
    "inversa_desc"           — idem, modulação S1->S4
    "conversa_asc"           — só a correlação conversa, enriquecida, modulação S4->S1
    "conversa_desc"          — idem, modulação S1->S4
    "ampliacao_inversa"     — correlação inversa, modulação S2->S1 com rótulos mobilizados na extensidade
    "ampliacao_conversa"    — idem, correlação conversa
    "direcoes_densidade"    — ciclo tensivo completo (polos + ascendência/descendência) + adensamento

As versões "ambas_*"/"inversa_*"/"conversa_*" não são o cone limpo — já
levam seta de modulação, rótulos de tendência (abaixo de cada S1..S4) e
destaque vermelho na intensidade/extensidade, com os rótulos mobilizados
padrão (MOBIL_INVERSA/MOBIL_CONVERSA, em campo_presenca_puro.py); a
correlação não usada (em "inversa_*" e "conversa_*") aparece apagada, cone e
extensidade.

TITULO e SUBTITULO, se deixados em None, usam o padrão de cada versão.
"""
from campo_presenca import campo_zonas, campo_valores_zonas, campo_direcoes_tensivas
from campo_presenca_puro import (
    campo_ambas_asc, campo_ambas_desc,
    campo_inversa_asc, campo_inversa_desc,
    campo_conversa_asc, campo_conversa_desc,
    campo_ampliacao, campo_direcoes_tensivas_densidade,
)

# ----------------------------------------------------------------------
# EDITE AQUI  ↓↓↓
# ----------------------------------------------------------------------
VERSAO = "direcoes"          # veja a lista de versões disponíveis acima
ARQUIVO_SAIDA = "campo_presenca.png"
TITULO = None                 # None usa o título padrão da versão
SUBTITULO = None              # None usa o subtítulo padrão da versão
# ----------------------------------------------------------------------
# EDITE AQUI  ↑↑↑
# ----------------------------------------------------------------------


def _kw(**kwargs):
    """Descarta parâmetros None para não sobrescrever os padrões de cada fábrica."""
    return {k: v for k, v in kwargs.items() if v is not None}


_FABRICAS = {
    "zonas":              lambda: campo_zonas(**_kw(titulo=TITULO)),
    "valores_zonas":      lambda: campo_valores_zonas(**_kw(titulo=TITULO)),
    "direcoes":           lambda: campo_direcoes_tensivas(**_kw(titulo=TITULO, subtitulo=SUBTITULO)),
    "ambas_asc":          lambda: campo_ambas_asc(**_kw(titulo=TITULO)),
    "ambas_desc":         lambda: campo_ambas_desc(**_kw(titulo=TITULO)),
    "inversa_asc":        lambda: campo_inversa_asc(**_kw(titulo=TITULO, subtitulo=SUBTITULO)),
    "inversa_desc":       lambda: campo_inversa_desc(**_kw(titulo=TITULO, subtitulo=SUBTITULO)),
    "conversa_asc":       lambda: campo_conversa_asc(**_kw(titulo=TITULO, subtitulo=SUBTITULO)),
    "conversa_desc":      lambda: campo_conversa_desc(**_kw(titulo=TITULO, subtitulo=SUBTITULO)),
    "ampliacao_inversa":  lambda: campo_ampliacao("inversa", **_kw(titulo=TITULO, subtitulo=SUBTITULO)),
    "ampliacao_conversa": lambda: campo_ampliacao("conversa", **_kw(titulo=TITULO, subtitulo=SUBTITULO)),
    "direcoes_densidade": lambda: campo_direcoes_tensivas_densidade(**_kw(titulo=TITULO, subtitulo=SUBTITULO)),
}


if __name__ == "__main__":
    if VERSAO not in _FABRICAS:
        raise SystemExit(f"VERSAO inválida: {VERSAO!r}. Opções: {', '.join(_FABRICAS)}")
    _FABRICAS[VERSAO]().salvar(ARQUIVO_SAIDA)
    print(f"salvo: {ARQUIVO_SAIDA}  (versão: {VERSAO})")

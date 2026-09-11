"""
gerar_percursos.py — gere percursos (trajetórias) de intensidade
=================================================================
Um PERCURSO liga 2 ou mais zonas por uma linha que vai do MEIO de uma zona ao
MEIO da seguinte (nunca pelos vértices), com seta:
    unidirecional  (->)   mostra o sentido do percurso
    bidirecional   (<->)  indica ida e volta
O percurso pode andar por um ou vários eixos ao mesmo tempo — depende das zonas.

Edite APENAS o bloco CENARIOS abaixo e rode:

    python3 gerar_percursos.py

Cada cenário gera um par de imagens: <prefixo>_completo.png (grade 4×4×4) e
<prefixo>_parcial.png (grade só nas 3 faces visíveis). Por padrão há dois
cenários — um percurso unidirecional e um bidirecional.
Rode a partir da pasta cubo_tri/ (onde está o cubo_tri_zonas_intensidade.py).

Cada zona é uma tupla (crença, confiança, intensidade). Valores possíveis:
    crença      : "não crê nada", "quase crê", "até crê", "crê totalmente"
    confiança   : "não confia nada", "quase confia", "até confia", "confia totalmente"
    intensidade : "demenos", "menos", "mais", "demais"

As zonas são coloridas pela temperatura da intensidade
(demais = vermelho ... demenos = amarelo).
"""
from cubo_tri_zonas_intensidade import zonas_percurso

# ----------------------------------------------------------------------
# EDITE AQUI  ↓↓↓
# Cada cenário vira um par de imagens (<prefixo>_completo.png e _parcial.png).
# Dentro de cada cenário, cada item é um percurso {"zonas": [...], "bidirecional": bool}.
# ----------------------------------------------------------------------
CENARIOS = {
    # percurso UNIDIRECIONAL (seta ->): subida pela diagonal
    "zonas_fiduciario_conversa_uni": [
        {
            "zonas": [
                ("não crê nada", "não confia nada", "demenos"),
                ("quase crê", "quase confia", "menos"),
                ("até crê", "até confia", "mais"),
                ("crê totalmente", "confia totalmente", "demais"),
            ],
            "bidirecional": False,
        },
    ],
    # percurso BIDIRECIONAL (seta <->): ida e volta na confiança, crença fixa
    "zonas_fiduciario_conversa_bi": [
        {
            "zonas": [
                ("não crê nada", "não confia nada", "demenos"),
                ("quase crê", "quase confia", "menos"),
                ("até crê", "até confia", "mais"),
                ("crê totalmente", "confia totalmente", "demais"),
            ],
            "bidirecional": True,
        },
    ],
}
# ----------------------------------------------------------------------
# EDITE AQUI  ↑↑↑
# ----------------------------------------------------------------------


if __name__ == "__main__":
    for prefixo, percursos in CENARIOS.items():
        for grade, sufixo in [("completa", "completo"), ("parcial", "parcial")]:
            saida = f"{prefixo}_{sufixo}.png"
            zonas_percurso(percursos, grade=grade).salvar(saida)
            print(f"salvo: {saida}  ({len(percursos)} percurso(s), grade {grade})")

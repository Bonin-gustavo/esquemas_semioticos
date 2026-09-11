"""
espacos.py — espaços de valor e gradações (CONTEÚDO EDITÁVEL)
==============================================================
Fonte única dos "conteúdos" dos eixos x/z e da intensidade. Para editar as
gradações de um eixo, ou para criar um espaço novo, mexa SOMENTE neste
arquivo — o plotter (cubo_tri_pontos_intensidade.py e
cubo_tri_zonas_intensidade.py) lê tudo daqui.

Convenções:
    INTENSIDADE  — eixo vertical, à ESQUERDA, comum a todos os espaços.
    eixo_x       — desce à DIREITA; 4 gradações, do – ao +.
    eixo_z       — sobe à DIREITA;  4 gradações, do – ao +.

Cada entrada de ESPACOS tem:
    eixo_x_nome / eixo_x_labels   (nome + 4 gradações do eixo que desce)
    eixo_z_nome / eixo_z_labels   (nome + 4 gradações do eixo que sobe)

As diagonais (conversa, inversa_1, inversa_2) são derivadas das gradações —
não precisam ser editadas à mão.
"""

# ----------------------------------------------------------------------
# Intensidade — eixo vertical, comum a todos os espaços. Não edite a
# ordem sem necessidade: os 4 rótulos alimentam a escala de cor e as diagonais.
# ----------------------------------------------------------------------
INTENSIDADE = ["demenos", "menos", "mais", "demais"]


# ----------------------------------------------------------------------
# Gradações de cada espaço (4 rótulos, do – ao +).
# ----------------------------------------------------------------------

# Fidúcia: confiança (S/S) × crença (S/O)
CONFIANCA = ["não confia nada", "quase confia", "até confia", "confia totalmente"]
CRENCA    = ["não crê nada", "quase crê", "até crê", "crê totalmente"]

# Veridictório: parecer × ser
PARECER = ["não parecer nada", "quase parecer", "parecer pouco", "parecer muito"]
SER     = ["não ser de forma alguma", "quase ser", "até ser", "ser exatamente"]

# Manipulação: querer × dever
QUERER = ["não querer de forma alguma", "quase querer", "querer pouco", "querer muito"]
DEVER  = ["não dever nada", "quase dever", "dever pouco", "dever muito"]

# Competencial: poder × saber
PODER = ["não poder nada", "quase poder", "poder pouco", "poder totalmente"]
SABER = ["não saber nada", "quase saber", "saber pouco", "saber exatamente"]


# ----------------------------------------------------------------------
# Espaços prontos. Para criar um novo, adicione uma entrada no mesmo
# formato (eixo_x + eixo_z); as fábricas genéricas passam a aceitá-lo.
# ----------------------------------------------------------------------
ESPACOS = {
    "fiduciario": {
        "eixo_x_nome": "confiança (S/S)", "eixo_x_labels": CONFIANCA,
        "eixo_z_nome": "crença (S/O)",     "eixo_z_labels": CRENCA,
    },
    "veridictorio": {
        "eixo_x_nome": "parecer", "eixo_x_labels": PARECER,
        "eixo_z_nome": "ser",     "eixo_z_labels": SER,
    },
    "manipulacao": {
        "eixo_x_nome": "querer", "eixo_x_labels": QUERER,
        "eixo_z_nome": "dever",  "eixo_z_labels": DEVER,
    },
    "competencial": {
        "eixo_x_nome": "poder", "eixo_x_labels": PODER,
        "eixo_z_nome": "saber", "eixo_z_labels": SABER,
    },
}


# ----------------------------------------------------------------------
# Percursos de exemplo — caminhos MANUAIS, específicos de cada espaço.
# Cada percurso é uma lista de zonas (eixo_z, eixo_x, intensidade).
# ----------------------------------------------------------------------
PERCURSOS = {
    "fiduciario": {
        "percurso_tres": [
            ("crê totalmente", "confia totalmente", "demais"),
            ("quase crê",      "até confia",        "menos"),
            ("não crê nada",   "quase confia",      "demenos"),
        ],
    },
    "veridictorio": {
        "percurso_dois": [
            ("não ser de forma alguma", "parecer muito", "demais"),
            ("até ser",                 "quase parecer", "menos"),
        ],
    },
    "manipulacao": {
        "percurso_quatro": [
            ("quase dever", "quase querer", "menos"),
            ("dever pouco", "quase querer", "demenos"),
            ("dever muito", "quase querer", "menos"),
            ("dever muito", "querer muito", "demais"),
        ],
    },
    "competencial": {
        "percurso_dois": [
            ("quase saber",      "não poder nada",   "menos"),
            ("saber exatamente", "poder totalmente", "demais"),
        ],
    },
}


# ----------------------------------------------------------------------
# Helpers — não precisam ser editados.
# ----------------------------------------------------------------------
def kw_espaco(nome):
    """Devolve os kwargs (eixo_x_* / eixo_z_*) do espaço `nome`, prontos para
    passar a qualquer fábrica de cubo_tri_pontos_* / cubo_tri_zonas_*."""
    cfg = ESPACOS[nome]
    return dict(eixo_x_nome=cfg["eixo_x_nome"], eixo_x_labels=cfg["eixo_x_labels"],
                eixo_z_nome=cfg["eixo_z_nome"], eixo_z_labels=cfg["eixo_z_labels"])


def diagonal(nome, tipo):
    """As 4 zonas da diagonal `tipo` do espaço `nome`, em ordem ascendente de
    intensidade, como lista de tuplas (eixo_z, eixo_x, intensidade).

    tipo:
        "conversa"  — os três eixos sobem juntos.
        "inversa_1" — eixo_x desce; eixo_z e intensidade sobem.
        "inversa_2" — eixo_z desce; eixo_x e intensidade sobem.
    """
    cfg = ESPACOS[nome]
    z, x = cfg["eixo_z_labels"], cfg["eixo_x_labels"]
    if tipo == "conversa":
        return [(z[i], x[i], INTENSIDADE[i]) for i in range(4)]
    if tipo == "inversa_1":
        return [(z[i], x[3 - i], INTENSIDADE[i]) for i in range(4)]
    if tipo == "inversa_2":
        return [(z[3 - i], x[i], INTENSIDADE[i]) for i in range(4)]
    raise ValueError(f"tipo de diagonal desconhecido: {tipo!r}")

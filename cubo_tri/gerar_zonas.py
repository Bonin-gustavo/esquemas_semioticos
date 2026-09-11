"""
gerar_zonas.py — gere zonas de intensidade destacadas
======================================================
Edite APENAS a lista ZONAS abaixo e rode:

    python3 gerar_zonas.py

O script gera AS DUAS versões de uma vez:
    zonas_completo.png  — grade 4×4×4 completa
    zonas_parcial.png   — grade só nas 3 faces visíveis

(Nomes diferentes dos exemplos de referência de cubo_tri_zonas_intensidade.py
— que gera zonas_fiduciario_zona_*.png com uma zona fixa — para um script não
sobrescrever a saída do outro.)
Rode a partir da pasta cubo_tri/ (onde está o cubo_tri_zonas_intensidade.py).

Cada zona é uma tupla (crença, confiança, intensidade). Valores possíveis:
    crença      : "não crê nada", "quase crê", "até crê", "crê totalmente"
    confiança   : "não confia nada", "quase confia", "até confia", "confia totalmente"
    intensidade : "demenos", "menos", "mais", "demais"

Dica: para empilhar uma zona EXATAMENTE abaixo de outra, mantenha crença e
confiança iguais e mude só a intensidade (ex.: abaixo de "demais" vem "mais").
As cores são atribuídas automaticamente pela temperatura da intensidade
(demais = vermelho ... demenos = amarelo).
"""
from cubo_tri_zonas_intensidade import zonas_zona_completo, zonas_zona_parcial

# ----------------------------------------------------------------------
# EDITE AQUI  ↓↓↓
# ----------------------------------------------------------------------
ZONAS = [
    ("até crê", "até confia", "mais"),
    ("quase crê",        "até confia", "mais"),
    ("até crê",        "quase confia", "mais"),
    ("quase crê",        "quase confia", "mais"),
    ("até crê", "até confia", "menos"),
    ("quase crê",        "até confia", "menos"),
    ("até crê",        "quase confia", "menos"),
    ("quase crê",        "quase confia", "menos"),

]
# ----------------------------------------------------------------------
# EDITE AQUI  ↑↑↑
# ----------------------------------------------------------------------


if __name__ == "__main__":
    for fabrica, saida in [
        (zonas_zona_completo, "zonas_completo.png"),
        (zonas_zona_parcial,  "zonas_parcial.png"),
    ]:
        fabrica(ZONAS).salvar(saida)
        print(f"salvo: {saida}  ({len(ZONAS)} zona(s))")

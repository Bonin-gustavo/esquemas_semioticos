"""
gerar_exemplos.py — regenera os exemplos de referência (pontos e zonas)
========================================================================
Gera os exemplos de referência dos dois códigos de intensidade, lendo os
espaços e gradações de `espacos.py` (fonte única):

    exemplos/pontos/   — pontos de intensidade (cubo_tri_pontos_intensidade.py)
    exemplos/zonas/    — zonas de intensidade (cubo_tri_zonas_intensidade.py)

Pontos — uma subpasta por espaço (mais o pontos_puro na raiz):

    exemplos/pontos/pontos_puro.png
    exemplos/pontos/fiduciario/pontos_fiduciario.png, _conversa,
        _inversa_1, _inversa_2, _percurso_*
    exemplos/pontos/veridictorio/..., manipulacao/..., competencial/...

Zonas — dezessete variantes por espaço:

    zonas_<espaço>_faces_completo/parcial, zonas_<espaço>_zona_completo/parcial,
    zonas_<espaço>_conversa_uni/bi, zonas_<espaço>_inversa_1/inversa_2_uni/bi
    (cada uma em _completo e _parcial), mais a inversa_2_uni_completo em
    ângulo alternativo (azm-120_elev20).

Rode a partir da pasta cubo_tri/:

    python3 gerar_exemplos.py

(Os scripts gerar_zonas.py e gerar_percursos.py continuam sendo a porta de
entrada para gerar UMA figura customizada por vez; este aqui só (re)faz o
conjunto completo de referência.)
"""
from pathlib import Path

import matplotlib.pyplot as plt

from espacos import ESPACOS, PERCURSOS, kw_espaco, diagonal
from cubo_tri_pontos_intensidade import (
    pontos_puro, pontos, pontos_diagonal, pontos_percurso,
)
from cubo_tri_zonas_intensidade import (
    zonas_faces_parcial, zonas_faces_completo,
    zonas_zona_parcial, zonas_zona_completo,
    zonas_percurso,
)


if __name__ == "__main__":
    base = Path(__file__).resolve().parent / "exemplos"

    # ---- pontos de intensidade (subpasta por espaço) ----
    pontos_dir = base / "pontos"
    pontos_dir.mkdir(parents=True, exist_ok=True)
    pontos_puro().salvar(pontos_dir / "pontos_puro.png")
    plt.close("all")
    for nome in ESPACOS:
        sub = pontos_dir / nome
        sub.mkdir(parents=True, exist_ok=True)
        pontos(nome).salvar(sub / f"pontos_{nome}.png")
        for tipo in ("conversa", "inversa_1", "inversa_2"):
            pontos_diagonal(nome, tipo).salvar(sub / f"pontos_{nome}_{tipo}.png")
        for chave, zonas in PERCURSOS.get(nome, {}).items():
            pontos_percurso(nome, zonas).salvar(sub / f"pontos_{nome}_{chave}.png")
        plt.close("all")
    print(f"salvos exemplos de pontos em exemplos/pontos/ (raiz + {len(ESPACOS)} espaços)")

    # ---- zonas de intensidade (dezessete variantes por espaço) ----
    zonas_dir = base / "zonas"
    for nome in ESPACOS:
        saida = zonas_dir / nome
        saida.mkdir(parents=True, exist_ok=True)
        kw = kw_espaco(nome)
        z, x = ESPACOS[nome]["eixo_z_labels"], ESPACOS[nome]["eixo_x_labels"]

        # 1-2) grade: completa e 3 faces visíveis
        zonas_faces_parcial(**kw).salvar(saida / f"zonas_{nome}_faces_parcial.png")
        zonas_faces_completo(**kw).salvar(saida / f"zonas_{nome}_faces_completo.png")

        # 3-4) uma zona destacada (canto máximo: eixo_z topo, eixo_x topo, demais)
        zona_top = (z[3], x[3], "demais")
        zonas_zona_parcial(zona_top, **kw).salvar(saida / f"zonas_{nome}_zona_parcial.png")
        zonas_zona_completo(zona_top, **kw).salvar(saida / f"zonas_{nome}_zona_completo.png")

        # 5-8) percurso CONVERSA: unidirecional e bidirecional, completa e parcial
        conversa = diagonal(nome, "conversa")
        uni = [{"zonas": conversa, "bidirecional": False}]
        bi  = [{"zonas": conversa, "bidirecional": True}]
        zonas_percurso(uni, grade="completa", **kw).salvar(saida / f"zonas_{nome}_conversa_uni_completo.png")
        zonas_percurso(uni, grade="parcial",  **kw).salvar(saida / f"zonas_{nome}_conversa_uni_parcial.png")
        zonas_percurso(bi,  grade="completa", **kw).salvar(saida / f"zonas_{nome}_conversa_bi_completo.png")
        zonas_percurso(bi,  grade="parcial",  **kw).salvar(saida / f"zonas_{nome}_conversa_bi_parcial.png")

        # 9-16) percursos INVERSAS:
        #   inversa_1 — eixo_x desce (demenos → demais)
        #   inversa_2 — eixo_z desce (demais → demenos, ordem do percurso invertida)
        inversa_1 = diagonal(nome, "inversa_1")
        inversa_2 = list(reversed(diagonal(nome, "inversa_2")))
        for variante, seq in [("inversa_1", inversa_1), ("inversa_2", inversa_2)]:
            uni = [{"zonas": seq, "bidirecional": False}]
            bi  = [{"zonas": seq, "bidirecional": True}]
            zonas_percurso(uni, grade="completa", **kw).salvar(saida / f"zonas_{nome}_{variante}_uni_completo.png")
            zonas_percurso(uni, grade="parcial",  **kw).salvar(saida / f"zonas_{nome}_{variante}_uni_parcial.png")
            zonas_percurso(bi,  grade="completa", **kw).salvar(saida / f"zonas_{nome}_{variante}_bi_completo.png")
            zonas_percurso(bi,  grade="parcial",  **kw).salvar(saida / f"zonas_{nome}_{variante}_bi_parcial.png")

        # extra) inversa_2 com câmera alternativa (azim=-120, elev=20) — separa
        # melhor as zonas da diagonal, que se sobrepõem na câmera padrão.
        uni2 = [{"zonas": inversa_2, "bidirecional": False}]
        zonas_percurso(uni2, grade="completa", azim=-120, elev=20, **kw).salvar(
            saida / f"zonas_{nome}_inversa_2_uni_completo_azm-120_elev20.png")

        plt.close("all")
        print(f"salvos 17 exemplos de zonas em exemplos/zonas/{nome}/")

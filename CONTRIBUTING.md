# Contribuindo

Obrigado pelo interesse em contribuir! Este repositório é uma ferramenta de
pesquisa aberta; contribuições de qualquer tipo são bem-vindas.

## Propor um novo esquema (ou ajustar gradações)

A maior parte do **conteúdo** (gradações dos eixos, espaços de valor e
percursos de exemplo) mora em `cubo_tri/espacos.py` — você não precisa mexer
nos plotters.

1. Abra uma [issue](https://github.com/Bonin-gustavo/esquemas_semioticos/issues)
   descrevendo a proposta (novo espaço, novas gradações, novo esquema, etc.).
2. Faça um *fork* e crie uma branch.
3. Edite `espacos.py` (e/ou os plotters, se for algo estrutural).
4. Regere os exemplos com `python3 cubo_tri/gerar_exemplos.py` e os do campo
   de presença com os scripts em `campo_presenca/`.
5. Abra um *pull request*.

## Reportar um bug ou pedir um ajuste

Use os templates de issue:
- **Bug report** — algo quebrou ou gera imagem errada.
- **Feature request** — novo esquema, ajuste, ou nova opção.
- **Question** — dúvida de uso (ou use as *Discussions*).

Inclua sempre: o que você esperava, o que aconteceu, e (se possível) o código
que você rodou.

## Convenções de commit

Mensagens curtas no padrão *Conventional Commits*:

- `feat:` novo esquema/funcionalidade
- `fix:` correção
- `docs:` documentação
- `refactor:` reorganização sem mudar comportamento

## Licença

Ao contribuir, você concorda que seu código será licenciado sob a licença MIT
(veja [LICENSE](LICENSE)); documentação e imagens sob CC BY 4.0 (veja
[LICENSE-CONTENT.md](LICENSE-CONTENT.md)).

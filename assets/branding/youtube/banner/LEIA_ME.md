# Banner YouTube — Parallax Lab

Entrega: 05/10/2026. Principal recomendada: `banner_01_institucional.png`.

## Arquivos

- `banner_01_institucional.png`: lockup central, assinatura em linha única.
- `banner_02_cinematografico.png`: símbolo lateral maior, assinatura em duas linhas.
- `banner_03_minimalista.png`: hierarquia tipográfica com símbolo acima.
- `banner_*_guia.png`: cada composição com máscara e indicação da área segura; somente revisão.
- `previa_recortes.png`: comparação de faixas desktop e recortes centrais reduzidos a 600 px.
- `gerar_banner.py`: fonte editável e reproduzível; usa fontes e símbolo oficiais por caminhos relativos.
- `qa_banner.json`: dimensões, bytes e limites geométricos de cada bloco essencial.

## Área segura e exportação

PNG RGB, 2560×1440. Guia conservador central: 1544×422 px, de (508,509) a (2052,931).
A [Ajuda oficial do YouTube](https://support.google.com/youtube/answer/10456525?hl=pt-BR), consultada nesta rodada, informa 1235×338 px seguros na dimensão mínima de 2048×1152 e recomenda 2560×1440. Ao escalar por 1,25, obtém-se aproximadamente 1544×423 px. O guia arredonda para dentro; todos os textos e o símbolo ficam dentro dele com margem.

As três exportações têm menos de 6 MB. Não enviar os arquivos de guia ou a prancha de revisão como banner.

## Identidade e QA

Símbolo preservado de `assets/branding/master/parallax_lab_icon_transparent.png`, com corte apenas do padding transparente e redução proporcional. Marca e assinatura em Space Grotesk; linha secundária em Inter. Fundo #050816, ciano #35D9FF protagonista e violeta contido. Sem fórmulas, CTA ou contatos.

Validação: geração das três variantes, assertions de limites seguros/tamanho, abertura dos PNGs e inspeção visual das composições completas, guias e recortes. Conteúdo íntegro, sem sobreposição ou clipping observado. A versão institucional oferece o melhor equilíbrio entre presença da marca, espaço negativo e leitura da assinatura; a cinematográfica dá mais presença ao símbolo.

O Python da `.venv` não iniciou no ambiente de execução desta rodada; foi usado o runtime Python já fornecido pelo Codex com Pillow/numpy. Ambiente e dependências do projeto não foram alterados. Reprodução: `python assets/branding/youtube/banner/gerar_banner.py` com Pillow/numpy disponíveis.

Não houve publicação/upload; o recorte efetivo no YouTube Studio e a leitura física em aparelho não foram verificados. As prévias são recortes geométricos, não capturas da plataforma. Alterações existentes no repositório foram preservadas.

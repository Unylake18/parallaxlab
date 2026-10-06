# Banner YouTube — Parallax Lab (proposta Claude)

Entrega: 05/10/2026. Alternativa à rodada já existente em `../banner/` (não alterada).
Principal recomendada: `banner_02_cinematografico.png`.

## Arquivos

- `banner_01_institucional.png`: lockup horizontal centrado (símbolo + logotipo), assinatura em ciano numa linha.
- `banner_02_cinematografico.png`: símbolo grande à esquerda; logotipo, assinatura em duas linhas (branco /
  gradiente ciano→violeta) e linha secundária à direita.
- `banner_03_minimalista.png`: só tipografia sobre fundo quase liso; logotipo grande, filete em gradiente.
- `banner_04_minimalista_cosmico.png`: layout da 03 sobre o fundo cósmico do canal; logotipo oficial PARALLAX LAB,
  assinatura e linha secundária em Space Grotesk Medium.
- `banner_*_guia.png`: guias de TV, desktop, tablet e área segura (só para revisão; não enviar ao YouTube).
- `previa_recortes.png`: faixa de desktop (2560×423) e recorte do celular (1546×423) de cada variação.
- `gerar_banner.py`: fonte editável e reproduzível (Pillow + numpy).
- `qa_banner.json`: resolução, tamanho e caixas do conteúdo essencial de cada variação.

## Marca e fundo

Símbolo e logotipo PARALLAX LAB são os oficiais (`master/parallax_lab_icon_transparent.png` e o logotipo
recortado de `overlays/parallax_lab_watermark.png`), sem redesenho; muda só a proporção símbolo/logotipo.
Assinatura em Space Grotesk; linha secundária em Inter. Fundo das variações 01 e 02: o banner 16:9 oficial com
o lockup central apagado e o miolo escurecido para leitura; nebulosas e planeta ficam só nas bordas.

## Área segura e QA

PNG RGB 2560×1440 (< 6 MB). Área segura 1546×423, de (507, 508) a (2053, 931). O script recusa exportar se
qualquer bloco essencial (símbolo, logotipo, assinatura, linha secundária) passar a menos de 20 px da borda
da área segura. Recorte real no YouTube Studio e leitura em aparelho não verificados.

# Padrões de produção

Observações de `vid_0001` e `vid_0002`, não requisitos automáticos dos próximos vídeos.

## Validados em múltiplos vídeos

- Resolver e conferir a primitiva pela derivada antes da animação. Os dois vídeos recuperam exatamente seus integrandos.
- Uma relação central legível por vez, com justificativa da escolha matemática e verificação no fim. A transformação mostra a conta, sem esconder a passagem decisiva.
- Quadro lógico 9×16; preview 540×960/15 fps e finais 1080×1920/30 fps. Equações grandes, watermark discreto e faixa inferior reservada à legenda funcionaram nos dois QA técnicos. Leitura física em celular ainda não foi comprovada.
- A fala aprovada orienta a permanência das fórmulas. Ambos preservam narração final, SRT separado com até duas linhas, escrita matemática visual (`du`, `dx`, símbolos) e MP4 com áudio e legendas.
- Usar correspondência visual explícita quando ela ajuda; quando não ajuda, entrar/sair com fades. `TransformMatchingTex` funcionou em passos do vídeo 1; no vídeo 2, cópias curtas e destino preparado esclareceram `u` e `du`.
- Final limpo e final legendado são saídas distintas. Nome, duração, áudio e SRT precisam estar identificados na ficha da unidade; MP4s ficam fora do Git pela política atual.

## Validados em um vídeo / candidatos

- `vid_0001`: sete blocos de TTS aprovados foram mantidos como fontes e montados em uma narração final. Este fluxo não define quantidade obrigatória de blocos.
- `vid_0002`: exportação única do ElevenLabs Studio, corte de silêncio inicial e ajuste pontual de nível funcionaram; Studio não é ferramenta obrigatória. A voz foi a referência explícita para refinar a cena.
- `vid_0002`: CTA discreto no último estado e coda de F/F′ sincronizada com os sinais funcionaram no QA; ainda falta repetição em outra unidade e revisão física.
- `vid_0002`: a escrita do SRT foi limpa de formas fonéticas como “dê u” para `du`. Texto para TTS e texto para legenda têm funções distintas.

## Soluções específicas

- `vid_0001`: redução do grau de x² para x justifica duas integrações por partes; distribuição do −2 e cancelamentos na regra do produto são deste exercício.
- `vid_0002`: `x² → u`, `2x dx → du`, regra da cadeia concreta e gráficos de `sin(x²)` com sua derivada são desta substituição. A coda reforça a relação já demonstrada e pode ser retirada sem perder a solução.

## Armadilhas conhecidas

- Na revisão do vídeo 2, auxiliares de `MathTex`, chaves e rótulos em movimento criaram sobreposições; separar origem, cópia e destino resolveu. Uma fórmula geral `f(g(x))` acrescentou uma camada desnecessária e foi removida.
- Os previews intermediários dos dois vídeos se acumularam em `renders/` e `media/`; os finais e o histórico em Markdown bastam após o QA.
- Confundir a fonetização usada para TTS com a legenda produziu texto pouco natural no vídeo 2.
- `uv run` falhou durante o render final do piloto no ambiente restrito do Codex, e outro runtime Python 3.12 com os pacotes da `.venv` permitiu concluir o render. O diagnóstico posterior confirmou `.venv`, cache e Manim saudáveis: faltava acesso aos caminhos externos do usuário. Se o erro reaparecer apenas nesse ambiente restrito, verificar permissões antes de recriar a `.venv` ou limpar o cache.

## Convenções de arquivos

- `videos/vid_NNNN_assunto/`: `cena.py`, `ficha.md`, `roteiro.md`, `revisao.md`, `publicacao.md`, `legenda.srt`, `audio/` e `capa_instagram.png` quando existir.
- `audio/narracao_final.*` preserva a fonte aprovada. Se a montagem exigir uma derivação, identificá-la como `audio/narracao_montagem.*` e guardar a receita.
- `renders/vid_NNNN_assunto_final_master_limpo.mp4` e `renders/vid_NNNN_assunto_final_legendado.mp4` são os dois entregáveis locais. `renders/` e `media/` são ignorados pelo Git; backup externo dos MP4s ainda precisa ser confirmado.
- `docs/estado_atual.md` registra a realidade operacional; `docs/decisoes.md`, decisões duradouras; `docs/identidade_visual.md`, marca; este arquivo, aprendizado empírico; a pasta da unidade, fatos daquele vídeo.

## Checklist de fechamento

1. Conferir conta e derivada independentemente; comparar cena, roteiro, voz e SRT.
2. Verificar no MP4 final resolução, fps, duração, áudio, início/fim e leitura de fórmulas/legendas/CTA em amostras.
3. Identificar master, legendado, fontes e capa; preservar fontes não regeneráveis e limpar previews substituídos.
4. Registrar publicação apenas com link/data reais; conferir em celular e confirmar backup dos MP4s antes de publicar.

Nenhum helper Manim foi extraído: `template.config` já atende aos dois, mas os
helpers de animação não mostram repetição suficiente. Os scripts pequenos de
montagem de áudio e legendas em `videos/` resolvem uma etapa técnica comum,
sem impor animação ou didática aos vídeos futuros.

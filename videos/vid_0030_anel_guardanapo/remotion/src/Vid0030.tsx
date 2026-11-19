// vid_0030 — composição Remotion. Remotion = maestro: não faz 3D nem matemática.
// Camadas, de baixo para cima: (1) fundo, (2) PNG por quadro do Three.js, (3) Manim CenaMat (PNG RGBA por quadro),
// (4) interface em React, lida do mesmo timeline.json e do mesmo ancoras_15fps.json.
// v3: layout por zonas (timeline "zonas"): título 56–118 px (máx. 2 linhas, um por vez), rótulos do 3D afastados
// ≥ 12 px da caixa projetada da silhueta (ancoras: "caixas"), margem lateral ≥ 24 px; cada texto aparece uma vez.
// Com a prop qa = true, cada quadro registra no console as caixas de todo elemento com data-g (QA de sobreposição).
import React, { useLayoutEffect } from 'react';
import { AbsoluteFill, Audio, Img, staticFile, useCurrentFrame, useVideoConfig, spring, continueRender, delayRender } from 'remotion';
import TL from '../../timeline.json';
import ANC15 from '../../ancoras_15fps.json';
import ANC30 from '../../ancoras_30fps.json';
let ANC: any = ANC15;                                                 // trocado pelo fps da composição (15 preview · 30 master)

const E: any = TL.eventos, G: any = TL.geometria;
// v4.2 (Kaio): h sempre magenta; R branco; ciano (acento) só para destaques que não são grandeza
const C = { h: '#EA63FF', R: '#F2F6FF', acento: '#35D9FF', a: '#9C8CFF', geo: '#B8C4DA', dim: '#8FA3C4', txt: '#F2F6FF', panel: '#0E2A52', borda: '#7FB2FF',
  fundo: '#050816', anel: '#5C93FF', esf: '#EA63FF', azulClaro: '#9CC8FF', Rtxt: '#F2F6FF' };   // Rtxt: magenta clareado (v4, contraste)
const MARGEM = 24, FOLGA = 12, RS = 28;                                // px no 540×960; RS = tamanho dos rótulos do 3D (v4)

// ---------- tempo (mesmas funções do cena3d.js e do cena.py) ----------
const clamp = (x: number, a: number, b: number) => Math.min(b, Math.max(a, x));
const suave = (u: number) => u * u * (3 - 2 * u);
const rampa = (t: number, t0: number, d: number) => suave(clamp((t - t0) / d, 0, 1));
// v4: entrada e saída de texto em no máximo 0,4 s (fórmula/rótulo legível desde a entrada)
const vis = (t: number, tin: number, din: number, tout = 1e9, dout = 0.6) =>
  rampa(t, tin, Math.min(din, 0.4)) * (1 - rampa(t, tout, Math.min(dout, 0.4)));
const pulso = (t: number, t0: number, d = 0.8) => { const u = clamp((t - t0) / d, 0, 1); return suave(1 - Math.abs(2 * u - 1)); };

// ---------- fonte Space Grotesk (de assets/, só leitura) ----------
const fonte = new FontFace('Space Grotesk', `url(${staticFile('fonts/SpaceGrotesk-Medium.ttf')})`, { weight: '500' });
const espera = delayRender('fonte Space Grotesk');
fonte.load().then(f => { (document as any).fonts.add(f); continueRender(espera); });

type Seg = string | [string, string];   // texto simples ou [texto, cor]
type Caixa = [number, number, number, number];
const caixaEm = (q: number, nome: string): Caixa | undefined => ((ANC as any).caixas[Math.min(ANC.quadros.length - 1, q)] || {})[nome];

export const Vid0030: React.FC<{ qa?: boolean }> = ({ qa }) => {
  const f = useCurrentFrame(), { fps, width: W, height: H } = useVideoConfig(), t = f / fps;
  ANC = fps === 30 ? ANC30 : ANC15;
  const u = W / 9, k = W / 540;                                        // px por unidade do Manim; escala do 540
  const px = (x: number, y: number): [number, number] => [(x + 4.5) / 9 * W, (8 - y) / 16 * H];
  const q = Math.min(ANC.quadros.length - 1, f);
  const anc = (n: string): [number, number] => { const [x, y] = (ANC.quadros[q] as any)[ANC.nomes.indexOf(n)]; return [x, y]; };
  const val = (n: string): number => (ANC.valores[q] as any)[ANC.valores_nomes.indexOf(n)];
  const fs = (size: number) => 0.8 * size * k;                         // tamanho do words() do Manim → px de CSS
  const mola = (t0: number) => spring({ frame: f - Math.round(t0 * fps), fps, config: { damping: 15, stiffness: 120 } });
  const larg = (txt: string, size: number) => txt.length * fs(size) * 0.6;   // largura estimada (caixa alta)

  // QA: caixas reais de cada elemento marcado (data-g), relativas ao quadro, no console (--log=verbose); não muda pixel
  useLayoutEffect(() => {
    const raiz = document.getElementById('quadro-vid0030');
    if (!qa || !raiz) return;
    const itens: any[] = [], o = raiz.getBoundingClientRect();
    raiz.querySelectorAll('[data-g]').forEach(el => {
      const r = (el as Element).getBoundingClientRect(), op = +((el as HTMLElement).dataset.op || 1);
      if (r.width > 0 && r.height > 0 && op > 0.003)
        itens.push([(el as HTMLElement).dataset.g, +(r.left - o.left).toFixed(1), +(r.top - o.top).toFixed(1), +(r.right - o.left).toFixed(1),
          +(r.bottom - o.top).toFixed(1), +op.toFixed(3), (el.textContent || '').slice(0, 60)]);
    });
    console.log('QA|' + f + '|' + JSON.stringify(itens));
  });

  // Texto centrado no ponto (X, Y) em px; 'esq' encosta a borda esquerda no ponto.
  const TxPx: React.FC<{ X: number; Y: number; size: number; segs: Seg[]; op: number; g: string; cor?: string; lado?: 'esq'; escala?: number }> =
    ({ X, Y, size, segs, op, g, cor = C.txt, lado, escala = 1 }) => {
      if (op <= 0.003) return null;
      return (
        <div data-g={g} data-op={op} style={{ position: 'absolute', left: X, top: Y, transform: `translate(${lado === 'esq' ? '0' : '-50%'}, -50%) scale(${escala})`,
          transformOrigin: lado === 'esq' ? 'left center' : 'center', fontFamily: 'Space Grotesk', fontWeight: 500, fontSize: fs(size),
          color: cor, opacity: op, whiteSpace: 'pre', lineHeight: 1 }}>
          {segs.map((s, i) => typeof s === 'string' ? <span key={i}>{s}</span> : <span key={i} style={{ color: s[1] }}>{s[0]}</span>)}
        </div>);
    };
  const Tx: React.FC<{ x?: number; y: number; size: number; segs: Seg[]; op: number; g: string; cor?: string; escala?: number }> =
    ({ x = 0, y, ...r }) => { const [X, Y] = px(x, y); return <TxPx X={X} Y={Y} {...r} />; };

  // Título de cena: zona 56–118 px, uma ou duas linhas (posições fixas: a 1ª linha não pula quando a 2ª chega).
  const Y_T1 = 87, Y_TA = 73, Y_TB = 103;
  const Titulo: React.FC<{ linhas: [Seg[], number][]; size?: number }> = ({ linhas, size = 30 }) => (
    <>{linhas.map(([segs, op], i) => <TxPx key={i} X={W / 2} Y={(linhas.length === 1 ? Y_T1 : i === 0 ? Y_TA : Y_TB) * k}
      size={size} segs={segs} op={op} g="titulo" />)}</>);

  // Lado do rótulo de uma régua, escolhido UMA vez para todo o intervalo em que ela aparece (sem pular de lado):
  // 'esq' = à esquerda da haste, se couber em todos os quadros com margem e folga da silhueta; senão 'cima' da silhueta.
  const ladoRegua = (n: string, solido: string, w: number, t0: number, t1: number): 'esq' | 'cima' => {
    const iN = ANC.nomes.indexOf(`${n}_cima`), iB = ANC.nomes.indexOf(`${n}_baixo`);
    for (let qq = Math.round(t0 * fps); qq <= Math.min(ANC.quadros.length - 1, Math.round(t1 * fps)); qq++) {
      const [ax] = px(...((ANC.quadros[qq] as any)[iN] as [number, number]));
      const [, ay] = px(...((ANC.quadros[qq] as any)[iN] as [number, number])), [, by] = px(...((ANC.quadros[qq] as any)[iB] as [number, number]));
      const b = caixaEm(qq, solido), x1 = ax - 0.14 * u, x0 = x1 - w, yc = (ay + by) / 2;
      if (x0 < MARGEM * k) return 'cima';
      if (b && x1 > b[0] * k - FOLGA * k && yc + fs(RS) / 2 > b[1] * k && yc - fs(RS) / 2 < b[3] * k) return 'cima';
    }
    return 'esq';
  };

  // Régua de h ancorada em 3D, quadro a quadro: haste entre n_cima/n_baixo (fora da silhueta, no mesmo plano de
  // profundidade das arestas do anel) + linhas de chamada tracejadas até as arestas. Rótulo pelo lado escolhido acima.
  const Regua: React.FC<{ n: string; solido: string; rotulo: string; op: number; janela: [number, number] }> = ({ n, solido, rotulo, op, janela }) => {
    if (op <= 0.003) return null;
    const [ax, ay] = px(...anc(`${n}_cima`)), [bx, by] = px(...anc(`${n}_baixo`));
    const [ex, ey] = px(...anc(`${n}_aresta_cima`)), [fx, fy] = px(...anc(`${n}_aresta_baixo`));
    const tk = 0.12 * u, sw = 3 * k, w = larg(rotulo, RS) + 12 * k, lado = ladoRegua(n, solido, w, janela[0], janela[1]);
    let rx: number, ry: number, tr: string;
    if (lado === 'esq') { rx = ax - 0.14 * u; ry = (ay + by) / 2; tr = 'translate(-100%, -50%)'; }
    else {
      const b = caixaEm(q, solido) || [ax / k, ay / k, ax / k, ay / k];
      rx = clamp(ax, MARGEM * k + w / 2, W - MARGEM * k - w / 2); ry = b[1] * k - FOLGA * k; tr = 'translate(-50%, -100%)';
    }
    return (
      <>
        <svg width={W} height={H} style={{ position: 'absolute', left: 0, top: 0, opacity: op }}>
          <g stroke={C.h} strokeWidth={1.5 * k} strokeDasharray={`${4 * k} ${4 * k}`} opacity={0.75}>
            <line data-g={`${n}_chamada`} data-op={op} x1={ax} y1={ay} x2={ex} y2={ey} />
            <line data-g={`${n}_chamada`} data-op={op} x1={bx} y1={by} x2={fx} y2={fy} />
          </g>
          {/* v4: halo escuro sob a haste (lê sobre qualquer fundo) */}
          <g stroke={C.fundo} strokeWidth={sw + 5 * k} strokeLinecap="butt" opacity={0.85}>
            <line x1={ax} y1={ay} x2={bx} y2={by} /><line x1={ax - tk} y1={ay} x2={ax + tk} y2={ay} /><line x1={bx - tk} y1={by} x2={bx + tk} y2={by} />
          </g>
          <g stroke={C.h} strokeWidth={sw} strokeLinecap="butt">
            <line data-g={n} data-op={op} x1={ax} y1={ay} x2={bx} y2={by} />
            <line data-g={n} data-op={op} x1={ax - tk} y1={ay} x2={ax + tk} y2={ay} />
            <line data-g={n} data-op={op} x1={bx - tk} y1={by} x2={bx + tk} y2={by} />
          </g>
        </svg>
        <div data-g={`${n}_rot`} data-op={op} style={{ position: 'absolute', left: rx, top: ry, transform: tr, fontFamily: 'Space Grotesk',
          fontWeight: 500, fontSize: fs(RS), color: C.h, opacity: op, whiteSpace: 'pre', lineHeight: 1, padding: `${3 * k}px ${6 * k}px`,
          background: 'rgba(5,8,22,0.82)', borderRadius: 4 * k }}>{rotulo}</div>
      </>);
  };

  // Rótulo à direita da silhueta de um anel do trio (≥ 12 px dela), centrado na altura do anel; linhas extras abaixo.
  const RotTrio: React.FC<{ i: number; linhas: [Seg[], number, string?][]; size: number }> = ({ i, linhas, size }) => {
    const b = caixaEm(q, `trio${i}`);
    if (!b) return null;
    const X = b[2] * k + FOLGA * k, Yc = (b[1] + b[3]) / 2 * k, passo = fs(size) * 1.25;
    return <>{linhas.map(([segs, op, cor], j) =>
      <TxPx key={j} X={X} Y={Yc + (j - (linhas.length - 1) / 2) * passo} size={size} lado="esq" segs={segs} op={op} cor={cor}
        g={`rot_trio${i}`} />)}</>;
  };

  const Chip: React.FC<{ y: number; size: number; texto: string; op: number; g: string }> = ({ y, size, texto, op, g }) => {
    if (op <= 0.003) return null;
    const [X, Y] = px(0, y);
    return <div data-g={g} data-op={op} style={{ position: 'absolute', left: X, top: Y, transform: 'translate(-50%, -50%)', padding: `${0.16 * u}px ${0.2 * u}px`,
      background: 'rgba(14,42,82,0.9)', border: `${2 * k}px solid ${C.borda}`, borderRadius: 0.12 * u, fontFamily: 'Space Grotesk', fontWeight: 500,
      fontSize: fs(size), color: C.txt, opacity: op, whiteSpace: 'pre', lineHeight: 1 }}>{texto}</div>;
  };

  // Etiquetas do hook: abaixo da maior caixa (anel + guardanapo + esfera fantasma) da janela inteira — fixas.
  const tagY = (() => {
    let fundo = 0;
    for (let qq = Math.round(E.tag_guardanapo * fps); qq <= Math.round(E.tag_furada_sai * fps + 15); qq++)
      for (const nm of ['trio1', 'guardanapo', 'fantasma']) { const b = caixaEm(qq, nm); if (b) fundo = Math.max(fundo, b[3]); }
    return fundo;
  })();

  const num = (v: number, d: number) => v.toFixed(d).replace('.', ',');
  const fim = E.endcard;
  const cabec = 1 - rampa(t, fim, 0.4);
  const hook = (t0: number) => Math.min(1, mola(t0)) * (1 - rampa(t, E.hook_sai, 0.6));
  const c04 = vis(t, E.cav_contadores + 0.45, 0.6, E.cav_sai, 0.8);
  const c06 = vis(t, E.prova_contador, 0.7, E.contador_sai, 0.4);
  const rg06 = vis(t, E.prova_contador, 0.7, E.prova_sai, 0.6);
  const prot = vis(t, E.protecao_c06 + 0.4, 0.8, E.prova_sai, 0.6);
  const t07 = vis(t, E.trio_final + 1.2, 0.6, E.fecho_sai, 0.6);   // só com a câmera parada no trio
  const pA = Math.max(0, ...E.cav_pulso.slice(1).map((tp: number) => pulso(t, tp)));
  const dz = (z: number) => (z >= 0 ? '+' : '') + num(z, 1);

  return (
    <AbsoluteFill id="quadro-vid0030" style={{ background: C.fundo }}>
      {/* v5: narração v2.1 (a cena foi sincronizada a ela: timeline.json "audio") */}
      <Audio src={staticFile('audio/narracao_v2.wav')} />
      {/* (2) 3D: um PNG por quadro do Three.js */}
      <Img src={staticFile(`frames3d/f${String(f).padStart(5, '0')}.png`)} style={{ position: 'absolute', width: W, height: H }} />
      {/* (3) matemática exata do Manim, com alfa (PNG RGBA por quadro: remotion/manim_png.py) */}
      <Img src={staticFile(`manim_png/f${String(f).padStart(5, '0')}.png`)} style={{ position: 'absolute', width: W, height: H }} />

      {/* (4) interface React · cabeçalho 0–50 px */}
      <Img data-g="cabecalho" data-op={0.4 * cabec} src={staticFile('marca/parallax_lab_watermark.png')}
        style={{ position: 'absolute', width: 1.8 * u, right: 0.28 * u, top: 0.28 * u, opacity: 0.4 * cabec }} />
      <div data-g="cabecalho" data-op={0.8 * cabec} style={{ position: 'absolute', left: 0.4 * u, top: 0.4 * u, fontFamily: 'Space Grotesk', fontWeight: 500, fontSize: fs(20),
        color: C.txt, opacity: 0.8 * cabec, whiteSpace: 'pre', lineHeight: 1 }}>ABSURDO CALCULÁVEL · EP. 03</div>

      {/* C01a · o objeto real; C01b · de onde vem o nome (a 1ª etiqueta sai antes da 2ª entrar, mesmo lugar) */}
      <TxPx X={W / 2} Y={tagY * k + FOLGA * k + fs(26) / 2 + 4 * k} size={26} cor="#E3F1FF" segs={['ANEL DE GUARDANAPO']}
        op={vis(t, E.tag_guardanapo, 0.6, E.tag_guardanapo_sai, 0.5)} g="tag_hook" />
      <TxPx X={W / 2} Y={tagY * k + FOLGA * k + fs(26) / 2 + 4 * k} size={26} cor="#E3F1FF" segs={['= ', ['ESFERA FURADA', '#F7B8FF']]}
        op={vis(t, E.tag_furada, 0.5, E.tag_furada_sai, 0.5)} g="tag_hook" />

      {/* C01c · a pergunta */}
      <Titulo size={32} linhas={[[['QUAL TEM MAIS VOLUME?'], hook(E.hook_titulo)],
        [['MESMA ALTURA: ', ['h = 6 cm', C.h]], hook(E.hook_titulo2)]]} />
      {G.trio.map((r: any, i: number) => <RotTrio key={i} i={i} size={RS} linhas={[[[`R = ${r.R} cm`], hook(E.hook_rotulos[i]), C.Rtxt]]} />)}
      {[0, 1, 2].map(i => <Regua key={i} n={`regua${i}`} solido={`trio${i}`} rotulo="6 cm" op={hook(E.hook_regua + i * 0.2)}
        janela={[E.hook_regua, E.hook_sai]} />)}

      {/* C03 · o raio sumiu (título, só no instante em que R sai) */}
      <Titulo linhas={[[['O ', ['RAIO DA ESFERA', C.R], ' SUMIU'], vis(t, E.R_sumiu_txt, 0.7, E.fatia_sai + 0.4, 0.4)]]} />

      {/* C04 · título e contadores (nos slots que as linhas usadas liberaram) */}
      <Titulo size={32} linhas={[[['MESMA ÁREA EM TODA ALTURA'], vis(t, E.cav_titulo, 0.7, E.cav_sai, 0.8)],
        [['LOGO, ', ['MESMO VOLUME', C.acento]], vis(t, E.cav_conclusao, 0.7, E.cav_sai, 0.8)]]} />
      <Tx y={-1.15} size={26} g="C04_cont" segs={[['z', C.geo], ` = ${dz(val('z'))} cm`.replace('+0,0', '0,0')]} op={c04} />
      <Tx x={anc('anel_base')[0]} y={-2.05} size={28} g="C04_cont" segs={[['A', C.anel], ` = ${num(val('A_anel_pi'), 2)}π cm²`]} op={c04} escala={1 + 0.12 * pA} />
      <Tx x={anc('esf_base')[0]} y={-2.05} size={28} g="C04_cont" segs={[['A', C.esf], ` = ${num(val('A_esfera_pi'), 2)}π cm²`]} op={c04} escala={1 + 0.12 * pA} />

      {/* C05 · as duas rotas */}
      <Titulo linhas={[[['DUAS ROTAS, ', ['O MESMO VOLUME', C.acento]], vis(t, E.volume_igual, 0.7, E.volume_sai, 0.6)]]} />

      {/* C06 · prova ao vivo */}
      <Titulo linhas={[[['MUDA A FORMA. NÃO MUDA O VOLUME.'], vis(t, E.forma_muda_txt, 0.7, E.prova_sai, 0.6)]]} />
      <Regua n="regua_anel" solido="anel" rotulo="h = 6 cm" op={rg06} janela={[E.prova_contador, E.prova_sai + 0.6]} />
      <Tx y={-2.04} size={28} g="C06_cont" segs={[['R', C.R], ` = ${num(val('R'), 1)} cm     `, ['a', C.a], ` = ${num(val('a_furo'), 1)} cm`]} op={c06} />
      <Chip y={-2.75} size={28} texto="V = 36π cm³ ≈ 113,1 cm³" op={c06} g="C06_chip" />
      <Tx y={-1.0} size={28} g="C06_prot" segs={['NÃO É QUALQUER FURO']} op={prot} />
      <Tx y={-1.45} size={28} g="C06_prot" segs={['QUE DÁ O MESMO VOLUME.']} op={prot} />
      <Tx y={-2.05} size={28} g="C06_prot" segs={['O QUE PRECISA SER IGUAL']} op={prot} />
      <Tx y={-2.5} size={28} g="C06_prot" segs={['É A ', ['ALTURA h', C.h], ' DO ANEL QUE SOBRA.']} op={prot} />

      {/* C07 · limites vistos no 3D: contador de h e V do anel que engrossa (a = 0) e afina (h → 0) */}
      {/* S14 (v5): h e V da MESMA altura interna; h com 2 casas, V = πh³/6 com 1 casa; pausas nos pontos exatos (timeline) */}
      <Tx y={-0.9} size={28} g="C07_cont" segs={[['h', C.h], ` = ${num(val('h'), 2)} cm     V = ${num(Math.PI * val('h') ** 3 / 6, 1)} cm³`]}
        op={vis(t, E.prova_sai + 0.5, 0.3, E.limites_sai, 0.3)} />   {/* entra parado em h = 6 cm (pausa ≥ 0,5 s) */}

      {/* C07 · trio de volta, volumes iguais, conclusão (a proteção não se repete aqui) */}
      {G.trio.map((r: any, i: number) => {
        const mv = Math.min(1, mola(E.trio_volumes + i * 0.25)) * (1 - rampa(t, E.fecho_sai, 0.6));
        return <RotTrio key={i} i={i} size={RS} linhas={[[[`R = ${r.R} cm`], t07, C.Rtxt], [['V = 36π cm³'], t < E.trio_volumes ? 0 : mv]]} />;
      })}
      {[0, 1, 2].map(i => <Regua key={i} n={`regua${i}`} solido={`trio${i}`} rotulo="6 cm" op={t07} janela={[E.trio_final + 1.2, E.fecho_sai + 0.6]} />)}
      <Titulo linhas={[[['SÓ A ', ['ALTURA', C.h], ' DETERMINA O VOLUME'], vis(t, E.conclusao_txt, 0.6, E.fecho_sai, 0.6)]]} />

      {/* END · cartão final */}
      {t >= fim && (() => {
        const sai = 1 - rampa(t, E.endcard_sai, 0.5), lg = rampa(t, fim + 0.4, 0.7) * sai, [lx, ly] = px(0, 2.3);
        return <>
          <Img data-g="end" data-op={lg} src={staticFile('marca/parallax_lab_watermark.png')} style={{ position: 'absolute', width: 4.4 * u, left: lx, top: ly,
            transform: `translate(-50%, -50%) scale(${0.96 + 0.04 * lg})`, opacity: lg }} />
          <Tx y={0.05} size={30} g="end" segs={['SE ESSA CONEXÃO ENTRE EQUAÇÃO']} op={rampa(t, fim + 1.1, 0.6) * sai} />
          <Tx y={-0.45} size={30} g="end" segs={['E FENÔMENO AJUDOU,']} op={rampa(t, fim + 1.1, 0.6) * sai} />
          <Tx y={-1.45} size={38} g="end" segs={['SEGUE O PARALLAX LAB']} op={rampa(t, fim + 1.7, 0.6) * sai} />
          {(() => { const [hx, hy] = px(0, -2.6), op = rampa(t, fim + 1.7, 0.6) * sai;
            return <div data-g="end" data-op={op} style={{ position: 'absolute', left: hx, top: hy, transform: 'translate(-50%, -50%)', fontFamily: 'Space Grotesk',
              fontWeight: 500, fontSize: fs(40), opacity: op, background: `linear-gradient(90deg, ${C.acento}, ${C.esf})`,
              WebkitBackgroundClip: 'text', backgroundClip: 'text', color: 'transparent', lineHeight: 1.1 }}>@labparallax</div>; })()}
        </>;
      })()}
    </AbsoluteFill>
  );
};

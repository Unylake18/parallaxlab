"""Narração v1.1 (handoff v2 §3–4): troca H1–H3, A2, B1-1, S1, S2, EN; cria B1-0; remove B1-8. Gera narracao_v11.md e ancoras.json (2,7 palavras/s)."""
import json,re
from pathlib import Path
U=Path(__file__).resolve().parent
v1=(U/'_v1'/'narracao_v1.md').read_text(encoding='utf-8')
blocos=re.findall(r'^(### ([^\n]+)\n(.*?))(?=^### |^## |\Z)',v1,re.M|re.S)
cab=re.split(r'^### ',v1,flags=re.M)[0]
NOVO={
'H1':("`D_34`; as duas bancadas idênticas girando a 1 volta/s; mostradores `ω = 1 VOLTA/S` iguais; rótulos pequenos `RETO` e `TORTO`",
"[curious] Dois halteres iguais, com a mesma massa, girando no mesmo tipo de motor, com a mesma velocidade angular. Nos dois, o centro de massa está bem em cima do eixo. A única diferença: um está reto, e o outro está torto."),
'H2':("a base do torto começa a balançar (`FORA DE ESCALA`); setas azuis finas nos dois mancais do torto, opostas, girando; a base do reto parada",
"[curious] Agora repara nas bancadas. A da direita balança, uma vez a cada volta. A da esquerda fica quietinha. Os mancais do haltere torto estão sendo empurrados, e esse empurrão gira junto com ele."),
'H3':("congela; topo `ω CONSTANTE… E MESMO ASSIM HÁ TORQUE`; hold de 2 s",
"[thoughtful] Só que a velocidade angular não muda, e o centro de massa nem sai do lugar. Então para que serve esse torque que os mancais fazem? Como pode existir torque sem a velocidade angular aumentar?"),
'A2':("`MOMENTO ANGULAR DO CORPO RÍGIDO`; `NESTE VÍDEO:` e três ícones (cone · haltere torto · roda)",
"[thoughtful] Hoje o assunto é o momento angular de um corpo rígido, e a gente vai responder essa pergunta em três passos: primeiro uma bolinha num pêndulo, depois esse haltere torto, e no fim a roda de um carro. Os três contam a mesma história."),
'B1-0':("`P_34` mais perto (pêndulo com ~65% da altura da coluna), pêndulo cônico girando, mostrador `ω` constante; seta azul do torque do peso saindo do prego, com sombra no piso, girando junto com a bolinha",
"[thoughtful] Para entender o haltere, a gente começa com uma coisa mais simples: uma bolinha só. Nesse pêndulo, ela anda num círculo deitado, sempre com a mesma rapidez. E, em relação ao prego, o peso dela faz torque. De novo: torque, e a velocidade angular não muda."),
'S1':("`D_34` de novo, as duas bancadas girando; no torto, L⃗ inclinado girando e a base balançando; no reto, L⃗ vertical parado; à direita, escritas uma a uma: L_z = I_z ω · τ⃗ = dL⃗/dt · Eixo principal: L⃗ = I ω⃗; depois três cartões `PANEL`",
"[calm, satisfied] Então, por que só a bancada do haltere torto balança? Porque, no haltere torto, o momento angular não aponta ao longo do eixo. Ele fica inclinado e gira junto com o haltere. Um vetor que gira está mudando, e mudar o momento angular exige torque. Quem faz esse torque são os mancais, e o empurrão deles, girando, balança a bancada. Esse torque é perpendicular ao eixo, por isso não muda a rapidez do giro: ele só muda a direção do momento angular. No haltere reto, o eixo é principal, o momento angular fica alinhado e ninguém precisa empurrar nada. Resumindo: a componente ao longo do eixo é sempre o momento de inércia vezes a velocidade angular. Mas o vetor inteiro só fica paralelo ao eixo quando o eixo é principal."),
'S2':("`plataforma_livre` girando; as massas deslizam para dentro; o mostrador vai de 1 para 3 voltas/s",
"[curious] E agora uma última cena. Uma plataforma girando livre, sem motor nenhum empurrando. Lá no meio, um carretel puxa as duas massas para perto do eixo. Nada de fora faz torque nela… e ela passa a girar três vezes mais rápido. Quem acelerou essa plataforma? E por que exatamente três vezes? É isso que a gente vai explorar quando o assunto for a conservação do momento angular."),
'EN':("encerramento padrão; ao lado da pergunta, a roda pequena com **um** excesso só (o CM sai do eixo: um ponto rosa fora do eixo)",
"[happy] Se essas conexões ajudaram você, se inscreve no Parallax Lab para acompanhar os próximos vídeos. E deixa nos comentários: se a roda tivesse um excesso de massa só, numa face só, os apoios sentiriam só um binário, ou alguma coisa a mais? Até a próxima!"),
}
saida=[cab.rstrip()+'\n']
ordem=[];dados={}
for bloco,aid_full,corpo in blocos:
    aid=aid_full.split(' · tela:')[0].split(' ·')[0].strip()
    if aid in ('B1-8','B5-5'):continue          # B5-5 cortado (handoff v3 §6)
    tela=aid_full.split(' · tela:',1)[1].strip();fala=corpo.strip()
    if aid in NOVO:tela,fala=NOVO[aid]
    if aid=='B6-4':
        fala=fala.split(' E, como ele cresce')[0].rstrip()          # corte autorizado: frase dos 50 km/h
        tela=tela.replace('; CONTA: 50 km/h → binário ÷ 4','')
    if aid=='B1-1':fala=fala.replace('Antes de somar muitas partículas, vamos entender uma só.','Então vamos olhar para o momento angular dela.')
    if aid=='B1-1':tela=tela.replace('canto linha 2 `UM L QUE SÓ VIRA`; ','canto linha 2 `UM L QUE SÓ VIRA`; ')
    ordem.append((aid,tela,fala))
    if aid=='A1':pass
# B1-0 entra antes de B1-1
i=[a for a,_,_ in ordem].index('B1-1')
ordem.insert(i,('B1-0',)+NOVO['B1-0'])
md=cab.rstrip()+'\n\n'
for aid,tela,fala in ordem:md+=f'### {aid} · tela: {tela}\n{fala}\n\n'
(U/'narracao_v11.md').write_text(md,encoding='utf-8')
anc={};ids=[];q=0
for aid,tela,fala in ordem:
    limpa=re.sub(r'\[[^\]]*\]','',fala).strip();palavras=re.findall(r'\w+',limpa.lower())
    hold=2 if aid in ('H3','B1-6','B3-4','B5-4') else 0
    n=round((.5+len(palavras)/2.7+hold)*15)
    anc[aid]=dict(palavras=len(palavras),ini=q/15,fim=(q+n)/15,dur=n/15,nominal=n/15,fala=' '.join(palavras),original=fala.strip(),tela=tela.strip(),hold=hold,t=[round(.15+k/2.7,4) for k in range(len(palavras))])
    ids.append(aid);q+=n
(U/'ancoras.json').write_text(json.dumps(dict(origem='Handoff v2 (narração v1.1); 2,7 palavras/s; tempos estimados, sem voz',ordem=ids,ancoras=anc),ensure_ascii=False,indent=1),encoding='utf-8')
print(len(ids),'âncoras;',sum(a['palavras'] for a in anc.values()),'palavras;',round(q/900,2),'min')

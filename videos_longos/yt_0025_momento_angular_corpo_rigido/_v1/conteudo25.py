"""Álgebra aprovada, transcrita por âncora; | separa tokens na MathTex de string única."""
CONTAS={
'B1-1':[r'\vec L|=|\vec r|\times|\vec p',r'\|\vec L\||=|r|p',r'\|\vec L\||=|\ell|m|v'],
'B1-3':[r'R|=|\ell|\sin|\theta',r'v|=|\omega|R',r'\|\vec L\||=|m|\omega|\ell^2|\sin|\theta',r'L_z|=|\|\vec L\||\sin|\theta',r'L_z|=|m|(\ell\sin\theta)^2|\omega',r'L_z|=|m|R^2|\omega',r'L_h|=|\|\vec L\||\cos|\theta',r'L_h|=|m|\omega|\ell^2|\sin|\theta|\cos|\theta'],
'B1-5':[r'\|d\vec L\||=|L_h|\cdot|\omega|dt',r'\left\|\frac{d\vec L}{dt}\right\||=|\omega|L_h',r'\tau|=|m|g|R',r'\tau|=|m|g|\ell|\sin|\theta'],
'B1-6':[r'\vec\tau|=|\frac{d\vec L}{dt}',r'mg\ell\sin\theta|=|\omega|\cdot|m\omega\ell^2\sin\theta\cos\theta',r'g|=|\omega^2|\ell|\cos|\theta',r'\omega^2|=|\frac{g}{\ell\cos\theta}',r'\omega|=|\sqrt{\frac{9{,}8}{1{,}00\cdot\cos30^\circ}}',r'\omega|=|3{,}36|\,\mathrm{rad/s}',r'T|=|\frac{2\pi}{\omega}|=|1{,}87|\,\mathrm{s}'],
'B1-8':[r'\vec\tau_{\mathrm{peso}}|+|\vec\tau_{\mathrm{fio}}|=|0',r'\vec L|=|\mathrm{constante}'],
'B2-1':[r'\vec L|=|\sum|\vec r_i|\times|\vec p_i',r'\frac{d\vec L}{dt}|=|\sum|\vec r_i|\times|\vec F_i',r'\vec F_i|=|\vec F_{\mathrm{ext}}|+|\vec F_{\mathrm{int}}',r'\frac{d\vec L}{dt}|=|\sum|\vec\tau_{\mathrm{ext}}'],
'B2-2':[r'\vec r_i|=|\vec\rho_i|+|z_i|\hat z'],
'B2-3':[r'\vec L_i|=|\vec r_i|\times|m_i|\vec v_i',r'\vec L_i|=|(\vec\rho_i+z_i\hat z)|\times|m_i|\vec v_i',r'\vec L_i|=|\vec\rho_i|\times|m_i|\vec v_i|+|z_i|\hat z|\times|m_i|\vec v_i'],
'B2-4':[r'm_i|\rho_i|v_i',r'v_i|=|\omega|\rho_i',r'm_i|\rho_i^2|\omega',r'L_z|=|\sum|m_i|\rho_i^2|\omega',r'L_z|=|(\sum m_i\rho_i^2)|\omega',r'L_z|=|I_z|\omega'],
'B2-5':[r'\vec\tau|=|\frac{d\vec L}{dt}',r'\tau_z|=|\frac{dL_z}{dt}',r'\tau_z|=|\frac{d(I_z\omega)}{dt}',r'\tau_z|=|I_z|\frac{d\omega}{dt}',r'\tau_z|=|I_z|\alpha'],
'B2-6':[r'L_z|=|I_z|\omega',r'\vec L_\perp|=|?'],
'B3-3':[r'\vec\rho_2|=|-|\vec\rho_1',r'z_2|=|-|z_1',r'z_2|\vec\rho_2|=|(-z_1)|(-\vec\rho_1)',r'z_2|\vec\rho_2|=|z_1|\vec\rho_1'],
'B3-5':[r'L_z|=|2|m|(\ell\sin\alpha)^2|\omega',r'L_z|=|2|\cdot|0{,}40|\cdot|(0{,}30\cdot0{,}5)^2|\cdot|2\pi',r'L_z|=|0{,}113|\,\mathrm{kg\,m^2/s}',r'L_\perp|=|2|m|\ell^2|\omega|\sin\alpha\cos\alpha',r'L_\perp|=|0{,}196|\,\mathrm{kg\,m^2/s}'],
'B3-6':[r'\vec L_\perp|=|-|\omega|\sum|m_i|z_i|\vec\rho_i',r'\vec\rho_i|=|(x_i,y_i)',r'\sum|mxz|\qquad|\sum|myz'],
'B4-1':[r'z|\vec\rho|+|z|(-\vec\rho)|=|0',r'\vec L_\perp|=|0'],
'B4-2':[r'L_z|=|I_z|\omega',r'\vec L|=|I|\vec\omega'],
'B5-1':[r'\frac{d\vec L}{dt}|=|\vec\omega|\times|\vec L',r'\left\|\frac{d\vec L}{dt}\right\||=|\omega|L_\perp',r'\tau|=|\omega|\cdot|2m\ell^2\omega\sin\alpha\cos\alpha',r'\tau|=|2m\ell^2|\omega^2|\sin\alpha\cos\alpha'],
'B5-2':[r'\omega|=|2\pi|\,\mathrm{rad/s}',r'L_\perp|=|0{,}196',r'\tau|=|1{,}23|\,\mathrm{N\,m}',r'\tau_z|=|0|\quad\Rightarrow\quad|\alpha|=|0'],
'B5-3':[r'\tau|=|F|d',r'F|=|\frac{\tau}{d}',r'F|=|\frac{1{,}23}{0{,}40}',r'F|=|3{,}1|\,\mathrm N'],
'B5-4':[r'F_c|=|m|\omega^2|\rho',r'F_c|=|0{,}40|\cdot|(2\pi)^2|\cdot|0{,}15',r'F_c|=|2{,}37|\,\mathrm N',r'\tau|=|F_c|\cdot|2\ell\cos\alpha',r'\tau|=|2{,}37|\cdot|0{,}52',r'\tau|=|1{,}23|\,\mathrm{N\,m}'],
'B5-5':[r'\tau|\propto|\omega^2',r'\omega|\times|3|\quad\Rightarrow\quad|\tau|\times|9',r'\tau|=|11{,}1|\,\mathrm{N\,m}',r'F|=|27{,}7|\,\mathrm N'],
'B6-2':[r'\sum|mxz|\ne|0'],
'B6-3':[r'v|=|\frac{100}{3{,}6}|=|27{,}8|\,\mathrm{m/s}',r'\omega|=|\frac vR',r'\omega|=|\frac{27{,}8}{0{,}30}',r'\omega|=|92{,}6|\,\mathrm{rad/s}',r'F|=|m|\omega^2|\rho',r'F|=|0{,}020|\cdot|92{,}6^2|\cdot|0{,}20',r'F|\approx|34|\,\mathrm N',r'\tau|=|F|\cdot|0{,}20',r'\tau|\approx|6{,}9|\,\mathrm{N\,m}'],
'B6-4':[r'50|\,\mathrm{km/h}',r'\omega|\div|2|\quad\Rightarrow\quad|\tau|\div|4'],
'B6-5':[r'\sum|mxz|=|0',r'\vec L|=|I|\vec\omega'],
'S1':[r'L_z|=|I_z|\omega',r'\vec\tau|=|\frac{d\vec L}{dt}',r'\vec L|=|I|\vec\omega']}

SELOS={
'B1-1':('HIPÓTESES','PONTO FIXO'),
'B1-6':('LEI GERAL',''),
'B1-8':('DE OUTRO PONTO',''),
'B2-1':('HIPÓTESES','FORÇAS INTERNAS'),
'B2-5':('RÍGIDO','MOMENTO DE INÉRCIA CONSTANTE'),
'B3-1':('HIPÓTESES','HASTE SEM MASSA'),
'B4-3':('REMONTADA',''),
'B5-3':('ATENÇÃO','SÓ A PARTE DO BINÁRIO'),
'B5-4':('CONFERE',''),
'B5-5':('CÂMERA LENTA','1/3'),
'B6-1':('HIPÓTESES','EIXO HORIZONTAL'),
'B6-2':('CÂMERA LENTA','VISTA EM RAIO X'),
'B6-3':('CÂMERA LENTA',''),
'B6-4':('CÂMERA LENTA',''),
'B6-5':('CÂMERA LENTA','VISTA EM RAIO X')}

TITULOS={'PH':'','PB1':'UM L QUE SÓ VIRA','PB2':'UM CORPO INTEIRO','PB3':'O HALTERE TORTO','PB4':'EIXO PRINCIPAL','PB5':'O QUE OS MANCAIS FAZEM','PB6':'A RODA','PS':'RESUMO'}
LOTES={'PH':['H1','H2','H3','A1','A2'], 'PB1':[f'B1-{i}' for i in range(1,9)],'PB2':[f'B2-{i}' for i in range(1,7)],'PB3':[f'B3-{i}' for i in range(1,8)],'PB4':[f'B4-{i}' for i in range(1,4)],'PB5':[f'B5-{i}' for i in range(1,6)],'PB6':[f'B6-{i}' for i in range(1,6)],'PS':['S1','S2','EN']}

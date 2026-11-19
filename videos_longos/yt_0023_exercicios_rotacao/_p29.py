def edit(P, pares):
    s = open(P, encoding='utf-8').read()
    for a, b in pares:
        assert s.count(a) == 1, (P, s.count(a), a[:100])
        s = s.replace(a, b)
    open(P, 'w', encoding='utf-8').write(s)
edit('sec_e1a.py', [
    ('''            self.v_flags["foco"] = nome.lower() if nome != "BLOCO" else ""
            pl = planos[nome]''', '''            self.v_flags["foco"] = nome.lower() if nome != "BLOCO" else ""
            self.v_flags["cord"] = nome == "BLOCO"                   # v5 OBJETO CORTADO: nos closes o fio e o bloco saem (o bloco saía cortado pela borda de baixo)
            pl = planos[nome]'''),
    ('''        self.gat("o bloco é solto do repouso")
        self.v_flags["foco"] = ""''', '''        self.gat("o bloco é solto do repouso")
        self.v_flags["foco"] = ""
        self.v_flags["cord"] = True'''),
    ('"ANEL": (-40.0, 10.0, 5.8, -3.85, 0.95, 0.0, 0.0)', '"ANEL": (-40.0, 10.0, 4.6, -3.85, 0.55, 0.0, 0.0)'),
])
print('ok')

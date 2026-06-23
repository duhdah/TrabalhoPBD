from database import conectar
import customtkinter as ctk

def carregarProjetos(colunaIdeias,colunaFazendo,colunaStandBy,colunaFeito,comboTipo,comboLider):
    for coluna in [colunaIdeias,colunaFazendo,colunaStandBy,colunaFeito]:
        for widget in coluna.winfo_children()[1:]:
            widget.destroy()

    tipo = comboTipo.get()
    lider = comboLider.get()

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT p.nomeProjeto, p.status, me.nomeCompleto
    FROM Projeto p JOIN Membro_Equipe me ON p.matriculaLider = me.matricula
    WHERE 1=1
    """
    parametros = []

    if tipo != "Todos":
        if tipo == "Ensino":
            sql += """
            AND EXISTS (
                SELECT 1
                FROM Projeto_Ensino pe
                WHERE pe.nomeProjeto = p.nomeProjeto
            )
            """

        if tipo == "Pesquisa":
            sql += """
            AND EXISTS (
                SELECT 1
                FROM Projeto_Pesquisa pp
                WHERE pp.nomeProjeto = p.nomeProjeto
            )
            """
        if tipo == "Extensao":
            sql += """
            AND EXISTS (
                SELECT 1
                FROM Projeto_Extensao px
                WHERE px.nomeProjeto = p.nomeProjeto
            )
            """

    if lider != "Todos":
        sql += " AND me.nomeCompleto = %s"
        parametros.append(lider)

    cursor.execute(sql, parametros)

    projetos = cursor.fetchall()

    cursor.close()
    conexao.close()

    for projeto in projetos:

        nome = projeto[0]
        status = projeto[1]

        if status == "Ideias":
            criarCardProjeto(colunaIdeias, nome)

        elif status == "Fazendo":
            criarCardProjeto(colunaFazendo, nome)

        elif status == "Stand By":
            criarCardProjeto(colunaStandBy, nome)

        else:
            criarCardProjeto(colunaFeito, nome)

def criarColuna(master, titulo, cor):
    frame = ctk.CTkFrame(master, corner_radius=20, fg_color=cor)
    texto = ctk.CTkLabel(frame, text=titulo, font=("Segoe UI", 20, "bold"))
    texto.pack(pady=10)
    return frame

def abrirDetalhesProjeto(nomeProjeto):
    print(nomeProjeto)

def criarCardProjeto(coluna, nomeProjeto):
    card = ctk.CTkButton(
        coluna,
        text=nomeProjeto,
        height=50,
        corner_radius=15,
        command=lambda: abrirDetalhesProjeto(nomeProjeto)
    )
    card.pack(fill="x", padx=10, pady=5)

def abrirTelaProjetos(janelaPrincipal):
    estadoPrincipal = janelaPrincipal.state()
    janelaPrincipal.withdraw()
    janelaProjetos = ctk.CTkToplevel()
    janelaProjetos.title("Projetos")
    janelaProjetos.geometry("1000x600")
    janelaPrincipal.configure(fg_color="#ffffff")
    
    if estadoPrincipal == "zoomed":
        janelaProjetos.state("zoomed")
    elif estadoPrincipal == "normal":
        janelaProjetos.state("normal")

    titulo = ctk.CTkLabel(janelaProjetos,text="Projetos",font=("Segoe UI", 32, "bold"))
    titulo.pack(pady=20)
    
    frameFiltros = ctk.CTkFrame(janelaProjetos,fg_color="transparent")
    frameFiltros.pack(pady=10)

    comboTipo = ctk.CTkComboBox(frameFiltros,values=["Todos","Ensino","Pesquisa","Extensao"],width=250)
    comboTipo.set("Todos")
    comboTipo.pack(side="left",padx=10)

    # Carregando os nomes dos petianos cadastrados no banco:
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT nomeCompleto
        FROM Membro_Equipe
        ORDER BY nomeCompleto
    """)

    lideres = ["Todos"]
    for linha in cursor.fetchall():
        lideres.append(linha[0])

    cursor.close()
    conexao.close()

    comboLider = ctk.CTkComboBox(frameFiltros,values=lideres,width=250)
    comboLider.set("Todos")
    comboLider.pack(side="left",padx=10)

    botaoFiltrar = ctk.CTkButton(frameFiltros,text="Filtrar")
    botaoFiltrar.pack(side="left",padx=10)

    areaKanban = ctk.CTkFrame(janelaProjetos, fg_color="transparent")
    areaKanban.pack(fill="both", expand=True, padx=20, pady=10)
    areaKanban.grid_columnconfigure((0,1,2,3), weight=1, uniform="col")
    areaKanban.grid_rowconfigure(0, weight=1)
    areaKanban.configure(height=500)
    areaKanban.pack_propagate(False)

    colunaIdeias = criarColuna(areaKanban, "Ideias", "#aac1ec")
    colunaFazendo = criarColuna(areaKanban, "Fazendo", "#aac1ec")
    colunaStandBy = criarColuna(areaKanban, "Stand By", "#aac1ec")
    colunaFeito = criarColuna(areaKanban, "Feito", "#aac1ec")

    colunaIdeias.grid(row=0, column=0, sticky="nsew", padx=10)
    colunaFazendo.grid(row=0, column=1, sticky="nsew", padx=10)
    colunaStandBy.grid(row=0, column=2, sticky="nsew", padx=10)
    colunaFeito.grid(row=0, column=3, sticky="nsew", padx=10)
    
    botaoFiltrar.configure(command=lambda:carregarProjetos(colunaIdeias,colunaFazendo,colunaStandBy,colunaFeito,comboTipo,comboLider))
    carregarProjetos(colunaIdeias,colunaFazendo,colunaStandBy,colunaFeito,comboTipo,comboLider)

    botaoAdicionar = ctk.CTkButton(janelaProjetos,text="+ Adicionar projeto",width=250,height=50)
    botaoAdicionar.pack(pady=20)

    def voltar():
        estadoProjetos = janelaProjetos.state()
        janelaProjetos.destroy()
        janelaPrincipal.deiconify()
        if estadoProjetos == "zoomed":
            janelaPrincipal.state("zoomed")
        else:
            janelaPrincipal.state("normal")
    
    botaoVoltar = ctk.CTkButton(janelaProjetos,text="Voltar",command=voltar)
    botaoVoltar.pack(pady=10)

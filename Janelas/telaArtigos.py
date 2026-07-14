from database import conectar
import customtkinter as ctk

def carregarArtigos(frameResultados, comboCongresso, comboStatus):

    for widget in frameResultados.winfo_children():
        widget.destroy()

    congresso = comboCongresso.get()
    status = comboStatus.get()

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT me.nomeCompleto, a.congresso, a.titulo, a.status,COALESCE(pa.nomeProjeto, 'Sem Projeto') AS nomeProjeto
    FROM Artigo_Cientifico a JOIN Membro_Equipe me ON a.matriculaAutor = me.matricula LEFT JOIN Projeto_Artigo pa ON pa.codigoArtigo = a.codigoArtigo
    WHERE 1=1
    """

    parametros = []

    if congresso != "Todos":
        sql += " AND TRIM(a.congresso) = %s"
        parametros.append(congresso.strip())

    if status != "Todos":
        sql += " AND TRIM(a.status) = %s"
        parametros.append(status.strip())

    cursor.execute(sql, parametros)

    artigos = cursor.fetchall()

    cursor.close()
    conexao.close()

    for artigo in artigos:

        autor = artigo[0]
        congresso = artigo[1]
        titulo = artigo[2]
        status = artigo[3]
        projeto = artigo[4]

        card = ctk.CTkFrame(frameResultados, corner_radius=20, fg_color="#c4cafb")
        card.pack(fill="x",padx=20,pady=10)

        card.grid_columnconfigure(0, weight=1, uniform="col")
        card.grid_columnconfigure(1, weight=1, uniform="col")

        lbl_projeto = ctk.CTkLabel(card, text=f"Projeto: {projeto}", font=("Segoe UI", 16), anchor="w")
        lbl_projeto.grid(row=0, column=0, sticky="w", padx=(20, 10))

        lbl_autor = ctk.CTkLabel(card, text=f"Autor: {autor}", font=("Segoe UI", 16), anchor="w")
        lbl_autor.grid(row=0, column=1, sticky="w", padx=(20, 10))

        lbl_congresso = ctk.CTkLabel(card, text=f"Congresso: {congresso}", font=("Segoe UI", 16), anchor="w")
        lbl_congresso.grid(row=1, column=0, sticky="w", padx=(20, 10))

        lbl_status = ctk.CTkLabel(card, text=f"Status: {status}", font=("Segoe UI", 16), anchor="w")
        lbl_status.grid(row=1, column=1, sticky="w", padx=(20, 10))
        
        lbl_titulo = ctk.CTkLabel(card, text=f"Título: {titulo}", font=("Segoe UI", 16), anchor="w")
        lbl_titulo.grid(row=2, column=0, columnspan=2, sticky="w", padx=(20, 10))


def abrirTelaArtigos(janelaPrincipal):
    estadoPrincipal = janelaPrincipal.state()
    janelaPrincipal.withdraw()
    janelaArtigos = ctk.CTkToplevel()
    janelaArtigos.title("Artigos")
    janelaArtigos.geometry("1000x600")

    if estadoPrincipal == "zoomed":
        janelaArtigos.state("zoomed")
    elif estadoPrincipal == "normal":
        janelaArtigos.state("normal")

    titulo = ctk.CTkLabel(janelaArtigos, text="Artigos", font=("Segoe UI", 32, "bold"))
    titulo.pack(pady=20)

    frameFiltros = ctk.CTkFrame(janelaArtigos,fg_color="transparent")
    frameFiltros.pack(pady=10)

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT DISTINCT congresso
        FROM Artigo_Cientifico
        ORDER BY congresso
    """)

    congressos = ["Todos"]

    for linha in cursor.fetchall():
        congressos.append(linha[0])

    cursor.close()
    conexao.close()

    comboCongresso = ctk.CTkComboBox(frameFiltros,values=congressos,width=250)
    comboCongresso.set("Todos")
    comboCongresso.pack(side="left",padx=10)

    comboStatus = ctk.CTkComboBox(
        frameFiltros,
        values=["Todos","Aceito","Submetido","Rejeitado","Publicado"],
        width=250
    )
    comboStatus.set("Todos")
    comboStatus.pack(side="left",padx=10)

    botaoFiltrar = ctk.CTkButton(frameFiltros, text="Filtrar", fg_color="#8b7fd9",hover_color="#7368bc",
        command=lambda:carregarArtigos(frameResultados,comboCongresso,comboStatus))
    botaoFiltrar.pack(side="left",padx=10)

    frameResultados = ctk.CTkScrollableFrame(janelaArtigos)
    frameResultados.pack(fill="both",expand=True,padx=20,pady=20)

    carregarArtigos(frameResultados,comboCongresso,comboStatus)

    def voltar():   
        estadoArtigos = janelaArtigos.state()
        janelaArtigos.destroy()
        janelaPrincipal.deiconify()
        if estadoArtigos == "zoomed":
            janelaPrincipal.state("zoomed")
        else:
            janelaPrincipal.state("normal")

    botaoVoltar = ctk.CTkButton(janelaArtigos,text="Voltar",command=voltar,width=120, fg_color="#8b7fd9",hover_color="#7368bc")
    botaoVoltar.pack(pady=10,anchor="e",padx=20)

    janelaArtigos.protocol("WM_DELETE_WINDOW", janelaPrincipal.destroy)

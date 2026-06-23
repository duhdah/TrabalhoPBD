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
    SELECT
        a.titulo,
        me.nomeCompleto,
        a.congresso,
        a.status
    FROM Artigo_Cientifico a
    JOIN Membro_Equipe me
        ON a.matriculaAutor = me.matricula
    WHERE 1=1
    """

    parametros = []

    if congresso != "Todos":
        sql += " AND a.congresso = %s"
        parametros.append(congresso)

    if status != "Todos":
        sql += " AND a.status = %s"
        parametros.append(status)

    cursor.execute(sql, parametros)

    artigos = cursor.fetchall()

    cursor.close()
    conexao.close()

    for artigo in artigos:

        titulo = artigo[0]
        autor = artigo[1]
        congresso = artigo[2]
        status = artigo[3]

        card = ctk.CTkFrame(frameResultados, corner_radius=20, fg_color="#aac1ec")
        card.pack(fill="x",padx=20,pady=10)

        texto = ctk.CTkLabel(
            card,justify="left",anchor="w",
            text=f"Título: {titulo}         "
            f"Autor: {autor}\n"
            f"Congresso: {congresso}        "
            f"Status: {status}",
            font=("Segoe UI", 16)
        )
        texto.pack(anchor="w", padx=20,pady=15)


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

    frameResultados = ctk.CTkScrollableFrame(janelaArtigos)
    frameResultados.pack(fill="both",expand=True,padx=20,pady=20)

    botaoFiltrar = ctk.CTkButton(
        frameFiltros,
        text="Filtrar",
        command=lambda:carregarArtigos(frameResultados,comboCongresso,comboStatus)
    )
    botaoFiltrar.pack(side="left",padx=10)

    carregarArtigos(frameResultados,comboCongresso,comboStatus)

    def voltar():   
        estadoArtigos = janelaArtigos.state()
        janelaArtigos.destroy()
        janelaPrincipal.deiconify()
        if estadoArtigos == "zoomed":
            janelaPrincipal.state("zoomed")
        else:
            janelaPrincipal.state("normal")

    botaoVoltar = ctk.CTkButton(janelaArtigos,text="Voltar",command=voltar,width=120)
    botaoVoltar.pack(pady=10,anchor="e",padx=20)
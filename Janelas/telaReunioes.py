from database import conectar
import customtkinter as ctk

def carregarReunioes(frameResultados):
    for widget in frameResultados.winfo_children():
        widget.destroy()

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT r.texto, r.assunto, r.data, r.coordenador, r.redator
    FROM Reuniao_Ata r
    ORDER BY r.data DESC
    """

    cursor.execute(sql)
    reunioes = cursor.fetchall()

    cursor.close()
    conexao.close()

    for reuniao in reunioes:

        titulo = reuniao[0]
        assunto = reuniao[1]
        data = reuniao[2]
        coordenador = reuniao[3]
        redator = reuniao[4]

        card = ctk.CTkFrame(frameResultados, corner_radius=20, fg_color="#aac1ec")
        card.pack(fill="x", padx=20, pady=10)

        texto = ctk.CTkLabel(
            card,
            justify="left",
            anchor="w",
            text=(
                f"Título: {titulo}        "
                f"Assunto: {assunto}        "
                f"Data: {data}\n"
                f"Coordenador: {coordenador}        "
                f"Redator: {redator}"
            ),
            font=("Segoe UI", 16)
        )
        texto.pack(anchor="w", padx=20, pady=15)

def abrirTelaReunioes(janelaPrincipal):
    estadoPrincipal = janelaPrincipal.state()
    janelaPrincipal.withdraw()
    janelaReunioes = ctk.CTkToplevel()
    janelaReunioes.title("Reuniões")
    janelaReunioes.geometry("1000x700")

    if estadoPrincipal == "zoomed":
        janelaReunioes.state("zoomed")
    else:
        janelaReunioes.state("normal")

    titulo = ctk.CTkLabel(janelaReunioes,text="Reuniões",font=("Segoe UI", 32, "bold"))
    titulo.pack(pady=20)

    frameResultados = ctk.CTkScrollableFrame(janelaReunioes)
    frameResultados.pack(fill="both", expand=True, padx=20, pady=20)

    carregarReunioes(frameResultados)

    def voltar():
        estadoReunioes = janelaReunioes.state()
        janelaReunioes.destroy()
        janelaPrincipal.deiconify()

        if estadoReunioes == "zoomed":
            janelaPrincipal.state("zoomed")
        else:
            janelaPrincipal.state("normal")

    botaoVoltar = ctk.CTkButton(janelaReunioes,text="Voltar",command=voltar,width=120)
    botaoVoltar.pack(pady=10, anchor="e", padx=20)

    janelaReunioes.protocol("WM_DELETE_WINDOW", janelaPrincipal.destroy)

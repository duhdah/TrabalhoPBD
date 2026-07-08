from database import conectar
import customtkinter as ctk

def carregarEventos(frameResultados):

    for widget in frameResultados.winfo_children():
        widget.destroy()

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT e.nomeProjeto, e.dataEvento, e.duracao
    FROM Evento e
    ORDER BY e.dataEvento
    """

    cursor.execute(sql)
    eventos = cursor.fetchall()

    cursor.close()
    conexao.close()

    for evento in eventos:
        nome_projeto = evento[0]
        data_evento = evento[1]
        duracao = evento[2]

        card = ctk.CTkFrame(frameResultados, corner_radius=20, fg_color="#aac1ec")
        card.pack(fill="x", padx=20, pady=10)

        texto = ctk.CTkLabel(
            card,justify="left",anchor="w",
            text=(
                f"Projeto: {nome_projeto}\n"
                f"Data: {data_evento}        "
                f"Duração: {duracao}h"
            ),
            font=("Segoe UI", 16)
        )
        texto.pack(anchor="w", padx=20, pady=15)

def abrirTelaEventos(janelaPrincipal):
    estadoPrincipal = janelaPrincipal.state()
    janelaPrincipal.withdraw()
    janelaEventos = ctk.CTkToplevel()
    janelaEventos.title("Eventos")
    janelaEventos.geometry("1000x600")

    if estadoPrincipal == "zoomed":
        janelaEventos.state("zoomed")
    else:
        janelaEventos.state("normal")

    titulo = ctk.CTkLabel(janelaEventos,text="Eventos",font=("Segoe UI", 32, "bold"))
    titulo.pack(pady=20)

    frameResultados = ctk.CTkScrollableFrame(janelaEventos)
    frameResultados.pack(fill="both", expand=True, padx=20, pady=20)

    carregarEventos(frameResultados)

    def voltar():
        estadoEventos = janelaEventos.state()
        janelaEventos.destroy()
        janelaPrincipal.deiconify()

        if estadoEventos == "zoomed":
            janelaPrincipal.state("zoomed")
        else:
            janelaPrincipal.state("normal")

    botaoVoltar = ctk.CTkButton(janelaEventos,text="Voltar",command=voltar)
    botaoVoltar.pack(pady=10, anchor="e", padx=20)
    
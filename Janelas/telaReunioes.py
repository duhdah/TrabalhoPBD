from database import conectar
import customtkinter as ctk

def carregarReunioes(frameResultados):
    for widget in frameResultados.winfo_children():
        widget.destroy()

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    SELECT r.texto, r.assunto, r.data,  mc.nomeCompleto, mr.nomeCompleto
    FROM Reuniao_Ata r
    JOIN Membro_Equipe mc ON r.matriculaCoordenador = mc.matricula
    JOIN Membro_Equipe mr ON r.matriculaRedator = mr.matricula
    ORDER BY r.data DESC
    """

    cursor.execute(sql)
    reunioes = cursor.fetchall()

    cursor.close()
    conexao.close()

    for reuniao in reunioes:

        texto_ata = reuniao[0]
        assunto = reuniao[1]
        data = reuniao[2]
        coordenador = reuniao[3]
        redator = reuniao[4]

        card = ctk.CTkFrame(frameResultados, corner_radius=20, fg_color="#c4cafb")
        card.pack(fill="x", padx=20, pady=10)

        card.grid_columnconfigure(0, weight=1, uniform="col")
        card.grid_columnconfigure(1, weight=1, uniform="col")

        lbl_assunto = ctk.CTkLabel(card, text=f"Assunto: {assunto}", font=("Segoe UI", 16, "bold"), anchor="w")
        lbl_assunto.grid(row=0, column=0, sticky="w", padx=(20, 10), pady=(15, 5))

        lbl_data = ctk.CTkLabel(card, text=f"Data: {data}", font=("Segoe UI", 16), anchor="w")
        lbl_data.grid(row=0, column=1, sticky="w", padx=(10, 20), pady=(15, 5))

        lbl_coordenador = ctk.CTkLabel(card, text=f"Coordenador: {coordenador}", font=("Segoe UI", 15), anchor="w")
        lbl_coordenador.grid(row=1, column=0, sticky="w", padx=(20, 10), pady=(5, 5))

        lbl_redator = ctk.CTkLabel(card, text=f"Redator: {redator}", font=("Segoe UI", 15), anchor="w")
        lbl_redator.grid(row=1, column=1, sticky="w", padx=(10, 20), pady=(5, 5))

        lbl_texto = ctk.CTkLabel(
            card, 
            text=f"Ata:\n{texto_ata}", 
            font=("Segoe UI", 14, "italic"), 
            justify="left", 
            anchor="w",
            wraplength=850
        )   
        lbl_texto.grid(row=2, column=0, columnspan=2, sticky="w", padx=20, pady=(10, 15))

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

    botaoVoltar = ctk.CTkButton(janelaReunioes,text="Voltar",command=voltar,width=120, fg_color="#8b7fd9",hover_color="#7368bc")
    botaoVoltar.pack(pady=10, anchor="e", padx=20)

    janelaReunioes.protocol("WM_DELETE_WINDOW", janelaPrincipal.destroy)

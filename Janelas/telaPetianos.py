from database import conectar
import customtkinter as ctk
from telaProjetos import abrirTelaProjetos
from PIL import Image

def abrirDetalhes(matricula):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT nomeCompleto, dataIngresso
        FROM Membro_Equipe
        WHERE matricula = %s
    """, (matricula,))
    nome, dataIngresso = cursor.fetchone()

    cursor.execute("""
        SELECT curso, semestre
        FROM Petiano
        WHERE matricula = %s
    """, (matricula,))
    petiano = cursor.fetchone()

    cursor.execute("""
        SELECT dataFimGestao
        FROM Tutor
        WHERE matricula = %s
    """, (matricula,))
    tutor = cursor.fetchone()

    cursor.execute("""
        SELECT nomeProjeto 
        FROM Projeto 
        WHERE matriculaLider = %s
        ORDER BY nomeProjeto
    """, (matricula,))
    projetos_liderados = [row[0] for row in cursor.fetchall()]

    cursor.execute("""
        SELECT nomeProjeto 
        FROM Projeto_Petiano 
        WHERE matricula = %s
        ORDER BY nomeProjeto
    """, (matricula,))
    projetos_participa = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conexao.close()

    janelaDetalhes = ctk.CTkToplevel()
    janelaDetalhes.title("Dados")       
    janelaDetalhes.geometry("400x300")
    janelaDetalhes.resizable(False, False)  
    janelaDetalhes.lift()
    janelaDetalhes.grab_set()   
    texto = f"""
        Nome: {nome} 
        Matrícula: {matricula} 
        Data de ingresso: {dataIngresso}"""
    if petiano:
        curso, semestre = petiano
        texto += f""" 
        Cargo: Petiano 
        Curso: {curso} 
        Semestre atual: {semestre}º
        Projetos que lidera:
        """
        if projetos_liderados:
            for proj in projetos_liderados:
                texto += f"""        • {proj}"""
        else:
            texto += """Não lidera nenhum projeto."""
        texto +=  """
        Projetos que participa:
        """
        if projetos_participa:
            for proj in projetos_participa:
                texto += f"""        • {proj}"""
        else:
            texto +=f"""Não participa de nenhum projeto."""
    elif tutor:
        dataFim = tutor[0]
        texto += f"""
        Cargo: Tutor 
        Fim da gestão: {dataFim}
        """

    label = ctk.CTkLabel(
        janelaDetalhes,
        text=texto,
        justify="left",
        anchor="w",
        font=("Segoe UI",14)
    )
    label.pack(fill="both",expand=True,padx=20,pady=20)

def carregarPetianos(area, linhaTopo):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT me.matricula, me.nomeCompleto
        FROM Tutor t
        JOIN Membro_Equipe me ON t.matricula = me.matricula;
    """)
    
    tutor = cursor.fetchone()
    if tutor:
        botaoTutor = criarPetiano(linhaTopo,tutor[0],tutor[1],"icon2.png")
        botaoTutor.pack(side="right", padx=10)

    cursor.execute("""
        SELECT me.matricula, me.nomeCompleto
        FROM Petiano p
        JOIN Membro_Equipe me ON p.matricula = me.matricula
        ORDER BY me.nomeCompleto
    """)

    petianos = cursor.fetchall()
    cursor.close()
    conexao.close()

    linha = 1
    coluna = 0
    for matricula, nome in petianos:    
        botao = criarPetiano(area,matricula,nome,"icon2.png")
        botao.grid(row=linha,column=coluna,sticky="nsew",padx=10,pady=10)
        coluna += 1
        if coluna == 4:
            coluna = 0
            linha += 1

def criarPetiano(frame, matricula, nome, imagem_path):
    icon2 = ctk.CTkImage(
        light_image=Image.open(imagem_path),
        dark_image=Image.open(imagem_path),
        size=(60, 60)
    )

    botao = ctk.CTkButton(
        frame,
        text=nome,
        image=icon2,
        compound="left",
        height=80,
        corner_radius=15,
        fg_color="#e8eafc",
        text_color="#1d2b7d",
        hover_color="#d8ddfc",
        command=lambda: abrirDetalhes(matricula)
    )

    return botao

def abrirTelaPetianos(janelaPrincipal):
    estadoPrincipal = janelaPrincipal.state()
    janelaPrincipal.withdraw()  
    janelaPetianos = ctk.CTkToplevel()
    janelaPetianos.title("Petianos")
    janelaPetianos.geometry("1000x600")     

    if estadoPrincipal == "zoomed":
        janelaPetianos.state("zoomed")
    elif estadoPrincipal == "normal":
        janelaPetianos.state("normal")

    area = ctk.CTkFrame(janelaPetianos, fg_color="transparent")
    area.pack(expand=True, fill="both", padx=20, pady=20)

    for i in range(4):
        area.grid_columnconfigure(i, weight=1, uniform="col")

    for i in range(4):
        area.grid_rowconfigure(i, weight=1)

    linha_topo = ctk.CTkFrame(area, fg_color="transparent")
    linha_topo.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)
    titulo = ctk.CTkLabel(linha_topo,text="Petianos",font=("Segoe UI", 26, "bold"),text_color="#1d2b7d")
    titulo.pack(side="left")    

    carregarPetianos(area, linha_topo)

    def voltar():
        estadoPetianos = janelaPetianos.state()
        janelaPetianos.destroy()
        janelaPrincipal.deiconify()
        if estadoPetianos == "zoomed":
            janelaPrincipal.state("zoomed")
        else:
            janelaPrincipal.state("normal")

    botaoVoltar = ctk.CTkButton(janelaPetianos,text="Voltar",command=voltar)
    botaoVoltar.pack(pady=10)
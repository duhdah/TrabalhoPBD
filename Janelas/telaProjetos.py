from database import conectar
import customtkinter as ctk
from tkinter import messagebox

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
        if status == "Ideias": criarCardProjeto(colunaIdeias, nome, colunaIdeias, colunaFazendo, colunaStandBy, colunaFeito, comboTipo, comboLider)
        elif status == "Fazendo": criarCardProjeto(colunaFazendo, nome, colunaIdeias, colunaFazendo, colunaStandBy, colunaFeito, comboTipo, comboLider)
        elif status == "Stand-By": criarCardProjeto(colunaStandBy, nome, colunaIdeias, colunaFazendo, colunaStandBy, colunaFeito, comboTipo, comboLider)
        else: criarCardProjeto(colunaFeito, nome, colunaIdeias, colunaFazendo, colunaStandBy, colunaFeito, comboTipo, comboLider)

def criarColuna(master, titulo, cor):
    frame = ctk.CTkFrame(master, corner_radius=20, fg_color=cor)
    texto = ctk.CTkLabel(frame, text=titulo, font=("Segoe UI", 20, "bold"))
    texto.pack(pady=10)
    return frame

def adicionarProjeto(janela, entradaNome, entradaDescricao, comboStatus, entradaCodigo, comboTipoForm, comboLiderForm, frameEspecifico, colunaIdeias, colunaFazendo, colunaStandBy, colunaFeito, comboTipoFiltro, comboLiderFiltro):    
    nome = entradaNome.get()
    descricao = entradaDescricao.get("1.0","end").strip()
    status = comboStatus.get()
    codigo = entradaCodigo.get()
    tipo = comboTipoForm.get()
    lider = comboLiderForm.get()
    valorExtra = ""
    dataEvento = None
    duracaoEvento = None
    if frameEspecifico:
        entradas = []
        for widget in frameEspecifico.winfo_children():
            if isinstance(widget, (ctk.CTkEntry,ctk.CTkComboBox)):
                valorExtra = widget.get()
            elif isinstance(widget, ctk.CTkEntry):
                valorExtra = widget.get()
            elif isinstance(widget, ctk.CTkFrame):
                for sub_widget in widget.winfo_children():
                    if isinstance(sub_widget, ctk.CTkEntry):
                        entradas.append(sub_widget.get())
        if valorExtra == "Evento" and len(entradas) >= 2:
            dataEvento = entradas[0]
            duracaoEvento = entradas[1]

    # Validar o preenchimento de todas as lacunas
    if not nome or not descricao or not status or not codigo or not tipo or not lider:
        for w in janela.winfo_children():
            if getattr(w, '_text', '') in ["Por favor, preencha todos os campos.", "O código deve ser um número inteiro.", "Já existe um projeto com este nome."]:
                w.destroy()
        lbl_erro = ctk.CTkLabel(janela, text="Por favor, preencha todos os campos.", text_color="red", font=("Segoe UI", 12, "bold"))
        lbl_erro.pack(pady=5)
        return

    if not valorExtra:
        lbl_erro = ctk.CTkLabel(janela, text="Por favor, preencha todos os campos.", text_color="red", font=("Segoe UI", 12, "bold"))
        lbl_erro.pack(pady=5)
        return

    if valorExtra == "Evento" and (not dataEvento or not duracaoEvento):
        lbl_erro = ctk.CTkLabel(janela, text="Por favor, preencha todos os campos.", text_color="red", font=("Segoe UI", 12, "bold"))
        lbl_erro.pack(pady=5)
        return  
    
    # Verificar se o código é um número inteiro (Integridade de domínio)
    try:
        codigo_inteiro = int(codigo)
        if codigo_inteiro <= 0:
            raise ValueError
    except ValueError:
        for w in janela.winfo_children():
            if getattr(w, '_text', '') in ["Por favor, preencha todos os campos.", "O código deve ser um número inteiro.", "Já existe um projeto com este nome."]:
                w.destroy()
        lbl_erro = ctk.CTkLabel(janela, text="O código deve ser um número inteiro.", text_color="red", font=("Segoe UI", 12, "bold"))
        lbl_erro.pack(pady=5)
        return

    conexao = conectar()
    cursor = conexao.cursor()
        
    cursor.execute("SELECT 1 FROM Projeto WHERE nomeProjeto = %s", (nome,))
    projeto_existe = cursor.fetchone()
        
    if projeto_existe:
        cursor.close()
        conexao.close()
            
        for w in janela.winfo_children():
            if getattr(w, '_text', '') in ["Por favor, preencha todos os campos.", "O código deve ser um número inteiro.", "Já existe um projeto com este nome."]:
                w.destroy()
                    
        lbl_erro = ctk.CTkLabel(janela, text="Já existe um projeto com este nome.", text_color="red", font=("Segoe UI", 12, "bold"))
        lbl_erro.pack(pady=5)
        return 

    cursor.execute("""
        SELECT matricula
        FROM Membro_Equipe
        WHERE nomeCompleto=%s
    """,(lider,))

    matricula = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO Projeto
        VALUES(%s,%s,%s,%s,%s)
    """,(nome,matricula,descricao,status,codigo))

    if tipo=="Ensino":
        cursor.execute("""INSERT INTO Projeto_Ensino VALUES(%s,%s)""",(nome,valorExtra))

    elif tipo=="Pesquisa":
        cursor.execute("""INSERT INTO Projeto_Pesquisa VALUES(%s,%s)""",(nome,valorExtra))

    else:
        cursor.execute("""INSERT INTO Projeto_Extensao VALUES(%s,%s)""",(nome,valorExtra))
        if valorExtra == "Evento" and dataEvento and duracaoEvento:
            cursor.execute("INSERT INTO Evento VALUES(%s,%s,%s)", (nome, dataEvento, int(duracaoEvento)))

    conexao.commit()
    cursor.close()
    conexao.close()
    carregarProjetos(colunaIdeias, colunaFazendo, colunaStandBy, colunaFeito, comboTipoFiltro, comboLiderFiltro)
    janela.destroy()

def salvarEdicaoProjeto(janela,nomeOriginal,entradaNome,entradaDescricao,comboStatus,entradaCodigo,comboTipo,comboLider, frameEspecifico,
                        colunaIdeias, colunaFazendo, colunaStandBy, colunaFeito, comboTipoFiltro, comboLiderFiltro, janelaDetalhes=None):
    nome = entradaNome.get()
    descricao = entradaDescricao.get("1.0","end").strip()   
    status = comboStatus.get()
    codigo = entradaCodigo.get()
    tipo = comboTipo.get()
    lider = comboLider.get()
    valorExtra = ""
    dataEvento = None
    duracaoEvento = None
    if frameEspecifico:
        entradas = []
        for widget in frameEspecifico.winfo_children():
            if isinstance(widget, (ctk.CTkEntry,ctk.CTkComboBox)):
                valorExtra = widget.get()
            elif isinstance(widget, ctk.CTkEntry):
                valorExtra = widget.get()
            elif isinstance(widget, ctk.CTkFrame):
                for sub_widget in widget.winfo_children():
                    if isinstance(sub_widget, ctk.CTkEntry):
                        entradas.append(sub_widget.get())
        if valorExtra == "Evento" and len(entradas) >= 2:
            dataEvento = entradas[0]
            duracaoEvento = entradas[1]
    
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT matricula
        FROM Membro_Equipe
        WHERE nomeCompleto=%s
    """,(lider,))

    matricula = cursor.fetchone()[0]

    cursor.execute("""
        UPDATE Projeto
        SET nomeProjeto=%s, matriculaLider=%s, descricao=%s, status=%s, codigoCobalto=%s
        WHERE nomeProjeto=%s
         """,(nome,matricula, descricao,status,codigo,nomeOriginal))
    
    cursor.execute("DELETE FROM Evento WHERE nomeProjeto=%s", (nomeOriginal,))
    cursor.execute("DELETE FROM Projeto_Ensino WHERE nomeProjeto=%s", (nome,))
    cursor.execute("DELETE FROM Projeto_Pesquisa WHERE nomeProjeto=%s", (nome,))
    cursor.execute("DELETE FROM Projeto_Extensao WHERE nomeProjeto=%s", (nome,))

    if tipo == "Ensino":
        cursor.execute("INSERT INTO Projeto_Ensino (nomeProjeto, topico) VALUES (%s, %s)", (nome, valorExtra))
    elif tipo == "Pesquisa":
        cursor.execute("INSERT INTO Projeto_Pesquisa (nomeProjeto, area) VALUES (%s, %s)", (nome, valorExtra))
    else:
        cursor.execute("INSERT INTO Projeto_Extensao (nomeProjeto, tipo) VALUES (%s, %s)", (nome, valorExtra))
        if valorExtra == "Evento" and dataEvento and duracaoEvento:
            cursor.execute("INSERT INTO Evento VALUES (%s, %s, %s)", (nome, dataEvento, int(duracaoEvento)))
            
    conexao.commit()
    cursor.close()
    conexao.close()

    if colunaIdeias and colunaFazendo and colunaStandBy and colunaFeito and comboTipoFiltro and comboLiderFiltro:
        carregarProjetos(colunaIdeias, colunaFazendo, colunaStandBy, colunaFeito, comboTipoFiltro, comboLiderFiltro)
        colunaIdeias.winfo_toplevel().update()

    janela.destroy()

    if janelaDetalhes and janelaDetalhes.winfo_exists():
        janelaDetalhes.destroy()
        abrirDetalhes(nome, colunaIdeias, colunaFazendo, colunaStandBy, colunaFeito, comboTipo, comboLider)

    
def abrirFormularioProjeto(janelaDetalhes, dadosProjeto=None,colunaIdeias=None,colunaFazendo=None,colunaStandBy=None,colunaFeito=None,comboTipoFiltro=None,comboLiderFiltro=None):
    janela = ctk.CTkToplevel()
    janela.title("Projeto")
    janela.geometry("550x600")
    titulo = "Novo projeto" if dadosProjeto is None else "Editar projeto"
    ctk.CTkLabel(janela,text=titulo,font=("Segoe UI",20,"bold")).pack(pady=10)
    janela.lift()
    janela.grab_set()

    ctk.CTkLabel(janela, text="Nome").pack(anchor="w", padx=30)
    entradaNome = ctk.CTkEntry(janela,width=400)
    entradaNome.pack(pady=3)

    ctk.CTkLabel(janela, text="Descrição").pack(anchor="w", padx=30)
    entradaDescricao = ctk.CTkTextbox(janela, width=400, height=60)
    entradaDescricao.pack(pady=3)

    ctk.CTkLabel(janela, text="Status").pack(anchor="w", padx=30)
    comboStatus = ctk.CTkComboBox(janela, values=["Ideias","Fazendo","Stand By","Feito"])
    comboStatus.pack(pady=3)

    ctk.CTkLabel(janela, text="Código (Cobalto)").pack(anchor="w", padx=30)
    entradaCodigo = ctk.CTkEntry(janela,width=400)
    entradaCodigo.pack(pady=3)

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT me.nomeCompleto
        FROM Petiano p
        JOIN Membro_Equipe me ON p.matricula = me.matricula
        ORDER BY me.nomeCompleto
    """)
    lideres = [x[0] for x in cursor.fetchall()]

    cursor.close()
    conexao.close()

    ctk.CTkLabel(janela, text="Líder").pack(anchor="w", padx=30)
    comboLiderForm = ctk.CTkComboBox(janela,values=lideres)
    comboLiderForm.pack(pady=3)

    ctk.CTkLabel(janela, text="Tipo").pack(anchor="w", padx=30)
    comboTipoForm = ctk.CTkComboBox(janela, values=["Ensino","Pesquisa","Extensao"])
    comboTipoForm.pack(pady=3)

    frameEspecifico = ctk.CTkFrame(janela,fg_color="transparent")
    frameEspecifico.pack(pady=3)

    def atualizarCampoTipo(tipo):
        for widget in frameEspecifico.winfo_children():
            widget.destroy()

        if tipo == "Ensino":
            ctk.CTkLabel(frameEspecifico,text="Tópico").pack()
            entradaExtra = ctk.CTkEntry(frameEspecifico,width=350)
            entradaExtra.pack(pady=3)

        elif tipo == "Pesquisa":
            ctk.CTkLabel(frameEspecifico,text="Área").pack()
            entradaExtra = ctk.CTkEntry(frameEspecifico,width=350)
            entradaExtra.pack(pady=3)

        else:
            ctk.CTkLabel(frameEspecifico,text="Tipo de extensão").pack()
            entradaExtra = ctk.CTkComboBox(frameEspecifico, values=["Curso", "Oficina", "Evento", "Outros"])
            entradaExtra.pack(pady=3)
            frameEvento = ctk.CTkFrame(frameEspecifico, fg_color="transparent")
            
            def conferirEvento(valor):
                for w in frameEvento.winfo_children():
                    w.destroy()
                if valor == "Evento":
                    ctk.CTkLabel(frameEvento, text="Data (AAAA-MM-DD)").pack(side="left", padx=5)
                    entData = ctk.CTkEntry(frameEvento, width=100, placeholder_text="2026-12-31")
                    entData.pack(side="left", padx=5)

                    ctk.CTkLabel(frameEvento, text="Duração (Horas)").pack(side="left", padx=5)
                    entDuracao = ctk.CTkEntry(frameEvento, width=60, placeholder_text="4")
                    entDuracao.pack(side="left", padx=5)
                
                    frameEvento.pack(pady=5)
                else:
                    frameEvento.pack_forget()   
            entradaExtra.configure(command=conferirEvento)
        return entradaExtra
    
    entradaExtra = None

    def mudouTipo(valor):
        nonlocal entradaExtra
        entradaExtra = atualizarCampoTipo(valor)

    comboTipoForm.configure(command=mudouTipo)

    if dadosProjeto:
        entradaNome.insert(0,dadosProjeto["nome"])
        entradaDescricao.insert("1.0",dadosProjeto["descricao"])
        comboStatus.set(dadosProjeto["status"])
        entradaCodigo.insert(0,dadosProjeto["codigo"])
        comboTipoForm.set(dadosProjeto["tipo"])
        comboLiderForm.set(dadosProjeto["lider"]) 
        entradaExtra = atualizarCampoTipo(dadosProjeto["tipo"])
        if isinstance(entradaExtra, ctk.CTkEntry):
            entradaExtra.insert(0, dadosProjeto["extra"])
        elif isinstance(entradaExtra, ctk.CTkComboBox):
            entradaExtra.set(dadosProjeto["extra"])
            if comboTipoForm.get() == "Extensao":
                try:
                    entradaExtra.cget("command")(dadosProjeto["extra"])
                except Exception:
                    pass

    if dadosProjeto is None:    
        comboTipoForm.set("Ensino")
        comboStatus.set("Ideias")
        entradaExtra = atualizarCampoTipo("Ensino")
        botao = ctk.CTkButton(janela,text="Salvar",
            command=lambda: adicionarProjeto(janela, entradaNome, entradaDescricao, comboStatus, entradaCodigo, comboTipoForm, comboLiderForm, frameEspecifico,
                colunaIdeias, colunaFazendo, colunaStandBy, colunaFeito, comboTipoFiltro, comboLiderFiltro))
    else:
        botao = ctk.CTkButton(  
            janela,text="Salvar alterações",
            command=lambda: salvarEdicaoProjeto(janela,dadosProjeto["nome"],entradaNome,entradaDescricao, 
                comboStatus,entradaCodigo,comboTipoForm,comboLiderForm, frameEspecifico, colunaIdeias, 
                colunaFazendo, colunaStandBy, colunaFeito, comboTipoFiltro, comboLiderFiltro, janelaDetalhes))
    botao.pack(pady=5)

def excluirProjeto(nomeProjeto, janelaDetalhes, colunaIdeias, colunaFazendo, colunaStandBy, colunaFeito, comboTipo, comboLider):
    resposta = messagebox.askyesno("Excluir projeto",f"Deseja realmente excluir o projeto?")
    if not resposta:
        return

    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("""
            DELETE FROM Projeto_Petiano
            WHERE nomeProjeto = %s
        """, (nomeProjeto,))

        cursor.execute("""
            DELETE FROM Reuniao_Projeto
            WHERE nomeProjeto = %s
        """, (nomeProjeto,))

        cursor.execute("""
            DELETE FROM Projeto_Aluno
            WHERE nomeProjeto = %s
        """, (nomeProjeto,))

        cursor.execute("""
            DELETE FROM Projeto_Artigo
            WHERE nomeProjeto = %s
        """, (nomeProjeto,))

        cursor.execute("""
            DELETE FROM Evento
            WHERE nomeProjeto = %s
        """, (nomeProjeto,))

        cursor.execute("""
            DELETE FROM MembroExterno_ProjetoExtensao
            WHERE nomeProjeto = %s
        """, (nomeProjeto,))

        cursor.execute("""
            DELETE FROM Projeto_Ensino
            WHERE nomeProjeto = %s
        """, (nomeProjeto,))

        cursor.execute("""
            DELETE FROM Projeto_Pesquisa
            WHERE nomeProjeto = %s
        """, (nomeProjeto,))

        cursor.execute("""
            DELETE FROM Projeto_Extensao
            WHERE nomeProjeto = %s
        """, (nomeProjeto,))

        cursor.execute("""
            DELETE FROM Projeto
            WHERE nomeProjeto = %s
        """, (nomeProjeto,))

        conexao.commit()
        messagebox.showinfo("Sucesso","Projeto excluído com sucesso.")  
        janelaDetalhes.destroy()

    except Exception as erro:
        conexao.rollback()
        messagebox.showerror("Erro",str(erro))

    finally:
        cursor.close()
        conexao.close()

    carregarProjetos(colunaIdeias,colunaFazendo,colunaStandBy,colunaFeito,comboTipo,comboLider)

def editarProjeto(nomeProjeto, janelaDetalhes):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT
            p.nomeProjeto,
            p.descricao,
            p.status,
            p.codigoCobalto,
            me.nomeCompleto,
            CASE
                WHEN pe.nomeProjeto IS NOT NULL THEN 'Ensino'
                WHEN pp.nomeProjeto IS NOT NULL THEN 'Pesquisa'
                WHEN px.nomeProjeto IS NOT NULL THEN 'Extensao'
            END,
            COALESCE(pe.topico, pp.area, px.tipo)
        FROM Projeto p
        JOIN Membro_Equipe me
            ON p.matriculaLider = me.matricula
        LEFT JOIN Projeto_Ensino pe
            ON p.nomeProjeto = pe.nomeProjeto
        LEFT JOIN Projeto_Pesquisa pp
            ON p.nomeProjeto = pp.nomeProjeto
        LEFT JOIN Projeto_Extensao px
            ON p.nomeProjeto = px.nomeProjeto
        WHERE p.nomeProjeto = %s
    """, (nomeProjeto,))

    projeto = cursor.fetchone()

    cursor.close()
    conexao.close()

    if not projeto:
        messagebox.showerror("Erro", "Projeto não encontrado.")
        return
    
    tipo = projeto[5] if projeto[5] is not None else "Ensino"
    extra = projeto[6] if projeto[6] is not None else ""

    dadosProjeto = {
        "nome": projeto[0],
        "descricao": projeto[1] if projeto[1] else "",
        "status": projeto[2],
        "codigo": projeto[3] if projeto[3] else "",
        "lider": projeto[4],
        "tipo": tipo,
        "extra": extra
    }

    abrirFormularioProjeto(janelaDetalhes, dadosProjeto,colunaIdeias=None,colunaFazendo=None,colunaStandBy=None,colunaFeito=None,comboTipoFiltro=None,comboLiderFiltro=None)

def abrirDetalhes(nomeProjeto, colunaIdeias, colunaFazendo, colunaStandBy, colunaFeito, comboTipo, comboLider):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT p.nomeProjeto, p.descricao, p.status, p.codigoCobalto, me.nomeCompleto,
        CASE
            WHEN pe.nomeProjeto IS NOT NULL THEN 'Ensino'
            WHEN pp.nomeProjeto IS NOT NULL THEN 'Pesquisa'
            WHEN px.nomeProjeto IS NOT NULL THEN 'Extensão'
        END AS tipo, 
        COALESCE(pe.topico, pp.area, px.tipo, 'Não informado') AS extra, ev.dataEvento, ev.duracao 
    FROM Projeto p
    JOIN Membro_Equipe me ON p.matriculaLider = me.matricula
    LEFT JOIN Projeto_Ensino pe ON p.nomeProjeto = pe.nomeProjeto
    LEFT JOIN Projeto_Pesquisa pp ON p.nomeProjeto = pp.nomeProjeto
    LEFT JOIN Projeto_Extensao px ON p.nomeProjeto = px.nomeProjeto
    LEFT JOIN Evento ev ON p.nomeProjeto = ev.nomeProjeto
    WHERE p.nomeProjeto = %s""",(nomeProjeto,))

    projeto = cursor.fetchone()
    cursor.close()
    conexao.close()

    if not projeto:
        messagebox.showerror("Erro", "Projeto não encontrado.")
        return
    
    janelaDetalhes = ctk.CTkToplevel()
    janelaDetalhes.title("Projeto")
    janelaDetalhes.geometry("500x400")
    janelaDetalhes.lift()
    janelaDetalhes.grab_set()
    texto = f"""
        Nome: {projeto[0]}
        Líder: {projeto[4]}  
        Tipo: {projeto[5]} 
        Status: {projeto[2]} 
        Código Cobalto: {projeto[3]}
        Descrição: {projeto[1]}"""
    if projeto[5] == 'Ensino':
        texto += f"""
        Tópico: {projeto[6]}
    """
    elif projeto[5] == 'Pesquisa':
        texto += f"""
        Área: {projeto[6]}
    """
    else:  
        texto += f"""
        Tipo de extensão: {projeto[6]}
    """
        if projeto[6] == 'Evento' and projeto[7]:
            texto += f"""        
        Data do Evento: {projeto[7]}
        Duração: {projeto[8]} horas
        """
    label = ctk.CTkLabel(janelaDetalhes,text=texto,justify="left",anchor="w",font=("Segoe UI",16))
    label.pack(fill="x",padx=20,pady=10)

    ctk.CTkButton(
        janelaDetalhes,
        text="Editar projeto",
        width=220,
        command=lambda: editarProjeto(projeto[0], janelaDetalhes)
    ).pack(pady=10)

    ctk.CTkButton(
        janelaDetalhes,
        text="Excluir projeto",
        width=220,
        fg_color="#d9534f",
        hover_color="#c9302c",
        command=lambda: excluirProjeto(projeto[0], janelaDetalhes, colunaIdeias, colunaFazendo, colunaStandBy, colunaFeito, comboTipo, comboLider)
    ).pack(pady=10)

def criarCardProjeto(coluna, nomeProjeto, colunaIdeias, colunaFazendo, colunaStandBy, colunaFeito, comboTipo, comboLider):
    card = ctk.CTkButton(
        coluna,
        text=nomeProjeto,
        height=50,
        corner_radius=15,
        command=lambda: abrirDetalhes(nomeProjeto, colunaIdeias, colunaFazendo, colunaStandBy, colunaFeito, comboTipo, comboLider)
    )
    card.pack(fill="x", padx=10, pady=5)

def abrirTelaProjetos(janelaPrincipal, janelaDetalhes=None):
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
    colunaStandBy = criarColuna(areaKanban, "Stand-By", "#aac1ec")
    colunaFeito = criarColuna(areaKanban, "Feito", "#aac1ec")

    colunaIdeias.grid(row=0, column=0, sticky="nsew", padx=10)
    colunaFazendo.grid(row=0, column=1, sticky="nsew", padx=10)
    colunaStandBy.grid(row=0, column=2, sticky="nsew", padx=10)
    colunaFeito.grid(row=0, column=3, sticky="nsew", padx=10)
    
    botaoFiltrar.configure(command=lambda:carregarProjetos(colunaIdeias,colunaFazendo,colunaStandBy,colunaFeito,comboTipo,comboLider))
    carregarProjetos(colunaIdeias,colunaFazendo,colunaStandBy,colunaFeito,comboTipo,comboLider)

    botaoAdicionar = ctk.CTkButton(janelaProjetos,text="+ Adicionar projeto",width=250,height=50,
        command=lambda: abrirFormularioProjeto(janelaDetalhes, None, colunaIdeias,colunaFazendo,colunaStandBy,colunaFeito,comboTipo,comboLider))
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

def abrirTelaAdicionarProjeto(colunaIdeias,colunaFazendo,colunaStandBy,colunaFeito,comboTipoFiltro,comboLiderFiltro):
    janelaAdProj = ctk.CTkToplevel()
    janelaAdProj.title("Adicionar projeto")
    janelaAdProj.geometry("450x800")        
    ctk.CTkLabel(janelaAdProj,text="Novo projeto",font=("Segoe UI", 28, "bold")).pack(pady=20)
    janelaAdProj.lift()
    janelaAdProj.grab_set()

    ctk.CTkLabel(janelaAdProj, text="Nome do projeto").pack(anchor="w", padx=30)
    entryNome = ctk.CTkEntry(janelaAdProj, width=420)
    entryNome.pack(pady=5)

    ctk.CTkLabel(janelaAdProj,text="Descrição").pack(anchor="w", padx=30)
    entryDescricao = ctk.CTkTextbox(janelaAdProj,width=420,height=120)
    entryDescricao.pack()
    
    ctk.CTkLabel(janelaAdProj, text="Código Cobalto").pack(anchor="w", padx=30)
    entryCodigo = ctk.CTkEntry(janelaAdProj, width=420)
    entryCodigo.pack(pady=5)

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT p.matricula, me.nomeCompleto
        FROM Petiano p
        JOIN Membro_Equipe me ON p.matricula = me.matricula
        ORDER BY me.nomeCompleto
    """)

    lideres = {}
    for matricula, nome in cursor.fetchall():
        lideres[nome] = matricula

    cursor.close()
    conexao.close()

    ctk.CTkLabel(janelaAdProj, text="Líder").pack(anchor="w", padx=30)
    comboLider = ctk.CTkComboBox(janelaAdProj,values=list(lideres.keys()),width=420)
    comboLider.pack(pady=5)
    
    ctk.CTkLabel(janelaAdProj, text="Tipo").pack(anchor="w", padx=30)
    comboTipo = ctk.CTkComboBox(janelaAdProj,values=["Ensino","Pesquisa","Extensao"],width=420)
    comboTipo.pack(pady=5)
    
    ctk.CTkLabel(janelaAdProj, text="Status").pack(anchor="w", padx=30)
    comboStatus = ctk.CTkComboBox(janelaAdProj,values=["Ideias","Fazendo","Stand By","Feito"],width=420)
    comboStatus.set("Ideias")
    comboStatus.pack(pady=5)

    def salvarProjeto():
        nome = entryNome.get()
        descricao = entryDescricao.get("1.0","end").strip()
        codigo = entryCodigo.get()
        lider = lideres[comboLider.get()]
        tipo = comboTipo.get()
        status = comboStatus.get()

        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO Projeto(nomeProjeto,matriculaLider,descricao,status,codigoCobalto)
            VALUES (%s,%s,%s,%s,%s) """,(nome,lider,descricao,status,codigo)
        )
        if tipo == "Ensino":
            cursor.execute("""INSERT INTO Projeto_Ensino VALUES (%s,%s)""", (nome,""))
        elif tipo == "Pesquisa":
            cursor.execute("""INSERT INTO Projeto_Pesquisa VALUES (%s,%s)""",(nome,""))
        else:
            cursor.execute("""INSERT INTO Projeto_Extensao VALUES (%s,%s)""",(nome,""))
        conexao.commit()
        cursor.close()
        conexao.close()

        carregarProjetos(colunaIdeias,colunaFazendo,colunaStandBy,colunaFeito,comboTipoFiltro,comboLiderFiltro)
        janelaAdProj.destroy()

    ctk.CTkButton(janelaAdProj, text="Salvar Projeto", command=salvarProjeto, width=220, height=45).pack(pady=25)
        
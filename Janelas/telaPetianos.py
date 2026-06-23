from database import conectar
import customtkinter as ctk
from telaProjetos import abrirTelaProjetos
from PIL import Image

def criarPetiano(master, nome, imagem_path):
    icon2 = ctk.CTkImage(
        light_image=Image.open(imagem_path),
        dark_image=Image.open(imagem_path),
        size=(60, 60)
    )

    botao = ctk.CTkButton(
        master,
        text=nome,
        image=icon2,
        compound="left",
        height=80,
        corner_radius=15,
        fg_color="#e8eafc",
        text_color="#1d2b7d",
        hover_color="#d8ddfc",
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
    tutor = criarPetiano(linha_topo, "Tutor", "icon2.png")
    tutor.pack(side="right", padx=10)

    p2 = criarPetiano(area, "P1", "icon2.png")
    p3 = criarPetiano(area, "P2", "icon2.png")
    p4 = criarPetiano(area, "P3", "icon2.png")
    p5 = criarPetiano(area, "P4", "icon2.png")

    p2.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    p3.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
    p4.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)
    p5.grid(row=1, column=3, sticky="nsew", padx=10, pady=10)

    p6 = criarPetiano(area, "P5", "icon2.png")
    p7 = criarPetiano(area, "P6", "icon2.png")
    p8 = criarPetiano(area, "P7", "icon2.png")
    p9 = criarPetiano(area, "P8", "icon2.png")

    p6.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
    p7.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
    p8.grid(row=2, column=2, sticky="nsew", padx=10, pady=10)
    p9.grid(row=2, column=3, sticky="nsew", padx=10, pady=10)   

    p10 = criarPetiano(area, "P9", "icon2.png")
    p11 = criarPetiano(area, "P10", "icon2.png")
    p12 = criarPetiano(area, "P11", "icon2.png")
    p13 = criarPetiano(area, "P12", "icon2.png")

    p10.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
    p11.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)
    p12.grid(row=3, column=2, sticky="nsew", padx=10, pady=10)
    p13.grid(row=3, column=3, sticky="nsew", padx=10, pady=10)

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
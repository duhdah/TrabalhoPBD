from database import conectar
import customtkinter as ctk
from telaProjetos import abrirTelaProjetos
from telaPetianos import abrirTelaPetianos
from telaArtigos import abrirTelaArtigos
from telaEventos import abrirTelaEventos
from telaReunioes import abrirTelaReunioes

from PIL import Image

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

janelaPrincipal = ctk.CTk()
janelaPrincipal.title("PET - Sistema")
janelaPrincipal.geometry("1000x600")
janelaPrincipal.configure(fg_color="#ffffff")

topo = ctk.CTkFrame(
    janelaPrincipal,
    corner_radius=25,
    height=150,
    fg_color="#c4cafb"
)
topo.pack(fill="x", padx=30, pady=30)
topo.pack_propagate(False)

imagem = ctk.CTkImage(
    light_image=Image.open("icon.png"),
    dark_image=Image.open("icon.png"),
    size=(120, 120)
)

foto = ctk.CTkLabel(topo,text="",image=imagem)
foto.pack(side="left", padx=40, pady=15)
foto.pack_propagate(False)

textoTopo = ctk.CTkLabel(
    topo,
    text="Bem-vindo(a), petiano(a)!",
    font=("Segoe UI", 28),
    text_color="#1d2b7d"
)
textoTopo.pack(side="left", padx=20)

centro = ctk.CTkFrame(janelaPrincipal, fg_color="transparent")
centro.pack(expand=True, fill="both", padx=40, pady=20)
centro.grid_rowconfigure(0, weight=1)
centro.grid_rowconfigure(1, weight=1)
centro.grid_columnconfigure((0, 1, 2), weight=1)

estiloBotao = {
    "corner_radius": 25,
    "font": ("Segoe UI", 22),
    "fg_color": "#e8eafc",
    "hover_color": "#d8ddfc",
    "text_color": "#1d2b7d",
    "height": 100
}

linha1 = ctk.CTkFrame(centro, fg_color="transparent" )
linha1.pack()

botaoProjetos = ctk.CTkButton(linha1, text="Projetos", width=300, command=lambda:  abrirTelaProjetos(janelaPrincipal),**estiloBotao)
botaoPetianos = ctk.CTkButton(linha1, text="Petianos", width=300,  command=lambda:  abrirTelaPetianos(janelaPrincipal), **estiloBotao )
botaoReunioes = ctk.CTkButton(linha1, text="Reuniões", width=300, command=lambda:  abrirTelaReunioes(janelaPrincipal), **estiloBotao)
botaoProjetos.pack(side="left", padx=20, pady=10, fill="both", expand=True)
botaoPetianos.pack(side="left", padx=20, pady=10, fill="both", expand=True)
botaoReunioes.pack(side="left", padx=20, pady=10, fill="both", expand=True)

linha2 = ctk.CTkFrame(centro, fg_color="transparent")
linha2.pack()

botaoEventos = ctk.CTkButton(linha2, text="Eventos", width=300, command=lambda:  abrirTelaEventos(janelaPrincipal), **estiloBotao)
botaoArtigos = ctk.CTkButton(linha2, text="Artigos", width=300,  command=lambda:  abrirTelaArtigos(janelaPrincipal), **estiloBotao)
botaoEventos.pack(side="left", padx=20, pady=10, fill="both", expand=True)
botaoArtigos.pack(side="left", padx=20, pady=10, fill="both", expand=True)

footer = ctk.CTkFrame(janelaPrincipal, fg_color="transparent")
footer.pack(side="bottom", fill="x", pady=10)

texto_footer = ctk.CTkLabel(
    footer,
    text="Projeto desenvolvido por Eduarda Medeiros, Jenifer Arena e Laura Garcia",
    font=("Segoe UI", 18),
    text_color="#1d2b7d"
)
texto_footer.pack()

janelaPrincipal.protocol("WM_DELETE_WINDOW", janelaPrincipal.destroy)
janelaPrincipal.mainloop()
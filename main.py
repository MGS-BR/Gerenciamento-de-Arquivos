import sys
import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, msg):
        self.widget.insert(END, msg)
        self.widget.see(END)

    def flush(self):
        pass

class Application:

    def centralizar_janela(self, janela):
        janela.update_idletasks()

        largura = janela.winfo_width()
        altura = janela.winfo_height()

        largura_tela = janela.winfo_screenwidth()
        altura_tela = janela.winfo_screenheight()

        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2)

        janela.geometry(f"+{x}+{y}")

    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "10")
        self.fontePadraoBold = ("Arial", "10", "bold")
        
        configBtn = Button(master, text="Configurações", command=self.config)
        configBtn.pack(pady=10)

        console = scrolledtext.ScrolledText(root, state='normal', height=15, width=50, bg='black', fg='white')
        console.pack(pady=10)
        sys.stdout = TextRedirector(console)

        self.localizacao_codigo_selecionado = self.localizao_codigo["Fim"]

        self.centralizar_janela(root)

    arquivo_selecionado = {
        "PDF": ".pdf",
        "XML": ".xml",
        "Pasta": ""
    }

    localizao_codigo = {
        "Início": "[:-3]",
        "Fim": "[:-4][-3:]"
    }

    def config(self):

        janelaConfig = Toplevel()
        janelaConfig.title("Configurações")
        janelaConfig.minsize(350,200)

        janelaConfig.grid_columnconfigure(0, weight=1)
        janelaConfig.grid_columnconfigure(1, weight=1)

        titulo = Label(janelaConfig, text="Configurações:", font=self.fontePadraoBold)
        titulo.grid(row=0, column=0, columnspan=2, pady=20)

        localCodigoLabel = Label(janelaConfig, text="Localização do código:", font=self.fontePadrao)
        localCodigoLabel.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        localCodigoCombo = ttk.Combobox(
            janelaConfig,
            values=list(self.localizao_codigo.keys()),
            state="readonly"
        )
        localCodigoCombo.current(1)
        localCodigoCombo.grid(row=1, column=1, padx=10, pady=10)

        frameBotoes = Frame(janelaConfig)
        frameBotoes.grid(row=2, column=0, columnspan=2, pady=20)

        sairBtn = Button(frameBotoes, text="Sair", command=janelaConfig.destroy, width=12)
        sairBtn.pack(side=LEFT, padx=10)

        def confirmar():
            self.localizacao_codigo_selecionado = self.localizao_codigo[localCodigoCombo.get()]
            messagebox.showinfo("Configurações", "Configurações salvas com sucesso!")
            janelaConfig.destroy()

        confirmarBtn = Button(frameBotoes, text="Confirmar", command=confirmar, width=12)
        confirmarBtn.pack(side=LEFT, padx=10)

        self.centralizar_janela(janelaConfig)

root = Tk()
root.title("Conntador")
Application(root)
root.mainloop()
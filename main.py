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

        master.minsize(500,400)

        main = Frame(master)
        main.pack(padx=20, pady=20)

        header = Frame(main)
        header.pack(pady=(0,20))
        
        titulo = Label(header, text="Gerenciador de Arquivos", font=self.fontePadraoBold)
        titulo.pack(side=LEFT)

        configBtn = Button(header, text="⚙", command=self.config)
        configBtn.pack(side=LEFT, padx=10)

        forms = Frame(main)
        forms.pack()

        tipoArquivoLabel = Label(forms, text="Tipo de arquivo:", font=self.fontePadrao, width=15, anchor="e")
        tipoArquivoLabel.grid(row=0, column=0, padx=10, pady=5)
        tipoArquivoCombo = ttk.Combobox(
            forms,
            values=list(self.arquivo_selecionado.keys()),
            state="readonly",
            width=25,
            )
        tipoArquivoCombo.current(0)
        tipoArquivoCombo.grid(row=0, column=1, pady=5)

        pastaOrigemLabel = Label(forms, text="Pasta de origem:", font=self.fontePadrao, width=15, anchor="e")
        pastaOrigemLabel.grid(row=1, column=0, padx=10, pady=5)

        pastaOrigemEntry = Entry(forms, width=35)
        pastaOrigemEntry.grid(row=1, column=1, pady=5)

        pastaOrigemBtn = Button(
        forms,
        text="📁",
        command=lambda: pastaOrigemEntry.insert(0, filedialog.askdirectory())
        )
        pastaOrigemBtn.grid(row=1, column=2, padx=5)

        pastaDestinoLabel = Label(forms, text="Pasta de destino:", font=self.fontePadrao, width=15, anchor="e")
        pastaDestinoLabel.grid(row=2, column=0, padx=10, pady=5)

        pastaDestinoEntry = Entry(forms, width=35)
        pastaDestinoEntry.grid(row=2, column=1, pady=5)

        pastaDestinoBtn = Button(
        forms,
        text="📁",
        command=lambda: pastaDestinoEntry.insert(0, filedialog.askdirectory())
        )
        pastaDestinoBtn.grid(row=2, column=2, padx=5)

        pastaCaminhoLabel = Label(forms, text="Caminho do arquivo:", font=self.fontePadrao, width=15, anchor="e")
        pastaCaminhoLabel.grid(row=3, column=0, padx=10, pady=5)

        pastaCaminhoEntry = Entry(forms, width=35)
        pastaCaminhoEntry.grid(row=3, column=1, pady=5)

        pastaCaminhoBtn = Button(
        forms,
        text="❓",
        command=lambda: messagebox.showinfo("Caminho do Arquivo", "Caminho a se percorrer após a pasta de destino para salvar os arquivos desejados.\nExemplo: 'Fiscal/2026/202601/Servicos Prestados'\n\nNão é obrigatório o preenchimento deste campo!")
        )
        pastaCaminhoBtn.grid(row=3, column=2, padx=5)

        renomearLabel = Label(forms, text="Renomear arquivos:", font=self.fontePadrao, width=15, anchor="e")
        renomearLabel.grid(row=4, column=0, padx=10, pady=5)

        renomearEntry = Entry(forms, width=35)
        renomearEntry.grid(row=4, column=1, pady=5)

        renomearBtn = Button(
        forms,
        text="❓",
        command=lambda: messagebox.showinfo("Renomear Arquivos", "Após mover os arquivos para a pasta de destino os arquivos serão renomeados para o texto informado neste campo.\n\nNão é obrigatório o preenchimento deste campo!")
        )
        renomearBtn.grid(row=4, column=2, padx=5)

        console = scrolledtext.ScrolledText(main, state='normal', height=15, width=50, bg='black', fg='white')
        console.pack(pady=20)

        sys.stdout = TextRedirector(console)

        self.localizacao_codigo_selecionado = 0

        self.centralizar_janela(master)

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
        localCodigoCombo.current(self.localizacao_codigo_selecionado)
        localCodigoCombo.grid(row=1, column=1, padx=10, pady=10)

        frameBotoes = Frame(janelaConfig)
        frameBotoes.grid(row=2, column=0, columnspan=2, pady=20)

        sairBtn = Button(frameBotoes, text="Sair", command=janelaConfig.destroy, width=12)
        sairBtn.pack(side=LEFT, padx=10)

        def confirmar():
            self.localizacao_codigo_selecionado = list(self.localizao_codigo.keys()).index(localCodigoCombo.get())
            messagebox.showinfo("Configurações", "Configurações salvas com sucesso!")
            janelaConfig.destroy()

        confirmarBtn = Button(frameBotoes, text="Confirmar", command=confirmar, width=12)
        confirmarBtn.pack(side=LEFT, padx=10)

        self.centralizar_janela(janelaConfig)

root = Tk()
root.title("Conntador")
Application(root)
root.mainloop()
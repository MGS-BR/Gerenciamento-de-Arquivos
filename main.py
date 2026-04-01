import sys
import shutil
import threading
from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from pathlib import Path


class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, msg):
        self.widget.insert(END, msg)
        self.widget.see(END)

    def flush(self):
        pass


class Application:

    arquivo_selecionado = {"PDF": ".pdf", "XML": ".xml", "Pasta": "", "Tudo": ""}

    localizacao_codigo = ["Início", "Fim"]

    tamanho_codigo = 3

    def centralizar_janela(self, janela):
        janela.update_idletasks()

        largura = janela.winfo_width()
        altura = janela.winfo_height()

        largura_tela = janela.winfo_screenwidth()
        altura_tela = janela.winfo_screenheight()

        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2)

        janela.geometry(f"+{x}+{y}")

    def selecionar_pasta(self, entry):

        pasta = filedialog.askdirectory()

        if pasta:
            entry.delete(0, END)
            entry.insert(0, pasta)

    def executar_thread(self, comando):
        threading.Thread(target=comando, daemon=True).start()

    def __init__(self, master=None):

        self.master = master
        self.executando = False

        self.fontePadrao = ("Arial", "10")
        self.fontePadraoBold = ("Arial", "10", "bold")

        master.minsize(500, 400)

        main = Frame(master)
        main.pack(padx=20, pady=20)

        header = Frame(main)
        header.pack(pady=(0, 20))

        titulo = Label(
            header, text="Gerenciador de Arquivos", font=self.fontePadraoBold
        )
        titulo.pack(side=LEFT)

        configBtn = Button(header, text="⚙", command=self.config)
        configBtn.pack(side=LEFT, padx=10)

        forms = Frame(main)
        forms.pack()

        tipoArquivoLabel = Label(
            forms, text="Tipo de arquivo:", font=self.fontePadrao, width=15, anchor="e"
        )
        tipoArquivoLabel.grid(row=0, column=0, padx=10, pady=5)
        self.tipoArquivoCombo = ttk.Combobox(
            forms,
            values=list(self.arquivo_selecionado.keys()),
            state="readonly",
            width=25,
        )
        self.tipoArquivoCombo.current(0)
        self.tipoArquivoCombo.grid(row=0, column=1, pady=5)

        pastaOrigemLabel = Label(
            forms, text="Pasta de origem:", font=self.fontePadrao, width=15, anchor="e"
        )
        pastaOrigemLabel.grid(row=1, column=0, padx=10, pady=5)

        self.pastaOrigemEntry = Entry(forms, width=35)
        self.pastaOrigemEntry.grid(row=1, column=1, pady=5)

        pastaOrigemBtn = Button(
            forms,
            text="📁",
            command=lambda: self.selecionar_pasta(self.pastaOrigemEntry),
        )
        pastaOrigemBtn.grid(row=1, column=2, padx=5)

        pastaDestinoLabel = Label(
            forms, text="Pasta de destino:", font=self.fontePadrao, width=15, anchor="e"
        )
        pastaDestinoLabel.grid(row=2, column=0, padx=10, pady=5)

        self.pastaDestinoEntry = Entry(forms, width=35)
        self.pastaDestinoEntry.grid(row=2, column=1, pady=5)

        pastaDestinoBtn = Button(
            forms,
            text="📁",
            command=lambda: self.selecionar_pasta(self.pastaDestinoEntry),
        )
        pastaDestinoBtn.grid(row=2, column=2, padx=5)

        pastaCaminhoLabel = Label(
            forms,
            text="Caminho do arquivo:",
            font=self.fontePadrao,
            width=15,
            anchor="e",
        )
        pastaCaminhoLabel.grid(row=3, column=0, padx=10, pady=5)

        self.pastaCaminhoEntry = Entry(forms, width=35)
        self.pastaCaminhoEntry.grid(row=3, column=1, pady=5)

        pastaCaminhoBtn = Button(
            forms,
            text="❓",
            command=lambda: messagebox.showinfo(
                "Caminho do Arquivo",
                "Caminho a se percorrer após a pasta de destino para salvar os arquivos desejados.\nExemplo: 'Fiscal/2026/202601/Servicos Prestados'\n\nNão é obrigatório o preenchimento deste campo!",
            ),
        )
        pastaCaminhoBtn.grid(row=3, column=2, padx=5)

        renomearLabel = Label(
            forms,
            text="Renomear arquivos:",
            font=self.fontePadrao,
            width=15,
            anchor="e",
        )
        renomearLabel.grid(row=4, column=0, padx=10, pady=5)

        self.renomearEntry = Entry(forms, width=35)
        self.renomearEntry.grid(row=4, column=1, pady=5)

        renomearBtn = Button(
            forms,
            text="❓",
            command=lambda: messagebox.showinfo(
                "Renomear Arquivos",
                "Após mover os arquivos para a pasta de destino os arquivos serão renomeados para o texto informado neste campo.\n\nNão é obrigatório o preenchimento deste campo!",
            ),
        )
        renomearBtn.grid(row=4, column=2, padx=5)

        self.executarBtn = Button(
            main,
            text="Executar",
            command=lambda: self.executar_thread(self.executar),
            width=20,
        )
        self.executarBtn.pack()

        self.progressLabel = Label(main, text="", font=self.fontePadrao)
        self.progressLabel.pack()

        self.progressBar = ttk.Progressbar(
            main, orient="horizontal", length=400, mode="determinate"
        )
        self.progressBar.pack()

        console = scrolledtext.ScrolledText(
            main, state="normal", height=15, width=50, bg="black", fg="white"
        )
        console.pack(pady=20)

        sys.stdout = TextRedirector(console)

        self.localizacao_codigo_selecionado = 1

        self.centralizar_janela(master)

    def config(self):

        janelaConfig = Toplevel()
        janelaConfig.title("Configurações")
        janelaConfig.minsize(350, 200)

        janelaConfig.grid_columnconfigure(0, weight=1)
        janelaConfig.grid_columnconfigure(1, weight=1)

        titulo = Label(janelaConfig, text="Configurações:", font=self.fontePadraoBold)
        titulo.grid(row=0, column=0, columnspan=2, pady=20)

        localCodigoLabel = Label(
            janelaConfig, text="Localização do código:", font=self.fontePadrao
        )
        localCodigoLabel.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        def mudar_exemplo(combo, label):

            selecionado = combo.get()

            textos = {
                "Início": "CODIGO arquivo de exemplo.pdf",
                "Fim": "arquivo de exemplo CODIGO.pdf",
            }

            label.config(text=f"Exemplo: '{textos[selecionado]}'")

        def exemplo_inicial(combo):

            selecionado = combo.get()

            if selecionado == "Início":
                return "Exemplo: CODIGO arquivo de exemplo.pdf"
            else:
                return "Exemplo: arquivo de exemplo CODIGO.pdf"

        localCodigoCombo = ttk.Combobox(
            janelaConfig, values=self.localizacao_codigo, state="readonly"
        )
        localCodigoCombo.current(self.localizacao_codigo_selecionado)
        localCodigoCombo.grid(row=1, column=1, padx=10, pady=10)

        exemploLabel = Label(
            janelaConfig,
            text=exemplo_inicial(localCodigoCombo),
            font=self.fontePadrao,
            fg="gray",
        )
        exemploLabel.grid(row=2, column=0, columnspan=2, pady=(0, 10))

        localCodigoCombo.bind(
            "<<ComboboxSelected>>",
            lambda e: mudar_exemplo(localCodigoCombo, exemploLabel),
        )

        caracteresCodigoTitulo = Label(
            janelaConfig,
            text="Quantidade de caracteres do código:",
            font=self.fontePadrao,
        )
        caracteresCodigoTitulo.grid(row=3, column=0, columnspan=2, pady=(10, 0))

        frameControle = Frame(janelaConfig)
        frameControle.grid(row=4, column=0, columnspan=2, pady=10)

        def atualizar_tamanho_codigo(label, operacao):

            numero_atualizado = int(quantidadeCodigoLabel.cget("text")) + (
                1 if operacao else -1
            )

            if numero_atualizado >= 1:
                label.config(text=numero_atualizado)

        diminuitBtn = Button(
            frameControle,
            text="➖",
            command=lambda: atualizar_tamanho_codigo(quantidadeCodigoLabel, False),
        )
        diminuitBtn.pack(side=LEFT)

        quantidadeCodigoLabel = Label(
            frameControle, text=self.tamanho_codigo, font=self.fontePadraoBold
        )
        quantidadeCodigoLabel.pack(side=LEFT)

        aumentarBtn = Button(
            frameControle,
            text="➕",
            command=lambda: atualizar_tamanho_codigo(quantidadeCodigoLabel, True),
        )
        aumentarBtn.pack(side=LEFT)

        frameBotoes = Frame(janelaConfig)
        frameBotoes.grid(row=5, column=0, columnspan=2, pady=20)

        sairBtn = Button(
            frameBotoes, text="Sair", command=janelaConfig.destroy, width=12
        )
        sairBtn.pack(side=LEFT, padx=10)

        def confirmar():
            self.localizacao_codigo_selecionado = self.localizacao_codigo.index(
                localCodigoCombo.get()
            )
            self.tamanho_codigo = int(quantidadeCodigoLabel.cget("text"))
            messagebox.showinfo("Configurações", "Configurações salvas com sucesso!")
            janelaConfig.destroy()

        confirmarBtn = Button(
            frameBotoes, text="Confirmar", command=confirmar, width=12
        )
        confirmarBtn.pack(side=LEFT, padx=10)

        self.centralizar_janela(janelaConfig)

    def validar_entradas(self):

        pastaOrigem = self.pastaOrigemEntry.get()
        pastaDestino = self.pastaDestinoEntry.get()

        if not pastaOrigem:
            messagebox.showerror(
                "Erro", "Por favor, preencha o campo de pasta de origem!"
            )
            return False
        if not pastaDestino:
            messagebox.showerror(
                "Erro", "Por favor, preencha o campo de pasta de destino!"
            )
            return False
        if not Path(pastaOrigem).exists():
            messagebox.showerror("Erro", "A pasta de origem não existe!")
            return False
        if not Path(pastaDestino).exists():
            messagebox.showerror("Erro", "A pasta de destino não existe!")
            return False
        if not Path(pastaOrigem).is_dir():
            messagebox.showerror("Erro", "A pasta de origem deve ser uma pasta!")
            return False
        if not Path(pastaDestino).is_dir():
            messagebox.showerror("Erro", "A pasta de destino deve ser uma pasta!")
            return False
        return True

    def atualizarProgresso(self, valor):

        if not self.executando:
            return

        self.progressBar["value"] = valor
        self.progressLabel.config(
            text=f"{int(self.progressBar['value'])} / {int(self.progressBar['maximum'])} arquivos"
        )

    def finalizar(self, movidos, erros, naoEncontrados):

        self.executando = False

        print(
            f"\nProcesso concluído!\n{movidos} arquivo(s) movido(s).\n{erros} arquivo(s) com erro ao mover.\n{naoEncontrados} arquivo(s) sem pasta correspondente.\n"
        )
        self.executarBtn.config(state="normal", text="Executar")
        self.progressLabel.config(text="Processo concluído!")

    def executar(self):

        if not self.validar_entradas():
            return

        self.executando = True

        pastaOrigem = Path(self.pastaOrigemEntry.get())
        pastaDestino = Path(self.pastaDestinoEntry.get())
        pastaCaminho = self.pastaCaminhoEntry.get()
        renomear = self.renomearEntry.get()
        tipoArquivo = self.tipoArquivoCombo.get()
        localCodigo = self.localizacao_codigo[self.localizacao_codigo_selecionado]

        tamanho_codigo = self.tamanho_codigo

        arquivosMovidos = 0
        arquivosErro = 0
        arquivosNaoEncontrados = 0

        self.master.after(
            0, lambda: self.executarBtn.config(state="disabled", text="Executando...")
        )

        arquivos = (
            {}
        )  # codigo = {"arquivo": "teste.pdf", "destino": "C:/destino/codigo"}

        for arquivo in pastaOrigem.glob(
            f"*{self.arquivo_selecionado[tipoArquivo]}"
        ):  # criar itens no dicionário

            if tipoArquivo == "Pasta":
                if arquivo.is_dir():
                    codigo = (
                        arquivo.stem[:tamanho_codigo]
                        if localCodigo == "Início"
                        else arquivo.stem[-tamanho_codigo:]
                    )
                    arquivos[codigo] = {"arquivo": arquivo, "destino": None}

            else:
                codigo = (
                    arquivo.stem[:tamanho_codigo]
                    if localCodigo == "Início"
                    else arquivo.stem[-tamanho_codigo:]
                )
                arquivos[codigo] = {"arquivo": arquivo, "destino": None}

        for (
            pasta
        ) in (
            pastaDestino.iterdir()
        ):  # adicionar a pasta de destino nos itens do dicionário

            if not pasta.is_dir():
                continue

            codigo = pasta.name[:tamanho_codigo]

            if codigo not in arquivos:
                continue

            arquivos[codigo]["destino"] = pasta

        totalArquivos = len(arquivos)
        print(f"Total de arquivos a mover: {totalArquivos}")

        self.progressBar["maximum"] = totalArquivos
        self.progressBar["value"] = 0

        for item in arquivos:  # mover os arquivos para a pasta de destino

            self.master.after(
                0, lambda: self.atualizarProgresso(self.progressBar["value"] + 1)
            )

            arquivo = arquivos[item]["arquivo"]

            if arquivos[item]["destino"] is None:
                arquivosNaoEncontrados += 1
                print(f"Nenhuma pasta de destino encontrada para {arquivo.name}")
                continue

            caminhoDestino = arquivos[item]["destino"] / pastaCaminho

            print(f"Movendo {arquivo.name}")

            try:

                if not caminhoDestino.exists():
                    caminhoDestino.mkdir(parents=True, exist_ok=True)

                if renomear:
                    novoNome = f"{renomear}{arquivo.suffix}"
                else:
                    novoNome = arquivo.name

                shutil.move(arquivo, caminhoDestino / novoNome)

                arquivosMovidos += 1

            except Exception as e:
                arquivosErro += 1
                print(f"Erro ao mover o arquivo '{arquivo.name}': {e}")

        self.master.after(
            0,
            lambda: self.finalizar(
                arquivosMovidos, arquivosErro, arquivosNaoEncontrados
            ),
        )


root = Tk()
root.title("Gerenciar Arquivos")
Application(root)
root.mainloop()

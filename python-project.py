#################################################################################################
##########                   PROGRAMA PYBANKIG                                     ##############
##########          PROGRAMA QUE SIMULA AÇÕES EM UMA CONTA BANCÁRIA                ##############
##########             DATA DE TÉRMINO 24/06/2017                                  ##############
##########           DESENVOLVIDO POR MATEUS MEDEIROS E LAIO ALENCAR               ##############
##########              PROFESSOR FLAVIUS GORGONIO                                 ##############
########## UFRN/CERES CAMPUS CAICÓ, BSI 2017.1, ALGORITMOS E LÓGICA DE PROGRAMAÇÃO ##############
#################################################################################################

from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.messagebox import askquestion
from datetime import *
import smtplib
import pickle



arquivo=open('clientes.txt', 'rb')
dados_cliente = pickle.load(arquivo)
arquivo.close()
#
arquivo1=open('relatorios.txt', 'rb')
relatorios_cliente=pickle.load(arquivo1)
arquivo.close()
#
arquivo2=open('extratos.txt', 'rb')
extratos_cliente=pickle.load(arquivo2)
arquivo.close()
#

print(dados_cliente)


class AutoScrollbar(Scrollbar):
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
            Scrollbar.set(self, lo, hi)

class banco(object):
    def __init__(self, principal):
        self.principal=None
        # CORES
        corfundo = '#500'
        # FONTE
        self.font = ('Verdana', '20', 'bold')
        self.font1 = ('Verdana', '12', 'bold')
        self.font3 = ('Times New Roman', '30', 'bold')
        self.font4 = ('Times New Roman', '12', 'bold')
        self.font5=('Times New Roman', '8','bold')
        self.dinheiro = 'R$'
        # TITULO
        self.frametitulo = Frame(principal, bg='#500')
        self.frametitulo.grid(pady=70)
        self.titulo = Label(self.frametitulo, text='PyBanking', bg='#500', fg='white', font=self.font3)
        self.titulo.grid()

        # FRAMES
        self.frameprincipal = Frame(principal, bg='#500')
        self.frameprincipal.grid(sticky=W)
        #
        self.framesecundario = Frame(principal, bg='#500')
        self.framesecundario.grid(sticky=W, pady=30)
        #
        self.frameimagem=Frame(principal,bg = '#500')
        self.frameimagem.grid(sticky = S, ipadx= 10, columnspan= 40)
        # IMAGEM
        logo = PhotoImage(file='bancosx.gif')
        self.logo = Label(self.frameimagem, bg='#500')
        self.logo['image'] = logo
        self.logo.image = logo
        self.logo.grid()


        # LOGUIN E SENHA
        self.mensagem = Label(self.frameprincipal, text='Login de Usuário', font=self.font, bg='#500', fg='white', pady=50)
        self.mensagem.grid(row=0, column=1)
        self.loguinusuario = Label(self.frameprincipal, text='Login:', bg='#500', fg='white', font = self.font1)
        self.loguinusuario.grid(row=1, column=0)
        self.loguinusuario1 = Entry(self.frameprincipal)
        self.loguinusuario1.grid(row=1, column=1)
        #
        self.senhausuario = Label(self.frameprincipal, text='Senha:', bg='#500', fg='white', font = self.font1)
        self.senhausuario.grid(row=2, column=0)
        self.senhausuario1 = Entry(self.frameprincipal, show='*')
        self.senhausuario1.grid(row=2, column=1)
        #

        # BOTÕES
        self.entrar = Button(self.frameprincipal, text='Entrar', bg='green', fg='White', width= 17, font = self.font1)
        self.entrar.bind("<Button-1>", self.acesso_usuario)
        self.entrar.grid(row=1, column=3)
        #
        self.nova = Button(self.frameprincipal, text='Nova conta usuário', bg='green', fg='white',width= 17,font = self.font1)
        self.nova.bind("<Button-1>", self.criarconta_usuario)
        self.nova.grid(row=2, column=3)
        #


    def salvar_arquivo(self):
        #FUNÇÃO PARA SALVAR APÓS ALGUMA MUDANÇA
        aux_dados = dados_cliente
        self.arquivo = open('clientes.txt', 'wb')
        pickle.dump(aux_dados, self.arquivo)
        self.arquivo.close()
    def salvar_arquivo1(self):
        aux_dados = extratos_cliente
        self.arquivo = open('extratos.txt', 'wb')
        pickle.dump(aux_dados, self.arquivo)
        self.arquivo.close()
    def salvar_arquivo2(self):
        aux_dados = relatorios_cliente
        self.arquivo = open('relatorios.txt', 'wb')
        pickle.dump(aux_dados, self.arquivo)
        self.arquivo.close()

    def enviar_email_diario(self,event):
        x = self.loguin_usuario_acesso  #RECEBO O LOGIN DE ENTRADA
        email = dados_cliente[x][7]      # POSICÇÃO DO EMAIL
        a=len(relatorios_cliente[x])     # QUANTOS RELATORIOS TEM NO DICIONARIOS
        nome=dados_cliente[x][5]          # NOME DO USUARIO
        # DATAS#
        hoje = date.today()                   # PEGANDO A DATA ATUAL E DIMINUINDO 1 DIA
        ate = date.fromordinal(hoje.toordinal() - 1)
        valor=0
        for k in range(a):
            diaAux, mesAux, anoAux = relatorios_cliente[x][k][1].split('/')
            dataAux = date(int(anoAux), int(mesAux), int(diaAux))
            if dataAux <= hoje and dataAux >= ate:
                valor+=relatorios_cliente[x][k][2]
        if valor > 500:
            msg1='Voce gastou mais que R$ 500,00, entao consideramos dia %s um bom dia para gastar!' % (ate)
        else:
            msg1='Voce gastou menos que R$ 500,00 nesse periodo, entao nao consideramos um dia de gastos.'
        print(valor)


        fromaddr = '<pybanking@gmail.com>'
        toaddrs = email
        msg = 'Ola senhor(a) %s!\nSeus gastos no ultimo dia foram de R$ %5.2f\n%s\nGratos, direcao PyBanking.' % (nome,valor,msg1)
        subject = 'PyBanking'
        message = 'Subject: %s\n\n%s' % (subject, msg)

        # Dados da conta utilizada para enviar o email
        username = 'pybanking@gmail.com'
        password = 'python123'

        # Lógica de envio dos dados
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.sendmail(fromaddr, toaddrs, message)
        server.quit()
    def enviar_email_semanal(self,event):
        x = self.loguin_usuario_acesso
        email = dados_cliente[x][7]
        a = len(relatorios_cliente[x])
        nome = dados_cliente[x][5]
        # DATAS#
        hoje = date.today()
        ate = date.fromordinal(hoje.toordinal() - 7)
        valor = 0
        for k in range(a):
            diaAux, mesAux, anoAux = relatorios_cliente[x][k][1].split('/')
            dataAux = date(int(anoAux), int(mesAux), int(diaAux))
            if dataAux <= hoje and dataAux >= ate:
                valor += relatorios_cliente[x][k][2]
        if valor > 1000:
            msg1 = 'Voce gastou mais que R$ 1000,00, entao consideramos uma boa semana para gastar!'
        else:
            msg1 = 'Voce gastou menos que R$ 1000,00 nesse periodo, entao nao consideramos uma semana de gastos.'
        print(valor)

        fromaddr = '<pybanking@gmail.com>'
        toaddrs = email
        msg = 'Ola senhor(a) %s!\nSeus gastos na ultima semana foram de R$ %5.2f\n%s\nGratos, direcao PyBanking.' % (
        nome, valor, msg1)
        subject = 'PyBanking'
        message = 'Subject: %s\n\n%s' % (subject, msg)

        # Dados da conta utilizada para enviar o email
        username = 'pybanking@gmail.com'
        password = 'python123'

        # Lógica de envio dos dados
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.sendmail(fromaddr, toaddrs, message)
        server.quit()
    def enviar_email_mensal(self,event):
        x = self.loguin_usuario_acesso
        email = dados_cliente[x][7]
        a = len(relatorios_cliente[x])
        nome = dados_cliente[x][5]
        # DATAS#
        hoje = date.today()
        ate = date.fromordinal(hoje.toordinal() - 31)
        valor = 0
        for k in range(a):
            diaAux, mesAux, anoAux = relatorios_cliente[x][k][1].split('/')
            dataAux = date(int(anoAux), int(mesAux), int(diaAux))
            if dataAux <= hoje and dataAux >= ate:
                valor += relatorios_cliente[x][k][2]
        if valor > 2500:
            msg1 = 'Voce gastou mais que R$ 2500,00, entao consideramos um bom mes para gastar!'
        else:
            msg1 = 'Voce gastou menos que R$ 2500,00 nesse periodo, entao nao consideramos um mes de gastos.'
        print(valor)

        fromaddr = '<pybanking@gmail.com>'
        toaddrs = email
        msg = 'Ola senhor(a) %s!\nSeus gastos no ultimo mes foram de R$ %5.2f\n%s\nGratos, direcao PyBanking.' % (
            nome, valor, msg1)
        subject = 'PyBanking'
        message = 'Subject: %s\n\n%s' % (subject, msg)

        # Dados da conta utilizada para enviar o email
        username = 'pybanking@gmail.com'
        password = 'python123'

        # Lógica de envio dos dados
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.sendmail(fromaddr, toaddrs, message)
        server.quit()
    def enviar_email_semestral(self,event):
        x = self.loguin_usuario_acesso
        email = dados_cliente[x][7]
        a = len(relatorios_cliente[x])
        nome = dados_cliente[x][5]
        # DATAS#
        hoje = date.today()
        ate = date.fromordinal(hoje.toordinal() - 182)
        valor = 0
        for k in range(a):
            diaAux, mesAux, anoAux = relatorios_cliente[x][k][1].split('/')
            dataAux = date(int(anoAux), int(mesAux), int(diaAux))
            if dataAux <= hoje and dataAux >= ate:
                valor += relatorios_cliente[x][k][2]
        if valor > 10000:
            msg1 = 'Voce gastou mais que R$ 10000,00, entao consideramos um bom semestre para gastar!'
        else:
            msg1 = 'Voce gastou menos que R$ 10000,00 nesse periodo, entao nao consideramos um semestre de gastos.'
        print(valor)

        fromaddr = '<pybanking@gmail.com>'
        toaddrs = email
        msg = 'Ola senhor(a) %s!\nSeus gastos no ultimo semestre foram de R$ %5.2f\n%s\nGratos, direcao PyBanking.' % (
            nome, valor, msg1)
        subject = 'PyBanking'
        message = 'Subject: %s\n\n%s' % (subject, msg)

        # Dados da conta utilizada para enviar o email
        username = 'pybanking@gmail.com'
        password = 'python123'

        # Lógica de envio dos dados
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.sendmail(fromaddr, toaddrs, message)
        server.quit()
    def enviar_email_anual(self,event):
        x = self.loguin_usuario_acesso
        email = dados_cliente[x][7]
        a = len(relatorios_cliente[x])
        nome = dados_cliente[x][5]
        # DATAS#
        hoje = date.today()
        ate = date.fromordinal(hoje.toordinal() - 365)
        valor = 0
        for k in range(a):
            diaAux, mesAux, anoAux = relatorios_cliente[x][k][1].split('/')
            dataAux = date(int(anoAux), int(mesAux), int(diaAux))
            if dataAux <= hoje and dataAux >= ate:
                valor += relatorios_cliente[x][k][2]
        if valor > 20000:
            msg1 = 'Voce gastou mais que R$ 25000,00, entao consideramos um bom ano para gastar!'
        else:
            msg1 = 'Voce gastou menos que R$ 25000,00 nesse periodo, entao nao consideramos um ano de gastos.'
        print(valor)

        fromaddr = '<pybanking@gmail.com>'
        toaddrs = email
        msg = 'Ola senhor(a) %s!\nSeus gastos no ultimo ano foram de R$ %5.2f\n%s\nGratos, direcao PyBanking.' % (
            nome, valor, msg1)
        subject = 'PyBanking'
        message = 'Subject: %s\n\n%s' % (subject, msg)

        # Dados da conta utilizada para enviar o email
        username = 'pybanking@gmail.com'
        password = 'python123'

        # Lógica de envio dos dados
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username, password)
        server.sendmail(fromaddr, toaddrs, message)
        server.quit()

    def criarconta_usuario(self, event):
        if self.principal is None:
            self.principal = Tk()
            self.principal.protocol("WM_DELETE_WINDOW", self.fecha_jan)
            # FRAMES
            self.framegeral = Frame(self.principal, bg='gray21')
            self.framegeral.grid()
            # LOGUIN
            self.loguin = Label(self.framegeral, text='Login:', font=self.font1, bg='gray21', fg='white')
            self.loguin.grid(row=0, column=0)
            self.loguin1 = Entry(self.framegeral)
            self.loguin1.grid(row=0, column=1)
            # SENHA
            self.senha = Label(self.framegeral, text='Senha: ', font=self.font1, bg='gray21', fg='white')
            self.senha.grid(row=1, column=0)
            self.senha1 = Entry(self.framegeral, show='*')
            self.senha1.grid(row=1, column=1)
            #BANCO
            bancox=('Banco do Brasil', 'Bradesco', 'Caixa Econômica Federal', 'Santander', 'HSBC', 'Itaú', 'BNDES', 'Banrisul', 'Banco do Nordeste')
            self.banco=Label(self.framegeral, text = 'Banco:', font = self.font1, bg = 'gray21', fg = 'white')
            self.banco.grid(row = 2, column = 0)
            self.banco1=Spinbox(self.framegeral,value =(bancox),state="readonly")
            self.banco1.grid(row = 2, column = 1)
            #N° CONTA
            self.nconta=Label(self.framegeral,text = 'N° Conta (8 números):', font = self.font1, bg = 'gray21', fg = 'white')
            self.nconta.grid(row= 3, column = 0)
            self.nconta1 = Entry(self.framegeral)
            self.nconta1.grid(row=3, column=1)
            #
            tipo=('Corrente','Poupança')
            self.tipoconta=Label(self.framegeral, text = 'Tipo de conta: ' , font= self.font1, bg = 'gray21',fg = 'white')
            self.tipoconta.grid(row=4, column=0)
            self.tipoconta1=Spinbox(self.framegeral, value=(tipo), state='readonly')
            self.tipoconta1.grid(row=4, column = 1)
            #N° CPF
            self.ncpf = Label(self.framegeral, text='N° CPF (Somente números) :', font=self.font1, bg='gray21', fg='white')
            self.ncpf.grid(row=5, column=0)
            self.ncpf1 = Entry(self.framegeral)
            self.ncpf1.grid(row=5, column=1)
            #NOME
            self.nome = Label(self.framegeral, text='Nome :', font=self.font1, bg='gray21', fg='white')
            self.nome.grid(row=6, column=0)
            self.nome1 = Entry(self.framegeral)
            self.nome1.grid(row=6, column=1)
            #EMAIL
            self.email=Label(self.framegeral, text='E-Mail :', font=self.font1, bg='gray21', fg='white')
            self.email.grid(row=7, column=0)
            self.email = Entry(self.framegeral)
            self.email.grid(row=7, column=1)
            

            # BOTÃO
            self.botaogravar = Button(self.framegeral, text='Cadastrar', font=self.font1, bg='green', fg='white')
            self.botaogravar.bind("<Button-1>", self.gravar_usuario)
            self.botaogravar.grid(row=8, column=1)
            #
            self.principal.configure(background='gray21')
            self.principal.wm_iconbitmap('icon.ico')
            self.principal.title('Nova conta usuario')
            self.principal.geometry('450x250')
        else:
            # Se já foi, basta colocá-la na frente
            self.principal.lift()
    def fecha_jan(self):
        # Seta de novo em None para recriar quando abrir
        self.principal.destroy()
        self.principal = None
    def fecha_jan1(self):
        self.janela_usuario.destroy()
        self.janela_usuario=None

    def gravar_usuario(self, event):
        loguin_gravar_usuario =self.loguin1.get().upper()
        senha_gravar_usuario = self.senha1.get()
        banco_gravar_usuario=self.banco1.get().upper()         #RECEBENDO OS DADOS DIGITADOS
        conta=self.nconta1.get()
        cpf=self.ncpf1.get()
        nome=self.nome1.get().upper()
        tipoconta=self.tipoconta1.get().upper()
        email=self.email.get()
        if loguin_gravar_usuario not in dados_cliente:         #VERIFICAÇÕES
                if len(loguin_gravar_usuario) != 0 and len(senha_gravar_usuario) != 0 and len(email) != 0 and len(nome) !=0 and len(banco_gravar_usuario) != 0:
                        if len(conta) == 8 and  len(cpf)==11:
                            if self.valida_cpf(cpf)==True:
                                if conta.isdigit():
                                        cont=0
                                        for i in dados_cliente:
                                            if dados_cliente[i][2] ==conta or dados_cliente[i][3]==cpf:  #VENDO SE O CPF JA ESTÁ CADASTRADO
                                                cont+=1
                                        if cont == 0:
                                            aux_extratos=[]
                                            aux_relatorios=[]
                                            relatorios_cliente[loguin_gravar_usuario] = aux_relatorios
                                            aux = [senha_gravar_usuario, banco_gravar_usuario, conta, cpf,0,nome,tipoconta,email]
                                            dados_cliente[loguin_gravar_usuario] = aux
                                            extratos_cliente[loguin_gravar_usuario]=aux_extratos
                                            showinfo(title='Êxito', message='Cadastro Realizado')       #GRAVANDO OS DADOS
                                            self.salvar_arquivo()
                                            self.salvar_arquivo1()
                                            self.salvar_arquivo2()
                                        else:
                                            showinfo(title='Falha', message='Já existe usuario cadastrdo com esse CPF ou N°CONTA!')
                                else:
                                    showinfo(title='Falha', message='Número de conta inválido, digite somente números.')
                            else:
                                showinfo(title='Falha', message='CPF inválido')
                        else:
                            showinfo(title='Falha', message='Digite 11 digitos para o cpf e 8 para a conta!')
                else:
                    showinfo(title='Falha', message='Você deixou campos em branco!')
        else:
            showinfo(title='Falha', message='Usuario já cadastrado')

    def acesso_usuario(self, event):
        self.loguin_usuario_acesso = self.loguinusuario1.get().upper()
        senha_usuario_acesso = self.senhausuario1.get()
        if self.loguin_usuario_acesso in dados_cliente:
            if dados_cliente[self.loguin_usuario_acesso][0] == senha_usuario_acesso:
                result=askquestion(title='Êxito', message='Acesso permitido, prosseguir?')
                if result == 'yes':
                    self.janela_usuario(event)

            else:
                showinfo(title='Falha', message='Acesso negado')
        else:
            showinfo(title='Falha', message='Usuario e/ou senha incorretos')

    def janela_usuario (self,event):
        if self.principal==None:
            self.janela_usuario=None
            self.principal = Tk()
            self.principal.protocol("WM_DELETE_WINDOW", self.fecha_jan)
            self.font = ('Verdana', '20', 'bold')
            self.font1 = ('Verdana', '10', 'bold')
            self.font2=('Times New Roman', '15', 'bold')
            # Frame
            self.frameUsuario = Frame(self.principal, bg='red4')
            self.frameUsuario.pack()
            self.frameBotao = Frame(self.principal, bg='red4',pady= 30)
            self.frameBotao.pack()
            #
            x = self.loguin_usuario_acesso
            self.boasvindas=Label(self.frameBotao, text='Seja bem vindo(a), Sr(a)' , fg = 'snow' , bg = 'red4', font=self.font,pady=30)
            self.boasvindas.pack()
            self.boasvindas1 = Label(self.frameBotao, fg='snow', bg='red4', font=self.font,pady=30)
            self.boasvindas1['text']=dados_cliente[x][5]
            self.boasvindas1.pack()

            # Botões
            self.opcaoUsuario = Button(self.frameBotao, text='Opções do Usuário', font=self.font2, bg='white', fg='black',width=100, padx=10,height = 2)
            self.opcaoUsuario.pack(side= TOP)
            self.opcaoUsuario.bind('<Button-1>', self.opcao_usuario)
            #
            self.operacaoConta = Button(self.frameBotao, text='Operações da Conta', font=self.font2, bg='white', fg='black',width=100, padx=10,height = 2)
            self.operacaoConta.bind('<Button-1>', self.operacoes_conta)
            self.operacaoConta.pack(side= TOP)
            #
            self.relatorio = Button(self.frameBotao, text='Relatórios', font=self.font2, bg='white', fg='black',width=100, padx=10, height = 2)
            self.relatorio.bind('<Button-1>', self.relatorios)
            self.relatorio.pack(side= TOP)
            #
            self.saldoextrato = Button(self.frameBotao, text='Informações, saldos e extratos', font=self.font2, bg='white', fg='black',width=100, padx=10,height = 2)
            self.saldoextrato.bind('<Button-1>', self.saldos_extratos)
            self.saldoextrato.pack(side= TOP)
            #
            self.inf_gerais1 = Button(self.frameBotao, text='Informações Gerais sobre o Programa', font=self.font2, bg='white', fg='black', width=100, padx=10,height = 2)
            self.inf_gerais1.bind('<Button-1>', self.inf_gerais)
            self.inf_gerais1.pack(side= TOP)
            #
            self.aviso=Label(self.frameBotao, text='*É extremamente aconselhavel ler as informações gerais sobre o programa antes de iniciar o uso.*' , fg = 'snow' , bg = 'red4', font=self.font4,pady=30)
            self.aviso.pack()

            self.principal.geometry("{0}x{1}+0+0".format(self.principal.winfo_screenwidth(), self.principal.winfo_screenheight()))
            self.principal.wm_iconbitmap('icon.ico')
            self.principal.configure(background='red4')
            self.principal.title('Tela do Usuário')
        else:
            # Se já foi, basta colocá-la na frente
            self.principal.lift()

    def opcao_usuario(self,event):
        if self.janela_usuario == None:
            self.janela_usuario=Tk()
            self.janela_usuario.protocol("WM_DELETE_WINDOW", self.fecha_jan1)
            self.font = ('Verdana', '20', 'bold')
            self.font1 = ('Verdana', '10', 'bold')
            # Frame
            self.frameSenha = Frame(self.janela_usuario, bg='red4')
            self.frameSenha.grid()
            self.frameBotao1 = Frame(self.janela_usuario, bg='red4')
            self.frameBotao1.grid()
            #
            self.tituloTela1 = Label(self.frameSenha, text='OPÇÕES USUÁRIO', fg='snow', bg='red4', font=self.font,pady=10)
            self.tituloTela1.grid(row=1, column=40)
            #
            # Botões
            self.alterarSenha = Button(self.frameBotao1, text='Alterar senha', font=self.font1, bg='white', fg='black', width=25, pady=10)
            self.alterarSenha.grid(row=1, column=1, pady=10)
            self.alterarSenha.bind('<Button-1>', self.alterar_senha)
            #
            self.deletarJanela = Button(self.frameBotao1, text='Deletar conta', font=self.font1, bg='white', fg='black', width=25, pady=10)
            self.deletarJanela.bind('<Button-1>', self.deletar_conta)
            self.deletarJanela.grid(row=2, column=1, pady=10)
            #
            self.alterarbanco=Button(self.frameBotao1, text = 'Alterar Banco', font = self.font1, bg = 'white', fg = 'black', width = 25, pady=10)
            self.alterarbanco.bind('<Button-1>', self.alterar_banco)
            self.alterarbanco.grid(row=3,column = 1, pady= 10)

            self.janela_usuario.configure(background='red4')
            self.janela_usuario.wm_iconbitmap('icon.ico')
            self.janela_usuario.title('Opções do Usuário')
        else:
            # Se já foi, basta colocá-la na frente
            self.janela_usuario.lift()

    def alterar_senha (self, event):
        alterarsenha= Tk()
        self.label=Label(alterarsenha, text = 'Nova senha', bg='red4', fg= 'snow', font = self.font1)
        self.label.pack()
        #
        self.entry=Entry(alterarsenha)
        self.entry.pack()
        #
        self.botao=Button(alterarsenha, text = 'Salvar', bg = 'green', fg = 'white', font=self.font1)
        self.botao.bind('<Button-1>', self.salvar)
        self.botao.pack()

        alterarsenha.configure(bg = 'red4')
        alterarsenha.wm_iconbitmap('icon.ico')
        alterarsenha.geometry('300x100')
        alterarsenha.mainloop()

    def salvar (self,event):
        x=self.entry.get()
        y=self.loguin_usuario_acesso
        if len(x)>0:
            dados_cliente[y][0]=x
            print(dados_cliente)
            showinfo(title='Êxito', message= 'Senha alterada com sucesso')
            self.salvar_arquivo()
            self.salvar_arquivo1()
            self.salvar_arquivo2()
        #

    def deletar_conta(self,event):
        deletarconta = Tk()
        self.label1 = Label(deletarconta, text='Digite seu loguin', font=self.font1, bg = 'red4', fg = 'snow')
        self.label1.pack()
        #
        self.entry1 = Entry(deletarconta)
        self.entry1.pack()
        #
        self.botao1 = Button(deletarconta, text='Deletar', bg = 'white', fg = 'black',font= self.font1)
        self.botao1.bind('<Button-1>', self.deletar)
        self.botao1.pack()
        #
        deletarconta.configure(bg='red4')
        deletarconta.wm_iconbitmap('icon.ico')
        deletarconta.geometry('300x100')
        deletarconta.mainloop()

    def deletar (self,event):
        if len(self.entry1.get()) != 0:
            if (self.loguin_usuario_acesso.upper()) == (self.entry1.get().upper()):
                y=askquestion(title = 'Aviso!',message= 'Tem certeza que deseja excluir sua conta?')
                if y == 'yes':
                    x = self.loguin_usuario_acesso
                    del dados_cliente[x]
                    del relatorios_cliente[x]
                    del extratos_cliente[x]
                    print(dados_cliente)
                    self.salvar_arquivo()
                    self.salvar_arquivo1()
                    self.salvar_arquivo2()

            else:
                showinfo(title='Aviso!', message='Login Inválido')
        else:
            showinfo(title='Aviso!', message='Login Inválido')

    def alterar_banco (self,event):
        alterar = Tk()
        bancox = ('Banco do Brasil', 'Bradesco', 'Caixa Econômica Federal', 'Santander', 'HSBC', 'Itaú', 'BNDES', 'Banrisul','Banco do Nordeste')
        bancoy=('Corrente', 'Poupança')
        self.label1 = Label(alterar, text='Número Conta:', font=self.font1, bg='red4', fg='snow')
        self.label1.grid(row= 0, column =0)
        self.entry1 = Entry(alterar)
        self.entry1.grid(row= 0, column =1)
        #
        self.label2=Label(alterar,text= 'Banco:', font = self.font1, bg ='red4', fg ='snow')
        self.label2.grid(row=1,column = 0)
        self.box=Spinbox(alterar, value = (bancox), state= 'readonly')
        self.box.grid(row=1, column =1)
        #
        self.label3=Label(alterar, text = 'Tipo conta:', font = self.font1, bg = 'red4', fg = 'snow')
        self.label3.grid(row=2,column =0)
        self.box1 = Spinbox(alterar, value=(bancoy), state='readonly')
        self.box1.grid(row=2, column=1)

        #
        self.botao1 = Button(alterar, text='Alterar', bg='white', fg='black', font=self.font1)
        self.botao1.bind('<Button-1>',self.alterar )
        self.botao1.grid(row = 3, column =1, pady = 20)
        #
        alterar.configure(bg='red4')
        alterar.wm_iconbitmap('icon.ico')
        alterar.geometry('330x150')
        alterar.mainloop()

    def alterar(self,event):
        x = self.loguin_usuario_acesso
        y=dados_cliente[x][4]
        a=self.entry1.get()
        conta = self.entry1.get()
        if a.isdigit():
            if len(a) ==8:
                if y==0:
                    cont = 0                         #VERIFICAÇÕES
                    for i in dados_cliente:
                        if dados_cliente[i][2] == conta:
                            cont += 1
                    if cont == 0:
                        for i in range(len(dados_cliente)):
                            dados_cliente[x][1]=self.box.get()
                            dados_cliente[x][2]=a
                            dados_cliente[x][4]=0
                            dados_cliente[x][6]=self.box1.get()            #SALVANDO
                            extratos_cliente[x]=[]
                            relatorios_cliente[x]=[]
                            self.salvar_arquivo()
                            self.salvar_arquivo1()
                            self.salvar_arquivo2()
                        showinfo(title='Êxito', message='Banco alterado com sucesso!')
                    else:
                        showinfo(title='Falha', message = 'Já existe esse número de banco cadastrado!')
                else:
                    showinfo(title='Falha', message='Saque todo dinheiro da conta antes de alterar o banco!')
            else:
                showinfo(title='Falha', message='Número da conta deve contar 8 números!')
        else:
            showinfo(title='Falha',message='Digite somente números!')

    def operacoes_conta(self,event):
        operacoes_conta = Tk ()

        self.font = ('Verdana', '20', 'bold')
        self.font1 = ('Verdana', '10', 'bold')
        # Frame
        self.frameoperacoes = Frame(operacoes_conta, bg='red4')
        self.frameoperacoes.grid()
        self.frameBotao1 = Frame(operacoes_conta, bg='red4')
        self.frameBotao1.grid()
        # Tela
        self.tituloTela2 = Label(self.frameoperacoes, text='Operações de Contas', fg='snow', bg='red4',font=self.font)
        self.tituloTela2.grid(row=1, column=40)

        # Botões
        self.botaosaque = Button(self.frameBotao1, text='Saque', font=self.font1, bg='snow',fg='black', width=25, padx=10)
        self.botaosaque.grid(row=3, column=1, padx=10, pady=10)
        self.botaosaque.bind('<Button-1>',self.saque)
        #
        self.botaodeposito = Button(self.frameBotao1, text='Deposito', font=self.font1, bg='snow',fg='black', width=25, padx=10)
        self.botaodeposito.bind('<Button-1>' , self.deposito)
        self.botaodeposito.grid(row=3, column=2, padx=10, pady=10)
        #
        self.botaotransf = Button(self.frameBotao1, text='Transferência', font=self.font1, bg='snow', fg='black', width=25, padx=10)
        self.botaotransf.bind('<Button-1>', self.transferencia)
        self.botaotransf.grid(row=3, column=3, padx=10, pady=10)
        #
        self.botaopag = Button(self.frameBotao1, text='Pagamentos', font=self.font1, bg='snow',fg='black', width=25, padx=10)
        self.botaopag.bind('<Button-1>', self.pagamento)
        self.botaopag.grid(row=4, column=1, padx=10, pady=10)
        #
        self.jurostaxas = Button(self.frameBotao1, text='Informações de Taxas', font=self.font1, bg='snow',fg='black', width=25, padx=10)
        self.jurostaxas.bind('<Button-1>', self.juros_taxas)
        self.jurostaxas.grid(row=4, column=2, padx=10, pady=10)
        #


        operacoes_conta.configure(background='red4')
        operacoes_conta.wm_iconbitmap('icon.ico')
        operacoes_conta.geometry('850x200')
        operacoes_conta.title('Tela do Usuário')
        operacoes_conta.mainloop()

    def saque (self,event):
        saque = Tk()
        #FRAMES
        self.framesaque=Frame(saque, bg='navajo White')
        self.framesaque.grid()
        #
        self.framesaque1=Frame(saque,bg='navajo White')
        self.framesaque1.grid()
        #
        x=self.loguin_usuario_acesso
        self.qnt=Label(self.framesaque, text = 'Seu saldo é: ' ,font=self.font, bg = 'navajo White',pady=10)
        self.qnt.grid(row = 1, column = 0)
        self.qnt1=Label(self.framesaque,font = self.font, bg = 'navajo White',fg = 'green', pady=10)
        self.qnt1.grid(row = 1, column = 1)
        self.qnt1['text']=('R$%10.2f' % dados_cliente[x][4])
        #
        self.saquelabel=Label(self.framesaque1, text = 'Quantidade que deseja sacar:', font = self.font1,bg = 'navajo White')
        self.saquelabel.grid(row=2,column = 1)
        self.saqueentry=Entry(self.framesaque1)
        self.saqueentry.grid(row = 2, column = 2)
        #
        self.saquebotao=Button(self.framesaque1, text = 'Sacar', font= self.font1, bg = 'green', fg = 'white', width = 10)
        self.saquebotao.bind('<Button-1>', self.sacar)
        self.saquebotao.grid(row = 3, column = 2)
        #
        self.saquebotaotudo=Button(self.framesaque1, text = 'Sacar tudo', font= self.font1, bg = 'green', fg = 'white', width= 10)
        self.saquebotaotudo.bind('<Button-1>',self.sacar_tudo)
        self.saquebotaotudo.grid(row=4, column=2,pady = 5)

        saque.title('Janela de Saques')
        saque.wm_iconbitmap('icon.ico')
        saque.configure(background='navajo White')
        saque.geometry('450x200')
        saque.mainloop()

    def sacar (self, event):
        x=self.loguin_usuario_acesso
        m =self.saqueentry.get()
        m1 = float(dados_cliente[x][4])
        typo = 'Saque'
        data = datetime.now()
        data1=data.strftime("%d %b %Y às %H:%M:%S")
        dataR = date.today().strftime("%d/%m/%Y")

        if self.valida_num(m) == True:  #VERIFICANDO SE A FUNÇÃO DE VALIDAÇÃO RETORNA VERDADEIRO
            m=float(m)
            if m1 >= m:
                if m >0:
                    m2=m1-m
                    aux_extratos=[typo,data1,m]
                    aux_relatorios = [typo, dataR, m]
                    extratos_cliente[x].append(aux_extratos)
                    relatorios_cliente[x].append(aux_relatorios)
                    dados_cliente[x][4]=m2                                     #SACANDO
                    self.qnt1['text'] =('%10.2f' % dados_cliente[x][4])
                    showinfo(title = 'Êxito', message='Saque realizado com sucesso!')
                    self.salvar_arquivo()
                    self.salvar_arquivo1()
                    self.salvar_arquivo2()
                else:
                    showinfo(title='Falha', message='Quantia inválida')
            else:
                showinfo(title='Falha', message='Você não possui essa quantidade para sacar')
        else:
            showinfo(title= 'Falha', message='Digite somente números')

    def sacar_tudo(self,event):
        x=self.loguin_usuario_acesso
        m1 = float(dados_cliente[x][4])
        if m1 >0:
            typo = 'Saque'
            data = datetime.now()
            data1=data.strftime("%d %b %Y às %H:%M:%S")
            dataR = date.today().strftime("%d/%m/%Y")
            aux_extratos=[typo,data1,m1]
            aux_relatorios=[typo,dataR,m1]
            extratos_cliente[x].append(aux_extratos)
            relatorios_cliente[x].append(aux_relatorios)
            dados_cliente[x][4]=0
            self.qnt1['text'] =('%10.2f' % dados_cliente[x][4])
            showinfo(title = 'Êxito', message='Saque realizado com sucesso!')
            self.salvar_arquivo()
            self.salvar_arquivo1()
            self.salvar_arquivo2()
        else:
            showinfo(title='Falha', message='Você não possui nada para sacar!')

    def deposito (self,event):
        deposito = Tk()
        #FRAMES
        self.framedeposito=Frame(deposito, bg='navajo White')
        self.framedeposito.grid()
        #
        self.framedeposito1=Frame(deposito,bg='navajo White')
        self.framedeposito1.grid()
        #
        x=self.loguin_usuario_acesso
        self.qntdep=Label(self.framedeposito, text = 'Seu saldo é: ',font=self.font,bg= 'navajo White', pady=10)
        self.qntdep.grid(row = 1, column = 0)
        self.qntdep1=Label(self.framedeposito,font = self.font, bg = 'navajo White', fg = 'green', pady=10)
        self.qntdep1.grid(row = 1, column = 1)
        self.qntdep1['text']=('R$%10.2f' % dados_cliente[x][4])
        #
        self.depositolabel=Label(self.framedeposito1, text = 'Quantidade que deseja Depositar (Máx: R$ 100000):', font = self.font1,bg = 'navajo White')
        self.depositolabel.grid(row=2,column = 1)
        self.depositoentry=Entry(self.framedeposito1)
        self.depositoentry.grid(row = 2, column = 2)
        self.depositobotao=Button(self.framedeposito1, text = 'Depositar', bg= 'green', fg = 'white')
        self.depositobotao.bind('<Button-1>', self.depositar)
        self.depositobotao.grid(row = 3, column = 2)

        deposito.title('Janela de Depósitos')
        deposito.wm_iconbitmap('icon.ico')
        deposito.configure(background='navajo White')
        deposito.geometry('550x200')

    def depositar (self,event):
        x = self.loguin_usuario_acesso
        m =self.depositoentry.get()
        m1 = float(dados_cliente[x][4])
        typo1 = 'Depósito'
        data = datetime.now()
        data1 = data.strftime("%d %b %Y às %H:%M:%S")
        if self.valida_num(m) == True:
            m=float(m)
            if m <=100000 and m >0:
                aux_extratos = [typo1, data1, m]
                extratos_cliente[x].append(aux_extratos)
                m2=m1+m
                dados_cliente[x][4] = m2
                self.qntdep1['text'] =('%10.2f' % dados_cliente[x][4])
                self.salvar_arquivo()
                self.salvar_arquivo1()
                self.salvar_arquivo2()
                showinfo(title='Êxito', message='Deposito realizado com sucesso!')
            else:
                showinfo(title='Falha', message='Quantidade indisponível!')
        else:
            showinfo(title='Falha', message='Digite somente números')

    def transferencia (self,event):
        transf = Tk()
        #FRAMES
        self.frametransf=Frame(transf, bg='navajo White')
        self.frametransf.grid()
        #
        x=self.loguin_usuario_acesso
        self.qntsaldo=Label(self.frametransf, text = 'Seu saldo é: ' ,font=self.font, bg = 'navajo White',pady=15)
        self.qntsaldo.grid(row = 1, column = 0)
        self.qntsaldo1=Label(self.frametransf,font = self.font, bg = 'navajo White', fg ='green',pady=15)
        self.qntsaldo1.grid(row = 1, column = 1)
        self.qntsaldo1['text']=('R$%10.2f' % dados_cliente[x][4])
        #
        self.qnttransf=Label(self.frametransf, text ='Quantidade da transferência' ,font= self.font1, bg= 'navajo White')
        self.qnttransf.grid(row = 2, column =0)
        self.qnttransf1=Entry(self.frametransf)
        self.qnttransf1.grid(row = 2, column = 1)
        #
        self.numconta=Label(self.frametransf, text = 'Número da conta à transferir', font = self.font1, bg = 'navajo White')
        self.numconta.grid(row=3,column = 0)
        self.numconta1=Entry(self.frametransf)
        self.numconta1.grid(row = 3, column =1)
        #
        self.botaotransferir=Button(self.frametransf, text = 'Transferir', font = self.font1, bg='green' ,fg= 'white')
        self.botaotransferir.bind('<Button-1>', self.transferir)
        self.botaotransferir.grid(row = 5, column =2 )
        #
        transf.title('Janela de Transferências')
        transf.wm_iconbitmap('icon.ico')
        transf.configure(background='navajo White')
        transf.geometry('500x200')

    def transferir (self,event):
        x = self.loguin_usuario_acesso
        aux=self.numconta1.get()
        m =(self.qnttransf1.get())
        m1 = float(dados_cliente[x][4])
        typo1 = 'Transferência'
        data = datetime.now()
        data1 = data.strftime("%d %b %Y às %H:%M:%S")
        dataR = date.today().strftime("%d/%m/%Y")

        if self.valida_num(m) == True:
            m=float(m)
            porc= m * 0.07
            m2=m+porc
            if m1 >= m:
                if m > 0:
                    if aux != dados_cliente[x][2]:          #VERIFICAÇÕES
                        cont = 0
                        for i in dados_cliente:
                            if aux == dados_cliente[i][2]:
                                cont+=1
                                nomebanco1=(dados_cliente[i][1].upper())
                                nomebanco2=(dados_cliente[x][1].upper())
                                if nomebanco1==nomebanco2:
                                    aux_relatorios=[typo1,dataR,m]
                                    aux_extratos = [typo1, data1, m]
                                    extratos_cliente[x].append(aux_extratos)
                                    relatorios_cliente[x].append(aux_relatorios)
                                    aux1=float(dados_cliente[i][4])                 #SE OS BANCOS FOREM IGUAIS, NAO SERÁ COBRADA TAXA
                                    m3=m1-m
                                    dados_cliente[x][4]=m3
                                    self.qntsaldo1['text']=('%10.2f' % dados_cliente[x][4])
                                    aux2=aux1+m
                                    dados_cliente[i][4]=aux2
                                    self.salvar_arquivo()
                                    self.salvar_arquivo1()
                                    self.salvar_arquivo2()
                                    showinfo(title='Êxito', message='Transferência  realizada com sucesso!')
                                    showinfo(title='Êxito', message='Bancos iguais, não foi cobrada nenhuma taxa de transferência!')
                                else:
                                    quest=askquestion(title='Aviso!' , message='Será cobrada uma taxa de 7% por conta da diferença de bancos, prosseguir?')
                                    if quest == 'yes':
                                        if m1 > m2:
                                            aux_relatorios = [typo1, dataR, m]
                                            aux_extratos = [typo1, data1, m2]
                                            extratos_cliente[x].append(aux_extratos)
                                            relatorios_cliente[x].append(aux_relatorios)
                                            aux1 = float(dados_cliente[i][4])
                                            m4 = m1 - m2
                                            dados_cliente[x][4] = m4                                      #CASO CONTRÁRIO SERÁ COBRADA UMA TAXA DE 7%
                                            self.qntsaldo1['text'] = ('%10.2f' % dados_cliente[x][4])
                                            aux2 = aux1 + m
                                            dados_cliente[i][4] = aux2
                                            self.salvar_arquivo()
                                            self.salvar_arquivo1()
                                            self.salvar_arquivo2()
                                            showinfo(title='Êxito', message='Transferência  realizada com sucesso!')
                                        else:
                                            showinfo(title='Falha', message = 'Dinheiro insuficiente para operação')
                        if cont == 0:
                            showinfo(title='Falha', message='Conta não encontrada')
                    else:
                        showinfo(title='Falha', message='Não é possível transferir para sua própria conta')
                else:
                    showinfo(title='Falha', message='Quantia inválida')
            else:
                showinfo(title='Falha', message='Você não possui essa quantidade para transferir')
        else:
            showinfo(title='Falha', message='Digite somente números')

    def pagamento (self,event):
        pagamento1 = Tk()
        #
        self.framePagamento = Frame(pagamento1, bg='navajo White')
        self.framePagamento.grid()
        self.frameBotaopag = Frame(pagamento1, bg='navajo White')
        self.frameBotaopag.grid()
        #
        x = self.loguin_usuario_acesso
        #
        self.saldopay=Label(self.framePagamento, text = 'Seu saldo é: ' ,font=self.font, bg = 'navajo White',pady=15)
        self.saldopay.grid(row=1, column = 0)
        self.saldoPay1 = Label(self.framePagamento, font = self.font, bg = 'navajo White', fg ='green',pady=15)
        self.saldoPay1['text'] = ('%10.2f' % dados_cliente[x][4])
        self.saldoPay1.grid(row=1, column=1)
        #
        self.qntpaga=Label(self.frameBotaopag,text = 'Valor Pagamento:' ,font = self.font1, bg = 'navajo White', fg = 'black')
        self.qntpaga.grid(row=1, column =0)
        self.paga = Entry(self.frameBotaopag)
        self.paga.grid(row=1, column=1)
        #
        self.tipo=Label(self.frameBotaopag,text = 'Tipo de pagamento (Ex: Conta d água)' ,font = self.font1, bg = 'navajo White', fg = 'black')
        self.tipo.grid(row = 2, column =0)
        self.tipo1=Entry(self.frameBotaopag)
        self.tipo1.grid(row=2,column = 1)

        self.botaoPagar = Button(self.frameBotaopag, text='Pagar', bg='green', fg='snow', width= 10)
        self.botaoPagar.bind('<Button-1>', self.pagar)
        self.botaoPagar.grid(row=5, column=1, pady= 15)


        pagamento1.title('Tela de pagamentos')
        pagamento1.wm_iconbitmap('icon.ico')
        pagamento1.configure(bg='navajo White')
        pagamento1.geometry('500x200')
        pagamento1.mainloop()

    def pagar (self,evento):
        x = self.loguin_usuario_acesso
        m = self.paga.get()
        m1 = float(dados_cliente[x][4])
        typo1 = self.tipo1.get()
        data = datetime.now()                             #RECEBENDO OS DADOS QUE SERÃO USADOS
        data1 = data.strftime("%d %b %Y às %H:%M:%S")
        dataR = date.today().strftime("%d/%m/%Y")
        #
        if self.valida_num(m) == True:
            m=float(m)
            porc=m*0.03
            m2=m+porc                                   #VERIFICAÇÕES

            if m1 >= m2:
                if len(self.tipo1.get()) !=0:
                    quest1=askquestion(title='Aviso!' ,message='Sera cobrada uma taxa de 3% para seu pagamento, prosseguir?')
                    if quest1  == 'yes':
                        aux_relatorio = [typo1, dataR, m2]
                        aux_extratos = [typo1, data1, m2]
                        extratos_cliente[x].append(aux_extratos)
                        relatorios_cliente[x].append(aux_relatorio)
                        m3 = m1 - m2
                        dados_cliente[x][4] = m3
                        self.saldoPay1['text'] = ('%10.2f' % dados_cliente[x][4])
                        self.salvar_arquivo()
                        self.salvar_arquivo1()
                        self.salvar_arquivo2()
                        showinfo(title='Êxito', message='Pagamento realizado com sucesso!')
                        print(relatorios_cliente)
                else:
                    showinfo(title='Falha', message='Digite do que é seu pagamento')
            else:
                showinfo(title='Falha', message='Você não possui essa quantidade para realizar pagamento')
        else:
            showinfo(title='Falha', message='Digite somente números no pagamento.')

    def juros_taxas (self,event):
        juros_taxas1= Tk()
        #
        self.framejuros_taxas=Frame(juros_taxas1, bg = 'snow')
        self.framejuros_taxas.grid()
        self.framejuros_taxas1=Frame(juros_taxas1, bg = 'snow')
        self.framejuros_taxas1.grid()
        #
        self.labeltitulo=Label(self.framejuros_taxas , text= 'Informações Juros e Taxas', bg = 'snow', fg = 'gray12',font = self.font,pady=15)
        self.labeltitulo.grid()
        #
        self.labeltaxa1=Label(self.framejuros_taxas1, text= 'Taxa Transferência mesmo banco: Isento', bg = 'snow', fg = 'green', font = self.font1)
        self.labeltaxa1.grid(row=1, column = 1)
        #
        self.labeltaxa2=Label(self.framejuros_taxas1, text= 'Taxa Transferência banco diferente: 7% do valor.',bg = 'snow', fg = 'green', font = self.font1)
        self.labeltaxa2.grid(row=2, column = 1)
        #
        self.labeltaxa3=Label(self.framejuros_taxas1, text = 'Taxa de pagamento: 3% do valor.', bg = 'snow', fg = 'green', font = self.font1)
        self.labeltaxa3.grid(row=3,column =1)
        #

        juros_taxas1.title('Informações Juros e Taxas')
        juros_taxas1.wm_iconbitmap('icon.ico')
        juros_taxas1.configure(bg='snow')
        juros_taxas1.geometry()
        juros_taxas1.mainloop()

    def saldos_extratos(self,event):
        saldos_extratos= Tk ()
        #
        self.unico=Frame(saldos_extratos, bg = 'snow')
        self.unico.pack()
        #
        self.titulox=Label(self.unico, bg = 'snow', fg = 'black', text = 'Informações', font = self.font,width=100, padx=10,height = 2)
        self.titulox.pack(side= TOP)
        #
        self.botaosaldo=Button(self.unico, bg = 'gray4', fg= 'snow', font= self.font2, text = 'Informações e Saldo',width=100, padx=10,height = 2)
        self.botaosaldo.bind('<Button-1>',self.inf_saldos)
        self.botaosaldo.pack(side = TOP)
        #
        self.botaoextrato=Button(self.unico, bg = 'gray4', fg = 'snow', font=self.font2, text = 'Extrato', width=100, padx=10,height = 2)
        self.botaoextrato.bind('<Button-1>', self.extratos)
        self.botaoextrato.pack(side= TOP)
        #
        self.botaolimpar=Button(self.unico,bg = 'gray4', fg = 'snow', font=self.font2, text = 'Limpar Extratos', width=100, padx=10,height = 2)
        self.botaolimpar.bind('<Button-1>', self.limpar)
        self.botaolimpar.pack(side=TOP)

        saldos_extratos.geometry('500x300')
        saldos_extratos.wm_iconbitmap('icon.ico')
        saldos_extratos.configure(bg='snow')
        saldos_extratos.title('Saldos e Extratos')
        saldos_extratos.mainloop()

    def limpar(self,event):
        x=self.loguin_usuario_acesso
        z=askquestion(title='Aviso', message='Seus extratos não serão recuperados, quer mesmo limpar?')
        if z =='yes':
            extratos_cliente[x]=[]
            self.salvar_arquivo()
            self.salvar_arquivo1()
            self.salvar_arquivo2()
            showinfo(title='Êxito', message='Tela limpada!')
    def limpar_relatorios(self,event):
        x = self.loguin_usuario_acesso
        z = askquestion(title='Aviso', message='Seus relatórios não serão recuperados, quer mesmo limpar?')
        if z == 'yes':
            relatorios_cliente[x] = []
            self.salvar_arquivo()
            self.salvar_arquivo1()
            self.salvar_arquivo2()
            showinfo(title='Êxito', message='Sucesso!!')

    def inf_saldos (self,event):
        inf_saldos = Tk()
        x = self.loguin_usuario_acesso
        #FRAMES
        self.frametitulo1=Frame(inf_saldos,bg='snow')
        self.frametitulo1.grid()
        self.frameinf=Frame(inf_saldos, bg='snow')
        self.frameinf.grid()
        #
        self.labeltitulo=Label(self.frametitulo1, text = 'Informações Conta', bg = 'snow', fg = 'black', font = self.font3)
        self.labeltitulo.grid(row=0, column = 1)
        #
        self.labelnome=Label(self.frameinf, text = 'Nome:' , bg = 'snow', fg = 'black', font=self.font3)
        self.labelnome.grid(row=0, column = 0)
        self.labelnome1 = Label(self.frameinf, bg='snow', fg='gray14', font=self.font)
        self.labelnome1['text']=dados_cliente[x][5]
        self.labelnome1.grid(row=0, column =1)
        #
        self.labelloguin = Label(self.frameinf, text='Login:', bg='snow', fg='black', font=self.font3)
        self.labelloguin.grid(row=1, column=0)
        self.labelloguin1 = Label(self.frameinf, bg='snow', fg='gray14', font=self.font)
        self.labelloguin1['text'] = x
        self.labelloguin1.grid(row=1, column=1)
        #
        self.labelbanco = Label(self.frameinf, text='Banco:', bg='snow', fg='black', font=self.font3)
        self.labelbanco.grid(row=2, column=0)
        self.labelbanco1 = Label(self.frameinf, bg='snow', fg='gray14', font=self.font)
        self.labelbanco1['text'] = dados_cliente[x][1]
        self.labelbanco1.grid(row=2, column=1)
        #
        self.labelnbanco = Label(self.frameinf, text='N° Conta:', bg='snow', fg='black', font=self.font3)
        self.labelnbanco.grid(row=3, column=0)
        self.labelnbanco1 = Label(self.frameinf, bg='snow', fg='gray14', font=self.font)
        self.labelnbanco1['text'] = dados_cliente[x][2]
        self.labelnbanco1.grid(row=3, column=1)
        #
        self.tipuconta=Label(self.frameinf, text = 'Tipo de conta:', bg = 'snow', fg= 'black', font = self.font3)
        self.tipuconta.grid(row=4,column =0)
        self.tipuconta1=Label(self.frameinf,bg='snow', fg = 'gray14', font=self.font)
        self.tipuconta1['text']=dados_cliente[x][6]
        self.tipuconta1.grid(row=4, column =1)
        #
        self.labelncpf = Label(self.frameinf, text='N° CPF:', bg='snow', fg='black', font=self.font3)
        self.labelncpf.grid(row=5, column=0)
        self.labelncpf1 = Label(self.frameinf, bg='snow', fg='gray14', font=self.font)
        self.labelncpf1['text'] = dados_cliente[x][3]
        self.labelncpf1.grid(row=5, column=1)
        #
        self.labelemail = Label(self.frameinf, text='E-Mail:', bg='snow', fg='black', font=self.font3)
        self.labelemail.grid(row=6, column=0)
        self.labelemail1 = Label(self.frameinf, bg='snow', fg='gray14', font=self.font)
        self.labelemail1['text'] = dados_cliente[x][7]
        self.labelemail1.grid(row=6, column=1)
        #
        self.labelsaldo = Label(self.frameinf, text='Saldo atual:', bg='snow', fg='black', font=self.font3)
        self.labelsaldo.grid(row=7, column=0)
        self.labelsaldo1 = Label(self.frameinf, bg='snow', fg='dark green', font=self.font)
        self.labelsaldo1['text'] = ('R$ %10.2f' % dados_cliente[x][4])
        self.labelsaldo1.grid(row=7, column=1)

        inf_saldos.title('Informações e Saldo')
        inf_saldos.wm_iconbitmap('icon.ico')
        inf_saldos.configure(bg='snow')
        inf_saldos.geometry("{0}x{1}+0+0".format(inf_saldos.winfo_screenwidth(), inf_saldos.winfo_screenheight()))
        inf_saldos.mainloop()

    def extratos (self,event):
        extratos1 = Tk()
        #SCROLLBAR LATERAL CONF
        vscrollbar = AutoScrollbar(extratos1)
        vscrollbar.grid(row=0, column=1, sticky=N + S)
        hscrollbar = AutoScrollbar(extratos1, orient=HORIZONTAL)
        hscrollbar.grid(row=1, column=0, sticky=E + W)
        #CANVAS, TELA DE ENVENTOS
        canvas = Canvas(extratos1,yscrollcommand=vscrollbar.set,xscrollcommand=hscrollbar.set, bg = 'snow')
        canvas.grid(row=0, column=0, sticky=N + S + E + W)
        #CONF
        vscrollbar.config(command=canvas.yview)
        hscrollbar.config(command=canvas.xview)
        extratos1.grid_rowconfigure(0, weight=1)
        extratos1.grid_columnconfigure(0, weight=1)
        #FRAME DA SCROLLBAR
        frame = Frame(canvas,bg= 'snow')
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(1, weight=1)
        #
        self.label1 = Label(frame, text='TIPO', font=self.font, bg='snow', fg='black', padx=20, pady=10)
        self.label1.grid(row=0, column=0)
        self.label2 = Label(frame, text='DATA', font=self.font, bg='snow', fg='black', padx=20, pady=10)
        self.label2.grid(row=0, column=1)
        self.label3 = Label(frame, text='VALOR', font=self.font, bg='snow', fg='black', padx=20, pady=10)
        self.label3.grid(row=0, column=2)
        #
        x = self.loguin_usuario_acesso
        a = len(extratos_cliente[x])
        for k in range(a):
            for i in range(3):
                self.q = Label(frame, font=self.font4, bg='snow', fg='medium blue')
                self.q['text'] = extratos_cliente[x][k][0]
                self.q.grid(row=k + 1, column=0)
                self.p = Label(frame, font=self.font4, bg='snow', fg='dodger blue')
                self.p['text'] = extratos_cliente[x][k][1]
                self.p.grid(row=k + 1, column=1)
                self.r = Label(frame, font=self.font4, bg='snow', fg='green3')
                self.r['text'] = ('%s   %10.2f'  % (self.dinheiro, extratos_cliente[x][k][2]))
                self.r.grid(row=k + 1, column=2)
        #
        canvas.create_window(0, 0, anchor=NW, window=frame)
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        #
        extratos1.title('Extratos')
        extratos1.wm_iconbitmap('icon.ico')
        extratos1.configure(bg='snow')
        extratos1.geometry("{0}x{1}+0+0".format(extratos1.winfo_screenwidth(), extratos1.winfo_screenheight()))
        extratos1.mainloop()

    def relatorios(self,event):
        root = Tk()
        self.frame=Frame(root)
        self.frame.pack()
        #
        self.b1=Button(self.frame, text = 'Relatório último dia', font=self.font1, bg='snow', fg='black', pady=10, width = 30)
        self.b1.bind('<Button-1>', self.relatorio_dia)
        self.b1.pack()
        self.b2=Button(self.frame, text = 'Relatório última semana', font=self.font1, bg='snow', fg='black', pady=10,width = 30)
        self.b2.bind('<Button-1>', self.relatorio_semana)
        self.b2.pack()
        self.b3 = Button(self.frame, text='Relatório último mês', font=self.font1, bg='snow', fg='black', pady=10,width=30)
        self.b3.bind('<Button-1>', self.relatorio_mes)
        self.b3.pack()
        self.b4 = Button(self.frame, text='Relatório último semestre', font=self.font1, bg='snow', fg='black', pady=10,width=30)
        self.b4.bind('<Button-1>', self.relatorio_semestre)
        self.b4.pack()
        self.b5 = Button(self.frame, text='Relatório último ano', font=self.font1, bg='snow', fg='black', pady=10,width=30)
        self.b5.bind('<Button-1>', self.relatorio_ano)
        self.b5.pack()
        self.b6 = Button(self.frame, text='Relatório personalizado', font=self.font1, bg='snow', fg='black', pady=10,width=30)
        self.b6.bind('<Button-1>', self.relatorio_personalizado)
        self.b6.pack()
        self.b7=Button(self.frame, text='Limpar Relatórios', font=self.font1, bg='snow', fg='black', pady=10,width=30)
        self.b7.bind('<Button-1>', self.limpar_relatorios)
        self.b7.pack()
        root.title('Relatórios')
        root.wm_iconbitmap('icon.ico')
        root.configure(bg='snow')
        root.geometry()
        root.mainloop()

    def relatorio_dia(self,event):
        extratos1 = Tk()

        # SCROLLBAR LATERAL CONF
        vscrollbar = AutoScrollbar(extratos1)
        vscrollbar.grid(row=0, column=1, sticky=N + S)
        hscrollbar = AutoScrollbar(extratos1, orient=HORIZONTAL)
        hscrollbar.grid(row=1, column=0, sticky=E + W)
        # CANVAS, TELA DE ENVENTOS
        canvas = Canvas(extratos1, yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set, bg='snow')
        canvas.grid(row=0, column=0, sticky=N + S + E + W)
        # CONF
        vscrollbar.config(command=canvas.yview)
        hscrollbar.config(command=canvas.xview)
        extratos1.grid_rowconfigure(0, weight=1)
        extratos1.grid_columnconfigure(0, weight=1)
        # FRAME DA SCROLLBAR
        frame = Frame(canvas, bg='snow')
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(1, weight=1)
        #
        self.label1 = Label(frame, text='TIPO', font=self.font, bg='snow', fg='black', padx=20, pady=10)
        self.label1.grid(row=0, column=0)
        self.label2 = Label(frame, text='DATA', font=self.font, bg='snow', fg='black', padx=20, pady=10)
        self.label2.grid(row=0, column=1)
        self.label3 = Label(frame, text='VALOR', font=self.font, bg='snow', fg='black', padx=20, pady=10)
        self.label3.grid(row=0, column=2)
        #
        x = self.loguin_usuario_acesso
        a = len(relatorios_cliente[x])
        #DATAS#
        hoje=date.today()
        ate = date.fromordinal(hoje.toordinal() - 1)
        aux=0
        lista=[]
        for k in range(a):
            diaAux, mesAux, anoAux = relatorios_cliente[x][k][1].split('/')
            dataAux = date(int(anoAux), int(mesAux), int(diaAux))
            if dataAux <= hoje and dataAux>= ate:
                self.q = Label(frame, font=self.font4, bg='snow', fg='medium blue')
                self.q['text'] = relatorios_cliente[x][k][0]
                self.q.grid(row=k + 1, column=0)
                self.p = Label(frame, font=self.font4, bg='snow', fg='dodger blue')
                self.p['text'] = relatorios_cliente[x][k][1]
                self.p.grid(row=k + 1, column=1)
                self.r = Label(frame, font=self.font4, bg='snow', fg='green3')
                self.r['text'] = ('%s   %10.2f' % (self.dinheiro, relatorios_cliente[x][k][2]))
                self.r.grid(row=k + 1, column=2)
            aux=k+2
        self.butaun=Button(frame,font=self.font4,bg = 'green', fg = 'white', text = 'Enviar análise via E-mail')
        self.butaun.bind('<Button-1>', self.enviar_email_diario)
        self.butaun.grid(row= aux, column = 1,pady = 15)

        #
        canvas.create_window(0, 0, anchor=NW, window=frame)
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        #
        extratos1.title('Relatório Diário')
        extratos1.wm_iconbitmap('icon.ico')
        extratos1.configure(bg='snow')
        extratos1.geometry("{0}x{1}+0+0".format(extratos1.winfo_screenwidth(), extratos1.winfo_screenheight()))
        extratos1.mainloop()

    def relatorio_semana(self,event):
        extratos1 = Tk()
        # SCROLLBAR LATERAL CONF
        vscrollbar = AutoScrollbar(extratos1)
        vscrollbar.grid(row=0, column=1, sticky=N + S)
        hscrollbar = AutoScrollbar(extratos1, orient=HORIZONTAL)
        hscrollbar.grid(row=1, column=0, sticky=E + W)
        # CANVAS, TELA DE ENVENTOS
        canvas = Canvas(extratos1, yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set, bg='snow')
        canvas.grid(row=0, column=0, sticky=N + S + E + W)
        # CONF
        vscrollbar.config(command=canvas.yview)
        hscrollbar.config(command=canvas.xview)
        extratos1.grid_rowconfigure(0, weight=1)
        extratos1.grid_columnconfigure(0, weight=1)
        # FRAME DA SCROLLBAR
        frame = Frame(canvas, bg='snow')
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(1, weight=1)
        #
        self.label1 = Label(frame, text='TIPO', font=self.font, bg='snow', fg='black', padx=20, pady=10)
        self.label1.grid(row=0, column=0)
        self.label2 = Label(frame, text='DATA', font=self.font, bg='snow', fg='black', padx=20, pady=10)
        self.label2.grid(row=0, column=1)
        self.label3 = Label(frame, text='VALOR', font=self.font, bg='snow', fg='black', padx=20, pady=10)
        self.label3.grid(row=0, column=2)
        #
        x = self.loguin_usuario_acesso
        a = len(relatorios_cliente[x])
        #DATAS#
        hoje=date.today()
        ate = date.fromordinal(hoje.toordinal() - 7)

        for k in range(a):
            diaAux, mesAux, anoAux = relatorios_cliente[x][k][1].split('/')
            dataAux = date(int(anoAux), int(mesAux), int(diaAux))
            for i in range(3):
                if dataAux <= hoje and dataAux>= ate:
                    self.q = Label(frame, font=self.font4, bg='snow', fg='medium blue')
                    self.q['text'] = relatorios_cliente[x][k][0]
                    self.q.grid(row=k + 1, column=0)
                    self.p = Label(frame, font=self.font4, bg='snow', fg='dodger blue')
                    self.p['text'] = relatorios_cliente[x][k][1]
                    self.p.grid(row=k + 1, column=1)
                    self.r = Label(frame, font=self.font4, bg='snow', fg='green3')
                    self.r['text'] = ('%s   %10.2f' % (self.dinheiro, relatorios_cliente[x][k][2]))
                    self.r.grid(row=k + 1, column=2)
                aux = k + 2
        self.butaun = Button(frame, font=self.font4, bg='green', fg='white', text='Enviar análise via E-mail')
        self.butaun.bind('<Button-1>', self.enviar_email_semanal)
        self.butaun.grid(row=aux, column=1, pady=15)
        #
        canvas.create_window(0, 0, anchor=NW, window=frame)
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        #
        extratos1.title('Extratos')
        extratos1.wm_iconbitmap('icon.ico')
        extratos1.configure(bg='snow')
        extratos1.geometry("{0}x{1}+0+0".format(extratos1.winfo_screenwidth(), extratos1.winfo_screenheight()))
        extratos1.mainloop()

    def relatorio_mes(self,event):
        extratos1 = Tk()
        # SCROLLBAR LATERAL CONF
        vscrollbar = AutoScrollbar(extratos1)
        vscrollbar.grid(row=0, column=1, sticky=N + S)
        hscrollbar = AutoScrollbar(extratos1, orient=HORIZONTAL)
        hscrollbar.grid(row=1, column=0, sticky=E + W)
        # CANVAS, TELA DE ENVENTOS
        canvas = Canvas(extratos1, yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set, bg='snow')
        canvas.grid(row=0, column=0, sticky=N + S + E + W)
        # CONF
        vscrollbar.config(command=canvas.yview)
        hscrollbar.config(command=canvas.xview)
        extratos1.grid_rowconfigure(0, weight=1)
        extratos1.grid_columnconfigure(0, weight=1)
        # FRAME DA SCROLLBAR
        frame = Frame(canvas, bg='snow')
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(1, weight=1)
        #
        self.label1 = Label(frame, text='TIPO', font=self.font, bg='snow', fg='black', padx=20, pady=10)
        self.label1.grid(row=0, column=0)
        self.label2 = Label(frame, text='DATA', font=self.font, bg='snow', fg='black', padx=20, pady=10)
        self.label2.grid(row=0, column=1)
        self.label3 = Label(frame, text='VALOR', font=self.font, bg='snow', fg='black', padx=20, pady=10)
        self.label3.grid(row=0, column=2)
        #
        x = self.loguin_usuario_acesso
        a = len(relatorios_cliente[x])
        #DATAS#
        hoje=date.today()
        ate = date.fromordinal(hoje.toordinal() - 31)

        for k in range(a):
            diaAux, mesAux, anoAux = relatorios_cliente[x][k][1].split('/')
            dataAux = date(int(anoAux), int(mesAux), int(diaAux))
            for i in range(3):
                if dataAux <= hoje and dataAux>= ate:
                    self.q = Label(frame, font=self.font4, bg='snow', fg='medium blue')
                    self.q['text'] = relatorios_cliente[x][k][0]
                    self.q.grid(row=k + 1, column=0)
                    self.p = Label(frame, font=self.font4, bg='snow', fg='dodger blue')
                    self.p['text'] = relatorios_cliente[x][k][1]
                    self.p.grid(row=k + 1, column=1)
                    self.r = Label(frame, font=self.font4, bg='snow', fg='green3')
                    self.r['text'] = ('%s   %10.2f' % (self.dinheiro, relatorios_cliente[x][k][2]))
                    self.r.grid(row=k + 1, column=2)
                aux = k + 2
        self.butaun = Button(frame, font=self.font4, bg='green', fg='white', text='Enviar análise via E-mail')
        self.butaun.bind('<Button-1>', self.enviar_email_mensal)
        self.butaun.grid(row=aux, column=1, pady=15)
        #
        canvas.create_window(0, 0, anchor=NW, window=frame)
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        #
        extratos1.title('Extratos')
        extratos1.wm_iconbitmap('icon.ico')
        extratos1.configure(bg='snow')
        extratos1.geometry("{0}x{1}+0+0".format(extratos1.winfo_screenwidth(), extratos1.winfo_screenheight()))
        extratos1.mainloop()

    def relatorio_semestre(self,event):
        extratos1 = Tk()
        # SCROLLBAR LATERAL CONF
        vscrollbar = AutoScrollbar(extratos1)
        vscrollbar.grid(row=0, column=1, sticky=N + S)
        hscrollbar = AutoScrollbar(extratos1, orient=HORIZONTAL)
        hscrollbar.grid(row=1, column=0, sticky=E + W)
        # CANVAS, TELA DE ENVENTOS
        canvas = Canvas(extratos1, yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set, bg='snow')
        canvas.grid(row=0, column=0, sticky=N + S + E + W)
        # CONF
        vscrollbar.config(command=canvas.yview)
        hscrollbar.config(command=canvas.xview)
        extratos1.grid_rowconfigure(0, weight=1)
        extratos1.grid_columnconfigure(0, weight=1)
        # FRAME DA SCROLLBAR
        frame = Frame(canvas, bg='snow')
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(1, weight=1)
        #
        self.label1 = Label(frame, text='TIPO', font=self.font, bg='snow', fg='black', padx=20, pady=10)
        self.label1.grid(row=0, column=0)
        self.label2 = Label(frame, text='DATA', font=self.font, bg='snow', fg='black', padx=20, pady=10)
        self.label2.grid(row=0, column=1)
        self.label3 = Label(frame, text='VALOR', font=self.font, bg='snow', fg='black', padx=20, pady=10)
        self.label3.grid(row=0, column=2)
        #
        x = self.loguin_usuario_acesso
        a = len(relatorios_cliente[x])
        #DATAS#
        hoje=date.today()
        ate = date.fromordinal(hoje.toordinal() - 182)

        for k in range(a):
            diaAux, mesAux, anoAux = relatorios_cliente[x][k][1].split('/')
            dataAux = date(int(anoAux), int(mesAux), int(diaAux))
            for i in range(3):
                if dataAux <= hoje and dataAux>= ate:
                    self.q = Label(frame, font=self.font4, bg='snow', fg='medium blue')
                    self.q['text'] = relatorios_cliente[x][k][0]
                    self.q.grid(row=k + 1, column=0)
                    self.p = Label(frame, font=self.font4, bg='snow', fg='dodger blue')
                    self.p['text'] = relatorios_cliente[x][k][1]
                    self.p.grid(row=k + 1, column=1)
                    self.r = Label(frame, font=self.font4, bg='snow', fg='green3')
                    self.r['text'] = ('%s   %10.2f' % (self.dinheiro, relatorios_cliente[x][k][2]))
                    self.r.grid(row=k + 1, column=2)
                aux = k + 2
        self.butaun = Button(frame, font=self.font4, bg='green', fg='white', text='Enviar análise via E-mail')
        self.butaun.bind('<Button-1>', self.enviar_email_semestral)
        self.butaun.grid(row=aux, column=1, pady=15)
        #
        canvas.create_window(0, 0, anchor=NW, window=frame)
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        #
        extratos1.title('Extratos')
        extratos1.wm_iconbitmap('icon.ico')
        extratos1.configure(bg='snow')
        extratos1.geometry("{0}x{1}+0+0".format(extratos1.winfo_screenwidth(), extratos1.winfo_screenheight()))
        extratos1.mainloop()

    def relatorio_ano(self,event):
        extratos1 = Tk()
        # SCROLLBAR LATERAL CONF
        vscrollbar = AutoScrollbar(extratos1)
        vscrollbar.grid(row=0, column=1, sticky=N + S)
        hscrollbar = AutoScrollbar(extratos1, orient=HORIZONTAL)
        hscrollbar.grid(row=1, column=0, sticky=E + W)
        # CANVAS, TELA DE ENVENTOS
        canvas = Canvas(extratos1, yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set, bg='snow')
        canvas.grid(row=0, column=0, sticky=N + S + E + W)
        # CONF
        vscrollbar.config(command=canvas.yview)
        hscrollbar.config(command=canvas.xview)
        extratos1.grid_rowconfigure(0, weight=1)
        extratos1.grid_columnconfigure(0, weight=1)
        # FRAME DA SCROLLBAR
        frame = Frame(canvas, bg='snow')
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(1, weight=1)
        #
        self.label1 = Label(frame, text='TIPO', font=self.font, bg='snow', fg='black', padx=20, pady=10)
        self.label1.grid(row=0, column=0)
        self.label2 = Label(frame, text='DATA', font=self.font, bg='snow', fg='black', padx=20, pady=10)
        self.label2.grid(row=0, column=1)
        self.label3 = Label(frame, text='VALOR', font=self.font, bg='snow', fg='black', padx=20, pady=10)
        self.label3.grid(row=0, column=2)
        #
        x = self.loguin_usuario_acesso
        a = len(relatorios_cliente[x])
        #DATAS#
        hoje=date.today()
        ate = date.fromordinal(hoje.toordinal() - 365)

        for k in range(a):
            diaAux, mesAux, anoAux = relatorios_cliente[x][k][1].split('/')
            dataAux = date(int(anoAux), int(mesAux), int(diaAux))
            for i in range(3):
                if dataAux <= hoje and dataAux>= ate:
                    self.q = Label(frame, font=self.font4, bg='snow', fg='medium blue')
                    self.q['text'] = relatorios_cliente[x][k][0]
                    self.q.grid(row=k + 1, column=0)
                    self.p = Label(frame, font=self.font4, bg='snow', fg='dodger blue')
                    self.p['text'] = relatorios_cliente[x][k][1]
                    self.p.grid(row=k + 1, column=1)
                    self.r = Label(frame, font=self.font4, bg='snow', fg='green3')
                    self.r['text'] = ('%s   %10.2f' % (self.dinheiro, relatorios_cliente[x][k][2]))
                    self.r.grid(row=k + 1, column=2)
                aux = k + 2
        self.butaun = Button(frame, font=self.font4, bg='green', fg='white', text='Enviar análise via E-mail')
        self.butaun.bind('<Button-1>', self.enviar_email_anual)
        self.butaun.grid(row=aux, column=1, pady=15)
        #
        canvas.create_window(0, 0, anchor=NW, window=frame)
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        #
        extratos1.title('Extratos')
        extratos1.wm_iconbitmap('icon.ico')
        extratos1.configure(bg='snow')
        extratos1.geometry("{0}x{1}+0+0".format(extratos1.winfo_screenwidth(), extratos1.winfo_screenheight()))
        extratos1.mainloop()

    def relatorio_personalizado (self,event):
        relatorios1 = Tk()
        valor1=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31)
        valor2=(1,2,3,4,5,6,7,8,9,10,11,12)
        valor3=(2017,2018,2019,2020,2021,2022,2023,2024,2025)
        self.frame11=Frame(relatorios1, bg='snow')
        self.frame11.grid()
        self.frame22=Frame(relatorios1, bg = 'snow')
        self.frame22.grid()
        self.frame33=Frame(relatorios1,bg='snow')
        self.frame33.grid()
        #
        self.labelX=Label(self.frame11, text= 'De' , bg= 'snow', fg = 'black', font = self.font1)
        self.labelX.grid(row=0, column =0)
        self.labelY=Label(self.frame11, text= 'Até' , bg= 'snow', fg = 'black', font = self.font1)
        self.labelY.grid(row= 0 , column = 4)
        #
        self.a1=Spinbox(self.frame11, value= (valor1), state='readonly')
        self.a1.grid(row=0,column = 1)
        self.a2 = Spinbox(self.frame11, value= (valor2), state='readonly')
        self.a2.grid(row=0, column=2)
        self.a3 = Spinbox(self.frame11, value= (2017), state='readonly')
        self.a3.grid(row=0, column=3)
        #
        self.b1 = Spinbox(self.frame11, value= (valor1), state='readonly')
        self.b1.grid(row=0, column=5)
        self.b2 = Spinbox(self.frame11, value= (valor2), state='readonly')
        self.b2.grid(row=0, column=6)
        self.b3 = Spinbox(self.frame11, value= (valor3), state='readonly')
        self.b3.grid(row=0, column=7)
        #
        self.pesqx=Button(self.frame11, text = 'Gerar', fg= 'snow', bg = 'green', font=self.font1)
        self.pesqx.bind('<Button-1>', self.gerar)
        self.pesqx.grid(row = 1, column = 4)
        #
        self.labe21 = Label(self.frame22, text='TIPO', font=self.font, bg='snow', fg='black', padx=20, pady=10)
        self.labe21.grid(row=0, column=0)
        self.labe22 = Label(self.frame22, text='DATA', font=self.font, bg='snow', fg='black', padx=20, pady=10)
        self.labe22.grid(row=0, column=1)
        self.labe23 = Label(self.frame22, text='VALOR', font=self.font, bg='snow', fg='black', padx=20, pady=10)
        self.labe23.grid(row=0, column=2)
        #
        self.q = Label(self.frame22, font=self.font4, bg='snow', fg='medium blue')
        self.p = Label(self.frame22, font=self.font4, bg='snow', fg='dodger blue')
        self.r = Label(self.frame22, font=self.font4, bg='snow', fg='green3')

        relatorios1.title('Relatórios')
        relatorios1.wm_iconbitmap('icon.ico')
        relatorios1.configure(bg='snow')
        relatorios1.geometry("{0}x{1}+0+0".format(relatorios1.winfo_screenwidth(), relatorios1.winfo_screenheight()))
        relatorios1.mainloop()

    def gerar (self,event):
        dia_de=int(self.a1.get())
        dia_ate=int(self.b1.get())
        mes_de=int(self.a2.get())
        mes_ate=int(self.b2.get())
        ano_de=int(self.a3.get())
        ano_ate=int(self.b3.get())
        x = self.loguin_usuario_acesso
        a=len(relatorios_cliente[x])
        try:
            if self.valida_data(dia_de, mes_de, ano_de, dia_ate, mes_ate, ano_ate) == True:
                data1=datetime(ano_de,mes_de,dia_de)
                data2=datetime(ano_ate, mes_ate,dia_ate)
                existe = False
                for k in range(a):
                    diaAux, mesAux, anoAux = relatorios_cliente[x][k][1].split('/')
                    dataAux=datetime(int(anoAux), int(mesAux),int(diaAux))
                    if data1 <= dataAux and dataAux <= data2:
                        self.q = Label(self.frame22, font=self.font4, bg='snow', fg='medium blue')
                        self.q['text'] = relatorios_cliente[x][k][0]
                        self.q.grid(row=k + 1, column=0)
                        self.p = Label(self.frame22, font=self.font4, bg='snow', fg='medium blue')
                        self.p['text'] = relatorios_cliente[x][k][1]
                        self.p.grid(row=k + 1, column=1)
                        self.r = Label(self.frame22, font=self.font4, bg='snow', fg='green3')
                        self.r['text'] = ('%s   %10.2f' % (self.dinheiro, relatorios_cliente[x][k][2]))
                        self.r.grid(row=k + 1, column=2)
                        existe=True
                if not existe:
                    showinfo(title='Falha', message='Não existe registros entre essas datas')
            else:
                showinfo(title='Falha', message='Você escolheu datas inválidas!')
        except:
            showinfo(title='Falha', message='Você escolheu datas inválidas!')

    def inf_gerais(self,event):
        inf1= Tk()
        #
        self.frame=Frame(inf1,bg='snow')
        self.frame.grid()
        self.frame1=Frame(inf1,bg='snow')
        self.frame1.grid()
        #
        self.label=Label(self.frame,text='Informações Gerais', bg = 'snow', fg= 'black', font = self.font)
        self.label.grid()
        #
        self.label2=Label(self.frame1, text = 'Programa desenvolvido por: @MateusMedeiros, @LaioAlencar.', bg = 'snow', fg = 'black', font = self.font4,pady=10)
        self.label2.grid(row=0, column =0)
        #
        self.label3 = Label(self.frame1, text='Utilize pontos (.) como separador de reais/centavos em suas transações!', bg='snow', fg='black', font=self.font4, pady=10)
        self.label3.grid(row=1, column=0)
        #
        self.label4 = Label(self.frame1, text='E-Mail contato: mateusmedeiros252525@hotmail.com / laioand98@gmail.com', bg='snow',fg='black', font=self.font4, pady=10)
        self.label4.grid(row=2, column=0)
        #
        self.label5 = Label(self.frame1, text='Programa fictício sem ligação com nenhum banco citado.', bg='snow',fg='black', font=self.font4, pady=10)
        self.label5.grid(row=3, column=0)
        #
        self.label6=Label(self.frame1, text='Problemas com saque podem ocorrer devido à porcentagens de taxas, utilize a opção sacar tudo nesses casos.', bg='snow',fg='black', font=self.font4, pady=10)
        self.label6.grid(row=4, column=0)
        #
        inf1.title('Informações Gerais')
        inf1.wm_iconbitmap('icon.ico')
        inf1.configure(bg='snow')
        inf1.geometry()
        inf1.mainloop()

    def valida_num(self, x):
        try:
            x= float(x)
            if x / 1 == x:
                return True
            else:
                return False
        except:
            return False

    def valida_data(self,dia,mes,ano,dia1,mes1,ano1):
        try:
            if mes==1 or mes==3 or mes==5 or mes==7 or mes==8 or mes==10  or mes==12:
                if dia <=31:
                    if mes1 == 1 or mes1 == 3 or mes1 == 5 or mes1 == 7 or mes1 == 8 or mes1 == 10 or mes1 == 12:
                        if dia1 <=31:
                            if ano == ano1:
                                if mes == mes1:
                                    if dia<=dia1:
                                        return True
                                    else:
                                        return False
                                elif mes<mes1:
                                    return True
                                else:
                                    return False
                            elif ano<ano1:
                                return True
                    elif mes1==2:
                        if dia<=28:
                            return True
                        else:
                            return False
                    else:
                        if dia <=30:
                            return True
                        else:
                            return False
            elif mes ==2:
                if dia <=28:
                    return True
                else:
                    return False
            else:
                if dia <=30:
                    return True
                else:
                    return False
        except:
            return False

    def valida_cpf(self,n):

        if n.isdigit():
            mult2 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
            mult = [10, 9, 8, 7, 6, 5, 4, 3, 2]
            n=list(n)
            soma = 0
            for i in range(len(n)):
                n[i] = int(n[i])
            for i in range(len(mult)):
                soma += n[i] * mult[i]
            d1 = 11 - (soma % 11)
            if d1 == 10:
                d1 = 0

            soma2 = 0
            for i in range(len(n)):
                n[i] = int(n[i])
            for i in range(len(mult2)):
                soma2 += n[i] * mult2[i]
            d2 = 11 - (soma2 % 11)
            if d2 == 10:
                d2 = 0

            if d1 == n[9] and d2 == n[10]:
                return True
            else:
                return False
        else:
            return False

principal = Tk()
banco(principal)
principal.wm_iconbitmap('icon.ico')
principal.configure(background='#500')
principal.title('PyBanking')
principal.geometry("{0}x{1}+0+0".format(principal.winfo_screenwidth(), principal.winfo_screenheight()))
principal.mainloop()

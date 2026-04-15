import sys
import subprocess

def install_package(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Instalando {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Lista de dependências necessárias
required_packages = ['reportlab', 'Pillow', 'pandas', 'openpyxl']

for package in required_packages:
    install_package(package)

# Agora importe normalmente
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.graphics.shapes import Drawing, Line
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import openpyxl
import os
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


# =============================================================================
# BANCO DE DADOS PARA MATRÍCULAS
# =============================================================================

def criar_banco_dados():
    conn = sqlite3.connect('matriculas.db')
    cursor = conn.cursor()

    # Tabela da Instituição
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS instituicao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            endereco TEXT NOT NULL,
            mantenedora TEXT NOT NULL,
            cnpj TEXT UNIQUE NOT NULL
        )
    ''')

    # Tabela de Alunos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            foto_path TEXT,
            numero_matricula TEXT UNIQUE NOT NULL,
            nome_completo TEXT NOT NULL,
            data_nascimento DATE NOT NULL,
            certidao_numero TEXT,
            certidao_livro TEXT,
            certidao_folha TEXT,
            certidao_data_expedicao DATE,
            certidao_cidade TEXT,
            certidao_uf TEXT,
            certidao_cartorio TEXT,
            rg_uf TEXT,
            rg_data_expedicao DATE,
            cpf TEXT UNIQUE,
            sexo TEXT,
            cor_raca TEXT,
            endereco_bairro TEXT,
            endereco_cidade TEXT,
            endereco_estado TEXT,
            endereco_cep TEXT,
            curso TEXT,
            ano_serie TEXT,
            data_ingresso DATE,
            necessidades_especiais TEXT,
            alergias TEXT,
            convenio_medico TEXT,
            colegio_anterior TEXT,
            email TEXT,
            celular TEXT,
            operadora TEXT,
            nome_mae TEXT
        )
    ''')

    # Tabela de Responsáveis Financeiros
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responsaveis_financeiros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER,
            nome_completo TEXT NOT NULL,
            estado_civil TEXT,
            guarda_menor TEXT,
            data_nascimento DATE,
            rg_uf TEXT,
            rg_data_expedicao DATE,
            cpf TEXT,
            parentesco_aluno TEXT,
            endereco_cobranca TEXT,
            endereco_residencial TEXT,
            bairro_residencial TEXT,
            cidade_residencial TEXT,
            estado_residencial TEXT,
            cep_residencial TEXT,
            telefone_residencial TEXT,
            endereco_comercial TEXT,
            bairro_comercial TEXT,
            cidade_comercial TEXT,
            estado_comercial TEXT,
            cep_comercial TEXT,
            telefone_comercial TEXT,
            email TEXT,
            celular TEXT,
            profissao TEXT,
            FOREIGN KEY (aluno_id) REFERENCES alunos (id)
        )
    ''')

    # Tabela de Responsáveis Pedagógicos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responsaveis_pedagogicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno_id INTEGER,
            nome_completo TEXT NOT NULL,
            parentesco_aluno TEXT,
            rg_uf TEXT,
            rg_data_expedicao DATE,
            cpf TEXT,
            data_nascimento DATE,
            tipo_endereco TEXT,
            endereco_completo TEXT,
            bairro TEXT,
            cidade TEXT,
            estado TEXT,
            cep TEXT,
            email TEXT,
            celular TEXT,
            operadora TEXT,
            FOREIGN KEY (aluno_id) REFERENCES alunos (id)
        )
    ''')

    conn.commit()
    conn.close()


# Executar criação do banco
criar_banco_dados()

import sys
import subprocess

def install_package(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Instalando {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Lista de dependências necessárias
required_packages = ['reportlab', 'Pillow', 'pandas', 'openpyxl']

for package in required_packages:
    install_package(package)

# Agora importe normalmente
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.graphics.shapes import Drawing, Line
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import openpyxl
# ... continue com o resto do seu código de 5146 linhas

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import sqlite3
from datetime import datetime, date, timedelta
import json
import os
import csv
from tkinter import filedialog
import hashlib
import shutil
import webbrowser
from PIL import Image, ImageTk
import calendar
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import time
import re


class ModernButton(tk.Button):
    def __init__(self, parent, text, command=None, color='#0046AD', **kwargs):
        super().__init__(parent, text=text, command=command, **kwargs)
        self.configure(
            bg=color,
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            border=0,
            padx=20,
            pady=10,
            cursor='hand2',
            bd=0,
            highlightthickness=0
        )
        self.original_color = color

        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)

    def _on_enter(self, event):
        if self['state'] != 'disabled':
            self.configure(bg='#FFCC00', fg='#0046AD')

    def _on_leave(self, event):
        if self['state'] != 'disabled':
            self.configure(bg=self.original_color, fg='white')


class CardFrame(tk.Frame):
    def __init__(self, parent, title, value, icon, color='#0046AD', **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg='white', relief='flat', bd=1, highlightbackground='#e0e0e0',
                       highlightthickness=1, padx=15, pady=15)

        # Icon e título
        top_frame = tk.Frame(self, bg='white')
        top_frame.pack(fill='x', pady=(0, 10))

        tk.Label(top_frame, text=icon, font=('Arial', 24),
                 bg='white', fg=color).pack(side='left')

        tk.Label(top_frame, text=title, font=('Arial', 12, 'bold'),
                 bg='white', fg='#666666').pack(side='right')

        # Valor
        tk.Label(self, text=str(value), font=('Arial', 28, 'bold'),
                 bg='white', fg=color).pack(anchor='w')

        # Barra colorida na parte inferior
        bar_frame = tk.Frame(self, height=4, bg=color)
        bar_frame.pack(fill='x', side='bottom', pady=(10, 0))
        bar_frame.pack_propagate(False)


class SistemaGestaoEscolar:
    def __init__(self, root):
        self.root = root
        self.root.title("Externato Colégio Objetivo - Sistema de Gestão Escolar Integrado")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f8f9fa')
        self.root.state('zoomed')

        # Configurar ícone
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass

        # Configurar estilo moderno
        self.setup_styles()

        # Configurações do sistema
        self.config_file = 'config.json'
        self.carregar_configuracoes()

        # Centralizar janela
        self.center_window()

        # Criar banco de dados
        self.criar_banco_dados()

        # Tela de login
        if not self.fazer_login():
            self.root.destroy()
            return

        # Configurar interface principal
        self.setup_interface()

        # Carregar dados iniciais
        self.carregar_dashboard()

        # Iniciar serviços em background
        self.iniciar_servicos_background()

    def setup_styles(self):
        """Configura os estilos visuais do sistema"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configurar Treeview
        style.configure('Custom.Treeview',
                        background='white',
                        foreground='black',
                        fieldbackground='white',
                        borderwidth=0,
                        font=('Arial', 10))

        style.configure('Custom.Treeview.Heading',
                        background='#0046AD',
                        foreground='white',
                        relief='flat',
                        borderwidth=0,
                        font=('Arial', 11, 'bold'))

        style.map('Custom.Treeview.Heading',
                  background=[('active', '#0066CC')])

        # CORREÇÃO: Seleção persistente na Treeview
        style.map('Custom.Treeview',
                  background=[('selected', '#FFCC00')],
                  foreground=[('selected', '#0046AD')])

        # Configurar Notebook (abas)
        style.configure('Custom.TNotebook',
                        background='#f8f9fa',
                        borderwidth=0)

        style.configure('Custom.TNotebook.Tab',
                        background='#e9ecef',
                        foreground='#666666',
                        padding=[20, 10],
                        font=('Arial', 10, 'bold'))

        style.map('Custom.TNotebook.Tab',
                  background=[('selected', '#0046AD')],
                  foreground=[('selected', 'white')])

    def carregar_configuracoes(self):
        """Carrega as configurações do sistema"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                # Configurações padrão
                self.config = {
                    'escola': {
                        'nome': 'Externato Colégio Objetivo',
                        'endereco': 'Rua Principal, 123 - Centro',
                        'telefone': '(11) 9999-9999',
                        'email': 'contato@externato.com.br',
                        'cnpj': '12.345.678/0001-90',
                        'diretor': 'Dr. João Silva',
                        'coordenador_pedagogico': 'Maria Santos'
                    },
                    'ano_letivo': '2024',
                    'media_aprovacao': 6.0,
                    'dias_letivos': 200,
                    'backup_automatico': True,
                    'notificacoes_email': False,
                    'limite_faltas': 25
                }
                self.salvar_configuracoes()
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
            self.config = {}

    def salvar_configuracoes(self):
        """Salva as configurações do sistema"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {str(e)}")

    def fazer_login(self):
        """Tela de login do sistema com tema Objetivo"""
        login_window = tk.Toplevel(self.root)
        login_window.title("Login - Externato Colégio Objetivo")
        login_window.geometry("500x500")
        login_window.configure(bg='#0046AD')
        login_window.transient(self.root)
        login_window.grab_set()
        login_window.resizable(False, False)

        # Centralizar
        self.center_dialog(login_window)

        # Frame principal do login
        main_frame = tk.Frame(login_window, bg='white', padx=40, pady=40)
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)

        # Logo e título
        logo_frame = tk.Frame(main_frame, bg='white')
        logo_frame.pack(pady=(0, 40))

        # Logo Objetivo
        logo_text = tk.Frame(logo_frame, bg='white')
        logo_text.pack()

        tk.Label(logo_text, text="●", font=('Arial', 48),
                 fg='#0046AD', bg='white').pack(side=tk.LEFT)

        tk.Label(logo_text, text="OBJETIVO", font=('Arial', 32, 'bold'),
                 fg='#0046AD', bg='white').pack(side=tk.LEFT, padx=10)

        tk.Label(logo_frame, text="Externato Colégio", font=('Arial', 16),
                 fg='#FFCC00', bg='white').pack()
        tk.Label(logo_frame, text="Sistema de Gestão Escolar Integrado", font=('Arial', 12),
                 fg='#666666', bg='white').pack()

        # Campos de login
        form_frame = tk.Frame(main_frame, bg='white')
        form_frame.pack(fill='x', pady=30)

        # Usuário
        tk.Label(form_frame, text="Usuário:", font=('Arial', 12, 'bold'),
                 bg='white', fg='#0046AD').grid(row=0, column=0, sticky='w', pady=15)
        usuario_entry = tk.Entry(form_frame, font=('Arial', 12), width=25,
                                 relief='solid', bd=2, highlightthickness=1,
                                 highlightcolor='#0046AD', bg='#f8f9fa', fg='#333333')
        usuario_entry.grid(row=0, column=1, pady=15, padx=15, sticky='ew')
        usuario_entry.focus()

        # Senha
        tk.Label(form_frame, text="Senha:", font=('Arial', 12, 'bold'),
                 bg='white', fg='#0046AD').grid(row=1, column=0, sticky='w', pady=15)
        senha_entry = tk.Entry(form_frame, font=('Arial', 12), width=25, show='*',
                               relief='solid', bd=2, highlightthickness=1,
                               highlightcolor='#0046AD', bg='#f8f9fa', fg='#333333')
        senha_entry.grid(row=1, column=1, pady=15, padx=15, sticky='ew')

        form_frame.columnconfigure(1, weight=1)

        # Botões
        btn_frame = tk.Frame(main_frame, bg='white')
        btn_frame.pack(pady=30)

        resultado_login = {'sucesso': False}

        def verificar_login():
            usuario = usuario_entry.get().strip()
            senha = senha_entry.get()

            if not usuario or not senha:
                messagebox.showwarning("Aviso", "Preencha todos os campos!")
                return

            # Verificar no banco de dados
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()
            self.cursor.execute(
                "SELECT u.id, u.nome, u.nivel, p.id FROM usuarios u LEFT JOIN professores p ON u.nome = p.nome WHERE u.usuario = ? AND u.senha = ? AND u.ativo = 1",
                (usuario, senha_hash)
            )
            usuario_data = self.cursor.fetchone()

            if usuario_data:
                self.usuario_id, self.usuario_nome, self.usuario_nivel, self.professor_id = usuario_data
                resultado_login['sucesso'] = True
                login_window.destroy()
            else:
                messagebox.showerror("Erro", "Usuário ou senha inválidos!")
                senha_entry.delete(0, tk.END)

        def sair():
            self.root.destroy()

        # Enter para logar
        def on_enter(event):
            verificar_login()

        usuario_entry.bind('<Return>', on_enter)
        senha_entry.bind('<Return>', on_enter)

        ModernButton(btn_frame, text="🎯 Entrar", command=verificar_login,
                     color='#0046AD', font=('Arial', 12)).pack(side=tk.LEFT, padx=15)

        ModernButton(btn_frame, text="🚪 Sair", command=sair,
                     color='#666666', font=('Arial', 12)).pack(side=tk.LEFT, padx=15)

        # Dicas de login
        dica_frame = tk.Frame(main_frame, bg='white')
        dica_frame.pack(pady=20)

        tk.Label(dica_frame, text="💡 Dica: Use 'admin' / 'admin123' ou 'professor' / 'prof123'",
                 font=('Arial', 10), bg='white', fg='#666666').pack()

        # Focar na janela de login
        self.root.wait_window(login_window)

        return resultado_login['sucesso']

    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def center_dialog(self, dialog):
        """Centraliza uma dialog na tela"""
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')

    def criar_banco_dados(self):
        """Cria o banco de dados SQLite com tabelas necessárias"""
        self.conn = sqlite3.connect('externato.db', check_same_thread=False)
        self.cursor = self.conn.cursor()

        # Tabela de Usuários
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                nome TEXT NOT NULL,
                email TEXT,
                nivel TEXT DEFAULT 'usuario',
                ativo INTEGER DEFAULT 1,
                data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
                ultimo_login TEXT,
                tentativas_login INTEGER DEFAULT 0,
                bloqueado INTEGER DEFAULT 0
            )
        ''')

        # Tabela de Alunos (expandida)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT UNIQUE,
                rg TEXT,
                email TEXT,
                telefone TEXT,
                celular TEXT,
                endereco TEXT,
                bairro TEXT,
                cidade TEXT,
                estado TEXT,
                cep TEXT,
                data_nascimento TEXT,
                nome_pai TEXT,
                nome_mae TEXT,
                telefone_responsavel TEXT,
                email_responsavel TEXT,
                data_matricula TEXT,
                status TEXT DEFAULT 'Ativo',
                observacoes TEXT,
                foto TEXT,
                naturalidade TEXT,
                nacionalidade TEXT,
                religiao TEXT,
                necessidades_especiais TEXT,
                medicamentos TEXT,
                alergias TEXT,
                plano_saude TEXT,
                contato_emergencia TEXT,
                telefone_emergencia TEXT
            )
        ''')

        # Tabela de Professores (expandida)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS professores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT UNIQUE,
                rg TEXT,
                email TEXT,
                telefone TEXT,
                celular TEXT,
                endereco TEXT,
                data_nascimento TEXT,
                formacao TEXT,
                especialidade TEXT,
                data_contratacao TEXT,
                salario REAL,
                status TEXT DEFAULT 'Ativo',
                banco TEXT,
                agencia TEXT,
                conta TEXT,
                pis TEXT,
                ctps TEXT,
                observacoes TEXT
            )
        ''')

        # Tabela de Turmas (expandida)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS turmas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                serie TEXT,
                turno TEXT,
                professor_id INTEGER,
                ano_letivo TEXT,
                capacidade INTEGER,
                sala TEXT,
                status TEXT DEFAULT 'Ativa',
                horario_inicio TEXT,
                horario_fim TEXT,
                dias_semana TEXT,
                observacoes TEXT,
                FOREIGN KEY (professor_id) REFERENCES professores (id)
            )
        ''')

        # Tabela de Matrículas (expandida)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS matriculas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_id INTEGER,
                turma_id INTEGER,
                data_matricula TEXT,
                status TEXT DEFAULT 'Ativa',
                numero_matricula TEXT UNIQUE,
                observacoes TEXT,
                data_transferencia TEXT,
                motivo_transferencia TEXT,
                FOREIGN KEY (aluno_id) REFERENCES alunos (id),
                FOREIGN KEY (turma_id) REFERENCES turmas (id)
            )
        ''')

        # Tabela de Disciplinas (expandida)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS disciplinas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                carga_horaria INTEGER,
                professor_id INTEGER,
                turma_id INTEGER,
                descricao TEXT,
                status TEXT DEFAULT 'Ativa',
                ementa TEXT,
                objetivos TEXT,
                competencias TEXT,
                bibliografia TEXT,
                avaliacao TEXT,
                recuperacao TEXT,
                FOREIGN KEY (professor_id) REFERENCES professores (id),
                FOREIGN KEY (turma_id) REFERENCES turmas (id)
            )
        ''')

        # Tabela de Notas (expandida)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_id INTEGER,
                disciplina_id INTEGER,
                nota1 REAL DEFAULT 0,
                nota2 REAL DEFAULT 0,
                nota3 REAL DEFAULT 0,
                nota4 REAL DEFAULT 0,
                nota_recuperacao REAL DEFAULT 0,
                media REAL DEFAULT 0,
                situacao TEXT DEFAULT 'Cursando',
                bimestre INTEGER,
                ano_letivo TEXT,
                observacoes TEXT,
                data_lancamento TEXT,
                professor_id INTEGER,
                FOREIGN KEY (aluno_id) REFERENCES alunos (id),
                FOREIGN KEY (disciplina_id) REFERENCES disciplinas (id),
                FOREIGN KEY (professor_id) REFERENCES professores (id)
            )
        ''')

        # Tabela de Frequência (expandida)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS frequencia (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_id INTEGER,
                disciplina_id INTEGER,
                turma_id INTEGER,
                data_aula TEXT,
                presente INTEGER DEFAULT 1,
                observacao TEXT,
                justificativa TEXT,
                data_justificativa TEXT,
                FOREIGN KEY (aluno_id) REFERENCES alunos (id),
                FOREIGN KEY (disciplina_id) REFERENCES disciplinas (id),
                FOREIGN KEY (turma_id) REFERENCES turmas (id)
            )
        ''')

        # Tabela de Diário de Aula (expandida)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS diario_aula (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                disciplina_id INTEGER,
                turma_id INTEGER,
                professor_id INTEGER,
                data_aula TEXT NOT NULL,
                conteudo TEXT NOT NULL,
                objetivos TEXT,
                metodologia TEXT,
                recursos TEXT,
                tarefa_casa TEXT,
                observacoes TEXT,
                presencas TEXT,
                data_registro TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (disciplina_id) REFERENCES disciplinas (id),
                FOREIGN KEY (turma_id) REFERENCES turmas (id),
                FOREIGN KEY (professor_id) REFERENCES professores (id)
            )
        ''')

        # Tabela de Eventos Escolares
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT,
                data_inicio TEXT,
                data_fim TEXT,
                local TEXT,
                tipo TEXT,
                responsavel TEXT,
                participantes TEXT,
                status TEXT DEFAULT 'Agendado',
                data_criacao TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Tabela de Comunicados
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS comunicados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                mensagem TEXT,
                destinatarios TEXT,
                data_publicacao TEXT,
                data_validade TEXT,
                prioridade TEXT DEFAULT 'Normal',
                status TEXT DEFAULT 'Ativo',
                autor_id INTEGER,
                data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (autor_id) REFERENCES usuarios (id)
            )
        ''')

        # Tabela de Ocorrências
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ocorrencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_id INTEGER,
                professor_id INTEGER,
                tipo TEXT,
                descricao TEXT,
                data_ocorrencia TEXT,
                medidas_tomadas TEXT,
                responsavel TEXT,
                status TEXT DEFAULT 'Aberta',
                data_registro TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (aluno_id) REFERENCES alunos (id),
                FOREIGN KEY (professor_id) REFERENCES professores (id)
            )
        ''')

        # Tabela de Planejamento Pedagógico
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS planejamento_pedagogico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                disciplina_id INTEGER,
                turma_id INTEGER,
                bimestre INTEGER,
                conteudos TEXT,
                habilidades TEXT,
                competencias TEXT,
                estrategias TEXT,
                recursos TEXT,
                avaliacao TEXT,
                data_planejamento TEXT,
                status TEXT DEFAULT 'Rascunho',
                FOREIGN KEY (disciplina_id) REFERENCES disciplinas (id),
                FOREIGN KEY (turma_id) REFERENCES turmas (id)
            )
        ''')

        # Tabela de Avaliações Institucionais
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS avaliacoes_institucionais (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT,
                data_aplicacao TEXT,
                tipo TEXT,
                participantes TEXT,
                resultados TEXT,
                observacoes TEXT,
                status TEXT DEFAULT 'Planejada',
                data_criacao TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Tabela de Histórico Escolar
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS historico_escolar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_id INTEGER,
                ano_letivo TEXT,
                serie TEXT,
                turma TEXT,
                escola_anterior TEXT,
                transferencia TEXT,
                observacoes TEXT,
                data_registro TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (aluno_id) REFERENCES alunos (id)
            )
        ''')

        # Tabela de Configurações do Sistema
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS configuracoes_sistema (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chave TEXT UNIQUE NOT NULL,
                valor TEXT,
                descricao TEXT,
                data_atualizacao TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Tabela de Logs do Sistema
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs_sistema (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                acao TEXT,
                modulo TEXT,
                descricao TEXT,
                data_hora TEXT DEFAULT CURRENT_TIMESTAMP,
                ip TEXT,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')

        # Tabela de Backup
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS backups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                arquivo TEXT,
                tamanho INTEGER,
                data_backup TEXT,
                status TEXT,
                observacoes TEXT
            )
        ''')

        self.conn.commit()

        # Inserir dados iniciais
        self.inserir_dados_iniciais()

    def inserir_dados_iniciais(self):
        """Insere dados iniciais para demonstração"""
        try:
            # Verificar se já existem usuários
            self.cursor.execute("SELECT COUNT(*) FROM usuarios")
            if self.cursor.fetchone()[0] == 0:
                # Inserir usuário admin padrão
                senha_admin = hashlib.sha256('admin123'.encode()).hexdigest()
                self.cursor.execute('''
                    INSERT INTO usuarios (usuario, senha, nome, email, nivel)
                    VALUES (?, ?, ?, ?, ?)
                ''', ('admin', senha_admin, 'Administrador Sistema', 'admin@externato.com', 'admin'))

                # Inserir usuário professor
                senha_prof = hashlib.sha256('prof123'.encode()).hexdigest()
                self.cursor.execute('''
                    INSERT INTO usuarios (usuario, senha, nome, email, nivel)
                    VALUES (?, ?, ?, ?, ?)
                ''', ('professor', senha_prof, 'Maria Silva', 'maria@externato.com', 'professor'))

                # Inserir coordenador
                senha_coord = hashlib.sha256('coord123'.encode()).hexdigest()
                self.cursor.execute('''
                    INSERT INTO usuarios (usuario, senha, nome, email, nivel)
                    VALUES (?, ?, ?, ?, ?)
                ''', ('coordenador', senha_coord, 'Carlos Santos', 'coordenacao@externato.com', 'coordenador'))

                # Inserir professores
                professores = [
                    ('Maria Silva', '111.222.333-44', 'maria@externato.com',
                     '(11) 9999-8888', 'Matemática', '2020-01-15', 3500.00),
                    ('João Santos', '222.333.444-55', 'joao@externato.com',
                     '(11) 8888-7777', 'Português', '2019-03-20', 3200.00),
                    ('Ana Costa', '333.444.555-66', 'ana@externato.com',
                     '(11) 7777-6666', 'História', '2021-02-10', 3000.00),
                    ('Pedro Oliveira', '444.555.666-77', 'pedro@externato.com',
                     '(11) 6666-5555', 'Geografia', '2018-08-15', 3100.00),
                    ('Carla Mendes', '555.666.777-88', 'carla@externato.com',
                     '(11) 5555-4444', 'Ciências', '2022-01-20', 2900.00),
                ]
                self.cursor.executemany('''
                    INSERT INTO professores (nome, cpf, email, telefone, especialidade, data_contratacao, salario)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', professores)

                # Inserir turmas
                turmas = [
                    ('1º Ano A', '1º Ano', 'Manhã', 1, '2024', 30, 'Sala 101', '07:00', '12:00', 'Segunda a Sexta'),
                    ('2º Ano B', '2º Ano', 'Tarde', 2, '2024', 25, 'Sala 102', '13:00', '18:00', 'Segunda a Sexta'),
                    ('3º Ano A', '3º Ano', 'Manhã', 3, '2024', 28, 'Sala 103', '07:00', '12:00', 'Segunda a Sexta'),
                    ('4º Ano B', '4º Ano', 'Tarde', 4, '2024', 26, 'Sala 104', '13:00', '18:00', 'Segunda a Sexta'),
                    ('5º Ano A', '5º Ano', 'Manhã', 5, '2024', 24, 'Sala 105', '07:00', '12:00', 'Segunda a Sexta'),
                ]
                self.cursor.executemany('''
                    INSERT INTO turmas (nome, serie, turno, professor_id, ano_letivo, capacidade, sala, horario_inicio, horario_fim, dias_semana)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', turmas)

                # Inserir alunos
                alunos = [
                    ('Pedro Oliveira', '555.666.777-88', 'pedro@externato.com',
                     '(11) 3333-2222', '(11) 96666-5555', 'Rua A, 123', 'Centro', 'São Paulo', 'SP', '01234-567',
                     '2010-05-15', 'Carlos Oliveira', 'Ana Oliveira', '(11) 95555-4444', 'responsavel@email.com',
                     '2024-01-10'),
                    ('Carla Mendes', '666.777.888-99', 'carla@externato.com',
                     '(11) 4444-3333', '(11) 95555-4444', 'Rua B, 456', 'Jardins', 'São Paulo', 'SP', '01234-568',
                     '2011-08-20', 'Roberto Mendes', 'Julia Mendes', '(11) 94444-3333', 'responsavel2@email.com',
                     '2024-01-10'),
                    ('Ana Costa', '777.888.999-00', 'ana@externato.com',
                     '(11) 5555-4444', '(11) 97777-6666', 'Rua C, 789', 'Moema', 'São Paulo', 'SP', '01234-569',
                     '2010-11-30', 'Paulo Costa', 'Sandra Costa', '(11) 93333-2222', 'responsavel3@email.com',
                     '2024-01-10'),
                    ('Lucas Santos', '888.999.000-11', 'lucas@externato.com',
                     '(11) 6666-5555', '(11) 98888-7777', 'Rua D, 321', 'Pinheiros', 'São Paulo', 'SP', '01234-570',
                     '2011-03-25', 'Marcos Santos', 'Fernanda Santos', '(11) 92222-1111', 'responsavel4@email.com',
                     '2024-01-10'),
                    ('Mariana Lima', '999.000.111-22', 'mariana@externato.com',
                     '(11) 7777-6666', '(11) 99999-8888', 'Rua E, 654', 'Vila Madalena', 'São Paulo', 'SP', '01234-571',
                     '2010-07-12', 'Ricardo Lima', 'Patricia Lima', '(11) 91111-0000', 'responsavel5@email.com',
                     '2024-01-10'),
                ]
                self.cursor.executemany('''
                    INSERT INTO alunos (nome, cpf, email, telefone, celular, endereco, bairro, cidade, estado, cep,
                    data_nascimento, nome_pai, nome_mae, telefone_responsavel, email_responsavel, data_matricula)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', alunos)

                # Matrículas
                matriculas = [
                    (1, 1, '2024-01-10', 'MAT2024001'),
                    (2, 1, '2024-01-10', 'MAT2024002'),
                    (3, 1, '2024-01-10', 'MAT2024003'),
                    (4, 2, '2024-01-10', 'MAT2024004'),
                    (5, 2, '2024-01-10', 'MAT2024005'),
                ]
                self.cursor.executemany('''
                    INSERT INTO matriculas (aluno_id, turma_id, data_matricula, numero_matricula)
                    VALUES (?, ?, ?, ?)
                ''', matriculas)

                # Disciplinas
                disciplinas = [
                    ('Matemática', 80, 1, 1, 'Matemática básica e avançada'),
                    ('Português', 80, 2, 1, 'Gramática e literatura'),
                    ('História', 60, 3, 1, 'História do Brasil'),
                    ('Geografia', 60, 4, 1, 'Geografia geral e do Brasil'),
                    ('Ciências', 60, 5, 1, 'Ciências naturais'),
                ]
                self.cursor.executemany('''
                    INSERT INTO disciplinas (nome, carga_horaria, professor_id, turma_id, descricao)
                    VALUES (?, ?, ?, ?, ?)
                ''', disciplinas)

                # Notas de exemplo
                notas = [
                    (1, 1, 7.5, 8.0, 6.5, 9.0, (7.5 + 8.0 + 6.5 + 9.0) / 4, 'Aprovado', 1, '2024'),
                    (2, 1, 6.0, 7.5, 8.0, 6.5, (6.0 + 7.5 + 8.0 + 6.5) / 4, 'Aprovado', 1, '2024'),
                    (3, 1, 5.0, 6.0, 4.5, 7.0, (5.0 + 6.0 + 4.5 + 7.0) / 4, 'Recuperação', 1, '2024'),
                    (4, 2, 8.0, 8.5, 9.0, 8.5, (8.0 + 8.5 + 9.0 + 8.5) / 4, 'Aprovado', 1, '2024'),
                    (5, 2, 7.0, 6.5, 7.5, 8.0, (7.0 + 6.5 + 7.5 + 8.0) / 4, 'Aprovado', 1, '2024'),
                ]
                self.cursor.executemany('''
                    INSERT INTO notas (aluno_id, disciplina_id, nota1, nota2, nota3, nota4, media, situacao, bimestre, ano_letivo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', notas)

                # Diário de aula de exemplo
                diario_aulas = [
                    (1, 1, 1, '2024-03-01', 'Introdução à álgebra: equações de primeiro grau',
                     'Aula introdutória bem participativa'),
                    (1, 1, 1, '2024-03-08', 'Sistemas de equações e problemas',
                     'Alunos apresentaram dificuldades em problemas contextualizados'),
                    (2, 1, 2, '2024-03-02', 'Análise sintática: sujeito e predicado',
                     'Exercícios práticos de identificação'),
                ]
                self.cursor.executemany('''
                    INSERT INTO diario_aula (disciplina_id, turma_id, professor_id, data_aula, conteudo, observacoes)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', diario_aulas)

                # Eventos escolares
                eventos = [
                    ('Reunião de Pais', 'Primeira reunião de pais do ano letivo', '2024-02-15', '2024-02-15',
                     'Auditório Principal', 'Reunião', 'Coordenação', 'Pais e Responsáveis'),
                    ('Festa Junina', 'Festa junina da escola', '2024-06-15', '2024-06-15',
                     'Pátio da Escola', 'Festividade', 'Comissão de Festas', 'Comunidade Escolar'),
                    ('Olimpíada de Matemática', 'Competição interna de matemática', '2024-08-20', '2024-08-20',
                     'Salas de Aula', 'Competição', 'Departamento de Matemática', 'Alunos do 6º ao 9º ano'),
                ]
                self.cursor.executemany('''
                    INSERT INTO eventos (titulo, descricao, data_inicio, data_fim, local, tipo, responsavel, participantes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', eventos)

                # Comunicados
                comunicados = [
                    ('Início das Aulas', 'As aulas terão início no dia 05/02/2024 conforme calendário escolar.',
                     'Todos', '2024-01-20', '2024-02-05', 'Alta', 1),
                    ('Recesso Escolar',
                     'Informamos que não haverá aula nos dias 20 e 21/02 devido ao feriado municipal.',
                     'Alunos e Professores', '2024-02-15', '2024-02-21', 'Média', 1),
                ]
                self.cursor.executemany('''
                    INSERT INTO comunicados (titulo, mensagem, destinatarios, data_publicacao, data_validade, prioridade, autor_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', comunicados)

                self.conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Dados iniciais já existem: {e}")

    def iniciar_servicos_background(self):
        """Inicia serviços em background"""
        try:
            # Backup automático
            if self.config.get('backup_automatico', True):
                threading.Thread(target=self.servico_backup_automatico, daemon=True).start()

            # Verificação de notificações
            threading.Thread(target=self.servico_notificacoes, daemon=True).start()
        except Exception as e:
            print(f"Erro ao iniciar serviços: {e}")

    def servico_backup_automatico(self):
        """Serviço de backup automático"""
        while True:
            try:
                # Fazer backup diário às 2h
                now = datetime.now()
                if now.hour == 2 and now.minute == 0:
                    self.criar_backup_automatico()
                time.sleep(60)  # Verificar a cada minuto
            except Exception as e:
                print(f"Erro no serviço de backup: {e}")
                time.sleep(300)  # Esperar 5 minutos em caso de erro

    def servico_notificacoes(self):
        """Serviço de verificação de notificações"""
        while True:
            try:
                self.verificar_notificacoes_pendentes()
                time.sleep(300)  # Verificar a cada 5 minutos
            except Exception as e:
                print(f"Erro no serviço de notificações: {e}")
                time.sleep(300)

    def criar_backup_automatico(self):
        """Cria backup automático do banco de dados"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = "backups"
            os.makedirs(backup_dir, exist_ok=True)

            backup_file = f"{backup_dir}/backup_auto_{timestamp}.db"
            shutil.copy2('externato.db', backup_file)

            # Registrar no banco
            tamanho = os.path.getsize(backup_file)
            self.cursor.execute('''
                INSERT INTO backups (arquivo, tamanho, data_backup, status, observacoes)
                VALUES (?, ?, ?, ?, ?)
            ''', (backup_file, tamanho, datetime.now().isoformat(), 'Sucesso', 'Backup automático'))

            self.conn.commit()

            # Manter apenas últimos 10 backups
            self.limpar_backups_antigos(backup_dir, 10)

        except Exception as e:
            print(f"Erro no backup automático: {e}")

    def limpar_backups_antigos(self, backup_dir, manter_quantidade):
        """Remove backups antigos"""
        try:
            backups = []
            for f in os.listdir(backup_dir):
                if f.startswith('backup_auto_') and f.endswith('.db'):
                    filepath = os.path.join(backup_dir, f)
                    backups.append((filepath, os.path.getctime(filepath)))

            # Ordenar por data de criação (mais antigos primeiro)
            backups.sort(key=lambda x: x[1])

            # Remover backups antigos
            while len(backups) > manter_quantidade:
                old_backup = backups.pop(0)
                os.remove(old_backup[0])

        except Exception as e:
            print(f"Erro ao limpar backups: {e}")

    def verificar_notificacoes_pendentes(self):
        """Verifica notificações pendentes"""
        try:
            # Verificar comunicados próximos do vencimento
            hoje = date.today().isoformat()
            self.cursor.execute('''
                SELECT COUNT(*) FROM comunicados
                WHERE data_validade BETWEEN ? AND date(?, '+3 days')
                AND status = 'Ativo'
            ''', (hoje, hoje))

            comunicados_proximos = self.cursor.fetchone()[0]

            # Verificar eventos próximos
            self.cursor.execute('''
                SELECT COUNT(*) FROM eventos
                WHERE data_inicio BETWEEN ? AND date(?, '+7 days')
                AND status = 'Agendado'
            ''', (hoje, hoje))

            eventos_proximos = self.cursor.fetchone()[0]

            # Aqui você pode implementar notificações na interface
            if comunicados_proximos > 0 or eventos_proximos > 0:
                self.mostrar_notificacao_sistema(comunicados_proximos, eventos_proximos)

        except Exception as e:
            print(f"Erro ao verificar notificações: {e}")

    def mostrar_notificacao_sistema(self, comunicados, eventos):
        """Mostra notificação no sistema"""
        try:
            # Esta função seria chamada para atualizar a interface
            # Por enquanto, apenas registra no log
            if hasattr(self, 'status_bar'):
                mensagem = f"📢 {comunicados} comunicados e {eventos} eventos próximos"
                self.status_bar.config(text=mensagem)
        except Exception as e:
            print(f"Erro ao mostrar notificação: {e}")

    def setup_interface(self):
        """Configura a interface gráfica principal"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#0046AD')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        self.setup_header(main_frame)

        # Content area
        content_container = tk.Frame(main_frame, bg='#f8f9fa')
        content_container.pack(fill=tk.BOTH, expand=True)

        # Sidebar
        self.setup_sidebar(content_container)

        # Área de conteúdo
        self.setup_content_area(content_container)

        # Status bar
        self.setup_status_bar(content_container)

        # Ajustar menu conforme perfil
        self.ajustar_menu_conforme_perfil()

    def setup_header(self, parent):
        """Configura o cabeçalho do sistema"""
        header = tk.Frame(parent, bg='#0046AD', height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        # Logo e título
        logo_frame = tk.Frame(header, bg='#0046AD')
        logo_frame.pack(side=tk.LEFT, padx=25, pady=15)

        # Logo Objetivo
        logo_text = tk.Frame(logo_frame, bg='#0046AD')
        logo_text.pack(side=tk.LEFT)

        tk.Label(logo_text, text="●", font=('Arial', 24),
                 fg='#FFCC00', bg='#0046AD').pack(side=tk.LEFT)

        tk.Label(logo_text, text="OBJETIVO", font=('Arial', 20, 'bold'),
                 fg='white', bg='#0046AD').pack(side=tk.LEFT, padx=8)

        escola_frame = tk.Frame(logo_frame, bg='#0046AD')
        escola_frame.pack(side=tk.LEFT, padx=10)

        tk.Label(escola_frame, text="Externato Colégio", font=('Arial', 12),
                 fg='#FFCC00', bg='#0046AD').pack()
        tk.Label(escola_frame, text="Sistema de Gestão Integrado", font=('Arial', 10),
                 fg='white', bg='#0046AD').pack()

        # Informações do usuário e data
        info_frame = tk.Frame(header, bg='#0046AD')
        info_frame.pack(side=tk.RIGHT, padx=25, pady=15)

        # Data e hora
        self.data_hora_label = tk.Label(info_frame, text="", font=('Arial', 10),
                                        bg='#0046AD', fg='white')
        self.data_hora_label.pack(side=tk.RIGHT, padx=10)
        self.atualizar_data_hora()

        # Info do usuário
        user_label = tk.Label(info_frame, text=f"👤 {self.usuario_nome} | {self.usuario_nivel.title()}",
                              font=('Arial', 10), bg='#0046AD', fg='#FFCC00')
        user_label.pack(side=tk.RIGHT, padx=10)

        # Botão configurações
        config_btn = ModernButton(info_frame, text="⚙️", command=self.abrir_configuracoes,
                                  color='#0046AD', font=('Arial', 12), padx=10, pady=5)
        config_btn.pack(side=tk.RIGHT, padx=5)

    def atualizar_data_hora(self):
        """Atualiza data e hora no header"""
        agora = datetime.now()
        texto_data = agora.strftime("%d/%m/%Y %H:%M:%S")
        self.data_hora_label.config(text=texto_data)
        self.root.after(1000, self.atualizar_data_hora)

    def setup_sidebar(self, parent):
        """Configura a barra lateral"""
        sidebar = tk.Frame(parent, bg='#0046AD', width=280)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        # Menu de navegação
        self.nav_buttons = {}

        nav_buttons_config = [
            ("📊 Dashboard", self.carregar_dashboard),
            ("👨🎓 Gestão de Alunos", self.carregar_gestao_alunos),
            ("👨🏫 Gestão de Professores", self.carregar_gestao_professores),
            ("🏫 Gestão de Turmas", self.carregar_gestao_turmas),
            ("📚 Gestão de Disciplinas", self.carregar_gestao_disciplinas),
            ("📝 Sistema de Notas", self.carregar_sistema_notas),
            ("📋 Controle de Matrículas", self.carregar_controle_matriculas),
            ("📓 Diário de Classe", self.carregar_diario_classe),
            ("✅ Controle de Frequência", self.carregar_controle_frequencia),
            ("📅 Calendário Escolar", self.carregar_calendario_escolar),
            ("📢 Comunicados e Avisos", self.carregar_comunicados_avisos),
            ("🔔 Ocorrências Disciplinares", self.carregar_ocorrencias_disciplinares),
            ("📋 Relatórios Gerenciais", self.carregar_relatorios_gerenciais),
            ("🎓 Histórico Escolar", self.carregar_historico_escolar),
            ("📈 Planejamento Pedagógico", self.carregar_planejamento_pedagogico),
            ("🏆 Avaliações Institucionais", self.carregar_avaliacoes_institucionais),
            ("⚙️ Configurações do Sistema", self.carregar_configuracoes_sistema),
        ]

        # Frame com scroll para a sidebar
        canvas = tk.Canvas(sidebar, bg='#0046AD', highlightthickness=0)
        scrollbar = ttk.Scrollbar(sidebar, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for i, (text, command) in enumerate(nav_buttons_config):
            btn = tk.Button(scrollable_frame, text=text, font=('Arial', 11),
                            bg='#0046AD', fg='white', bd=0, anchor='w', padx=25,
                            command=command, cursor='hand2', pady=12)
            btn.pack(fill=tk.X, pady=1)

            # Efeitos hover
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg='#0066CC'))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg='#0046AD'))

            self.nav_buttons[text] = btn

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.ativar_botao("📊 Dashboard")

        # Logout
        logout_frame = tk.Frame(scrollable_frame, bg='#0046AD')
        logout_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        ModernButton(logout_frame, text="🚪 Sair do Sistema", command=self.sair,
                     color='#FF6B6B', font=('Arial', 11)).pack(fill=tk.X, padx=20)

    def setup_content_area(self, parent):
        """Configura a área de conteúdo principal"""
        self.content_frame = tk.Frame(parent, bg='#f8f9fa')
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def setup_status_bar(self, parent):
        """Configura a barra de status"""
        self.status_bar = tk.Label(parent, text="Sistema carregado com sucesso | Externato Colégio Objetivo",
                                   font=('Arial', 9), bg='#0046AD', fg='white', anchor='w')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def ajustar_menu_conforme_perfil(self):
        """Ajusta o menu lateral conforme o perfil do usuário"""
        if self.usuario_nivel == 'professor':
            opcoes_restritas = [
                "💰 Gestão Financeira",
                "👨🏫 Gestão de Professores",
                "⚙️ Configurações do Sistema",
                "📈 Relatórios Gerenciais"
            ]
            for opcao in opcoes_restritas:
                if opcao in self.nav_buttons:
                    self.nav_buttons[opcao].pack_forget()

        elif self.usuario_nivel == 'coordenador':
            opcoes_restritas = ["💰 Gestão Financeira", "⚙️ Configurações do Sistema"]
            for opcao in opcoes_restritas:
                if opcao in self.nav_buttons:
                    self.nav_buttons[opcao].pack_forget()

    def ativar_botao(self, nome_botao):
        """Ativa o botão de navegação selecionado"""
        for nome, btn in self.nav_buttons.items():
            if nome == nome_botao:
                btn.configure(bg='#FFCC00', fg='#0046AD')
            else:
                btn.configure(bg='#0046AD', fg='white')

    def sair(self):
        """Sair do sistema"""
        if messagebox.askyesno("Sair", "Deseja realmente sair do sistema?"):
            try:
                # Registrar log de saída
                self.registrar_log('LOGOUT', 'Sistema', f'Usuário {self.usuario_nome} saiu do sistema')
                self.conn.close()
                self.root.destroy()
            except Exception as e:
                self.root.destroy()

    def limpar_conteudo(self):
        """Limpa o conteúdo da área principal"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def criar_toolbar(self, parent, botoes):
        """Cria uma barra de ferramentas padronizada"""
        toolbar = tk.Frame(parent, bg='white', relief='flat', bd=1, height=60)
        toolbar.pack(fill=tk.X, pady=(0, 20))
        toolbar.pack_propagate(False)

        left_frame = tk.Frame(toolbar, bg='white')
        left_frame.pack(side=tk.LEFT, padx=20, pady=15)

        for texto, comando, cor in botoes:
            btn = ModernButton(left_frame, text=texto, command=comando, color=cor)
            btn.pack(side=tk.LEFT, padx=5)

        return toolbar

    def criar_tabela(self, parent, colunas, altura=20):
        """Cria uma tabela padronizada"""
        frame = tk.Frame(parent, bg='white', relief='flat', bd=1)
        frame.pack(fill=tk.BOTH, expand=True)

        # Treeview
        tree = ttk.Treeview(frame, columns=colunas, show='headings', height=altura, style='Custom.Treeview')

        # Configurar colunas
        for col in colunas:
            tree.heading(col, text=col)
            tree.column(col, width=120, minwidth=100)

        # Scrollbars
        v_scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        h_scroll = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        # Layout
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        return tree

    def registrar_log(self, acao, modulo, descricao):
        """Registra log de atividades do sistema"""
        try:
            self.cursor.execute('''
                INSERT INTO logs_sistema (usuario_id, acao, modulo, descricao, data_hora)
                VALUES (?, ?, ?, ?, ?)
            ''', (self.usuario_id, acao, modulo, descricao, datetime.now().isoformat()))
            self.conn.commit()
        except Exception as e:
            print(f"Erro ao registrar log: {e}")

    # ========== DASHBOARD PRINCIPAL ==========

    def carregar_dashboard(self):
        """Carrega o dashboard principal"""
        self.limpar_conteudo()
        self.ativar_botao("📊 Dashboard")
        self.registrar_log('ACESSO', 'Dashboard', 'Acessou o dashboard principal')

        # Título
        title_frame = tk.Frame(self.content_frame, bg='#f8f9fa')
        title_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(title_frame, text="Dashboard Principal", font=('Arial', 24, 'bold'),
                 bg='#f8f9fa', fg='#0046AD').pack(anchor='w')

        tk.Label(title_frame, text="Visão geral do sistema educacional - Externato Colégio Objetivo",
                 font=('Arial', 12), bg='#f8f9fa', fg='#666666').pack(anchor='w')

        # Frame principal do dashboard
        main_dashboard = tk.Frame(self.content_frame, bg='#f8f9fa')
        main_dashboard.pack(fill=tk.BOTH, expand=True)

        # Container com scroll
        canvas = tk.Canvas(main_dashboard, bg='#f8f9fa', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_dashboard, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Estatísticas
        stats_frame = tk.Frame(scrollable_frame, bg='#f8f9fa')
        stats_frame.pack(fill=tk.X, pady=(0, 30))

        # Buscar estatísticas
        stats_data = self.buscar_estatisticas_dashboard()

        for i, (titulo, valor, icon, cor) in enumerate(stats_data):
            card = CardFrame(stats_frame, titulo, valor, icon, cor, width=200, height=120)
            card.grid(row=0, column=i, padx=10, pady=10, sticky='nsew')

        for i in range(len(stats_data)):
            stats_frame.columnconfigure(i, weight=1)

        # Gráficos e métricas
        metrics_frame = tk.Frame(scrollable_frame, bg='#f8f9fa')
        metrics_frame.pack(fill=tk.X, pady=20)

        # Abas para diferentes visualizações
        notebook = ttk.Notebook(metrics_frame, style='Custom.TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Aba 1: Visão Geral
        aba_visao_geral = ttk.Frame(notebook)
        notebook.add(aba_visao_geral, text="📈 Visão Geral")

        self.carregar_visao_geral_dashboard(aba_visao_geral)

        # Aba 2: Desempenho Acadêmico
        aba_desempenho = ttk.Frame(notebook)
        notebook.add(aba_desempenho, text="🎓 Desempenho")

        self.carregar_desempenho_dashboard(aba_desempenho)

        # Aba 3: Frequência
        aba_frequencia = ttk.Frame(notebook)
        notebook.add(aba_frequencia, text="✅ Frequência")

        self.carregar_frequencia_dashboard(aba_frequencia)

        # Ações rápidas
        actions_frame = tk.Frame(scrollable_frame, bg='#f8f9fa')
        actions_frame.pack(fill=tk.X, pady=20)

        tk.Label(actions_frame, text="⚡ Ações Rápidas", font=('Arial', 18, 'bold'),
                 bg='#f8f9fa', fg='#0046AD').pack(anchor='w', pady=(0, 15))

        acoes_frame = tk.Frame(actions_frame, bg='#f8f9fa')
        acoes_frame.pack(fill=tk.X)

        acoes = [
            ("➕ Novo Aluno", self.novo_aluno, '#0046AD'),
            ("👨🏫 Novo Professor", self.novo_professor, '#0046AD'),
            ("🏫 Nova Turma", self.nova_turma, '#0046AD'),
            ("📝 Lançar Notas", self.lancar_notas, '#0046AD'),
            ("📓 Registrar Aula", self.nova_aula_diario, '#0046AD'),
            ("📢 Novo Comunicado", self.novo_comunicado, '#0046AD'),
            ("📅 Novo Evento", self.novo_evento, '#0046AD'),
            ("📋 Relatório Rápido", self.gerar_relatorio_rapido, '#0046AD'),
        ]

        # Organizar em duas linhas
        linha1 = tk.Frame(acoes_frame, bg='#f8f9fa')
        linha1.pack(fill=tk.X, pady=5)
        linha2 = tk.Frame(acoes_frame, bg='#f8f9fa')
        linha2.pack(fill=tk.X, pady=5)

        for i, (texto, comando, cor) in enumerate(acoes):
            if i < 4:
                btn = ModernButton(linha1, text=texto, command=comando, color=cor)
                btn.pack(side=tk.LEFT, padx=5)
            else:
                btn = ModernButton(linha2, text=texto, command=comando, color=cor)
                btn.pack(side=tk.LEFT, padx=5)

        # Atividades recentes
        atividades_frame = tk.Frame(scrollable_frame, bg='#f8f9fa')
        atividades_frame.pack(fill=tk.X, pady=20)

        tk.Label(atividades_frame, text="🕐 Atividades Recentes", font=('Arial', 18, 'bold'),
                 bg='#f8f9fa', fg='#0046AD').pack(anchor='w', pady=(0, 15))

        self.carregar_atividades_recentes(atividades_frame)

        # Avisos e notificações
        if hasattr(self, 'usuario_nivel'):
            if self.usuario_nivel == 'professor':
                self.carregar_avisos_professor(scrollable_frame)
            elif self.usuario_nivel == 'coordenador':
                self.carregar_avisos_coordenador(scrollable_frame)
            else:
                self.carregar_avisos_administrativos(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def buscar_estatisticas_dashboard(self):
        """Busca estatísticas atualizadas do banco para o dashboard"""
        try:
            total_alunos = self.cursor.execute("SELECT COUNT(*) FROM alunos WHERE status='Ativo'").fetchone()[0]
            total_professores = self.cursor.execute("SELECT COUNT(*) FROM professores WHERE status='Ativo'").fetchone()[
                0]
            total_turmas = self.cursor.execute("SELECT COUNT(*) FROM turmas WHERE status='Ativa'").fetchone()[0]
            total_disciplinas = self.cursor.execute("SELECT COUNT(*) FROM disciplinas WHERE status='Ativa'").fetchone()[
                0]

            # Estatísticas específicas para professores
            if hasattr(self, 'usuario_nivel') and self.usuario_nivel == 'professor':
                self.cursor.execute("SELECT id FROM professores WHERE nome = ?", (self.usuario_nome,))
                professor = self.cursor.fetchone()
                if professor:
                    professor_id = professor[0]
                    total_minhas_disciplinas = self.cursor.execute(
                        "SELECT COUNT(*) FROM disciplinas WHERE professor_id = ?", (professor_id,)
                    ).fetchone()[0]
                    total_aulas = self.cursor.execute(
                        "SELECT COUNT(*) FROM diario_aula WHERE professor_id = ?", (professor_id,)
                    ).fetchone()[0]

                    # Alunos do professor
                    total_meus_alunos = self.cursor.execute('''
                        SELECT COUNT(DISTINCT m.aluno_id)
                        FROM matriculas m
                        JOIN turmas t ON m.turma_id = t.id
                        JOIN disciplinas d ON t.id = d.turma_id
                        WHERE d.professor_id = ? AND m.status = 'Ativa'
                    ''', (professor_id,)).fetchone()[0]

                    return [
                        ("Minhas Disciplinas", total_minhas_disciplinas, "📚", "#0046AD"),
                        ("Aulas Ministradas", total_aulas, "📅", "#FFCC00"),
                        ("Meus Alunos", total_meus_alunos, "👨🎓", "#0046AD"),
                        ("Turmas", total_turmas, "🏫", "#FFCC00"),
                    ]

            # Estatísticas para coordenador
            elif hasattr(self, 'usuario_nivel') and self.usuario_nivel == 'coordenador':
                total_ocorrencias = \
                    self.cursor.execute("SELECT COUNT(*) FROM ocorrencias WHERE status='Aberta'").fetchone()[0]
                total_comunicados = \
                    self.cursor.execute("SELECT COUNT(*) FROM comunicados WHERE status='Ativo'").fetchone()[0]

                return [
                    ("Alunos Ativos", total_alunos, "👨🎓", "#0046AD"),
                    ("Professores", total_professores, "👨🏫", "#FFCC00"),
                    ("Ocorrências Abertas", total_ocorrencias, "🔔", "#FF6B6B"),
                    ("Comunicados Ativos", total_comunicados, "📢", "#0046AD"),
                ]

            # Estatísticas para admin
            return [
                ("Alunos Ativos", total_alunos, "👨🎓", "#0046AD"),
                ("Professores", total_professores, "👨🏫", "#FFCC00"),
                ("Turmas Ativas", total_turmas, "🏫", "#0046AD"),
                ("Disciplinas", total_disciplinas, "📚", "#FFCC00"),
            ]
        except Exception as e:
            print(f"Erro ao buscar estatísticas: {e}")
            return [
                ("Alunos Ativos", "0", "👨🎓", "#0046AD"),
                ("Professores", "0", "👨🏫", "#FFCC00"),
                ("Turmas", "0", "🏫", "#0046AD"),
                ("Disciplinas", "0", "📚", "#FFCC00"),
            ]

    def carregar_visao_geral_dashboard(self, parent):
        """Carrega visão geral no dashboard"""
        try:
            # Métricas rápidas
            metrics_frame = tk.Frame(parent, bg='white', relief='flat', bd=1, padx=20, pady=15)
            metrics_frame.pack(fill=tk.X, pady=10)

            tk.Label(metrics_frame, text="Métricas do Sistema", font=('Arial', 14, 'bold'),
                     bg='white', fg='#0046AD').pack(anchor='w')

            # Buscar métricas
            total_matriculas = self.cursor.execute("SELECT COUNT(*) FROM matriculas WHERE status='Ativa'").fetchone()[0]
            media_geral = self.cursor.execute("SELECT AVG(media) FROM notas WHERE media > 0").fetchone()[0] or 0
            frequencia_media = self.cursor.execute("SELECT AVG(presente) * 100 FROM frequencia").fetchone()[0] or 0

            metrics_text = f"""
            • Total de Matrículas Ativas: {total_matriculas}
            • Média Geral dos Alunos: {media_geral:.2f}
            • Frequência Média: {frequencia_media:.1f}%
            • Taxa de Aprovação: {self.calcular_taxa_aprovacao():.1f}%
            """

            tk.Label(metrics_frame, text=metrics_text, font=('Arial', 11),
                     bg='white', fg='#666666', justify=tk.LEFT).pack(anchor='w', pady=10)

        except Exception as e:
            print(f"Erro ao carregar visão geral: {e}")

    def carregar_desempenho_dashboard(self, parent):
        """Carrega dados de desempenho no dashboard"""
        try:
            desempenho_frame = tk.Frame(parent, bg='white', relief='flat', bd=1, padx=20, pady=15)
            desempenho_frame.pack(fill=tk.X, pady=10)

            tk.Label(desempenho_frame, text="Desempenho por Turma", font=('Arial', 14, 'bold'),
                     bg='white', fg='#0046AD').pack(anchor='w')

            # Buscar desempenho por turma
            self.cursor.execute('''
                SELECT t.nome, AVG(n.media) as media_turma,
                       COUNT(CASE WHEN n.media >= 6 THEN 1 END) as aprovados,
                       COUNT(CASE WHEN n.media < 6 THEN 1 END) as em_recuperacao
                FROM turmas t
                JOIN matriculas m ON t.id = m.turma_id
                JOIN notas n ON m.aluno_id = n.aluno_id
                WHERE t.status = 'Ativa' AND m.status = 'Ativa'
                GROUP BY t.nome
                ORDER BY media_turma DESC
            ''')

            turmas_desempenho = self.cursor.fetchall()

            if turmas_desempenho:
                for turma, media, aprovados, recuperacao in turmas_desempenho:
                    turma_frame = tk.Frame(desempenho_frame, bg='#f8f9fa', relief='flat', bd=1, padx=10, pady=5)
                    turma_frame.pack(fill=tk.X, pady=2)

                    info_text = f"{turma}: Média {media:.2f} | Aprovados: {aprovados} | Recuperação: {recuperacao}"
                    tk.Label(turma_frame, text=info_text, font=('Arial', 10),
                             bg='#f8f9fa', justify=tk.LEFT).pack(anchor='w')
            else:
                tk.Label(desempenho_frame, text="Nenhum dado de desempenho disponível",
                         font=('Arial', 11), bg='white', fg='#666666').pack(anchor='w')

        except Exception as e:
            print(f"Erro ao carregar desempenho: {e}")

    def carregar_frequencia_dashboard(self, parent):
        """Carrega dados de frequência no dashboard"""
        try:
            frequencia_frame = tk.Frame(parent, bg='white', relief='flat', bd=1, padx=20, pady=15)
            frequencia_frame.pack(fill=tk.X, pady=10)

            tk.Label(frequencia_frame, text="Frequência por Disciplina", font=('Arial', 14, 'bold'),
                     bg='white', fg='#0046AD').pack(anchor='w')

            # Buscar frequência por disciplina
            self.cursor.execute('''
                SELECT d.nome,
                       COUNT(f.id) as total_registros,
                       COUNT(CASE WHEN f.presente = 1 THEN 1 END) as presencas,
                       ROUND(COUNT(CASE WHEN f.presente = 1 THEN 1 END) * 100.0 / COUNT(f.id), 2) as percentual
                FROM disciplinas d
                LEFT JOIN frequencia f ON d.id = f.disciplina_id
                WHERE d.status = 'Ativa'
                GROUP BY d.nome
                ORDER BY percentual DESC
                LIMIT 10
            ''')

            frequencia_disciplinas = self.cursor.fetchall()

            if frequencia_disciplinas:
                for disciplina, total, presencas, percentual in frequencia_disciplinas:
                    disc_frame = tk.Frame(frequencia_frame, bg='#f8f9fa', relief='flat', bd=1, padx=10, pady=5)
                    disc_frame.pack(fill=tk.X, pady=2)

                    info_text = f"{disciplina}: {presencas}/{total} ({percentual}%)"
                    tk.Label(disc_frame, text=info_text, font=('Arial', 10),
                             bg='#f8f9fa', justify=tk.LEFT).pack(anchor='w')
            else:
                tk.Label(frequencia_frame, text="Nenhum registro de frequência disponível",
                         font=('Arial', 11), bg='white', fg='#666666').pack(anchor='w')

        except Exception as e:
            print(f"Erro ao carregar frequência: {e}")

    def carregar_atividades_recentes(self, parent):
        """Carrega atividades recentes no dashboard"""
        try:
            atividades_frame = tk.Frame(parent, bg='white', relief='flat', bd=1, padx=20, pady=15)
            atividades_frame.pack(fill=tk.X, pady=10)

            # Buscar logs recentes
            self.cursor.execute('''
                SELECT l.acao, l.modulo, l.descricao, l.data_hora, u.nome
                FROM logs_sistema l
                JOIN usuarios u ON l.usuario_id = u.id
                ORDER BY l.data_hora DESC
                LIMIT 10
            ''')

            logs = self.cursor.fetchall()

            if logs:
                for acao, modulo, descricao, data_hora, usuario in logs:
                    log_frame = tk.Frame(atividades_frame, bg='#f8f9fa', relief='flat', bd=1, padx=10, pady=5)
                    log_frame.pack(fill=tk.X, pady=2)

                    data_formatada = datetime.fromisoformat(data_hora).strftime("%d/%m/%Y %H:%M")
                    info_text = f"{data_formatada} | {usuario} | {acao} em {modulo}: {descricao}"

                    tk.Label(log_frame, text=info_text, font=('Arial', 9),
                             bg='#f8f9fa', justify=tk.LEFT, wraplength=800).pack(anchor='w')
            else:
                tk.Label(atividades_frame, text="Nenhuma atividade recente registrada",
                         font=('Arial', 11), bg='white', fg='#666666').pack(anchor='w')

        except Exception as e:
            print(f"Erro ao carregar atividades: {e}")

    def calcular_taxa_aprovacao(self):
        """Calcula a taxa de aprovação geral"""
        try:
            self.cursor.execute('''
                SELECT COUNT(*) as total,
                       COUNT(CASE WHEN media >= 6 THEN 1 END) as aprovados
                FROM notas
                WHERE media > 0
            ''')
            resultado = self.cursor.fetchone()
            if resultado and resultado[0] > 0:
                return (resultado[1] / resultado[0]) * 100
            return 0
        except:
            return 0

    def carregar_avisos_professor(self, parent):
        """Carrega avisos específicos para professores"""
        avisos_frame = tk.Frame(parent, bg='#FFF9E6', relief='flat', bd=1, padx=20, pady=15)
        avisos_frame.pack(fill=tk.X, pady=20)

        tk.Label(avisos_frame, text="📢 Avisos do Professor", font=('Arial', 14, 'bold'),
                 bg='#FFF9E6', fg='#0046AD').pack(anchor='w', pady=(0, 10))

        try:
            self.cursor.execute("SELECT id FROM professores WHERE nome = ?", (self.usuario_nome,))
            professor = self.cursor.fetchone()

            if professor:
                professor_id = professor[0]

                # Aulas pendentes
                self.cursor.execute('''
                    SELECT COUNT(*) FROM diario_aula
                    WHERE professor_id = ? AND date(data_aula) = date('now')
                ''', (professor_id,))
                aulas_hoje = self.cursor.fetchone()[0]

                # Notas pendentes
                self.cursor.execute('''
                    SELECT COUNT(DISTINCT n.disciplina_id)
                    FROM notas n
                    JOIN disciplinas d ON n.disciplina_id = d.id
                    WHERE d.professor_id = ? AND n.media = 0 AND n.bimestre = ?
                ''', (professor_id, self.obter_bimestre_atual()))
                notas_pendentes = self.cursor.fetchone()[0]

                # Frequência pendente
                self.cursor.execute('''
                    SELECT COUNT(DISTINCT data_aula)
                    FROM diario_aula
                    WHERE professor_id = ? AND presencas IS NULL
                ''', (professor_id,))
                frequencia_pendente = self.cursor.fetchone()[0]

                avisos_text = f"""
                • Aulas para hoje: {aulas_hoje}
                • Disciplinas com notas pendentes: {notas_pendentes}
                • Aulas com frequência pendente: {frequencia_pendente}
                • Próximas atividades: Verificar planejamento pedagógico
                """

                tk.Label(avisos_frame, text=avisos_text, font=('Arial', 11),
                         bg='#FFF9E6', fg='#666666', justify=tk.LEFT).pack(anchor='w', pady=(0, 10))

        except Exception as e:
            print(f"Erro ao carregar avisos: {e}")

    def carregar_avisos_coordenador(self, parent):
        """Carrega avisos específicos para coordenadores"""
        avisos_frame = tk.Frame(parent, bg='#E6F3FF', relief='flat', bd=1, padx=20, pady=15)
        avisos_frame.pack(fill=tk.X, pady=20)

        tk.Label(avisos_frame, text="📢 Avisos da Coordenação", font=('Arial', 14, 'bold'),
                 bg='#E6F3FF', fg='#0046AD').pack(anchor='w', pady=(0, 10))

        try:
            # Ocorrências pendentes
            ocorrencias_pendentes = self.cursor.execute(
                "SELECT COUNT(*) FROM ocorrencias WHERE status='Aberta'"
            ).fetchone()[0]

            # Comunicados próximos do vencimento
            hoje = date.today().isoformat()
            comunicados_vencendo = self.cursor.execute('''
                SELECT COUNT(*) FROM comunicados
                WHERE data_validade BETWEEN ? AND date(?, '+3 days')
                AND status = 'Ativo'
            ''', (hoje, hoje)).fetchone()[0]

            # Eventos próximos
            eventos_proximos = self.cursor.execute('''
                SELECT COUNT(*) FROM eventos
                WHERE data_inicio BETWEEN ? AND date(?, '+7 days')
                AND status = 'Agendado'
            ''', (hoje, hoje)).fetchone()[0]

            avisos_text = f"""
            • Ocorrências pendentes: {ocorrencias_pendentes}
            • Comunicados próximos do vencimento: {comunicados_vencendo}
            • Eventos próximos: {eventos_proximos}
            • Reuniões pedagógicas: Verificar calendário
            """

            tk.Label(avisos_frame, text=avisos_text, font=('Arial', 11),
                     bg='#E6F3FF', fg='#666666', justify=tk.LEFT).pack(anchor='w', pady=(0, 10))

        except Exception as e:
            print(f"Erro ao carregar avisos coordenador: {e}")

    def carregar_avisos_administrativos(self, parent):
        """Carrega avisos para administradores"""
        avisos_frame = tk.Frame(parent, bg='#E6F3FF', relief='flat', bd=1, padx=20, pady=15)
        avisos_frame.pack(fill=tk.X, pady=20)

        tk.Label(avisos_frame, text="📢 Avisos do Sistema", font=('Arial', 14, 'bold'),
                 bg='#E6F3FF', fg='#0046AD').pack(anchor='w', pady=(0, 10))

        try:
            # Estatísticas gerais
            total_alunos = self.cursor.execute("SELECT COUNT(*) FROM alunos WHERE status='Ativo'").fetchone()[0]
            total_professores = self.cursor.execute("SELECT COUNT(*) FROM professores WHERE status='Ativo'").fetchone()[
                0]
            total_turmas = self.cursor.execute("SELECT COUNT(*) FROM turmas WHERE status='Ativa'").fetchone()[0]

            # Backup status
            ultimo_backup = self.cursor.execute(
                "SELECT data_backup FROM backups ORDER BY id DESC LIMIT 1"
            ).fetchone()

            backup_status = "OK" if ultimo_backup else "Pendente"

            avisos_text = f"""
            • Total de alunos ativos: {total_alunos}
            • Professores ativos: {total_professores}
            • Turmas ativas: {total_turmas}
            • Status do backup: {backup_status}
            • Próximos eventos: Reunião pedagógica mensal
            """

            tk.Label(avisos_frame, text=avisos_text, font=('Arial', 11),
                     bg='#E6F3FF', fg='#666666', justify=tk.LEFT).pack(anchor='w', pady=(0, 10))

        except Exception as e:
            print(f"Erro ao carregar avisos administrativos: {e}")

    def obter_bimestre_atual(self):
        """Retorna o bimestre atual baseado na data"""
        mes_atual = datetime.now().month
        if mes_atual in [1, 2]:
            return 1
        elif mes_atual in [3, 4]:
            return 2
        elif mes_atual in [5, 6]:
            return 3
        elif mes_atual in [7, 8]:
            return 4
        else:
            return 1  # Padrão para o primeiro bimestre

    # ========== MÓDULO GESTÃO DE ALUNOS ==========

    def carregar_gestao_alunos(self):
        """Carrega o módulo completo de gestão de alunos"""
        self.limpar_conteudo()
        self.ativar_botao("👨🎓 Gestão de Alunos")
        self.registrar_log('ACESSO', 'Gestão de Alunos', 'Acessou módulo de gestão de alunos')

        # Título
        title_frame = tk.Frame(self.content_frame, bg='#f8f9fa')
        title_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(title_frame, text="Gestão de Alunos", font=('Arial', 24, 'bold'),
                 bg='#f8f9fa', fg='#0046AD').pack(anchor='w')

        tk.Label(title_frame, text="Cadastro, consulta e gestão completa de alunos",
                 font=('Arial', 12), bg='#f8f9fa', fg='#666666').pack(anchor='w')

        # Notebook com abas
        notebook = ttk.Notebook(self.content_frame, style='Custom.TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Aba 1: Lista de Alunos
        aba_lista = ttk.Frame(notebook)
        notebook.add(aba_lista, text="👥 Lista de Alunos")

        self.carregar_aba_lista_alunos(aba_lista)

        # Aba 2: Cadastro de Alunos
        aba_cadastro = ttk.Frame(notebook)
        notebook.add(aba_cadastro, text="➕ Cadastro")

        self.carregar_aba_cadastro_alunos(aba_cadastro)

        # Aba 3: Relatórios de Alunos
        aba_relatorios = ttk.Frame(notebook)
        notebook.add(aba_relatorios, text="📊 Relatórios")

        self.carregar_aba_relatorios_alunos(aba_relatorios)

    def carregar_aba_lista_alunos(self, parent):
        """Carrega aba de lista de alunos"""
        # Barra de ferramentas
        botoes = [
            ("🔍 Buscar", self.buscar_alunos, '#0046AD'),
            ("📝 Editar", self.editar_aluno, '#0046AD'),
            ("🗑️ Excluir", self.excluir_aluno, '#FF6B6B'),
            ("📋 Exportar", self.exportar_alunos, '#0046AD'),
            ("🖨️ Imprimir", self.imprimir_lista_alunos, '#0046AD'),
        ]
        toolbar = self.criar_toolbar(parent, botoes)

        # Filtros
        filtros_frame = tk.Frame(toolbar, bg='white')
        filtros_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        tk.Label(filtros_frame, text="Filtro:", font=('Arial', 9),
                 bg='white').pack(side=tk.LEFT, padx=5)

        self.filtro_status_alunos = ttk.Combobox(filtros_frame,
                                                 values=['Todos', 'Ativo', 'Inativo', 'Transferido'],
                                                 state='readonly', width=12)
        self.filtro_status_alunos.pack(side=tk.LEFT, padx=5)
        self.filtro_status_alunos.set('Ativo')

        self.filtro_turma_alunos = ttk.Combobox(filtros_frame,
                                                values=['Todas'] + self.obter_turmas_combo(),
                                                state='readonly', width=15)
        self.filtro_turma_alunos.pack(side=tk.LEFT, padx=5)
        self.filtro_turma_alunos.set('Todas')

        ModernButton(filtros_frame, text="Aplicar",
                     command=self.aplicar_filtros_alunos,
                     color='#0046AD').pack(side=tk.LEFT, padx=5)

        # Campo de busca
        search_frame = tk.Frame(toolbar, bg='white')
        search_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.search_var_alunos = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var_alunos,
                                width=30, font=('Arial', 10), relief='solid', bd=1)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind('<KeyRelease>', self.buscar_alunos)

        # Tabela de alunos
        colunas = ('ID', 'Nome', 'CPF', 'Email', 'Telefone', 'Turma', 'Status', 'Data Matrícula')
        self.tree_alunos = self.criar_tabela(parent, colunas)

        # Carregar dados
        self.carregar_dados_alunos()

    def carregar_aba_cadastro_alunos(self, parent):
        """Carrega aba de cadastro de alunos"""
        form_frame = tk.Frame(parent, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Container com scroll
        canvas = tk.Canvas(form_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Formulário de cadastro
        self.criar_formulario_aluno(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def carregar_aba_relatorios_alunos(self, parent):
        """Carrega aba de relatórios de alunos"""
        relatorios_frame = tk.Frame(parent, bg='#f8f9fa')
        relatorios_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(relatorios_frame, text="Relatórios de Alunos", font=('Arial', 16, 'bold'),
                 bg='#f8f9fa', fg='#0046AD').pack(anchor='w', pady=(0, 20))

        # Grid de relatórios
        grid_frame = tk.Frame(relatorios_frame, bg='#f8f9fa')
        grid_frame.pack(fill=tk.BOTH, expand=True)

        relatorios = [
            ("📋 Lista Completa", self.gerar_relatorio_alunos_completo,
             "Lista completa de todos os alunos cadastrados"),
            ("🎓 Alunos por Turma", self.gerar_relatorio_alunos_turma,
             "Relação de alunos organizada por turma"),
            ("📊 Estatísticas Gerais", self.gerar_relatorio_estatisticas_alunos,
             "Estatísticas e métricas dos alunos"),
            ("📅 Aniversariantes", self.gerar_relatorio_aniversariantes,
             "Lista de aniversariantes do mês"),
            ("📍 Alunos por Bairro", self.gerar_relatorio_alunos_bairro,
             "Distribuição geográfica dos alunos"),
            ("🚨 Alunos Inativos", self.gerar_relatorio_alunos_inativos,
             "Relação de alunos com matrícula inativa"),
        ]

        for i, (titulo, comando, descricao) in enumerate(relatorios):
            row = i // 3
            col = i % 3

            card = tk.Frame(grid_frame, bg='white', relief='flat', bd=1,
                            highlightbackground='#e0e0e0', highlightthickness=1)
            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            card.configure(width=250, height=120)

            tk.Label(card, text=titulo, font=('Arial', 12, 'bold'),
                     bg='white', fg='#0046AD').pack(pady=(15, 5))

            tk.Label(card, text=descricao, font=('Arial', 9),
                     bg='white', fg='#666666', wraplength=220).pack(pady=5, padx=10)

            ModernButton(card, text="Gerar Relatório", command=comando,
                         color='#0046AD', font=('Arial', 10)).pack(pady=10)

        for i in range(3):
            grid_frame.columnconfigure(i, weight=1)
        for i in range(2):
            grid_frame.rowconfigure(i, weight=1)

    def criar_formulario_aluno(self, parent):
        """Cria formulário de cadastro de aluno"""
        # Dados Pessoais
        dados_frame = tk.LabelFrame(parent, text="Dados Pessoais", font=('Arial', 12, 'bold'),
                                    bg='white', fg='#0046AD', padx=15, pady=15)
        dados_frame.pack(fill=tk.X, pady=10)

        campos_dados = [
            ("Nome Completo*", "entry", None),
            ("CPF", "entry", None),
            ("RG", "entry", None),
            ("Data Nascimento", "entry", None),
            ("Email", "entry", None),
            ("Telefone", "entry", None),
            ("Celular", "entry", None),
        ]

        self.entries_aluno = {}
        linha = 0
        coluna = 0

        for label, tipo, valores in campos_dados:
            tk.Label(dados_frame, text=label, font=('Arial', 10, 'bold'),
                     bg='white', fg='#0046AD').grid(row=linha, column=coluna * 2, sticky='w', pady=5, padx=5)

            if tipo == "entry":
                entry = tk.Entry(dados_frame, width=25, font=('Arial', 10), relief='solid', bd=1)
                entry.grid(row=linha, column=coluna * 2 + 1, pady=5, padx=5, sticky='ew')
                self.entries_aluno[label] = entry

            coluna += 1
            if coluna >= 2:
                coluna = 0
                linha += 1

        # Endereço
        endereco_frame = tk.LabelFrame(parent, text="Endereço", font=('Arial', 12, 'bold'),
                                       bg='white', fg='#0046AD', padx=15, pady=15)
        endereco_frame.pack(fill=tk.X, pady=10)

        campos_endereco = [
            ("Endereço", "entry", None),
            ("Bairro", "entry", None),
            ("Cidade", "entry", None),
            ("Estado", "combo", ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
                                 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
                                 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']),
            ("CEP", "entry", None),
        ]

        linha = 0
        for label, tipo, valores in campos_endereco:
            tk.Label(endereco_frame, text=label, font=('Arial', 10, 'bold'),
                     bg='white', fg='#0046AD').grid(row=linha, column=0, sticky='w', pady=5, padx=5)

            if tipo == "entry":
                entry = tk.Entry(endereco_frame, width=40, font=('Arial', 10), relief='solid', bd=1)
                entry.grid(row=linha, column=1, pady=5, padx=5, sticky='ew', columnspan=3)
                self.entries_aluno[label] = entry
            elif tipo == "combo":
                combo = ttk.Combobox(endereco_frame, values=valores, state='readonly', width=37)
                combo.grid(row=linha, column=1, pady=5, padx=5, sticky='ew', columnspan=3)
                self.entries_aluno[label] = combo

            linha += 1

        # Responsáveis
        responsaveis_frame = tk.LabelFrame(parent, text="Responsáveis", font=('Arial', 12, 'bold'),
                                           bg='white', fg='#0046AD', padx=15, pady=15)
        responsaveis_frame.pack(fill=tk.X, pady=10)

        campos_responsaveis = [
            ("Nome do Pai", "entry", None),
            ("Nome da Mãe", "entry", None),
            ("Telefone Responsável", "entry", None),
            ("Email Responsável", "entry", None),
        ]

        linha = 0
        coluna = 0
        for label, tipo, valores in campos_responsaveis:
            tk.Label(responsaveis_frame, text=label, font=('Arial', 10, 'bold'),
                     bg='white', fg='#0046AD').grid(row=linha, column=coluna * 2, sticky='w', pady=5, padx=5)

            if tipo == "entry":
                entry = tk.Entry(responsaveis_frame, width=25, font=('Arial', 10), relief='solid', bd=1)
                entry.grid(row=linha, column=coluna * 2 + 1, pady=5, padx=5, sticky='ew')
                self.entries_aluno[label] = entry

            coluna += 1
            if coluna >= 2:
                coluna = 0
                linha += 1

        # Informações Adicionais
        info_frame = tk.LabelFrame(parent, text="Informações Adicionais", font=('Arial', 12, 'bold'),
                                   bg='white', fg='#0046AD', padx=15, pady=15)
        info_frame.pack(fill=tk.X, pady=10)

        campos_info = [
            ("Naturalidade", "entry", None),
            ("Nacionalidade", "entry", None),
            ("Religião", "entry", None),
            ("Necessidades Especiais", "entry", None),
            ("Medicamentos", "text", None),
            ("Alergias", "text", None),
            ("Plano de Saúde", "entry", None),
            ("Contato Emergência", "entry", None),
            ("Telefone Emergência", "entry", None),
        ]

        linha = 0
        coluna = 0
        for label, tipo, valores in campos_info:
            tk.Label(info_frame, text=label, font=('Arial', 10, 'bold'),
                     bg='white', fg='#0046AD').grid(row=linha, column=coluna * 2, sticky='w', pady=5, padx=5)

            if tipo == "entry":
                entry = tk.Entry(info_frame, width=25, font=('Arial', 10), relief='solid', bd=1)
                entry.grid(row=linha, column=coluna * 2 + 1, pady=5, padx=5, sticky='ew')
                self.entries_aluno[label] = entry
            elif tipo == "text":
                text = tk.Text(info_frame, width=25, height=3, font=('Arial', 10), relief='solid', bd=1)
                text.grid(row=linha, column=coluna * 2 + 1, pady=5, padx=5, sticky='ew')
                self.entries_aluno[label] = text

            coluna += 1
            if coluna >= 2:
                coluna = 0
                linha += 1

        # Status
        status_frame = tk.Frame(parent, bg='white')
        status_frame.pack(fill=tk.X, pady=10)

        tk.Label(status_frame, text="Status:", font=('Arial', 10, 'bold'),
                 bg='white', fg='#0046AD').pack(side=tk.LEFT, padx=5)

        self.status_aluno = ttk.Combobox(status_frame, values=['Ativo', 'Inativo', 'Transferido'],
                                         state='readonly', width=15)
        self.status_aluno.set('Ativo')
        self.status_aluno.pack(side=tk.LEFT, padx=5)

        # Botões
        botoes_frame = tk.Frame(parent, bg='white')
        botoes_frame.pack(pady=20)

        ModernButton(botoes_frame, text="🗑️ Limpar",
                     command=self.limpar_formulario_aluno,
                     color='#666666').pack(side=tk.LEFT, padx=10)

        ModernButton(botoes_frame, text="💾 Salvar Aluno",
                     command=self.salvar_aluno,
                     color='#0046AD').pack(side=tk.LEFT, padx=10)

        # Configurar pesos das colunas
        for frame in [dados_frame, endereco_frame, responsaveis_frame, info_frame]:
            frame.columnconfigure(1, weight=1)
            frame.columnconfigure(3, weight=1)

    def limpar_formulario_aluno(self):
        """Limpa todos os campos do formulário de aluno"""
        for entry in self.entries_aluno.values():
            if isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)
            elif isinstance(entry, tk.Text):
                entry.delete('1.0', tk.END)
            elif isinstance(entry, ttk.Combobox):
                entry.set('')

        self.status_aluno.set('Ativo')

    def salvar_aluno(self):
        """Salva os dados do aluno no banco de dados"""
        try:
            # Validar campos obrigatórios
            if not self.entries_aluno["Nome Completo*"].get().strip():
                messagebox.showwarning("Aviso", "O campo Nome Completo é obrigatório!")
                return

            # Coletar dados
            dados = {
                'nome': self.entries_aluno["Nome Completo*"].get().strip(),
                'cpf': self.entries_aluno["CPF"].get().strip(),
                'rg': self.entries_aluno["RG"].get().strip(),
                'data_nascimento': self.entries_aluno["Data Nascimento"].get().strip(),
                'email': self.entries_aluno["Email"].get().strip(),
                'telefone': self.entries_aluno["Telefone"].get().strip(),
                'celular': self.entries_aluno["Celular"].get().strip(),
                'endereco': self.entries_aluno["Endereço"].get().strip(),
                'bairro': self.entries_aluno["Bairro"].get().strip(),
                'cidade': self.entries_aluno["Cidade"].get().strip(),
                'estado': self.entries_aluno["Estado"].get().strip(),
                'cep': self.entries_aluno["CEP"].get().strip(),
                'nome_pai': self.entries_aluno["Nome do Pai"].get().strip(),
                'nome_mae': self.entries_aluno["Nome da Mãe"].get().strip(),
                'telefone_responsavel': self.entries_aluno["Telefone Responsável"].get().strip(),
                'email_responsavel': self.entries_aluno["Email Responsável"].get().strip(),
                'naturalidade': self.entries_aluno["Naturalidade"].get().strip(),
                'nacionalidade': self.entries_aluno["Nacionalidade"].get().strip(),
                'religiao': self.entries_aluno["Religião"].get().strip(),
                'necessidades_especiais': self.entries_aluno["Necessidades Especiais"].get().strip(),
                'medicamentos': self.entries_aluno["Medicamentos"].get("1.0", tk.END).strip(),
                'alergias': self.entries_aluno["Alergias"].get("1.0", tk.END).strip(),
                'plano_saude': self.entries_aluno["Plano de Saúde"].get().strip(),
                'contato_emergencia': self.entries_aluno["Contato Emergência"].get().strip(),
                'telefone_emergencia': self.entries_aluno["Telefone Emergência"].get().strip(),
                'status': self.status_aluno.get(),
                'data_matricula': date.today().strftime("%Y-%m-%d")
            }

            # Verificar se CPF já existe
            if dados['cpf']:
                self.cursor.execute("SELECT id FROM alunos WHERE cpf = ?", (dados['cpf'],))
                if self.cursor.fetchone():
                    messagebox.showerror("Erro", "CPF já cadastrado no sistema!")
                    return

            # Inserir no banco
            self.cursor.execute('''
                INSERT INTO alunos (
                    nome, cpf, rg, data_nascimento, email, telefone, celular,
                    endereco, bairro, cidade, estado, cep, nome_pai, nome_mae,
                    telefone_responsavel, email_responsavel, naturalidade, nacionalidade,
                    religiao, necessidades_especiais, medicamentos, alergias, plano_saude,
                    contato_emergencia, telefone_emergencia, status, data_matricula
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', tuple(dados.values()))

            self.conn.commit()

            # Registrar log
            self.registrar_log('CADASTRO', 'Alunos', f'Cadastrou aluno: {dados["nome"]}')

            messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
            self.limpar_formulario_aluno()
            self.carregar_dados_alunos()

        except sqlite3.IntegrityError as e:
            messagebox.showerror("Erro", f"Erro de integridade: {str(e)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar aluno: {str(e)}")

    def carregar_dados_alunos(self, query=None, filtro_status='Ativo', filtro_turma='Todas'):
        """Carrega dados dos alunos na tabela"""
        for item in self.tree_alunos.get_children():
            self.tree_alunos.delete(item)

        sql = '''
            SELECT a.id, a.nome, a.cpf, a.email, a.telefone,
                   COALESCE(t.nome, 'Sem turma'), a.status, a.data_matricula
            FROM alunos a
            LEFT JOIN matriculas m ON a.id = m.aluno_id AND m.status = 'Ativa'
            LEFT JOIN turmas t ON m.turma_id = t.id
            WHERE 1=1
        '''
        params = []

        if query:
            sql += ' AND (a.nome LIKE ? OR a.cpf LIKE ? OR a.email LIKE ?)'
            params.extend([f'%{query}%', f'%{query}%', f'%{query}%'])

        if filtro_status != 'Todos':
            sql += ' AND a.status = ?'
            params.append(filtro_status)

        if filtro_turma != 'Todas':
            sql += ' AND t.nome = ?'
            params.append(filtro_turma)

        sql += ' ORDER BY a.nome'

        self.cursor.execute(sql, params)
        alunos = self.cursor.fetchall()

        for aluno in alunos:
            self.tree_alunos.insert('', tk.END, values=aluno)

    def buscar_alunos(self, event=None):
        """Busca alunos na tabela"""
        query = self.search_var_alunos.get()
        self.carregar_dados_alunos(query)

    def aplicar_filtros_alunos(self):
        """Aplica filtros na tabela de alunos"""
        status = self.filtro_status_alunos.get()
        turma = self.filtro_turma_alunos.get()
        self.carregar_dados_alunos(None, status, turma)

    def obter_turmas_combo(self):
        """Retorna lista de turmas para combobox"""
        self.cursor.execute("SELECT nome FROM turmas WHERE status='Ativa' ORDER BY nome")
        return [turma[0] for turma in self.cursor.fetchall()]

    def editar_aluno(self):
        """Edita aluno selecionado"""
        selection = self.tree_alunos.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um aluno para editar!")
            return

        item = self.tree_alunos.item(selection[0])
        aluno_id = item['values'][0]
        self.abrir_edicao_aluno(aluno_id)

    def excluir_aluno(self):
        """Exclui aluno selecionado"""
        selection = self.tree_alunos.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um aluno para excluir!")
            return

        item = self.tree_alunos.item(selection[0])
        aluno_id, nome = item['values'][0], item['values'][1]

        resposta = messagebox.askyesno("Confirmar Exclusão",
                                       f"Tem certeza que deseja excluir o aluno {nome}?\n\nEsta ação não pode ser desfeita!")

        if resposta:
            try:
                self.cursor.execute("DELETE FROM alunos WHERE id = ?", (aluno_id,))
                self.conn.commit()

                # Registrar log
                self.registrar_log('EXCLUSAO', 'Alunos', f'Excluiu aluno: {nome}')

                messagebox.showinfo("Sucesso", "Aluno excluído com sucesso!")
                self.carregar_dados_alunos()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir aluno: {str(e)}")

    def exportar_alunos(self):
        """Exporta lista de alunos para CSV"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Exportar lista de alunos"
            )

            if filename:
                self.cursor.execute('''
                    SELECT a.nome, a.cpf, a.email, a.telefone, a.celular,
                           a.endereco, a.bairro, a.cidade, a.estado, a.data_nascimento,
                           a.nome_pai, a.nome_mae, a.telefone_responsavel, a.status,
                           t.nome as turma
                    FROM alunos a
                    LEFT JOIN matriculas m ON a.id = m.aluno_id AND m.status = 'Ativa'
                    LEFT JOIN turmas t ON m.turma_id = t.id
                    ORDER BY a.nome
                ''')

                alunos = self.cursor.fetchall()

                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Nome', 'CPF', 'Email', 'Telefone', 'Celular', 'Endereço',
                                     'Bairro', 'Cidade', 'Estado', 'Data Nascimento', 'Nome Pai',
                                     'Nome Mãe', 'Telefone Responsável', 'Status', 'Turma'])
                    writer.writerows(alunos)

                messagebox.showinfo("Sucesso", f"Lista de alunos exportada para: {filename}")

                # Registrar log
                self.registrar_log('EXPORTACAO', 'Alunos', 'Exportou lista de alunos para CSV')

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar alunos: {str(e)}")

    def imprimir_lista_alunos(self):
        """Gera PDF com lista de alunos"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Salvar lista de alunos como PDF"
            )

            if filename:
                self.cursor.execute('''
                    SELECT a.nome, a.cpf, a.email, a.telefone, t.nome as turma, a.status
                    FROM alunos a
                    LEFT JOIN matriculas m ON a.id = m.aluno_id AND m.status = 'Ativa'
                    LEFT JOIN turmas t ON m.turma_id = t.id
                    ORDER BY t.nome, a.nome
                ''')

                alunos = self.cursor.fetchall()

                # Criar PDF
                c = canvas.Canvas(filename, pagesize=A4)
                width, height = A4

                # Cabeçalho
                c.setFont("Helvetica-Bold", 16)
                c.drawString(50, height - 50, "EXTERNATO COLÉGIO OBJETIVO")
                c.setFont("Helvetica", 12)
                c.drawString(50, height - 70, "Lista de Alunos")
                c.drawString(50, height - 85, f"Data: {date.today().strftime('%d/%m/%Y')}")

                # Tabela
                data = [['Nome', 'CPF', 'Email', 'Telefone', 'Turma', 'Status']]
                for aluno in alunos:
                    data.append([aluno[0], aluno[1] or '', aluno[2] or '', aluno[3] or '', aluno[4] or '', aluno[5]])

                table = Table(data, colWidths=[120, 100, 120, 80, 80, 60])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0046AD')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))

                table.wrapOn(c, width, height)
                table.drawOn(c, 50, height - 150)

                c.save()
                messagebox.showinfo("Sucesso", f"PDF gerado: {filename}")

                # Registrar log
                self.registrar_log('IMPRESSAO', 'Alunos', 'Gerou PDF com lista de alunos')

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar PDF: {str(e)}")

    def abrir_edicao_aluno(self, aluno_id):
        """Abre janela para editar aluno existente"""
        try:
            # Buscar dados do aluno
            self.cursor.execute("SELECT * FROM alunos WHERE id = ?", (aluno_id,))
            aluno = self.cursor.fetchone()

            if not aluno:
                messagebox.showerror("Erro", "Aluno não encontrado!")
                return

            # Criar janela de edição
            edit_window = tk.Toplevel(self.root)
            edit_window.title(f"Editar Aluno - ID: {aluno_id}")
            edit_window.geometry("800x600")
            edit_window.configure(bg='white')
            edit_window.transient(self.root)
            edit_window.grab_set()
            self.center_dialog(edit_window)

            # Header
            header_frame = tk.Frame(edit_window, bg='#0046AD', height=60)
            header_frame.pack(fill=tk.X)
            header_frame.pack_propagate(False)

            tk.Label(header_frame, text=f"Editar Aluno: {aluno[1]}",
                     font=('Arial', 14, 'bold'), bg='#0046AD', fg='white').pack(expand=True)

            # Container com scroll
            container = tk.Frame(edit_window, bg='white')
            container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            canvas = tk.Canvas(container, bg='white', highlightthickness=0)
            scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)

            scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            # Formulário de edição (similar ao de cadastro)
            self.criar_formulario_edicao_aluno(scrollable_frame, aluno)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Botões
            btn_frame = tk.Frame(edit_window, bg='white')
            btn_frame.pack(pady=20)

            ModernButton(btn_frame, text="Cancelar", command=edit_window.destroy,
                         color='#666666').pack(side=tk.LEFT, padx=10)

            ModernButton(btn_frame, text="Salvar Alterações",
                         command=lambda: self.salvar_edicao_aluno(aluno_id, edit_window),
                         color='#0046AD').pack(side=tk.LEFT, padx=10)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir edição: {str(e)}")

    def criar_formulario_edicao_aluno(self, parent, aluno):
        """Cria formulário de edição preenchido com dados do aluno"""
        colunas = [desc[0] for desc in self.cursor.description]
        aluno_dict = dict(zip(colunas, aluno))

        # Dados Pessoais
        dados_frame = tk.LabelFrame(parent, text="Dados Pessoais", font=('Arial', 12, 'bold'),
                                    bg='white', fg='#0046AD', padx=15, pady=15)
        dados_frame.pack(fill=tk.X, pady=10)

        campos = [
            ("Nome Completo*", "entry", aluno_dict.get('nome', '')),
            ("CPF", "entry", aluno_dict.get('cpf', '')),
            ("RG", "entry", aluno_dict.get('rg', '')),
            ("Data Nascimento", "entry", aluno_dict.get('data_nascimento', '')),
            ("Email", "entry", aluno_dict.get('email', '')),
            ("Telefone", "entry", aluno_dict.get('telefone', '')),
            ("Celular", "entry", aluno_dict.get('celular', '')),
        ]

        self.entries_edicao_aluno = {}
        linha = 0
        coluna = 0

        for label, tipo, valor in campos:
            tk.Label(dados_frame, text=label, font=('Arial', 10, 'bold'),
                     bg='white', fg='#0046AD').grid(row=linha, column=coluna * 2, sticky='w', pady=5, padx=5)

            if tipo == "entry":
                entry = tk.Entry(dados_frame, width=25, font=('Arial', 10), relief='solid', bd=1)
                entry.insert(0, str(valor) if valor else '')
                entry.grid(row=linha, column=coluna * 2 + 1, pady=5, padx=5, sticky='ew')
                self.entries_edicao_aluno[label] = entry

            coluna += 1
            if coluna >= 2:
                coluna = 0
                linha += 1

        # Status
        status_frame = tk.Frame(parent, bg='white')
        status_frame.pack(fill=tk.X, pady=10)

        tk.Label(status_frame, text="Status:", font=('Arial', 10, 'bold'),
                 bg='white', fg='#0046AD').pack(side=tk.LEFT, padx=5)

        self.status_edicao_aluno = ttk.Combobox(status_frame, values=['Ativo', 'Inativo', 'Transferido'],
                                                state='readonly', width=15)
        self.status_edicao_aluno.set(aluno_dict.get('status', 'Ativo'))
        self.status_edicao_aluno.pack(side=tk.LEFT, padx=5)

        # Configurar pesos das colunas
        dados_frame.columnconfigure(1, weight=1)
        dados_frame.columnconfigure(3, weight=1)

    def salvar_edicao_aluno(self, aluno_id, window):
        """Salva as alterações do aluno editado"""
        try:
            # Coletar dados
            dados = {
                'nome': self.entries_edicao_aluno["Nome Completo*"].get().strip(),
                'cpf': self.entries_edicao_aluno["CPF"].get().strip(),
                'rg': self.entries_edicao_aluno["RG"].get().strip(),
                'data_nascimento': self.entries_edicao_aluno["Data Nascimento"].get().strip(),
                'email': self.entries_edicao_aluno["Email"].get().strip(),
                'telefone': self.entries_edicao_aluno["Telefone"].get().strip(),
                'celular': self.entries_edicao_aluno["Celular"].get().strip(),
                'status': self.status_edicao_aluno.get()
            }

            # Validar campos obrigatórios
            if not dados['nome']:
                messagebox.showwarning("Aviso", "O campo Nome Completo é obrigatório!")
                return

            # Atualizar no banco
            self.cursor.execute('''
                UPDATE alunos SET nome=?, cpf=?, rg=?, data_nascimento=?,
                email=?, telefone=?, celular=?, status=? WHERE id=?
            ''', (dados['nome'], dados['cpf'], dados['rg'], dados['data_nascimento'],
                  dados['email'], dados['telefone'], dados['celular'], dados['status'], aluno_id))

            self.conn.commit()

            # Registrar log
            self.registrar_log('EDICAO', 'Alunos', f'Editou aluno: {dados["nome"]}')

            messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")
            window.destroy()
            self.carregar_dados_alunos()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar aluno: {str(e)}")

    # ========== FUNÇÕES DE RELATÓRIOS DE ALUNOS ==========

    def gerar_relatorio_alunos_completo(self):
        """Gera relatório completo de alunos"""
        try:
            self.cursor.execute('''
                SELECT a.nome, a.cpf, a.email, a.telefone, a.celular, a.data_nascimento,
                       a.endereco, a.bairro, a.cidade, a.estado, a.nome_pai, a.nome_mae,
                       a.telefone_responsavel, a.status, t.nome as turma, a.data_matricula
                FROM alunos a
                LEFT JOIN matriculas m ON a.id = m.aluno_id AND m.status = 'Ativa'
                LEFT JOIN turmas t ON m.turma_id = t.id
                ORDER BY a.nome
            ''')

            alunos = self.cursor.fetchall()

            relatorio = "RELATÓRIO COMPLETO DE ALUNOS\n"
            relatorio += "=" * 50 + "\n\n"
            relatorio += f"Total de alunos: {len(alunos)}\n"
            relatorio += f"Data do relatório: {date.today().strftime('%d/%m/%Y')}\n\n"

            for aluno in alunos:
                relatorio += f"Nome: {aluno[0]}\n"
                relatorio += f"CPF: {aluno[1] or 'Não informado'}\n"
                relatorio += f"Email: {aluno[2] or 'Não informado'}\n"
                relatorio += f"Telefone: {aluno[3] or 'Não informado'} | Celular: {aluno[4] or 'Não informado'}\n"
                relatorio += f"Data Nascimento: {aluno[5] or 'Não informada'}\n"
                relatorio += f"Endereço: {aluno[6] or 'Não informado'}, {aluno[7] or ''} - {aluno[8] or ''}/{aluno[9] or ''}\n"
                relatorio += f"Responsáveis: {aluno[10] or 'Não informado'} / {aluno[11] or 'Não informado'}\n"
                relatorio += f"Tel. Responsável: {aluno[12] or 'Não informado'}\n"
                relatorio += f"Turma: {aluno[14] or 'Sem turma'} | Status: {aluno[13]}\n"
                relatorio += f"Data Matrícula: {aluno[15] or 'Não informada'}\n"
                relatorio += "-" * 50 + "\n"

            self.mostrar_relatorio("Relatório Completo de Alunos", relatorio)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")

    def gerar_relatorio_alunos_turma(self):
        """Gera relatório de alunos por turma"""
        try:
            self.cursor.execute('''
                SELECT t.nome as turma, a.nome, a.email, a.telefone, a.status
                FROM alunos a
                JOIN matriculas m ON a.id = m.aluno_id
                JOIN turmas t ON m.turma_id = t.id
                WHERE m.status = 'Ativa'
                ORDER BY t.nome, a.nome
            ''')

            alunos_turma = self.cursor.fetchall()

            relatorio = "RELATÓRIO DE ALUNOS POR TURMA\n"
            relatorio += "=" * 40 + "\n\n"

            turma_atual = None
            for turma, nome, email, telefone, status in alunos_turma:
                if turma != turma_atual:
                    if turma_atual:
                        relatorio += "\n"
                    turma_atual = turma
                    relatorio += f"TURMA: {turma}\n"
                    relatorio += "-" * 30 + "\n"

                relatorio += f"{nome} | {email or 'Sem email'} | {telefone or 'Sem telefone'} | {status}\n"

            self.mostrar_relatorio("Alunos por Turma", relatorio)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")

    def gerar_relatorio_estatisticas_alunos(self):
        """Gera relatório de estatísticas dos alunos"""
        try:
            # Total por status
            self.cursor.execute('''
                SELECT status, COUNT(*) as total
                FROM alunos
                GROUP BY status
            ''')
            status_stats = self.cursor.fetchall()

            # Total por turma
            self.cursor.execute('''
                SELECT t.nome, COUNT(*) as total
                FROM alunos a
                JOIN matriculas m ON a.id = m.aluno_id AND m.status = 'Ativa'
                JOIN turmas t ON m.turma_id = t.id
                GROUP BY t.nome
                ORDER BY t.nome
            ''')
            turma_stats = self.cursor.fetchall()

            # Idade média
            self.cursor.execute('''
                SELECT AVG((julianday('now') - julianday(data_nascimento)) / 365.25)
                FROM alunos
                WHERE data_nascimento IS NOT NULL
            ''')
            idade_media = self.cursor.fetchone()[0] or 0

            relatorio = "ESTATÍSTICAS DE ALUNOS\n"
            relatorio += "=" * 30 + "\n\n"

            relatorio += "DISTRIBUIÇÃO POR STATUS:\n"
            for status, total in status_stats:
                relatorio += f"• {status}: {total} alunos\n"

            relatorio += f"\nIDADE MÉDIA: {idade_media:.1f} anos\n"

            relatorio += "\nDISTRIBUIÇÃO POR TURMA:\n"
            for turma, total in turma_stats:
                relatorio += f"• {turma}: {total} alunos\n"

            self.mostrar_relatorio("Estatísticas de Alunos", relatorio)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")

    def gerar_relatorio_aniversariantes(self):
        """Gera relatório de aniversariantes do mês"""
        try:
            mes_atual = datetime.now().month
            self.cursor.execute('''
                SELECT nome, data_nascimento, email, telefone, t.nome as turma
                FROM alunos a
                LEFT JOIN matriculas m ON a.id = m.aluno_id AND m.status = 'Ativa'
                LEFT JOIN turmas t ON m.turma_id = t.id
                WHERE strftime('%m', data_nascimento) = ?
                ORDER BY strftime('%d', data_nascimento), nome
            ''', (str(mes_atual).zfill(2),))

            aniversariantes = self.cursor.fetchall()

            relatorio = f"ANIVERSARIANTES DO MÊS {mes_atual}\n"
            relatorio += "=" * 40 + "\n\n"

            if aniversariantes:
                for nome, data_nasc, email, telefone, turma in aniversariantes:
                    if data_nasc:
                        dia = datetime.strptime(data_nasc, '%Y-%m-%d').day
                        relatorio += f"• {dia:02d}/{mes_atual:02d} - {nome}"
                        relatorio += f" | {turma or 'Sem turma'}"
                        relatorio += f" | {telefone or 'Sem telefone'}\n"
            else:
                relatorio += "Nenhum aniversariante este mês.\n"

            self.mostrar_relatorio("Aniversariantes", relatorio)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")

    def gerar_relatorio_alunos_bairro(self):
        """Gera relatório de alunos por bairro"""
        try:
            self.cursor.execute('''
                SELECT bairro, COUNT(*) as total, cidade, estado
                FROM alunos
                WHERE bairro IS NOT NULL AND bairro != ''
                GROUP BY bairro, cidade, estado
                ORDER BY total DESC, bairro
            ''')

            bairros = self.cursor.fetchall()

            relatorio = "DISTRIBUIÇÃO GEOGRÁFICA DOS ALUNOS\n"
            relatorio += "=" * 50 + "\n\n"

            total_alunos = 0
            for bairro, total, cidade, estado in bairros:
                relatorio += f"• {bairro}"
                if cidade:
                    relatorio += f" - {cidade}"
                if estado:
                    relatorio += f"/{estado}"
                relatorio += f": {total} alunos\n"
                total_alunos += total

            relatorio += f"\nTOTAL DE ALUNOS COM ENDEREÇO: {total_alunos}\n"

            self.mostrar_relatorio("Alunos por Bairro", relatorio)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")

    def gerar_relatorio_alunos_inativos(self):
        """Gera relatório de alunos inativos"""
        try:
            self.cursor.execute('''
                SELECT nome, cpf, email, telefone, data_matricula,
                       (SELECT nome FROM turmas t
                        JOIN matriculas m ON t.id = m.turma_id
                        WHERE m.aluno_id = a.id AND m.status != 'Ativa'
                        ORDER BY m.id DESC LIMIT 1) as ultima_turma
                FROM alunos a
                WHERE status = 'Inativo'
                ORDER BY nome
            ''')

            inativos = self.cursor.fetchall()

            relatorio = "RELATÓRIO DE ALUNOS INATIVOS\n"
            relatorio += "=" * 40 + "\n\n"

            if inativos:
                for nome, cpf, email, telefone, data_matricula, ultima_turma in inativos:
                    relatorio += f"• {nome}\n"
                    relatorio += f"  CPF: {cpf or 'Não informado'}\n"
                    relatorio += f"  Email: {email or 'Não informado'}\n"
                    relatorio += f"  Telefone: {telefone or 'Não informado'}\n"
                    relatorio += f"  Data Matrícula: {data_matricula or 'Não informada'}\n"
                    relatorio += f"  Última Turma: {ultima_turma or 'Não informada'}\n"
                    relatorio += "-" * 30 + "\n"
            else:
                relatorio += "Nenhum aluno inativo encontrado.\n"

            self.mostrar_relatorio("Alunos Inativos", relatorio)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")

    def mostrar_relatorio(self, titulo, conteudo):
        """Mostra relatório em uma janela"""
        dialog = tk.Toplevel(self.root)
        dialog.title(titulo)
        dialog.geometry("800x600")
        dialog.configure(bg='white')
        self.center_dialog(dialog)

        tk.Label(dialog, text=titulo, font=('Arial', 16, 'bold'),
                 bg='white', fg='#0046AD').pack(pady=10)

        text_frame = tk.Frame(dialog, bg='white')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        text_widget = tk.Text(text_frame, font=('Arial', 10), wrap=tk.WORD)
        text_widget.insert(tk.END, conteudo)
        text_widget.config(state=tk.DISABLED)

        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)

        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def exportar():
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt")],
                title=f"Salvar {titulo}"
            )
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(conteudo)
                messagebox.showinfo("Sucesso", f"Relatório salvo em: {filename}")

        ModernButton(dialog, text="💾 Exportar Relatório",
                     command=exportar, color='#0046AD').pack(pady=10)

    # ========== MÓDULO GESTÃO DE PROFESSORES ==========

    def carregar_gestao_professores(self):
        """Carrega o módulo completo de gestão de professores"""
        self.limpar_conteudo()
        self.ativar_botao("👨🏫 Gestão de Professores")
        self.registrar_log('ACESSO', 'Gestão de Professores', 'Acessou módulo de gestão de professores')

        # Título
        title_frame = tk.Frame(self.content_frame, bg='#f8f9fa')
        title_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(title_frame, text="Gestão de Professores", font=('Arial', 24, 'bold'),
                 bg='#f8f9fa', fg='#0046AD').pack(anchor='w')

        tk.Label(title_frame, text="Cadastro, consulta e gestão completa do corpo docente",
                 font=('Arial', 12), bg='#f8f9fa', fg='#666666').pack(anchor='w')

        # Notebook com abas
        notebook = ttk.Notebook(self.content_frame, style='Custom.TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Aba 1: Lista de Professores
        aba_lista = ttk.Frame(notebook)
        notebook.add(aba_lista, text="👥 Lista de Professores")

        self.carregar_aba_lista_professores(aba_lista)

        # Aba 2: Cadastro de Professores
        aba_cadastro = ttk.Frame(notebook)
        notebook.add(aba_cadastro, text="➕ Cadastro")

        self.carregar_aba_cadastro_professores(aba_cadastro)

        # Aba 3: Relatórios de Professores
        aba_relatorios = ttk.Frame(notebook)
        notebook.add(aba_relatorios, text="📊 Relatórios")

        self.carregar_aba_relatorios_professores(aba_relatorios)

    def carregar_aba_lista_professores(self, parent):
        """Carrega aba de lista de professores"""
        # Barra de ferramentas
        botoes = [
            ("🔍 Buscar", self.buscar_professores, '#0046AD'),
            ("📝 Editar", self.editar_professor, '#0046AD'),
            ("🗑️ Excluir", self.excluir_professor, '#FF6B6B'),
            ("📋 Exportar", self.exportar_professores, '#0046AD'),
            ("🖨️ Imprimir", self.imprimir_lista_professores, '#0046AD'),
        ]
        toolbar = self.criar_toolbar(parent, botoes)

        # Filtros
        filtros_frame = tk.Frame(toolbar, bg='white')
        filtros_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        tk.Label(filtros_frame, text="Filtro:", font=('Arial', 9),
                 bg='white').pack(side=tk.LEFT, padx=5)

        self.filtro_status_professores = ttk.Combobox(filtros_frame,
                                                      values=['Todos', 'Ativo', 'Inativo'],
                                                      state='readonly', width=12)
        self.filtro_status_professores.pack(side=tk.LEFT, padx=5)
        self.filtro_status_professores.set('Ativo')

        ModernButton(filtros_frame, text="Aplicar",
                     command=self.aplicar_filtros_professores,
                     color='#0046AD').pack(side=tk.LEFT, padx=5)

        # Campo de busca
        search_frame = tk.Frame(toolbar, bg='white')
        search_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.search_var_professores = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var_professores,
                                width=30, font=('Arial', 10), relief='solid', bd=1)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind('<KeyRelease>', self.buscar_professores)

        # Tabela de professores
        colunas = ('ID', 'Nome', 'CPF', 'Email', 'Telefone', 'Especialidade', 'Salário', 'Status')
        self.tree_professores = self.criar_tabela(parent, colunas)

        # Carregar dados
        self.carregar_dados_professores()

    def carregar_aba_cadastro_professores(self, parent):
        """Carrega aba de cadastro de professores"""
        form_frame = tk.Frame(parent, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Container com scroll
        canvas = tk.Canvas(form_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Formulário de cadastro
        self.criar_formulario_professor(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def carregar_aba_relatorios_professores(self, parent):
        """Carrega aba de relatórios de professores"""
        relatorios_frame = tk.Frame(parent, bg='#f8f9fa')
        relatorios_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(relatorios_frame, text="Relatórios de Professores", font=('Arial', 16, 'bold'),
                 bg='#f8f9fa', fg='#0046AD').pack(anchor='w', pady=(0, 20))

        # Grid de relatórios
        grid_frame = tk.Frame(relatorios_frame, bg='#f8f9fa')
        grid_frame.pack(fill=tk.BOTH, expand=True)

        relatorios = [
            ("📋 Lista Completa", self.gerar_relatorio_professores_completo,
             "Lista completa de todos os professores cadastrados"),
            ("🎓 Professores por Disciplina", self.gerar_relatorio_professores_disciplina,
             "Relação de professores organizada por disciplina"),
            ("💰 Folha de Pagamento", self.gerar_relatorio_folha_pagamento,
             "Relatório com dados salariais dos professores"),
            ("📅 Aniversariantes", self.gerar_relatorio_aniversariantes_professores,
             "Lista de aniversariantes do mês"),
            ("📊 Estatísticas", self.gerar_relatorio_estatisticas_professores,
             "Estatísticas e métricas do corpo docente"),
        ]

        for i, (titulo, comando, descricao) in enumerate(relatorios):
            row = i // 3
            col = i % 3

            card = tk.Frame(grid_frame, bg='white', relief='flat', bd=1,
                            highlightbackground='#e0e0e0', highlightthickness=1)
            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            card.configure(width=250, height=120)

            tk.Label(card, text=titulo, font=('Arial', 12, 'bold'),
                     bg='white', fg='#0046AD').pack(pady=(15, 5))

            tk.Label(card, text=descricao, font=('Arial', 9),
                     bg='white', fg='#666666', wraplength=220).pack(pady=5, padx=10)

            ModernButton(card, text="Gerar Relatório", command=comando,
                         color='#0046AD', font=('Arial', 10)).pack(pady=10)

        for i in range(3):
            grid_frame.columnconfigure(i, weight=1)
        for i in range(2):
            grid_frame.rowconfigure(i, weight=1)

    def criar_formulario_professor(self, parent):
        """Cria formulário de cadastro de professor"""
        # Dados Pessoais
        dados_frame = tk.LabelFrame(parent, text="Dados Pessoais", font=('Arial', 12, 'bold'),
                                    bg='white', fg='#0046AD', padx=15, pady=15)
        dados_frame.pack(fill=tk.X, pady=10)

        campos_dados = [
            ("Nome Completo*", "entry", None),
            ("CPF", "entry", None),
            ("RG", "entry", None),
            ("Data Nascimento", "entry", None),
            ("Email", "entry", None),
            ("Telefone", "entry", None),
            ("Celular", "entry", None),
            ("Endereço", "entry", None),
        ]

        self.entries_professor = {}
        linha = 0
        coluna = 0

        for label, tipo, valores in campos_dados:
            tk.Label(dados_frame, text=label, font=('Arial', 10, 'bold'),
                     bg='white', fg='#0046AD').grid(row=linha, column=coluna * 2, sticky='w', pady=5, padx=5)

            if tipo == "entry":
                entry = tk.Entry(dados_frame, width=25, font=('Arial', 10), relief='solid', bd=1)
                entry.grid(row=linha, column=coluna * 2 + 1, pady=5, padx=5, sticky='ew')
                self.entries_professor[label] = entry

            coluna += 1
            if coluna >= 2:
                coluna = 0
                linha += 1

        # Dados Profissionais
        profissional_frame = tk.LabelFrame(parent, text="Dados Profissionais", font=('Arial', 12, 'bold'),
                                           bg='white', fg='#0046AD', padx=15, pady=15)
        profissional_frame.pack(fill=tk.X, pady=10)

        campos_profissional = [
            ("Formação Acadêmica", "entry", None),
            ("Especialidade", "entry", None),
            ("Data Contratação", "entry", None),
            ("Salário (R$)", "entry", None),
        ]

        linha = 0
        for label, tipo, valores in campos_profissional:
            tk.Label(profissional_frame, text=label, font=('Arial', 10, 'bold'),
                     bg='white', fg='#0046AD').grid(row=linha, column=0, sticky='w', pady=5, padx=5)

            if tipo == "entry":
                entry = tk.Entry(profissional_frame, width=40, font=('Arial', 10), relief='solid', bd=1)
                entry.grid(row=linha, column=1, pady=5, padx=5, sticky='ew', columnspan=3)
                self.entries_professor[label] = entry

            linha += 1

        # Dados Bancários
        bancario_frame = tk.LabelFrame(parent, text="Dados Bancários", font=('Arial', 12, 'bold'),
                                       bg='white', fg='#0046AD', padx=15, pady=15)
        bancario_frame.pack(fill=tk.X, pady=10)

        campos_bancarios = [
            ("Banco", "entry", None),
            ("Agência", "entry", None),
            ("Conta", "entry", None),
            ("PIS", "entry", None),
            ("CTPS", "entry", None),
        ]

        linha = 0
        coluna = 0
        for label, tipo, valores in campos_bancarios:
            tk.Label(bancario_frame, text=label, font=('Arial', 10, 'bold'),
                     bg='white', fg='#0046AD').grid(row=linha, column=coluna * 2, sticky='w', pady=5, padx=5)

            if tipo == "entry":
                entry = tk.Entry(bancario_frame, width=20, font=('Arial', 10), relief='solid', bd=1)
                entry.grid(row=linha, column=coluna * 2 + 1, pady=5, padx=5, sticky='ew')
                self.entries_professor[label] = entry

            coluna += 1
            if coluna >= 2:
                coluna = 0
                linha += 1

        # Status
        status_frame = tk.Frame(parent, bg='white')
        status_frame.pack(fill=tk.X, pady=10)

        tk.Label(status_frame, text="Status:", font=('Arial', 10, 'bold'),
                 bg='white', fg='#0046AD').pack(side=tk.LEFT, padx=5)

        self.status_professor = ttk.Combobox(status_frame, values=['Ativo', 'Inativo'],
                                             state='readonly', width=15)
        self.status_professor.set('Ativo')
        self.status_professor.pack(side=tk.LEFT, padx=5)

        # Botões
        botoes_frame = tk.Frame(parent, bg='white')
        botoes_frame.pack(pady=20)

        ModernButton(botoes_frame, text="🗑️ Limpar",
                     command=self.limpar_formulario_professor,
                     color='#666666').pack(side=tk.LEFT, padx=10)

        ModernButton(botoes_frame, text="💾 Salvar Professor",
                     command=self.salvar_professor,
                     color='#0046AD').pack(side=tk.LEFT, padx=10)

        # Configurar pesos das colunas
        for frame in [dados_frame, profissional_frame, bancario_frame]:
            frame.columnconfigure(1, weight=1)
            frame.columnconfigure(3, weight=1)

    def limpar_formulario_professor(self):
        """Limpa todos os campos do formulário de professor"""
        for entry in self.entries_professor.values():
            if isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)

        self.status_professor.set('Ativo')

    def salvar_professor(self):
        """Salva os dados do professor no banco de dados"""
        try:
            # Validar campos obrigatórios
            if not self.entries_professor["Nome Completo*"].get().strip():
                messagebox.showwarning("Aviso", "O campo Nome Completo é obrigatório!")
                return

            # Coletar dados
            dados = {
                'nome': self.entries_professor["Nome Completo*"].get().strip(),
                'cpf': self.entries_professor["CPF"].get().strip(),
                'rg': self.entries_professor["RG"].get().strip(),
                'data_nascimento': self.entries_professor["Data Nascimento"].get().strip(),
                'email': self.entries_professor["Email"].get().strip(),
                'telefone': self.entries_professor["Telefone"].get().strip(),
                'celular': self.entries_professor["Celular"].get().strip(),
                'endereco': self.entries_professor["Endereço"].get().strip(),
                'formacao': self.entries_professor["Formação Acadêmica"].get().strip(),
                'especialidade': self.entries_professor["Especialidade"].get().strip(),
                'data_contratacao': self.entries_professor["Data Contratação"].get().strip(),
                'salario': float(self.entries_professor["Salário (R$)"].get() or 0),
                'banco': self.entries_professor["Banco"].get().strip(),
                'agencia': self.entries_professor["Agência"].get().strip(),
                'conta': self.entries_professor["Conta"].get().strip(),
                'pis': self.entries_professor["PIS"].get().strip(),
                'ctps': self.entries_professor["CTPS"].get().strip(),
                'status': self.status_professor.get()
            }

            # Verificar se CPF já existe
            if dados['cpf']:
                self.cursor.execute("SELECT id FROM professores WHERE cpf = ?", (dados['cpf'],))
                if self.cursor.fetchone():
                    messagebox.showerror("Erro", "CPF já cadastrado no sistema!")
                    return

            # Inserir no banco
            self.cursor.execute('''
                INSERT INTO professores (
                    nome, cpf, rg, data_nascimento, email, telefone, celular, endereco,
                    formacao, especialidade, data_contratacao, salario, banco, agencia,
                    conta, pis, ctps, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (dados['nome'], dados['cpf'], dados['rg'], dados['data_nascimento'],
                  dados['email'], dados['telefone'], dados['celular'], dados['endereco'],
                  dados['formacao'], dados['especialidade'], dados['data_contratacao'],
                  dados['salario'], dados['banco'], dados['agencia'], dados['conta'],
                  dados['pis'], dados['ctps'], dados['status']))

            self.conn.commit()

            # Registrar log
            self.registrar_log('CADASTRO', 'Professores', f'Cadastrou professor: {dados["nome"]}')

            messagebox.showinfo("Sucesso", "Professor cadastrado com sucesso!")
            self.limpar_formulario_professor()
            self.carregar_dados_professores()

        except sqlite3.IntegrityError as e:
            messagebox.showerror("Erro", f"Erro de integridade: {str(e)}")
        except ValueError as e:
            messagebox.showerror("Erro", "Valor do salário inválido!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar professor: {str(e)}")

    def carregar_dados_professores(self, query=None, filtro_status='Ativo'):
        """Carrega dados dos professores na tabela"""
        for item in self.tree_professores.get_children():
            self.tree_professores.delete(item)

        sql = '''
            SELECT id, nome, cpf, email, telefone, especialidade, salario, status
            FROM professores
            WHERE 1=1
        '''
        params = []

        if query:
            sql += ' AND (nome LIKE ? OR cpf LIKE ? OR email LIKE ? OR especialidade LIKE ?)'
            params.extend([f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'])

        if filtro_status != 'Todos':
            sql += ' AND status = ?'
            params.append(filtro_status)

        sql += ' ORDER BY nome'

        self.cursor.execute(sql, params)
        professores = self.cursor.fetchall()

        for prof in professores:
            # Formatar salário
            prof_list = list(prof)
            prof_list[6] = f"R$ {prof[6]:.2f}" if prof[6] else "R$ 0,00"
            self.tree_professores.insert('', tk.END, values=prof_list)

    def buscar_professores(self, event=None):
        """Busca professores na tabela"""
        query = self.search_var_professores.get()
        self.carregar_dados_professores(query)

    def aplicar_filtros_professores(self):
        """Aplica filtros na tabela de professores"""
        status = self.filtro_status_professores.get()
        self.carregar_dados_professores(None, status)

    def editar_professor(self):
        """Edita professor selecionado"""
        selection = self.tree_professores.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um professor para editar!")
            return

        item = self.tree_professores.item(selection[0])
        professor_id = item['values'][0]
        self.abrir_edicao_professor(professor_id)

    def excluir_professor(self):
        """Exclui professor selecionado"""
        selection = self.tree_professores.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um professor para excluir!")
            return

        item = self.tree_professores.item(selection[0])
        professor_id, nome = item['values'][0], item['values'][1]

        resposta = messagebox.askyesno("Confirmar Exclusão",
                                       f"Tem certeza que deseja excluir o professor {nome}?\n\nEsta ação não pode ser desfeita!")

        if resposta:
            try:
                # Verificar se o professor está vinculado a alguma disciplina
                self.cursor.execute("SELECT COUNT(*) FROM disciplinas WHERE professor_id = ?", (professor_id,))
                if self.cursor.fetchone()[0] > 0:
                    messagebox.showerror("Erro",
                                         "Não é possível excluir o professor pois ele está vinculado a disciplinas!")
                    return

                self.cursor.execute("DELETE FROM professores WHERE id = ?", (professor_id,))
                self.conn.commit()

                # Registrar log
                self.registrar_log('EXCLUSAO', 'Professores', f'Excluiu professor: {nome}')

                messagebox.showinfo("Sucesso", "Professor excluído com sucesso!")
                self.carregar_dados_professores()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir professor: {str(e)}")

    def exportar_professores(self):
        """Exporta lista de professores para CSV"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Exportar lista de professores"
            )

            if filename:
                self.cursor.execute('''
                    SELECT nome, cpf, email, telefone, celular, formacao, especialidade,
                           data_contratacao, salario, banco, agencia, conta, status
                    FROM professores
                    ORDER BY nome
                ''')

                professores = self.cursor.fetchall()

                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Nome', 'CPF', 'Email', 'Telefone', 'Celular', 'Formação',
                                     'Especialidade', 'Data Contratação', 'Salário', 'Banco',
                                     'Agência', 'Conta', 'Status'])
                    writer.writerows(professores)

                messagebox.showinfo("Sucesso", f"Lista de professores exportada para: {filename}")

                # Registrar log
                self.registrar_log('EXPORTACAO', 'Professores', 'Exportou lista de professores para CSV')

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar professores: {str(e)}")

    def imprimir_lista_professores(self):
        """Gera PDF com lista de professores"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Salvar lista de professores como PDF"
            )

            if filename:
                self.cursor.execute('''
                    SELECT nome, cpf, email, telefone, especialidade, salario, status
                    FROM professores
                    ORDER BY nome
                ''')

                professores = self.cursor.fetchall()

                # Criar PDF
                c = canvas.Canvas(filename, pagesize=A4)
                width, height = A4

                # Cabeçalho
                c.setFont("Helvetica-Bold", 16)
                c.drawString(50, height - 50, "EXTERNATO COLÉGIO OBJETIVO")
                c.setFont("Helvetica", 12)
                c.drawString(50, height - 70, "Lista de Professores")
                c.drawString(50, height - 85, f"Data: {date.today().strftime('%d/%m/%Y')}")

                # Tabela
                data = [['Nome', 'CPF', 'Email', 'Telefone', 'Especialidade', 'Salário', 'Status']]
                for prof in professores:
                    salario = f"R$ {prof[5]:.2f}" if prof[5] else "R$ 0,00"
                    data.append([prof[0], prof[1] or '', prof[2] or '', prof[3] or '', prof[4] or '', salario, prof[6]])

                table = Table(data, colWidths=[100, 80, 100, 80, 80, 70, 60])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0046AD')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))

                table.wrapOn(c, width, height)
                table.drawOn(c, 30, height - 150)

                c.save()
                messagebox.showinfo("Sucesso", f"PDF gerado: {filename}")

                # Registrar log
                self.registrar_log('IMPRESSAO', 'Professores', 'Gerou PDF com lista de professores')

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar PDF: {str(e)}")

    # ========== FUNÇÕES DE RELATÓRIOS DE PROFESSORES ==========

    def gerar_relatorio_professores_completo(self):
        """Gera relatório completo de professores"""
        try:
            self.cursor.execute('''
                SELECT nome, cpf, email, telefone, celular, formacao, especialidade,
                       data_contratacao, salario, endereco, status
                FROM professores
                ORDER BY nome
            ''')

            professores = self.cursor.fetchall()

            relatorio = "RELATÓRIO COMPLETO DE PROFESSORES\n"
            relatorio += "=" * 50 + "\n\n"
            relatorio += f"Total de professores: {len(professores)}\n"
            relatorio += f"Data do relatório: {date.today().strftime('%d/%m/%Y')}\n\n"

            for prof in professores:
                relatorio += f"Nome: {prof[0]}\n"
                relatorio += f"CPF: {prof[1] or 'Não informado'}\n"
                relatorio += f"Email: {prof[2] or 'Não informado'}\n"
                relatorio += f"Telefone: {prof[3] or 'Não informado'} | Celular: {prof[4] or 'Não informado'}\n"
                relatorio += f"Formação: {prof[5] or 'Não informada'}\n"
                relatorio += f"Especialidade: {prof[6] or 'Não informada'}\n"
                relatorio += f"Data Contratação: {prof[7] or 'Não informada'}\n"
                relatorio += f"Salário: R$ {prof[8]:.2f if prof[8] else 0:.2f}\n"
                relatorio += f"Endereço: {prof[9] or 'Não informado'}\n"
                relatorio += f"Status: {prof[10]}\n"
                relatorio += "-" * 50 + "\n"

            self.mostrar_relatorio("Relatório Completo de Professores", relatorio)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")

    def gerar_relatorio_professores_disciplina(self):
        """Gera relatório de professores por disciplina"""
        try:
            self.cursor.execute('''
                SELECT p.nome, p.especialidade, d.nome as disciplina, t.nome as turma
                FROM professores p
                LEFT JOIN disciplinas d ON p.id = d.professor_id
                LEFT JOIN turmas t ON d.turma_id = t.id
                WHERE p.status = 'Ativo'
                ORDER BY p.nome, d.nome
            ''')

            professores_disc = self.cursor.fetchall()

            relatorio = "PROFESSORES E SUAS DISCIPLINAS\n"
            relatorio += "=" * 40 + "\n\n"

            professor_atual = None
            for professor, especialidade, disciplina, turma in professores_disc:
                if professor != professor_atual:
                    if professor_atual:
                        relatorio += "\n"
                    professor_atual = professor
                    relatorio += f"PROFESSOR: {professor}\n"
                    relatorio += f"Especialidade: {especialidade or 'Não informada'}\n"
                    relatorio += "Disciplinas:\n"

                if disciplina:
                    relatorio += f"  • {disciplina}"
                    if turma:
                        relatorio += f" ({turma})"
                    relatorio += "\n"
                else:
                    relatorio += "  • Nenhuma disciplina atribuída\n"

            self.mostrar_relatorio("Professores por Disciplina", relatorio)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")

    def gerar_relatorio_folha_pagamento(self):
        """Gera relatório da folha de pagamento"""
        try:
            self.cursor.execute('''
                SELECT nome, especialidade, salario, data_contratacao, status
                FROM professores
                WHERE status = 'Ativo'
                ORDER BY salario DESC
            ''')

            folha = self.cursor.fetchall()

            total_salarios = sum(prof[2] for prof in folha if prof[2])

            relatorio = "FOLHA DE PAGAMENTO - PROFESSORES\n"
            relatorio += "=" * 50 + "\n\n"

            relatorio += f"Total de professores ativos: {len(folha)}\n"
            relatorio += f"Total da folha: R$ {total_salarios:.2f}\n"
            relatorio += f"Média salarial: R$ {total_salarios / len(folha) if folha else 0:.2f}\n\n"

            relatorio += "DETALHAMENTO:\n"
            relatorio += "-" * 50 + "\n"

            for nome, especialidade, salario, data_contratacao, status in folha:
                relatorio += f"{nome}\n"
                relatorio += f"  Especialidade: {especialidade or 'Não informada'}\n"
                relatorio += f"  Salário: R$ {salario:.2f if salario else 0:.2f}\n"
                relatorio += f"  Data Contratação: {data_contratacao or 'Não informada'}\n\n"

            self.mostrar_relatorio("Folha de Pagamento", relatorio)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")

    def gerar_relatorio_aniversariantes_professores(self):
        """Gera relatório de aniversariantes do mês"""
        try:
            mes_atual = datetime.now().month
            self.cursor.execute('''
                SELECT nome, data_nascimento, email, telefone, especialidade
                FROM professores
                WHERE strftime('%m', data_nascimento) = ?
                ORDER BY strftime('%d', data_nascimento), nome
            ''', (str(mes_atual).zfill(2),))

            aniversariantes = self.cursor.fetchall()

            relatorio = f"ANIVERSARIANTES DO MÊS {mes_atual} - PROFESSORES\n"
            relatorio += "=" * 50 + "\n\n"

            if aniversariantes:
                for nome, data_nasc, email, telefone, especialidade in aniversariantes:
                    if data_nasc:
                        dia = datetime.strptime(data_nasc, '%Y-%m-%d').day
                        relatorio += f"• {dia:02d}/{mes_atual:02d} - {nome}"
                        relatorio += f" | {especialidade or 'Sem especialidade'}"
                        relatorio += f" | {telefone or 'Sem telefone'}\n"
            else:
                relatorio += "Nenhum aniversariante este mês.\n"

            self.mostrar_relatorio("Aniversariantes - Professores", relatorio)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")

    def gerar_relatorio_estatisticas_professores(self):
        """Gera relatório de estatísticas dos professores"""
        try:
            # Total por status
            self.cursor.execute('''
                SELECT status, COUNT(*) as total
                FROM professores
                GROUP BY status
            ''')
            status_stats = self.cursor.fetchall()

            # Total por especialidade
            self.cursor.execute('''
                SELECT especialidade, COUNT(*) as total
                FROM professores
                WHERE especialidade IS NOT NULL AND especialidade != ''
                GROUP BY especialidade
                ORDER BY total DESC
            ''')
            especialidade_stats = self.cursor.fetchall()

            # Tempo médio de casa
            self.cursor.execute('''
                SELECT AVG((julianday('now') - julianday(data_contratacao)) / 365.25)
                FROM professores
                WHERE data_contratacao IS NOT NULL AND status = 'Ativo'
            ''')
            tempo_medio = self.cursor.fetchone()[0] or 0

            relatorio = "ESTATÍSTICAS DO CORPO DOCENTE\n"
            relatorio += "=" * 40 + "\n\n"

            relatorio += "DISTRIBUIÇÃO POR STATUS:\n"
            for status, total in status_stats:
                relatorio += f"• {status}: {total} professores\n"

            relatorio += f"\nTEMPO MÉDIO DE CASA: {tempo_medio:.1f} anos\n"

            relatorio += "\nDISTRIBUIÇÃO POR ESPECIALIDADE:\n"
            for especialidade, total in especialidade_stats:
                relatorio += f"• {especialidade}: {total} professores\n"

            self.mostrar_relatorio("Estatísticas de Professores", relatorio)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")

    # ========== FUNÇÕES AUXILIARES ==========

    def abrir_configuracoes(self):
        """Abre janela de configurações do sistema"""
        self.carregar_configuracoes_sistema()

    def novo_aluno(self):
        """Abre cadastro de novo aluno"""
        self.carregar_gestao_alunos()
        # Seleciona a aba de cadastro
        notebook = self.content_frame.winfo_children()[0]
        if isinstance(notebook, ttk.Notebook):
            notebook.select(1)  # Seleciona segunda aba (cadastro)

    def novo_professor(self):
        """Abre cadastro de novo professor"""
        self.carregar_gestao_professores()
        # Seleciona a aba de cadastro
        notebook = self.content_frame.winfo_children()[0]
        if isinstance(notebook, ttk.Notebook):
            notebook.select(1)  # Seleciona segunda aba (cadastro)

    def nova_turma(self):
        """Abre cadastro de nova turma"""
        self.carregar_gestao_turmas()

    def lancar_notas(self):
        """Abre lançamento de notas"""
        self.carregar_sistema_notas()

    def nova_aula_diario(self):
        """Abre registro de nova aula"""
        self.carregar_diario_classe()

    def novo_comunicado(self):
        """Abre criação de novo comunicado"""
        self.carregar_comunicados_avisos()

    def novo_evento(self):
        """Abre criação de novo evento"""
        self.carregar_calendario_escolar()

    def gerar_relatorio_rapido(self):
        """Gera relatório rápido do sistema"""
        try:
            # Estatísticas rápidas
            total_alunos = self.cursor.execute("SELECT COUNT(*) FROM alunos WHERE status='Ativo'").fetchone()[0]
            total_professores = self.cursor.execute("SELECT COUNT(*) FROM professores WHERE status='Ativo'").fetchone()[
                0]
            total_turmas = self.cursor.execute("SELECT COUNT(*) FROM turmas WHERE status='Ativa'").fetchone()[0]

            relatorio = "RELATÓRIO RÁPIDO DO SISTEMA\n"
            relatorio += "=" * 35 + "\n\n"
            relatorio += f"📊 ESTATÍSTICAS GERAIS:\n"
            relatorio += f"• Alunos ativos: {total_alunos}\n"
            relatorio += f"• Professores ativos: {total_professores}\n"
            relatorio += f"• Turmas ativas: {total_turmas}\n"
            relatorio += f"• Data: {date.today().strftime('%d/%m/%Y')}\n"
            relatorio += f"• Usuário: {self.usuario_nome}\n"

            self.mostrar_relatorio("Relatório Rápido", relatorio)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")

    # ========== MÓDULO GESTÃO DE TURMAS (COMPLETO) ==========

    def carregar_gestao_turmas(self):
        """Carrega o módulo completo de gestão de turmas"""
        self.limpar_conteudo()
        self.ativar_botao("🏫 Gestão de Turmas")
        self.registrar_log('ACESSO', 'Gestão de Turmas', 'Acessou módulo de gestão de turmas')

        # Título
        title_frame = tk.Frame(self.content_frame, bg='#f8f9fa')
        title_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(title_frame, text="Gestão de Turmas", font=('Arial', 24, 'bold'),
                 bg='#f8f9fa', fg='#0046AD').pack(anchor='w')

        tk.Label(title_frame, text="Cadastro, consulta e gestão completa das turmas escolares",
                 font=('Arial', 12), bg='#f8f9fa', fg='#666666').pack(anchor='w')

        # Notebook com abas
        notebook = ttk.Notebook(self.content_frame, style='Custom.TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Aba 1: Lista de Turmas
        aba_lista = ttk.Frame(notebook)
        notebook.add(aba_lista, text="🏫 Lista de Turmas")

        self.carregar_aba_lista_turmas(aba_lista)

        # Aba 2: Cadastro de Turmas
        aba_cadastro = ttk.Frame(notebook)
        notebook.add(aba_cadastro, text="➕ Nova Turma")

        self.carregar_aba_cadastro_turmas(aba_cadastro)

        # Aba 3: Alunos por Turma
        aba_alunos = ttk.Frame(notebook)
        notebook.add(aba_alunos, text="👨🎓 Alunos por Turma")

        self.carregar_aba_alunos_turma(aba_alunos)

    def carregar_aba_lista_turmas(self, parent):
        """Carrega aba de lista de turmas"""
        # Barra de ferramentas
        botoes = [
            ("🔍 Buscar", self.buscar_turmas, '#0046AD'),
            ("📝 Editar", self.editar_turma, '#0046AD'),
            ("🗑️ Excluir", self.excluir_turma, '#FF6B6B'),
            ("📋 Exportar", self.exportar_turmas, '#0046AD'),
            ("🖨️ Imprimir", self.imprimir_lista_turmas, '#0046AD'),
        ]
        toolbar = self.criar_toolbar(parent, botoes)

        # Filtros
        filtros_frame = tk.Frame(toolbar, bg='white')
        filtros_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        tk.Label(filtros_frame, text="Filtro:", font=('Arial', 9),
                 bg='white').pack(side=tk.LEFT, padx=5)

        self.filtro_status_turmas = ttk.Combobox(filtros_frame,
                                                 values=['Todas', 'Ativa', 'Inativa'],
                                                 state='readonly', width=12)
        self.filtro_status_turmas.pack(side=tk.LEFT, padx=5)
        self.filtro_status_turmas.set('Ativa')

        self.filtro_turno_turmas = ttk.Combobox(filtros_frame,
                                                values=['Todos', 'Manhã', 'Tarde', 'Noite'],
                                                state='readonly', width=12)
        self.filtro_turno_turmas.pack(side=tk.LEFT, padx=5)
        self.filtro_turno_turmas.set('Todos')

        ModernButton(filtros_frame, text="Aplicar",
                     command=self.aplicar_filtros_turmas,
                     color='#0046AD').pack(side=tk.LEFT, padx=5)

        # Campo de busca
        search_frame = tk.Frame(toolbar, bg='white')
        search_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.search_var_turmas = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var_turmas,
                                width=30, font=('Arial', 10), relief='solid', bd=1)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind('<KeyRelease>', self.buscar_turmas)

        # Tabela de turmas
        colunas = ('ID', 'Nome', 'Série', 'Turno', 'Professor', 'Capacidade', 'Sala', 'Alunos', 'Status')
        self.tree_turmas = self.criar_tabela(parent, colunas)

        # Carregar dados
        self.carregar_dados_turmas()

    def carregar_dados_turmas(self, query=None, filtro_status='Ativa', filtro_turno='Todos'):
        """Carrega dados das turmas na tabela"""
        for item in self.tree_turmas.get_children():
            self.tree_turmas.delete(item)

        sql = '''
            SELECT t.id, t.nome, t.serie, t.turno, p.nome, t.capacidade, t.sala,
                   (SELECT COUNT(*) FROM matriculas m WHERE m.turma_id = t.id AND m.status = 'Ativa'),
                   t.status
            FROM turmas t
            LEFT JOIN professores p ON t.professor_id = p.id
            WHERE 1=1
        '''
        params = []

        if query:
            sql += ' AND (t.nome LIKE ? OR t.serie LIKE ? OR p.nome LIKE ? OR t.sala LIKE ?)'
            params.extend([f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'])

        if filtro_status != 'Todas':
            sql += ' AND t.status = ?'
            params.append(filtro_status)

        if filtro_turno != 'Todos':
            sql += ' AND t.turno = ?'
            params.append(filtro_turno)

        sql += ' ORDER BY t.serie, t.nome'

        self.cursor.execute(sql, params)
        turmas = self.cursor.fetchall()

        for turma in turmas:
            self.tree_turmas.insert('', tk.END, values=turma)

    def carregar_aba_cadastro_turmas(self, parent):
        """Carrega aba de cadastro de turmas"""
        form_frame = tk.Frame(parent, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Container com scroll
        canvas = tk.Canvas(form_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Formulário de cadastro
        self.criar_formulario_turma(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def criar_formulario_turma(self, parent):
        """Cria formulário de cadastro de turma"""
        # Dados Básicos
        dados_frame = tk.LabelFrame(parent, text="Dados da Turma", font=('Arial', 12, 'bold'),
                                    bg='white', fg='#0046AD', padx=15, pady=15)
        dados_frame.pack(fill=tk.X, pady=10)

        campos_dados = [
            ("Nome da Turma*", "entry", None),
            ("Série/Ano*", "combo", ['1º Ano', '2º Ano', '3º Ano', '4º Ano', '5º Ano',
                                     '6º Ano', '7º Ano', '8º Ano', '9º Ano', '1º EM', '2º EM', '3º EM']),
            ("Turno*", "combo", ['Manhã', 'Tarde', 'Noite']),
            ("Professor Responsável", "combo", self.obter_professores_combo()),
            ("Capacidade*", "entry", None),
            ("Sala", "entry", None),
            ("Ano Letivo", "entry", None),
        ]

        self.entries_turma = {}
        linha = 0
        coluna = 0

        for label, tipo, valores in campos_dados:
            tk.Label(dados_frame, text=label, font=('Arial', 10, 'bold'),
                     bg='white', fg='#0046AD').grid(row=linha, column=coluna * 2, sticky='w', pady=5, padx=5)

            if tipo == "entry":
                entry = tk.Entry(dados_frame, width=25, font=('Arial', 10), relief='solid', bd=1)
                entry.grid(row=linha, column=coluna * 2 + 1, pady=5, padx=5, sticky='ew')
                self.entries_turma[label] = entry
            elif tipo == "combo":
                combo = ttk.Combobox(dados_frame, values=valores, state='readonly', width=22)
                combo.grid(row=linha, column=coluna * 2 + 1, pady=5, padx=5, sticky='ew')
                self.entries_turma[label] = combo

            coluna += 1
            if coluna >= 2:
                coluna = 0
                linha += 1

        # Horários
        horarios_frame = tk.LabelFrame(parent, text="Horários de Aula", font=('Arial', 12, 'bold'),
                                       bg='white', fg='#0046AD', padx=15, pady=15)
        horarios_frame.pack(fill=tk.X, pady=10)

        campos_horarios = [
            ("Horário Início", "entry", None),
            ("Horário Fim", "entry", None),
            ("Dias da Semana", "combo", ['Segunda a Sexta', 'Segunda a Sábado', 'Personalizado']),
        ]

        linha = 0
        for label, tipo, valores in campos_horarios:
            tk.Label(horarios_frame, text=label, font=('Arial', 10, 'bold'),
                     bg='white', fg='#0046AD').grid(row=linha, column=0, sticky='w', pady=5, padx=5)

            if tipo == "entry":
                entry = tk.Entry(horarios_frame, width=30, font=('Arial', 10), relief='solid', bd=1)
                entry.grid(row=linha, column=1, pady=5, padx=5, sticky='ew', columnspan=3)
                self.entries_turma[label] = entry
            elif tipo == "combo":
                combo = ttk.Combobox(horarios_frame, values=valores, state='readonly', width=27)
                combo.grid(row=linha, column=1, pady=5, padx=5, sticky='ew', columnspan=3)
                self.entries_turma[label] = combo

            linha += 1

        # Status
        status_frame = tk.Frame(parent, bg='white')
        status_frame.pack(fill=tk.X, pady=10)

        tk.Label(status_frame, text="Status:", font=('Arial', 10, 'bold'),
                 bg='white', fg='#0046AD').pack(side=tk.LEFT, padx=5)

        self.status_turma = ttk.Combobox(status_frame, values=['Ativa', 'Inativa'],
                                         state='readonly', width=15)
        self.status_turma.set('Ativa')
        self.status_turma.pack(side=tk.LEFT, padx=5)

        # Botões
        botoes_frame = tk.Frame(parent, bg='white')
        botoes_frame.pack(pady=20)

        ModernButton(botoes_frame, text="🗑️ Limpar",
                     command=self.limpar_formulario_turma,
                     color='#666666').pack(side=tk.LEFT, padx=10)

        ModernButton(botoes_frame, text="💾 Salvar Turma",
                     command=self.salvar_turma,
                     color='#0046AD').pack(side=tk.LEFT, padx=10)

        # Configurar pesos das colunas
        dados_frame.columnconfigure(1, weight=1)
        dados_frame.columnconfigure(3, weight=1)
        horarios_frame.columnconfigure(1, weight=1)

    def obter_professores_combo(self):
        """Retorna lista de professores para combobox"""
        self.cursor.execute("SELECT nome FROM professores WHERE status='Ativo' ORDER BY nome")
        return [''] + [prof[0] for prof in self.cursor.fetchall()]

    def limpar_formulario_turma(self):
        """Limpa todos os campos do formulário de turma"""
        for entry in self.entries_turma.values():
            if isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)
            elif isinstance(entry, ttk.Combobox):
                entry.set('')

        self.status_turma.set('Ativa')
        # Definir ano letivo atual como padrão
        if "Ano Letivo" in self.entries_turma:
            self.entries_turma["Ano Letivo"].insert(0, str(datetime.now().year))

    def salvar_turma(self):
        """Salva os dados da turma no banco de dados"""
        try:
            # Validar campos obrigatórios
            if not self.entries_turma["Nome da Turma*"].get().strip():
                messagebox.showwarning("Aviso", "O campo Nome da Turma é obrigatório!")
                return
            if not self.entries_turma["Série/Ano*"].get().strip():
                messagebox.showwarning("Aviso", "O campo Série/Ano é obrigatório!")
                return
            if not self.entries_turma["Turno*"].get().strip():
                messagebox.showwarning("Aviso", "O campo Turno é obrigatório!")
                return

            # Obter ID do professor
            professor_nome = self.entries_turma["Professor Responsável"].get()
            professor_id = None
            if professor_nome:
                self.cursor.execute("SELECT id FROM professores WHERE nome = ?", (professor_nome,))
                result = self.cursor.fetchone()
                professor_id = result[0] if result else None

            # Coletar dados
            dados = {
                'nome': self.entries_turma["Nome da Turma*"].get().strip(),
                'serie': self.entries_turma["Série/Ano*"].get().strip(),
                'turno': self.entries_turma["Turno*"].get().strip(),
                'professor_id': professor_id,
                'capacidade': int(self.entries_turma["Capacidade*"].get() or 0),
                'sala': self.entries_turma["Sala"].get().strip(),
                'ano_letivo': self.entries_turma["Ano Letivo"].get().strip() or str(datetime.now().year),
                'horario_inicio': self.entries_turma["Horário Início"].get().strip(),
                'horario_fim': self.entries_turma["Horário Fim"].get().strip(),
                'dias_semana': self.entries_turma["Dias da Semana"].get().strip(),
                'status': self.status_turma.get()
            }

            # Verificar se turma já existe
            self.cursor.execute("SELECT id FROM turmas WHERE nome = ? AND ano_letivo = ?",
                                (dados['nome'], dados['ano_letivo']))
            if self.cursor.fetchone():
                messagebox.showerror("Erro", "Já existe uma turma com este nome no ano letivo!")
                return

            # Inserir no banco
            self.cursor.execute('''
                INSERT INTO turmas (
                    nome, serie, turno, professor_id, capacidade, sala, ano_letivo,
                    horario_inicio, horario_fim, dias_semana, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (dados['nome'], dados['serie'], dados['turno'], dados['professor_id'],
                  dados['capacidade'], dados['sala'], dados['ano_letivo'],
                  dados['horario_inicio'], dados['horario_fim'], dados['dias_semana'],
                  dados['status']))

            self.conn.commit()

            # Registrar log
            self.registrar_log('CADASTRO', 'Turmas', f'Cadastrou turma: {dados["nome"]}')

            messagebox.showinfo("Sucesso", "Turma cadastrada com sucesso!")
            self.limpar_formulario_turma()
            self.carregar_dados_turmas()

        except ValueError as e:
            messagebox.showerror("Erro", "Capacidade deve ser um número válido!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar turma: {str(e)}")

    def carregar_aba_alunos_turma(self, parent):
        """Carrega aba de alunos por turma"""
        # Frame de seleção
        selecao_frame = tk.Frame(parent, bg='white', relief='flat', bd=1, padx=20, pady=15)
        selecao_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(selecao_frame, text="Selecionar Turma:", font=('Arial', 11, 'bold'),
                 bg='white', fg='#0046AD').pack(side=tk.LEFT, padx=5)

        self.turma_selecionada = ttk.Combobox(selecao_frame,
                                              values=self.obter_turmas_combo(),
                                              state='readonly', width=30)
        self.turma_selecionada.pack(side=tk.LEFT, padx=5)
        self.turma_selecionada.bind('<<ComboboxSelected>>', self.carregar_alunos_turma_selecionada)

        ModernButton(selecao_frame, text="🔄 Atualizar",
                     command=self.carregar_alunos_turma_selecionada,
                     color='#0046AD').pack(side=tk.LEFT, padx=5)

        # Tabela de alunos da turma
        colunas = ('ID', 'Nome', 'CPF', 'Email', 'Telefone', 'Data Matrícula', 'Status')
        self.tree_alunos_turma = self.criar_tabela(parent, colunas)

        # Informações da turma
        self.info_turma_label = tk.Label(parent, text="Selecione uma turma para ver os alunos",
                                         font=('Arial', 11), bg='#f8f9fa', fg='#666666')
        self.info_turma_label.pack(pady=10)

    def carregar_alunos_turma_selecionada(self, event=None):
        """Carrega alunos da turma selecionada"""
        turma_nome = self.turma_selecionada.get()
        if not turma_nome:
            return

        # Limpar tabela
        for item in self.tree_alunos_turma.get_children():
            self.tree_alunos_turma.delete(item)

        try:
            # Buscar ID da turma
            self.cursor.execute("SELECT id FROM turmas WHERE nome = ?", (turma_nome,))
            turma_id = self.cursor.fetchone()
            if not turma_id:
                return

            turma_id = turma_id[0]

            # Buscar alunos da turma
            self.cursor.execute('''
                SELECT a.id, a.nome, a.cpf, a.email, a.telefone, m.data_matricula, a.status
                FROM alunos a
                JOIN matriculas m ON a.id = m.aluno_id
                WHERE m.turma_id = ? AND m.status = 'Ativa'
                ORDER BY a.nome
            ''', (turma_id,))

            alunos = self.cursor.fetchall()

            for aluno in alunos:
                self.tree_alunos_turma.insert('', tk.END, values=aluno)

            # Atualizar informações
            self.cursor.execute('''
                SELECT capacidade, COUNT(*) as total_alunos
                FROM turmas t
                LEFT JOIN matriculas m ON t.id = m.turma_id AND m.status = 'Ativa'
                WHERE t.id = ?
                GROUP BY t.capacidade
            ''', (turma_id,))

            info = self.cursor.fetchone()
            if info:
                capacidade, total_alunos = info
                vagas_disponiveis = capacidade - total_alunos
                self.info_turma_label.config(
                    text=f"Turma: {turma_nome} | Alunos: {total_alunos}/{capacidade} | Vagas: {vagas_disponiveis}"
                )

        except Exception as e:
            print(f"Erro ao carregar alunos da turma: {e}")

    def buscar_turmas(self, event=None):
        """Busca turmas na tabela"""
        query = self.search_var_turmas.get()
        self.carregar_dados_turmas(query)

    def aplicar_filtros_turmas(self):
        """Aplica filtros na tabela de turmas"""
        status = self.filtro_status_turmas.get()
        turno = self.filtro_turno_turmas.get()
        self.carregar_dados_turmas(None, status, turno)

    def editar_turma(self):
        """Edita turma selecionada"""
        selection = self.tree_turmas.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma turma para editar!")
            return

        item = self.tree_turmas.item(selection[0])
        turma_id = item['values'][0]
        self.abrir_edicao_turma(turma_id)

    def excluir_turma(self):
        """Exclui turma selecionada"""
        selection = self.tree_turmas.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma turma para excluir!")
            return

        item = self.tree_turmas.item(selection[0])
        turma_id, nome = item['values'][0], item['values'][1]

        # Verificar se há alunos na turma
        self.cursor.execute("SELECT COUNT(*) FROM matriculas WHERE turma_id = ? AND status = 'Ativa'", (turma_id,))
        total_alunos = self.cursor.fetchone()[0]

        if total_alunos > 0:
            messagebox.showerror("Erro",
                                 f"Não é possível excluir a turma {nome} pois existem {total_alunos} alunos matriculados!")
            return

        resposta = messagebox.askyesno("Confirmar Exclusão",
                                       f"Tem certeza que deseja excluir a turma {nome}?\n\nEsta ação não pode ser desfeita!")

        if resposta:
            try:
                self.cursor.execute("DELETE FROM turmas WHERE id = ?", (turma_id,))
                self.conn.commit()

                # Registrar log
                self.registrar_log('EXCLUSAO', 'Turmas', f'Excluiu turma: {nome}')

                messagebox.showinfo("Sucesso", "Turma excluída com sucesso!")
                self.carregar_dados_turmas()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir turma: {str(e)}")

    def exportar_turmas(self):
        """Exporta lista de turmas para CSV"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Exportar lista de turmas"
            )

            if filename:
                self.cursor.execute('''
                    SELECT t.nome, t.serie, t.turno, p.nome as professor, t.capacidade, t.sala,
                           t.ano_letivo, t.horario_inicio, t.horario_fim, t.dias_semana, t.status,
                           (SELECT COUNT(*) FROM matriculas m WHERE m.turma_id = t.id AND m.status = 'Ativa') as alunos
                FROM turmas t
                LEFT JOIN professores p ON t.professor_id = p.id
                ORDER BY t.serie, t.nome
                ''')

                turmas = self.cursor.fetchall()

                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Nome', 'Série', 'Turno', 'Professor', 'Capacidade', 'Sala',
                                     'Ano Letivo', 'Horário Início', 'Horário Fim', 'Dias Semana',
                                     'Status', 'Alunos Matriculados'])
                    writer.writerows(turmas)

                messagebox.showinfo("Sucesso", f"Lista de turmas exportada para: {filename}")

                # Registrar log
                self.registrar_log('EXPORTACAO', 'Turmas', 'Exportou lista de turmas para CSV')

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar turmas: {str(e)}")

    def imprimir_lista_turmas(self):
        """Gera PDF com lista de turmas"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Salvar lista de turmas como PDF"
            )

            if filename:
                self.cursor.execute('''
                    SELECT t.nome, t.serie, t.turno, p.nome as professor, t.capacidade, t.sala,
                           (SELECT COUNT(*) FROM matriculas m WHERE m.turma_id = t.id AND m.status = 'Ativa') as alunos,
                           t.status
                FROM turmas t
                LEFT JOIN professores p ON t.professor_id = p.id
                ORDER BY t.serie, t.nome
                ''')

                turmas = self.cursor.fetchall()

                # Criar PDF
                c = canvas.Canvas(filename, pagesize=A4)
                width, height = A4

                # Cabeçalho
                c.setFont("Helvetica-Bold", 16)
                c.drawString(50, height - 50, "EXTERNATO COLÉGIO OBJETIVO")
                c.setFont("Helvetica", 12)
                c.drawString(50, height - 70, "Lista de Turmas")
                c.drawString(50, height - 85, f"Data: {date.today().strftime('%d/%m/%Y')}")

                # Tabela
                data = [['Nome', 'Série', 'Turno', 'Professor', 'Capacidade', 'Sala', 'Alunos', 'Status']]
                for turma in turmas:
                    data.append([turma[0], turma[1], turma[2], turma[3] or '', str(turma[4]),
                                 turma[5] or '', str(turma[6]), turma[7]])

                table = Table(data, colWidths=[80, 60, 60, 80, 60, 50, 50, 50])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0046AD')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))

                table.wrapOn(c, width, height)
                table.drawOn(c, 30, height - 150)

                c.save()
                messagebox.showinfo("Sucesso", f"PDF gerado: {filename}")

                # Registrar log
                self.registrar_log('IMPRESSAO', 'Turmas', 'Gerou PDF com lista de turmas')

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar PDF: {str(e)}")

    # ========== MÓDULO SISTEMA DE NOTAS (COMPLETO) ==========

    def carregar_sistema_notas(self):
        """Carrega o módulo completo de sistema de notas"""
        self.limpar_conteudo()
        self.ativar_botao("📝 Sistema de Notas")
        self.registrar_log('ACESSO', 'Sistema de Notas', 'Acessou módulo de sistema de notas')

        # Título
        title_frame = tk.Frame(self.content_frame, bg='#f8f9fa')
        title_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(title_frame, text="Sistema de Notas", font=('Arial', 24, 'bold'),
                 bg='#f8f9fa', fg='#0046AD').pack(anchor='w')

        tk.Label(title_frame, text="Lançamento e consulta de notas dos alunos",
                 font=('Arial', 12), bg='#f8f9fa', fg='#666666').pack(anchor='w')

        # Frame de seleção
        selecao_frame = tk.Frame(self.content_frame, bg='white', relief='flat', bd=1, padx=20, pady=15)
        selecao_frame.pack(fill=tk.X, pady=(0, 20))

        # Linha 1: Turma e Disciplina
        linha1 = tk.Frame(selecao_frame, bg='white')
        linha1.pack(fill=tk.X, pady=5)

        tk.Label(linha1, text="Turma:", font=('Arial', 10, 'bold'),
                 bg='white', fg='#0046AD').pack(side=tk.LEFT, padx=5)

        self.turma_notas = ttk.Combobox(linha1, values=self.obter_turmas_combo(),
                                        state='readonly', width=25)
        self.turma_notas.pack(side=tk.LEFT, padx=5)
        self.turma_notas.bind('<<ComboboxSelected>>', self.carregar_disciplinas_turma)

        tk.Label(linha1, text="Disciplina:", font=('Arial', 10, 'bold'),
                 bg='white', fg='#0046AD').pack(side=tk.LEFT, padx=(20, 5))

        self.disciplina_notas = ttk.Combobox(linha1, state='readonly', width=25)
        self.disciplina_notas.pack(side=tk.LEFT, padx=5)
        self.disciplina_notas.bind('<<ComboboxSelected>>', self.carregar_notas_turma)

        # Linha 2: Bimestre e Ano Letivo
        linha2 = tk.Frame(selecao_frame, bg='white')
        linha2.pack(fill=tk.X, pady=5)

        tk.Label(linha2, text="Bimestre:", font=('Arial', 10, 'bold'),
                 bg='white', fg='#0046AD').pack(side=tk.LEFT, padx=5)

        self.bimestre_notas = ttk.Combobox(linha2, values=['1', '2', '3', '4'],
                                           state='readonly', width=10)
        self.bimestre_notas.set(str(self.obter_bimestre_atual()))
        self.bimestre_notas.pack(side=tk.LEFT, padx=5)
        self.bimestre_notas.bind('<<ComboboxSelected>>', self.carregar_notas_turma)

        tk.Label(linha2, text="Ano Letivo:", font=('Arial', 10, 'bold'),
                 bg='white', fg='#0046AD').pack(side=tk.LEFT, padx=(20, 5))

        self.ano_letivo_notas = ttk.Combobox(linha2, values=[str(datetime.now().year), str(datetime.now().year + 1)],
                                             state='readonly', width=10)
        self.ano_letivo_notas.set(str(datetime.now().year))
        self.ano_letivo_notas.pack(side=tk.LEFT, padx=5)
        self.ano_letivo_notas.bind('<<ComboboxSelected>>', self.carregar_notas_turma)

        ModernButton(linha2, text="🔄 Carregar Notas",
                     command=self.carregar_notas_turma,
                     color='#0046AD').pack(side=tk.LEFT, padx=20)

        # Tabela de notas
        colunas = ('ID Aluno', 'Nome', 'Nota 1', 'Nota 2', 'Nota 3', 'Nota 4', 'Média', 'Situação', 'Ações')
        self.tree_notas = self.criar_tabela(self.content_frame, colunas)

        # Barra de ferramentas
        botoes_frame = tk.Frame(self.content_frame, bg='#f8f9fa')
        botoes_frame.pack(fill=tk.X, pady=10)

        ModernButton(botoes_frame, text="💾 Salvar Todas as Notas",
                     command=self.salvar_todas_notas,
                     color='#0046AD').pack(side=tk.LEFT, padx=5)

        ModernButton(botoes_frame, text="📊 Calcular Médias",
                     command=self.calcular_medias,
                     color='#0046AD').pack(side=tk.LEFT, padx=5)

        ModernButton(botoes_frame, text="📋 Relatório de Notas",
                     command=self.gerar_relatorio_notas,
                     color='#0046AD').pack(side=tk.LEFT, padx=5)

        # Dicionário para armazenar entradas de notas
        self.entries_notas = {}

    def carregar_disciplinas_turma(self, event=None):
        """Carrega disciplinas da turma selecionada"""
        turma_nome = self.turma_notas.get()
        if not turma_nome:
            return

        try:
            # Buscar ID da turma
            self.cursor.execute("SELECT id FROM turmas WHERE nome = ?", (turma_nome,))
            turma_id = self.cursor.fetchone()
            if not turma_id:
                return

            turma_id = turma_id[0]

            # Buscar disciplinas da turma
            self.cursor.execute('''
                SELECT d.nome 
                FROM disciplinas d 
                WHERE d.turma_id = ? AND d.status = 'Ativa'
                ORDER BY d.nome
            ''', (turma_id,))

            disciplinas = [disc[0] for disc in self.cursor.fetchall()]
            self.disciplina_notas['values'] = disciplinas

            if disciplinas:
                self.disciplina_notas.set(disciplinas[0])
                self.carregar_notas_turma()

        except Exception as e:
            print(f"Erro ao carregar disciplinas: {e}")

    def carregar_notas_turma(self, event=None):
        """Carrega notas dos alunos da turma selecionada"""
        turma_nome = self.turma_notas.get()
        disciplina_nome = self.disciplina_notas.get()
        bimestre = self.bimestre_notas.get()
        ano_letivo = self.ano_letivo_notas.get()

        if not all([turma_nome, disciplina_nome, bimestre, ano_letivo]):
            return

        # Limpar tabela e dicionário de entradas
        for item in self.tree_notas.get_children():
            self.tree_notas.delete(item)
        self.entries_notas.clear()

        try:
            # Buscar IDs
            self.cursor.execute("SELECT id FROM turmas WHERE nome = ?", (turma_nome,))
            turma_id = self.cursor.fetchone()[0]

            self.cursor.execute("SELECT id FROM disciplinas WHERE nome = ? AND turma_id = ?",
                                (disciplina_nome, turma_id))
            disciplina_id = self.cursor.fetchone()[0]

            # Buscar alunos da turma
            self.cursor.execute('''
                SELECT a.id, a.nome
                FROM alunos a
                JOIN matriculas m ON a.id = m.aluno_id
                WHERE m.turma_id = ? AND m.status = 'Ativa'
                ORDER BY a.nome
            ''', (turma_id,))

            alunos = self.cursor.fetchall()

            for aluno_id, aluno_nome in alunos:
                # Buscar notas existentes
                self.cursor.execute('''
                    SELECT nota1, nota2, nota3, nota4, media, situacao
                    FROM notas
                    WHERE aluno_id = ? AND disciplina_id = ? AND bimestre = ? AND ano_letivo = ?
                ''', (aluno_id, disciplina_id, bimestre, ano_letivo))

                nota_data = self.cursor.fetchone()
                if nota_data:
                    nota1, nota2, nota3, nota4, media, situacao = nota_data
                else:
                    nota1 = nota2 = nota3 = nota4 = media = 0.0
                    situacao = 'Cursando'

                # Inserir na tabela
                valores = (aluno_id, aluno_nome,
                           f"{nota1:.1f}" if nota1 else "0.0",
                           f"{nota2:.1f}" if nota2 else "0.0",
                           f"{nota3:.1f}" if nota3 else "0.0",
                           f"{nota4:.1f}" if nota4 else "0.0",
                           f"{media:.1f}" if media else "0.0",
                           situacao,
                           "Editar")

                item = self.tree_notas.insert('', tk.END, values=valores)

                # Armazenar referências para as entradas
                self.entries_notas[aluno_id] = {
                    'item': item,
                    'nota1': nota1,
                    'nota2': nota2,
                    'nota3': nota3,
                    'nota4': nota4,
                    'media': media,
                    'situacao': situacao
                }

            # Configurar duplo clique para editar
            self.tree_notas.bind('<Double-1>', self.editar_nota_aluno)

        except Exception as e:
            print(f"Erro ao carregar notas: {e}")

    def editar_nota_aluno(self, event):
        """Abre janela para editar notas de um aluno"""
        item = self.tree_notas.selection()[0]
        valores = self.tree_notas.item(item, 'values')

        aluno_id = int(valores[0])
        aluno_nome = valores[1]

        # Criar janela de edição
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Editar Notas - {aluno_nome}")
        edit_window.geometry("400x300")
        edit_window.configure(bg='white')
        edit_window.transient(self.root)
        edit_window.grab_set()
        self.center_dialog(edit_window)

        # Header
        header_frame = tk.Frame(edit_window, bg='#0046AD', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        tk.Label(header_frame, text=f"Editar Notas: {aluno_nome}",
                 font=('Arial', 14, 'bold'), bg='#0046AD', fg='white').pack(expand=True)

        # Formulário
        form_frame = tk.Frame(edit_window, bg='white', padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        dados_aluno = self.entries_notas[aluno_id]

        campos = [
            ("Nota 1:", dados_aluno['nota1']),
            ("Nota 2:", dados_aluno['nota2']),
            ("Nota 3:", dados_aluno['nota3']),
            ("Nota 4:", dados_aluno['nota4']),
        ]

        entries = {}
        for i, (label, valor) in enumerate(campos):
            tk.Label(form_frame, text=label, font=('Arial', 11, 'bold'),
                     bg='white', fg='#0046AD').grid(row=i, column=0, sticky='w', pady=10)

            entry = tk.Entry(form_frame, width=10, font=('Arial', 11), justify='center')
            entry.insert(0, str(valor) if valor else "0.0")
            entry.grid(row=i, column=1, pady=10, padx=10)
            entries[label] = entry

        # Média atual
        tk.Label(form_frame, text="Média Atual:", font=('Arial', 11, 'bold'),
                 bg='white', fg='#0046AD').grid(row=4, column=0, sticky='w', pady=10)

        media_label = tk.Label(form_frame, text=f"{dados_aluno['media']:.1f}",
                               font=('Arial', 11, 'bold'), bg='white', fg='#0046AD')
        media_label.grid(row=4, column=1, pady=10, padx=10)

        def calcular_e_salvar():
            try:
                # Coletar notas
                notas = []
                for label in ["Nota 1:", "Nota 2:", "Nota 3:", "Nota 4:"]:
                    valor = entries[label].get().replace(',', '.')
                    nota = float(valor) if valor else 0.0
                    notas.append(nota)

                # Calcular média
                media = sum(notas) / len(notas)
                media_label.config(text=f"{media:.1f}")

                # Determinar situação
                situacao = 'Aprovado' if media >= 6.0 else 'Recuperação' if media >= 4.0 else 'Reprovado'

                # Atualizar dados
                dados_aluno.update({
                    'nota1': notas[0],
                    'nota2': notas[1],
                    'nota3': notas[2],
                    'nota4': notas[3],
                    'media': media,
                    'situacao': situacao
                })

                # Atualizar tabela
                novos_valores = (aluno_id, aluno_nome,
                                 f"{notas[0]:.1f}", f"{notas[1]:.1f}",
                                 f"{notas[2]:.1f}", f"{notas[3]:.1f}",
                                 f"{media:.1f}", situacao, "Editar")
                self.tree_notas.item(item, values=novos_valores)

                messagebox.showinfo("Sucesso", "Notas atualizadas com sucesso!")
                edit_window.destroy()

            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos!")

        # Botões
        btn_frame = tk.Frame(edit_window, bg='white')
        btn_frame.pack(pady=20)

        ModernButton(btn_frame, text="Calcular Média",
                     command=calcular_e_salvar,
                     color='#0046AD').pack(side=tk.LEFT, padx=10)

        ModernButton(btn_frame, text="Cancelar",
                     command=edit_window.destroy,
                     color='#666666').pack(side=tk.LEFT, padx=10)

    def salvar_todas_notas(self):
        """Salva todas as notas no banco de dados"""
        turma_nome = self.turma_notas.get()
        disciplina_nome = self.disciplina_notas.get()
        bimestre = self.bimestre_notas.get()
        ano_letivo = self.ano_letivo_notas.get()

        if not all([turma_nome, disciplina_nome, bimestre, ano_letivo]):
            messagebox.showwarning("Aviso", "Selecione turma, disciplina, bimestre e ano letivo!")
            return

        try:
            # Buscar IDs
            self.cursor.execute("SELECT id FROM turmas WHERE nome = ?", (turma_nome,))
            turma_id = self.cursor.fetchone()[0]

            self.cursor.execute("SELECT id FROM disciplinas WHERE nome = ? AND turma_id = ?",
                                (disciplina_nome, turma_id))
            disciplina_id = self.cursor.fetchone()[0]

            # Obter professor da disciplina
            self.cursor.execute("SELECT professor_id FROM disciplinas WHERE id = ?", (disciplina_id,))
            professor_id = self.cursor.fetchone()[0]

            total_salvas = 0
            for aluno_id, dados in self.entries_notas.items():
                # Verificar se já existe registro
                self.cursor.execute('''
                    SELECT id FROM notas 
                    WHERE aluno_id = ? AND disciplina_id = ? AND bimestre = ? AND ano_letivo = ?
                ''', (aluno_id, disciplina_id, bimestre, ano_letivo))

                existe = self.cursor.fetchone()

                if existe:
                    # Atualizar
                    self.cursor.execute('''
                        UPDATE notas SET nota1=?, nota2=?, nota3=?, nota4=?, media=?, situacao=?
                        WHERE aluno_id=? AND disciplina_id=? AND bimestre=? AND ano_letivo=?
                    ''', (dados['nota1'], dados['nota2'], dados['nota3'], dados['nota4'],
                          dados['media'], dados['situacao'], aluno_id, disciplina_id, bimestre, ano_letivo))
                else:
                    # Inserir novo
                    self.cursor.execute('''
                        INSERT INTO notas (aluno_id, disciplina_id, nota1, nota2, nota3, nota4,
                                         media, situacao, bimestre, ano_letivo, professor_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (aluno_id, disciplina_id, dados['nota1'], dados['nota2'], dados['nota3'],
                          dados['nota4'], dados['media'], dados['situacao'], bimestre, ano_letivo, professor_id))

                total_salvas += 1

            self.conn.commit()

            # Registrar log
            self.registrar_log('ATUALIZACAO', 'Notas',
                               f'Salvou {total_salvas} notas - {disciplina_nome} - {turma_nome}')

            messagebox.showinfo("Sucesso", f"{total_salvas} notas salvas com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar notas: {str(e)}")

    def calcular_medias(self):
        """Calcula médias para todos os alunos"""
        for aluno_id, dados in self.entries_notas.items():
            notas = [dados['nota1'], dados['nota2'], dados['nota3'], dados['nota4']]
            media = sum(notas) / len(notas)

            # Atualizar situação
            situacao = 'Aprovado' if media >= 6.0 else 'Recuperação' if media >= 4.0 else 'Reprovado'

            dados['media'] = media
            dados['situacao'] = situacao

            # Atualizar tabela
            item = dados['item']
            valores = list(self.tree_notas.item(item, 'values'))
            valores[6] = f"{media:.1f}"  # Média
            valores[7] = situacao  # Situação
            self.tree_notas.item(item, values=valores)

        messagebox.showinfo("Sucesso", "Médias calculadas para todos os alunos!")

    def gerar_relatorio_notas(self):
        """Gera relatório de notas"""
        turma_nome = self.turma_notas.get()
        disciplina_nome = self.disciplina_notas.get()
        bimestre = self.bimestre_notas.get()

        if not all([turma_nome, disciplina_nome, bimestre]):
            messagebox.showwarning("Aviso", "Selecione turma, disciplina e bimestre!")
            return

        try:
            relatorio = f"RELATÓRIO DE NOTAS - {disciplina_nome}\n"
            relatorio += "=" * 50 + "\n\n"
            relatorio += f"Turma: {turma_nome}\n"
            relatorio += f"Bimestre: {bimestre}\n"
            relatorio += f"Data: {date.today().strftime('%d/%m/%Y')}\n\n"

            relatorio += "ALUNOS E NOTAS:\n"
            relatorio += "-" * 50 + "\n"

            aprovados = 0
            recuperacao = 0
            reprovados = 0

            for aluno_id, dados in self.entries_notas.items():
                # Buscar nome do aluno
                item = self.tree_notas.item(dados['item'])
                aluno_nome = item['values'][1]

                relatorio += f"{aluno_nome}:\n"
                relatorio += f"  N1: {dados['nota1']:.1f} | N2: {dados['nota2']:.1f} | "
                relatorio += f"N3: {dados['nota3']:.1f} | N4: {dados['nota4']:.1f}\n"
                relatorio += f"  Média: {dados['media']:.1f} | Situação: {dados['situacao']}\n\n"

                # Contar situações
                if dados['situacao'] == 'Aprovado':
                    aprovados += 1
                elif dados['situacao'] == 'Recuperação':
                    recuperacao += 1
                else:
                    reprovados += 1

            relatorio += f"\nRESUMO:\n"
            relatorio += f"Aprovados: {aprovados}\n"
            relatorio += f"Recuperação: {recuperacao}\n"
            relatorio += f"Reprovados: {reprovados}\n"
            relatorio += f"Total: {len(self.entries_notas)}\n"
            relatorio += f"Taxa de Aprovação: {(aprovados / len(self.entries_notas)) * 100:.1f}%"

            self.mostrar_relatorio(f"Notas - {disciplina_nome}", relatorio)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")

    # ========== MÓDULO DIÁRIO DE CLASSE (COMPLETO) ==========

    def carregar_diario_classe(self):
        """Carrega o módulo completo de diário de classe"""
        self.limpar_conteudo()
        self.ativar_botao("📓 Diário de Classe")
        self.registrar_log('ACESSO', 'Diário de Classe', 'Acessou módulo de diário de classe')

        # Título
        title_frame = tk.Frame(self.content_frame, bg='#f8f9fa')
        title_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(title_frame, text="Diário de Classe", font=('Arial', 24, 'bold'),
                 bg='#f8f9fa', fg='#0046AD').pack(anchor='w')

        tk.Label(title_frame, text="Registro de aulas e conteúdo ministrado",
                 font=('Arial', 12), bg='#f8f9fa', fg='#666666').pack(anchor='w')

        # Notebook com abas
        notebook = ttk.Notebook(self.content_frame, style='Custom.TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Aba 1: Registrar Aula
        aba_registro = ttk.Frame(notebook)
        notebook.add(aba_registro, text="➕ Registrar Aula")

        self.carregar_aba_registro_aula(aba_registro)

        # Aba 2: Consultar Aulas
        aba_consulta = ttk.Frame(notebook)
        notebook.add(aba_consulta, text="📋 Consultar Aulas")

        self.carregar_aba_consulta_aulas(aba_consulta)

    def carregar_aba_registro_aula(self, parent):
        """Carrega aba de registro de aula"""
        form_frame = tk.Frame(parent, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Container com scroll
        canvas = tk.Canvas(form_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Formulário de registro
        self.criar_formulario_diario(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def criar_formulario_diario(self, parent):
        """Cria formulário de registro no diário"""
        # Dados da Aula
        dados_frame = tk.LabelFrame(parent, text="Dados da Aula", font=('Arial', 12, 'bold'),
                                    bg='white', fg='#0046AD', padx=15, pady=15)
        dados_frame.pack(fill=tk.X, pady=10)

        campos_dados = [
            ("Turma*", "combo", self.obter_turmas_combo()),
            ("Disciplina*", "combo", []),
            ("Data da Aula*", "entry", None),
            ("Conteúdo Ministrado*", "entry", None),
        ]

        self.entries_diario = {}
        linha = 0

        for label, tipo, valores in campos_dados:
            tk.Label(dados_frame, text=label, font=('Arial', 10, 'bold'),
                     bg='white', fg='#0046AD').grid(row=linha, column=0, sticky='w', pady=5, padx=5)

            if tipo == "entry":
                entry = tk.Entry(dados_frame, width=50, font=('Arial', 10), relief='solid', bd=1)
                entry.grid(row=linha, column=1, pady=5, padx=5, sticky='ew', columnspan=3)
                self.entries_diario[label] = entry

                # Preencher data atual se for o campo de data
                if label == "Data da Aula*":
                    entry.insert(0, date.today().strftime('%d/%m/%Y'))

            elif tipo == "combo":
                combo = ttk.Combobox(dados_frame, values=valores, state='readonly', width=47)
                combo.grid(row=linha, column=1, pady=5, padx=5, sticky='ew', columnspan=3)
                self.entries_diario[label] = combo

                # Configurar evento para carregar disciplinas quando turma for selecionada
                if label == "Turma*":
                    combo.bind('<<ComboboxSelected>>', self.carregar_disciplinas_diario)

            linha += 1

        # Detalhes da Aula
        detalhes_frame = tk.LabelFrame(parent, text="Detalhes da Aula", font=('Arial', 12, 'bold'),
                                       bg='white', fg='#0046AD', padx=15, pady=15)
        detalhes_frame.pack(fill=tk.X, pady=10)

        campos_detalhes = [
            ("Objetivos da Aula", "text", None),
            ("Metodologia Utilizada", "text", None),
            ("Recursos Didáticos", "text", None),
            ("Tarefa de Casa", "text", None),
            ("Observações", "text", None),
        ]

        linha = 0
        for label, tipo, valores in campos_detalhes:
            tk.Label(detalhes_frame, text=label, font=('Arial', 10, 'bold'),
                     bg='white', fg='#0046AD').grid(row=linha, column=0, sticky='nw', pady=5, padx=5)

            if tipo == "text":
                text = tk.Text(detalhes_frame, width=50, height=3, font=('Arial', 10), relief='solid', bd=1)
                text.grid(row=linha, column=1, pady=5, padx=5, sticky='ew', columnspan=3)
                self.entries_diario[label] = text

            linha += 1

        # Botões
        botoes_frame = tk.Frame(parent, bg='white')
        botoes_frame.pack(pady=20)

        ModernButton(botoes_frame, text="🗑️ Limpar",
                     command=self.limpar_formulario_diario,
                     color='#666666').pack(side=tk.LEFT, padx=10)

        ModernButton(botoes_frame, text="💾 Registrar Aula",
                     command=self.registrar_aula_diario,
                     color='#0046AD').pack(side=tk.LEFT, padx=10)

        # Configurar pesos das colunas
        dados_frame.columnconfigure(1, weight=1)
        detalhes_frame.columnconfigure(1, weight=1)

    def carregar_disciplinas_diario(self, event=None):
        """Carrega disciplinas da turma selecionada no diário"""
        turma_nome = self.entries_diario["Turma*"].get()
        if not turma_nome:
            return

        try:
            # Buscar ID da turma
            self.cursor.execute("SELECT id FROM turmas WHERE nome = ?", (turma_nome,))
            turma_id = self.cursor.fetchone()
            if not turma_id:
                return

            turma_id = turma_id[0]

            # Buscar disciplinas da turma
            self.cursor.execute('''
                SELECT d.nome 
                FROM disciplinas d 
                WHERE d.turma_id = ? AND d.status = 'Ativa'
                ORDER BY d.nome
            ''', (turma_id,))

            disciplinas = [disc[0] for disc in self.cursor.fetchall()]
            self.entries_diario["Disciplina*"]['values'] = disciplinas

            if disciplinas:
                self.entries_diario["Disciplina*"].set(disciplinas[0])

        except Exception as e:
            print(f"Erro ao carregar disciplinas: {e}")

    def limpar_formulario_diario(self):
        """Limpa todos os campos do formulário do diário"""
        for entry in self.entries_diario.values():
            if isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)
            elif isinstance(entry, ttk.Combobox):
                entry.set('')
            elif isinstance(entry, tk.Text):
                entry.delete('1.0', tk.END)

        # Preencher data atual
        if "Data da Aula*" in self.entries_diario:
            self.entries_diario["Data da Aula*"].insert(0, date.today().strftime('%d/%m/%Y'))

    def registrar_aula_diario(self):
        """Registra aula no diário de classe"""
        try:
            # Validar campos obrigatórios
            if not self.entries_diario["Turma*"].get().strip():
                messagebox.showwarning("Aviso", "Selecione a turma!")
                return
            if not self.entries_diario["Disciplina*"].get().strip():
                messagebox.showwarning("Aviso", "Selecione a disciplina!")
                return
            if not self.entries_diario["Data da Aula*"].get().strip():
                messagebox.showwarning("Aviso", "Informe a data da aula!")
                return
            if not self.entries_diario["Conteúdo Ministrado*"].get().strip():
                messagebox.showwarning("Aviso", "Informe o conteúdo ministrado!")
                return

            # Buscar IDs
            turma_nome = self.entries_diario["Turma*"].get()
            disciplina_nome = self.entries_diario["Disciplina*"].get()

            self.cursor.execute("SELECT id FROM turmas WHERE nome = ?", (turma_nome,))
            turma_id = self.cursor.fetchone()[0]

            self.cursor.execute("SELECT id, professor_id FROM disciplinas WHERE nome = ? AND turma_id = ?",
                                (disciplina_nome, turma_id))
            disciplina_info = self.cursor.fetchone()
            disciplina_id, professor_id = disciplina_info

            # Converter data
            data_aula_str = self.entries_diario["Data da Aula*"].get()
            try:
                data_aula = datetime.strptime(data_aula_str, '%d/%m/%Y').strftime('%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Erro", "Data inválida! Use o formato DD/MM/AAAA")
                return

            # Coletar dados
            dados = {
                'disciplina_id': disciplina_id,
                'turma_id': turma_id,
                'professor_id': professor_id,
                'data_aula': data_aula,
                'conteudo': self.entries_diario["Conteúdo Ministrado*"].get().strip(),
                'objetivos': self.entries_diario["Objetivos da Aula"].get("1.0", tk.END).strip(),
                'metodologia': self.entries_diario["Metodologia Utilizada"].get("1.0", tk.END).strip(),
                'recursos': self.entries_diario["Recursos Didáticos"].get("1.0", tk.END).strip(),
                'tarefa_casa': self.entries_diario["Tarefa de Casa"].get("1.0", tk.END).strip(),
                'observacoes': self.entries_diario["Observações"].get("1.0", tk.END).strip(),
            }

            # Inserir no banco
            self.cursor.execute('''
                INSERT INTO diario_aula (
                    disciplina_id, turma_id, professor_id, data_aula, conteudo,
                    objetivos, metodologia, recursos, tarefa_casa, observacoes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (dados['disciplina_id'], dados['turma_id'], dados['professor_id'],
                  dados['data_aula'], dados['conteudo'], dados['objetivos'],
                  dados['metodologia'], dados['recursos'], dados['tarefa_casa'],
                  dados['observacoes']))

            self.conn.commit()

            # Registrar log
            self.registrar_log('REGISTRO', 'Diário de Aula',
                               f'Registrou aula: {disciplina_nome} - {turma_nome} - {data_aula_str}')

            messagebox.showinfo("Sucesso", "Aula registrada no diário com sucesso!")
            self.limpar_formulario_diario()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao registrar aula: {str(e)}")

    def carregar_aba_consulta_aulas(self, parent):
        """Carrega aba de consulta de aulas"""
        # Frame de filtros
        filtros_frame = tk.Frame(parent, bg='white', relief='flat', bd=1, padx=20, pady=15)
        filtros_frame.pack(fill=tk.X, pady=(0, 20))

        # Linha 1
        linha1 = tk.Frame(filtros_frame, bg='white')
        linha1.pack(fill=tk.X, pady=5)

        tk.Label(linha1, text="Turma:", font=('Arial', 10, 'bold'),
                 bg='white', fg='#0046AD').pack(side=tk.LEFT, padx=5)

        self.turma_consulta_diario = ttk.Combobox(linha1, values=self.obter_turmas_combo(),
                                                  state='readonly', width=25)
        self.turma_consulta_diario.pack(side=tk.LEFT, padx=5)

        tk.Label(linha1, text="Disciplina:", font=('Arial', 10, 'bold'),
                 bg='white', fg='#0046AD').pack(side=tk.LEFT, padx=(20, 5))

        self.disciplina_consulta_diario = ttk.Combobox(linha1, state='readonly', width=25)
        self.disciplina_consulta_diario.pack(side=tk.LEFT, padx=5)

        # Linha 2
        linha2 = tk.Frame(filtros_frame, bg='white')
        linha2.pack(fill=tk.X, pady=5)

        tk.Label(linha2, text="Data Início:", font=('Arial', 10, 'bold'),
                 bg='white', fg='#0046AD').pack(side=tk.LEFT, padx=5)

        self.data_inicio_diario = tk.Entry(linha2, width=12, font=('Arial', 10))
        self.data_inicio_diario.pack(side=tk.LEFT, padx=5)
        self.data_inicio_diario.insert(0, date.today().replace(day=1).strftime('%d/%m/%Y'))

        tk.Label(linha2, text="Data Fim:", font=('Arial', 10, 'bold'),
                 bg='white', fg='#0046AD').pack(side=tk.LEFT, padx=(20, 5))

        self.data_fim_diario = tk.Entry(linha2, width=12, font=('Arial', 10))
        self.data_fim_diario.pack(side=tk.LEFT, padx=5)
        self.data_fim_diario.insert(0, date.today().strftime('%d/%m/%Y'))

        ModernButton(linha2, text="🔍 Buscar Aulas",
                     command=self.buscar_aulas_diario,
                     color='#0046AD').pack(side=tk.LEFT, padx=20)

        ModernButton(linha2, text="📋 Relatório",
                     command=self.gerar_relatorio_diario,
                     color='#0046AD').pack(side=tk.LEFT, padx=5)

        # Tabela de aulas
        colunas = ('ID', 'Data', 'Turma', 'Disciplina', 'Conteúdo', 'Professor', 'Registro')
        self.tree_diario = self.criar_tabela(parent, colunas)

        # Configurar evento para carregar disciplinas
        self.turma_consulta_diario.bind('<<ComboboxSelected>>', self.carregar_disciplinas_consulta_diario)

    def carregar_disciplinas_consulta_diario(self, event=None):
        """Carrega disciplinas para consulta no diário"""
        turma_nome = self.turma_consulta_diario.get()
        if not turma_nome:
            return

        try:
            # Buscar ID da turma
            self.cursor.execute("SELECT id FROM turmas WHERE nome = ?", (turma_nome,))
            turma_id = self.cursor.fetchone()
            if not turma_id:
                return

            turma_id = turma_id[0]

            # Buscar disciplinas da turma
            self.cursor.execute('''
                SELECT d.nome 
                FROM disciplinas d 
                WHERE d.turma_id = ? AND d.status = 'Ativa'
                ORDER BY d.nome
            ''', (turma_id,))

            disciplinas = [disc[0] for disc in self.cursor.fetchall()]
            self.disciplina_consulta_diario['values'] = disciplinas

        except Exception as e:
            print(f"Erro ao carregar disciplinas: {e}")

    def buscar_aulas_diario(self):
        """Busca aulas no diário conforme filtros"""
        # Limpar tabela
        for item in self.tree_diario.get_children():
            self.tree_diario.delete(item)

        turma_nome = self.turma_consulta_diario.get()
        disciplina_nome = self.disciplina_consulta_diario.get()
        data_inicio = self.data_inicio_diario.get()
        data_fim = self.data_fim_diario.get()

        try:
            sql = '''
                SELECT da.id, da.data_aula, t.nome, d.nome, da.conteudo, p.nome, da.data_registro
                FROM diario_aula da
                JOIN turmas t ON da.turma_id = t.id
                JOIN disciplinas d ON da.disciplina_id = d.id
                JOIN professores p ON da.professor_id = p.id
                WHERE 1=1
            '''
            params = []

            if turma_nome:
                sql += ' AND t.nome = ?'
                params.append(turma_nome)

            if disciplina_nome:
                sql += ' AND d.nome = ?'
                params.append(disciplina_nome)

            if data_inicio:
                try:
                    data_ini = datetime.strptime(data_inicio, '%d/%m/%Y').strftime('%Y-%m-%d')
                    sql += ' AND da.data_aula >= ?'
                    params.append(data_ini)
                except ValueError:
                    pass

            if data_fim:
                try:
                    data_f = datetime.strptime(data_fim, '%d/%m/%Y').strftime('%Y-%m-%d')
                    sql += ' AND da.data_aula <= ?'
                    params.append(data_f)
                except ValueError:
                    pass

            sql += ' ORDER BY da.data_aula DESC, t.nome'

            self.cursor.execute(sql, params)
            aulas = self.cursor.fetchall()

            for aula in aulas:
                # Formatar data
                data_formatada = datetime.strptime(aula[1], '%Y-%m-%d').strftime('%d/%m/%Y')
                registro_formatado = datetime.strptime(aula[6], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M')

                valores = (aula[0], data_formatada, aula[2], aula[3],
                           aula[4][:50] + "..." if len(aula[4]) > 50 else aula[4],
                           aula[5], registro_formatado)
                self.tree_diario.insert('', tk.END, values=valores)

        except Exception as e:
            print(f"Erro ao buscar aulas: {e}")

    def gerar_relatorio_diario(self):
        """Gera relatório do diário de classe"""
        turma_nome = self.turma_consulta_diario.get()
        disciplina_nome = self.disciplina_consulta_diario.get()
        data_inicio = self.data_inicio_diario.get()
        data_fim = self.data_fim_diario.get()

        try:
            # Buscar aulas
            sql = '''
                SELECT da.data_aula, t.nome, d.nome, da.conteudo, p.nome, 
                       da.objetivos, da.metodologia, da.recursos, da.tarefa_casa, da.observacoes
                FROM diario_aula da
                JOIN turmas t ON da.turma_id = t.id
                JOIN disciplinas d ON da.disciplina_id = d.id
                JOIN professores p ON da.professor_id = p.id
                WHERE 1=1
            '''
            params = []

            if turma_nome:
                sql += ' AND t.nome = ?'
                params.append(turma_nome)

            if disciplina_nome:
                sql += ' AND d.nome = ?'
                params.append(disciplina_nome)

            if data_inicio:
                try:
                    data_ini = datetime.strptime(data_inicio, '%d/%m/%Y').strftime('%Y-%m-%d')
                    sql += ' AND da.data_aula >= ?'
                    params.append(data_ini)
                except ValueError:
                    pass

            if data_fim:
                try:
                    data_f = datetime.strptime(data_fim, '%d/%m/%Y').strftime('%Y-%m-%d')
                    sql += ' AND da.data_aula <= ?'
                    params.append(data_f)
                except ValueError:
                    pass

            sql += ' ORDER BY da.data_aula, t.nome'

            self.cursor.execute(sql, params)
            aulas = self.cursor.fetchall()

            relatorio = "RELATÓRIO DO DIÁRIO DE CLASSE\n"
            relatorio += "=" * 50 + "\n\n"

            if turma_nome:
                relatorio += f"Turma: {turma_nome}\n"
            if disciplina_nome:
                relatorio += f"Disciplina: {disciplina_nome}\n"
            if data_inicio and data_fim:
                relatorio += f"Período: {data_inicio} a {data_fim}\n"

            relatorio += f"Data do relatório: {date.today().strftime('%d/%m/%Y')}\n\n"

            relatorio += f"Total de aulas registradas: {len(aulas)}\n\n"

            for aula in aulas:
                data_formatada = datetime.strptime(aula[0], '%Y-%m-%d').strftime('%d/%m/%Y')
                relatorio += f"Data: {data_formatada}\n"
                relatorio += f"Turma: {aula[1]} | Disciplina: {aula[2]} | Professor: {aula[4]}\n"
                relatorio += f"Conteúdo: {aula[3]}\n"

                if aula[5]:  # Objetivos
                    relatorio += f"Objetivos: {aula[5]}\n"
                if aula[6]:  # Metodologia
                    relatorio += f"Metodologia: {aula[6]}\n"
                if aula[7]:  # Recursos
                    relatorio += f"Recursos: {aula[7]}\n"
                if aula[8]:  # Tarefa de casa
                    relatorio += f"Tarefa: {aula[8]}\n"
                if aula[9]:  # Observações
                    relatorio += f"Observações: {aula[9]}\n"

                relatorio += "-" * 50 + "\n\n"

            self.mostrar_relatorio("Relatório do Diário", relatorio)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")

    # ========== MÓDULO GESTÃO DE DISCIPLINAS ==========

    def carregar_gestao_disciplinas(self):
        """Carrega módulo de gestão de disciplinas"""
        self.limpar_conteudo()
        self.ativar_botao("📚 Gestão de Disciplinas")
        self.registrar_log('ACESSO', 'Gestão de Disciplinas', 'Acessou módulo de gestão de disciplinas')

        # Frame principal com notebook
        main_frame = tk.Frame(self.content_frame, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Título
        title_frame = tk.Frame(main_frame, bg='#f8f9fa')
        title_frame.pack(fill='x', pady=(0, 20))

        tk.Label(title_frame, text="Gestão de Disciplinas", font=('Arial', 24, 'bold'),
                 bg='#f8f9fa', fg='#0046AD').pack(anchor='w')

        tk.Label(title_frame, text="Cadastro e gerenciamento de disciplinas escolares",
                 font=('Arial', 12), bg='#f8f9fa', fg='#666666').pack(anchor='w')

        # Notebook para abas
        notebook = ttk.Notebook(main_frame, style='Custom.TNotebook')
        notebook.pack(fill='both', expand=True)

        # Abas
        self.carregar_aba_lista_disciplinas_modulo(notebook)
        self.carregar_aba_cadastro_disciplinas_modulo(notebook)
        self.carregar_aba_relatorios_disciplinas(notebook)

    def carregar_aba_lista_disciplinas_modulo(self, parent):
        """Aba de listagem de disciplinas"""
        frame = tk.Frame(parent, bg='white')
        parent.add(frame, text='📋 Lista de Disciplinas')

        # Barra de ferramentas
        toolbar = tk.Frame(frame, bg='white', pady=10)
        toolbar.pack(fill='x', padx=20)

        # Busca
        search_frame = tk.Frame(toolbar, bg='white')
        search_frame.pack(side='left', fill='x', expand=True)

        tk.Label(search_frame, text="🔍 Buscar:", font=('Arial', 10, 'bold'),
                bg='white', fg='#0046AD').pack(side='left', padx=5)

        self.busca_disciplina_var = tk.StringVar()
        busca_entry = tk.Entry(search_frame, textvariable=self.busca_disciplina_var,
                              font=('Arial', 10), width=40, relief='solid', bd=1)
        busca_entry.pack(side='left', padx=5)
        busca_entry.bind('<KeyRelease>', self.buscar_disciplinas_modulo)

        # Filtros
        tk.Label(search_frame, text="Status:", font=('Arial', 10),
                bg='white', fg='#666666').pack(side='left', padx=(20, 5))

        self.filtro_status_disciplina = ttk.Combobox(search_frame, values=['Todas', 'Ativa', 'Inativa'],
                                                     state='readonly', width=12, font=('Arial', 10))
        self.filtro_status_disciplina.set('Ativa')
        self.filtro_status_disciplina.pack(side='left', padx=5)
        self.filtro_status_disciplina.bind('<<ComboboxSelected>>', lambda e: self.aplicar_filtros_disciplinas_modulo())

        # Botões de ação
        btn_frame = tk.Frame(toolbar, bg='white')
        btn_frame.pack(side='right')

        ModernButton(btn_frame, text="➕ Nova", command=lambda: parent.select(1),
                    color='#0046AD').pack(side='left', padx=5)

        ModernButton(btn_frame, text="✏️ Editar", command=self.editar_disciplina_modulo,
                    color='#FFCC00').pack(side='left', padx=5)

        ModernButton(btn_frame, text="🗑️ Excluir", command=self.excluir_disciplina_modulo,
                    color='#dc3545').pack(side='left', padx=5)

        ModernButton(btn_frame, text="📊 Exportar", command=self.exportar_disciplinas_modulo,
                    color='#28a745').pack(side='left', padx=5)

        # Tabela de disciplinas
        table_frame = tk.Frame(frame, bg='white')
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Scrollbars
        scroll_y = ttk.Scrollbar(table_frame)
        scroll_y.pack(side='right', fill='y')

        scroll_x = ttk.Scrollbar(table_frame, orient='horizontal')
        scroll_x.pack(side='bottom', fill='x')

        # Treeview
        colunas = ('ID', 'Nome', 'Carga Horária', 'Professor', 'Turma', 'Status')
        self.tree_disciplinas_modulo = ttk.Treeview(table_frame, columns=colunas, show='headings',
                                            yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set,
                                            style='Custom.Treeview', height=20)

        # Configurar colunas
        self.tree_disciplinas_modulo.heading('ID', text='ID')
        self.tree_disciplinas_modulo.heading('Nome', text='Nome da Disciplina')
        self.tree_disciplinas_modulo.heading('Carga Horária', text='Carga Horária (h)')
        self.tree_disciplinas_modulo.heading('Professor', text='Professor')
        self.tree_disciplinas_modulo.heading('Turma', text='Turma')
        self.tree_disciplinas_modulo.heading('Status', text='Status')

        self.tree_disciplinas_modulo.column('ID', width=50, anchor='center')
        self.tree_disciplinas_modulo.column('Nome', width=250, anchor='w')
        self.tree_disciplinas_modulo.column('Carga Horária', width=120, anchor='center')
        self.tree_disciplinas_modulo.column('Professor', width=200, anchor='w')
        self.tree_disciplinas_modulo.column('Turma', width=150, anchor='w')
        self.tree_disciplinas_modulo.column('Status', width=100, anchor='center')

        scroll_y.config(command=self.tree_disciplinas_modulo.yview)
        scroll_x.config(command=self.tree_disciplinas_modulo.xview)

        self.tree_disciplinas_modulo.pack(fill='both', expand=True)

        # Carregar dados
        self.carregar_dados_disciplinas_modulo()

        # Bind duplo clique para editar
        self.tree_disciplinas_modulo.bind('<Double-1>', lambda e: self.editar_disciplina_modulo())

    def carregar_dados_disciplinas_modulo(self, query=None, filtro_status='Ativa'):
        """Carrega dados das disciplinas na tabela"""
        for item in self.tree_disciplinas_modulo.get_children():
            self.tree_disciplinas_modulo.delete(item)

        try:
            if query:
                sql = '''
                    SELECT d.id, d.nome, d.carga_horaria, p.nome, t.nome, d.status
                    FROM disciplinas d
                    LEFT JOIN professores p ON d.professor_id = p.id
                    LEFT JOIN turmas t ON d.turma_id = t.id
                    WHERE (d.nome LIKE ? OR p.nome LIKE ? OR t.nome LIKE ?)
                '''
                params = [f'%{query}%', f'%{query}%', f'%{query}%']

                if filtro_status != 'Todas':
                    sql += ' AND d.status = ?'
                    params.append(filtro_status)

                sql += ' ORDER BY d.nome'
                self.cursor.execute(sql, params)
            else:
                if filtro_status == 'Todas':
                    self.cursor.execute('''
                        SELECT d.id, d.nome, d.carga_horaria, p.nome, t.nome, d.status
                        FROM disciplinas d
                        LEFT JOIN professores p ON d.professor_id = p.id
                        LEFT JOIN turmas t ON d.turma_id = t.id
                        ORDER BY d.nome
                    ''')
                else:
                    self.cursor.execute('''
                        SELECT d.id, d.nome, d.carga_horaria, p.nome, t.nome, d.status
                        FROM disciplinas d
                        LEFT JOIN professores p ON d.professor_id = p.id
                        LEFT JOIN turmas t ON d.turma_id = t.id
                        WHERE d.status = ?
                        ORDER BY d.nome
                    ''', (filtro_status,))

            disciplinas = self.cursor.fetchall()

            for disc in disciplinas:
                disc_id, nome, carga, professor, turma, status = disc
                professor = professor if professor else 'Não atribuído'
                turma = turma if turma else 'Não atribuída'
                carga = f'{carga}h' if carga else '0h'

                # Cor de status
                tags = ('ativa',) if status == 'Ativa' else ('inativa',)
                self.tree_disciplinas_modulo.insert('', 'end', values=(disc_id, nome, carga, professor, turma, status), tags=tags)

            # Configurar cores
            self.tree_disciplinas_modulo.tag_configure('ativa', foreground='#28a745')
            self.tree_disciplinas_modulo.tag_configure('inativa', foreground='#dc3545')

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar disciplinas: {str(e)}")

    def buscar_disciplinas_modulo(self, event=None):
        """Busca disciplinas"""
        query = self.busca_disciplina_var.get()
        filtro_status = self.filtro_status_disciplina.get()
        self.carregar_dados_disciplinas_modulo(query, filtro_status)

    def aplicar_filtros_disciplinas_modulo(self):
        """Aplica filtros na lista de disciplinas"""
        query = self.busca_disciplina_var.get()
        filtro_status = self.filtro_status_disciplina.get()
        self.carregar_dados_disciplinas_modulo(query, filtro_status)

    def carregar_aba_cadastro_disciplinas_modulo(self, parent):
        """Aba de cadastro de disciplinas"""
        frame = tk.Frame(parent, bg='white')
        parent.add(frame, text='➕ Cadastrar Disciplina')

        # Container com scroll
        canvas = tk.Canvas(frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Título
        title_frame = tk.Frame(scrollable_frame, bg='white')
        title_frame.pack(fill='x', pady=(20, 20), padx=20)

        tk.Label(title_frame, text="📚 Cadastro de Disciplina", font=('Arial', 18, 'bold'),
                bg='white', fg='#0046AD').pack(side='left')

        # Frame do formulário
        form_frame = tk.Frame(scrollable_frame, bg='white')
        form_frame.pack(fill='both', expand=True, padx=40)

        self.entries_disciplina_modulo = {}

        # Campos do formulário
        campos = [
            ('nome', 'Nome da Disciplina *', 'entry'),
            ('carga_horaria', 'Carga Horária (horas) *', 'entry'),
            ('professor_id', 'Professor', 'combo_professor'),
            ('turma_id', 'Turma', 'combo_turma'),
            ('descricao', 'Descrição', 'text'),
            ('status', 'Status', 'combo_status')
        ]

        row = 0
        for field, label, tipo in campos:
            # Label
            tk.Label(form_frame, text=label, font=('Arial', 11, 'bold'),
                    bg='white', fg='#0046AD').grid(row=row, column=0, sticky='w', pady=10, padx=10)

            # Campo
            if tipo == 'entry':
                entry = tk.Entry(form_frame, font=('Arial', 11), width=50, relief='solid', bd=1)
                entry.grid(row=row, column=1, sticky='ew', pady=10, padx=10)
                self.entries_disciplina_modulo[field] = entry

            elif tipo == 'text':
                text_widget = tk.Text(form_frame, font=('Arial', 10), width=50, height=4,
                                     relief='solid', bd=1, wrap='word')
                text_widget.grid(row=row, column=1, sticky='ew', pady=10, padx=10)
                self.entries_disciplina_modulo[field] = text_widget

            elif tipo == 'combo_professor':
                # Buscar professores
                self.cursor.execute("SELECT id, nome FROM professores WHERE status = 'Ativo' ORDER BY nome")
                professores = self.cursor.fetchall()
                prof_values = ['Selecione...'] + [f"{p[0]} - {p[1]}" for p in professores]

                combo = ttk.Combobox(form_frame, values=prof_values, state='readonly',
                                    font=('Arial', 11), width=48)
                combo.set('Selecione...')
                combo.grid(row=row, column=1, sticky='ew', pady=10, padx=10)
                self.entries_disciplina_modulo[field] = combo

            elif tipo == 'combo_turma':
                # Buscar turmas
                self.cursor.execute("SELECT id, nome FROM turmas WHERE status = 'Ativa' ORDER BY nome")
                turmas = self.cursor.fetchall()
                turma_values = ['Selecione...'] + [f"{t[0]} - {t[1]}" for t in turmas]

                combo = ttk.Combobox(form_frame, values=turma_values, state='readonly',
                                    font=('Arial', 11), width=48)
                combo.set('Selecione...')
                combo.grid(row=row, column=1, sticky='ew', pady=10, padx=10)
                self.entries_disciplina_modulo[field] = combo

            elif tipo == 'combo_status':
                combo = ttk.Combobox(form_frame, values=['Ativa', 'Inativa'], state='readonly',
                                    font=('Arial', 11), width=48)
                combo.set('Ativa')
                combo.grid(row=row, column=1, sticky='ew', pady=10, padx=10)
                self.entries_disciplina_modulo[field] = combo

            row += 1

        form_frame.columnconfigure(1, weight=1)

        # Botões
        btn_frame = tk.Frame(scrollable_frame, bg='white')
        btn_frame.pack(fill='x', pady=20, padx=40)

        ModernButton(btn_frame, text="💾 Salvar Disciplina", command=self.salvar_disciplina_modulo,
                    color='#0046AD').pack(side='left', padx=10)

        ModernButton(btn_frame, text="🔄 Limpar", command=self.limpar_formulario_disciplina_modulo,
                    color='#666666').pack(side='left', padx=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def limpar_formulario_disciplina_modulo(self):
        """Limpa o formulário de disciplina"""
        for field, widget in self.entries_disciplina_modulo.items():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, tk.Text):
                widget.delete('1.0', tk.END)
            elif isinstance(widget, ttk.Combobox):
                if field == 'status':
                    widget.set('Ativa')
                else:
                    widget.set('Selecione...')

    def salvar_disciplina_modulo(self):
        """Salva uma nova disciplina"""
        try:
            # Validar campos obrigatórios
            nome = self.entries_disciplina_modulo['nome'].get().strip()
            carga_horaria = self.entries_disciplina_modulo['carga_horaria'].get().strip()

            if not nome:
                messagebox.showwarning("Aviso", "O nome da disciplina é obrigatório!")
                return

            if not carga_horaria:
                messagebox.showwarning("Aviso", "A carga horária é obrigatória!")
                return

            try:
                carga_horaria = int(carga_horaria)
            except:
                messagebox.showwarning("Aviso", "A carga horária deve ser um número inteiro!")
                return

            # Obter professor e turma
            professor_combo = self.entries_disciplina_modulo['professor_id'].get()
            turma_combo = self.entries_disciplina_modulo['turma_id'].get()

            professor_id = None
            if professor_combo != 'Selecione...':
                professor_id = int(professor_combo.split(' - ')[0])

            turma_id = None
            if turma_combo != 'Selecione...':
                turma_id = int(turma_combo.split(' - ')[0])

            # Obter outros campos
            descricao = self.entries_disciplina_modulo['descricao'].get('1.0', tk.END).strip()
            status = self.entries_disciplina_modulo['status'].get()

            # Inserir no banco
            self.cursor.execute('''
                INSERT INTO disciplinas (nome, carga_horaria, professor_id, turma_id, descricao, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nome, carga_horaria, professor_id, turma_id, descricao, status))

            self.conn.commit()

            messagebox.showinfo("Sucesso", f"Disciplina '{nome}' cadastrada com sucesso!")
            self.registrar_log('CADASTRO', 'Disciplinas', f'Cadastrou disciplina: {nome}')

            # Limpar formulário
            self.limpar_formulario_disciplina_modulo()

            # Atualizar lista
            self.carregar_dados_disciplinas_modulo()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar disciplina: {str(e)}")

    def editar_disciplina_modulo(self):
        """Edita uma disciplina selecionada"""
        selected = self.tree_disciplinas_modulo.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma disciplina para editar!")
            return

        disc_id = self.tree_disciplinas_modulo.item(selected[0])['values'][0]
        messagebox.showinfo("Info", f"Funcionalidade de edição da disciplina ID {disc_id} será implementada.")

    def excluir_disciplina_modulo(self):
        """Exclui uma disciplina selecionada"""
        selected = self.tree_disciplinas_modulo.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma disciplina para excluir!")
            return

        disc_id = self.tree_disciplinas_modulo.item(selected[0])['values'][0]
        disc_nome = self.tree_disciplinas_modulo.item(selected[0])['values'][1]

        resposta = messagebox.askyesno("Confirmar Exclusão",
                                       f"Deseja realmente excluir a disciplina '{disc_nome}'?")

        if resposta:
            try:
                self.cursor.execute("DELETE FROM disciplinas WHERE id = ?", (disc_id,))
                self.conn.commit()

                messagebox.showinfo("Sucesso", f"Disciplina '{disc_nome}' excluída com sucesso!")
                self.registrar_log('EXCLUSÃO', 'Disciplinas', f'Excluiu disciplina: {disc_nome}')

                self.carregar_dados_disciplinas_modulo()

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir disciplina: {str(e)}")

    def exportar_disciplinas_modulo(self):
        """Exporta lista de disciplinas para Excel"""
        try:
            filtro_status = self.filtro_status_disciplina.get()

            if filtro_status == 'Todas':
                self.cursor.execute('''
                    SELECT d.id, d.nome, d.carga_horaria, p.nome, t.nome, d.status
                    FROM disciplinas d
                    LEFT JOIN professores p ON d.professor_id = p.id
                    LEFT JOIN turmas t ON d.turma_id = t.id
                    ORDER BY d.nome
                ''')
            else:
                self.cursor.execute('''
                    SELECT d.id, d.nome, d.carga_horaria, p.nome, t.nome, d.status
                    FROM disciplinas d
                    LEFT JOIN professores p ON d.professor_id = p.id
                    LEFT JOIN turmas t ON d.turma_id = t.id
                    WHERE d.status = ?
                    ORDER BY d.nome
                ''', (filtro_status,))

            disciplinas = self.cursor.fetchall()

            if not disciplinas:
                messagebox.showwarning("Aviso", "Não há disciplinas para exportar!")
                return

            # Criar DataFrame
            df = pd.DataFrame(disciplinas, columns=['ID', 'Nome', 'Carga Horária', 'Professor',
                                                   'Turma', 'Status'])

            # Salvar arquivo
            filename = filedialog.asksaveasfilename(
                defaultextension='.xlsx',
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialfile=f'disciplinas_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
            )

            if filename:
                df.to_excel(filename, index=False, engine='openpyxl')
                messagebox.showinfo("Sucesso", f"Disciplinas exportadas com sucesso!\n\nArquivo: {filename}")
                self.registrar_log('EXPORTAÇÃO', 'Disciplinas', f'Exportou lista de disciplinas')

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar disciplinas: {str(e)}")

    def carregar_aba_relatorios_disciplinas(self, parent):
        """Aba de relatórios de disciplinas"""
        frame = tk.Frame(parent, bg='#f8f9fa')
        parent.add(frame, text='📊 Relatórios')

        tk.Label(frame, text="Relatórios de Disciplinas", font=('Arial', 16, 'bold'),
                 bg='#f8f9fa', fg='#0046AD').pack(pady=20)

        tk.Label(frame, text="Funcionalidade de relatórios em desenvolvimento", font=('Arial', 12),
                 bg='#f8f9fa', fg='#666666').pack(pady=10)

    # ========== MÓDULO CONTROLE DE MATRÍCULAS ==========

    def carregar_controle_matriculas(self):
        """Carrega módulo de controle de matrículas"""
        self.limpar_conteudo()
        self.ativar_botao("📋 Controle de Matrículas")
        self.registrar_log('ACESSO', 'Controle de Matrículas', 'Acessou módulo de controle de matrículas')

        # Frame principal
        main_frame = tk.Frame(self.content_frame, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Título
        title_frame = tk.Frame(main_frame, bg='#f8f9fa')
        title_frame.pack(fill='x', pady=(0, 20))

        tk.Label(title_frame, text="Controle de Matrículas", font=('Arial', 24, 'bold'),
                 bg='#f8f9fa', fg='#0046AD').pack(anchor='w')

        tk.Label(title_frame, text="Gerenciamento completo de matrículas de alunos",
                 font=('Arial', 12), bg='#f8f9fa', fg='#666666').pack(anchor='w')

        # Notebook
        notebook = ttk.Notebook(main_frame, style='Custom.TNotebook')
        notebook.pack(fill='both', expand=True)

        # Abas
        self.carregar_aba_lista_matriculas(notebook)
        self.carregar_aba_nova_matricula(notebook)
        self.carregar_aba_relatorios_matriculas(notebook)

    def carregar_aba_lista_matriculas(self, parent):
        """Aba de listagem de matrículas"""
        frame = tk.Frame(parent, bg='white')
        parent.add(frame, text='📋 Lista de Matrículas')

        # Barra de ferramentas
        toolbar = tk.Frame(frame, bg='white', pady=10)
        toolbar.pack(fill='x', padx=20)

        # Busca
        search_frame = tk.Frame(toolbar, bg='white')
        search_frame.pack(side='left', fill='x', expand=True)

        tk.Label(search_frame, text="🔍 Buscar:", font=('Arial', 10, 'bold'),
                bg='white', fg='#0046AD').pack(side='left', padx=5)

        self.busca_matricula_var = tk.StringVar()
        busca_entry = tk.Entry(search_frame, textvariable=self.busca_matricula_var,
                              font=('Arial', 10), width=40, relief='solid', bd=1)
        busca_entry.pack(side='left', padx=5)
        busca_entry.bind('<KeyRelease>', self.buscar_matriculas)

        # Filtros
        tk.Label(search_frame, text="Status:", font=('Arial', 10),
                bg='white', fg='#666666').pack(side='left', padx=(20, 5))

        self.filtro_status_matricula = ttk.Combobox(search_frame, values=['Todas', 'Ativa', 'Inativa', 'Transferida'],
                                                     state='readonly', width=12, font=('Arial', 10))
        self.filtro_status_matricula.set('Ativa')
        self.filtro_status_matricula.pack(side='left', padx=5)
        self.filtro_status_matricula.bind('<<ComboboxSelected>>', lambda e: self.aplicar_filtros_matriculas())

        # Botões de ação
        btn_frame = tk.Frame(toolbar, bg='white')
        btn_frame.pack(side='right')

        ModernButton(btn_frame, text="➕ Nova Matrícula", command=lambda: parent.select(1),
                    color='#0046AD').pack(side='left', padx=5)

        ModernButton(btn_frame, text="✏️ Editar", command=self.editar_matricula,
                    color='#FFCC00').pack(side='left', padx=5)

        ModernButton(btn_frame, text="🔄 Transferir", command=self.transferir_matricula,
                    color='#17a2b8').pack(side='left', padx=5)

        ModernButton(btn_frame, text="❌ Cancelar", command=self.cancelar_matricula,
                    color='#dc3545').pack(side='left', padx=5)

        ModernButton(btn_frame, text="📊 Exportar", command=self.exportar_matriculas,
                    color='#28a745').pack(side='left', padx=5)

        # Tabela de matrículas
        table_frame = tk.Frame(frame, bg='white')
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Scrollbars
        scroll_y = ttk.Scrollbar(table_frame)
        scroll_y.pack(side='right', fill='y')

        scroll_x = ttk.Scrollbar(table_frame, orient='horizontal')
        scroll_x.pack(side='bottom', fill='x')

        # Treeview
        colunas = ('ID', 'Nº Matrícula', 'Aluno', 'Turma', 'Data Matrícula', 'Status')
        self.tree_matriculas = ttk.Treeview(table_frame, columns=colunas, show='headings',
                                           yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set,
                                           style='Custom.Treeview', height=20)

        # Configurar colunas
        self.tree_matriculas.heading('ID', text='ID')
        self.tree_matriculas.heading('Nº Matrícula', text='Nº Matrícula')
        self.tree_matriculas.heading('Aluno', text='Nome do Aluno')
        self.tree_matriculas.heading('Turma', text='Turma')
        self.tree_matriculas.heading('Data Matrícula', text='Data Matrícula')
        self.tree_matriculas.heading('Status', text='Status')

        self.tree_matriculas.column('ID', width=50, anchor='center')
        self.tree_matriculas.column('Nº Matrícula', width=120, anchor='center')
        self.tree_matriculas.column('Aluno', width=250, anchor='w')
        self.tree_matriculas.column('Turma', width=150, anchor='w')
        self.tree_matriculas.column('Data Matrícula', width=120, anchor='center')
        self.tree_matriculas.column('Status', width=100, anchor='center')

        scroll_y.config(command=self.tree_matriculas.yview)
        scroll_x.config(command=self.tree_matriculas.xview)

        self.tree_matriculas.pack(fill='both', expand=True)

        # Carregar dados
        self.carregar_dados_matriculas()

        # Bind duplo clique para editar
        self.tree_matriculas.bind('<Double-1>', lambda e: self.editar_matricula())

    def carregar_dados_matriculas(self, query=None, filtro_status='Ativa'):
        """Carrega dados das matrículas na tabela"""
        for item in self.tree_matriculas.get_children():
            self.tree_matriculas.delete(item)

        try:
            if query:
                sql = '''
                    SELECT m.id, m.numero_matricula, a.nome, t.nome, m.data_matricula, m.status
                    FROM matriculas m
                    INNER JOIN alunos a ON m.aluno_id = a.id
                    LEFT JOIN turmas t ON m.turma_id = t.id
                    WHERE (a.nome LIKE ? OR m.numero_matricula LIKE ? OR t.nome LIKE ?)
                '''
                params = [f'%{query}%', f'%{query}%', f'%{query}%']

                if filtro_status != 'Todas':
                    sql += ' AND m.status = ?'
                    params.append(filtro_status)

                sql += ' ORDER BY m.data_matricula DESC'
                self.cursor.execute(sql, params)
            else:
                if filtro_status == 'Todas':
                    self.cursor.execute('''
                        SELECT m.id, m.numero_matricula, a.nome, t.nome, m.data_matricula, m.status
                        FROM matriculas m
                        INNER JOIN alunos a ON m.aluno_id = a.id
                        LEFT JOIN turmas t ON m.turma_id = t.id
                        ORDER BY m.data_matricula DESC
                    ''')
                else:
                    self.cursor.execute('''
                        SELECT m.id, m.numero_matricula, a.nome, t.nome, m.data_matricula, m.status
                        FROM matriculas m
                        INNER JOIN alunos a ON m.aluno_id = a.id
                        LEFT JOIN turmas t ON m.turma_id = t.id
                        WHERE m.status = ?
                        ORDER BY m.data_matricula DESC
                    ''', (filtro_status,))

            matriculas = self.cursor.fetchall()

            for mat in matriculas:
                mat_id, numero, aluno, turma, data, status = mat
                turma = turma if turma else 'Não atribuída'

                # Cor de status
                if status == 'Ativa':
                    tags = ('ativa',)
                elif status == 'Inativa':
                    tags = ('inativa',)
                else:
                    tags = ('transferida',)

                self.tree_matriculas.insert('', 'end', values=(mat_id, numero, aluno, turma, data, status), tags=tags)

            # Configurar cores
            self.tree_matriculas.tag_configure('ativa', foreground='#28a745')
            self.tree_matriculas.tag_configure('inativa', foreground='#dc3545')
            self.tree_matriculas.tag_configure('transferida', foreground='#ffc107')

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar matrículas: {str(e)}")

    def buscar_matriculas(self, event=None):
        """Busca matrículas"""
        query = self.busca_matricula_var.get()
        filtro_status = self.filtro_status_matricula.get()
        self.carregar_dados_matriculas(query, filtro_status)

    def aplicar_filtros_matriculas(self):
        """Aplica filtros na lista de matrículas"""
        query = self.busca_matricula_var.get()
        filtro_status = self.filtro_status_matricula.get()
        self.carregar_dados_matriculas(query, filtro_status)

    def carregar_aba_nova_matricula(self, parent):
        """Aba de nova matrícula"""
        frame = tk.Frame(parent, bg='white')
        parent.add(frame, text='➕ Nova Matrícula')

        # Container com scroll
        canvas = tk.Canvas(frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Título
        title_frame = tk.Frame(scrollable_frame, bg='white')
        title_frame.pack(fill='x', pady=(20, 20), padx=20)

        tk.Label(title_frame, text="📋 Nova Matrícula", font=('Arial', 18, 'bold'),
                bg='white', fg='#0046AD').pack(side='left')

        # Frame do formulário
        form_frame = tk.Frame(scrollable_frame, bg='white')
        form_frame.pack(fill='both', expand=True, padx=40)

        self.entries_matricula = {}

        # Campos do formulário
        campos = [
            ('aluno_id', 'Aluno *', 'combo_aluno'),
            ('turma_id', 'Turma *', 'combo_turma'),
            ('data_matricula', 'Data da Matrícula *', 'entry'),
            ('numero_matricula', 'Número da Matrícula (automático)', 'entry_readonly'),
            ('observacoes', 'Observações', 'text')
        ]

        row = 0
        for field, label, tipo in campos:
            # Label
            tk.Label(form_frame, text=label, font=('Arial', 11, 'bold'),
                    bg='white', fg='#0046AD').grid(row=row, column=0, sticky='w', pady=10, padx=10)

            # Campo
            if tipo == 'entry':
                entry = tk.Entry(form_frame, font=('Arial', 11), width=50, relief='solid', bd=1)
                if field == 'data_matricula':
                    entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
                entry.grid(row=row, column=1, sticky='ew', pady=10, padx=10)
                self.entries_matricula[field] = entry

            elif tipo == 'entry_readonly':
                entry = tk.Entry(form_frame, font=('Arial', 11), width=50, relief='solid', bd=1, state='readonly')
                # Gerar número automático
                self.cursor.execute("SELECT COUNT(*) FROM matriculas")
                count = self.cursor.fetchone()[0]
                numero_auto = f"MAT{datetime.now().year}{str(count + 1).zfill(5)}"
                entry.configure(state='normal')
                entry.insert(0, numero_auto)
                entry.configure(state='readonly')
                entry.grid(row=row, column=1, sticky='ew', pady=10, padx=10)
                self.entries_matricula[field] = entry

            elif tipo == 'text':
                text_widget = tk.Text(form_frame, font=('Arial', 10), width=50, height=4,
                                     relief='solid', bd=1, wrap='word')
                text_widget.grid(row=row, column=1, sticky='ew', pady=10, padx=10)
                self.entries_matricula[field] = text_widget

            elif tipo == 'combo_aluno':
                # Buscar alunos ativos
                self.cursor.execute("SELECT id, nome FROM alunos WHERE status = 'Ativo' ORDER BY nome")
                alunos = self.cursor.fetchall()
                aluno_values = ['Selecione...'] + [f"{a[0]} - {a[1]}" for a in alunos]

                combo = ttk.Combobox(form_frame, values=aluno_values, state='readonly',
                                    font=('Arial', 11), width=48)
                combo.set('Selecione...')
                combo.grid(row=row, column=1, sticky='ew', pady=10, padx=10)
                self.entries_matricula[field] = combo

            elif tipo == 'combo_turma':
                # Buscar turmas ativas
                self.cursor.execute("SELECT id, nome, serie FROM turmas WHERE status = 'Ativa' ORDER BY nome")
                turmas = self.cursor.fetchall()
                turma_values = ['Selecione...'] + [f"{t[0]} - {t[1]} ({t[2]})" for t in turmas]

                combo = ttk.Combobox(form_frame, values=turma_values, state='readonly',
                                    font=('Arial', 11), width=48)
                combo.set('Selecione...')
                combo.grid(row=row, column=1, sticky='ew', pady=10, padx=10)
                self.entries_matricula[field] = combo

            row += 1

        form_frame.columnconfigure(1, weight=1)

        # Botões
        btn_frame = tk.Frame(scrollable_frame, bg='white')
        btn_frame.pack(fill='x', pady=20, padx=40)

        ModernButton(btn_frame, text="💾 Salvar Matrícula", command=self.salvar_matricula,
                    color='#0046AD').pack(side='left', padx=10)

        ModernButton(btn_frame, text="🔄 Limpar", command=self.limpar_formulario_matricula,
                    color='#666666').pack(side='left', padx=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def limpar_formulario_matricula(self):
        """Limpa o formulário de matrícula"""
        for field, widget in self.entries_matricula.items():
            if isinstance(widget, tk.Entry):
                if field == 'data_matricula':
                    widget.delete(0, tk.END)
                    widget.insert(0, datetime.now().strftime('%Y-%m-%d'))
                elif field != 'numero_matricula':  # Não limpar número automático
                    widget.delete(0, tk.END)
            elif isinstance(widget, tk.Text):
                widget.delete('1.0', tk.END)
            elif isinstance(widget, ttk.Combobox):
                widget.set('Selecione...')

        # Atualizar número automático
        self.cursor.execute("SELECT COUNT(*) FROM matriculas")
        count = self.cursor.fetchone()[0]
        numero_auto = f"MAT{datetime.now().year}{str(count + 1).zfill(5)}"
        self.entries_matricula['numero_matricula'].configure(state='normal')
        self.entries_matricula['numero_matricula'].delete(0, tk.END)
        self.entries_matricula['numero_matricula'].insert(0, numero_auto)
        self.entries_matricula['numero_matricula'].configure(state='readonly')

    def salvar_matricula(self):
        """Salva uma nova matrícula"""
        try:
            # Validar campos obrigatórios
            aluno_combo = self.entries_matricula['aluno_id'].get()
            turma_combo = self.entries_matricula['turma_id'].get()
            data_matricula = self.entries_matricula['data_matricula'].get().strip()

            if aluno_combo == 'Selecione...':
                messagebox.showwarning("Aviso", "Selecione um aluno!")
                return

            if turma_combo == 'Selecione...':
                messagebox.showwarning("Aviso", "Selecione uma turma!")
                return

            if not data_matricula:
                messagebox.showwarning("Aviso", "A data da matrícula é obrigatória!")
                return

            aluno_id = int(aluno_combo.split(' - ')[0])
            turma_id = int(turma_combo.split(' - ')[0])

            numero_matricula = self.entries_matricula['numero_matricula'].get()
            observacoes = self.entries_matricula['observacoes'].get('1.0', tk.END).strip()

            # Verificar se aluno já tem matrícula ativa
            self.cursor.execute('''
                SELECT COUNT(*) FROM matriculas 
                WHERE aluno_id = ? AND status = 'Ativa'
            ''', (aluno_id,))

            if self.cursor.fetchone()[0] > 0:
                messagebox.showwarning("Aviso", "Este aluno já possui uma matrícula ativa!")
                return

            # Inserir no banco
            self.cursor.execute('''
                INSERT INTO matriculas (aluno_id, turma_id, data_matricula, numero_matricula, 
                                       observacoes, status)
                VALUES (?, ?, ?, ?, ?, 'Ativa')
            ''', (aluno_id, turma_id, data_matricula, numero_matricula, observacoes))

            self.conn.commit()

            messagebox.showinfo("Sucesso", f"Matrícula '{numero_matricula}' realizada com sucesso!")
            self.registrar_log('CADASTRO', 'Matrículas', f'Nova matrícula: {numero_matricula}')

            # Limpar formulário
            self.limpar_formulario_matricula()

            # Atualizar lista
            self.carregar_dados_matriculas()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar matrícula: {str(e)}")

    def editar_matricula(self):
        """Edita uma matrícula selecionada"""
        selected = self.tree_matriculas.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma matrícula para editar!")
            return

        mat_id = self.tree_matriculas.item(selected[0])['values'][0]
        messagebox.showinfo("Info", f"Funcionalidade de edição da matrícula ID {mat_id} será implementada.")

    def transferir_matricula(self):
        """Transfere um aluno para outra turma"""
        selected = self.tree_matriculas.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma matrícula para transferir!")
            return

        mat_id = self.tree_matriculas.item(selected[0])['values'][0]
        messagebox.showinfo("Info", f"Funcionalidade de transferência da matrícula ID {mat_id} será implementada.")

    def cancelar_matricula(self):
        """Cancela uma matrícula"""
        selected = self.tree_matriculas.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma matrícula para cancelar!")
            return

        mat_id = self.tree_matriculas.item(selected[0])['values'][0]
        mat_numero = self.tree_matriculas.item(selected[0])['values'][1]

        resposta = messagebox.askyesno("Confirmar Cancelamento",
                                       f"Deseja realmente cancelar a matrícula '{mat_numero}'?")

        if resposta:
            try:
                self.cursor.execute("UPDATE matriculas SET status = 'Inativa' WHERE id = ?", (mat_id,))
                self.conn.commit()

                messagebox.showinfo("Sucesso", f"Matrícula '{mat_numero}' cancelada com sucesso!")
                self.registrar_log('CANCELAMENTO', 'Matrículas', f'Cancelou matrícula: {mat_numero}')

                self.carregar_dados_matriculas()

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao cancelar matrícula: {str(e)}")

    def exportar_matriculas(self):
        """Exporta lista de matrículas para Excel"""
        try:
            filtro_status = self.filtro_status_matricula.get()

            if filtro_status == 'Todas':
                self.cursor.execute('''
                    SELECT m.id, m.numero_matricula, a.nome, t.nome, m.data_matricula, m.status
                    FROM matriculas m
                    INNER JOIN alunos a ON m.aluno_id = a.id
                    LEFT JOIN turmas t ON m.turma_id = t.id
                    ORDER BY m.data_matricula DESC
                ''')
            else:
                self.cursor.execute('''
                    SELECT m.id, m.numero_matricula, a.nome, t.nome, m.data_matricula, m.status
                    FROM matriculas m
                    INNER JOIN alunos a ON m.aluno_id = a.id
                    LEFT JOIN turmas t ON m.turma_id = t.id
                    WHERE m.status = ?
                    ORDER BY m.data_matricula DESC
                ''', (filtro_status,))

            matriculas = self.cursor.fetchall()

            if not matriculas:
                messagebox.showwarning("Aviso", "Não há matrículas para exportar!")
                return

            # Criar DataFrame
            df = pd.DataFrame(matriculas, columns=['ID', 'Nº Matrícula', 'Aluno', 'Turma',
                                                   'Data Matrícula', 'Status'])

            # Salvar arquivo
            filename = filedialog.asksaveasfilename(
                defaultextension='.xlsx',
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                initialfile=f'matriculas_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
            )

            if filename:
                df.to_excel(filename, index=False, engine='openpyxl')
                messagebox.showinfo("Sucesso", f"Matrículas exportadas com sucesso!\n\nArquivo: {filename}")
                self.registrar_log('EXPORTAÇÃO', 'Matrículas', f'Exportou lista de matrículas')

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar matrículas: {str(e)}")

    def carregar_aba_relatorios_matriculas(self, parent):
        """Aba de relatórios de matrículas"""
        frame = tk.Frame(parent, bg='#f8f9fa')
        parent.add(frame, text='📊 Relatórios')

        tk.Label(frame, text="Relatórios de Matrículas", font=('Arial', 16, 'bold'),
                 bg='#f8f9fa', fg='#0046AD').pack(pady=20)

        tk.Label(frame, text="Funcionalidade de relatórios em desenvolvimento", font=('Arial', 12),
                 bg='#f8f9fa', fg='#666666').pack(pady=10)

    # ========== MÓDULO CONTROLE DE FREQUÊNCIA ==========

    def carregar_controle_frequencia(self):
        """Carrega módulo de controle de frequência"""
        self.limpar_conteudo()
        self.ativar_botao("✅ Controle de Frequência")
        self.registrar_log('ACESSO', 'Controle de Frequência', 'Acessou módulo de controle de frequência')

        # Frame principal
        main_frame = tk.Frame(self.content_frame, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Título
        title_frame = tk.Frame(main_frame, bg='#f8f9fa')
        title_frame.pack(fill='x', pady=(0, 20))

        tk.Label(title_frame, text="Controle de Frequência", font=('Arial', 24, 'bold'),
                 bg='#f8f9fa', fg='#0046AD').pack(anchor='w')

        tk.Label(title_frame, text="Registro e acompanhamento de presença dos alunos",
                 font=('Arial', 12), bg='#f8f9fa', fg='#666666').pack(anchor='w')

        # Notebook
        notebook = ttk.Notebook(main_frame, style='Custom.TNotebook')
        notebook.pack(fill='both', expand=True)

        # Abas
        self.carregar_aba_registro_frequencia(notebook)
        self.carregar_aba_consulta_frequencia(notebook)
        self.carregar_aba_relatorio_frequencia(notebook)

    def carregar_aba_registro_frequencia(self, parent):
        """Aba de registro de frequência"""
        frame = tk.Frame(parent, bg='white')
        parent.add(frame, text='✅ Registrar Frequência')

        # Container com scroll
        canvas = tk.Canvas(frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Título
        title_frame = tk.Frame(scrollable_frame, bg='white')
        title_frame.pack(fill='x', pady=(20, 20), padx=20)

        tk.Label(title_frame, text="✅ Registro de Frequência", font=('Arial', 18, 'bold'),
                bg='white', fg='#0046AD').pack(side='left')

        # Seleção de turma e disciplina
        select_frame = tk.Frame(scrollable_frame, bg='white')
        select_frame.pack(fill='x', padx=40, pady=10)

        # Turma
        tk.Label(select_frame, text="Turma:", font=('Arial', 11, 'bold'),
                bg='white', fg='#0046AD').grid(row=0, column=0, sticky='w', pady=10, padx=10)

        self.cursor.execute("SELECT id, nome, serie FROM turmas WHERE status = 'Ativa' ORDER BY nome")
        turmas = self.cursor.fetchall()
        turma_values = ['Selecione...'] + [f"{t[0]} - {t[1]} ({t[2]})" for t in turmas]

        self.combo_turma_freq = ttk.Combobox(select_frame, values=turma_values, state='readonly',
                                            font=('Arial', 11), width=40)
        self.combo_turma_freq.set('Selecione...')
        self.combo_turma_freq.grid(row=0, column=1, sticky='ew', pady=10, padx=10)
        self.combo_turma_freq.bind('<<ComboboxSelected>>', self.carregar_alunos_frequencia)

        # Disciplina
        tk.Label(select_frame, text="Disciplina:", font=('Arial', 11, 'bold'),
                bg='white', fg='#0046AD').grid(row=1, column=0, sticky='w', pady=10, padx=10)

        self.combo_disciplina_freq = ttk.Combobox(select_frame, values=['Selecione uma turma primeiro'],
                                                 state='readonly', font=('Arial', 11), width=40)
        self.combo_disciplina_freq.set('Selecione uma turma primeiro')
        self.combo_disciplina_freq.grid(row=1, column=1, sticky='ew', pady=10, padx=10)

        # Data
        tk.Label(select_frame, text="Data:", font=('Arial', 11, 'bold'),
                bg='white', fg='#0046AD').grid(row=2, column=0, sticky='w', pady=10, padx=10)

        self.entry_data_freq = tk.Entry(select_frame, font=('Arial', 11), width=42, relief='solid', bd=1)
        self.entry_data_freq.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.entry_data_freq.grid(row=2, column=1, sticky='ew', pady=10, padx=10)

        select_frame.columnconfigure(1, weight=1)

        # Botão carregar alunos
        btn_carregar = tk.Frame(scrollable_frame, bg='white')
        btn_carregar.pack(pady=10)

        ModernButton(btn_carregar, text="📋 Carregar Alunos", command=self.carregar_alunos_frequencia,
                    color='#0046AD').pack()

        # Frame para lista de alunos
        self.frame_lista_freq = tk.Frame(scrollable_frame, bg='white')
        self.frame_lista_freq.pack(fill='both', expand=True, padx=40, pady=20)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def carregar_alunos_frequencia(self, event=None):
        """Carrega lista de alunos para registro de frequência"""
        # Limpar frame anterior
        for widget in self.frame_lista_freq.winfo_children():
            widget.destroy()

        turma_combo = self.combo_turma_freq.get()
        if turma_combo == 'Selecione...':
            messagebox.showwarning("Aviso", "Selecione uma turma!")
            return

        turma_id = int(turma_combo.split(' - ')[0])

        # Carregar disciplinas da turma
        self.cursor.execute('''
            SELECT id, nome FROM disciplinas 
            WHERE turma_id = ? AND status = 'Ativa'
            ORDER BY nome
        ''', (turma_id,))
        disciplinas = self.cursor.fetchall()

        if disciplinas:
            disc_values = ['Selecione...'] + [f"{d[0]} - {d[1]}" for d in disciplinas]
            self.combo_disciplina_freq.configure(values=disc_values)
            self.combo_disciplina_freq.set('Selecione...')
        else:
            self.combo_disciplina_freq.configure(values=['Nenhuma disciplina encontrada'])
            self.combo_disciplina_freq.set('Nenhuma disciplina encontrada')

        # Carregar alunos da turma
        self.cursor.execute('''
            SELECT a.id, a.nome
            FROM alunos a
            INNER JOIN matriculas m ON a.id = m.aluno_id
            WHERE m.turma_id = ? AND m.status = 'Ativa' AND a.status = 'Ativo'
            ORDER BY a.nome
        ''', (turma_id,))

        alunos = self.cursor.fetchall()

        if not alunos:
            tk.Label(self.frame_lista_freq, text="Nenhum aluno encontrado nesta turma.",
                    font=('Arial', 12), bg='white', fg='#666666').pack(pady=20)
            return

        # Título da lista
        tk.Label(self.frame_lista_freq, text="Lista de Alunos - Marque os PRESENTES:",
                font=('Arial', 12, 'bold'), bg='white', fg='#0046AD').pack(anchor='w', pady=10)

        # Frame para checkboxes
        check_frame = tk.Frame(self.frame_lista_freq, bg='white')
        check_frame.pack(fill='both', expand=True)

        self.freq_vars = {}

        for i, (aluno_id, aluno_nome) in enumerate(alunos):
            var = tk.IntVar(value=1)  # Presente por padrão
            self.freq_vars[aluno_id] = var

            row_frame = tk.Frame(check_frame, bg='white')
            row_frame.pack(fill='x', pady=2)

            tk.Checkbutton(row_frame, text=f"{aluno_nome}", variable=var,
                          font=('Arial', 11), bg='white', fg='#333333',
                          selectcolor='#FFCC00', activebackground='white').pack(side='left', padx=10)

        # Botões de ação
        btn_frame = tk.Frame(self.frame_lista_freq, bg='white')
        btn_frame.pack(pady=20)

        ModernButton(btn_frame, text="✅ Marcar Todos Presentes",
                    command=lambda: self.marcar_todos_freq(1),
                    color='#28a745').pack(side='left', padx=10)

        ModernButton(btn_frame, text="❌ Marcar Todos Ausentes",
                    command=lambda: self.marcar_todos_freq(0),
                    color='#dc3545').pack(side='left', padx=10)

        ModernButton(btn_frame, text="💾 Salvar Frequência",
                    command=self.salvar_frequencia,
                    color='#0046AD').pack(side='left', padx=10)

    def marcar_todos_freq(self, valor):
        """Marca todos os alunos como presentes ou ausentes"""
        for var in self.freq_vars.values():
            var.set(valor)

    def salvar_frequencia(self):
        """Salva o registro de frequência"""
        try:
            turma_combo = self.combo_turma_freq.get()
            disciplina_combo = self.combo_disciplina_freq.get()
            data_aula = self.entry_data_freq.get().strip()

            if turma_combo == 'Selecione...':
                messagebox.showwarning("Aviso", "Selecione uma turma!")
                return

            if disciplina_combo == 'Selecione...' or disciplina_combo == 'Nenhuma disciplina encontrada':
                messagebox.showwarning("Aviso", "Selecione uma disciplina!")
                return

            if not data_aula:
                messagebox.showwarning("Aviso", "Informe a data da aula!")
                return

            turma_id = int(turma_combo.split(' - ')[0])
            disciplina_id = int(disciplina_combo.split(' - ')[0])

            # Verificar se já existe registro para esta data
            self.cursor.execute('''
                SELECT COUNT(*) FROM frequencia 
                WHERE turma_id = ? AND disciplina_id = ? AND data_aula = ?
            ''', (turma_id, disciplina_id, data_aula))

            if self.cursor.fetchone()[0] > 0:
                resposta = messagebox.askyesno("Aviso",
                                              "Já existe registro de frequência para esta data.\n"
                                              "Deseja sobrescrever?")
                if not resposta:
                    return

                # Deletar registros antigos
                self.cursor.execute('''
                    DELETE FROM frequencia 
                    WHERE turma_id = ? AND disciplina_id = ? AND data_aula = ?
                ''', (turma_id, disciplina_id, data_aula))

            # Inserir novos registros
            for aluno_id, var in self.freq_vars.items():
                presente = var.get()
                self.cursor.execute('''
                    INSERT INTO frequencia (aluno_id, disciplina_id, turma_id, data_aula, presente)
                    VALUES (?, ?, ?, ?, ?)
                ''', (aluno_id, disciplina_id, turma_id, data_aula, presente))

            self.conn.commit()

            messagebox.showinfo("Sucesso", "Frequência registrada com sucesso!")
            self.registrar_log('REGISTRO', 'Frequência', f'Registrou frequência para {data_aula}')

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar frequência: {str(e)}")

    def carregar_aba_consulta_frequencia(self, parent):
        """Aba de consulta de frequência"""
        frame = tk.Frame(parent, bg='white')
        parent.add(frame, text='🔍 Consultar Frequência')

        tk.Label(frame, text="Consulta de Frequência", font=('Arial', 16, 'bold'),
                 bg='white', fg='#0046AD').pack(pady=20)

        tk.Label(frame, text="Funcionalidade de consulta em desenvolvimento", font=('Arial', 12),
                 bg='white', fg='#666666').pack(pady=10)

    def carregar_aba_relatorio_frequencia(self, parent):
        """Aba de relatórios de frequência"""
        frame = tk.Frame(parent, bg='#f8f9fa')
        parent.add(frame, text='📊 Relatórios')

        tk.Label(frame, text="Relatórios de Frequência", font=('Arial', 16, 'bold'),
                 bg='#f8f9fa', fg='#0046AD').pack(pady=20)

        tk.Label(frame, text="Funcionalidade de relatórios em desenvolvimento", font=('Arial', 12),
                 bg='#f8f9fa', fg='#666666').pack(pady=10)

    
    def carregar_calendario_escolar(self):
        """Carrega módulo de calendário escolar funcional"""
        self.limpar_conteudo()
        self.ativar_botao("📅 Calendário Escolar")
        self.registrar_log('ACESSO', 'Calendário Escolar', 'Acessou módulo de calendário escolar')

        main_frame = tk.Frame(self.content_frame, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        header = tk.Frame(main_frame, bg='#f8f9fa')
        header.pack(fill='x', pady=(0, 20))

        tk.Label(header, text="📅 Calendário Escolar", font=('Arial', 24, 'bold'),
                 bg='#f8f9fa', fg='#0046AD').pack(side='left')

        nav_frame = tk.Frame(header, bg='#f8f9fa')
        nav_frame.pack(side='right')

        hoje = datetime.now()
        self.cal_mes = hoje.month
        self.cal_ano = hoje.year

        def atualizar_calendario():
            for widget in cal_grid.winfo_children():
                widget.destroy()
            
            lbl_mes_ano.config(text=f"{calendar.month_name[self.cal_mes].upper()} {self.cal_ano}")
            
            dias = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']
            for i, dia in enumerate(dias):
                lbl = tk.Label(cal_grid, text=dia, font=('Arial', 10, 'bold'), 
                               bg='#0046AD', fg='white', width=10, pady=5)
                lbl.grid(row=0, column=i, padx=1, pady=1, sticky='nsew')

            cal = calendar.monthcalendar(self.cal_ano, self.cal_mes)
            for r, semana in enumerate(cal):
                for c, dia in enumerate(semana):
                    if dia == 0:
                        lbl = tk.Label(cal_grid, text="", bg='white', relief='flat')
                    else:
                        bg_color = 'white'
                        if dia == hoje.day and self.cal_mes == hoje.month and self.cal_ano == hoje.year:
                            bg_color = '#FFCC00'
                        
                        lbl = tk.Label(cal_grid, text=str(dia), font=('Arial', 12),
                                       bg=bg_color, relief='solid', bd=1,
                                       width=10, height=4, anchor='nw', padx=5, pady=5)
                        
                        if dia == 5 and self.cal_mes == 2:
                            tk.Label(lbl, text="Início Aulas", font=('Arial', 8), bg='#0046AD', fg='white').pack(fill='x', pady=2)

                    lbl.grid(row=r+1, column=c, padx=1, pady=1, sticky='nsew')

        def mes_anterior():
            self.cal_mes -= 1
            if self.cal_mes < 1: self.cal_mes = 12; self.cal_ano -= 1
            atualizar_calendario()

        def proximo_mes():
            self.cal_mes += 1
            if self.cal_mes > 12: self.cal_mes = 1; self.cal_ano += 1
            atualizar_calendario()

        tk.Button(nav_frame, text="◀", command=mes_anterior, bg='#0046AD', fg='white', relief='flat', padx=10).pack(side='left', padx=5)
        lbl_mes_ano = tk.Label(nav_frame, text="", font=('Arial', 14, 'bold'), bg='#f8f9fa', width=20)
        lbl_mes_ano.pack(side='left')
        tk.Button(nav_frame, text="▶", command=proximo_mes, bg='#0046AD', fg='white', relief='flat', padx=10).pack(side='left', padx=5)

        cal_grid = tk.Frame(main_frame, bg='#e0e0e0')
        cal_grid.pack(fill='both', expand=True)
        for i in range(7): cal_grid.columnconfigure(i, weight=1)
        atualizar_calendario()


    # ========== MÓDULO COMUNICADOS E AVISOS ==========

    
    def carregar_comunicados_avisos(self):
        """Carrega módulo de comunicados e avisos funcional"""
        self.limpar_conteudo()
        self.ativar_botao("📢 Comunicados e Avisos")
        self.registrar_log('ACESSO', 'Comunicados', 'Acessou módulo de comunicados')

        main_frame = tk.Frame(self.content_frame, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        tk.Label(main_frame, text="📢 Comunicados e Avisos", font=('Arial', 24, 'bold'),
                 bg='#f8f9fa', fg='#0046AD').pack(anchor='w', pady=(0, 20))

        list_frame = tk.Frame(main_frame, bg='white', relief='solid', bd=1)
        list_frame.pack(fill='both', expand=True)

        columns = ('ID', 'Título', 'Data', 'Prioridade')
        tree = ttk.Treeview(list_frame, columns=columns, show='headings', style='Custom.Treeview')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(side='left', fill='both', expand=True)

        btn_frame = tk.Frame(main_frame, bg='#f8f9fa')
        btn_frame.pack(fill='x', pady=20)
        ModernButton(btn_frame, text="➕ Novo Comunicado", color='#0046AD').pack(side='left', padx=5)


    # ========== MÓDULO OCORRÊNCIAS DISCIPLINARES ==========

    
    def carregar_ocorrencias_disciplinares(self):
        """Carrega módulo de ocorrências disciplinares funcional"""
        self.limpar_conteudo()
        self.ativar_botao("🔔 Ocorrências Disciplinares")
        self.registrar_log('ACESSO', 'Ocorrências', 'Acessou módulo de ocorrências')

        main_frame = tk.Frame(self.content_frame, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        tk.Label(main_frame, text="🔔 Ocorrências Disciplinares", font=('Arial', 24, 'bold'),
                 bg='#f8f9fa', fg='#0046AD').pack(anchor='w', pady=(0, 20))

        list_frame = tk.Frame(main_frame, bg='white', relief='solid', bd=1)
        list_frame.pack(fill='both', expand=True)

        columns = ('ID', 'Aluno', 'Tipo', 'Data', 'Status')
        tree = ttk.Treeview(list_frame, columns=columns, show='headings', style='Custom.Treeview')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(side='left', fill='both', expand=True)

        btn_frame = tk.Frame(main_frame, bg='#f8f9fa')
        btn_frame.pack(fill='x', pady=20)
        ModernButton(btn_frame, text="➕ Registrar Ocorrência", color='#0046AD').pack(side='left', padx=5)


    # ========== MÓDULO RELATÓRIOS GERENCIAIS ==========

    
    def carregar_relatorios_gerenciais(self):
        """Carrega módulo de relatórios gerenciais funcional"""
        self.limpar_conteudo()
        self.ativar_botao("📋 Relatórios Gerenciais")
        
        main_frame = tk.Frame(self.content_frame, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        tk.Label(main_frame, text="📋 Relatórios Gerenciais", font=('Arial', 24, 'bold'),
                 bg='#f8f9fa', fg='#0046AD').pack(anchor='w', pady=(0, 20))

        grid_frame = tk.Frame(main_frame, bg='#f8f9fa')
        grid_frame.pack(fill='both', expand=True)

        relatorios = [
            ("📊 Desempenho por Turma", "Visualizar médias e aprovações"),
            ("👥 Lista de Alunos Ativos", "Relatório completo de matrículas"),
            ("💰 Resumo Financeiro", "Balanço de mensalidades"),
            ("📅 Frequência Mensal", "Relatório de assiduidade")
        ]

        for i, (titulo, desc) in enumerate(relatorios):
            card = tk.Frame(grid_frame, bg='white', relief='solid', bd=1, padx=15, pady=15)
            card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky='nsew')
            tk.Label(card, text=titulo, font=('Arial', 12, 'bold'), bg='white', fg='#0046AD').pack(anchor='w')
            tk.Label(card, text=desc, font=('Arial', 10), bg='white', fg='#666666').pack(anchor='w', pady=5)
            ModernButton(card, text="Gerar PDF", color='#666666').pack(anchor='e')


    # ========== MÓDULO HISTÓRICO ESCOLAR ==========

    def carregar_historico_escolar(self):
        """Carrega módulo de histórico escolar"""
        self.limpar_conteudo()
        self.ativar_botao("🎓 Histórico Escolar")
        self.registrar_log('ACESSO', 'Histórico Escolar', 'Acessou módulo de histórico escolar')

        tk.Label(self.content_frame, text="Módulo de Histórico Escolar - Registro Acadêmico Completo",
                 font=('Arial', 16), bg='#f8f9fa').pack(expand=True)

    # ========== MÓDULO PLANEJAMENTO PEDAGÓGICO ==========

    def carregar_planejamento_pedagogico(self):
        """Carrega módulo de planejamento pedagógico"""
        self.limpar_conteudo()
        self.ativar_botao("📈 Planejamento Pedagógico")
        self.registrar_log('ACESSO', 'Planejamento Pedagógico', 'Acessou módulo de planejamento pedagógico')

        tk.Label(self.content_frame, text="Módulo de Planejamento Pedagógico - Estrutura Curricular",
                 font=('Arial', 16), bg='#f8f9fa').pack(expand=True)

    # ========== MÓDULO AVALIAÇÕES INSTITUCIONAIS ==========

    def carregar_avaliacoes_institucionais(self):
        """Carrega módulo de avaliações institucionais"""
        self.limpar_conteudo()
        self.ativar_botao("🏆 Avaliações Institucionais")
        self.registrar_log('ACESSO', 'Avaliações Institucionais', 'Acessou módulo de avaliações institucionais')

        tk.Label(self.content_frame, text="Módulo de Avaliações Institucionais - Pesquisas e Avaliações",
                 font=('Arial', 16), bg='#f8f9fa').pack(expand=True)

    # ========== MÓDULO CONFIGURAÇÕES DO SISTEMA ==========

    def carregar_configuracoes_sistema(self):
        """Carrega módulo de configurações do sistema"""
        self.limpar_conteudo()
        self.ativar_botao("⚙️ Configurações do Sistema")
        self.registrar_log('ACESSO', 'Configurações do Sistema', 'Acessou módulo de configurações do sistema')

        tk.Label(self.content_frame, text="Módulo de Configurações do Sistema - Personalização do Sistema",
                 font=('Arial', 16), bg='#f8f9fa').pack(expand=True)


# ========== EXECUÇÃO DO SISTEMA ==========
class SistemaMatriculas:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Matrículas Escolares")
        self.root.geometry("1200x800")

        # Criar notebook para abas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Abas do sistema
        self.criar_aba_instituicao()
        self.criar_aba_aluno()
        self.criar_aba_responsavel_financeiro()
        self.criar_aba_responsavel_pedagogico()
        self.criar_aba_consultas()

    def criar_aba_instituicao(self):
        # Implementação da aba da instituição
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Instituição")

        # Campos da instituição
        ttk.Label(frame, text="Dados da Instituição", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2,
                                                                                       pady=10)

        campos_instituicao = [
            ("Nome da Instituição:", "nome"),
            ("Endereço:", "endereco"),
            ("Mantenedora:", "mantenedora"),
            ("CNPJ:", "cnpj")
        ]

        self.entries_instituicao = {}
        for i, (label, field) in enumerate(campos_instituicao):
            ttk.Label(frame, text=label).grid(row=i + 1, column=0, sticky='w', padx=5, pady=5)
            entry = ttk.Entry(frame, width=50)
            entry.grid(row=i + 1, column=1, padx=5, pady=5)
            self.entries_instituicao[field] = entry

        ttk.Button(frame, text="Salvar Dados da Instituição",
                   command=self.salvar_instituicao).grid(row=5, column=0, columnspan=2, pady=10)

    def criar_aba_aluno(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Dados do Aluno")

        # Criar scrollbar
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Campos do aluno
        ttk.Label(scrollable_frame, text="Dados do Beneficiário (ALUNO)",
                  font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        campos_aluno = [
            # Dados básicos
            ("Número de Matrícula:", "numero_matricula"),
            ("Nome Completo:", "nome_completo"),
            ("Data Nascimento (dd/mm/aaaa):", "data_nascimento"),
            ("CPF:", "cpf"),

            # Certidão de Nascimento
            ("Certidão - Número:", "certidao_numero"),
            ("Certidão - Livro:", "certidao_livro"),
            ("Certidão - Folha:", "certidao_folha"),
            ("Certidão - Data Expedição:", "certidao_data_expedicao"),
            ("Certidão - Cidade:", "certidao_cidade"),
            ("Certidão - UF:", "certidao_uf"),
            ("Certidão - Cartório:", "certidao_cartorio"),

            # RG
            ("RG - UF:", "rg_uf"),
            ("RG - Data Expedição:", "rg_data_expedicao"),

            # Dados pessoais
            ("Sexo:", "sexo"),
            ("Cor/Raça:", "cor_raca"),

            # Endereço
            ("Bairro:", "endereco_bairro"),
            ("Cidade:", "endereco_cidade"),
            ("Estado:", "endereco_estado"),
            ("CEP:", "endereco_cep"),

            # Dados escolares
            ("Curso:", "curso"),
            ("Ano/Série:", "ano_serie"),
            ("Data Ingresso:", "data_ingresso"),

            # Saúde e informações
            ("Necessidades Especiais:", "necessidades_especiais"),
            ("Alergias:", "alergias"),
            ("Convênio Médico:", "convenio_medico"),
            ("Colégio Anterior:", "colegio_anterior"),

            # Contato
            ("Email:", "email"),
            ("Celular:", "celular"),
            ("Operadora:", "operadora"),
            ("Nome Completo da Mãe:", "nome_mae")
        ]

        self.entries_aluno = {}
        for i, (label, field) in enumerate(campos_aluno):
            ttk.Label(scrollable_frame, text=label).grid(row=i + 1, column=0, sticky='w', padx=5, pady=2)
            if field in ['sexo', 'cor_raca', 'curso', 'ano_serie']:
                # Combobox para campos com opções fixas
                if field == 'sexo':
                    values = ['Masculino', 'Feminino']
                elif field == 'cor_raca':
                    values = ['Branca', 'Preta', 'Amarela', 'Parda', 'Indígena']
                elif field == 'curso':
                    values = ['Educação Infantil', 'Ensino Fundamental 1', 'Ensino Fundamental 2', 'Ensino Médio']
                elif field == 'ano_serie':
                    values = [
                        'Berçário', 'Maternal', 'Infantil I', 'Infantil II', 'Infantil III', 'Infantil IV',
                        '1º ano', '2º ano', '3º ano', '4º ano', '5º ano',
                        '6º ano', '7º ano', '8º ano', '9º ano',
                        '1ª série', '2ª série', '3ª série'
                    ]

                combobox = ttk.Combobox(scrollable_frame, values=values, width=47)
                combobox.grid(row=i + 1, column=1, padx=5, pady=2)
                self.entries_aluno[field] = combobox
            else:
                entry = ttk.Entry(scrollable_frame, width=50)
                entry.grid(row=i + 1, column=1, padx=5, pady=2)
                self.entries_aluno[field] = entry

        # Botão para upload de foto
        ttk.Button(scrollable_frame, text="Upload Foto do Aluno",
                   command=self.upload_foto).grid(row=len(campos_aluno) + 1, column=0, pady=10)

        self.foto_path_label = ttk.Label(scrollable_frame, text="Nenhuma foto selecionada")
        self.foto_path_label.grid(row=len(campos_aluno) + 1, column=1, pady=10)

        # Botão salvar
        ttk.Button(scrollable_frame, text="Salvar Dados do Aluno",
                   command=self.salvar_aluno).grid(row=len(campos_aluno) + 2, column=0, columnspan=2, pady=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def criar_aba_responsavel_financeiro(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Responsável Financeiro")
        # Implementação similar à aba do aluno...

    def criar_aba_responsavel_pedagogico(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Responsável Pedagógico")
        # Implementação similar...

    def criar_aba_consultas(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Consultas")
        # Implementação das consultas...

    def upload_foto(self):
        filename = filedialog.askopenfilename(
            title="Selecionar Foto do Aluno",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if filename:
            self.foto_path = filename
            self.foto_path_label.config(text=os.path.basename(filename))

    def salvar_instituicao(self):
        # Implementação para salvar dados da instituição
        pass

    def salvar_aluno(self):
        # Implementação para salvar dados do aluno
        try:
            conn = sqlite3.connect('matriculas.db')
            cursor = conn.cursor()

            # Coletar dados dos campos
            dados_aluno = {}
            for field, entry in self.entries_aluno.items():
                if isinstance(entry, ttk.Combobox):
                    dados_aluno[field] = entry.get()
                else:
                    dados_aluno[field] = entry.get()

            # Inserir no banco de dados
            cursor.execute('''
                INSERT INTO alunos (
                    foto_path, numero_matricula, nome_completo, data_nascimento,
                    certidao_numero, certidao_livro, certidao_folha, certidao_data_expedicao,
                    certidao_cidade, certidao_uf, certidao_cartorio, rg_uf, rg_data_expedicao,
                    cpf, sexo, cor_raca, endereco_bairro, endereco_cidade, endereco_estado,
                    endereco_cep, curso, ano_serie, data_ingresso, necessidades_especiais,
                    alergias, convenio_medico, colegio_anterior, email, celular, operadora, nome_mae
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                getattr(self, 'foto_path', ''),
                dados_aluno['numero_matricula'],
                dados_aluno['nome_completo'],
                dados_aluno['data_nascimento'],
                dados_aluno['certidao_numero'],
                dados_aluno['certidao_livro'],
                dados_aluno['certidao_folha'],
                dados_aluno['certidao_data_expedicao'],
                dados_aluno['certidao_cidade'],
                dados_aluno['certidao_uf'],
                dados_aluno['certidao_cartorio'],
                dados_aluno['rg_uf'],
                dados_aluno['rg_data_expedicao'],
                dados_aluno['cpf'],
                dados_aluno['sexo'],
                dados_aluno['cor_raca'],
                dados_aluno['endereco_bairro'],
                dados_aluno['endereco_cidade'],
                dados_aluno['endereco_estado'],
                dados_aluno['endereco_cep'],
                dados_aluno['curso'],
                dados_aluno['ano_serie'],
                dados_aluno['data_ingresso'],
                dados_aluno['necessidades_especiais'],
                dados_aluno['alergias'],
                dados_aluno['convenio_medico'],
                dados_aluno['colegio_anterior'],
                dados_aluno['email'],
                dados_aluno['celular'],
                dados_aluno['operadora'],
                dados_aluno['nome_mae']
            ))

            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Dados do aluno salvos com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar dados: {str(e)}")

            # =============================================================================
            # FUNÇÃO PARA INICIAR SISTEMA DE MATRÍCULAS
            # =============================================================================

            def abrir_sistema_matriculas():
                """Função para abrir o sistema de matrículas em uma nova janela"""
                root = tk.Toplevel()
                root.title("Sistema de Matrículas Escolares")
                root.geometry("1200x800")
                app = SistemaMatriculas(root)
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = SistemaGestaoEscolar(root)
        root.mainloop()
    except Exception as e:
        print(f"Erro ao executar o sistema: {e}")
        messagebox.showerror("Erro", f"Falha ao iniciar o sistema: {str(e)}")
        if __name__ == "__main__":
            # Seu código principal existente...

            # Adicione um botão para matrículas (adapte conforme sua interface)
            botao_matriculas = tk.Button(sua_janela_principal,
                                         text="📋 Sistema de Matrículas",
                                         command=abrir_sistema_matriculas,
                                         font=("Arial", 12),
                                         bg="blue", fg="white")
            botao_matriculas.pack(pady=10)

"""
PROJETO ESCOLA - SISTEMA DE GESTÃƒO ESCOLAR
VersÃ£o Desktop PyQt5 - Aprimorada com melhorias visuais e organizaÃ§Ã£o
Autoria Original: Alessandro Matheusti
Data: 2024
"""

import sys
import os
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import calendar
import hashlib
import json
import csv
import tempfile
import webbrowser
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Any

# PyQt5 imports - organizados por mÃ³dulo
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, 
    QLineEdit, QTextEdit, QComboBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QStackedWidget, QMessageBox, QInputDialog, QFileDialog,
    QProgressBar, QGroupBox, QFrame, QTabWidget, QDateEdit,
    QCheckBox, QRadioButton, QButtonGroup, QSpinBox,
    QDoubleSpinBox, QSlider, QProgressDialog, QDialog,
    QFormLayout, QListWidget, QListWidgetItem, QTreeWidget,
    QTreeWidgetItem, QSplitter, QToolBar, QStatusBar,
    QMenuBar, QMenu, QAction, QStyleFactory, QDialogButtonBox,
    QScrollArea, QSizePolicy, QSpacerItem,
    QStyle
    QGraphicsDropShadowEffect,
    QStyle,
)

from PyQt5.QtCore import (
    Qt, QTimer, QDate, QTime, QDateTime, QSize,
    QPropertyAnimation, QEasingCurve, pyqtProperty, pyqtSignal,
    QRect, QPoint, QThread, pyqtSlot, QSettings, QRegExp,
    QItemSelectionModel
)

from PyQt5.QtGui import (
    QFont, QIcon, QPixmap, QColor, QPalette, QBrush,
    QLinearGradient, QRadialGradient, QConicalGradient,
    QPainter, QPen, QFontMetrics, QIntValidator,
    QDoubleValidator, QRegExpValidator, QKeySequence,
    QImage, QTransform, QMovie, QTextCursor, QTextCharFormat,
    QTextTableFormat, QTextLength, QDesktopServices
)

# ConfiguraÃ§Ãµes iniciais
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

# ============================================
# STYLESHEET GLOBAL MODERNO E PROFISSIONAL
# ============================================
GLOBAL_STYLESHEET = """
/* ===== ESTILOS GERAIS ===== */
QMainWindow {
    background-color: #f5f7fa;
    font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
}

QWidget {
    font-size: 13px;
    color: #333333;
}

/* ===== BOTÃ•ES PRIMÃRIOS ===== */
QPushButton {
    background-color: #2c3e50;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 13px;
    min-height: 36px;
    transition: all 0.2s ease;
}

QPushButton:hover {
    background-color: #34495e;
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

QPushButton:pressed {
    background-color: #1a252f;
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

QPushButton:disabled {
    background-color: #bdc3c7;
    color: #7f8c8d;
}

/* ===== BOTÃ•ES SECUNDÃRIOS (Azul original) ===== */
QPushButton[class="secondary"] {
    background-color: #3498db;
}

QPushButton[class="secondary"]:hover {
    background-color: #2980b9;
}

QPushButton[class="secondary"]:pressed {
    background-color: #1c6ea4;
}

/* ===== BOTÃ•ES DE SUCESSO (Verde original) ===== */
QPushButton[class="success"] {
    background-color: #27ae60;
}

QPushButton[class="success"]:hover {
    background-color: #219653;
}

QPushButton[class="success"]:pressed {
    background-color: #1e874b;
}

/* ===== BOTÃ•ES DE PERIGO (Vermelho original) ===== */
QPushButton[class="danger"] {
    background-color: #e74c3c;
}

QPushButton[class="danger"]:hover {
    background-color: #c0392b;
}

QPushButton[class="danger"]:pressed {
    background-color: #a93226;
}

/* ===== BOTÃ•ES DE AVISO (Laranja original) ===== */
QPushButton[class="warning"] {
    background-color: #f39c12;
}

QPushButton[class="warning"]:hover {
    background-color: #d68910;
}

QPushButton[class="warning"]:pressed {
    background-color: #b9770e;
}

/* ===== CAMPOS DE ENTRADA ===== */
QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {
    background-color: white;
    border: 2px solid #dce1e6;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 13px;
    selection-background-color: #3498db;
    selection-color: white;
    transition: border-color 0.2s ease;
}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus, 
QSpinBox:focus, QDoubleSpinBox:focus, QDateEdit:focus {
    border-color: #3498db;
    box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

QLineEdit:hover, QTextEdit:hover, QComboBox:hover,
QSpinBox:hover, QDoubleSpinBox:hover, QDateEdit:hover {
    border-color: #a0c5e8;
}

/* ===== TABELAS ===== */
QTableWidget {
    background-color: white;
    border: 1px solid #dce1e6;
    border-radius: 6px;
    gridline-color: #ecf0f1;
    alternate-background-color: #f8f9fa;
    selection-background-color: #e3f2fd;
    selection-color: #2c3e50;
}

QTableWidget::item {
    padding: 8px;
    border-bottom: 1px solid #ecf0f1;
}

QTableWidget::item:selected {
    background-color: #e3f2fd;
    color: #2c3e50;
}

QHeaderView::section {
    background-color: #2c3e50;
    color: white;
    padding: 12px 8px;
    border: none;
    font-weight: 600;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

QHeaderView::section:hover {
    background-color: #34495e;
}

/* ===== ABAS ===== */
QTabWidget::pane {
    border: 1px solid #dce1e6;
    border-radius: 6px;
    background-color: white;
    margin-top: 2px;
}

QTabBar::tab {
    background-color: #ecf0f1;
    color: #7f8c8d;
    padding: 12px 24px;
    margin-right: 4px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    font-weight: 600;
    transition: all 0.2s ease;
}

QTabBar::tab:hover {
    background-color: #d5dbdb;
    color: #2c3e50;
}

QTabBar::tab:selected {
    background-color: #2c3e50;
    color: white;
    border-bottom: 3px solid #3498db;
}

/* ===== GRUPOS ===== */
QGroupBox {
    font-weight: 600;
    font-size: 14px;
    color: #2c3e50;
    border: 2px solid #dce1e6;
    border-radius: 8px;
    margin-top: 20px;
    padding-top: 15px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 15px;
    padding: 0 10px;
    background-color: #f5f7fa;
}

/* ===== BARRAS DE PROGRESSO ===== */
QProgressBar {
    border: 2px solid #dce1e6;
    border-radius: 6px;
    background-color: white;
    text-align: center;
    color: #2c3e50;
    font-weight: 600;
}

QProgressBar::chunk {
    background-color: #3498db;
    border-radius: 4px;
    transition: width 0.3s ease;
}

QProgressBar::chunk:hover {
    background-color: #2980b9;
}

/* ===== CHECKBOXES E RADIO BUTTONS ===== */
QCheckBox, QRadioButton {
    spacing: 8px;
    font-size: 13px;
    color: #333333;
}

QCheckBox::indicator, QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #dce1e6;
    border-radius: 4px;
    background-color: white;
}

QCheckBox::indicator:checked, QRadioButton::indicator:checked {
    background-color: #3498db;
    border-color: #3498db;
}

QCheckBox::indicator:checked:hover, QRadioButton::indicator:checked:hover {
    background-color: #2980b9;
    border-color: #2980b9;
}

/* ===== SCROLLBARS ===== */
QScrollBar:vertical, QScrollBar:horizontal {
    border: none;
    background-color: #ecf0f1;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
    background-color: #bdc3c7;
    border-radius: 6px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {
    background-color: #95a5a6;
}

QScrollBar::add-line, QScrollBar::sub-line {
    border: none;
    background: none;
}

/* ===== MENUS ===== */
QMenuBar {
    background-color: #2c3e50;
    color: white;
    padding: 6px;
    font-weight: 600;
}

QMenuBar::item {
    padding: 8px 16px;
    background-color: transparent;
    border-radius: 4px;
}

QMenuBar::item:selected {
    background-color: #34495e;
}

QMenu {
    background-color: white;
    border: 1px solid #dce1e6;
    border-radius: 6px;
    padding: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

QMenu::item {
    padding: 10px 24px;
    border-radius: 4px;
    margin: 2px 0;
}

QMenu::item:selected {
    background-color: #e3f2fd;
    color: #2c3e50;
}

/* ===== STATUS BAR ===== */
QStatusBar {
    background-color: #2c3e50;
    color: white;
    font-size: 12px;
    padding: 6px 12px;
}

/* ===== SEPARADORES ===== */
QFrame[frameShape="4"] { /* HLine */
    background-color: #dce1e6;
    max-height: 2px;
    min-height: 2px;
    border: none;
}

QFrame[frameShape="5"] { /* VLine */
    background-color: #dce1e6;
    max-width: 2px;
    min-width: 2px;
    border: none;
}

/* ===== BADGES E LABELS ESPECIAIS ===== */
QLabel[class="title"] {
    font-size: 24px;
    font-weight: 700;
    color: #2c3e50;
    padding: 10px 0;
}

QLabel[class="subtitle"] {
    font-size: 18px;
    font-weight: 600;
    color: #34495e;
    padding: 8px 0;
}

QLabel[class="success-badge"] {
    background-color: #d5f4e6;
    color: #27ae60;
    border-radius: 12px;
    padding: 4px 12px;
    font-weight: 600;
    font-size: 12px;
}

QLabel[class="warning-badge"] {
    background-color: #fef5e7;
    color: #f39c12;
    border-radius: 12px;
    padding: 4px 12px;
    font-weight: 600;
    font-size: 12px;
}

QLabel[class="danger-badge"] {
    background-color: #fdeaea;
    color: #e74c3c;
    border-radius: 12px;
    padding: 4px 12px;
    font-weight: 600;
    font-size: 12px;
}

QLabel[class="info-badge"] {
    background-color: #e3f2fd;
    color: #3498db;
    border-radius: 12px;
    padding: 4px 12px;
    font-weight: 600;
    font-size: 12px;
}
"""


# ============================================
# CLASSES AUXILIARES E UTILITÃRIAS
# ============================================

class DatabaseManager:
    """Gerenciador de banco de dados SQLite com mÃ©todos aprimorados"""

    def __init__(self, db_path="escola.db"):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self.init_database()

    def connect(self):
        """Estabelece conexÃ£o com o banco de dados"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            self.connection.execute("PRAGMA foreign_keys = ON")
            return True
        except sqlite3.Error as e:
            QMessageBox.critical(None, "Erro de Banco de Dados",
                                 f"Falha ao conectar ao banco de dados:\nfrom PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton,
    QLineEdit, QTextEdit, QComboBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QVBoxLayout, QHBoxLayout, QGridLayout,
    QStackedWidget, QMessageBox, QInputDialog, QFileDialog,
    QProgressBar, QGroupBox, QFrame, QTabWidget, QDateEdit,
    QCheckBox, QRadioButton, QButtonGroup, QSpinBox,
    QDoubleSpinBox, QSlider, QProgressDialog, QDialog,
    QFormLayout, QListWidget, QListWidgetItem, QTreeWidget,
    QTreeWidgetItem, QSplitter, QToolBar, QStatusBar,
    QMenuBar, QMenu, QAction, QStyleFactory, QDialogButtonBox,
    QScrollArea, QSizePolicy, QSpacerItem,
    QGraphicsDropShadowEffect,
    QStyle
)\n{str(e)}")
            return False

    def disconnect(self):
        """Fecha a conexÃ£o com o banco de dados"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def init_database(self):
        """Inicializa o banco de dados com todas as tabelas necessÃ¡rias"""
        if not self.connect():
            return False

        try:
            # Tabela de administradores
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS administradores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT UNIQUE NOT NULL,
                    senha TEXT NOT NULL,
                    nome TEXT NOT NULL,
                    email TEXT,
                    telefone TEXT,
                    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ultimo_login TIMESTAMP,
                    ativo INTEGER DEFAULT 1
                )
            ''')

            # Tabela de professores
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS professores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cpf TEXT UNIQUE,
                    telefone TEXT,
                    email TEXT,
                    materia TEXT,
                    formacao TEXT,
                    data_contratacao DATE,
                    salario REAL,
                    endereco TEXT,
                    observacoes TEXT,
                    ativo INTEGER DEFAULT 1,
                    usuario TEXT UNIQUE,
                    senha TEXT,
                    foto BLOB,
                    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Tabela de alunos
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS alunos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    data_nascimento DATE,
                    cpf TEXT UNIQUE,
                    rg TEXT,
                    nome_mae TEXT,
                    nome_pai TEXT,
                    telefone_responsavel TEXT,
                    email TEXT,
                    endereco TEXT,
                    bairro TEXT,
                    cidade TEXT,
                    cep TEXT,
                    serie TEXT,
                    turma TEXT,
                    turno TEXT,
                    data_matricula DATE,
                    status TEXT DEFAULT 'Ativo',
                    observacoes TEXT,
                    foto BLOB,
                    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Tabela de disciplinas
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS disciplinas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    codigo TEXT UNIQUE,
                    carga_horaria INTEGER,
                    serie TEXT,
                    professor_id INTEGER,
                    descricao TEXT,
                    ativa INTEGER DEFAULT 1,
                    FOREIGN KEY (professor_id) REFERENCES professores(id)
                )
            ''')

            # Tabela de notas
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS notas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    aluno_id INTEGER NOT NULL,
                    disciplina_id INTEGER NOT NULL,
                    bimestre INTEGER,
                    nota1 REAL,
                    nota2 REAL,
                    nota3 REAL,
                    nota4 REAL,
                    media REAL,
                    faltas INTEGER,
                    situacao TEXT,
                    observacoes TEXT,
                    data_lancamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    professor_id INTEGER,
                    FOREIGN KEY (aluno_id) REFERENCES alunos(id),
                    FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id),
                    FOREIGN KEY (professor_id) REFERENCES professores(id)
                )
            ''')

            # Tabela de frequÃªncia
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS frequencia (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    aluno_id INTEGER NOT NULL,
                    data DATE NOT NULL,
                    presente INTEGER DEFAULT 1,
                    disciplina_id INTEGER,
                    observacoes TEXT,
                    professor_id INTEGER,
                    FOREIGN KEY (aluno_id) REFERENCES alunos(id),
                    FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id),
                    FOREIGN KEY (professor_id) REFERENCES professores(id)
                )
            ''')

            # Tabela de turmas
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS turmas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    serie TEXT,
                    turno TEXT,
                    sala TEXT,
                    capacidade INTEGER,
                    professor_responsavel_id INTEGER,
                    ano_letivo INTEGER,
                    ativa INTEGER DEFAULT 1,
                    FOREIGN KEY (professor_responsavel_id) REFERENCES professores(id)
                )
            ''')

            # Tabela de horÃ¡rios
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS horarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    turma_id INTEGER NOT NULL,
                    disciplina_id INTEGER NOT NULL,
                    professor_id INTEGER NOT NULL,
                    dia_semana TEXT,
                    hora_inicio TIME,
                    hora_fim TIME,
                    sala TEXT,
                    ativo INTEGER DEFAULT 1,
                    FOREIGN KEY (turma_id) REFERENCES turmas(id),
                    FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id),
                    FOREIGN KEY (professor_id) REFERENCES professores(id)
                )
            ''')

            # Tabela de eventos
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS eventos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    descricao TEXT,
                    data_inicio DATE,
                    data_fim DATE,
                    tipo TEXT,
                    local TEXT,
                    responsavel TEXT,
                    ativo INTEGER DEFAULT 1,
                    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Tabela de comunicados
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS comunicados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    mensagem TEXT,
                    destinatarios TEXT,
                    data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    prioridade TEXT,
                    lido INTEGER DEFAULT 0,
                    ativo INTEGER DEFAULT 1
                )
            ''')

            # Tabela de configuraÃ§Ãµes
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS configuracoes (
                    chave TEXT PRIMARY KEY,
                    valor TEXT,
                    descricao TEXT,
                    tipo TEXT,
                    categoria TEXT,
                    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Tabela de backups
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS backups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_arquivo TEXT,
                    caminho TEXT,
                    tamanho INTEGER,
                    data_backup TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    tipo TEXT,
                    observacoes TEXT
                )
            ''')

            # Inserir administrador padrÃ£o se nÃ£o existir
            self.cursor.execute("SELECT COUNT(*) FROM administradores WHERE usuario = 'admin'")
            if self.cursor.fetchone()[0] == 0:
                senha_hash = hashlib.sha256("admin123".encode()).hexdigest()
                self.cursor.execute('''
                    INSERT INTO administradores (usuario, senha, nome, email, ativo)
                    VALUES (?, ?, ?, ?, ?)
                ''', ('admin', senha_hash, 'Administrador Principal', 'admin@escola.com', 1))

            # Inserir configuraÃ§Ãµes padrÃ£o
            configuracoes_padrao = [
                ('nome_escola', 'Escola Objetivo', 'Nome da instituiÃ§Ã£o', 'texto', 'geral'),
                ('ano_letivo', str(date.today().year), 'Ano letivo atual', 'numero', 'geral'),
                ('quantidade_bimestres', '4', 'Quantidade de bimestres', 'numero', 'notas'),
                ('media_aprovacao', '7.0', 'MÃ©dia para aprovaÃ§Ã£o', 'decimal', 'notas'),
                ('media_recuperacao', '5.0', 'MÃ©dia para recuperaÃ§Ã£o', 'decimal', 'notas'),
                ('max_faltas', '25', 'MÃ¡ximo de faltas permitidas', 'numero', 'frequencia'),
                ('hora_inicio_aula', '07:00', 'Hora de inÃ­cio das aulas', 'texto', 'horarios'),
                ('hora_fim_aula', '12:00', 'Hora de tÃ©rmino das aulas', 'texto', 'horarios'),
                ('turnos', 'Matutino,Vespertino,Noturno', 'Turnos disponÃ­veis', 'texto', 'turmas'),
                ('series', '1Âº Ano,2Âº Ano,3Âº Ano,4Âº Ano,5Âº Ano,6Âº Ano,7Âº Ano,8Âº Ano,9Âº Ano,1Âº EM,2Âº EM,3Âº EM',
                 'SÃ©ries disponÃ­veis', 'texto', 'turmas')
            ]

            for chave, valor, descricao, tipo, categoria in configuracoes_padrao:
                self.cursor.execute('''
                    INSERT OR IGNORE INTO configuracoes (chave, valor, descricao, tipo, categoria)
                    VALUES (?, ?, ?, ?, ?)
                ''', (chave, valor, descricao, tipo, categoria))

            self.connection.commit()
            print("Banco de dados inicializado com sucesso!")
            return True

        except sqlite3.Error as e:
            QMessageBox.critical(None, "Erro de Banco de Dados",
                                 f"Falha ao inicializar banco de dados:\n{str(e)}")
            return False
        finally:
            self.disconnect()

    def execute_query(self, query, params=(), fetch=False):
        """Executa uma query SQL com tratamento de erro aprimorado"""
        try:
            if not self.connect():
                return None

            self.cursor.execute(query, params)

            if fetch:
                if 'SELECT' in query.upper() or 'PRAGMA' in query.upper():
                    result = self.cursor.fetchall()
                else:
                    result = self.cursor.lastrowid
            else:
                self.connection.commit()
                result = True

            return result

        except sqlite3.Error as e:
            self.connection.rollback()
            print(f"Erro na query: {query}")
            print(f"ParÃ¢metros: {params}")
            print(f"Erro SQLite: {e}")
            return None
        finally:
            self.disconnect()

    def get_config(self, chave, default=None):
        """ObtÃ©m uma configuraÃ§Ã£o do banco de dados"""
        result = self.execute_query(
            "SELECT valor FROM configuracoes WHERE chave = ?",
            (chave,),
            fetch=True
        )

        if result and len(result) > 0:
            return result[0][0]
        return default

    def set_config(self, chave, valor, descricao="", tipo="texto", categoria="geral"):
        """Define uma configuraÃ§Ã£o no banco de dados"""
        return self.execute_query('''
            INSERT OR REPLACE INTO configuracoes (chave, valor, descricao, tipo, categoria)
            VALUES (?, ?, ?, ?, ?)
        ''', (chave, valor, descricao, tipo, categoria))

    def backup_database(self, backup_path=None):
        """Realiza backup do banco de dados"""
        try:
            if backup_path is None:
                backup_dir = os.path.join(os.path.expanduser("~"), "BackupsEscola")
                os.makedirs(backup_dir, exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = os.path.join(backup_dir, f"backup_escola_{timestamp}.db")

            # Conectar ao banco de dados original
            source_conn = sqlite3.connect(self.db_path)
            source_cursor = source_conn.cursor()

            # Conectar ao banco de dados de backup
            backup_conn = sqlite3.connect(backup_path)

            # Fazer o backup
            source_conn.backup(backup_conn)

            # Fechar conexÃµes
            source_cursor.close()
            source_conn.close()
            backup_conn.close()

            # Registrar o backup
            tamanho = os.path.getsize(backup_path)
            self.execute_query('''
                INSERT INTO backups (nome_arquivo, caminho, tamanho, tipo, observacoes)
                VALUES (?, ?, ?, ?, ?)
            ''', (os.path.basename(backup_path), backup_path, tamanho, 'completo', 'Backup automÃ¡tico'))

            return backup_path

        except Exception as e:
            QMessageBox.critical(None, "Erro no Backup",
                                 f"Falha ao realizar backup:\n{str(e)}")
            return None


class AnimacaoBotao(QPushButton):
    """Classe para botÃµes com animaÃ§Ãµes suaves"""

    def __init__(self, text="", parent=None, cor_normal="#2c3e50", cor_hover="#34495e", cor_press="#1a252f"):
        super().__init__(text, parent)

        self.cor_normal = cor_normal
        self.cor_hover = cor_hover
        self.cor_press = cor_press

        # Configurar estilos dinÃ¢micos
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.cor_normal};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: 600;
                font-size: 13px;
                min-height: 36px;
            }}
            QPushButton:hover {{
                background-color: {self.cor_hover};
            }}
            QPushButton:pressed {{
                background-color: {self.cor_press};
            }}
        """)

        # Configurar efeitos de sombra
        self.setGraphicsEffect(self.create_shadow_effect())

    def create_shadow_effect(self):
        """Cria efeito de sombra para o botÃ£o"""
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 40))
        return shadow

    def enterEvent(self, event):
        """AnimaÃ§Ã£o ao entrar no botÃ£o"""
        self.animacao = QPropertyAnimation(self, b"geometry")
        self.animacao.setDuration(150)
        self.animacao.setStartValue(self.geometry())
        self.animacao.setEndValue(QRect(
            self.x(), self.y() - 1,
            self.width(), self.height()
        ))
        self.animacao.setEasingCurve(QEasingCurve.OutCubic)
        self.animacao.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """AnimaÃ§Ã£o ao sair do botÃ£o"""
        self.animacao = QPropertyAnimation(self, b"geometry")
        self.animacao.setDuration(150)
        self.animacao.setStartValue(self.geometry())
        self.animacao.setEndValue(QRect(
            self.x(), self.y() + 1,
            self.width(), self.height()
        ))
        self.animacao.setEasingCurve(QEasingCurve.OutCubic)
        self.animacao.start()
        super().leaveEvent(event)


class CardWidget(QFrame):
    """Widget de card moderno para exibiÃ§Ã£o de informaÃ§Ãµes"""

    def __init__(self, titulo="", parent=None, cor_borda="#dce1e6", cor_fundo="#ffffff"):
        super().__init__(parent)

        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setLineWidth(1)

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # TÃ­tulo do card
        if titulo:
            self.lbl_titulo = QLabel(titulo)
            self.lbl_titulo.setObjectName("card_titulo")
            self.lbl_titulo.setStyleSheet("""
                QLabel#card_titulo {
                    font-size: 16px;
                    font-weight: 700;
                    color: #2c3e50;
                    padding-bottom: 8px;
                    border-bottom: 2px solid #3498db;
                }
            """)
            layout.addWidget(self.lbl_titulo)

        # Ãrea de conteÃºdo (serÃ¡ preenchida pelas subclasses)
        self.conteudo_widget = QWidget()
        layout.addWidget(self.conteudo_widget)

        # Aplicar estilo
        self.setStyleSheet(f"""
            CardWidget {{
                background-color: {cor_fundo};
                border: 2px solid {cor_borda};
                border-radius: 10px;
                padding: 0px;
            }}
            CardWidget:hover {{
                border-color: #3498db;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            }}
        """)


class LoadingOverlay(QWidget):
    """Overlay de carregamento com spinner animado"""

    def __init__(self, parent=None, mensagem="Carregando..."):
        super().__init__(parent)

        if parent:
            self.setGeometry(parent.rect())

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Layout central
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Container do spinner
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 12px;
                padding: 30px;
                border: 1px solid #dce1e6;
            }
        """)
        container.setFixedSize(200, 150)

        container_layout = QVBoxLayout(container)
        container_layout.setAlignment(Qt.AlignCenter)
        container_layout.setSpacing(20)

        # Spinner animado
        self.spinner = QLabel()
        self.spinner_movie = QMovie()

        # Criar spinner animado (usando caracteres ASCII se nÃ£o houver GIF)
        spinner_frames = ["â ‹", "â ™", "â ¹", "â ¸", "â ¼", "â ´", "â ¦", "â §", "â ‡", "â "]
        self.spinner_index = 0
        self.spinner_frames = spinner_frames

        self.spinner.setText(self.spinner_frames[0])
        self.spinner.setStyleSheet("""
            QLabel {
                font-size: 32px;
                color: #3498db;
                font-weight: bold;
            }
        """)
        self.spinner.setAlignment(Qt.AlignCenter)

        # Timer para animaÃ§Ã£o do spinner
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animar_spinner)
        self.timer.start(100)

        # Texto de carregamento
        self.lbl_mensagem = QLabel(mensagem)
        self.lbl_mensagem.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #2c3e50;
                font-weight: 600;
            }
        """)
        self.lbl_mensagem.setAlignment(Qt.AlignCenter)

        # Adicionar widgets ao container
        container_layout.addWidget(self.spinner)
        container_layout.addWidget(self.lbl_mensagem)

        # Adicionar container ao layout principal
        layout.addWidget(container)

    def animar_spinner(self):
        """Anima o spinner ASCII"""
        self.spinner_index = (self.spinner_index + 1) % len(self.spinner_frames)
        self.spinner.setText(self.spinner_frames[self.spinner_index])

    def showEvent(self, event):
        """Centraliza o overlay quando mostrado"""
        if self.parent():
            self.setGeometry(self.parent().rect())
        super().showEvent(event)

    def set_mensagem(self, mensagem):
        """Altera a mensagem de carregamento"""
        self.lbl_mensagem.setText(mensagem)


class ValidadorCampos:
    """Classe para validaÃ§Ã£o de campos de entrada"""

    @staticmethod
    def validar_cpf(cpf):
        """Valida CPF brasileiro"""
        cpf = ''.join(filter(str.isdigit, cpf))

        if len(cpf) != 11:
            return False

        if cpf in [s * 11 for s in [str(n) for n in range(10)]]:
            return False

        # CÃ¡lculo do primeiro dÃ­gito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto

        if digito1 != int(cpf[9]):
            return False

        # CÃ¡lculo do segundo dÃ­gito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto

        return digito2 == int(cpf[10])

    @staticmethod
    def validar_email(email):
        """Valida formato de email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validar_telefone(telefone):
        """Valida telefone brasileiro"""
        telefone = ''.join(filter(str.isdigit, telefone))
        return 10 <= len(telefone) <= 11

    @staticmethod
    def validar_data(data_str):
        """Valida data no formato DD/MM/YYYY"""
        try:
            datetime.strptime(data_str, '%d/%m/%Y')
            return True
        except ValueError:
            return False

    @staticmethod
    def formatar_cpf(cpf):
        """Formata CPF para o padrÃ£o XXX.XXX.XXX-XX"""
        cpf = ''.join(filter(str.isdigit, cpf))
        if len(cpf) == 11:
            return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
        return cpf

    @staticmethod
    def formatar_telefone(telefone):
        """Formata telefone para o padrÃ£o (XX) XXXXX-XXXX"""
        telefone = ''.join(filter(str.isdigit, telefone))
        if len(telefone) == 11:
            return f'({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}'
        elif len(telefone) == 10:
            return f'({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}'
        return telefone


class ExportadorDados:
    """Classe para exportaÃ§Ã£o de dados em diferentes formatos"""

    def __init__(self, db_manager):
        self.db = db_manager

    def exportar_para_excel(self, query, nome_arquivo, cabecalhos=None):
        """Exporta dados para arquivo Excel"""
        try:
            dados = self.db.execute_query(query, fetch=True)

            if not dados:
                return False, "Nenhum dado para exportar"

            df = pd.DataFrame(dados)

            if cabecalhos and len(cabecalhos) == len(df.columns):
                df.columns = cabecalhos

            # Criar diretÃ³rio de exportaÃ§Ã£o
            export_dir = os.path.join(os.path.expanduser("~"), "ExportacoesEscola")
            os.makedirs(export_dir, exist_ok=True)

            # Adicionar timestamp ao nome do arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            caminho_completo = os.path.join(export_dir, f"{nome_arquivo}_{timestamp}.xlsx")

            # Exportar para Excel
            with pd.ExcelWriter(caminho_completo, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Dados', index=False)

                # Ajustar largura das colunas
                worksheet = writer.sheets['Dados']
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width

            return True, caminho_completo

        except Exception as e:
            return False, f"Erro ao exportar para Excel: {str(e)}"

    def exportar_para_csv(self, query, nome_arquivo, delimitador=";"):
        """Exporta dados para arquivo CSV"""
        try:
            dados = self.db.execute_query(query, fetch=True)

            if not dados:
                return False, "Nenhum dado para exportar"

            # Criar diretÃ³rio de exportaÃ§Ã£o
            export_dir = os.path.join(os.path.expanduser("~"), "ExportacoesEscola")
            os.makedirs(export_dir, exist_ok=True)

            # Adicionar timestamp ao nome do arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            caminho_completo = os.path.join(export_dir, f"{nome_arquivo}_{timestamp}.csv")

            # Exportar para CSV
            with open(caminho_completo, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile, delimiter=delimitador)

                # Escrever cabeÃ§alhos
                if 'SELECT' in query.upper():
                    self.db.connect()
                    self.db.cursor.execute(query)
                    cabecalhos = [description[0] for description in self.db.cursor.description]
                    writer.writerow(cabecalhos)
                    self.db.disconnect()

                # Escrever dados
                for linha in dados:
                    writer.writerow(linha)

            return True, caminho_completo

        except Exception as e:
            return False, f"Erro ao exportar para CSV: {str(e)}"

    def exportar_para_pdf(self, titulo, dados, cabecalhos, nome_arquivo):
        """Exporta dados para arquivo PDF (simplificado)"""
        try:
            # Em um sistema real, usaria uma biblioteca como ReportLab
            # Aqui Ã© uma implementaÃ§Ã£o simplificada

            from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
            from PyQt5.QtWidgets import QTextDocument

            # Criar documento HTML
            html = f"""
            <html>
            <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th {{ background-color: #2c3e50; color: white; padding: 12px; text-align: left; }}
                td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                .footer {{ margin-top: 30px; color: #7f8c8d; font-size: 12px; text-align: center; }}
            </style>
            </head>
            <body>
                <h1>{titulo}</h1>
                <p>Exportado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
                <table>
                    <tr>
            """

            # Adicionar cabeÃ§alhos
            for cabecalho in cabecalhos:
                html += f"<th>{cabecalho}</th>"
            html += "</tr>"

            # Adicionar dados
            for linha in dados:
                html += "<tr>"
                for valor in linha:
                    html += f"<td>{valor}</td>"
                html += "</tr>"

            html += f"""
                </table>
                <div class="footer">
                    Sistema Escola Objetivo - ExportaÃ§Ã£o de Dados
                </div>
            </body>
            </html>
            """

            # Criar diretÃ³rio de exportaÃ§Ã£o
            export_dir = os.path.join(os.path.expanduser("~"), "ExportacoesEscola")
            os.makedirs(export_dir, exist_ok=True)

            # Adicionar timestamp ao nome do arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            caminho_completo = os.path.join(export_dir, f"{nome_arquivo}_{timestamp}.pdf")

            # Configurar impressora para PDF
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(caminho_completo)
            printer.setPageSize(QPrinter.A4)
            printer.setPageMargins(10, 10, 10, 10, QPrinter.Millimeter)

            # Criar e imprimir documento
            document = QTextDocument()
            document.setHtml(html)
            document.print_(printer)

            return True, caminho_completo

        except Exception as e:
            return False, f"Erro ao exportar para PDF: {str(e)}"


# ============================================
# JANELA PRINCIPAL DE LOGIN
# ============================================

class JanelaLogin(QMainWindow):
    """Janela de login aprimorada com design moderno"""

    login_sucesso = pyqtSignal(str, str)  # sinal para login bem-sucedido (usuario, tipo)

    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.init_ui()
        self.carregar_configuracoes()

    def init_ui(self):
        """Inicializa a interface grÃ¡fica da janela de login"""
        self.setWindowTitle("Escola Objetivo - Sistema de GestÃ£o")
        self.setFixedSize(1000, 600)

        # Centralizar janela
        self.center_window()

        # Aplicar estilo global
        self.setStyleSheet(GLOBAL_STYLESHEET)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal com gradiente de fundo
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Painel esquerdo (imagem/branding)
        left_panel = QWidget()
        left_panel.setObjectName("leftPanel")
        left_panel.setStyleSheet("""
            QWidget#leftPanel {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #2c3e50, 
                    stop: 1 #3498db
                );
                border-right: 2px solid #2980b9;
            }
        """)
        left_panel.setFixedWidth(400)

        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(40, 60, 40, 60)
        left_layout.setSpacing(30)
        left_layout.setAlignment(Qt.AlignCenter)

        # Logo/Ãcone
        lbl_logo = QLabel()
        lbl_logo.setPixmap(self.criar_logo())
        lbl_logo.setAlignment(Qt.AlignCenter)
        lbl_logo.setStyleSheet("""
            QLabel {
                padding: 20px;
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
        """)

        # TÃ­tulo do sistema
        lbl_titulo = QLabel("SISTEMA DE GESTÃƒO ESCOLAR")
        lbl_titulo.setObjectName("loginTitle")
        lbl_titulo.setStyleSheet("""
            QLabel#loginTitle {
                font-size: 28px;
                font-weight: 800;
                color: white;
                text-align: center;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
                letter-spacing: 1px;
            }
        """)
        lbl_titulo.setAlignment(Qt.AlignCenter)

        # SubtÃ­tulo
        lbl_subtitulo = QLabel("Escola Objetivo")
        lbl_subtitulo.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 600;
                color: rgba(255, 255, 255, 0.9);
                text-align: center;
                font-style: italic;
            }
        """)
        lbl_subtitulo.setAlignment(Qt.AlignCenter)

        # InformaÃ§Ãµes
        lbl_info = QLabel("Acesso seguro ao sistema de gestÃ£o acadÃªmica")
        lbl_info.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: rgba(255, 255, 255, 0.7);
                text-align: center;
                padding: 20px;
                background-color: rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        lbl_info.setAlignment(Qt.AlignCenter)
        lbl_info.setWordWrap(True)

        # Adicionar widgets ao painel esquerdo
        left_layout.addWidget(lbl_logo)
        left_layout.addWidget(lbl_titulo)
        left_layout.addWidget(lbl_subtitulo)
        left_layout.addSpacing(20)
        left_layout.addWidget(lbl_info)
        left_layout.addStretch()

        # Painel direito (formulÃ¡rio de login)
        right_panel = QWidget()
        right_panel.setObjectName("rightPanel")
        right_panel.setStyleSheet("""
            QWidget#rightPanel {
                background-color: #ffffff;
            }
        """)

        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(80, 80, 80, 80)
        right_layout.setSpacing(30)

        # TÃ­tulo do formulÃ¡rio
        lbl_login_titulo = QLabel("FAZER LOGIN")
        lbl_login_titulo.setObjectName("formTitle")
        lbl_login_titulo.setStyleSheet("""
            QLabel#formTitle {
                font-size: 24px;
                font-weight: 700;
                color: #2c3e50;
                text-align: center;
                padding-bottom: 10px;
                border-bottom: 3px solid #3498db;
            }
        """)
        lbl_login_titulo.setAlignment(Qt.AlignCenter)

        # Seletor de tipo de login
        self.combo_tipo_login = QComboBox()
        self.combo_tipo_login.addItems(["Administrador", "Professor"])
        self.combo_tipo_login.setStyleSheet("""
            QComboBox {
                padding: 12px;
                font-size: 14px;
                font-weight: 600;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 15px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 8px solid #2c3e50;
            }
        """)
        self.combo_tipo_login.currentIndexChanged.connect(self.atualizar_formulario_login)

        # FormulÃ¡rio de login
        form_layout = QVBoxLayout()
        form_layout.setSpacing(20)

        # Campo usuÃ¡rio
        lbl_usuario = QLabel("UsuÃ¡rio:")
        lbl_usuario.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 600;
                color: #2c3e50;
            }
        """)

        self.txt_usuario = QLineEdit()
        self.txt_usuario.setPlaceholderText("Digite seu nome de usuÃ¡rio")
        self.txt_usuario.setMinimumHeight(45)
        self.txt_usuario.setStyleSheet("""
            QLineEdit {
                padding-left: 15px;
                font-size: 14px;
            }
        """)

        # Campo senha
        lbl_senha = QLabel("Senha:")
        lbl_senha.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 600;
                color: #2c3e50;
            }
        """)

        self.txt_senha = QLineEdit()
        self.txt_senha.setPlaceholderText("Digite sua senha")
        self.txt_senha.setEchoMode(QLineEdit.Password)
        self.txt_senha.setMinimumHeight(45)
        self.txt_senha.setStyleSheet("""
            QLineEdit {
                padding-left: 15px;
                font-size: 14px;
            }
        """)

        # BotÃ£o para mostrar/ocultar senha
        self.btn_toggle_senha = QPushButton()
        self.btn_toggle_senha.setIcon(self.style().standardIcon(31))
        self.btn_toggle_senha.setFixedSize(30, 30)
        self.btn_toggle_senha.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgba(52, 152, 219, 0.1);
                border-radius: 4px;
            }
        """)
        self.btn_toggle_senha.clicked.connect(self.toggle_senha_visibilidade)

        # Layout para senha com botÃ£o
        senha_layout = QHBoxLayout()
        senha_layout.addWidget(self.txt_senha)
        senha_layout.addWidget(self.btn_toggle_senha)

        # Checkbox lembrar usuÃ¡rio
        self.check_lembrar = QCheckBox("Lembrar usuÃ¡rio")
        self.check_lembrar.setStyleSheet("""
            QCheckBox {
                font-size: 13px;
                color: #7f8c8d;
            }
        """)

        # BotÃµes
        botoes_layout = QHBoxLayout()
        botoes_layout.setSpacing(15)

        self.btn_login = AnimacaoBotao("ENTRAR", cor_normal="#3498db", cor_hover="#2980b9", cor_press="#1c6ea4")
        self.btn_login.setMinimumHeight(50)
        self.btn_login.setIcon(self.style().standardIcon(QStyle.SP_DialogOkButton))
        self.btn_login.clicked.connect(self.realizar_login)

        self.btn_sair = QPushButton("SAIR")
        self.btn_sair.setObjectName("danger")
        self.btn_sair.setMinimumHeight(50)
        self.btn_sair.setIcon(self.style().standardIcon(QStyle.SP_DialogCancelButton))
        self.btn_sair.clicked.connect(self.close)

        botoes_layout.addWidget(self.btn_login)
        botoes_layout.addWidget(self.btn_sair)

        # Adicionar widgets ao formulÃ¡rio
        form_layout.addWidget(lbl_usuario)
        form_layout.addWidget(self.txt_usuario)
        form_layout.addSpacing(10)
        form_layout.addWidget(lbl_senha)
        form_layout.addLayout(senha_layout)
        form_layout.addWidget(self.check_lembrar)
        form_layout.addSpacing(30)
        form_layout.addLayout(botoes_layout)

        # Links/recursos
        links_layout = QHBoxLayout()
        links_layout.setAlignment(Qt.AlignCenter)
        links_layout.setSpacing(20)

        btn_recuperar = QPushButton("Esqueci a senha")
        btn_recuperar.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #3498db;
                border: none;
                font-size: 12px;
                text-decoration: underline;
                padding: 5px;
            }
            QPushButton:hover {
                color: #2980b9;
                background-color: transparent;
            }
        """)
        btn_recuperar.clicked.connect(self.recuperar_senha)

        btn_ajuda = QPushButton("Ajuda")
        btn_ajuda.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #7f8c8d;
                border: none;
                font-size: 12px;
                padding: 5px;
            }
            QPushButton:hover {
                color: #2c3e50;
                background-color: transparent;
            }
        """)
        btn_ajuda.clicked.connect(self.mostrar_ajuda)

        links_layout.addWidget(btn_recuperar)
        links_layout.addWidget(QLabel("â€¢"))
        links_layout.addWidget(btn_ajuda)

        # VersÃ£o do sistema
        lbl_versao = QLabel(f"VersÃ£o 2.0.0 | {datetime.now().year}")
        lbl_versao.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #95a5a6;
                text-align: center;
            }
        """)
        lbl_versao.setAlignment(Qt.AlignCenter)

        # Adicionar tudo ao painel direito
        right_layout.addWidget(lbl_login_titulo)
        right_layout.addSpacing(10)
        right_layout.addWidget(self.combo_tipo_login)
        right_layout.addSpacing(20)
        right_layout.addLayout(form_layout)
        right_layout.addLayout(links_layout)
        right_layout.addStretch()
        right_layout.addWidget(lbl_versao)

        # Adicionar painÃ©is ao layout principal
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)

        # Carregar usuÃ¡rio lembrado
        self.carregar_usuario_lembrado()

        # Conectar tecla Enter ao botÃ£o de login
        self.txt_senha.returnPressed.connect(self.realizar_login)

    def criar_logo(self):
        """Cria um logo grÃ¡fico para o sistema"""
        from PyQt5.QtGui import QPainter, QLinearGradient, QBrush

        pixmap = QPixmap(200, 200)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Gradiente de fundo do logo
        gradient = QLinearGradient(0, 0, 200, 200)
        gradient.setColorAt(0, QColor(52, 152, 219))
        gradient.setColorAt(1, QColor(41, 128, 185))

        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)

        # Desenhar cÃ­rculo principal
        painter.drawEllipse(20, 20, 160, 160)

        # Desenhar sÃ­mbolo de educaÃ§Ã£o (livro)
        painter.setPen(QPen(Qt.white, 8))
        painter.setBrush(Qt.NoBrush)

        # Livro aberto
        painter.drawArc(60, 70, 40, 60, 30 * 16, 120 * 16)
        painter.drawArc(100, 70, 40, 60, 30 * 16, 120 * 16)

        # Linha central do livro
        painter.drawLine(100, 100, 100, 130)

        painter.end()

        return pixmap

    def center_window(self):
        """Centraliza a janela na tela"""
        screen = QApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        center_point = screen.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

    def carregar_configuracoes(self):
        """Carrega configuraÃ§Ãµes do sistema"""
        self.nome_escola = self.db.get_config('nome_escola', 'Escola Objetivo')
        self.setWindowTitle(f"{self.nome_escola} - Sistema de GestÃ£o")

    def carregar_usuario_lembrado(self):
        """Carrega usuÃ¡rio lembrado das configuraÃ§Ãµes"""
        settings = QSettings("EscolaObjetivo", "SistemaGestao")
        usuario_salvo = settings.value("ultimo_usuario", "")

        if usuario_salvo:
            self.txt_usuario.setText(usuario_salvo)
            self.check_lembrar.setChecked(True)
            self.txt_senha.setFocus()

    def atualizar_formulario_login(self, index):
        """Atualiza o formulÃ¡rio de login baseado no tipo selecionado"""
        tipo = self.combo_tipo_login.currentText()

        if tipo == "Administrador":
            self.txt_usuario.setPlaceholderText("Digite seu nome de administrador")
        else:  # Professor
            self.txt_usuario.setPlaceholderText("Digite seu CPF ou usuÃ¡rio")

    def toggle_senha_visibilidade(self):
        """Alterna a visibilidade da senha"""
        if self.txt_senha.echoMode() == QLineEdit.Password:
            self.txt_senha.setEchoMode(QLineEdit.Normal)
            self.btn_toggle_senha.setIcon(self.style().standardIcon(getattr(QStyle, 'SP_FileDialogInfoView')))
        else:
            self.txt_senha.setEchoMode(QLineEdit.Password)
            self.btn_toggle_senha.setIcon(self.style().standardIcon(31))

    def realizar_login(self):
        """Realiza o processo de login"""
        usuario = self.txt_usuario.text().strip()
        senha = self.txt_senha.text().strip()
        tipo = self.combo_tipo_login.currentText()

        # ValidaÃ§Ãµes bÃ¡sicas
        if not usuario:
            self.mostrar_erro("Campo obrigatÃ³rio", "Por favor, informe o usuÃ¡rio.")
            self.txt_usuario.setFocus()
            return

        if not senha:
            self.mostrar_erro("Campo obrigatÃ³rio", "Por favor, informe a senha.")
            self.txt_senha.setFocus()
            return

        # Criar overlay de carregamento
        overlay = LoadingOverlay(self, "Verificando credenciais...")
        overlay.show()
        QApplication.processEvents()

        try:
            if tipo == "Administrador":
                autenticado, dados = self.verificar_login_administrador(usuario, senha)
            else:  # Professor
                autenticado, dados = self.verificar_login_professor(usuario, senha)

            overlay.close()

            if autenticado:
                # Salvar usuÃ¡rio se marcado para lembrar
                if self.check_lembrar.isChecked():
                    settings = QSettings("EscolaObjetivo", "SistemaGestao")
                    settings.setValue("ultimo_usuario", usuario)

                # Atualizar Ãºltimo login no banco
                self.atualizar_ultimo_login(tipo, dados['id'])

                # Emitir sinal de sucesso
                self.login_sucesso.emit(tipo, json.dumps(dados))
                self.close()
            else:
                self.mostrar_erro("Login invÃ¡lido", "UsuÃ¡rio ou senha incorretos.")
                self.txt_senha.selectAll()
                self.txt_senha.setFocus()

        except Exception as e:
            overlay.close()
            self.mostrar_erro("Erro no login", f"Ocorreu um erro durante o login:\n{str(e)}")

    def verificar_login_administrador(self, usuario, senha):
        """Verifica credenciais de administrador"""
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()

        resultado = self.db.execute_query('''
            SELECT id, usuario, nome, email, ativo 
            FROM administradores 
            WHERE usuario = ? AND senha = ? AND ativo = 1
        ''', (usuario, senha_hash), fetch=True)

        if resultado and len(resultado) > 0:
            dados = {
                'id': resultado[0][0],
                'usuario': resultado[0][1],
                'nome': resultado[0][2],
                'email': resultado[0][3],
                'tipo': 'administrador'
            }
            return True, dados

        return False, None

    def verificar_login_professor(self, usuario, senha):
        """Verifica credenciais de professor"""
        # Tentar login por usuÃ¡rio/senha
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()

        resultado = self.db.execute_query('''
            SELECT id, nome, cpf, email, materia, usuario
            FROM professores 
            WHERE (usuario = ? OR cpf = ?) AND senha = ? AND ativo = 1
        ''', (usuario, usuario, senha_hash), fetch=True)

        if resultado and len(resultado) > 0:
            dados = {
                'id': resultado[0][0],
                'nome': resultado[0][1],
                'cpf': resultado[0][2],
                'email': resultado[0][3],
                'materia': resultado[0][4],
                'usuario': resultado[0][5],
                'tipo': 'professor'
            }
            return True, dados

        return False, None

    def atualizar_ultimo_login(self, tipo, id_usuario):
        """Atualiza o timestamp do Ãºltimo login"""
        data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if tipo == "Administrador":
            self.db.execute_query(
                "UPDATE administradores SET ultimo_login = ? WHERE id = ?",
                (data_atual, id_usuario)
            )
        else:  # Professor
            self.db.execute_query(
                "UPDATE professores SET ultimo_login = ? WHERE id = ?",
                (data_atual, id_usuario)
            )

    def recuperar_senha(self):
        """Abre diÃ¡logo para recuperaÃ§Ã£o de senha"""
        dialog = QDialog(self)
        dialog.setWindowTitle("RecuperaÃ§Ã£o de Senha")
        dialog.setFixedSize(500, 350)
        dialog.setStyleSheet(GLOBAL_STYLESHEET)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # TÃ­tulo
        lbl_titulo = QLabel("RECUPERAR SENHA")
        lbl_titulo.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: 700;
                color: #2c3e50;
                text-align: center;
                padding-bottom: 10px;
                border-bottom: 2px solid #3498db;
            }
        """)

        # InstruÃ§Ãµes
        lbl_instrucoes = QLabel(
            "Para recuperar sua senha, informe seu email cadastrado. "
            "Enviaremos um link para redefiniÃ§Ã£o."
        )
        lbl_instrucoes.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #7f8c8d;
                text-align: center;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 6px;
                border: 1px solid #ecf0f1;
            }
        """)
        lbl_instrucoes.setWordWrap(True)

        # Tipo de conta
        lbl_tipo = QLabel("Tipo de conta:")
        lbl_tipo.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 600;
                color: #2c3e50;
            }
        """)

        combo_tipo = QComboBox()
        combo_tipo.addItems(["Administrador", "Professor"])

        # Campo email
        lbl_email = QLabel("Email cadastrado:")
        lbl_email.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: 600;
                color: #2c3e50;
            }
        """)

        txt_email = QLineEdit()
        txt_email.setPlaceholderText("seu.email@escola.com")

        # BotÃµes
        botoes_layout = QHBoxLayout()
        btn_enviar = AnimacaoBotao("ENVIAR LINK", cor_normal="#3498db", cor_hover="#2980b9", cor_press="#1c6ea4")
        btn_cancelar = QPushButton("CANCELAR")
        btn_cancelar.setObjectName("danger")
        btn_cancelar.clicked.connect(dialog.reject)

        botoes_layout.addWidget(btn_enviar)
        botoes_layout.addWidget(btn_cancelar)

        # Adicionar widgets
        layout.addWidget(lbl_titulo)
        layout.addWidget(lbl_instrucoes)
        layout.addWidget(lbl_tipo)
        layout.addWidget(combo_tipo)
        layout.addWidget(lbl_email)
        layout.addWidget(txt_email)
        layout.addStretch()
        layout.addLayout(botoes_layout)

        # FunÃ§Ã£o de envio (simulada)
        def enviar_link():
            email = txt_email.text().strip()
            if not ValidadorCampos.validar_email(email):
                QMessageBox.warning(dialog, "Email invÃ¡lido",
                                    "Por favor, informe um email vÃ¡lido.")
                return

            # SimulaÃ§Ã£o de envio
            QMessageBox.information(dialog, "Link enviado",
                                    f"Um link de recuperaÃ§Ã£o foi enviado para {email}.\n"
                                    "Verifique sua caixa de entrada.")
            dialog.accept()

        btn_enviar.clicked.connect(enviar_link)

        dialog.exec_()

    def mostrar_ajuda(self):
        """Mostra diÃ¡logo de ajuda"""
        QMessageBox.information(self, "Ajuda - Login",
                                "Para acessar o sistema:\n\n"
                                "1. Selecione o tipo de conta (Administrador ou Professor)\n"
                                "2. Informe seu usuÃ¡rio e senha\n"
                                "3. Clique em ENTRAR\n\n"
                                "Contate o administrador do sistema se tiver dificuldades.")

    def mostrar_erro(self, titulo, mensagem):
        """Mostra mensagem de erro estilizada"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(titulo)
        msg_box.setText(mensagem)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QMessageBox QLabel {
                font-size: 13px;
                color: #2c3e50;
            }
            QMessageBox QPushButton {
                min-width: 80px;
                min-height: 35px;
                font-weight: 600;
            }
        """)
        msg_box.exec_()

    def closeEvent(self, event):
        """Evento ao fechar a janela"""
        resposta = QMessageBox.question(
            self, "Confirmar saÃ­da",
            "Deseja realmente sair do sistema?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


# ============================================
# JANELA PRINCIPAL DO SISTEMA
# ============================================

class JanelaPrincipal(QMainWindow):
    """Janela principal do sistema apÃ³s login"""

    def __init__(self, tipo_usuario, dados_usuario):
        super().__init__()
        self.tipo_usuario = tipo_usuario
        self.dados_usuario = dados_usuario
        self.db = DatabaseManager()
        self.paginas = {}
        self.init_ui()

    def init_ui(self):
        """Inicializa a interface grÃ¡fica da janela principal"""
        self.setWindowTitle(f"Escola Objetivo - Sistema de GestÃ£o")
        self.setGeometry(100, 100, 1400, 800)

        # Aplicar estilo global
        self.setStyleSheet(GLOBAL_STYLESHEET)

        # Configurar menu bar
        self.criar_menu_bar()

        # Configurar toolbar
        self.criar_toolbar()

        # Configurar status bar
        self.criar_status_bar()

        # Widget central com layout em pilha
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Criar pÃ¡ginas do sistema
        self.criar_pagina_inicial()
        self.criar_pagina_alunos()
        self.criar_pagina_professores()
        self.criar_pagina_disciplinas()
        self.criar_pagina_notas()
        self.criar_pagina_frequencia()
        self.criar_pagina_turmas()
        self.criar_pagina_relatorios()
        self.criar_pagina_configuracoes()

        # Mostrar pÃ¡gina inicial
        self.central_widget.setCurrentWidget(self.paginas['inicial'])

        # Carregar dados iniciais
        self.carregar_dados_iniciais()

    def criar_menu_bar(self):
        """Cria a barra de menus"""
        menu_bar = self.menuBar()

        # Menu Arquivo
        menu_arquivo = menu_bar.addMenu("&Arquivo")

        act_backup = QAction("&Backup do Sistema", self)
        act_backup.setShortcut("Ctrl+B")
        act_backup.triggered.connect(self.realizar_backup)
        menu_arquivo.addAction(act_backup)

        menu_arquivo.addSeparator()

        act_exportar = QAction("&Exportar Dados", self)
        act_exportar.triggered.connect(self.exportar_dados)
        menu_arquivo.addAction(act_exportar)

        act_importar = QAction("&Importar Dados", self)
        act_importar.triggered.connect(self.importar_dados)
        menu_arquivo.addAction(act_importar)

        menu_arquivo.addSeparator()

        act_sair = QAction("&Sair", self)
        act_sair.setShortcut("Ctrl+Q")
        act_sair.triggered.connect(self.close)
        menu_arquivo.addAction(act_sair)

        # Menu Cadastros
        menu_cadastros = menu_bar.addMenu("&Cadastros")

        act_alunos = QAction("&Alunos", self)
        act_alunos.setShortcut("Ctrl+A")
        act_alunos.triggered.connect(lambda: self.mostrar_pagina('alunos'))
        menu_cadastros.addAction(act_alunos)

        act_professores = QAction("&Professores", self)
        act_professores.setShortcut("Ctrl+P")
        act_professores.triggered.connect(lambda: self.mostrar_pagina('professores'))
        menu_cadastros.addAction(act_professores)

        act_disciplinas = QAction("&Disciplinas", self)
        act_disciplinas.triggered.connect(lambda: self.mostrar_pagina('disciplinas'))
        menu_cadastros.addAction(act_disciplinas)

        act_turmas = QAction("&Turmas", self)
        act_turmas.triggered.connect(lambda: self.mostrar_pagina('turmas'))
        menu_cadastros.addAction(act_turmas)

        # Menu AcadÃªmico
        menu_academico = menu_bar.addMenu("&AcadÃªmico")

        act_notas = QAction("&LanÃ§ar Notas", self)
        act_notas.setShortcut("Ctrl+N")
        act_notas.triggered.connect(lambda: self.mostrar_pagina('notas'))
        menu_academico.addAction(act_notas)

        act_frequencia = QAction("&Registrar FrequÃªncia", self)
        act_frequencia.setShortcut("Ctrl+F")
        act_frequencia.triggered.connect(lambda: self.mostrar_pagina('frequencia'))
        menu_academico.addAction(act_frequencia)

        act_boletim = QAction("&Gerar Boletim", self)
        act_boletim.triggered.connect(self.gerar_boletim)
        menu_academico.addAction(act_boletim)

        # Menu RelatÃ³rios
        menu_relatorios = menu_bar.addMenu("&RelatÃ³rios")

        act_rel_alunos = QAction("&RelatÃ³rio de Alunos", self)
        act_rel_alunos.triggered.connect(self.gerar_relatorio_alunos)
        menu_relatorios.addAction(act_rel_alunos)

        act_rel_notas = QAction("&RelatÃ³rio de Notas", self)
        act_rel_notas.triggered.connect(self.gerar_relatorio_notas)
        menu_relatorios.addAction(act_rel_notas)

        act_rel_frequencia = QAction("&RelatÃ³rio de FrequÃªncia", self)
        act_rel_frequencia.triggered.connect(self.gerar_relatorio_frequencia)
        menu_relatorios.addAction(act_rel_frequencia)

        menu_relatorios.addSeparator()

        act_rel_personalizado = QAction("&RelatÃ³rio Personalizado", self)
        act_rel_personalizado.triggered.connect(self.relatorio_personalizado)
        menu_relatorios.addAction(act_rel_personalizado)

        # Menu Sistema
        menu_sistema = menu_bar.addMenu("&Sistema")

        act_config = QAction("&ConfiguraÃ§Ãµes", self)
        act_config.triggered.connect(lambda: self.mostrar_pagina('configuracoes'))
        menu_sistema.addAction(act_config)

        act_usuarios = QAction("&UsuÃ¡rios", self)
        act_usuarios.triggered.connect(self.gerenciar_usuarios)
        menu_sistema.addAction(act_usuarios)

        menu_sistema.addSeparator()

        act_trocar_usuario = QAction("&Trocar UsuÃ¡rio", self)
        act_trocar_usuario.triggered.connect(self.trocar_usuario)
        menu_sistema.addAction(act_trocar_usuario)

        act_sobre = QAction("&Sobre", self)
        act_sobre.triggered.connect(self.mostrar_sobre)
        menu_sistema.addAction(act_sobre)

        # Aplicar estilo Ã  barra de menus
        menu_bar.setStyleSheet("""
            QMenuBar {
                background-color: #2c3e50;
                color: white;
                font-weight: 600;
                padding: 6px;
            }
            QMenuBar::item {
                padding: 8px 16px;
                background-color: transparent;
                border-radius: 4px;
            }
            QMenuBar::item:selected {
                background-color: #34495e;
            }
        """)

    def criar_toolbar(self):
        """Cria a barra de ferramentas"""
        toolbar = QToolBar("Barra de Ferramentas")
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)

        # BotÃµes da toolbar
        act_inicio = QAction(QIcon(), "InÃ­cio", self)
        act_inicio.triggered.connect(lambda: self.mostrar_pagina('inicial'))
        toolbar.addAction(act_inicio)

        toolbar.addSeparator()

        act_alunos = QAction(QIcon(), "Alunos", self)
        act_alunos.triggered.connect(lambda: self.mostrar_pagina('alunos'))
        toolbar.addAction(act_alunos)

        act_professores = QAction(QIcon(), "Professores", self)
        act_professores.triggered.connect(lambda: self.mostrar_pagina('professores'))
        toolbar.addAction(act_professores)

        act_notas = QAction(QIcon(), "Notas", self)
        act_notas.triggered.connect(lambda: self.mostrar_pagina('notas'))
        toolbar.addAction(act_notas)

        act_frequencia = QAction(QIcon(), "FrequÃªncia", self)
        act_frequencia.triggered.connect(lambda: self.mostrar_pagina('frequencia'))
        toolbar.addAction(act_frequencia)

        toolbar.addSeparator()

        act_relatorios = QAction(QIcon(), "RelatÃ³rios", self)
        act_relatorios.triggered.connect(lambda: self.mostrar_pagina('relatorios'))
        toolbar.addAction(act_relatorios)

        # Adicionar espaÃ§ador
        toolbar.addWidget(QWidget())

        # UsuÃ¡rio atual
        lbl_usuario = QLabel(f"UsuÃ¡rio: {self.dados_usuario.get('nome', '')}")
        lbl_usuario.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-weight: 600;
                padding: 4px 12px;
                background-color: #ecf0f1;
                border-radius: 4px;
                border: 1px solid #dce1e6;
            }
        """)
        toolbar.addWidget(lbl_usuario)

    def criar_status_bar(self):
        """Cria a barra de status"""
        status_bar = self.statusBar()

        # Status do banco de dados
        self.lbl_status_db = QLabel(" Banco de dados: Conectado")
        self.lbl_status_db.setStyleSheet("""
            QLabel {
                color: #27ae60;
                font-weight: 600;
                padding: 2px 8px;
                background-color: #d5f4e6;
                border-radius: 3px;
                border: 1px solid #a3e4c0;
            }
        """)
        status_bar.addPermanentWidget(self.lbl_status_db)

        # Data e hora atualizadas em tempo real
        self.lbl_data_hora = QLabel()
        self.lbl_data_hora.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-weight: 600;
                padding: 2px 8px;
            }
        """)
        status_bar.addPermanentWidget(self.lbl_data_hora)

        # Atualizar data/hora
        self.timer_data_hora = QTimer(self)
        self.timer_data_hora.timeout.connect(self.atualizar_data_hora)
        self.timer_data_hora.start(1000)  # Atualizar a cada segundo
        self.atualizar_data_hora()

    def atualizar_data_hora(self):
        """Atualiza a data e hora na status bar"""
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.lbl_data_hora.setText(f" {data_hora}")

    def criar_pagina_inicial(self):
        """Cria a pÃ¡gina inicial/dashboard"""
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # TÃ­tulo da pÃ¡gina
        lbl_titulo = QLabel("DASHBOARD - VISÃƒO GERAL")
        lbl_titulo.setObjectName("title")
        lbl_titulo.setStyleSheet("""
            QLabel#title {
                font-size: 24px;
                font-weight: 700;
                color: #2c3e50;
                padding-bottom: 10px;
                border-bottom: 3px solid #3498db;
            }
        """)

        # SubtÃ­tulo com saudaÃ§Ã£o
        saudacao = self.obter_saudacao()
        lbl_saudacao = QLabel(f"{saudacao}, {self.dados_usuario.get('nome', 'UsuÃ¡rio')}!")
        lbl_saudacao.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #7f8c8d;
                font-weight: 600;
            }
        """)

        # Grid de cards de estatÃ­sticas
        grid_cards = QGridLayout()
        grid_cards.setSpacing(20)

        # Card: Total de Alunos
        card_alunos = CardWidget("ALUNOS CADASTRADOS")
        layout_alunos = QVBoxLayout(card_alunos.conteudo_widget)
        self.lbl_total_alunos = QLabel("Carregando...")
        self.lbl_total_alunos.setStyleSheet("""
            QLabel {
                font-size: 36px;
                font-weight: 800;
                color: #3498db;
                text-align: center;
            }
        """)
        self.lbl_total_alunos.setAlignment(Qt.AlignCenter)

        lbl_info_alunos = QLabel("Alunos ativos no sistema")
        lbl_info_alunos.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #7f8c8d;
                text-align: center;
            }
        """)
        lbl_info_alunos.setAlignment(Qt.AlignCenter)

        layout_alunos.addWidget(self.lbl_total_alunos)
        layout_alunos.addWidget(lbl_info_alunos)

        # Card: Total de Professores
        card_professores = CardWidget("PROFESSORES")
        layout_professores = QVBoxLayout(card_professores.conteudo_widget)
        self.lbl_total_professores = QLabel("Carregando...")
        self.lbl_total_professores.setStyleSheet("""
            QLabel {
                font-size: 36px;
                font-weight: 800;
                color: #27ae60;
                text-align: center;
            }
        """)
        self.lbl_total_professores.setAlignment(Qt.AlignCenter)

        lbl_info_professores = QLabel("Professores ativos")
        lbl_info_professores.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #7f8c8d;
                text-align: center;
            }
        """)
        lbl_info_professores.setAlignment(Qt.AlignCenter)

        layout_professores.addWidget(self.lbl_total_professores)
        layout_professores.addWidget(lbl_info_professores)

        # Card: MÃ©dia Geral
        card_media = CardWidget("MÃ‰DIA GERAL")
        layout_media = QVBoxLayout(card_media.conteudo_widget)
        self.lbl_media_geral = QLabel("Carregando...")
        self.lbl_media_geral.setStyleSheet("""
            QLabel {
                font-size: 36px;
                font-weight: 800;
                color: #f39c12;
                text-align: center;
            }
        """)
        self.lbl_media_geral.setAlignment(Qt.AlignCenter)

        lbl_info_media = QLabel("MÃ©dia das notas")
        lbl_info_media.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #7f8c8d;
                text-align: center;
            }
        """)
        lbl_info_media.setAlignment(Qt.AlignCenter)

        layout_media.addWidget(self.lbl_media_geral)
        layout_media.addWidget(lbl_info_media)

        # Card: FrequÃªncia
        card_frequencia = CardWidget("FREQUÃŠNCIA")
        layout_frequencia = QVBoxLayout(card_frequencia.conteudo_widget)
        self.lbl_frequencia = QLabel("Carregando...")
        self.lbl_frequencia.setStyleSheet("""
            QLabel {
                font-size: 36px;
                font-weight: 800;
                color: #e74c3c;
                text-align: center;
            }
        """)
        self.lbl_frequencia.setAlignment(Qt.AlignCenter)

        lbl_info_frequencia = QLabel("PresenÃ§a mÃ©dia")
        lbl_info_frequencia.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #7f8c8d;
                text-align: center;
            }
        """)
        lbl_info_frequencia.setAlignment(Qt.AlignCenter)

        layout_frequencia.addWidget(self.lbl_frequencia)
        layout_frequencia.addWidget(lbl_info_frequencia)

        # Adicionar cards ao grid
        grid_cards.addWidget(card_alunos, 0, 0)
        grid_cards.addWidget(card_professores, 0, 1)
        grid_cards.addWidget(card_media, 1, 0)
        grid_cards.addWidget(card_frequencia, 1, 1)

        # AÃ§Ãµes rÃ¡pidas
        group_acoes = QGroupBox("AÃ‡Ã•ES RÃPIDAS")
        group_acoes.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: 700;
                color: #2c3e50;
                border: 2px solid #dce1e6;
                border-radius: 8px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 15px;
                padding: 0 10px;
                background-color: #f5f7fa;
            }
        """)

        layout_acoes = QHBoxLayout()
        layout_acoes.setSpacing(15)

        btn_cad_aluno = AnimacaoBotao("Cadastrar Aluno", cor_normal="#3498db", cor_hover="#2980b9", cor_press="#1c6ea4")
        btn_cad_aluno.clicked.connect(lambda: self.mostrar_pagina('alunos'))

        btn_lancar_nota = AnimacaoBotao("LanÃ§ar Nota", cor_normal="#27ae60", cor_hover="#219653", cor_press="#1e874b")
        btn_lancar_nota.clicked.connect(lambda: self.mostrar_pagina('notas'))

        btn_reg_frequencia = AnimacaoBotao("Registrar FrequÃªncia", cor_normal="#f39c12", cor_hover="#d68910",
                                           cor_press="#b9770e")
        btn_reg_frequencia.clicked.connect(lambda: self.mostrar_pagina('frequencia'))

        btn_ger_relatorio = AnimacaoBotao("Gerar RelatÃ³rio", cor_normal="#9b59b6", cor_hover="#8e44ad",
                                          cor_press="#7d3c98")
        btn_ger_relatorio.clicked.connect(lambda: self.mostrar_pagina('relatorios'))

        layout_acoes.addWidget(btn_cad_aluno)
        layout_acoes.addWidget(btn_lancar_nota)
        layout_acoes.addWidget(btn_reg_frequencia)
        layout_acoes.addWidget(btn_ger_relatorio)
        layout_acoes.addStretch()

        group_acoes.setLayout(layout_acoes)

        # Atividades recentes
        group_atividades = QGroupBox("ATIVIDADES RECENTES")
        group_atividades.setStyleSheet(group_acoes.styleSheet())

        layout_atividades = QVBoxLayout()
        self.list_atividades = QListWidget()
        self.list_atividades.setStyleSheet("""
            QListWidget {
                border: 1px solid #dce1e6;
                border-radius: 6px;
                background-color: white;
                padding: 5px;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #ecf0f1;
                font-size: 13px;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: #2c3e50;
            }
        """)
        layout_atividades.addWidget(self.list_atividades)
        group_atividades.setLayout(layout_atividades)

        # Adicionar tudo ao layout principal
        layout.addWidget(lbl_titulo)
        layout.addWidget(lbl_saudacao)
        layout.addLayout(grid_cards)
        layout.addWidget(group_acoes)
        layout.addWidget(group_atividades)

        self.paginas['inicial'] = pagina
        self.central_widget.addWidget(pagina)

    def criar_pagina_alunos(self):
        """Cria a pÃ¡gina de gerenciamento de alunos"""
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # CabeÃ§alho
        cabecalho_layout = QHBoxLayout()

        lbl_titulo = QLabel("GESTÃƒO DE ALUNOS")
        lbl_titulo.setObjectName("title")

        # Barra de busca
        self.txt_busca_aluno = QLineEdit()
        self.txt_busca_aluno.setPlaceholderText("Buscar aluno por nome, CPF ou turma...")
        self.txt_busca_aluno.setMinimumHeight(40)
        self.txt_busca_aluno.textChanged.connect(self.buscar_alunos)

        # BotÃµes de aÃ§Ã£o
        btn_novo = AnimacaoBotao("Novo Aluno", cor_normal="#27ae60", cor_hover="#219653", cor_press="#1e874b")
        btn_novo.setIcon(self.style().standardIcon(QStyle.SP_FileIcon))
        btn_novo.clicked.connect(self.cadastrar_aluno)

        btn_editar = AnimacaoBotao("Editar", cor_normal="#3498db", cor_hover="#2980b9", cor_press="#1c6ea4")
        btn_editar.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        btn_editar.clicked.connect(self.editar_aluno)

        btn_excluir = AnimacaoBotao("Excluir", cor_normal="#e74c3c", cor_hover="#c0392b", cor_press="#a93226")
        btn_excluir.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        btn_excluir.clicked.connect(self.excluir_aluno)

        btn_imprimir = AnimacaoBotao("Imprimir", cor_normal="#f39c12", cor_hover="#d68910", cor_press="#b9770e")
        btn_imprimir.setIcon(self.style().standardIcon(QStyle.SP_FileDialogListView))
        btn_imprimir.clicked.connect(self.imprimir_lista_alunos)

        cabecalho_layout.addWidget(lbl_titulo)
        cabecalho_layout.addStretch()
        cabecalho_layout.addWidget(self.txt_busca_aluno, 2)
        cabecalho_layout.addWidget(btn_novo)
        cabecalho_layout.addWidget(btn_editar)
        cabecalho_layout.addWidget(btn_excluir)
        cabecalho_layout.addWidget(btn_imprimir)

        # Tabela de alunos
        self.tabela_alunos = QTableWidget()
        self.tabela_alunos.setColumnCount(10)
        self.tabela_alunos.setHorizontalHeaderLabels([
            "ID", "Nome", "CPF", "Data Nasc.", "Turma", "SÃ©rie",
            "ResponsÃ¡vel", "Telefone", "Status", "Data MatrÃ­cula"
        ])

        # Configurar tabela
        self.tabela_alunos.setAlternatingRowColors(True)
        self.tabela_alunos.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela_alunos.setSelectionMode(QTableWidget.SingleSelection)
        self.tabela_alunos.setEditTriggers(QTableWidget.NoEditTriggers)

        # Ajustar largura das colunas
        header = self.tabela_alunos.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Nome
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Turma
        header.setSectionResizeMode(9, QHeaderView.ResizeToContents)  # Data MatrÃ­cula

        # Conectar duplo clique
        self.tabela_alunos.doubleClicked.connect(self.ver_detalhes_aluno)

        # EstatÃ­sticas
        stats_layout = QHBoxLayout()

        lbl_total = QLabel("Total de alunos: 0")
        lbl_total.setObjectName("info-badge")

        lbl_ativos = QLabel("Ativos: 0")
        lbl_ativos.setObjectName("success-badge")

        lbl_inativos = QLabel("Inativos: 0")
        lbl_inativos.setObjectName("danger-badge")

        stats_layout.addWidget(lbl_total)
        stats_layout.addWidget(lbl_ativos)
        stats_layout.addWidget(lbl_inativos)
        stats_layout.addStretch()

        # Adicionar tudo ao layout
        layout.addLayout(cabecalho_layout)
        layout.addWidget(self.tabela_alunos)
        layout.addLayout(stats_layout)

        self.paginas['alunos'] = pagina
        self.central_widget.addWidget(pagina)

    def criar_pagina_professores(self):
        """Cria a pÃ¡gina de gerenciamento de professores"""
        # ImplementaÃ§Ã£o similar Ã  pÃ¡gina de alunos
        pagina = QWidget()
        # ... (cÃ³digo similar ao de alunos)

        self.paginas['professores'] = pagina
        self.central_widget.addWidget(pagina)

    def criar_pagina_disciplinas(self):
        """Cria a pÃ¡gina de gerenciamento de disciplinas"""
        pagina = QWidget()
        # ... (cÃ³digo similar)

        self.paginas['disciplinas'] = pagina
        self.central_widget.addWidget(pagina)

    def criar_pagina_notas(self):
        """Cria a pÃ¡gina de lanÃ§amento de notas"""
        pagina = QWidget()
        # ... (cÃ³digo similar)

        self.paginas['notas'] = pagina
        self.central_widget.addWidget(pagina)

    def criar_pagina_frequencia(self):
        """Cria a pÃ¡gina de registro de frequÃªncia"""
        pagina = QWidget()
        # ... (cÃ³digo similar)

        self.paginas['frequencia'] = pagina
        self.central_widget.addWidget(pagina)

    def criar_pagina_turmas(self):
        """Cria a pÃ¡gina de gerenciamento de turmas"""
        pagina = QWidget()
        # ... (cÃ³digo similar)

        self.paginas['turmas'] = pagina
        self.central_widget.addWidget(pagina)

    def criar_pagina_relatorios(self):
        """Cria a pÃ¡gina de relatÃ³rios"""
        pagina = QWidget()
        # ... (cÃ³digo similar)

        self.paginas['relatorios'] = pagina
        self.central_widget.addWidget(pagina)

    def criar_pagina_configuracoes(self):
        """Cria a pÃ¡gina de configuraÃ§Ãµes"""
        pagina = QWidget()
        # ... (cÃ³digo similar)

        self.paginas['configuracoes'] = pagina
        self.central_widget.addWidget(pagina)

    def carregar_dados_iniciais(self):
        """Carrega dados iniciais para o dashboard"""
        # Carregar totais
        self.carregar_totais_alunos()
        self.carregar_totais_professores()
        self.carregar_media_geral()
        self.carregar_frequencia_media()
        self.carregar_atividades_recentes()

    def carregar_totais_alunos(self):
        """Carrega o total de alunos"""
        try:
            resultado = self.db.execute_query(
                "SELECT COUNT(*) FROM alunos WHERE status = 'Ativo'",
                fetch=True
            )
            if resultado:
                self.lbl_total_alunos.setText(str(resultado[0][0]))
        except:
            self.lbl_total_alunos.setText("Erro")

    def carregar_totais_professores(self):
        """Carrega o total de professores"""
        try:
            resultado = self.db.execute_query(
                "SELECT COUNT(*) FROM professores WHERE ativo = 1",
                fetch=True
            )
            if resultado:
                self.lbl_total_professores.setText(str(resultado[0][0]))
        except:
            self.lbl_total_professores.setText("Erro")

    def carregar_media_geral(self):
        """Carrega a mÃ©dia geral das notas"""
        try:
            resultado = self.db.execute_query(
                "SELECT AVG(media) FROM notas WHERE media IS NOT NULL",
                fetch=True
            )
            if resultado and resultado[0][0]:
                media = float(resultado[0][0])
                self.lbl_media_geral.setText(f"{media:.1f}")
            else:
                self.lbl_media_geral.setText("N/A")
        except:
            self.lbl_media_geral.setText("Erro")

    def carregar_frequencia_media(self):
        """Carrega a frequÃªncia mÃ©dia"""
        try:
            resultado = self.db.execute_query(
                "SELECT AVG(presente) * 100 FROM frequencia",
                fetch=True
            )
            if resultado and resultado[0][0]:
                frequencia = float(resultado[0][0])
                self.lbl_frequencia.setText(f"{frequencia:.1f}%")
            else:
                self.lbl_frequencia.setText("N/A")
        except:
            self.lbl_frequencia.setText("Erro")

    def carregar_atividades_recentes(self):
        """Carrega atividades recentes"""
        atividades = [
            "Novo aluno cadastrado: JoÃ£o Silva",
            "Notas lanÃ§adas para MatemÃ¡tica - 1Âº Bimestre",
            "FrequÃªncia registrada para Turma A",
            "RelatÃ³rio de desempenho gerado",
            "Backup do sistema realizado"
        ]

        self.list_atividades.clear()
        for atividade in atividades:
            item = QListWidgetItem(f"â€¢ {atividade}")
            self.list_atividades.addItem(item)

    def obter_saudacao(self):
        """Retorna a saudaÃ§Ã£o apropriada para a hora atual"""
        hora_atual = datetime.now().hour

        if 5 <= hora_atual < 12:
            return "Bom dia"
        elif 12 <= hora_atual < 18:
            return "Boa tarde"
        else:
            return "Boa noite"

    def mostrar_pagina(self, nome_pagina):
        """Mostra a pÃ¡gina especificada"""
        if nome_pagina in self.paginas:
            self.central_widget.setCurrentWidget(self.paginas[nome_pagina])

            # Atualizar dados da pÃ¡gina se necessÃ¡rio
            if nome_pagina == 'inicial':
                self.carregar_dados_iniciais()
            elif nome_pagina == 'alunos':
                self.carregar_tabela_alunos()

    def carregar_tabela_alunos(self):
        """Carrega dados na tabela de alunos"""
        try:
            query = """
                SELECT id, nome, cpf, data_nascimento, turma, serie, 
                       nome_mae, telefone_responsavel, status, data_matricula
                FROM alunos
                ORDER BY nome
            """

            alunos = self.db.execute_query(query, fetch=True)

            self.tabela_alunos.setRowCount(0)

            for row_num, aluno in enumerate(alunos):
                self.tabela_alunos.insertRow(row_num)

                for col_num, valor in enumerate(aluno):
                    if col_num == 2 and valor:  # CPF
                        valor = ValidadorCampos.formatar_cpf(valor)
                    elif col_num == 7 and valor:  # Telefone
                        valor = ValidadorCampos.formatar_telefone(valor)
                    elif col_num in [3, 9] and valor:  # Datas
                        try:
                            data_obj = datetime.strptime(valor, '%Y-%m-%d')
                            valor = data_obj.strftime('%d/%m/%Y')
                        except:
                            pass

                    item = QTableWidgetItem(str(valor if valor else ""))

                    # Colorir status
                    if col_num == 8:  # Coluna de status
                        if valor == 'Ativo':
                            item.setForeground(QColor('#27ae60'))
                            item.setFont(QFont('', weight=QFont.Bold))
                        else:
                            item.setForeground(QColor('#e74c3c'))

                    self.tabela_alunos.setItem(row_num, col_num, item)

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar alunos:\n{str(e)}")

    def buscar_alunos(self):
        """Busca alunos baseado no texto da busca"""
        texto = self.txt_busca_aluno.text().strip()

        if not texto:
            self.carregar_tabela_alunos()
            return

        try:
            query = f"""
                SELECT id, nome, cpf, data_nascimento, turma, serie, 
                       nome_mae, telefone_responsavel, status, data_matricula
                FROM alunos
                WHERE nome LIKE ? OR cpf LIKE ? OR turma LIKE ? OR serie LIKE ?
                ORDER BY nome
            """

            parametro = f"%{texto}%"
            alunos = self.db.execute_query(
                query,
                (parametro, parametro, parametro, parametro),
                fetch=True
            )

            self.tabela_alunos.setRowCount(0)

            for row_num, aluno in enumerate(alunos):
                self.tabela_alunos.insertRow(row_num)

                for col_num, valor in enumerate(aluno):
                    item = QTableWidgetItem(str(valor if valor else ""))
                    self.tabela_alunos.setItem(row_num, col_num, item)

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao buscar alunos:\n{str(e)}")

    def cadastrar_aluno(self):
        """Abre diÃ¡logo para cadastrar novo aluno"""
        dialog = CadastroAlunoDialog(self)
        if dialog.exec_():
            self.carregar_tabela_alunos()
            self.carregar_totais_alunos()

    def editar_aluno(self):
        """Abre diÃ¡logo para editar aluno selecionado"""
        selecionados = self.tabela_alunos.selectedItems()

        if not selecionados:
            QMessageBox.warning(self, "SeleÃ§Ã£o necessÃ¡ria",
                                "Por favor, selecione um aluno para editar.")
            return

        id_aluno = int(self.tabela_alunos.item(selecionados[0].row(), 0).text())

        dialog = CadastroAlunoDialog(self, id_aluno)
        if dialog.exec_():
            self.carregar_tabela_alunos()

    def excluir_aluno(self):
        """Exclui aluno selecionado"""
        selecionados = self.tabela_alunos.selectedItems()

        if not selecionados:
            QMessageBox.warning(self, "SeleÃ§Ã£o necessÃ¡ria",
                                "Por favor, selecione um aluno para excluir.")
            return

        id_aluno = int(self.tabela_alunos.item(selecionados[0].row(), 0).text())
        nome_aluno = self.tabela_alunos.item(selecionados[0].row(), 1).text()

        resposta = QMessageBox.question(
            self, "Confirmar exclusÃ£o",
            f"Tem certeza que deseja excluir o aluno '{nome_aluno}'?\n\n"
            "Esta aÃ§Ã£o nÃ£o pode ser desfeita.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            try:
                self.db.execute_query(
                    "DELETE FROM alunos WHERE id = ?",
                    (id_aluno,)
                )

                QMessageBox.information(self, "Sucesso", "Aluno excluÃ­do com sucesso!")
                self.carregar_tabela_alunos()
                self.carregar_totais_alunos()

            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Falha ao excluir aluno:\n{str(e)}")

    def ver_detalhes_aluno(self, index):
        """Mostra detalhes do aluno em duplo clique"""
        row = index.row()
        id_aluno = int(self.tabela_alunos.item(row, 0).text())

        dialog = DetalhesAlunoDialog(self, id_aluno)
        dialog.exec_()

    def imprimir_lista_alunos(self):
        """Imprime lista de alunos"""
        QMessageBox.information(self, "Funcionalidade em desenvolvimento",
                                "A impressÃ£o de listas serÃ¡ implementada na prÃ³xima versÃ£o.")

    def realizar_backup(self):
        """Realiza backup do sistema"""
        try:
            backup_path = self.db.backup_database()

            if backup_path:
                QMessageBox.information(self, "Backup realizado",
                                        f"Backup criado com sucesso em:\n{backup_path}")
            else:
                QMessageBox.warning(self, "Backup falhou",
                                    "NÃ£o foi possÃ­vel criar o backup.")

        except Exception as e:
            QMessageBox.critical(self, "Erro no backup", f"Erro ao realizar backup:\n{str(e)}")

    def exportar_dados(self):
        """Exporta dados do sistema"""
        QMessageBox.information(self, "Funcionalidade em desenvolvimento",
                                "A exportaÃ§Ã£o de dados serÃ¡ implementada na prÃ³xima versÃ£o.")

    def importar_dados(self):
        """Importa dados para o sistema"""
        QMessageBox.information(self, "Funcionalidade em desenvolvimento",
                                "A importaÃ§Ã£o de dados serÃ¡ implementada na prÃ³xima versÃ£o.")

    def gerar_boletim(self):
        """Gera boletim escolar"""
        QMessageBox.information(self, "Funcionalidade em desenvolvimento",
                                "A geraÃ§Ã£o de boletins serÃ¡ implementada na prÃ³xima versÃ£o.")

    def gerar_relatorio_alunos(self):
        """Gera relatÃ³rio de alunos"""
        QMessageBox.information(self, "Funcionalidade em desenvolvimento",
                                "A geraÃ§Ã£o de relatÃ³rios serÃ¡ implementada na prÃ³xima versÃ£o.")

    def gerar_relatorio_notas(self):
        """Gera relatÃ³rio de notas"""
        QMessageBox.information(self, "Funcionalidade em desenvolvimento",
                                "A geraÃ§Ã£o de relatÃ³rios serÃ¡ implementada na prÃ³xima versÃ£o.")

    def gerar_relatorio_frequencia(self):
        """Gera relatÃ³rio de frequÃªncia"""
        QMessageBox.information(self, "Funcionalidade em desenvolvimento",
                                "A geraÃ§Ã£o de relatÃ³rios serÃ¡ implementada na prÃ³xima versÃ£o.")

    def relatorio_personalizado(self):
        """Gera relatÃ³rio personalizado"""
        QMessageBox.information(self, "Funcionalidade em desenvolvimento",
                                "A geraÃ§Ã£o de relatÃ³rios serÃ¡ implementada na prÃ³xima versÃ£o.")

    def gerenciar_usuarios(self):
        """Gerencia usuÃ¡rios do sistema"""
        QMessageBox.information(self, "Funcionalidade em desenvolvimento",
                                "O gerenciamento de usuÃ¡rios serÃ¡ implementado na prÃ³xima versÃ£o.")

    def trocar_usuario(self):
        """Troca o usuÃ¡rio atual"""
        resposta = QMessageBox.question(
            self, "Trocar usuÃ¡rio",
            "Deseja realmente sair e fazer login com outro usuÃ¡rio?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            self.close()
            # Em uma implementaÃ§Ã£o real, aqui voltaria para a tela de login

    def mostrar_sobre(self):
        """Mostra informaÃ§Ãµes sobre o sistema"""
        QMessageBox.about(self, "Sobre o Sistema",
                          "Sistema de GestÃ£o Escolar - Escola Objetivo\n\n"
                          "VersÃ£o: 2.0.0\n"
                          "Desenvolvido por: Alessandro Matheusti\n"
                          "Tecnologias: PyQt5, SQLite, Python\n\n"
                          "Â© 2024 Todos os direitos reservados.")

    def closeEvent(self, event):
        """Evento ao fechar a janela principal"""
        resposta = QMessageBox.question(
            self, "Confirmar saÃ­da",
            "Deseja realmente sair do sistema?\n\n"
            "Certifique-se de que todos os dados foram salvos.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


# ============================================
# DIÃLOGOS E FORMULÃRIOS
# ============================================

class CadastroAlunoDialog(QDialog):
    """DiÃ¡logo para cadastro/ediÃ§Ã£o de alunos"""

    def __init__(self, parent=None, id_aluno=None):
        super().__init__(parent)
        self.id_aluno = id_aluno
        self.db = DatabaseManager()
        self.modo_edicao = id_aluno is not None

        self.setWindowTitle("Cadastrar Aluno" if not self.modo_edicao else "Editar Aluno")
        self.setFixedSize(800, 700)
        self.setStyleSheet(GLOBAL_STYLESHEET)

        self.init_ui()
        self.carregar_dados_aluno() if self.modo_edicao else None

    def init_ui(self):
        """Inicializa a interface do diÃ¡logo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # TÃ­tulo
        titulo = "CADASTRAR NOVO ALUNO" if not self.modo_edicao else "EDITAR ALUNO"
        lbl_titulo = QLabel(titulo)
        lbl_titulo.setObjectName("title")
        lbl_titulo.setStyleSheet("""
            QLabel#title {
                font-size: 20px;
                font-weight: 700;
                color: #2c3e50;
                text-align: center;
                padding-bottom: 10px;
                border-bottom: 2px solid #3498db;
            }
        """)

        # Abas para organizaÃ§Ã£o
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #dce1e6;
                border-radius: 6px;
                background-color: white;
            }
        """)

        # Aba: Dados Pessoais
        aba_dados = QWidget()
        layout_dados = QFormLayout(aba_dados)
        layout_dados.setContentsMargins(20, 20, 20, 20)
        layout_dados.setSpacing(15)
        layout_dados.setLabelAlignment(Qt.AlignRight)

        # Campos
        self.txt_nome = QLineEdit()
        self.txt_nome.setPlaceholderText("Nome completo do aluno")

        self.txt_data_nasc = QDateEdit()
        self.txt_data_nasc.setCalendarPopup(True)
        self.txt_data_nasc.setDate(QDate.currentDate().addYears(-10))
        self.txt_data_nasc.setDisplayFormat("dd/MM/yyyy")

        self.txt_cpf = QLineEdit()
        self.txt_cpf.setPlaceholderText("000.000.000-00")
        self.txt_cpf.setInputMask("000.000.000-00")

        self.txt_rg = QLineEdit()
        self.txt_rg.setPlaceholderText("NÃºmero do RG")

        self.txt_nome_mae = QLineEdit()
        self.txt_nome_mae.setPlaceholderText("Nome completo da mÃ£e")

        self.txt_nome_pai = QLineEdit()
        self.txt_nome_pai.setPlaceholderText("Nome completo do pai")

        self.txt_telefone = QLineEdit()
        self.txt_telefone.setPlaceholderText("(00) 00000-0000")
        self.txt_telefone.setInputMask("(00) 00000-0000")

        self.txt_email = QLineEdit()
        self.txt_email.setPlaceholderText("email@exemplo.com")

        # Adicionar campos Ã  aba
        layout_dados.addRow("Nome completo:", self.txt_nome)
        layout_dados.addRow("Data de nascimento:", self.txt_data_nasc)
        layout_dados.addRow("CPF:", self.txt_cpf)
        layout_dados.addRow("RG:", self.txt_rg)
        layout_dados.addRow("Nome da mÃ£e:", self.txt_nome_mae)
        layout_dados.addRow("Nome do pai:", self.txt_nome_pai)
        layout_dados.addRow("Telefone:", self.txt_telefone)
        layout_dados.addRow("Email:", self.txt_email)

        # Aba: EndereÃ§o e MatrÃ­cula
        aba_endereco = QWidget()
        layout_endereco = QFormLayout(aba_endereco)
        layout_endereco.setContentsMargins(20, 20, 20, 20)
        layout_endereco.setSpacing(15)

        self.txt_endereco = QLineEdit()
        self.txt_endereco.setPlaceholderText("Rua, nÃºmero, complemento")

        self.txt_bairro = QLineEdit()
        self.txt_bairro.setPlaceholderText("Bairro")

        self.txt_cidade = QLineEdit()
        self.txt_cidade.setPlaceholderText("Cidade")

        self.txt_cep = QLineEdit()
        self.txt_cep.setPlaceholderText("00000-000")
        self.txt_cep.setInputMask("00000-000")

        self.combo_serie = QComboBox()
        series = self.db.get_config('series', '1Âº Ano,2Âº Ano,3Âº Ano,4Âº Ano,5Âº Ano').split(',')
        self.combo_serie.addItems(series)

        self.combo_turma = QComboBox()
        self.combo_turma.addItems(["A", "B", "C", "D", "E"])

        self.combo_turno = QComboBox()
        turnos = self.db.get_config('turnos', 'Matutino,Vespertino,Noturno').split(',')
        self.combo_turno.addItems(turnos)

        self.txt_data_matricula = QDateEdit()
        self.txt_data_matricula.setCalendarPopup(True)
        self.txt_data_matricula.setDate(QDate.currentDate())
        self.txt_data_matricula.setDisplayFormat("dd/MM/yyyy")

        self.combo_status = QComboBox()
        self.combo_status.addItems(["Ativo", "Inativo", "Transferido", "Evadido"])

        self.txt_observacoes = QTextEdit()
        self.txt_observacoes.setMaximumHeight(100)
        self.txt_observacoes.setPlaceholderText("ObservaÃ§Ãµes sobre o aluno...")

        # Adicionar campos Ã  aba
        layout_endereco.addRow("EndereÃ§o:", self.txt_endereco)
        layout_endereco.addRow("Bairro:", self.txt_bairro)
        layout_endereco.addRow("Cidade:", self.txt_cidade)
        layout_endereco.addRow("CEP:", self.txt_cep)
        layout_endereco.addRow("SÃ©rie:", self.combo_serie)
        layout_endereco.addRow("Turma:", self.combo_turma)
        layout_endereco.addRow("Turno:", self.combo_turno)
        layout_endereco.addRow("Data matrÃ­cula:", self.txt_data_matricula)
        layout_endereco.addRow("Status:", self.combo_status)
        layout_endereco.addRow("ObservaÃ§Ãµes:", self.txt_observacoes)

        # Adicionar abas ao tab widget
        tab_widget.addTab(aba_dados, "Dados Pessoais")
        tab_widget.addTab(aba_endereco, "EndereÃ§o & MatrÃ­cula")

        # BotÃµes
        botoes_layout = QHBoxLayout()

        self.btn_salvar = AnimacaoBotao(
            "SALVAR" if not self.modo_edicao else "ATUALIZAR",
            cor_normal="#27ae60", cor_hover="#219653", cor_press="#1e874b"
        )
        self.btn_salvar.setMinimumHeight(45)
        self.btn_salvar.clicked.connect(self.salvar_aluno)

        self.btn_cancelar = QPushButton("CANCELAR")
        self.btn_cancelar.setObjectName("danger")
        self.btn_cancelar.setMinimumHeight(45)
        self.btn_cancelar.clicked.connect(self.reject)

        if self.modo_edicao:
            self.btn_excluir = QPushButton("EXCLUIR")
            self.btn_excluir.setObjectName("warning")
            self.btn_excluir.setMinimumHeight(45)
            self.btn_excluir.clicked.connect(self.excluir_aluno)
            botoes_layout.addWidget(self.btn_excluir)

        botoes_layout.addStretch()
        botoes_layout.addWidget(self.btn_salvar)
        botoes_layout.addWidget(self.btn_cancelar)

        # Adicionar tudo ao layout principal
        layout.addWidget(lbl_titulo)
        layout.addWidget(tab_widget)
        layout.addLayout(botoes_layout)

    def carregar_dados_aluno(self):
        """Carrega dados do aluno para ediÃ§Ã£o"""
        try:
            aluno = self.db.execute_query(
                "SELECT * FROM alunos WHERE id = ?",
                (self.id_aluno,),
                fetch=True
            )

            if aluno and len(aluno) > 0:
                dados = aluno[0]

                # Dados pessoais
                self.txt_nome.setText(dados[1] if dados[1] else "")

                if dados[2]:  # Data nascimento
                    data_nasc = QDate.fromString(dados[2], 'yyyy-MM-dd')
                    self.txt_data_nasc.setDate(data_nasc)

                if dados[3]:  # CPF
                    cpf_formatado = ValidadorCampos.formatar_cpf(dados[3])
                    self.txt_cpf.setText(cpf_formatado)

                self.txt_rg.setText(dados[4] if dados[4] else "")
                self.txt_nome_mae.setText(dados[5] if dados[5] else "")
                self.txt_nome_pai.setText(dados[6] if dados[6] else "")

                if dados[7]:  # Telefone
                    telefone_formatado = ValidadorCampos.formatar_telefone(dados[7])
                    self.txt_telefone.setText(telefone_formatado)

                self.txt_email.setText(dados[8] if dados[8] else "")

                # EndereÃ§o
                self.txt_endereco.setText(dados[9] if dados[9] else "")
                self.txt_bairro.setText(dados[10] if dados[10] else "")
                self.txt_cidade.setText(dados[11] if dados[11] else "")
                self.txt_cep.setText(dados[12] if dados[12] else "")

                # MatrÃ­cula
                self.combo_serie.setCurrentText(dados[13] if dados[13] else "")
                self.combo_turma.setCurrentText(dados[14] if dados[14] else "")
                self.combo_turno.setCurrentText(dados[15] if dados[15] else "")

                if dados[16]:  # Data matrÃ­cula
                    data_mat = QDate.fromString(dados[16], 'yyyy-MM-dd')
                    self.txt_data_matricula.setDate(data_mat)

                if dados[17]:  # Status
                    self.combo_status.setCurrentText(dados[17])

                self.txt_observacoes.setText(dados[18] if dados[18] else "")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar dados do aluno:\n{str(e)}")

    def validar_campos(self):
        """Valida os campos do formulÃ¡rio"""
        erros = []

        # Nome obrigatÃ³rio
        if not self.txt_nome.text().strip():
            erros.append("Nome completo Ã© obrigatÃ³rio.")

        # CPF vÃ¡lido
        cpf = self.txt_cpf.text().replace('.', '').replace('-', '')
        if cpf and not ValidadorCampos.validar_cpf(cpf):
            erros.append("CPF invÃ¡lido.")

        # Email vÃ¡lido se preenchido
        email = self.txt_email.text().strip()
        if email and not ValidadorCampos.validar_email(email):
            erros.append("Email invÃ¡lido.")

        # Telefone vÃ¡lido
        telefone = self.txt_telefone.text().replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        if telefone and not ValidadorCampos.validar_telefone(telefone):
            erros.append("Telefone invÃ¡lido.")

        return erros

    def salvar_aluno(self):
        """Salva ou atualiza o aluno no banco de dados"""
        # Validar campos
        erros = self.validar_campos()
        if erros:
            QMessageBox.warning(self, "Erros no formulÃ¡rio", "\n".join(erros))
            return

        # Preparar dados
        dados = {
            'nome': self.txt_nome.text().strip(),
            'data_nascimento': self.txt_data_nasc.date().toString('yyyy-MM-dd'),
            'cpf': self.txt_cpf.text().replace('.', '').replace('-', ''),
            'rg': self.txt_rg.text().strip(),
            'nome_mae': self.txt_nome_mae.text().strip(),
            'nome_pai': self.txt_nome_pai.text().strip(),
            'telefone_responsavel': self.txt_telefone.text().replace('(', '').replace(')', '').replace('-', '').replace(
                ' ', ''),
            'email': self.txt_email.text().strip(),
            'endereco': self.txt_endereco.text().strip(),
            'bairro': self.txt_bairro.text().strip(),
            'cidade': self.txt_cidade.text().strip(),
            'cep': self.txt_cep.text().replace('-', ''),
            'serie': self.combo_serie.currentText(),
            'turma': self.combo_turma.currentText(),
            'turno': self.combo_turno.currentText(),
            'data_matricula': self.txt_data_matricula.date().toString('yyyy-MM-dd'),
            'status': self.combo_status.currentText(),
            'observacoes': self.txt_observacoes.toPlainText().strip()
        }

        try:
            if self.modo_edicao:
                # Atualizar aluno existente
                query = '''
                    UPDATE alunos SET
                        nome = ?, data_nascimento = ?, cpf = ?, rg = ?,
                        nome_mae = ?, nome_pai = ?, telefone_responsavel = ?, email = ?,
                        endereco = ?, bairro = ?, cidade = ?, cep = ?,
                        serie = ?, turma = ?, turno = ?, data_matricula = ?,
                        status = ?, observacoes = ?
                    WHERE id = ?
                '''

                params = (
                    dados['nome'], dados['data_nascimento'], dados['cpf'], dados['rg'],
                    dados['nome_mae'], dados['nome_pai'], dados['telefone_responsavel'], dados['email'],
                    dados['endereco'], dados['bairro'], dados['cidade'], dados['cep'],
                    dados['serie'], dados['turma'], dados['turno'], dados['data_matricula'],
                    dados['status'], dados['observacoes'], self.id_aluno
                )

                self.db.execute_query(query, params)
                QMessageBox.information(self, "Sucesso", "Aluno atualizado com sucesso!")

            else:
                # Inserir novo aluno
                query = '''
                    INSERT INTO alunos (
                        nome, data_nascimento, cpf, rg, nome_mae, nome_pai,
                        telefone_responsavel, email, endereco, bairro, cidade, cep,
                        serie, turma, turno, data_matricula, status, observacoes, data_cadastro
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                '''

                params = (
                    dados['nome'], dados['data_nascimento'], dados['cpf'], dados['rg'],
                    dados['nome_mae'], dados['nome_pai'], dados['telefone_responsavel'], dados['email'],
                    dados['endereco'], dados['bairro'], dados['cidade'], dados['cep'],
                    dados['serie'], dados['turma'], dados['turno'], dados['data_matricula'],
                    dados['status'], dados['observacoes']
                )

                self.db.execute_query(query, params)
                QMessageBox.information(self, "Sucesso", "Aluno cadastrado com sucesso!")

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao salvar aluno:\n{str(e)}")

    def excluir_aluno(self):
        """Exclui o aluno atual"""
        resposta = QMessageBox.question(
            self, "Confirmar exclusÃ£o",
            "Tem certeza que deseja excluir este aluno?\n\n"
            "Esta aÃ§Ã£o nÃ£o pode ser desfeita.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            try:
                self.db.execute_query(
                    "DELETE FROM alunos WHERE id = ?",
                    (self.id_aluno,)
                )

                QMessageBox.information(self, "Sucesso", "Aluno excluÃ­do com sucesso!")
                self.accept()

            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Falha ao excluir aluno:\n{str(e)}")


class DetalhesAlunoDialog(QDialog):
    """DiÃ¡logo para exibir detalhes completos do aluno"""

    def __init__(self, parent=None, id_aluno=None):
        super().__init__(parent)
        self.id_aluno = id_aluno
        self.db = DatabaseManager()

        self.setWindowTitle("Detalhes do Aluno")
        self.setFixedSize(900, 700)
        self.setStyleSheet(GLOBAL_STYLESHEET)

        self.init_ui()
        self.carregar_detalhes_aluno()

    def init_ui(self):
        """Inicializa a interface do diÃ¡logo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # CabeÃ§alho com nome do aluno
        self.lbl_nome_aluno = QLabel()
        self.lbl_nome_aluno.setObjectName("title")
        self.lbl_nome_aluno.setStyleSheet("""
            QLabel#title {
                font-size: 22px;
                font-weight: 700;
                color: #2c3e50;
                text-align: center;
                padding: 15px;
                background-color: #e3f2fd;
                border-radius: 8px;
                border: 2px solid #3498db;
            }
        """)

        # Abas para diferentes informaÃ§Ãµes
        tab_widget = QTabWidget()

        # Aba: InformaÃ§Ãµes Pessoais
        aba_info = QWidget()
        self.layout_info = QFormLayout(aba_info)
        self.layout_info.setContentsMargins(20, 20, 20, 20)
        self.layout_info.setSpacing(10)

        # Aba: HistÃ³rico AcadÃªmico
        aba_academico = QWidget()
        layout_academico = QVBoxLayout(aba_academico)

        self.tabela_notas = QTableWidget()
        self.tabela_notas.setColumnCount(6)
        self.tabela_notas.setHorizontalHeaderLabels([
            "Disciplina", "1Âº Bim", "2Âº Bim", "3Âº Bim", "4Âº Bim", "MÃ©dia"
        ])

        layout_academico.addWidget(QLabel("HistÃ³rico de Notas:"))
        layout_academico.addWidget(self.tabela_notas)

        # Aba: FrequÃªncia
        aba_frequencia = QWidget()
        layout_frequencia = QVBoxLayout(aba_frequencia)

        self.tabela_frequencia = QTableWidget()
        self.tabela_frequencia.setColumnCount(4)
        self.tabela_frequencia.setHorizontalHeaderLabels([
            "Data", "Disciplina", "PresenÃ§a", "ObservaÃ§Ãµes"
        ])

        layout_frequencia.addWidget(QLabel("Registro de FrequÃªncia:"))
        layout_frequencia.addWidget(self.tabela_frequencia)

        # Adicionar abas
        tab_widget.addTab(aba_info, "InformaÃ§Ãµes")
        tab_widget.addTab(aba_academico, "Notas")
        tab_widget.addTab(aba_frequencia, "FrequÃªncia")

        # BotÃµes
        botoes_layout = QHBoxLayout()

        btn_fechar = AnimacaoBotao("FECHAR", cor_normal="#7f8c8d", cor_hover="#95a5a6", cor_press="#5d6d7e")
        btn_fechar.clicked.connect(self.close)

        btn_imprimir = AnimacaoBotao("IMPRIMIR", cor_normal="#3498db", cor_hover="#2980b9", cor_press="#1c6ea4")
        btn_imprimir.clicked.connect(self.imprimir_detalhes)

        btn_editar = AnimacaoBotao("EDITAR", cor_normal="#27ae60", cor_hover="#219653", cor_press="#1e874b")
        btn_editar.clicked.connect(self.editar_aluno)

        botoes_layout.addWidget(btn_editar)
        botoes_layout.addWidget(btn_imprimir)
        botoes_layout.addStretch()
        botoes_layout.addWidget(btn_fechar)

        # Adicionar tudo ao layout
        layout.addWidget(self.lbl_nome_aluno)
        layout.addWidget(tab_widget)
        layout.addLayout(botoes_layout)

    def carregar_detalhes_aluno(self):
        """Carrega detalhes completos do aluno"""
        try:
            # Carregar informaÃ§Ãµes bÃ¡sicas
            aluno = self.db.execute_query(
                "SELECT * FROM alunos WHERE id = ?",
                (self.id_aluno,),
                fetch=True
            )

            if aluno and len(aluno) > 0:
                dados = aluno[0]

                # Atualizar tÃ­tulo
                self.lbl_nome_aluno.setText(dados[1])

                # Adicionar informaÃ§Ãµes pessoais
                self.adicionar_info("CPF:", ValidadorCampos.formatar_cpf(dados[3]) if dados[3] else "NÃ£o informado")
                self.adicionar_info("RG:", dados[4] if dados[4] else "NÃ£o informado")
                self.adicionar_info("Data Nascimento:",
                                    datetime.strptime(dados[2], '%Y-%m-%d').strftime('%d/%m/%Y') if dados[
                                        2] else "NÃ£o informada")
                self.adicionar_info("Idade:", self.calcular_idade(dados[2]) if dados[2] else "NÃ£o informada")
                self.adicionar_info("Nome da MÃ£e:", dados[5] if dados[5] else "NÃ£o informado")
                self.adicionar_info("Nome do Pai:", dados[6] if dados[6] else "NÃ£o informado")
                self.adicionar_info("Telefone:",
                                    ValidadorCampos.formatar_telefone(dados[7]) if dados[7] else "NÃ£o informado")
                self.adicionar_info("Email:", dados[8] if dados[8] else "NÃ£o informado")

                self.layout_info.addRow(QLabel(""), QLabel(""))  # EspaÃ§ador

                # InformaÃ§Ãµes de endereÃ§o
                self.adicionar_info("EndereÃ§o:", dados[9] if dados[9] else "NÃ£o informado")
                self.adicionar_info("Bairro:", dados[10] if dados[10] else "NÃ£o informado")
                self.adicionar_info("Cidade:", dados[11] if dados[11] else "NÃ£o informado")
                self.adicionar_info("CEP:", dados[12] if dados[12] else "NÃ£o informado")

                self.layout_info.addRow(QLabel(""), QLabel(""))  # EspaÃ§ador

                # InformaÃ§Ãµes acadÃªmicas
                self.adicionar_info("SÃ©rie:", dados[13] if dados[13] else "NÃ£o informado")
                self.adicionar_info("Turma:", dados[14] if dados[14] else "NÃ£o informado")
                self.adicionar_info("Turno:", dados[15] if dados[15] else "NÃ£o informado")
                self.adicionar_info("Data MatrÃ­cula:",
                                    datetime.strptime(dados[16], '%Y-%m-%d').strftime('%d/%m/%Y') if dados[
                                        16] else "NÃ£o informada")
                self.adicionar_info("Status:", dados[17] if dados[17] else "NÃ£o informado")

                # Carregar notas
                self.carregar_notas_aluno()

                # Carregar frequÃªncia
                self.carregar_frequencia_aluno()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar detalhes do aluno:\n{str(e)}")

    def adicionar_info(self, label, valor):
        """Adiciona uma linha de informaÃ§Ã£o ao formulÃ¡rio"""
        lbl_label = QLabel(label)
        lbl_label.setStyleSheet("font-weight: 600; color: #2c3e50;")

        lbl_valor = QLabel(valor)
        lbl_valor.setStyleSheet("color: #34495e;")

        self.layout_info.addRow(lbl_label, lbl_valor)

    def calcular_idade(self, data_nascimento):
        """Calcula idade a partir da data de nascimento"""
        try:
            nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d')
            hoje = datetime.now()

            idade = hoje.year - nascimento.year

            # Ajustar se ainda nÃ£o fez aniversÃ¡rio este ano
            if (hoje.month, hoje.day) < (nascimento.month, nascimento.day):
                idade -= 1

            return f"{idade} anos"
        except:
            return "NÃ£o calculada"

    def carregar_notas_aluno(self):
        """Carrega notas do aluno"""
        try:
            notas = self.db.execute_query('''
                SELECT d.nome, n.bimestre, n.nota1, n.nota2, n.nota3, n.nota4, n.media
                FROM notas n
                JOIN disciplinas d ON n.disciplina_id = d.id
                WHERE n.aluno_id = ?
                ORDER BY d.nome, n.bimestre
            ''', (self.id_aluno,), fetch=True)

            # Organizar por disciplina
            notas_por_disciplina = {}
            for disciplina, bimestre, n1, n2, n3, n4, media in notas:
                if disciplina not in notas_por_disciplina:
                    notas_por_disciplina[disciplina] = [None, None, None, None, 0.0]  # 4 bimestres + mÃ©dia

                if 1 <= bimestre <= 4:
                    # Calcular mÃ©dia do bimestre
                    notas_bimestre = [n for n in [n1, n2, n3, n4] if n is not None]
                    media_bimestre = sum(notas_bimestre) / len(notas_bimestre) if notas_bimestre else 0.0

                    notas_por_disciplina[disciplina][bimestre - 1] = f"{media_bimestre:.1f}"

                # Atualizar mÃ©dia geral se disponÃ­vel
                if media:
                    notas_por_disciplina[disciplina][4] = media

            # Preencher tabela
            self.tabela_notas.setRowCount(len(notas_por_disciplina))

            for row, (disciplina, dados) in enumerate(notas_por_disciplina.items()):
                self.tabela_notas.setItem(row, 0, QTableWidgetItem(disciplina))

                for bim in range(4):
                    item = QTableWidgetItem(dados[bim] if dados[bim] else "-")

                    # Colorir notas baixas
                    if dados[bim] and float(dados[bim]) < 5.0:
                        item.setForeground(QColor('#e74c3c'))
                    elif dados[bim] and float(dados[bim]) < 7.0:
                        item.setForeground(QColor('#f39c12'))
                    else:
                        item.setForeground(QColor('#27ae60'))

                    self.tabela_notas.setItem(row, bim + 1, item)

                # MÃ©dia final
                item_media = QTableWidgetItem(f"{dados[4]:.1f}" if dados[4] else "-")
                item_media.setFont(QFont('', weight=QFont.Bold))

                if dados[4]:
                    if dados[4] < 5.0:
                        item_media.setForeground(QColor('#e74c3c'))
                    elif dados[4] < 7.0:
                        item_media.setForeground(QColor('#f39c12'))
                    else:
                        item_media.setForeground(QColor('#27ae60'))

                self.tabela_notas.setItem(row, 5, item_media)

        except Exception as e:
            print(f"Erro ao carregar notas: {e}")

    def carregar_frequencia_aluno(self):
        """Carrega frequÃªncia do aluno"""
        try:
            frequencia = self.db.execute_query('''
                SELECT f.data, d.nome, f.presente, f.observacoes
                FROM frequencia f
                LEFT JOIN disciplinas d ON f.disciplina_id = d.id
                WHERE f.aluno_id = ?
                ORDER BY f.data DESC
                LIMIT 50
            ''', (self.id_aluno,), fetch=True)

            self.tabela_frequencia.setRowCount(len(frequencia))

            for row, (data, disciplina, presente, obs) in enumerate(frequencia):
                # Data
                data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%d/%m/%Y')
                self.tabela_frequencia.setItem(row, 0, QTableWidgetItem(data_formatada))

                # Disciplina
                self.tabela_frequencia.setItem(row, 1, QTableWidgetItem(disciplina if disciplina else "Geral"))

                # PresenÃ§a
                status = "Presente" if presente == 1 else "Faltou"
                item_presenca = QTableWidgetItem(status)

                if presente == 1:
                    item_presenca.setForeground(QColor('#27ae60'))
                    item_presenca.setFont(QFont('', weight=QFont.Bold))
                else:
                    item_presenca.setForeground(QColor('#e74c3c'))
                    item_presenca.setFont(QFont('', weight=QFont.Bold))

                self.tabela_frequencia.setItem(row, 2, item_presenca)

                # ObservaÃ§Ãµes
                self.tabela_frequencia.setItem(row, 3, QTableWidgetItem(obs if obs else ""))

        except Exception as e:
            print(f"Erro ao carregar frequÃªncia: {e}")

    def imprimir_detalhes(self):
        """Imprime detalhes do aluno"""
        QMessageBox.information(self, "Funcionalidade em desenvolvimento",
                                "A impressÃ£o de detalhes serÃ¡ implementada na prÃ³xima versÃ£o.")

    def editar_aluno(self):
        """Abre diÃ¡logo para editar o aluno"""
        self.close()
        # Em uma implementaÃ§Ã£o real, aqui abriria o diÃ¡logo de ediÃ§Ã£o


# ============================================
# FUNÃ‡ÃƒO PRINCIPAL E INICIALIZAÃ‡ÃƒO
# ============================================

def main():
    """FunÃ§Ã£o principal do aplicativo"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Estilo moderno

    # Aplicar stylesheet global
    app.setStyleSheet(GLOBAL_STYLESHEET)

    # Verificar e inicializar banco de dados
    db_manager = DatabaseManager()
    if not db_manager.init_database():
        QMessageBox.critical(None, "Erro CrÃ­tico",
                             "NÃ£o foi possÃ­vel inicializar o banco de dados.\n"
                             "O aplicativo serÃ¡ fechado.")
        sys.exit(1)

    # Mostrar tela de login
    login_window = JanelaLogin()
    login_window.show()

    def on_login_sucesso(tipo_usuario, dados_json):
        """Callback para login bem-sucedido"""
        dados_usuario = json.loads(dados_json)

        # Fechar tela de login
        login_window.close()

        # Abrir tela principal
        main_window = JanelaPrincipal(tipo_usuario, dados_usuario)
        main_window.show()

    # Conectar sinal de login
    login_window.login_sucesso.connect(on_login_sucesso)

    # Executar aplicaÃ§Ã£o
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
"""
PROJETO ESCOLA - SISTEMA DE GESTÃƒO ESCOLAR
Parte 2/10 - ContinuaÃ§Ã£o das funcionalidades principais
"""


# ============================================
# PÃGINA DE PROFESSORES (COMPLETA)
# ============================================

def criar_pagina_professores(self):
    """Cria a pÃ¡gina de gerenciamento de professores - COMPLETA"""
    pagina = QWidget()
    layout = QVBoxLayout(pagina)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(20)

    # CabeÃ§alho
    cabecalho_layout = QHBoxLayout()

    lbl_titulo = QLabel("GESTÃƒO DE PROFESSORES")
    lbl_titulo.setObjectName("title")

    # Barra de busca
    self.txt_busca_professor = QLineEdit()
    self.txt_busca_professor.setPlaceholderText("Buscar professor por nome, CPF ou matÃ©ria...")
    self.txt_busca_professor.setMinimumHeight(40)
    self.txt_busca_professor.textChanged.connect(self.buscar_professores)

    # BotÃµes de aÃ§Ã£o
    btn_novo = AnimacaoBotao("Novo Professor", cor_normal="#27ae60", cor_hover="#219653", cor_press="#1e874b")
    btn_novo.setIcon(self.style().standardIcon(QStyle.SP_FileIcon))
    btn_novo.clicked.connect(self.cadastrar_professor)

    btn_editar = AnimacaoBotao("Editar", cor_normal="#3498db", cor_hover="#2980b9", cor_press="#1c6ea4")
    btn_editar.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
    btn_editar.clicked.connect(self.editar_professor)

    btn_excluir = AnimacaoBotao("Excluir", cor_normal="#e74c3c", cor_hover="#c0392b", cor_press="#a93226")
    btn_excluir.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
    btn_excluir.clicked.connect(self.excluir_professor)

    btn_horarios = AnimacaoBotao("HorÃ¡rios", cor_normal="#9b59b6", cor_hover="#8e44ad", cor_press="#7d3c98")
    btn_horarios.setIcon(self.style().standardIcon(QStyle.SP_FileDialogListView))
    btn_horarios.clicked.connect(self.ver_horarios_professor)

    cabecalho_layout.addWidget(lbl_titulo)
    cabecalho_layout.addStretch()
    cabecalho_layout.addWidget(self.txt_busca_professor, 2)
    cabecalho_layout.addWidget(btn_novo)
    cabecalho_layout.addWidget(btn_editar)
    cabecalho_layout.addWidget(btn_excluir)
    cabecalho_layout.addWidget(btn_horarios)

    # Tabela de professores
    self.tabela_professores = QTableWidget()
    self.tabela_professores.setColumnCount(10)
    self.tabela_professores.setHorizontalHeaderLabels([
        "ID", "Nome", "CPF", "MatÃ©ria", "FormaÃ§Ã£o", "Telefone",
        "Email", "Data ContrataÃ§Ã£o", "SalÃ¡rio", "Status"
    ])

    # Configurar tabela
    self.tabela_professores.setAlternatingRowColors(True)
    self.tabela_professores.setSelectionBehavior(QTableWidget.SelectRows)
    self.tabela_professores.setSelectionMode(QTableWidget.SingleSelection)
    self.tabela_professores.setEditTriggers(QTableWidget.NoEditTriggers)

    # Ajustar largura das colunas
    header = self.tabela_professores.horizontalHeader()
    header.setSectionResizeMode(1, QHeaderView.Stretch)  # Nome
    header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # MatÃ©ria
    header.setSectionResizeMode(9, QHeaderView.ResizeToContents)  # Status

    # Conectar duplo clique
    self.tabela_professores.doubleClicked.connect(self.ver_detalhes_professor)

    # EstatÃ­sticas
    stats_layout = QHBoxLayout()

    self.lbl_total_prof = QLabel("Total de professores: 0")
    self.lbl_total_prof.setObjectName("info-badge")

    self.lbl_prof_ativos = QLabel("Ativos: 0")
    self.lbl_prof_ativos.setObjectName("success-badge")

    self.lbl_prof_inativos = QLabel("Inativos: 0")
    self.lbl_prof_inativos.setObjectName("danger-badge")

    stats_layout.addWidget(self.lbl_total_prof)
    stats_layout.addWidget(self.lbl_prof_ativos)
    stats_layout.addWidget(self.lbl_prof_inativos)
    stats_layout.addStretch()

    # Adicionar tudo ao layout
    layout.addLayout(cabecalho_layout)
    layout.addWidget(self.tabela_professores)
    layout.addLayout(stats_layout)

    self.paginas['professores'] = pagina
    self.central_widget.addWidget(pagina)

    # Carregar dados iniciais
    self.carregar_tabela_professores()


def carregar_tabela_professores(self):
    """Carrega dados na tabela de professores"""
    try:
        query = """
                SELECT id, nome, cpf, materia, formacao, telefone, 
                       email, data_contratacao, salario, ativo
                FROM professores
                ORDER BY nome
            """

        professores = self.db.execute_query(query, fetch=True)

        self.tabela_professores.setRowCount(0)

        for row_num, professor in enumerate(professores):
            self.tabela_professores.insertRow(row_num)

            for col_num, valor in enumerate(professor):
                if col_num == 2 and valor:  # CPF
                    valor = ValidadorCampos.formatar_cpf(valor)
                elif col_num == 5 and valor:  # Telefone
                    valor = ValidadorCampos.formatar_telefone(valor)
                elif col_num == 7 and valor:  # Data contrataÃ§Ã£o
                    try:
                        data_obj = datetime.strptime(valor, '%Y-%m-%d')
                        valor = data_obj.strftime('%d/%m/%Y')
                    except:
                        pass
                elif col_num == 8 and valor:  # SalÃ¡rio
                    valor = f"R$ {float(valor):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                elif col_num == 9:  # Status
                    valor = "Ativo" if valor == 1 else "Inativo"

                item = QTableWidgetItem(str(valor if valor else ""))

                # Colorir status
                if col_num == 9:
                    if professor[9] == 1:  # Ativo
                        item.setForeground(QColor('#27ae60'))
                        item.setFont(QFont('', weight=QFont.Bold))
                    else:
                        item.setForeground(QColor('#e74c3c'))

                self.tabela_professores.setItem(row_num, col_num, item)

        # Atualizar estatÃ­sticas
        self.atualizar_estatisticas_professores(professores)

    except Exception as e:
        QMessageBox.critical(self, "Erro", f"Falha ao carregar professores:\n{str(e)}")


def atualizar_estatisticas_professores(self, professores):
    """Atualiza as estatÃ­sticas de professores"""
    total = len(professores)
    ativos = sum(1 for p in professores if p[9] == 1)
    inativos = total - ativos

    self.lbl_total_prof.setText(f"Total de professores: {total}")
    self.lbl_prof_ativos.setText(f"Ativos: {ativos}")
    self.lbl_prof_inativos.setText(f"Inativos: {inativos}")


def buscar_professores(self):
    """Busca professores baseado no texto da busca"""
    texto = self.txt_busca_professor.text().strip()

    if not texto:
        self.carregar_tabela_professores()
        return

    try:
        query = f"""
                SELECT id, nome, cpf, materia, formacao, telefone, 
                       email, data_contratacao, salario, ativo
                FROM professores
                WHERE nome LIKE ? OR cpf LIKE ? OR materia LIKE ? OR formacao LIKE ?
                ORDER BY nome
            """

        parametro = f"%{texto}%"
        professores = self.db.execute_query(
            query,
            (parametro, parametro, parametro, parametro),
            fetch=True
        )

        self.tabela_professores.setRowCount(0)

        for row_num, professor in enumerate(professores):
            self.tabela_professores.insertRow(row_num)

            for col_num, valor in enumerate(professor):
                item = QTableWidgetItem(str(valor if valor else ""))
                self.tabela_professores.setItem(row_num, col_num, item)

        self.atualizar_estatisticas_professores(professores)

    except Exception as e:
        QMessageBox.critical(self, "Erro", f"Falha ao buscar professores:\n{str(e)}")


def cadastrar_professor(self):
    """Abre diÃ¡logo para cadastrar novo professor"""
    dialog = CadastroProfessorDialog(self)
    if dialog.exec_():
        self.carregar_tabela_professores()


def editar_professor(self):
    """Abre diÃ¡logo para editar professor selecionado"""
    selecionados = self.tabela_professores.selectedItems()

    if not selecionados:
        QMessageBox.warning(self, "SeleÃ§Ã£o necessÃ¡ria",
                            "Por favor, selecione um professor para editar.")
        return

    id_professor = int(self.tabela_professores.item(selecionados[0].row(), 0).text())

    dialog = CadastroProfessorDialog(self, id_professor)
    if dialog.exec_():
        self.carregar_tabela_professores()


def excluir_professor(self):
    """Exclui professor selecionado"""
    selecionados = self.tabela_professores.selectedItems()

    if not selecionados:
        QMessageBox.warning(self, "SeleÃ§Ã£o necessÃ¡ria",
                            "Por favor, selecione um professor para excluir.")
        return

    id_professor = int(self.tabela_professores.item(selecionados[0].row(), 0).text())
    nome_professor = self.tabela_professores.item(selecionados[0].row(), 1).text()

    resposta = QMessageBox.question(
        self, "Confirmar exclusÃ£o",
        f"Tem certeza que deseja excluir o professor '{nome_professor}'?\n\n"
        "Esta aÃ§Ã£o nÃ£o pode ser desfeita.",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )

    if resposta == QMessageBox.Yes:
        try:
            # Verificar se o professor tem disciplinas associadas
            disciplinas = self.db.execute_query(
                "SELECT COUNT(*) FROM disciplinas WHERE professor_id = ?",
                (id_professor,),
                fetch=True
            )

            if disciplinas and disciplinas[0][0] > 0:
                QMessageBox.warning(self, "Professor possui disciplinas",
                                    "Este professor estÃ¡ vinculado a disciplinas.\n"
                                    "Remova as associaÃ§Ãµes primeiro.")
                return

            self.db.execute_query(
                "DELETE FROM professores WHERE id = ?",
                (id_professor,)
            )

            QMessageBox.information(self, "Sucesso", "Professor excluÃ­do com sucesso!")
            self.carregar_tabela_professores()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao excluir professor:\n{str(e)}")


def ver_detalhes_professor(self, index):
    """Mostra detalhes do professor em duplo clique"""
    row = index.row()
    id_professor = int(self.tabela_professores.item(row, 0).text())

    dialog = DetalhesProfessorDialog(self, id_professor)
    dialog.exec_()


def ver_horarios_professor(self):
    """Mostra horÃ¡rios do professor selecionado"""
    selecionados = self.tabela_professores.selectedItems()

    if not selecionados:
        QMessageBox.warning(self, "SeleÃ§Ã£o necessÃ¡ria",
                            "Por favor, selecione um professor para ver horÃ¡rios.")
        return

    id_professor = int(self.tabela_professores.item(selecionados[0].row(), 0).text())
    nome_professor = self.tabela_professores.item(selecionados[0].row(), 1).text()

    dialog = HorariosProfessorDialog(self, id_professor, nome_professor)
    dialog.exec_()


# ============================================
# DIÃLOGO DE CADASTRO DE PROFESSOR
# ============================================

class CadastroProfessorDialog(QDialog):
    """DiÃ¡logo para cadastro/ediÃ§Ã£o de professores"""

    def __init__(self, parent=None, id_professor=None):
        super().__init__(parent)
        self.id_professor = id_professor
        self.db = DatabaseManager()
        self.modo_edicao = id_professor is not None

        self.setWindowTitle("Cadastrar Professor" if not self.modo_edicao else "Editar Professor")
        self.setFixedSize(800, 750)
        self.setStyleSheet(GLOBAL_STYLESHEET)

        self.init_ui()
        self.carregar_dados_professor() if self.modo_edicao else None

    def init_ui(self):
        """Inicializa a interface do diÃ¡logo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # TÃ­tulo
        titulo = "CADASTRAR NOVO PROFESSOR" if not self.modo_edicao else "EDITAR PROFESSOR"
        lbl_titulo = QLabel(titulo)
        lbl_titulo.setObjectName("title")

        # Abas para organizaÃ§Ã£o
        tab_widget = QTabWidget()

        # Aba: Dados Pessoais
        aba_dados = QWidget()
        layout_dados = QFormLayout(aba_dados)
        layout_dados.setContentsMargins(20, 20, 20, 20)
        layout_dados.setSpacing(15)

        # Campos de dados pessoais
        self.txt_nome = QLineEdit()
        self.txt_nome.setPlaceholderText("Nome completo do professor")

        self.txt_cpf = QLineEdit()
        self.txt_cpf.setPlaceholderText("000.000.000-00")
        self.txt_cpf.setInputMask("000.000.000-00")

        self.txt_telefone = QLineEdit()
        self.txt_telefone.setPlaceholderText("(00) 00000-0000")
        self.txt_telefone.setInputMask("(00) 00000-0000")

        self.txt_email = QLineEdit()
        self.txt_email.setPlaceholderText("professor@escola.com")

        self.txt_endereco = QLineEdit()
        self.txt_endereco.setPlaceholderText("EndereÃ§o completo")

        # Adicionar campos Ã  aba
        layout_dados.addRow("Nome completo:", self.txt_nome)
        layout_dados.addRow("CPF:", self.txt_cpf)
        layout_dados.addRow("Telefone:", self.txt_telefone)
        layout_dados.addRow("Email:", self.txt_email)
        layout_dados.addRow("EndereÃ§o:", self.txt_endereco)

        # Aba: Dados Profissionais
        aba_profissional = QWidget()
        layout_profissional = QFormLayout(aba_profissional)
        layout_profissional.setContentsMargins(20, 20, 20, 20)
        layout_profissional.setSpacing(15)

        self.txt_materia = QLineEdit()
        self.txt_materia.setPlaceholderText("Ex: MatemÃ¡tica, PortuguÃªs, HistÃ³ria")

        self.txt_formacao = QLineEdit()
        self.txt_formacao.setPlaceholderText("Ex: Licenciatura em MatemÃ¡tica")

        self.txt_data_contratacao = QDateEdit()
        self.txt_data_contratacao.setCalendarPopup(True)
        self.txt_data_contratacao.setDate(QDate.currentDate())
        self.txt_data_contratacao.setDisplayFormat("dd/MM/yyyy")

        self.txt_salario = QDoubleSpinBox()
        self.txt_salario.setRange(0, 99999.99)
        self.txt_salario.setPrefix("R$ ")
        self.txt_salario.setDecimals(2)
        self.txt_salario.setSingleStep(500.00)
        self.txt_salario.setValue(2000.00)

        self.combo_status = QComboBox()
        self.combo_status.addItems(["Ativo", "Inativo"])

        self.txt_observacoes = QTextEdit()
        self.txt_observacoes.setMaximumHeight(100)
        self.txt_observacoes.setPlaceholderText("ObservaÃ§Ãµes sobre o professor...")

        # Adicionar campos Ã  aba
        layout_profissional.addRow("MatÃ©ria principal:", self.txt_materia)
        layout_profissional.addRow("FormaÃ§Ã£o acadÃªmica:", self.txt_formacao)
        layout_profissional.addRow("Data de contrataÃ§Ã£o:", self.txt_data_contratacao)
        layout_profissional.addRow("SalÃ¡rio:", self.txt_salario)
        layout_profissional.addRow("Status:", self.combo_status)
        layout_profissional.addRow("ObservaÃ§Ãµes:", self.txt_observacoes)

        # Aba: Credenciais de Acesso
        aba_credenciais = QWidget()
        layout_credenciais = QFormLayout(aba_credenciais)
        layout_credenciais.setContentsMargins(20, 20, 20, 20)
        layout_credenciais.setSpacing(15)

        self.txt_usuario = QLineEdit()
        self.txt_usuario.setPlaceholderText("Nome de usuÃ¡rio para login")

        self.txt_senha = QLineEdit()
        self.txt_senha.setPlaceholderText("Senha para acesso ao sistema")
        self.txt_senha.setEchoMode(QLineEdit.Password)

        self.txt_confirmar_senha = QLineEdit()
        self.txt_confirmar_senha.setPlaceholderText("Confirmar senha")
        self.txt_confirmar_senha.setEchoMode(QLineEdit.Password)

        # Checkbox para gerar senha automÃ¡tica
        self.check_gerar_senha = QCheckBox("Gerar senha automÃ¡tica")
        self.check_gerar_senha.stateChanged.connect(self.toggle_gerar_senha)

        # BotÃ£o para gerar senha
        self.btn_gerar_senha = QPushButton("Gerar Senha")
        self.btn_gerar_senha.setObjectName("secondary")
        self.btn_gerar_senha.clicked.connect(self.gerar_senha_automatica)

        layout_credenciais.addRow("UsuÃ¡rio:", self.txt_usuario)
        layout_credenciais.addRow("Senha:", self.txt_senha)
        layout_credenciais.addRow("Confirmar senha:", self.txt_confirmar_senha)
        layout_credenciais.addRow("", self.check_gerar_senha)
        layout_credenciais.addRow("", self.btn_gerar_senha)

        # Adicionar abas ao tab widget
        tab_widget.addTab(aba_dados, "Dados Pessoais")
        tab_widget.addTab(aba_profissional, "Dados Profissionais")
        tab_widget.addTab(aba_credenciais, "Credenciais de Acesso")

        # BotÃµes
        botoes_layout = QHBoxLayout()

        self.btn_salvar = AnimacaoBotao(
            "SALVAR" if not self.modo_edicao else "ATUALIZAR",
            cor_normal="#27ae60", cor_hover="#219653", cor_press="#1e874b"
        )
        self.btn_salvar.setMinimumHeight(45)
        self.btn_salvar.clicked.connect(self.salvar_professor)

        self.btn_cancelar = QPushButton("CANCELAR")
        self.btn_cancelar.setObjectName("danger")
        self.btn_cancelar.setMinimumHeight(45)
        self.btn_cancelar.clicked.connect(self.reject)

        if self.modo_edicao:
            self.btn_excluir = QPushButton("EXCLUIR")
            self.btn_excluir.setObjectName("warning")
            self.btn_excluir.setMinimumHeight(45)
            self.btn_excluir.clicked.connect(self.excluir_professor)
            botoes_layout.addWidget(self.btn_excluir)

        botoes_layout.addStretch()
        botoes_layout.addWidget(self.btn_salvar)
        botoes_layout.addWidget(self.btn_cancelar)

        # Adicionar tudo ao layout principal
        layout.addWidget(lbl_titulo)
        layout.addWidget(tab_widget)
        layout.addLayout(botoes_layout)

        # Inicializar estado dos campos de senha
        self.toggle_gerar_senha()

    def carregar_dados_professor(self):
        """Carrega dados do professor para ediÃ§Ã£o"""
        try:
            professor = self.db.execute_query(
                "SELECT * FROM professores WHERE id = ?",
                (self.id_professor,),
                fetch=True
            )

            if professor and len(professor) > 0:
                dados = professor[0]

                # Dados pessoais
                self.txt_nome.setText(dados[1] if dados[1] else "")

                if dados[2]:  # CPF
                    cpf_formatado = ValidadorCampos.formatar_cpf(dados[2])
                    self.txt_cpf.setText(cpf_formatado)

                if dados[3]:  # Telefone
                    telefone_formatado = ValidadorCampos.formatar_telefone(dados[3])
                    self.txt_telefone.setText(telefone_formatado)

                self.txt_email.setText(dados[4] if dados[4] else "")
                self.txt_materia.setText(dados[5] if dados[5] else "")
                self.txt_formacao.setText(dados[6] if dados[6] else "")

                if dados[7]:  # Data contrataÃ§Ã£o
                    data_contr = QDate.fromString(dados[7], 'yyyy-MM-dd')
                    self.txt_data_contratacao.setDate(data_contr)

                if dados[8]:  # SalÃ¡rio
                    self.txt_salario.setValue(float(dados[8]))

                self.txt_endereco.setText(dados[9] if dados[9] else "")
                self.txt_observacoes.setText(dados[10] if dados[10] else "")

                # Status
                self.combo_status.setCurrentIndex(0 if dados[11] == 1 else 1)

                # Credenciais
                self.txt_usuario.setText(dados[12] if dados[12] else "")
                # Senha nÃ£o Ã© carregada por seguranÃ§a

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar dados do professor:\n{str(e)}")

    def toggle_gerar_senha(self):
        """Ativa/desativa campos de senha baseado no checkbox"""
        if self.check_gerar_senha.isChecked():
            self.txt_senha.setEnabled(False)
            self.txt_confirmar_senha.setEnabled(False)
            self.btn_gerar_senha.setEnabled(True)
        else:
            self.txt_senha.setEnabled(True)
            self.txt_confirmar_senha.setEnabled(True)
            self.btn_gerar_senha.setEnabled(False)

    def gerar_senha_automatica(self):
        """Gera uma senha aleatÃ³ria"""
        import random
        import string

        # Gerar senha de 8 caracteres com letras e nÃºmeros
        caracteres = string.ascii_letters + string.digits
        senha = ''.join(random.choice(caracteres) for i in range(8))

        self.txt_senha.setText(senha)
        self.txt_confirmar_senha.setText(senha)

        QMessageBox.information(self, "Senha Gerada",
                                f"Senha gerada: {senha}\n\n"
                                "Anote esta senha para fornecÃª-la ao professor.")

    def validar_campos(self):
        """Valida os campos do formulÃ¡rio"""
        erros = []

        # Nome obrigatÃ³rio
        if not self.txt_nome.text().strip():
            erros.append("Nome completo Ã© obrigatÃ³rio.")

        # CPF vÃ¡lido
        cpf = self.txt_cpf.text().replace('.', '').replace('-', '')
        if cpf and not ValidadorCampos.validar_cpf(cpf):
            erros.append("CPF invÃ¡lido.")

        # Email vÃ¡lido se preenchido
        email = self.txt_email.text().strip()
        if email and not ValidadorCampos.validar_email(email):
            erros.append("Email invÃ¡lido.")

        # MatÃ©ria obrigatÃ³ria
        if not self.txt_materia.text().strip():
            erros.append("MatÃ©ria Ã© obrigatÃ³ria.")

        # ValidaÃ§Ã£o de credenciais (apenas para novo professor)
        if not self.modo_edicao:
            usuario = self.txt_usuario.text().strip()
            senha = self.txt_senha.text().strip()
            confirmar_senha = self.txt_confirmar_senha.text().strip()

            if not usuario:
                erros.append("UsuÃ¡rio Ã© obrigatÃ³rio.")
            else:
                # Verificar se usuÃ¡rio jÃ¡ existe
                resultado = self.db.execute_query(
                    "SELECT COUNT(*) FROM professores WHERE usuario = ?",
                    (usuario,),
                    fetch=True
                )
                if resultado and resultado[0][0] > 0:
                    erros.append("UsuÃ¡rio jÃ¡ estÃ¡ em uso.")

            if not self.check_gerar_senha.isChecked():
                if not senha:
                    erros.append("Senha Ã© obrigatÃ³ria.")
                elif len(senha) < 6:
                    erros.append("Senha deve ter no mÃ­nimo 6 caracteres.")
                elif senha != confirmar_senha:
                    erros.append("As senhas nÃ£o conferem.")

        return erros

    def salvar_professor(self):
        """Salva ou atualiza o professor no banco de dados"""
        # Validar campos
        erros = self.validar_campos()
        if erros:
            QMessageBox.warning(self, "Erros no formulÃ¡rio", "\n".join(erros))
            return

        # Preparar dados
        dados = {
            'nome': self.txt_nome.text().strip(),
            'cpf': self.txt_cpf.text().replace('.', '').replace('-', ''),
            'telefone': self.txt_telefone.text().replace('(', '').replace(')', '').replace('-', '').replace(' ', ''),
            'email': self.txt_email.text().strip(),
            'materia': self.txt_materia.text().strip(),
            'formacao': self.txt_formacao.text().strip(),
            'data_contratacao': self.txt_data_contratacao.date().toString('yyyy-MM-dd'),
            'salario': self.txt_salario.value(),
            'endereco': self.txt_endereco.text().strip(),
            'observacoes': self.txt_observacoes.toPlainText().strip(),
            'ativo': 1 if self.combo_status.currentText() == "Ativo" else 0,
            'usuario': self.txt_usuario.text().strip(),
            'senha': ""
        }

        # Gerar senha hash se necessÃ¡rio
        if not self.modo_edicao or self.txt_senha.text():
            senha = self.txt_senha.text() if not self.check_gerar_senha.isChecked() else self.txt_senha.text()
            dados['senha'] = hashlib.sha256(senha.encode()).hexdigest()

        try:
            if self.modo_edicao:
                # Atualizar professor existente
                if dados['senha']:
                    query = '''
                        UPDATE professores SET
                            nome = ?, cpf = ?, telefone = ?, email = ?, materia = ?,
                            formacao = ?, data_contratacao = ?, salario = ?, endereco = ?,
                            observacoes = ?, ativo = ?, usuario = ?, senha = ?
                        WHERE id = ?
                    '''
                    params = (
                        dados['nome'], dados['cpf'], dados['telefone'], dados['email'],
                        dados['materia'], dados['formacao'], dados['data_contratacao'],
                        dados['salario'], dados['endereco'], dados['observacoes'],
                        dados['ativo'], dados['usuario'], dados['senha'], self.id_professor
                    )
                else:
                    query = '''
                        UPDATE professores SET
                            nome = ?, cpf = ?, telefone = ?, email = ?, materia = ?,
                            formacao = ?, data_contratacao = ?, salario = ?, endereco = ?,
                            observacoes = ?, ativo = ?, usuario = ?
                        WHERE id = ?
                    '''
                    params = (
                        dados['nome'], dados['cpf'], dados['telefone'], dados['email'],
                        dados['materia'], dados['formacao'], dados['data_contratacao'],
                        dados['salario'], dados['endereco'], dados['observacoes'],
                        dados['ativo'], dados['usuario'], self.id_professor
                    )

                self.db.execute_query(query, params)
                QMessageBox.information(self, "Sucesso", "Professor atualizado com sucesso!")

            else:
                # Inserir novo professor
                query = '''
                    INSERT INTO professores (
                        nome, cpf, telefone, email, materia, formacao,
                        data_contratacao, salario, endereco, observacoes,
                        ativo, usuario, senha, data_cadastro
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                '''

                params = (
                    dados['nome'], dados['cpf'], dados['telefone'], dados['email'],
                    dados['materia'], dados['formacao'], dados['data_contratacao'],
                    dados['salario'], dados['endereco'], dados['observacoes'],
                    dados['ativo'], dados['usuario'], dados['senha']
                )

                self.db.execute_query(query, params)
                QMessageBox.information(self, "Sucesso", "Professor cadastrado com sucesso!")

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao salvar professor:\n{str(e)}")

    def excluir_professor(self):
        """Exclui o professor atual"""
        resposta = QMessageBox.question(
            self, "Confirmar exclusÃ£o",
            "Tem certeza que deseja excluir este professor?\n\n"
            "Esta aÃ§Ã£o nÃ£o pode ser desfeita.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            try:
                self.db.execute_query(
                    "DELETE FROM professores WHERE id = ?",
                    (self.id_professor,)
                )

                QMessageBox.information(self, "Sucesso", "Professor excluÃ­do com sucesso!")
                self.accept()

            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Falha ao excluir professor:\n{str(e)}")


# ============================================
# DIÃLOGO DE DETALHES DO PROFESSOR
# ============================================

class DetalhesProfessorDialog(QDialog):
    """DiÃ¡logo para exibir detalhes completos do professor"""

    def __init__(self, parent=None, id_professor=None):
        super().__init__(parent)
        self.id_professor = id_professor
        self.db = DatabaseManager()

        self.setWindowTitle("Detalhes do Professor")
        self.setFixedSize(900, 700)
        self.setStyleSheet(GLOBAL_STYLESHEET)

        self.init_ui()
        self.carregar_detalhes_professor()

    def init_ui(self):
        """Inicializa a interface do diÃ¡logo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # CabeÃ§alho com nome do professor
        self.lbl_nome_professor = QLabel()
        self.lbl_nome_professor.setObjectName("title")
        self.lbl_nome_professor.setStyleSheet("""
            QLabel#title {
                font-size: 22px;
                font-weight: 700;
                color: #2c3e50;
                text-align: center;
                padding: 15px;
                background-color: #e8f6f3;
                border-radius: 8px;
                border: 2px solid #27ae60;
            }
        """)

        # Abas para diferentes informaÃ§Ãµes
        tab_widget = QTabWidget()

        # Aba: InformaÃ§Ãµes Pessoais
        aba_info = QWidget()
        self.layout_info = QFormLayout(aba_info)
        self.layout_info.setContentsMargins(20, 20, 20, 20)
        self.layout_info.setSpacing(10)

        # Aba: Disciplinas Ministradas
        aba_disciplinas = QWidget()
        layout_disciplinas = QVBoxLayout(aba_disciplinas)

        self.tabela_disciplinas = QTableWidget()
        self.tabela_disciplinas.setColumnCount(5)
        self.tabela_disciplinas.setHorizontalHeaderLabels([
            "CÃ³digo", "Disciplina", "SÃ©rie", "Carga HorÃ¡ria", "Status"
        ])

        layout_disciplinas.addWidget(QLabel("Disciplinas Ministradas:"))
        layout_disciplinas.addWidget(self.tabela_disciplinas)

        # Aba: HorÃ¡rios
        aba_horarios = QWidget()
        layout_horarios = QVBoxLayout(aba_horarios)

        self.tabela_horarios = QTableWidget()
        self.tabela_horarios.setColumnCount(6)
        self.tabela_horarios.setHorizontalHeaderLabels([
            "Dia", "HorÃ¡rio", "Disciplina", "Turma", "Sala", "Status"
        ])

        layout_horarios.addWidget(QLabel("HorÃ¡rios de Aula:"))
        layout_horarios.addWidget(self.tabela_horarios)

        # Adicionar abas
        tab_widget.addTab(aba_info, "InformaÃ§Ãµes")
        tab_widget.addTab(aba_disciplinas, "Disciplinas")
        tab_widget.addTab(aba_horarios, "HorÃ¡rios")

        # BotÃµes
        botoes_layout = QHBoxLayout()

        btn_fechar = AnimacaoBotao("FECHAR", cor_normal="#7f8c8d", cor_hover="#95a5a6", cor_press="#5d6d7e")
        btn_fechar.clicked.connect(self.close)

        btn_editar = AnimacaoBotao("EDITAR", cor_normal="#3498db", cor_hover="#2980b9", cor_press="#1c6ea4")
        btn_editar.clicked.connect(self.editar_professor)

        botoes_layout.addWidget(btn_editar)
        botoes_layout.addStretch()
        botoes_layout.addWidget(btn_fechar)

        # Adicionar tudo ao layout
        layout.addWidget(self.lbl_nome_professor)
        layout.addWidget(tab_widget)
        layout.addLayout(botoes_layout)

    def carregar_detalhes_professor(self):
        """Carrega detalhes completos do professor"""
        try:
            # Carregar informaÃ§Ãµes bÃ¡sicas
            professor = self.db.execute_query(
                "SELECT * FROM professores WHERE id = ?",
                (self.id_professor,),
                fetch=True
            )

            if professor and len(professor) > 0:
                dados = professor[0]

                # Atualizar tÃ­tulo
                self.lbl_nome_professor.setText(dados[1])

                # Adicionar informaÃ§Ãµes pessoais
                self.adicionar_info("CPF:", ValidadorCampos.formatar_cpf(dados[2]) if dados[2] else "NÃ£o informado")
                self.adicionar_info("Telefone:",
                                    ValidadorCampos.formatar_telefone(dados[3]) if dados[3] else "NÃ£o informado")
                self.adicionar_info("Email:", dados[4] if dados[4] else "NÃ£o informado")
                self.adicionar_info("MatÃ©ria Principal:", dados[5] if dados[5] else "NÃ£o informado")
                self.adicionar_info("FormaÃ§Ã£o:", dados[6] if dados[6] else "NÃ£o informado")

                if dados[7]:  # Data contrataÃ§Ã£o
                    data_contr = datetime.strptime(dados[7], '%Y-%m-%d').strftime('%d/%m/%Y')
                    tempo_servico = self.calcular_tempo_servico(dados[7])
                    self.adicionar_info("Data ContrataÃ§Ã£o:", f"{data_contr} ({tempo_servico})")
                else:
                    self.adicionar_info("Data ContrataÃ§Ã£o:", "NÃ£o informada")

                if dados[8]:  # SalÃ¡rio
                    salario_formatado = f"R$ {float(dados[8]):,.2f}".replace(',', 'X').replace('.', ',').replace('X',
                                                                                                                 '.')
                    self.adicionar_info("SalÃ¡rio:", salario_formatado)
                else:
                    self.adicionar_info("SalÃ¡rio:", "NÃ£o informado")

                self.adicionar_info("EndereÃ§o:", dados[9] if dados[9] else "NÃ£o informado")
                self.adicionar_info("ObservaÃ§Ãµes:", dados[10] if dados[10] else "Nenhuma")

                status = "Ativo" if dados[11] == 1 else "Inativo"
                status_cor = "#27ae60" if dados[11] == 1 else "#e74c3c"
                self.adicionar_info_colorido("Status:", status, status_cor)

                # Carregar disciplinas
                self.carregar_disciplinas_professor()

                # Carregar horÃ¡rios
                self.carregar_horarios_professor()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar detalhes do professor:\n{str(e)}")

    def adicionar_info(self, label, valor):
        """Adiciona uma linha de informaÃ§Ã£o ao formulÃ¡rio"""
        lbl_label = QLabel(label)
        lbl_label.setStyleSheet("font-weight: 600; color: #2c3e50;")

        lbl_valor = QLabel(valor)
        lbl_valor.setStyleSheet("color: #34495e;")

        self.layout_info.addRow(lbl_label, lbl_valor)

    def adicionar_info_colorido(self, label, valor, cor):
        """Adiciona uma linha de informaÃ§Ã£o com cor especÃ­fica"""
        lbl_label = QLabel(label)
        lbl_label.setStyleSheet("font-weight: 600; color: #2c3e50;")

        lbl_valor = QLabel(valor)
        lbl_valor.setStyleSheet(f"color: {cor}; font-weight: 600;")

        self.layout_info.addRow(lbl_label, lbl_valor)

    def calcular_tempo_servico(self, data_contratacao):
        """Calcula tempo de serviÃ§o a partir da data de contrataÃ§Ã£o"""
        try:
            contrato = datetime.strptime(data_contratacao, '%Y-%m-%d')
            hoje = datetime.now()

            anos = hoje.year - contrato.year
            meses = hoje.month - contrato.month

            if meses < 0:
                anos -= 1
                meses += 12

            if anos > 0:
                return f"{anos} ano{'s' if anos > 1 else ''}"
            else:
                return f"{meses} mes{'es' if meses > 1 else ''}"
        except:
            return "NÃ£o calculado"

    def carregar_disciplinas_professor(self):
        """Carrega disciplinas ministradas pelo professor"""
        try:
            disciplinas = self.db.execute_query('''
                SELECT codigo, nome, serie, carga_horaria, ativa
                FROM disciplinas
                WHERE professor_id = ?
                ORDER BY serie, nome
            ''', (self.id_professor,), fetch=True)

            self.tabela_disciplinas.setRowCount(len(disciplinas))

            for row, (codigo, nome, serie, carga_horaria, ativa) in enumerate(disciplinas):
                self.tabela_disciplinas.setItem(row, 0, QTableWidgetItem(codigo if codigo else "-"))
                self.tabela_disciplinas.setItem(row, 1, QTableWidgetItem(nome))
                self.tabela_disciplinas.setItem(row, 2, QTableWidgetItem(serie if serie else "Geral"))

                item_carga = QTableWidgetItem(str(carga_horaria) if carga_horaria else "-")
                self.tabela_disciplinas.setItem(row, 3, item_carga)

                status = "Ativa" if ativa == 1 else "Inativa"
                item_status = QTableWidgetItem(status)

                if ativa == 1:
                    item_status.setForeground(QColor('#27ae60'))
                    item_status.setFont(QFont('', weight=QFont.Bold))
                else:
                    item_status.setForeground(QColor('#e74c3c'))

                self.tabela_disciplinas.setItem(row, 4, item_status)

        except Exception as e:
            print(f"Erro ao carregar disciplinas: {e}")

    def carregar_horarios_professor(self):
        """Carrega horÃ¡rios do professor"""
        try:
            horarios = self.db.execute_query('''
                SELECT h.dia_semana, h.hora_inicio, h.hora_fim, 
                       d.nome, t.nome, h.sala, h.ativo
                FROM horarios h
                JOIN disciplinas d ON h.disciplina_id = d.id
                JOIN turmas t ON h.turma_id = t.id
                WHERE h.professor_id = ?
                ORDER BY 
                    CASE h.dia_semana
                        WHEN 'Segunda' THEN 1
                        WHEN 'TerÃ§a' THEN 2
                        WHEN 'Quarta' THEN 3
                        WHEN 'Quinta' THEN 4
                        WHEN 'Sexta' THEN 5
                        WHEN 'SÃ¡bado' THEN 6
                        ELSE 7
                    END,
                    h.hora_inicio
            ''', (self.id_professor,), fetch=True)

            self.tabela_horarios.setRowCount(len(horarios))

            for row, (dia, inicio, fim, disciplina, turma, sala, ativo) in enumerate(horarios):
                self.tabela_horarios.setItem(row, 0, QTableWidgetItem(dia))

                # Formatar horÃ¡rio
                horario_formatado = f"{inicio} - {fim}" if inicio and fim else "NÃ£o definido"
                self.tabela_horarios.setItem(row, 1, QTableWidgetItem(horario_formatado))

                self.tabela_horarios.setItem(row, 2, QTableWidgetItem(disciplina))
                self.tabela_horarios.setItem(row, 3, QTableWidgetItem(turma))
                self.tabela_horarios.setItem(row, 4, QTableWidgetItem(sala if sala else "-"))

                status = "Ativo" if ativo == 1 else "Inativo"
                item_status = QTableWidgetItem(status)

                if ativo == 1:
                    item_status.setForeground(QColor('#27ae60'))
                else:
                    item_status.setForeground(QColor('#e74c3c'))

                self.tabela_horarios.setItem(row, 5, item_status)

        except Exception as e:
            print(f"Erro ao carregar horÃ¡rios: {e}")

    def editar_professor(self):
        """Abre diÃ¡logo para editar o professor"""
        self.close()
        # Em uma implementaÃ§Ã£o real, aqui abriria o diÃ¡logo de ediÃ§Ã£o


# ============================================
# DIÃLOGO DE HORÃRIOS DO PROFESSOR
# ============================================

class HorariosProfessorDialog(QDialog):
    """DiÃ¡logo para visualizaÃ§Ã£o e gerenciamento de horÃ¡rios do professor"""

    def __init__(self, parent=None, id_professor=None, nome_professor=""):
        super().__init__(parent)
        self.id_professor = id_professor
        self.nome_professor = nome_professor
        self.db = DatabaseManager()

        self.setWindowTitle(f"HorÃ¡rios - {nome_professor}")
        self.setFixedSize(1000, 700)
        self.setStyleSheet(GLOBAL_STYLESHEET)

        self.init_ui()
        self.carregar_horarios()

    def init_ui(self):
        """Inicializa a interface do diÃ¡logo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # CabeÃ§alho
        cabecalho_layout = QHBoxLayout()

        lbl_titulo = QLabel(f"HORÃRIOS DE AULA - {self.nome_professor.upper()}")
        lbl_titulo.setObjectName("title")

        # Filtros
        filtros_layout = QHBoxLayout()

        lbl_dia = QLabel("Dia da semana:")
        self.combo_dia = QComboBox()
        self.combo_dia.addItems(["Todos", "Segunda", "TerÃ§a", "Quarta", "Quinta", "Sexta", "SÃ¡bado"])
        self.combo_dia.currentIndexChanged.connect(self.filtrar_horarios)

        lbl_status = QLabel("Status:")
        self.combo_status = QComboBox()
        self.combo_status.addItems(["Todos", "Ativos", "Inativos"])
        self.combo_status.currentIndexChanged.connect(self.filtrar_horarios)

        filtros_layout.addWidget(lbl_dia)
        filtros_layout.addWidget(self.combo_dia)
        filtros_layout.addWidget(lbl_status)
        filtros_layout.addWidget(self.combo_status)
        filtros_layout.addStretch()

        # BotÃµes de aÃ§Ã£o
        btn_novo = AnimacaoBotao("Novo HorÃ¡rio", cor_normal="#27ae60", cor_hover="#219653", cor_press="#1e874b")
        btn_novo.clicked.connect(self.novo_horario)

        btn_editar = AnimacaoBotao("Editar", cor_normal="#3498db", cor_hover="#2980b9", cor_press="#1c6ea4")
        btn_editar.clicked.connect(self.editar_horario)

        btn_excluir = AnimacaoBotao("Excluir", cor_normal="#e74c3c", cor_hover="#c0392b", cor_press="#a93226")
        btn_excluir.clicked.connect(self.excluir_horario)

        # Tabela de horÃ¡rios
        self.tabela_horarios = QTableWidget()
        self.tabela_horarios.setColumnCount(8)
        self.tabela_horarios.setHorizontalHeaderLabels([
            "ID", "Dia", "HorÃ¡rio", "Disciplina", "Turma", "Sala", "Status", "AÃ§Ãµes"
        ])

        # Configurar tabela
        self.tabela_horarios.setAlternatingRowColors(True)
        self.tabela_horarios.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela_horarios.setSelectionMode(QTableWidget.SingleSelection)
        self.tabela_horarios.setEditTriggers(QTableWidget.NoEditTriggers)

        # Ocultar coluna ID
        self.tabela_horarios.setColumnHidden(0, True)

        # Ajustar largura das colunas
        header = self.tabela_horarios.horizontalHeader()
        header.setSectionResizeMode(3, QHeaderView.Stretch)  # Disciplina
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)  # AÃ§Ãµes

        # Resumo
        self.lbl_resumo = QLabel()
        self.lbl_resumo.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #2c3e50;
                font-weight: 600;
                padding: 10px;
                background-color: #f8f9fa;
                border-radius: 6px;
                border: 1px solid #dce1e6;
            }
        """)

        # BotÃµes inferiores
        botoes_layout = QHBoxLayout()

        btn_imprimir = AnimacaoBotao("Imprimir Grade", cor_normal="#f39c12", cor_hover="#d68910", cor_press="#b9770e")
        btn_imprimir.clicked.connect(self.imprimir_grade)

        btn_fechar = QPushButton("FECHAR")
        btn_fechar.setObjectName("danger")
        btn_fechar.clicked.connect(self.close)

        botoes_layout.addWidget(btn_imprimir)
        botoes_layout.addStretch()
        botoes_layout.addWidget(btn_fechar)

        # Montar layout
        cabecalho_layout.addWidget(lbl_titulo)
        cabecalho_layout.addStretch()
        cabecalho_layout.addWidget(btn_novo)
        cabecalho_layout.addWidget(btn_editar)
        cabecalho_layout.addWidget(btn_excluir)

        layout.addLayout(cabecalho_layout)
        layout.addLayout(filtros_layout)
        layout.addWidget(self.tabela_horarios)
        layout.addWidget(self.lbl_resumo)
        layout.addLayout(botoes_layout)

    def carregar_horarios(self):
        """Carrega todos os horÃ¡rios do professor"""
        try:
            self.horarios_completos = self.db.execute_query('''
                SELECT h.id, h.dia_semana, h.hora_inicio, h.hora_fim, 
                       d.nome as disciplina, t.nome as turma, 
                       h.sala, h.ativo
                FROM horarios h
                JOIN disciplinas d ON h.disciplina_id = d.id
                JOIN turmas t ON h.turma_id = t.id
                WHERE h.professor_id = ?
                ORDER BY 
                    CASE h.dia_semana
                        WHEN 'Segunda' THEN 1
                        WHEN 'TerÃ§a' THEN 2
                        WHEN 'Quarta' THEN 3
                        WHEN 'Quinta' THEN 4
                        WHEN 'Sexta' THEN 5
                        WHEN 'SÃ¡bado' THEN 6
                        ELSE 7
                    END,
                    h.hora_inicio
            ''', (self.id_professor,), fetch=True)

            self.aplicar_filtros()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar horÃ¡rios:\n{str(e)}")

    def aplicar_filtros(self):
        """Aplica filtros aos horÃ¡rios"""
        if not self.horarios_completos:
            self.tabela_horarios.setRowCount(0)
            self.lbl_resumo.setText("Nenhum horÃ¡rio encontrado.")
            return

        # Filtrar por dia
        dia_filtro = self.combo_dia.currentText()
        status_filtro = self.combo_status.currentText()

        horarios_filtrados = []

        for horario in self.horarios_completos:
            id_horario, dia, inicio, fim, disciplina, turma, sala, ativo = horario

            # Aplicar filtro de dia
            if dia_filtro != "Todos" and dia != dia_filtro:
                continue

            # Aplicar filtro de status
            status_texto = "Ativo" if ativo == 1 else "Inativo"
            if status_filtro == "Ativos" and ativo != 1:
                continue
            elif status_filtro == "Inativos" and ativo != 0:
                continue

            horarios_filtrados.append(horario)

        # Atualizar tabela
        self.tabela_horarios.setRowCount(len(horarios_filtrados))

        for row, (id_horario, dia, inicio, fim, disciplina, turma, sala, ativo) in enumerate(horarios_filtrados):
            # ID (oculto)
            self.tabela_horarios.setItem(row, 0, QTableWidgetItem(str(id_horario)))

            # Dia
            self.tabela_horarios.setItem(row, 1, QTableWidgetItem(dia))

            # HorÃ¡rio
            horario_formatado = f"{inicio} - {fim}" if inicio and fim else "NÃ£o definido"
            self.tabela_horarios.setItem(row, 2, QTableWidgetItem(horario_formatado))

            # Disciplina
            self.tabela_horarios.setItem(row, 3, QTableWidgetItem(disciplina))

            # Turma
            self.tabela_horarios.setItem(row, 4, QTableWidgetItem(turma))

            # Sala
            self.tabela_horarios.setItem(row, 5, QTableWidgetItem(sala if sala else "-"))

            # Status
            status = "Ativo" if ativo == 1 else "Inativo"
            item_status = QTableWidgetItem(status)

            if ativo == 1:
                item_status.setForeground(QColor('#27ae60'))
                item_status.setFont(QFont('', weight=QFont.Bold))
            else:
                item_status.setForeground(QColor('#e74c3c'))

            self.tabela_horarios.setItem(row, 6, item_status)

            # BotÃµes de aÃ§Ã£o
            widget_acoes = QWidget()
            layout_acoes = QHBoxLayout(widget_acoes)
            layout_acoes.setContentsMargins(5, 2, 5, 2)
            layout_acoes.setSpacing(5)

            btn_ativar = QPushButton("Ativar" if ativo == 0 else "Desativar")
            btn_ativar.setFixedSize(80, 25)
            btn_ativar.setObjectName("warning" if ativo == 1 else "success")
            btn_ativar.clicked.connect(lambda checked, id=id_horario: self.toggle_status_horario(id))

            layout_acoes.addWidget(btn_ativar)
            widget_acoes.setLayout(layout_acoes)

            self.tabela_horarios.setCellWidget(row, 7, widget_acoes)

        # Atualizar resumo
        total = len(horarios_filtrados)
        ativos = sum(1 for h in horarios_filtrados if h[7] == 1)
        horas_semana = self.calcular_horas_semana(horarios_filtrados)

        self.lbl_resumo.setText(
            f"Total de horÃ¡rios: {total} | "
            f"Ativos: {ativos} | "
            f"Inativos: {total - ativos} | "
            f"Carga horÃ¡ria semanal: {horas_semana} horas"
        )

    def filtrar_horarios(self):
        """Aplica filtros quando selecionados"""
        self.aplicar_filtros()

    def calcular_horas_semana(self, horarios):
        """Calcula a carga horÃ¡ria semanal total"""
        total_minutos = 0

        for horario in horarios:
            inicio = horario[2]  # hora_inicio
            fim = horario[3]  # hora_fim

            if inicio and fim:
                try:
                    # Converter strings HH:MM para minutos
                    h1, m1 = map(int, inicio.split(':'))
                    h2, m2 = map(int, fim.split(':'))

                    minutos = (h2 * 60 + m2) - (h1 * 60 + m1)
                    if minutos > 0:
                        total_minutos += minutos
                except:
                    continue

        horas = total_minutos // 60
        minutos = total_minutos % 60

        return f"{horas}:{minutos:02d}"

    def novo_horario(self):
        """Abre diÃ¡logo para criar novo horÃ¡rio"""
        dialog = CadastroHorarioDialog(self, self.id_professor)
        if dialog.exec_():
            self.carregar_horarios()

    def editar_horario(self):
        """Abre diÃ¡logo para editar horÃ¡rio selecionado"""
        selecionados = self.tabela_horarios.selectedItems()

        if not selecionados:
            QMessageBox.warning(self, "SeleÃ§Ã£o necessÃ¡ria",
                                "Por favor, selecione um horÃ¡rio para editar.")
            return

        id_horario = int(self.tabela_horarios.item(selecionados[0].row(), 0).text())

        dialog = CadastroHorarioDialog(self, self.id_professor, id_horario)
        if dialog.exec_():
            self.carregar_horarios()

    def excluir_horario(self):
        """Exclui horÃ¡rio selecionado"""
        selecionados = self.tabela_horarios.selectedItems()

        if not selecionados:
            QMessageBox.warning(self, "SeleÃ§Ã£o necessÃ¡ria",
                                "Por favor, selecione um horÃ¡rio para excluir.")
            return

        id_horario = int(self.tabela_horarios.item(selecionados[0].row(), 0).text())

        resposta = QMessageBox.question(
            self, "Confirmar exclusÃ£o",
            "Tem certeza que deseja excluir este horÃ¡rio?\n\n"
            "Esta aÃ§Ã£o nÃ£o pode ser desfeita.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            try:
                self.db.execute_query(
                    "DELETE FROM horarios WHERE id = ?",
                    (id_horario,)
                )

                QMessageBox.information(self, "Sucesso", "HorÃ¡rio excluÃ­do com sucesso!")
                self.carregar_horarios()

            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Falha ao excluir horÃ¡rio:\n{str(e)}")

    def toggle_status_horario(self, id_horario):
        """Alterna status do horÃ¡rio (ativo/inativo)"""
        try:
            # Obter status atual
            resultado = self.db.execute_query(
                "SELECT ativo FROM horarios WHERE id = ?",
                (id_horario,),
                fetch=True
            )

            if resultado:
                novo_status = 0 if resultado[0][0] == 1 else 1

                self.db.execute_query(
                    "UPDATE horarios SET ativo = ? WHERE id = ?",
                    (novo_status, id_horario)
                )

                status_text = "ativado" if novo_status == 1 else "desativado"
                QMessageBox.information(self, "Sucesso", f"HorÃ¡rio {status_text} com sucesso!")
                self.carregar_horarios()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao alterar status do horÃ¡rio:\n{str(e)}")

    def imprimir_grade(self):
        """Imprime grade de horÃ¡rios do professor"""
        QMessageBox.information(self, "Funcionalidade em desenvolvimento",
                                "A impressÃ£o da grade de horÃ¡rios serÃ¡ implementada na prÃ³xima versÃ£o.")


"""
PROJETO ESCOLA - SISTEMA DE GESTÃƒO ESCOLAR
Parte 3/10 - ContinuaÃ§Ã£o: Disciplinas, Turmas e Cadastro de HorÃ¡rios
"""


# ============================================
# DIÃLOGO DE CADASTRO DE HORÃRIO
# ============================================

class CadastroHorarioDialog(QDialog):
    """DiÃ¡logo para cadastro/ediÃ§Ã£o de horÃ¡rios"""

    def __init__(self, parent=None, id_professor=None, id_horario=None):
        super().__init__(parent)
        self.id_professor = id_professor
        self.id_horario = id_horario
        self.db = DatabaseManager()
        self.modo_edicao = id_horario is not None

        self.setWindowTitle("Cadastrar HorÃ¡rio" if not self.modo_edicao else "Editar HorÃ¡rio")
        self.setFixedSize(600, 500)
        self.setStyleSheet(GLOBAL_STYLESHEET)

        self.init_ui()
        self.carregar_disciplinas()
        self.carregar_turmas()
        self.carregar_dados_horario() if self.modo_edicao else None

    def init_ui(self):
        """Inicializa a interface do diÃ¡logo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # TÃ­tulo
        titulo = "CADASTRAR NOVO HORÃRIO" if not self.modo_edicao else "EDITAR HORÃRIO"
        lbl_titulo = QLabel(titulo)
        lbl_titulo.setObjectName("title")

        # FormulÃ¡rio
        form_layout = QFormLayout()
        form_layout.setContentsMargins(10, 10, 10, 10)
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)

        # Dia da semana
        self.combo_dia = QComboBox()
        self.combo_dia.addItems(["Segunda", "TerÃ§a", "Quarta", "Quinta", "Sexta", "SÃ¡bado"])

        # HorÃ¡rio de inÃ­cio
        self.time_inicio = QTimeEdit()
        self.time_inicio.setDisplayFormat("HH:mm")
        self.time_inicio.setTime(QTime(7, 0))  # 07:00 padrÃ£o

        # HorÃ¡rio de fim
        self.time_fim = QTimeEdit()
        self.time_fim.setDisplayFormat("HH:mm")
        self.time_fim.setTime(QTime(8, 0))  # 08:00 padrÃ£o

        # Disciplina
        self.combo_disciplina = QComboBox()

        # Turma
        self.combo_turma = QComboBox()

        # Sala
        self.txt_sala = QLineEdit()
        self.txt_sala.setPlaceholderText("Ex: Sala 101, LaboratÃ³rio 2")

        # Status
        self.combo_status = QComboBox()
        self.combo_status.addItems(["Ativo", "Inativo"])

        # Adicionar campos ao formulÃ¡rio
        form_layout.addRow("Dia da semana:", self.combo_dia)

        horario_layout = QHBoxLayout()
        horario_layout.addWidget(self.time_inicio)
        horario_layout.addWidget(QLabel("atÃ©"))
        horario_layout.addWidget(self.time_fim)
        form_layout.addRow("HorÃ¡rio:", horario_layout)

        form_layout.addRow("Disciplina:", self.combo_disciplina)
        form_layout.addRow("Turma:", self.combo_turma)
        form_layout.addRow("Sala:", self.txt_sala)
        form_layout.addRow("Status:", self.combo_status)

        # ValidaÃ§Ã£o de horÃ¡rio
        self.lbl_validacao = QLabel()
        self.lbl_validacao.setStyleSheet("color: #e74c3c; font-weight: 600;")
        self.lbl_validacao.setVisible(False)

        # Conectar validaÃ§Ã£o de horÃ¡rio
        self.time_inicio.timeChanged.connect(self.validar_horario)
        self.time_fim.timeChanged.connect(self.validar_horario)

        # BotÃµes
        botoes_layout = QHBoxLayout()

        self.btn_salvar = AnimacaoBotao(
            "SALVAR" if not self.modo_edicao else "ATUALIZAR",
            cor_normal="#27ae60", cor_hover="#219653", cor_press="#1e874b"
        )
        self.btn_salvar.setMinimumHeight(45)
        self.btn_salvar.clicked.connect(self.salvar_horario)

        self.btn_cancelar = QPushButton("CANCELAR")
        self.btn_cancelar.setObjectName("danger")
        self.btn_cancelar.setMinimumHeight(45)
        self.btn_cancelar.clicked.connect(self.reject)

        if self.modo_edicao:
            self.btn_excluir = QPushButton("EXCLUIR")
            self.btn_excluir.setObjectName("warning")
            self.btn_excluir.setMinimumHeight(45)
            self.btn_excluir.clicked.connect(self.excluir_horario)
            botoes_layout.addWidget(self.btn_excluir)

        botoes_layout.addStretch()
        botoes_layout.addWidget(self.btn_salvar)
        botoes_layout.addWidget(self.btn_cancelar)

        # Adicionar tudo ao layout principal
        layout.addWidget(lbl_titulo)
        layout.addLayout(form_layout)
        layout.addWidget(self.lbl_validacao)
        layout.addStretch()
        layout.addLayout(botoes_layout)

    def carregar_disciplinas(self):
        """Carrega disciplinas do professor no combobox"""
        try:
            disciplinas = self.db.execute_query('''
                SELECT id, nome, serie 
                FROM disciplinas 
                WHERE professor_id = ? AND ativa = 1
                ORDER BY nome
            ''', (self.id_professor,), fetch=True)

            self.combo_disciplina.clear()

            for id_disciplina, nome, serie in disciplinas:
                texto = f"{nome} ({serie})" if serie else nome
                self.combo_disciplina.addItem(texto, id_disciplina)

            if self.combo_disciplina.count() == 0:
                self.combo_disciplina.addItem("Nenhuma disciplina disponÃ­vel", -1)
                self.combo_disciplina.setEnabled(False)

        except Exception as e:
            print(f"Erro ao carregar disciplinas: {e}")

    def carregar_turmas(self):
        """Carrega turmas disponÃ­veis no combobox"""
        try:
            turmas = self.db.execute_query('''
                SELECT id, nome, serie 
                FROM turmas 
                WHERE ativa = 1
                ORDER BY serie, nome
            ''', fetch=True)

            self.combo_turma.clear()

            for id_turma, nome, serie in turmas:
                texto = f"{nome} - {serie}" if serie else nome
                self.combo_turma.addItem(texto, id_turma)

            if self.combo_turma.count() == 0:
                self.combo_turma.addItem("Nenhuma turma disponÃ­vel", -1)
                self.combo_turma.setEnabled(False)

        except Exception as e:
            print(f"Erro ao carregar turmas: {e}")

    def carregar_dados_horario(self):
        """Carrega dados do horÃ¡rio para ediÃ§Ã£o"""
        try:
            horario = self.db.execute_query('''
                SELECT dia_semana, hora_inicio, hora_fim, 
                       disciplina_id, turma_id, sala, ativo
                FROM horarios 
                WHERE id = ?
            ''', (self.id_horario,), fetch=True)

            if horario and len(horario) > 0:
                dados = horario[0]

                # Dia da semana
                index = self.combo_dia.findText(dados[0])
                if index >= 0:
                    self.combo_dia.setCurrentIndex(index)

                # HorÃ¡rios
                if dados[1]:  # hora_inicio
                    try:
                        horas, minutos = map(int, dados[1].split(':'))
                        self.time_inicio.setTime(QTime(horas, minutos))
                    except:
                        pass

                if dados[2]:  # hora_fim
                    try:
                        horas, minutos = map(int, dados[2].split(':'))
                        self.time_fim.setTime(QTime(horas, minutos))
                    except:
                        pass

                # Disciplina
                for i in range(self.combo_disciplina.count()):
                    if self.combo_disciplina.itemData(i) == dados[3]:
                        self.combo_disciplina.setCurrentIndex(i)
                        break

                # Turma
                for i in range(self.combo_turma.count()):
                    if self.combo_turma.itemData(i) == dados[4]:
                        self.combo_turma.setCurrentIndex(i)
                        break

                # Sala
                self.txt_sala.setText(dados[5] if dados[5] else "")

                # Status
                self.combo_status.setCurrentIndex(0 if dados[6] == 1 else 1)

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar dados do horÃ¡rio:\n{str(e)}")

    def validar_horario(self):
        """Valida se o horÃ¡rio Ã© vÃ¡lido (inÃ­cio < fim)"""
        inicio = self.time_inicio.time()
        fim = self.time_fim.time()

        if inicio >= fim:
            self.lbl_validacao.setText("ERRO: HorÃ¡rio de inÃ­cio deve ser anterior ao horÃ¡rio de fim.")
            self.lbl_validacao.setVisible(True)
            self.btn_salvar.setEnabled(False)
        else:
            self.lbl_validacao.setVisible(False)
            self.btn_salvar.setEnabled(True)

    def validar_campos(self):
        """Valida os campos do formulÃ¡rio"""
        erros = []

        # Verificar disciplina selecionada
        if self.combo_disciplina.currentData() == -1:
            erros.append("Nenhuma disciplina disponÃ­vel para este professor.")

        # Verificar turma selecionada
        if self.combo_turma.currentData() == -1:
            erros.append("Nenhuma turma disponÃ­vel.")

        # Verificar conflito de horÃ¡rio
        if not self.verificar_conflito_horario():
            erros.append("Conflito de horÃ¡rio: JÃ¡ existe um horÃ¡rio para esta turma/disciplina no mesmo perÃ­odo.")

        return erros

    def verificar_conflito_horario(self):
        """Verifica se hÃ¡ conflito com outros horÃ¡rios"""
        try:
            dia = self.combo_dia.currentText()
            inicio = self.time_inicio.time().toString("HH:mm")
            fim = self.time_fim.time().toString("HH:mm")
            turma_id = self.combo_turma.currentData()
            disciplina_id = self.combo_disciplina.currentData()

            # Query para verificar conflitos
            query = '''
                SELECT COUNT(*) 
                FROM horarios 
                WHERE dia_semana = ? 
                  AND turma_id = ? 
                  AND (
                    (hora_inicio <= ? AND hora_fim > ?) OR
                    (hora_inicio < ? AND hora_fim >= ?) OR
                    (hora_inicio >= ? AND hora_fim <= ?)
                  )
                  AND ativo = 1
            '''

            # Para ediÃ§Ã£o, excluir o prÃ³prio horÃ¡rio
            if self.modo_edicao:
                query += " AND id != ?"
                params = (dia, turma_id, inicio, inicio, fim, fim, inicio, fim, self.id_horario)
            else:
                params = (dia, turma_id, inicio, inicio, fim, fim, inicio, fim)

            resultado = self.db.execute_query(query, params, fetch=True)

            if resultado and resultado[0][0] > 0:
                return False

            # Verificar conflito para o professor
            query_professor = '''
                SELECT COUNT(*) 
                FROM horarios 
                WHERE dia_semana = ? 
                  AND professor_id = ? 
                  AND (
                    (hora_inicio <= ? AND hora_fim > ?) OR
                    (hora_inicio < ? AND hora_fim >= ?) OR
                    (hora_inicio >= ? AND hora_fim <= ?)
                  )
                  AND ativo = 1
            '''

            if self.modo_edicao:
                query_professor += " AND id != ?"
                params_prof = (dia, self.id_professor, inicio, inicio, fim, fim, inicio, fim, self.id_horario)
            else:
                params_prof = (dia, self.id_professor, inicio, inicio, fim, fim, inicio, fim)

            resultado_prof = self.db.execute_query(query_professor, params_prof, fetch=True)

            if resultado_prof and resultado_prof[0][0] > 0:
                return False

            return True

        except Exception as e:
            print(f"Erro ao verificar conflito: {e}")
            return True  # Em caso de erro, permite continuar

    def salvar_horario(self):
        """Salva ou atualiza o horÃ¡rio no banco de dados"""
        # Validar campos
        erros = self.validar_campos()
        if erros:
            QMessageBox.warning(self, "Erros no formulÃ¡rio", "\n".join(erros))
            return

        # Validar horÃ¡rio
        if self.time_inicio.time() >= self.time_fim.time():
            QMessageBox.warning(self, "HorÃ¡rio invÃ¡lido",
                                "HorÃ¡rio de inÃ­cio deve ser anterior ao horÃ¡rio de fim.")
            return

        # Preparar dados
        dados = {
            'dia_semana': self.combo_dia.currentText(),
            'hora_inicio': self.time_inicio.time().toString("HH:mm"),
            'hora_fim': self.time_fim.time().toString("HH:mm"),
            'disciplina_id': self.combo_disciplina.currentData(),
            'turma_id': self.combo_turma.currentData(),
            'professor_id': self.id_professor,
            'sala': self.txt_sala.text().strip(),
            'ativo': 1 if self.combo_status.currentText() == "Ativo" else 0
        }

        try:
            if self.modo_edicao:
                # Atualizar horÃ¡rio existente
                query = '''
                    UPDATE horarios SET
                        dia_semana = ?, hora_inicio = ?, hora_fim = ?,
                        disciplina_id = ?, turma_id = ?, professor_id = ?,
                        sala = ?, ativo = ?
                    WHERE id = ?
                '''

                params = (
                    dados['dia_semana'], dados['hora_inicio'], dados['hora_fim'],
                    dados['disciplina_id'], dados['turma_id'], dados['professor_id'],
                    dados['sala'], dados['ativo'], self.id_horario
                )

                self.db.execute_query(query, params)
                QMessageBox.information(self, "Sucesso", "HorÃ¡rio atualizado com sucesso!")

            else:
                # Inserir novo horÃ¡rio
                query = '''
                    INSERT INTO horarios (
                        dia_semana, hora_inicio, hora_fim,
                        disciplina_id, turma_id, professor_id,
                        sala, ativo
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                '''

                params = (
                    dados['dia_semana'], dados['hora_inicio'], dados['hora_fim'],
                    dados['disciplina_id'], dados['turma_id'], dados['professor_id'],
                    dados['sala'], dados['ativo']
                )

                self.db.execute_query(query, params)
                QMessageBox.information(self, "Sucesso", "HorÃ¡rio cadastrado com sucesso!")

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao salvar horÃ¡rio:\n{str(e)}")

    def excluir_horario(self):
        """Exclui o horÃ¡rio atual"""
        resposta = QMessageBox.question(
            self, "Confirmar exclusÃ£o",
            "Tem certeza que deseja excluir este horÃ¡rio?\n\n"
            "Esta aÃ§Ã£o nÃ£o pode ser desfeita.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            try:
                self.db.execute_query(
                    "DELETE FROM horarios WHERE id = ?",
                    (self.id_horario,)
                )

                QMessageBox.information(self, "Sucesso", "HorÃ¡rio excluÃ­do com sucesso!")
                self.accept()

            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Falha ao excluir horÃ¡rio:\n{str(e)}")

    # ============================================
    # PÃGINA DE DISCIPLINAS (COMPLETA)
    # ============================================

    def criar_pagina_disciplinas(self):
        """Cria a pÃ¡gina de gerenciamento de disciplinas - COMPLETA"""
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # CabeÃ§alho
        cabecalho_layout = QHBoxLayout()

        lbl_titulo = QLabel("GESTÃƒO DE DISCIPLINAS")
        lbl_titulo.setObjectName("title")

        # Barra de busca
        self.txt_busca_disciplina = QLineEdit()
        self.txt_busca_disciplina.setPlaceholderText("Buscar disciplina por nome, cÃ³digo ou sÃ©rie...")
        self.txt_busca_disciplina.setMinimumHeight(40)
        self.txt_busca_disciplina.textChanged.connect(self.buscar_disciplinas)

        # BotÃµes de aÃ§Ã£o
        btn_novo = AnimacaoBotao("Nova Disciplina", cor_normal="#27ae60", cor_hover="#219653", cor_press="#1e874b")
        btn_novo.setIcon(self.style().standardIcon(QStyle.SP_FileIcon))
        btn_novo.clicked.connect(self.cadastrar_disciplina)

        btn_editar = AnimacaoBotao("Editar", cor_normal="#3498db", cor_hover="#2980b9", cor_press="#1c6ea4")
        btn_editar.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        btn_editar.clicked.connect(self.editar_disciplina)

        btn_excluir = AnimacaoBotao("Excluir", cor_normal="#e74c3c", cor_hover="#c0392b", cor_press="#a93226")
        btn_excluir.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        btn_excluir.clicked.connect(self.excluir_disciplina)

        btn_associar = AnimacaoBotao("Associar Professor", cor_normal="#9b59b6", cor_hover="#8e44ad",
                                     cor_press="#7d3c98")
        btn_associar.setIcon(self.style().standardIcon(QStyle.SP_FileDialogListView))
        btn_associar.clicked.connect(self.associar_professor_disciplina)

        cabecalho_layout.addWidget(lbl_titulo)
        cabecalho_layout.addStretch()
        cabecalho_layout.addWidget(self.txt_busca_disciplina, 2)
        cabecalho_layout.addWidget(btn_novo)
        cabecalho_layout.addWidget(btn_editar)
        cabecalho_layout.addWidget(btn_excluir)
        cabecalho_layout.addWidget(btn_associar)

        # Tabela de disciplinas
        self.tabela_disciplinas = QTableWidget()
        self.tabela_disciplinas.setColumnCount(8)
        self.tabela_disciplinas.setHorizontalHeaderLabels([
            "ID", "Nome", "CÃ³digo", "SÃ©rie", "Carga HorÃ¡ria", "Professor", "Status", "DescriÃ§Ã£o"
        ])

        # Configurar tabela
        self.tabela_disciplinas.setAlternatingRowColors(True)
        self.tabela_disciplinas.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela_disciplinas.setSelectionMode(QTableWidget.SingleSelection)
        self.tabela_disciplinas.setEditTriggers(QTableWidget.NoEditTriggers)

        # Ajustar largura das colunas
        header = self.tabela_disciplinas.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Nome
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Professor
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)  # DescriÃ§Ã£o

        # Conectar duplo clique
        self.tabela_disciplinas.doubleClicked.connect(self.ver_detalhes_disciplina)

        # Filtros
        filtros_layout = QHBoxLayout()

        lbl_serie = QLabel("Filtrar por sÃ©rie:")
        self.combo_filtro_serie = QComboBox()
        self.combo_filtro_serie.addItem("Todas as sÃ©ries")

        # Carregar sÃ©ries do banco
        series_config = self.db.get_config('series', '1Âº Ano,2Âº Ano,3Âº Ano,4Âº Ano,5Âº Ano')
        if series_config:
            series = series_config.split(',')
            for serie in series:
                self.combo_filtro_serie.addItem(serie.strip())

        self.combo_filtro_serie.currentIndexChanged.connect(self.filtrar_disciplinas_por_serie)

        lbl_status = QLabel("Filtrar por status:")
        self.combo_filtro_status = QComboBox()
        self.combo_filtro_status.addItems(["Todos", "Ativas", "Inativas"])
        self.combo_filtro_status.currentIndexChanged.connect(self.filtrar_disciplinas_por_status)

        filtros_layout.addWidget(lbl_serie)
        filtros_layout.addWidget(self.combo_filtro_serie)
        filtros_layout.addWidget(lbl_status)
        filtros_layout.addWidget(self.combo_filtro_status)
        filtros_layout.addStretch()

        # EstatÃ­sticas
        stats_layout = QHBoxLayout()

        self.lbl_total_disc = QLabel("Total de disciplinas: 0")
        self.lbl_total_disc.setObjectName("info-badge")

        self.lbl_disc_ativas = QLabel("Ativas: 0")
        self.lbl_disc_ativas.setObjectName("success-badge")

        self.lbl_disc_inativas = QLabel("Inativas: 0")
        self.lbl_disc_inativas.setObjectName("danger-badge")

        stats_layout.addWidget(self.lbl_total_disc)
        stats_layout.addWidget(self.lbl_disc_ativas)
        stats_layout.addWidget(self.lbl_disc_inativas)
        stats_layout.addStretch()

        # Adicionar tudo ao layout
        layout.addLayout(cabecalho_layout)
        layout.addLayout(filtros_layout)
        layout.addWidget(self.tabela_disciplinas)
        layout.addLayout(stats_layout)

        self.paginas['disciplinas'] = pagina
        self.central_widget.addWidget(pagina)

        # Carregar dados iniciais
        self.carregar_tabela_disciplinas()

    def carregar_tabela_disciplinas(self):
        """Carrega dados na tabela de disciplinas"""
        try:
            query = """
                SELECT d.id, d.nome, d.codigo, d.serie, d.carga_horaria, 
                       p.nome as professor, d.ativa, d.descricao
                FROM disciplinas d
                LEFT JOIN professores p ON d.professor_id = p.id
                ORDER BY d.serie, d.nome
            """

            disciplinas = self.db.execute_query(query, fetch=True)

            self.tabela_disciplinas.setRowCount(0)
            self.disciplinas_completas = disciplinas  # Salvar para filtragem

            for row_num, disciplina in enumerate(disciplinas):
                self.tabela_disciplinas.insertRow(row_num)

                for col_num, valor in enumerate(disciplina):
                    item = QTableWidgetItem(str(valor if valor else ""))

                    # Colorir status
                    if col_num == 6:  # Coluna ativa
                        if valor == 1:
                            item.setText("Ativa")
                            item.setForeground(QColor('#27ae60'))
                            item.setFont(QFont('', weight=QFont.Bold))
                        else:
                            item.setText("Inativa")
                            item.setForeground(QColor('#e74c3c'))

                    self.tabela_disciplinas.setItem(row_num, col_num, item)

            # Atualizar estatÃ­sticas
            self.atualizar_estatisticas_disciplinas(disciplinas)

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar disciplinas:\n{str(e)}")

    def atualizar_estatisticas_disciplinas(self, disciplinas):
        """Atualiza as estatÃ­sticas de disciplinas"""
        total = len(disciplinas)
        ativas = sum(1 for d in disciplinas if d[6] == 1)
        inativas = total - ativas

        self.lbl_total_disc.setText(f"Total de disciplinas: {total}")
        self.lbl_disc_ativas.setText(f"Ativas: {ativas}")
        self.lbl_disc_inativas.setText(f"Inativas: {inativas}")

    def buscar_disciplinas(self):
        """Busca disciplinas baseado no texto da busca"""
        texto = self.txt_busca_disciplina.text().strip().lower()

        if not self.disciplinas_completas:
            return

        disciplinas_filtradas = []

        for disciplina in self.disciplinas_completas:
            # Verificar se o texto estÃ¡ em algum campo
            match = False

            for campo in disciplina:
                if campo and texto in str(campo).lower():
                    match = True
                    break

            if match:
                disciplinas_filtradas.append(disciplina)

        # Atualizar tabela com resultados filtrados
        self.tabela_disciplinas.setRowCount(0)

        for row_num, disciplina in enumerate(disciplinas_filtradas):
            self.tabela_disciplinas.insertRow(row_num)

            for col_num, valor in enumerate(disciplina):
                item = QTableWidgetItem(str(valor if valor else ""))

                if col_num == 6:  # Status
                    if valor == 1:
                        item.setText("Ativa")
                        item.setForeground(QColor('#27ae60'))
                        item.setFont(QFont('', weight=QFont.Bold))
                    else:
                        item.setText("Inativa")
                        item.setForeground(QColor('#e74c3c'))

                self.tabela_disciplinas.setItem(row_num, col_num, item)

        self.atualizar_estatisticas_disciplinas(disciplinas_filtradas)

    def filtrar_disciplinas_por_serie(self):
        """Filtra disciplinas por sÃ©rie selecionada"""
        serie_filtro = self.combo_filtro_serie.currentText()

        if serie_filtro == "Todas as sÃ©ries" or not self.disciplinas_completas:
            self.carregar_tabela_disciplinas()
            return

        disciplinas_filtradas = []

        for disciplina in self.disciplinas_completas:
            serie = disciplina[3]  # Ãndice da sÃ©rie

            if serie and serie_filtro in str(serie):
                disciplinas_filtradas.append(disciplina)

        # Atualizar tabela
        self.atualizar_tabela_com_disciplinas(disciplinas_filtradas)

    def filtrar_disciplinas_por_status(self):
        """Filtra disciplinas por status selecionado"""
        status_filtro = self.combo_filtro_status.currentText()

        if status_filtro == "Todos" or not self.disciplinas_completas:
            self.carregar_tabela_disciplinas()
            return

        disciplinas_filtradas = []

        for disciplina in self.disciplinas_completas:
            ativa = disciplina[6]  # Ãndice do status

            if status_filtro == "Ativas" and ativa == 1:
                disciplinas_filtradas.append(disciplina)
            elif status_filtro == "Inativas" and ativa == 0:
                disciplinas_filtradas.append(disciplina)

        # Atualizar tabela
        self.atualizar_tabela_com_disciplinas(disciplinas_filtradas)

    def atualizar_tabela_com_disciplinas(self, disciplinas):
        """Atualiza a tabela com a lista de disciplinas fornecida"""
        self.tabela_disciplinas.setRowCount(0)

        for row_num, disciplina in enumerate(disciplinas):
            self.tabela_disciplinas.insertRow(row_num)

            for col_num, valor in enumerate(disciplina):
                item = QTableWidgetItem(str(valor if valor else ""))

                if col_num == 6:  # Status
                    if valor == 1:
                        item.setText("Ativa")
                        item.setForeground(QColor('#27ae60'))
                        item.setFont(QFont('', weight=QFont.Bold))
                    else:
                        item.setText("Inativa")
                        item.setForeground(QColor('#e74c3c'))

                self.tabela_disciplinas.setItem(row_num, col_num, item)

        self.atualizar_estatisticas_disciplinas(disciplinas)

    def cadastrar_disciplina(self):
        """Abre diÃ¡logo para cadastrar nova disciplina"""
        dialog = CadastroDisciplinaDialog(self)
        if dialog.exec_():
            self.carregar_tabela_disciplinas()

    def editar_disciplina(self):
        """Abre diÃ¡logo para editar disciplina selecionada"""
        selecionados = self.tabela_disciplinas.selectedItems()

        if not selecionados:
            QMessageBox.warning(self, "SeleÃ§Ã£o necessÃ¡ria",
                                "Por favor, selecione uma disciplina para editar.")
            return

        id_disciplina = int(self.tabela_disciplinas.item(selecionados[0].row(), 0).text())

        dialog = CadastroDisciplinaDialog(self, id_disciplina)
        if dialog.exec_():
            self.carregar_tabela_disciplinas()

    def excluir_disciplina(self):
        """Exclui disciplina selecionada"""
        selecionados = self.tabela_disciplinas.selectedItems()

        if not selecionados:
            QMessageBox.warning(self, "SeleÃ§Ã£o necessÃ¡ria",
                                "Por favor, selecione uma disciplina para excluir.")
            return

        id_disciplina = int(self.tabela_disciplinas.item(selecionados[0].row(), 0).text())
        nome_disciplina = self.tabela_disciplinas.item(selecionados[0].row(), 1).text()

        resposta = QMessageBox.question(
            self, "Confirmar exclusÃ£o",
            f"Tem certeza que deseja excluir a disciplina '{nome_disciplina}'?\n\n"
            "Esta aÃ§Ã£o nÃ£o pode ser desfeita.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            try:
                # Verificar se a disciplina tem notas associadas
                notas = self.db.execute_query(
                    "SELECT COUNT(*) FROM notas WHERE disciplina_id = ?",
                    (id_disciplina,),
                    fetch=True
                )

                if notas and notas[0][0] > 0:
                    QMessageBox.warning(self, "Disciplina possui notas",
                                        "Esta disciplina possui notas lanÃ§adas.\n"
                                        "NÃ£o Ã© possÃ­vel excluÃ­-la.")
                    return

                # Verificar se a disciplina tem horÃ¡rios associados
                horarios = self.db.execute_query(
                    "SELECT COUNT(*) FROM horarios WHERE disciplina_id = ?",
                    (id_disciplina,),
                    fetch=True
                )

                if horarios and horarios[0][0] > 0:
                    QMessageBox.warning(self, "Disciplina possui horÃ¡rios",
                                        "Esta disciplina possui horÃ¡rios cadastrados.\n"
                                        "Remova os horÃ¡rios primeiro.")
                    return

                self.db.execute_query(
                    "DELETE FROM disciplinas WHERE id = ?",
                    (id_disciplina,)
                )

                QMessageBox.information(self, "Sucesso", "Disciplina excluÃ­da com sucesso!")
                self.carregar_tabela_disciplinas()

            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Falha ao excluir disciplina:\n{str(e)}")

    def ver_detalhes_disciplina(self, index):
        """Mostra detalhes da disciplina em duplo clique"""
        row = index.row()
        id_disciplina = int(self.tabela_disciplinas.item(row, 0).text())

        dialog = DetalhesDisciplinaDialog(self, id_disciplina)
        dialog.exec_()

    def associar_professor_disciplina(self):
        """Associa um professor Ã  disciplina selecionada"""
        selecionados = self.tabela_disciplinas.selectedItems()

        if not selecionados:
            QMessageBox.warning(self, "SeleÃ§Ã£o necessÃ¡ria",
                                "Por favor, selecione uma disciplina para associar um professor.")
            return

        id_disciplina = int(self.tabela_disciplinas.item(selecionados[0].row(), 0).text())
        nome_disciplina = self.tabela_disciplinas.item(selecionados[0].row(), 1).text()

        dialog = AssociarProfessorDialog(self, id_disciplina, nome_disciplina)
        if dialog.exec_():
            self.carregar_tabela_disciplinas()


# ============================================
# DIÃLOGO DE CADASTRO DE DISCIPLINA
# ============================================

class CadastroDisciplinaDialog(QDialog):
    """DiÃ¡logo para cadastro/ediÃ§Ã£o de disciplinas"""

    def __init__(self, parent=None, id_disciplina=None):
        super().__init__(parent)
        self.id_disciplina = id_disciplina
        self.db = DatabaseManager()
        self.modo_edicao = id_disciplina is not None

        self.setWindowTitle("Cadastrar Disciplina" if not self.modo_edicao else "Editar Disciplina")
        self.setFixedSize(600, 500)
        self.setStyleSheet(GLOBAL_STYLESHEET)

        self.init_ui()
        self.carregar_series()
        self.carregar_professores()
        self.carregar_dados_disciplina() if self.modo_edicao else None

    def init_ui(self):
        """Inicializa a interface do diÃ¡logo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # TÃ­tulo
        titulo = "CADASTRAR NOVA DISCIPLINA" if not self.modo_edicao else "EDITAR DISCIPLINA"
        lbl_titulo = QLabel(titulo)
        lbl_titulo.setObjectName("title")

        # FormulÃ¡rio
        form_layout = QFormLayout()
        form_layout.setContentsMargins(10, 10, 10, 10)
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)

        # Nome da disciplina
        self.txt_nome = QLineEdit()
        self.txt_nome.setPlaceholderText("Ex: MatemÃ¡tica, PortuguÃªs, HistÃ³ria")

        # CÃ³digo da disciplina
        self.txt_codigo = QLineEdit()
        self.txt_codigo.setPlaceholderText("Ex: MAT-101, POR-201")

        # SÃ©rie
        self.combo_serie = QComboBox()

        # Carga horÃ¡ria
        self.spin_carga_horaria = QSpinBox()
        self.spin_carga_horaria.setRange(0, 200)
        self.spin_carga_horaria.setSuffix(" horas")
        self.spin_carga_horaria.setValue(40)

        # Professor responsÃ¡vel
        self.combo_professor = QComboBox()
        self.combo_professor.addItem("Nenhum", -1)

        # Status
        self.combo_status = QComboBox()
        self.combo_status.addItems(["Ativa", "Inativa"])

        # DescriÃ§Ã£o
        self.txt_descricao = QTextEdit()
        self.txt_descricao.setMaximumHeight(100)
        self.txt_descricao.setPlaceholderText("DescriÃ§Ã£o da disciplina...")

        # Adicionar campos ao formulÃ¡rio
        form_layout.addRow("Nome da disciplina:", self.txt_nome)
        form_layout.addRow("CÃ³digo:", self.txt_codigo)
        form_layout.addRow("SÃ©rie:", self.combo_serie)
        form_layout.addRow("Carga horÃ¡ria:", self.spin_carga_horaria)
        form_layout.addRow("Professor responsÃ¡vel:", self.combo_professor)
        form_layout.addRow("Status:", self.combo_status)
        form_layout.addRow("DescriÃ§Ã£o:", self.txt_descricao)

        # BotÃµes
        botoes_layout = QHBoxLayout()

        self.btn_salvar = AnimacaoBotao(
            "SALVAR" if not self.modo_edicao else "ATUALIZAR",
            cor_normal="#27ae60", cor_hover="#219653", cor_press="#1e874b"
        )
        self.btn_salvar.setMinimumHeight(45)
        self.btn_salvar.clicked.connect(self.salvar_disciplina)

        self.btn_cancelar = QPushButton("CANCELAR")
        self.btn_cancelar.setObjectName("danger")
        self.btn_cancelar.setMinimumHeight(45)
        self.btn_cancelar.clicked.connect(self.reject)

        if self.modo_edicao:
            self.btn_excluir = QPushButton("EXCLUIR")
            self.btn_excluir.setObjectName("warning")
            self.btn_excluir.setMinimumHeight(45)
            self.btn_excluir.clicked.connect(self.excluir_disciplina)
            botoes_layout.addWidget(self.btn_excluir)

        botoes_layout.addStretch()
        botoes_layout.addWidget(self.btn_salvar)
        botoes_layout.addWidget(self.btn_cancelar)

        # Adicionar tudo ao layout principal
        layout.addWidget(lbl_titulo)
        layout.addLayout(form_layout)
        layout.addStretch()
        layout.addLayout(botoes_layout)

    def carregar_series(self):
        """Carrega sÃ©ries disponÃ­veis no combobox"""
        series_config = self.db.get_config('series', '1Âº Ano,2Âº Ano,3Âº Ano,4Âº Ano,5Âº Ano')

        if series_config:
            series = series_config.split(',')
            for serie in series:
                self.combo_serie.addItem(serie.strip())

        self.combo_serie.addItem("Geral")

    def carregar_professores(self):
        """Carrega professores ativos no combobox"""
        try:
            professores = self.db.execute_query('''
                SELECT id, nome, materia 
                FROM professores 
                WHERE ativo = 1
                ORDER BY nome
            ''', fetch=True)

            for id_professor, nome, materia in professores:
                texto = f"{nome} ({materia})" if materia else nome
                self.combo_professor.addItem(texto, id_professor)

        except Exception as e:
            print(f"Erro ao carregar professores: {e}")

    def carregar_dados_disciplina(self):
        """Carrega dados da disciplina para ediÃ§Ã£o"""
        try:
            disciplina = self.db.execute_query(
                "SELECT * FROM disciplinas WHERE id = ?",
                (self.id_disciplina,),
                fetch=True
            )

            if disciplina and len(disciplina) > 0:
                dados = disciplina[0]

                self.txt_nome.setText(dados[1] if dados[1] else "")
                self.txt_codigo.setText(dados[2] if dados[2] else "")

                # SÃ©rie
                if dados[3]:  # sÃ©rie
                    index = self.combo_serie.findText(dados[3])
                    if index >= 0:
                        self.combo_serie.setCurrentIndex(index)

                if dados[4]:  # carga_horaria
                    self.spin_carga_horaria.setValue(int(dados[4]))

                # Professor
                if dados[5]:  # professor_id
                    for i in range(self.combo_professor.count()):
                        if self.combo_professor.itemData(i) == dados[5]:
                            self.combo_professor.setCurrentIndex(i)
                            break

                self.txt_descricao.setText(dados[6] if dados[6] else "")

                # Status
                self.combo_status.setCurrentIndex(0 if dados[7] == 1 else 1)

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar dados da disciplina:\n{str(e)}")

    def validar_campos(self):
        """Valida os campos do formulÃ¡rio"""
        erros = []

        # Nome obrigatÃ³rio
        if not self.txt_nome.text().strip():
            erros.append("Nome da disciplina Ã© obrigatÃ³rio.")

        # CÃ³digo Ãºnico (se preenchido)
        codigo = self.txt_codigo.text().strip()
        if codigo:
            query = "SELECT COUNT(*) FROM disciplinas WHERE codigo = ?"
            params = [codigo]

            if self.modo_edicao:
                query += " AND id != ?"
                params.append(self.id_disciplina)

            resultado = self.db.execute_query(query, tuple(params), fetch=True)

            if resultado and resultado[0][0] > 0:
                erros.append("CÃ³digo da disciplina jÃ¡ estÃ¡ em uso.")

        return erros

    def salvar_disciplina(self):
        """Salva ou atualiza a disciplina no banco de dados"""
        # Validar campos
        erros = self.validar_campos()
        if erros:
            QMessageBox.warning(self, "Erros no formulÃ¡rio", "\n".join(erros))
            return

        # Preparar dados
        dados = {
            'nome': self.txt_nome.text().strip(),
            'codigo': self.txt_codigo.text().strip(),
            'serie': self.combo_serie.currentText(),
            'carga_horaria': self.spin_carga_horaria.value(),
            'professor_id': self.combo_professor.currentData(),
            'descricao': self.txt_descricao.toPlainText().strip(),
            'ativa': 1 if self.combo_status.currentText() == "Ativa" else 0
        }

        # Se professor_id for -1 (Nenhum), definir como NULL
        if dados['professor_id'] == -1:
            dados['professor_id'] = None

        try:
            if self.modo_edicao:
                # Atualizar disciplina existente
                query = '''
                    UPDATE disciplinas SET
                        nome = ?, codigo = ?, serie = ?, carga_horaria = ?,
                        professor_id = ?, descricao = ?, ativa = ?
                    WHERE id = ?
                '''

                params = (
                    dados['nome'], dados['codigo'], dados['serie'], dados['carga_horaria'],
                    dados['professor_id'], dados['descricao'], dados['ativa'], self.id_disciplina
                )

                self.db.execute_query(query, params)
                QMessageBox.information(self, "Sucesso", "Disciplina atualizada com sucesso!")

            else:
                # Inserir nova disciplina
                query = '''
                    INSERT INTO disciplinas (
                        nome, codigo, serie, carga_horaria,
                        professor_id, descricao, ativa
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                '''

                params = (
                    dados['nome'], dados['codigo'], dados['serie'], dados['carga_horaria'],
                    dados['professor_id'], dados['descricao'], dados['ativa']
                )

                self.db.execute_query(query, params)
                QMessageBox.information(self, "Sucesso", "Disciplina cadastrada com sucesso!")

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao salvar disciplina:\n{str(e)}")

    def excluir_disciplina(self):
        """Exclui a disciplina atual"""
        resposta = QMessageBox.question(
            self, "Confirmar exclusÃ£o",
            "Tem certeza que deseja excluir esta disciplina?\n\n"
            "Esta aÃ§Ã£o nÃ£o pode ser desfeita.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            try:
                self.db.execute_query(
                    "DELETE FROM disciplinas WHERE id = ?",
                    (self.id_disciplina,)
                )

                QMessageBox.information(self, "Sucesso", "Disciplina excluÃ­da com sucesso!")
                self.accept()

            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Falha ao excluir disciplina:\n{str(e)}")


# ============================================
# DIÃLOGO DE DETALHES DA DISCIPLINA
# ============================================

class DetalhesDisciplinaDialog(QDialog):
    """DiÃ¡logo para exibir detalhes completos da disciplina"""

    def __init__(self, parent=None, id_disciplina=None):
        super().__init__(parent)
        self.id_disciplina = id_disciplina
        self.db = DatabaseManager()

        self.setWindowTitle("Detalhes da Disciplina")
        self.setFixedSize(900, 700)
        self.setStyleSheet(GLOBAL_STYLESHEET)

        self.init_ui()
        self.carregar_detalhes_disciplina()

    def init_ui(self):
        """Inicializa a interface do diÃ¡logo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # CabeÃ§alho com nome da disciplina
        self.lbl_nome_disciplina = QLabel()
        self.lbl_nome_disciplina.setObjectName("title")
        self.lbl_nome_disciplina.setStyleSheet("""
            QLabel#title {
                font-size: 22px;
                font-weight: 700;
                color: #2c3e50;
                text-align: center;
                padding: 15px;
                background-color: #fff3cd;
                border-radius: 8px;
                border: 2px solid #f39c12;
            }
        """)

        # Abas para diferentes informaÃ§Ãµes
        tab_widget = QTabWidget()

        # Aba: InformaÃ§Ãµes Gerais
        aba_info = QWidget()
        self.layout_info = QFormLayout(aba_info)
        self.layout_info.setContentsMargins(20, 20, 20, 20)
        self.layout_info.setSpacing(10)

        # Aba: Alunos Matriculados
        aba_alunos = QWidget()
        layout_alunos = QVBoxLayout(aba_alunos)

        self.tabela_alunos = QTableWidget()
        self.tabela_alunos.setColumnCount(5)
        self.tabela_alunos.setHorizontalHeaderLabels([
            "Nome", "Turma", "MÃ©dia", "Faltas", "Status"
        ])

        layout_alunos.addWidget(QLabel("Alunos Matriculados:"))
        layout_alunos.addWidget(self.tabela_alunos)

        # Aba: HorÃ¡rios
        aba_horarios = QWidget()
        layout_horarios = QVBoxLayout(aba_horarios)

        self.tabela_horarios = QTableWidget()
        self.tabela_horarios.setColumnCount(6)
        self.tabela_horarios.setHorizontalHeaderLabels([
            "Dia", "HorÃ¡rio", "Professor", "Turma", "Sala", "Status"
        ])

        layout_horarios.addWidget(QLabel("HorÃ¡rios da Disciplina:"))
        layout_horarios.addWidget(self.tabela_horarios)

        # Adicionar abas
        tab_widget.addTab(aba_info, "InformaÃ§Ãµes")
        tab_widget.addTab(aba_alunos, "Alunos")
        tab_widget.addTab(aba_horarios, "HorÃ¡rios")

        # BotÃµes
        botoes_layout = QHBoxLayout()

        btn_fechar = AnimacaoBotao("FECHAR", cor_normal="#7f8c8d", cor_hover="#95a5a6", cor_press="#5d6d7e")
        btn_fechar.clicked.connect(self.close)

        btn_editar = AnimacaoBotao("EDITAR", cor_normal="#3498db", cor_hover="#2980b9", cor_press="#1c6ea4")
        btn_editar.clicked.connect(self.editar_disciplina)

        botoes_layout.addWidget(btn_editar)
        botoes_layout.addStretch()
        botoes_layout.addWidget(btn_fechar)

        # Adicionar tudo ao layout
        layout.addWidget(self.lbl_nome_disciplina)
        layout.addWidget(tab_widget)
        layout.addLayout(botoes_layout)

    def carregar_detalhes_disciplina(self):
        """Carrega detalhes completos da disciplina"""
        try:
            # Carregar informaÃ§Ãµes bÃ¡sicas
            disciplina = self.db.execute_query(
                "SELECT * FROM disciplinas WHERE id = ?",
                (self.id_disciplina,),
                fetch=True
            )

            if disciplina and len(disciplina) > 0:
                dados = disciplina[0]

                # Atualizar tÃ­tulo
                nome_completo = f"{dados[1]}"
                if dados[2]:  # cÃ³digo
                    nome_completo += f" ({dados[2]})"
                self.lbl_nome_disciplina.setText(nome_completo)

                # Adicionar informaÃ§Ãµes gerais
                self.adicionar_info("CÃ³digo:", dados[2] if dados[2] else "NÃ£o informado")
                self.adicionar_info("SÃ©rie:", dados[3] if dados[3] else "Geral")

                if dados[4]:  # carga horÃ¡ria
                    self.adicionar_info("Carga horÃ¡ria:", f"{dados[4]} horas")
                else:
                    self.adicionar_info("Carga horÃ¡ria:", "NÃ£o informada")

                # Professor responsÃ¡vel
                if dados[5]:  # professor_id
                    professor = self.db.execute_query(
                        "SELECT nome, materia FROM professores WHERE id = ?",
                        (dados[5],),
                        fetch=True
                    )

                    if professor and len(professor) > 0:
                        prof_nome, prof_materia = professor[0]
                        texto_professor = f"{prof_nome}"
                        if prof_materia:
                            texto_professor += f" ({prof_materia})"
                        self.adicionar_info("Professor responsÃ¡vel:", texto_professor)
                    else:
                        self.adicionar_info("Professor responsÃ¡vel:", "NÃ£o atribuÃ­do")
                else:
                    self.adicionar_info("Professor responsÃ¡vel:", "NÃ£o atribuÃ­do")

                self.adicionar_info("DescriÃ§Ã£o:", dados[6] if dados[6] else "Nenhuma descriÃ§Ã£o fornecida.")

                status = "Ativa" if dados[7] == 1 else "Inativa"
                status_cor = "#27ae60" if dados[7] == 1 else "#e74c3c"
                self.adicionar_info_colorido("Status:", status, status_cor)

                # Carregar alunos matriculados
                self.carregar_alunos_disciplina()

                # Carregar horÃ¡rios
                self.carregar_horarios_disciplina()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar detalhes da disciplina:\n{str(e)}")

    def adicionar_info(self, label, valor):
        """Adiciona uma linha de informaÃ§Ã£o ao formulÃ¡rio"""
        lbl_label = QLabel(label)
        lbl_label.setStyleSheet("font-weight: 600; color: #2c3e50;")

        lbl_valor = QLabel(valor)
        lbl_valor.setStyleSheet("color: #34495e;")

        self.layout_info.addRow(lbl_label, lbl_valor)

    def adicionar_info_colorido(self, label, valor, cor):
        """Adiciona uma linha de informaÃ§Ã£o com cor especÃ­fica"""
        lbl_label = QLabel(label)
        lbl_label.setStyleSheet("font-weight: 600; color: #2c3e50;")

        lbl_valor = QLabel(valor)
        lbl_valor.setStyleSheet(f"color: {cor}; font-weight: 600;")

        self.layout_info.addRow(lbl_label, lbl_valor)

    def carregar_alunos_disciplina(self):
        """Carrega alunos matriculados na disciplina"""
        try:
            # Obter alunos que tÃªm notas nesta disciplina
            alunos = self.db.execute_query('''
                SELECT DISTINCT a.nome, a.turma, n.media, n.faltas, a.status
                FROM notas n
                JOIN alunos a ON n.aluno_id = a.id
                WHERE n.disciplina_id = ?
                ORDER BY a.nome
            ''', (self.id_disciplina,), fetch=True)

            self.tabela_alunos.setRowCount(len(alunos))

            for row, (nome, turma, media, faltas, status) in enumerate(alunos):
                self.tabela_alunos.setItem(row, 0, QTableWidgetItem(nome))
                self.tabela_alunos.setItem(row, 1, QTableWidgetItem(turma if turma else "-"))

                # MÃ©dia
                item_media = QTableWidgetItem(f"{media:.1f}" if media else "-")
                if media:
                    if media < 5.0:
                        item_media.setForeground(QColor('#e74c3c'))
                    elif media < 7.0:
                        item_media.setForeground(QColor('#f39c12'))
                    else:
                        item_media.setForeground(QColor('#27ae60'))
                    item_media.setFont(QFont('', weight=QFont.Bold))

                self.tabela_alunos.setItem(row, 2, item_media)

                # Faltas
                self.tabela_alunos.setItem(row, 3, QTableWidgetItem(str(faltas) if faltas else "-"))

                # Status do aluno
                item_status = QTableWidgetItem(status if status else "-")
                if status == "Ativo":
                    item_status.setForeground(QColor('#27ae60'))
                else:
                    item_status.setForeground(QColor('#e74c3c'))

                self.tabela_alunos.setItem(row, 4, item_status)

        except Exception as e:
            print(f"Erro ao carregar alunos: {e}")

    def carregar_horarios_disciplina(self):
        """Carrega horÃ¡rios da disciplina"""
        try:
            horarios = self.db.execute_query('''
                SELECT h.dia_semana, h.hora_inicio, h.hora_fim, 
                       p.nome, t.nome, h.sala, h.ativo
                FROM horarios h
                JOIN professores p ON h.professor_id = p.id
                JOIN turmas t ON h.turma_id = t.id
                WHERE h.disciplina_id = ?
                ORDER BY 
                    CASE h.dia_semana
                        WHEN 'Segunda' THEN 1
                        WHEN 'TerÃ§a' THEN 2
                        WHEN 'Quarta' THEN 3
                        WHEN 'Quinta' THEN 4
                        WHEN 'Sexta' THEN 5
                        WHEN 'SÃ¡bado' THEN 6
                        ELSE 7
                    END,
                    h.hora_inicio
            ''', (self.id_disciplina,), fetch=True)

            self.tabela_horarios.setRowCount(len(horarios))

            for row, (dia, inicio, fim, professor, turma, sala, ativo) in enumerate(horarios):
                self.tabela_horarios.setItem(row, 0, QTableWidgetItem(dia))

                # HorÃ¡rio
                horario_formatado = f"{inicio} - {fim}" if inicio and fim else "NÃ£o definido"
                self.tabela_horarios.setItem(row, 1, QTableWidgetItem(horario_formatado))

                self.tabela_horarios.setItem(row, 2, QTableWidgetItem(professor))
                self.tabela_horarios.setItem(row, 3, QTableWidgetItem(turma))
                self.tabela_horarios.setItem(row, 4, QTableWidgetItem(sala if sala else "-"))

                status = "Ativo" if ativo == 1 else "Inativo"
                item_status = QTableWidgetItem(status)

                if ativo == 1:
                    item_status.setForeground(QColor('#27ae60'))
                else:
                    item_status.setForeground(QColor('#e74c3c'))

                self.tabela_horarios.setItem(row, 5, item_status)

        except Exception as e:
            print(f"Erro ao carregar horÃ¡rios: {e}")

    def editar_disciplina(self):
        """Abre diÃ¡logo para editar a disciplina"""
        self.close()
        # Em uma implementaÃ§Ã£o real, aqui abriria o diÃ¡logo de ediÃ§Ã£o


"""
PROJETO ESCOLA - SISTEMA DE GESTÃƒO ESCOLAR
Parte 4/10 - ContinuaÃ§Ã£o: Associar Professor, Turmas, Notas e FrequÃªncia
"""


# ============================================
# DIÃLOGO DE ASSOCIAR PROFESSOR Ã€ DISCIPLINA
# ============================================

class AssociarProfessorDialog(QDialog):
    """DiÃ¡logo para associar um professor a uma disciplina"""

    def __init__(self, parent=None, id_disciplina=None, nome_disciplina=""):
        super().__init__(parent)
        self.id_disciplina = id_disciplina
        self.nome_disciplina = nome_disciplina
        self.db = DatabaseManager()

        self.setWindowTitle(f"Associar Professor - {nome_disciplina}")
        self.setFixedSize(600, 400)
        self.setStyleSheet(GLOBAL_STYLESHEET)

        self.init_ui()
        self.carregar_professores_disponiveis()

    def init_ui(self):
        """Inicializa a interface do diÃ¡logo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # TÃ­tulo
        lbl_titulo = QLabel(f"ASSOCIAR PROFESSOR Ã€ DISCIPLINA")
        lbl_titulo.setObjectName("title")

        # Nome da disciplina
        lbl_disciplina = QLabel(f"Disciplina: {self.nome_disciplina}")
        lbl_disciplina.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 600;
                color: #2c3e50;
                padding: 10px;
                background-color: #f8f9fa;
                border-radius: 6px;
                border: 1px solid #dce1e6;
            }
        """)

        # Lista de professores disponÃ­veis
        lbl_selecionar = QLabel("Selecione um professor:")
        lbl_selecionar.setStyleSheet("font-weight: 600; color: #2c3e50;")

        self.list_professores = QListWidget()
        self.list_professores.setStyleSheet("""
            QListWidget {
                border: 2px solid #dce1e6;
                border-radius: 6px;
                padding: 5px;
                background-color: white;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #ecf0f1;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: #2c3e50;
                border-radius: 4px;
            }
        """)

        # InformaÃ§Ãµes do professor selecionado
        self.lbl_info_professor = QLabel()
        self.lbl_info_professor.setStyleSheet("""
            QLabel {
                padding: 15px;
                background-color: #e8f6f3;
                border-radius: 6px;
                border: 1px solid #a3e4c0;
                color: #27ae60;
                font-size: 13px;
            }
        """)
        self.lbl_info_professor.setVisible(False)
        self.lbl_info_professor.setWordWrap(True)

        # BotÃµes
        botoes_layout = QHBoxLayout()

        self.btn_associar = AnimacaoBotao("ASSOCIAR PROFESSOR", cor_normal="#27ae60", cor_hover="#219653",
                                          cor_press="#1e874b")
        self.btn_associar.setMinimumHeight(45)
        self.btn_associar.clicked.connect(self.associar_professor)
        self.btn_associar.setEnabled(False)

        btn_remover = AnimacaoBotao("REMOVER ASSOCIAÃ‡ÃƒO", cor_normal="#e74c3c", cor_hover="#c0392b",
                                    cor_press="#a93226")
        btn_remover.setMinimumHeight(45)
        btn_remover.clicked.connect(self.remover_associacao)

        btn_cancelar = QPushButton("CANCELAR")
        btn_cancelar.setObjectName("danger")
        btn_cancelar.setMinimumHeight(45)
        btn_cancelar.clicked.connect(self.reject)

        botoes_layout.addWidget(self.btn_associar)
        botoes_layout.addWidget(btn_remover)
        botoes_layout.addStretch()
        botoes_layout.addWidget(btn_cancelar)

        # Conectar seleÃ§Ã£o de item
        self.list_professores.itemSelectionChanged.connect(self.professor_selecionado)

        # Adicionar tudo ao layout
        layout.addWidget(lbl_titulo)
        layout.addWidget(lbl_disciplina)
        layout.addWidget(lbl_selecionar)
        layout.addWidget(self.list_professores)
        layout.addWidget(self.lbl_info_professor)
        layout.addLayout(botoes_layout)

    def carregar_professores_disponiveis(self):
        """Carrega professores disponÃ­veis para associaÃ§Ã£o"""
        try:
            # Obter professor atual da disciplina
            professor_atual = self.db.execute_query(
                "SELECT professor_id FROM disciplinas WHERE id = ?",
                (self.id_disciplina,),
                fetch=True
            )

            professor_atual_id = professor_atual[0][0] if professor_atual and professor_atual[0][0] else None

            # Obter todos os professores ativos
            professores = self.db.execute_query('''
                SELECT id, nome, materia, telefone, email
                FROM professores 
                WHERE ativo = 1
                ORDER BY nome
            ''', fetch=True)

            self.list_professores.clear()
            self.professores_data = []  # Armazenar dados dos professores

            for id_prof, nome, materia, telefone, email in professores:
                item_text = f"{nome}"
                if materia:
                    item_text += f" - {materia}"

                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, id_prof)

                # Marcar professor atual se existir
                if professor_atual_id and id_prof == professor_atual_id:
                    item.setSelected(True)
                    item.setBackground(QColor('#e3f2fd'))
                    item.setForeground(QColor('#2c3e50'))
                    item.setText(f"âœ“ {item_text} (Atual)")

                    # Mostrar informaÃ§Ãµes do professor atual
                    info = f"Professor atual: {nome}"
                    if materia:
                        info += f" | MatÃ©ria: {materia}"
                    if telefone:
                        info += f" | Telefone: {ValidadorCampos.formatar_telefone(telefone)}"
                    if email:
                        info += f" | Email: {email}"

                    self.lbl_info_professor.setText(info)
                    self.lbl_info_professor.setVisible(True)

                self.list_professores.addItem(item)
                self.professores_data.append((id_prof, nome, materia, telefone, email))

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar professores:\n{str(e)}")

    def professor_selecionado(self):
        """Quando um professor Ã© selecionado na lista"""
        selecionados = self.list_professores.selectedItems()

        if selecionados:
            item = selecionados[0]
            professor_id = item.data(Qt.UserRole)

            # Encontrar dados do professor selecionado
            for id_prof, nome, materia, telefone, email in self.professores_data:
                if id_prof == professor_id:
                    info = f"Professor selecionado: {nome}"
                    if materia:
                        info += f" | MatÃ©ria: {materia}"
                    if telefone:
                        info += f" | Telefone: {ValidadorCampos.formatar_telefone(telefone)}"
                    if email:
                        info += f" | Email: {email}"

                    self.lbl_info_professor.setText(info)
                    self.lbl_info_professor.setVisible(True)
                    self.btn_associar.setEnabled(True)
                    break

    def associar_professor(self):
        """Associa o professor selecionado Ã  disciplina"""
        selecionados = self.list_professores.selectedItems()

        if not selecionados:
            QMessageBox.warning(self, "SeleÃ§Ã£o necessÃ¡ria",
                                "Por favor, selecione um professor.")
            return

        item = selecionados[0]
        professor_id = item.data(Qt.UserRole)

        try:
            # Atualizar disciplina com o novo professor
            self.db.execute_query(
                "UPDATE disciplinas SET professor_id = ? WHERE id = ?",
                (professor_id, self.id_disciplina)
            )

            QMessageBox.information(self, "Sucesso",
                                    "Professor associado Ã  disciplina com sucesso!")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao associar professor:\n{str(e)}")

    def remover_associacao(self):
        """Remove a associaÃ§Ã£o atual do professor com a disciplina"""
        resposta = QMessageBox.question(
            self, "Confirmar remoÃ§Ã£o",
            "Tem certeza que deseja remover o professor associado a esta disciplina?\n\n"
            "A disciplina ficarÃ¡ sem professor responsÃ¡vel.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            try:
                self.db.execute_query(
                    "UPDATE disciplinas SET professor_id = NULL WHERE id = ?",
                    (self.id_disciplina,)
                )

                QMessageBox.information(self, "Sucesso",
                                        "AssociaÃ§Ã£o de professor removida com sucesso!")
                self.accept()

            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Falha ao remover associaÃ§Ã£o:\n{str(e)}")

    # ============================================
    # PÃGINA DE TURMAS (COMPLETA)
    # ============================================

    def criar_pagina_turmas(self):
        """Cria a pÃ¡gina de gerenciamento de turmas - COMPLETA"""
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # CabeÃ§alho
        cabecalho_layout = QHBoxLayout()

        lbl_titulo = QLabel("GESTÃƒO DE TURMAS")
        lbl_titulo.setObjectName("title")

        # Barra de busca
        self.txt_busca_turma = QLineEdit()
        self.txt_busca_turma.setPlaceholderText("Buscar turma por nome, sÃ©rie ou professor...")
        self.txt_busca_turma.setMinimumHeight(40)
        self.txt_busca_turma.textChanged.connect(self.buscar_turmas)

        # BotÃµes de aÃ§Ã£o
        btn_novo = AnimacaoBotao("Nova Turma", cor_normal="#27ae60", cor_hover="#219653", cor_press="#1e874b")
        btn_novo.setIcon(self.style().standardIcon(QStyle.SP_FileIcon))
        btn_novo.clicked.connect(self.cadastrar_turma)

        btn_editar = AnimacaoBotao("Editar", cor_normal="#3498db", cor_hover="#2980b9", cor_press="#1c6ea4")
        btn_editar.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        btn_editar.clicked.connect(self.editar_turma)

        btn_excluir = AnimacaoBotao("Excluir", cor_normal="#e74c3c", cor_hover="#c0392b", cor_press="#a93226")
        btn_excluir.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        btn_excluir.clicked.connect(self.excluir_turma)

        btn_alunos = AnimacaoBotao("Ver Alunos", cor_normal="#9b59b6", cor_hover="#8e44ad", cor_press="#7d3c98")
        btn_alunos.setIcon(self.style().standardIcon(QStyle.SP_FileDialogListView))
        btn_alunos.clicked.connect(self.ver_alunos_turma)

        cabecalho_layout.addWidget(lbl_titulo)
        cabecalho_layout.addStretch()
        cabecalho_layout.addWidget(self.txt_busca_turma, 2)
        cabecalho_layout.addWidget(btn_novo)
        cabecalho_layout.addWidget(btn_editar)
        cabecalho_layout.addWidget(btn_excluir)
        cabecalho_layout.addWidget(btn_alunos)

        # Tabela de turmas
        self.tabela_turmas = QTableWidget()
        self.tabela_turmas.setColumnCount(9)
        self.tabela_turmas.setHorizontalHeaderLabels([
            "ID", "Nome", "SÃ©rie", "Turno", "Sala", "Capacidade",
            "Alunos", "Professor ResponsÃ¡vel", "Status"
        ])

        # Configurar tabela
        self.tabela_turmas.setAlternatingRowColors(True)
        self.tabela_turmas.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela_turmas.setSelectionMode(QTableWidget.SingleSelection)
        self.tabela_turmas.setEditTriggers(QTableWidget.NoEditTriggers)

        # Ajustar largura das colunas
        header = self.tabela_turmas.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Nome
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)  # Professor
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)  # Status

        # Conectar duplo clique
        self.tabela_turmas.doubleClicked.connect(self.ver_detalhes_turma)

        # Filtros
        filtros_layout = QHBoxLayout()

        lbl_serie = QLabel("Filtrar por sÃ©rie:")
        self.combo_filtro_serie_turma = QComboBox()
        self.combo_filtro_serie_turma.addItem("Todas as sÃ©ries")

        # Carregar sÃ©ries do banco
        series_config = self.db.get_config('series', '1Âº Ano,2Âº Ano,3Âº Ano,4Âº Ano,5Âº Ano')
        if series_config:
            series = series_config.split(',')
            for serie in series:
                self.combo_filtro_serie_turma.addItem(serie.strip())

        self.combo_filtro_serie_turma.currentIndexChanged.connect(self.filtrar_turmas_por_serie)

        lbl_turno = QLabel("Filtrar por turno:")
        self.combo_filtro_turno_turma = QComboBox()
        self.combo_filtro_turno_turma.addItem("Todos os turnos")

        # Carregar turnos do banco
        turnos_config = self.db.get_config('turnos', 'Matutino,Vespertino,Noturno')
        if turnos_config:
            turnos = turnos_config.split(',')
            for turno in turnos:
                self.combo_filtro_turno_turma.addItem(turno.strip())

        self.combo_filtro_turno_turma.currentIndexChanged.connect(self.filtrar_turmas_por_turno)

        filtros_layout.addWidget(lbl_serie)
        filtros_layout.addWidget(self.combo_filtro_serie_turma)
        filtros_layout.addWidget(lbl_turno)
        filtros_layout.addWidget(self.combo_filtro_turno_turma)
        filtros_layout.addStretch()

        # EstatÃ­sticas
        stats_layout = QHBoxLayout()

        self.lbl_total_turmas = QLabel("Total de turmas: 0")
        self.lbl_total_turmas.setObjectName("info-badge")

        self.lbl_turmas_ativas = QLabel("Ativas: 0")
        self.lbl_turmas_ativas.setObjectName("success-badge")

        self.lbl_turmas_inativas = QLabel("Inativas: 0")
        self.lbl_turmas_inativas.setObjectName("danger-badge")

        stats_layout.addWidget(self.lbl_total_turmas)
        stats_layout.addWidget(self.lbl_turmas_ativas)
        stats_layout.addWidget(self.lbl_turmas_inativas)
        stats_layout.addStretch()

        # Adicionar tudo ao layout
        layout.addLayout(cabecalho_layout)
        layout.addLayout(filtros_layout)
        layout.addWidget(self.tabela_turmas)
        layout.addLayout(stats_layout)

        self.paginas['turmas'] = pagina
        self.central_widget.addWidget(pagina)

        # Carregar dados iniciais
        self.carregar_tabela_turmas()

    def carregar_tabela_turmas(self):
        """Carrega dados na tabela de turmas"""
        try:
            query = """
                SELECT t.id, t.nome, t.serie, t.turno, t.sala, t.capacidade,
                       (SELECT COUNT(*) FROM alunos WHERE turma = t.nome AND status = 'Ativo') as total_alunos,
                       p.nome as professor_responsavel, t.ativa
                FROM turmas t
                LEFT JOIN professores p ON t.professor_responsavel_id = p.id
                ORDER BY t.serie, t.nome
            """

            turmas = self.db.execute_query(query, fetch=True)

            self.tabela_turmas.setRowCount(0)
            self.turmas_completas = turmas  # Salvar para filtragem

            for row_num, turma in enumerate(turmas):
                self.tabela_turmas.insertRow(row_num)

                for col_num, valor in enumerate(turma):
                    item = QTableWidgetItem(str(valor if valor else ""))

                    # Colorir status
                    if col_num == 8:  # Coluna ativa
                        if valor == 1:
                            item.setText("Ativa")
                            item.setForeground(QColor('#27ae60'))
                            item.setFont(QFont('', weight=QFont.Bold))
                        else:
                            item.setText("Inativa")
                            item.setForeground(QColor('#e74c3c'))

                    # Destacar lotaÃ§Ã£o
                    if col_num == 5 and col_num == 6:  # Capacidade e Alunos
                        capacidade = turma[5]
                        alunos = turma[6]
                        if capacidade and alunos:
                            if alunos >= capacidade:
                                item.setForeground(QColor('#e74c3c'))
                                item.setFont(QFont('', weight=QFont.Bold))
                            elif alunos >= capacidade * 0.8:
                                item.setForeground(QColor('#f39c12'))

                    self.tabela_turmas.setItem(row_num, col_num, item)

            # Atualizar estatÃ­sticas
            self.atualizar_estatisticas_turmas(turmas)

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar turmas:\n{str(e)}")

    def atualizar_estatisticas_turmas(self, turmas):
        """Atualiza as estatÃ­sticas de turmas"""
        total = len(turmas)
        ativas = sum(1 for t in turmas if t[8] == 1)
        inativas = total - ativas

        self.lbl_total_turmas.setText(f"Total de turmas: {total}")
        self.lbl_turmas_ativas.setText(f"Ativas: {ativas}")
        self.lbl_turmas_inativas.setText(f"Inativas: {inativas}")

    def buscar_turmas(self):
        """Busca turmas baseado no texto da busca"""
        texto = self.txt_busca_turma.text().strip().lower()

        if not self.turmas_completas:
            return

        turmas_filtradas = []

        for turma in self.turmas_completas:
            # Verificar se o texto estÃ¡ em algum campo
            match = False

            for campo in turma:
                if campo and texto in str(campo).lower():
                    match = True
                    break

            if match:
                turmas_filtradas.append(turma)

        # Atualizar tabela com resultados filtrados
        self.tabela_turmas.setRowCount(0)

        for row_num, turma in enumerate(turmas_filtradas):
            self.tabela_turmas.insertRow(row_num)

            for col_num, valor in enumerate(turma):
                item = QTableWidgetItem(str(valor if valor else ""))

                if col_num == 8:  # Status
                    if valor == 1:
                        item.setText("Ativa")
                        item.setForeground(QColor('#27ae60'))
                        item.setFont(QFont('', weight=QFont.Bold))
                    else:
                        item.setText("Inativa")
                        item.setForeground(QColor('#e74c3c'))

                self.tabela_turmas.setItem(row_num, col_num, item)

        self.atualizar_estatisticas_turmas(turmas_filtradas)

    def filtrar_turmas_por_serie(self):
        """Filtra turmas por sÃ©rie selecionada"""
        serie_filtro = self.combo_filtro_serie_turma.currentText()

        if serie_filtro == "Todas as sÃ©ries" or not self.turmas_completas:
            self.carregar_tabela_turmas()
            return

        turmas_filtradas = []

        for turma in self.turmas_completas:
            serie = turma[2]  # Ãndice da sÃ©rie

            if serie and serie_filtro in str(serie):
                turmas_filtradas.append(turma)

        # Atualizar tabela
        self.atualizar_tabela_com_turmas(turmas_filtradas)

    def filtrar_turmas_por_turno(self):
        """Filtra turmas por turno selecionado"""
        turno_filtro = self.combo_filtro_turno_turma.currentText()

        if turno_filtro == "Todos os turnos" or not self.turmas_completas:
            self.carregar_tabela_turmas()
            return

        turmas_filtradas = []

        for turma in self.turmas_completas:
            turno = turma[3]  # Ãndice do turno

            if turno and turno_filtro in str(turno):
                turmas_filtradas.append(turma)

        # Atualizar tabela
        self.atualizar_tabela_com_turmas(turmas_filtradas)

    def atualizar_tabela_com_turmas(self, turmas):
        """Atualiza a tabela com a lista de turmas fornecida"""
        self.tabela_turmas.setRowCount(0)

        for row_num, turma in enumerate(turmas):
            self.tabela_turmas.insertRow(row_num)

            for col_num, valor in enumerate(turma):
                item = QTableWidgetItem(str(valor if valor else ""))

                if col_num == 8:  # Status
                    if valor == 1:
                        item.setText("Ativa")
                        item.setForeground(QColor('#27ae60'))
                        item.setFont(QFont('', weight=QFont.Bold))
                    else:
                        item.setText("Inativa")
                        item.setForeground(QColor('#e74c3c'))

                self.tabela_turmas.setItem(row_num, col_num, item)

        self.atualizar_estatisticas_turmas(turmas)

    def cadastrar_turma(self):
        """Abre diÃ¡logo para cadastrar nova turma"""
        dialog = CadastroTurmaDialog(self)
        if dialog.exec_():
            self.carregar_tabela_turmas()

    def editar_turma(self):
        """Abre diÃ¡logo para editar turma selecionada"""
        selecionados = self.tabela_turmas.selectedItems()

        if not selecionados:
            QMessageBox.warning(self, "SeleÃ§Ã£o necessÃ¡ria",
                                "Por favor, selecione uma turma para editar.")
            return

        id_turma = int(self.tabela_turmas.item(selecionados[0].row(), 0).text())

        dialog = CadastroTurmaDialog(self, id_turma)
        if dialog.exec_():
            self.carregar_tabela_turmas()

    def excluir_turma(self):
        """Exclui turma selecionada"""
        selecionados = self.tabela_turmas.selectedItems()

        if not selecionados:
            QMessageBox.warning(self, "SeleÃ§Ã£o necessÃ¡ria",
                                "Por favor, selecione uma turma para excluir.")
            return

        id_turma = int(self.tabela_turmas.item(selecionados[0].row(), 0).text())
        nome_turma = self.tabela_turmas.item(selecionados[0].row(), 1).text()

        resposta = QMessageBox.question(
            self, "Confirmar exclusÃ£o",
            f"Tem certeza que deseja excluir a turma '{nome_turma}'?\n\n"
            "Esta aÃ§Ã£o nÃ£o pode ser desfeita.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            try:
                # Verificar se a turma tem alunos associados
                alunos = self.db.execute_query(
                    "SELECT COUNT(*) FROM alunos WHERE turma = ?",
                    (nome_turma,),
                    fetch=True
                )

                if alunos and alunos[0][0] > 0:
                    QMessageBox.warning(self, "Turma possui alunos",
                                        "Esta turma possui alunos matriculados.\n"
                                        "NÃ£o Ã© possÃ­vel excluÃ­-la.")
                    return

                # Verificar se a turma tem horÃ¡rios associados
                horarios = self.db.execute_query(
                    "SELECT COUNT(*) FROM horarios WHERE turma_id = ?",
                    (id_turma,),
                    fetch=True
                )

                if horarios and horarios[0][0] > 0:
                    QMessageBox.warning(self, "Turma possui horÃ¡rios",
                                        "Esta turma possui horÃ¡rios cadastrados.\n"
                                        "Remova os horÃ¡rios primeiro.")
                    return

                self.db.execute_query(
                    "DELETE FROM turmas WHERE id = ?",
                    (id_turma,)
                )

                QMessageBox.information(self, "Sucesso", "Turma excluÃ­da com sucesso!")
                self.carregar_tabela_turmas()

            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Falha ao excluir turma:\n{str(e)}")

    def ver_detalhes_turma(self, index):
        """Mostra detalhes da turma em duplo clique"""
        row = index.row()
        id_turma = int(self.tabela_turmas.item(row, 0).text())

        dialog = DetalhesTurmaDialog(self, id_turma)
        dialog.exec_()

    def ver_alunos_turma(self):
        """Mostra alunos da turma selecionada"""
        selecionados = self.tabela_turmas.selectedItems()

        if not selecionados:
            QMessageBox.warning(self, "SeleÃ§Ã£o necessÃ¡ria",
                                "Por favor, selecione uma turma para ver os alunos.")
            return

        nome_turma = self.tabela_turmas.item(selecionados[0].row(), 1).text()

        dialog = AlunosTurmaDialog(self, nome_turma)
        dialog.exec_()


# ============================================
# DIÃLOGO DE CADASTRO DE TURMA
# ============================================

class CadastroTurmaDialog(QDialog):
    """DiÃ¡logo para cadastro/ediÃ§Ã£o de turmas"""

    def __init__(self, parent=None, id_turma=None):
        super().__init__(parent)
        self.id_turma = id_turma
        self.db = DatabaseManager()
        self.modo_edicao = id_turma is not None

        self.setWindowTitle("Cadastrar Turma" if not self.modo_edicao else "Editar Turma")
        self.setFixedSize(600, 500)
        self.setStyleSheet(GLOBAL_STYLESHEET)

        self.init_ui()
        self.carregar_series()
        self.carregar_turnos()
        self.carregar_professores()
        self.carregar_dados_turma() if self.modo_edicao else None

    def init_ui(self):
        """Inicializa a interface do diÃ¡logo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # TÃ­tulo
        titulo = "CADASTRAR NOVA TURMA" if not self.modo_edicao else "EDITAR TURMA"
        lbl_titulo = QLabel(titulo)
        lbl_titulo.setObjectName("title")

        # FormulÃ¡rio
        form_layout = QFormLayout()
        form_layout.setContentsMargins(10, 10, 10, 10)
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)

        # Nome da turma
        self.txt_nome = QLineEdit()
        self.txt_nome.setPlaceholderText("Ex: Turma A, 1Âº Ano A")

        # SÃ©rie
        self.combo_serie = QComboBox()

        # Turno
        self.combo_turno = QComboBox()

        # Sala
        self.txt_sala = QLineEdit()
        self.txt_sala.setPlaceholderText("Ex: Sala 101, LaboratÃ³rio 2")

        # Capacidade
        self.spin_capacidade = QSpinBox()
        self.spin_capacidade.setRange(1, 100)
        self.spin_capacidade.setValue(30)

        # Ano letivo
        self.spin_ano_letivo = QSpinBox()
        self.spin_ano_letivo.setRange(2000, 2100)
        self.spin_ano_letivo.setValue(date.today().year)

        # Professor responsÃ¡vel
        self.combo_professor = QComboBox()
        self.combo_professor.addItem("Nenhum", -1)

        # Status
        self.combo_status = QComboBox()
        self.combo_status.addItems(["Ativa", "Inativa"])

        # Adicionar campos ao formulÃ¡rio
        form_layout.addRow("Nome da turma:", self.txt_nome)
        form_layout.addRow("SÃ©rie:", self.combo_serie)
        form_layout.addRow("Turno:", self.combo_turno)
        form_layout.addRow("Sala:", self.txt_sala)
        form_layout.addRow("Capacidade:", self.spin_capacidade)
        form_layout.addRow("Ano letivo:", self.spin_ano_letivo)
        form_layout.addRow("Professor responsÃ¡vel:", self.combo_professor)
        form_layout.addRow("Status:", self.combo_status)

        # BotÃµes
        botoes_layout = QHBoxLayout()

        self.btn_salvar = AnimacaoBotao(
            "SALVAR" if not self.modo_edicao else "ATUALIZAR",
            cor_normal="#27ae60", cor_hover="#219653", cor_press="#1e874b"
        )
        self.btn_salvar.setMinimumHeight(45)
        self.btn_salvar.clicked.connect(self.salvar_turma)

        self.btn_cancelar = QPushButton("CANCELAR")
        self.btn_cancelar.setObjectName("danger")
        self.btn_cancelar.setMinimumHeight(45)
        self.btn_cancelar.clicked.connect(self.reject)

        if self.modo_edicao:
            self.btn_excluir = QPushButton("EXCLUIR")
            self.btn_excluir.setObjectName("warning")
            self.btn_excluir.setMinimumHeight(45)
            self.btn_excluir.clicked.connect(self.excluir_turma)
            botoes_layout.addWidget(self.btn_excluir)

        botoes_layout.addStretch()
        botoes_layout.addWidget(self.btn_salvar)
        botoes_layout.addWidget(self.btn_cancelar)

        # Adicionar tudo ao layout principal
        layout.addWidget(lbl_titulo)
        layout.addLayout(form_layout)
        layout.addStretch()
        layout.addLayout(botoes_layout)

    def carregar_series(self):
        """Carrega sÃ©ries disponÃ­veis no combobox"""
        series_config = self.db.get_config('series', '1Âº Ano,2Âº Ano,3Âº Ano,4Âº Ano,5Âº Ano')

        if series_config:
            series = series_config.split(',')
            for serie in series:
                self.combo_serie.addItem(serie.strip())

    def carregar_turnos(self):
        """Carrega turnos disponÃ­veis no combobox"""
        turnos_config = self.db.get_config('turnos', 'Matutino,Vespertino,Noturno')

        if turnos_config:
            turnos = turnos_config.split(',')
            for turno in turnos:
                self.combo_turno.addItem(turno.strip())

    def carregar_professores(self):
        """Carrega professores ativos no combobox"""
        try:
            professores = self.db.execute_query('''
                SELECT id, nome, materia 
                FROM professores 
                WHERE ativo = 1
                ORDER BY nome
            ''', fetch=True)

            for id_professor, nome, materia in professores:
                texto = f"{nome} ({materia})" if materia else nome
                self.combo_professor.addItem(texto, id_professor)

        except Exception as e:
            print(f"Erro ao carregar professores: {e}")

    def carregar_dados_turma(self):
        """Carrega dados da turma para ediÃ§Ã£o"""
        try:
            turma = self.db.execute_query(
                "SELECT * FROM turmas WHERE id = ?",
                (self.id_turma,),
                fetch=True
            )

            if turma and len(turma) > 0:
                dados = turma[0]

                self.txt_nome.setText(dados[1] if dados[1] else "")

                # SÃ©rie
                if dados[2]:  # sÃ©rie
                    index = self.combo_serie.findText(dados[2])
                    if index >= 0:
                        self.combo_serie.setCurrentIndex(index)

                # Turno
                if dados[3]:  # turno
                    index = self.combo_turno.findText(dados[3])
                    if index >= 0:
                        self.combo_turno.setCurrentIndex(index)

                self.txt_sala.setText(dados[4] if dados[4] else "")

                if dados[5]:  # capacidade
                    self.spin_capacidade.setValue(int(dados[5]))

                # Professor responsÃ¡vel
                if dados[6]:  # professor_responsavel_id
                    for i in range(self.combo_professor.count()):
                        if self.combo_professor.itemData(i) == dados[6]:
                            self.combo_professor.setCurrentIndex(i)
                            break

                if dados[7]:  # ano_letivo
                    self.spin_ano_letivo.setValue(int(dados[7]))

                # Status
                self.combo_status.setCurrentIndex(0 if dados[8] == 1 else 1)

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar dados da turma:\n{str(e)}")

    def validar_campos(self):
        """Valida os campos do formulÃ¡rio"""
        erros = []

        # Nome obrigatÃ³rio
        if not self.txt_nome.text().strip():
            erros.append("Nome da turma Ã© obrigatÃ³rio.")

        # Verificar se jÃ¡ existe turma com mesmo nome, sÃ©rie e turno
        nome = self.txt_nome.text().strip()
        serie = self.combo_serie.currentText()
        turno = self.combo_turno.currentText()

        query = "SELECT COUNT(*) FROM turmas WHERE nome = ? AND serie = ? AND turno = ?"
        params = [nome, serie, turno]

        if self.modo_edicao:
            query += " AND id != ?"
            params.append(self.id_turma)

        resultado = self.db.execute_query(query, tuple(params), fetch=True)

        if resultado and resultado[0][0] > 0:
            erros.append("JÃ¡ existe uma turma com este nome, sÃ©rie e turno.")

        return erros

    def salvar_turma(self):
        """Salva ou atualiza a turma no banco de dados"""
        # Validar campos
        erros = self.validar_campos()
        if erros:
            QMessageBox.warning(self, "Erros no formulÃ¡rio", "\n".join(erros))
            return

        # Preparar dados
        dados = {
            'nome': self.txt_nome.text().strip(),
            'serie': self.combo_serie.currentText(),
            'turno': self.combo_turno.currentText(),
            'sala': self.txt_sala.text().strip(),
            'capacidade': self.spin_capacidade.value(),
            'professor_responsavel_id': self.combo_professor.currentData(),
            'ano_letivo': self.spin_ano_letivo.value(),
            'ativa': 1 if self.combo_status.currentText() == "Ativa" else 0
        }

        # Se professor_id for -1 (Nenhum), definir como NULL
        if dados['professor_responsavel_id'] == -1:
            dados['professor_responsavel_id'] = None

        try:
            if self.modo_edicao:
                # Atualizar turma existente
                query = '''
                    UPDATE turmas SET
                        nome = ?, serie = ?, turno = ?, sala = ?, capacidade = ?,
                        professor_responsavel_id = ?, ano_letivo = ?, ativa = ?
                    WHERE id = ?
                '''

                params = (
                    dados['nome'], dados['serie'], dados['turno'], dados['sala'], dados['capacidade'],
                    dados['professor_responsavel_id'], dados['ano_letivo'], dados['ativa'], self.id_turma
                )

                self.db.execute_query(query, params)
                QMessageBox.information(self, "Sucesso", "Turma atualizada com sucesso!")

            else:
                # Inserir nova turma
                query = '''
                    INSERT INTO turmas (
                        nome, serie, turno, sala, capacidade,
                        professor_responsavel_id, ano_letivo, ativa
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                '''

                params = (
                    dados['nome'], dados['serie'], dados['turno'], dados['sala'], dados['capacidade'],
                    dados['professor_responsavel_id'], dados['ano_letivo'], dados['ativa']
                )

                self.db.execute_query(query, params)
                QMessageBox.information(self, "Sucesso", "Turma cadastrada com sucesso!")

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao salvar turma:\n{str(e)}")

    def excluir_turma(self):
        """Exclui a turma atual"""
        resposta = QMessageBox.question(
            self, "Confirmar exclusÃ£o",
            "Tem certeza que deseja excluir esta turma?\n\n"
            "Esta aÃ§Ã£o nÃ£o pode ser desfeita.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            try:
                self.db.execute_query(
                    "DELETE FROM turmas WHERE id = ?",
                    (self.id_turma,)
                )

                QMessageBox.information(self, "Sucesso", "Turma excluÃ­da com sucesso!")
                self.accept()

            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Falha ao excluir turma:\n{str(e)}")


# ============================================
# DIÃLOGO DE DETALHES DA TURMA
# ============================================

class DetalhesTurmaDialog(QDialog):
    """DiÃ¡logo para exibir detalhes completos da turma"""

    def __init__(self, parent=None, id_turma=None):
        super().__init__(parent)
        self.id_turma = id_turma
        self.db = DatabaseManager()

        self.setWindowTitle("Detalhes da Turma")
        self.setFixedSize(900, 700)
        self.setStyleSheet(GLOBAL_STYLESHEET)

        self.init_ui()
        self.carregar_detalhes_turma()

    def init_ui(self):
        """Inicializa a interface do diÃ¡logo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # CabeÃ§alho com nome da turma
        self.lbl_nome_turma = QLabel()
        self.lbl_nome_turma.setObjectName("title")
        self.lbl_nome_turma.setStyleSheet("""
            QLabel#title {
                font-size: 22px;
                font-weight: 700;
                color: #2c3e50;
                text-align: center;
                padding: 15px;
                background-color: #d6eaf8;
                border-radius: 8px;
                border: 2px solid #3498db;
            }
        """)

        # Abas para diferentes informaÃ§Ãµes
        tab_widget = QTabWidget()

        # Aba: InformaÃ§Ãµes Gerais
        aba_info = QWidget()
        self.layout_info = QFormLayout(aba_info)
        self.layout_info.setContentsMargins(20, 20, 20, 20)
        self.layout_info.setSpacing(10)

        # Aba: Alunos
        aba_alunos = QWidget()
        layout_alunos = QVBoxLayout(aba_alunos)

        self.tabela_alunos = QTableWidget()
        self.tabela_alunos.setColumnCount(6)
        self.tabela_alunos.setHorizontalHeaderLabels([
            "Nome", "Data Nasc.", "ResponsÃ¡vel", "Telefone", "Status", "Data MatrÃ­cula"
        ])

        layout_alunos.addWidget(QLabel("Alunos da Turma:"))
        layout_alunos.addWidget(self.tabela_alunos)

        # Aba: Disciplinas
        aba_disciplinas = QWidget()
        layout_disciplinas = QVBoxLayout(aba_disciplinas)

        self.tabela_disciplinas = QTableWidget()
        self.tabela_disciplinas.setColumnCount(5)
        self.tabela_disciplinas.setHorizontalHeaderLabels([
            "Disciplina", "Professor", "Carga HorÃ¡ria", "Dias", "Status"
        ])

        layout_disciplinas.addWidget(QLabel("Disciplinas da Turma:"))
        layout_disciplinas.addWidget(self.tabela_disciplinas)

        # Adicionar abas
        tab_widget.addTab(aba_info, "InformaÃ§Ãµes")
        tab_widget.addTab(aba_alunos, "Alunos")
        tab_widget.addTab(aba_disciplinas, "Disciplinas")

        # BotÃµes
        botoes_layout = QHBoxLayout()

        btn_fechar = AnimacaoBotao("FECHAR", cor_normal="#7f8c8d", cor_hover="#95a5a6", cor_press="#5d6d7e")
        btn_fechar.clicked.connect(self.close)

        btn_editar = AnimacaoBotao("EDITAR", cor_normal="#3498db", cor_hover="#2980b9", cor_press="#1c6ea4")
        btn_editar.clicked.connect(self.editar_turma)

        botoes_layout.addWidget(btn_editar)
        botoes_layout.addStretch()
        botoes_layout.addWidget(btn_fechar)

        # Adicionar tudo ao layout
        layout.addWidget(self.lbl_nome_turma)
        layout.addWidget(tab_widget)
        layout.addLayout(botoes_layout)

    def carregar_detalhes_turma(self):
        """Carrega detalhes completos da turma"""
        try:
            # Carregar informaÃ§Ãµes bÃ¡sicas
            turma = self.db.execute_query(
                "SELECT * FROM turmas WHERE id = ?",
                (self.id_turma,),
                fetch=True
            )

            if turma and len(turma) > 0:
                dados = turma[0]

                # Atualizar tÃ­tulo
                nome_completo = f"{dados[1]} - {dados[2]} ({dados[3]})"
                self.lbl_nome_turma.setText(nome_completo)

                # Adicionar informaÃ§Ãµes gerais
                self.adicionar_info("SÃ©rie:", dados[2] if dados[2] else "NÃ£o informada")
                self.adicionar_info("Turno:", dados[3] if dados[3] else "NÃ£o informado")
                self.adicionar_info("Sala:", dados[4] if dados[4] else "NÃ£o informada")
                self.adicionar_info("Capacidade:", str(dados[5]) if dados[5] else "NÃ£o informada")

                # Professor responsÃ¡vel
                if dados[6]:  # professor_responsavel_id
                    professor = self.db.execute_query(
                        "SELECT nome, materia FROM professores WHERE id = ?",
                        (dados[6],),
                        fetch=True
                    )

                    if professor and len(professor) > 0:
                        prof_nome, prof_materia = professor[0]
                        texto_professor = f"{prof_nome}"
                        if prof_materia:
                            texto_professor += f" ({prof_materia})"
                        self.adicionar_info("Professor responsÃ¡vel:", texto_professor)
                    else:
                        self.adicionar_info("Professor responsÃ¡vel:", "NÃ£o atribuÃ­do")
                else:
                    self.adicionar_info("Professor responsÃ¡vel:", "NÃ£o atribuÃ­do")

                self.adicionar_info("Ano letivo:", str(dados[7]) if dados[7] else "NÃ£o informado")

                # Contar alunos na turma
                nome_turma = dados[1]
                total_alunos = self.db.execute_query(
                    "SELECT COUNT(*) FROM alunos WHERE turma = ? AND status = 'Ativo'",
                    (nome_turma,),
                    fetch=True
                )

                if total_alunos:
                    self.adicionar_info("Total de alunos:", str(total_alunos[0][0]))

                    # Calcular porcentagem de ocupaÃ§Ã£o
                    if dados[5]:  # capacidade
                        capacidade = dados[5]
                        ocupacao = (total_alunos[0][0] / capacidade) * 100
                        self.adicionar_info_colorido(
                            "OcupaÃ§Ã£o:",
                            f"{ocupacao:.1f}%",
                            "#e74c3c" if ocupacao >= 100 else "#f39c12" if ocupacao >= 80 else "#27ae60"
                        )

                status = "Ativa" if dados[8] == 1 else "Inativa"
                status_cor = "#27ae60" if dados[8] == 1 else "#e74c3c"
                self.adicionar_info_colorido("Status:", status, status_cor)

                # Carregar alunos da turma
                self.carregar_alunos_turma(nome_turma)

                # Carregar disciplinas da turma
                self.carregar_disciplinas_turma()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar detalhes da turma:\n{str(e)}")

    def adicionar_info(self, label, valor):
        """Adiciona uma linha de informaÃ§Ã£o ao formulÃ¡rio"""
        lbl_label = QLabel(label)
        lbl_label.setStyleSheet("font-weight: 600; color: #2c3e50;")

        lbl_valor = QLabel(valor)
        lbl_valor.setStyleSheet("color: #34495e;")

        self.layout_info.addRow(lbl_label, lbl_valor)

    def adicionar_info_colorido(self, label, valor, cor):
        """Adiciona uma linha de informaÃ§Ã£o com cor especÃ­fica"""
        lbl_label = QLabel(label)
        lbl_label.setStyleSheet("font-weight: 600; color: #2c3e50;")

        lbl_valor = QLabel(valor)
        lbl_valor.setStyleSheet(f"color: {cor}; font-weight: 600;")

        self.layout_info.addRow(lbl_label, lbl_valor)

    def carregar_alunos_turma(self, nome_turma):
        """Carrega alunos da turma"""
        try:
            alunos = self.db.execute_query('''
                SELECT nome, data_nascimento, nome_mae, telefone_responsavel, status, data_matricula
                FROM alunos
                WHERE turma = ? AND status = 'Ativo'
                ORDER BY nome
            ''', (nome_turma,), fetch=True)

            self.tabela_alunos.setRowCount(len(alunos))

            for row, (nome, data_nasc, responsavel, telefone, status, data_mat) in enumerate(alunos):
                self.tabela_alunos.setItem(row, 0, QTableWidgetItem(nome))

                # Data de nascimento formatada
                if data_nasc:
                    try:
                        data_obj = datetime.strptime(data_nasc, '%Y-%m-%d')
                        data_formatada = data_obj.strftime('%d/%m/%Y')
                    except:
                        data_formatada = data_nasc
                else:
                    data_formatada = "-"

                self.tabela_alunos.setItem(row, 1, QTableWidgetItem(data_formatada))
                self.tabela_alunos.setItem(row, 2, QTableWidgetItem(responsavel if responsavel else "-"))

                # Telefone formatado
                telefone_formatado = ValidadorCampos.formatar_telefone(telefone) if telefone else "-"
                self.tabela_alunos.setItem(row, 3, QTableWidgetItem(telefone_formatado))

                # Status
                item_status = QTableWidgetItem(status if status else "-")
                if status == "Ativo":
                    item_status.setForeground(QColor('#27ae60'))
                else:
                    item_status.setForeground(QColor('#e74c3c'))

                self.tabela_alunos.setItem(row, 4, item_status)

                # Data de matrÃ­cula formatada
                if data_mat:
                    try:
                        data_obj = datetime.strptime(data_mat, '%Y-%m-%d')
                        data_formatada = data_obj.strftime('%d/%m/%Y')
                    except:
                        data_formatada = data_mat
                else:
                    data_formatada = "-"

                self.tabela_alunos.setItem(row, 5, QTableWidgetItem(data_formatada))

        except Exception as e:
            print(f"Erro ao carregar alunos: {e}")

    def carregar_disciplinas_turma(self):
        """Carrega disciplinas ministradas para a turma"""
        try:
            # Obter disciplinas atravÃ©s dos horÃ¡rios
            disciplinas = self.db.execute_query('''
                SELECT DISTINCT d.nome, p.nome, d.carga_horaria, 
                       GROUP_CONCAT(DISTINCT h.dia_semana) as dias,
                       d.ativa
                FROM horarios h
                JOIN disciplinas d ON h.disciplina_id = d.id
                LEFT JOIN professores p ON d.professor_id = p.id
                WHERE h.turma_id = ? AND h.ativo = 1
                GROUP BY d.id
                ORDER BY d.nome
            ''', (self.id_turma,), fetch=True)

            self.tabela_disciplinas.setRowCount(len(disciplinas))

            for row, (disciplina, professor, carga_horaria, dias, ativa) in enumerate(disciplinas):
                self.tabela_disciplinas.setItem(row, 0, QTableWidgetItem(disciplina))
                self.tabela_disciplinas.setItem(row, 1, QTableWidgetItem(professor if professor else "-"))
                self.tabela_disciplinas.setItem(row, 2, QTableWidgetItem(str(carga_horaria) if carga_horaria else "-"))
                self.tabela_disciplinas.setItem(row, 3, QTableWidgetItem(dias if dias else "-"))

                status = "Ativa" if ativa == 1 else "Inativa"
                item_status = QTableWidgetItem(status)

                if ativa == 1:
                    item_status.setForeground(QColor('#27ae60'))
                else:
                    item_status.setForeground(QColor('#e74c3c'))

                self.tabela_disciplinas.setItem(row, 4, item_status)

        except Exception as e:
            print(f"Erro ao carregar disciplinas: {e}")

    def editar_turma(self):
        """Abre diÃ¡logo para editar a turma"""
        self.close()
        # Em uma implementaÃ§Ã£o real, aqui abriria o diÃ¡logo de ediÃ§Ã£o


# ============================================
# DIÃLOGO DE ALUNOS DA TURMA
# ============================================

class AlunosTurmaDialog(QDialog):
    """DiÃ¡logo para visualizaÃ§Ã£o e gerenciamento de alunos de uma turma"""

    def __init__(self, parent=None, nome_turma=""):
        super().__init__(parent)
        self.nome_turma = nome_turma
        self.db = DatabaseManager()

        self.setWindowTitle(f"Alunos - {nome_turma}")
        self.setFixedSize(1000, 700)
        self.setStyleSheet(GLOBAL_STYLESHEET)

        self.init_ui()
        self.carregar_alunos_turma()

    def init_ui(self):
        """Inicializa a interface do diÃ¡logo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # CabeÃ§alho
        cabecalho_layout = QHBoxLayout()

        lbl_titulo = QLabel(f"ALUNOS DA TURMA - {self.nome_turma.upper()}")
        lbl_titulo.setObjectName("title")

        # Filtros
        filtros_layout = QHBoxLayout()

        lbl_status = QLabel("Filtrar por status:")
        self.combo_filtro_status = QComboBox()
        self.combo_filtro_status.addItems(["Todos", "Ativos", "Inativos"])
        self.combo_filtro_status.currentIndexChanged.connect(self.filtrar_alunos)

        lbl_serie = QLabel("Filtrar por sÃ©rie:")
        self.combo_filtro_serie = QComboBox()
        self.combo_filtro_serie.addItem("Todas as sÃ©ries")

        # Carregar sÃ©ries Ãºnicas dos alunos da turma
        self.carregar_series_turma()
        self.combo_filtro_serie.currentIndexChanged.connect(self.filtrar_alunos)

        filtros_layout.addWidget(lbl_status)
        filtros_layout.addWidget(self.combo_filtro_status)
        filtros_layout.addWidget(lbl_serie)
        filtros_layout.addWidget(self.combo_filtro_serie)
        filtros_layout.addStretch()

        # BotÃµes de aÃ§Ã£o
        btn_adicionar = AnimacaoBotao("Adicionar Aluno", cor_normal="#27ae60", cor_hover="#219653", cor_press="#1e874b")
        btn_adicionar.clicked.connect(self.adicionar_aluno)

        btn_remover = AnimacaoBotao("Remover da Turma", cor_normal="#e74c3c", cor_hover="#c0392b", cor_press="#a93226")
        btn_remover.clicked.connect(self.remover_aluno_turma)

        btn_transferir = AnimacaoBotao("Transferir", cor_normal="#3498db", cor_hover="#2980b9", cor_press="#1c6ea4")
        btn_transferir.clicked.connect(self.transferir_aluno)

        # Tabela de alunos
        self.tabela_alunos = QTableWidget()
        self.tabela_alunos.setColumnCount(9)
        self.tabela_alunos.setHorizontalHeaderLabels([
            "ID", "Nome", "CPF", "Data Nasc.", "SÃ©rie", "ResponsÃ¡vel",
            "Telefone", "Status", "Data MatrÃ­cula"
        ])

        # Configurar tabela
        self.tabela_alunos.setAlternatingRowColors(True)
        self.tabela_alunos.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela_alunos.setSelectionMode(QTableWidget.ExtendedSelection)
        self.tabela_alunos.setEditTriggers(QTableWidget.NoEditTriggers)

        # Ocultar coluna ID
        self.tabela_alunos.setColumnHidden(0, True)

        # Ajustar largura das colunas
        header = self.tabela_alunos.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Nome
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # ResponsÃ¡vel

        # Resumo
        self.lbl_resumo = QLabel()
        self.lbl_resumo.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #2c3e50;
                font-weight: 600;
                padding: 10px;
                background-color: #f8f9fa;
                border-radius: 6px;
                border: 1px solid #dce1e6;
            }
        """)

        # BotÃµes inferiores
        botoes_layout = QHBoxLayout()

        btn_imprimir = AnimacaoBotao("Imprimir Lista", cor_normal="#f39c12", cor_hover="#d68910", cor_press="#b9770e")
        btn_imprimir.clicked.connect(self.imprimir_lista)

        btn_fechar = QPushButton("FECHAR")
        btn_fechar.setObjectName("danger")
        btn_fechar.clicked.connect(self.close)

        botoes_layout.addWidget(btn_adicionar)
        botoes_layout.addWidget(btn_remover)
        botoes_layout.addWidget(btn_transferir)
        botoes_layout.addWidget(btn_imprimir)
        botoes_layout.addStretch()
        botoes_layout.addWidget(btn_fechar)

        # Montar layout
        cabecalho_layout.addWidget(lbl_titulo)
        cabecalho_layout.addStretch()

        layout.addLayout(cabecalho_layout)
        layout.addLayout(filtros_layout)
        layout.addWidget(self.tabela_alunos)
        layout.addWidget(self.lbl_resumo)
        layout.addLayout(botoes_layout)


"""
PROJETO ESCOLA - SISTEMA DE GESTÃƒO ESCOLAR
Parte 5/10 - ContinuaÃ§Ã£o: Alunos da Turma, Notas e FrequÃªncia
"""


def carregar_series_turma(self):
    """Carrega sÃ©ries Ãºnicas dos alunos da turma"""
    try:
        series = self.db.execute_query('''
                SELECT DISTINCT serie 
                FROM alunos 
                WHERE turma = ? AND serie IS NOT NULL
                ORDER BY serie
            ''', (self.nome_turma,), fetch=True)

        for serie in series:
            if serie[0]:
                self.combo_filtro_serie.addItem(serie[0])

    except Exception as e:
        print(f"Erro ao carregar sÃ©ries: {e}")


def carregar_alunos_turma(self):
    """Carrega todos os alunos da turma"""
    try:
        self.alunos_completos = self.db.execute_query('''
                SELECT id, nome, cpf, data_nascimento, serie, 
                       nome_mae, telefone_responsavel, status, data_matricula
                FROM alunos
                WHERE turma = ?
                ORDER BY nome
            ''', (self.nome_turma,), fetch=True)

        self.aplicar_filtros_alunos()

    except Exception as e:
        QMessageBox.critical(self, "Erro", f"Falha ao carregar alunos:\n{str(e)}")


def aplicar_filtros_alunos(self):
    """Aplica filtros aos alunos"""
    if not self.alunos_completos:
        self.tabela_alunos.setRowCount(0)
        self.lbl_resumo.setText(f"Turma {self.nome_turma} - Nenhum aluno encontrado.")
        return

    # Filtrar por status
    status_filtro = self.combo_filtro_status.currentText()
    serie_filtro = self.combo_filtro_serie.currentText()

    alunos_filtrados = []

    for aluno in self.alunos_completos:
        id_aluno, nome, cpf, data_nasc, serie, responsavel, telefone, status, data_mat = aluno

        # Aplicar filtro de status
        if status_filtro == "Ativos" and status != "Ativo":
            continue
        elif status_filtro == "Inativos" and status == "Ativo":
            continue

        # Aplicar filtro de sÃ©rie
        if serie_filtro != "Todas as sÃ©ries" and serie != serie_filtro:
            continue

        alunos_filtrados.append(aluno)

    # Atualizar tabela
    self.tabela_alunos.setRowCount(len(alunos_filtrados))

    for row, (id_aluno, nome, cpf, data_nasc, serie, responsavel, telefone, status, data_mat) in enumerate(
            alunos_filtrados):
        # ID (oculto)
        self.tabela_alunos.setItem(row, 0, QTableWidgetItem(str(id_aluno)))

        # Nome
        self.tabela_alunos.setItem(row, 1, QTableWidgetItem(nome))

        # CPF formatado
        cpf_formatado = ValidadorCampos.formatar_cpf(cpf) if cpf else "-"
        self.tabela_alunos.setItem(row, 2, QTableWidgetItem(cpf_formatado))

        # Data de nascimento formatada
        if data_nasc:
            try:
                data_obj = datetime.strptime(data_nasc, '%Y-%m-%d')
                data_formatada = data_obj.strftime('%d/%m/%Y')
            except:
                data_formatada = data_nasc
        else:
            data_formatada = "-"

        self.tabela_alunos.setItem(row, 3, QTableWidgetItem(data_formatada))

        # SÃ©rie
        self.tabela_alunos.setItem(row, 4, QTableWidgetItem(serie if serie else "-"))

        # ResponsÃ¡vel
        self.tabela_alunos.setItem(row, 5, QTableWidgetItem(responsavel if responsavel else "-"))

        # Telefone formatado
        telefone_formatado = ValidadorCampos.formatar_telefone(telefone) if telefone else "-"
        self.tabela_alunos.setItem(row, 6, QTableWidgetItem(telefone_formatado))

        # Status
        item_status = QTableWidgetItem(status if status else "-")

        if status == "Ativo":
            item_status.setForeground(QColor('#27ae60'))
            item_status.setFont(QFont('', weight=QFont.Bold))
        else:
            item_status.setForeground(QColor('#e74c3c'))

        self.tabela_alunos.setItem(row, 7, item_status)

        # Data de matrÃ­cula formatada
        if data_mat:
            try:
                data_obj = datetime.strptime(data_mat, '%Y-%m-%d')
                data_formatada = data_obj.strftime('%d/%m/%Y')
            except:
                data_formatada = data_mat
        else:
            data_formatada = "-"

        self.tabela_alunos.setItem(row, 8, QTableWidgetItem(data_formatada))

    # Atualizar resumo
    total = len(alunos_filtrados)
    ativos = sum(1 for a in alunos_filtrados if a[7] == "Ativo")
    inativos = total - ativos

    self.lbl_resumo.setText(
        f"Turma {self.nome_turma} | "
        f"Total de alunos: {total} | "
        f"Ativos: {ativos} | "
        f"Inativos: {inativos}"
    )


def filtrar_alunos(self):
    """Aplica filtros quando selecionados"""
    self.aplicar_filtros_alunos()


def adicionar_aluno(self):
    """Abre diÃ¡logo para adicionar aluno Ã  turma"""
    dialog = AdicionarAlunoTurmaDialog(self, self.nome_turma)
    if dialog.exec_():
        self.carregar_alunos_turma()


def remover_aluno_turma(self):
    """Remove aluno selecionado da turma"""
    selecionados = self.tabela_alunos.selectedItems()

    if not selecionados:
        QMessageBox.warning(self, "SeleÃ§Ã£o necessÃ¡ria",
                            "Por favor, selecione um ou mais alunos para remover da turma.")
        return

    # Obter IDs Ãºnicos dos alunos selecionados
    ids_alunos = set()
    rows_selecionadas = set()

    for item in selecionados:
        row = item.row()
        rows_selecionadas.add(row)

    for row in rows_selecionadas:
        id_aluno = int(self.tabela_alunos.item(row, 0).text())
        ids_alunos.add(id_aluno)

    nomes_alunos = []
    for row in rows_selecionadas:
        nome = self.tabela_alunos.item(row, 1).text()
        nomes_alunos.append(nome)

    resposta = QMessageBox.question(
        self, "Confirmar remoÃ§Ã£o",
        f"Tem certeza que deseja remover {len(ids_alunos)} aluno(s) da turma?\n\n"
        f"Alunos: {', '.join(nomes_alunos[:3])}{'...' if len(nomes_alunos) > 3 else ''}",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )

    if resposta == QMessageBox.Yes:
        try:
            for id_aluno in ids_alunos:
                self.db.execute_query(
                    "UPDATE alunos SET turma = NULL WHERE id = ?",
                    (id_aluno,)
                )

            QMessageBox.information(self, "Sucesso",
                                    f"{len(ids_alunos)} aluno(s) removido(s) da turma com sucesso!")
            self.carregar_alunos_turma()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao remover alunos da turma:\n{str(e)}")


def transferir_aluno(self):
    """Transfere aluno selecionado para outra turma"""
    selecionados = self.tabela_alunos.selectedItems()

    if not selecionados:
        QMessageBox.warning(self, "SeleÃ§Ã£o necessÃ¡ria",
                            "Por favor, selecione um aluno para transferir.")
        return

    row = selecionados[0].row()
    id_aluno = int(self.tabela_alunos.item(row, 0).text())
    nome_aluno = self.tabela_alunos.item(row, 1).text()

    dialog = TransferirAlunoDialog(self, id_aluno, nome_aluno, self.nome_turma)
    if dialog.exec_():
        self.carregar_alunos_turma()


def imprimir_lista(self):
    """Imprime lista de alunos da turma"""
    QMessageBox.information(self, "Funcionalidade em desenvolvimento",
                            "A impressÃ£o de listas serÃ¡ implementada na prÃ³xima versÃ£o.")


# ============================================
# DIÃLOGO DE ADICIONAR ALUNO Ã€ TURMA
# ============================================

class AdicionarAlunoTurmaDialog(QDialog):
    """DiÃ¡logo para adicionar aluno Ã  turma"""

    def __init__(self, parent=None, nome_turma=""):
        super().__init__(parent)
        self.nome_turma = nome_turma
        self.db = DatabaseManager()

        self.setWindowTitle(f"Adicionar Aluno Ã  Turma {nome_turma}")
        self.setFixedSize(800, 600)
        self.setStyleSheet(GLOBAL_STYLESHEET)

        self.init_ui()
        self.carregar_alunos_sem_turma()

    def init_ui(self):
        """Inicializa a interface do diÃ¡logo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # TÃ­tulo
        lbl_titulo = QLabel(f"ADICIONAR ALUNO Ã€ TURMA")
        lbl_titulo.setObjectName("title")

        # InformaÃ§Ã£o da turma
        lbl_info_turma = QLabel(f"Turma: {self.nome_turma}")
        lbl_info_turma.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 600;
                color: #2c3e50;
                padding: 10px;
                background-color: #e3f2fd;
                border-radius: 6px;
                border: 1px solid #3498db;
            }
        """)

        # Barra de busca
        self.txt_busca_aluno = QLineEdit()
        self.txt_busca_aluno.setPlaceholderText("Buscar aluno por nome ou CPF...")
        self.txt_busca_aluno.setMinimumHeight(40)
        self.txt_busca_aluno.textChanged.connect(self.buscar_alunos_sem_turma)

        # Tabela de alunos sem turma
        lbl_selecionar = QLabel("Alunos sem turma (selecione para adicionar):")
        lbl_selecionar.setStyleSheet("font-weight: 600; color: #2c3e50;")

        self.tabela_alunos = QTableWidget()
        self.tabela_alunos.setColumnCount(6)
        self.tabela_alunos.setHorizontalHeaderLabels([
            "ID", "Nome", "CPF", "Data Nasc.", "SÃ©rie", "Status"
        ])

        # Configurar tabela
        self.tabela_alunos.setAlternatingRowColors(True)
        self.tabela_alunos.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela_alunos.setSelectionMode(QTableWidget.ExtendedSelection)
        self.tabela_alunos.setEditTriggers(QTableWidget.NoEditTriggers)

        # Ocultar coluna ID
        self.tabela_alunos.setColumnHidden(0, True)

        # Ajustar largura das colunas
        header = self.tabela_alunos.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Nome

        # InformaÃ§Ãµes do aluno selecionado
        self.lbl_info_selecionado = QLabel("Nenhum aluno selecionado.")
        self.lbl_info_selecionado.setStyleSheet("""
            QLabel {
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 6px;
                border: 1px solid #dce1e6;
                color: #7f8c8d;
                font-size: 13px;
            }
        """)
        self.lbl_info_selecionado.setWordWrap(True)

        # Conectar seleÃ§Ã£o
        self.tabela_alunos.itemSelectionChanged.connect(self.aluno_selecionado)

        # BotÃµes
        botoes_layout = QHBoxLayout()

        self.btn_adicionar = AnimacaoBotao("ADICIONAR Ã€ TURMA", cor_normal="#27ae60", cor_hover="#219653",
                                           cor_press="#1e874b")
        self.btn_adicionar.setMinimumHeight(45)
        self.btn_adicionar.clicked.connect(self.adicionar_alunos_selecionados)
        self.btn_adicionar.setEnabled(False)

        btn_cancelar = QPushButton("CANCELAR")
        btn_cancelar.setObjectName("danger")
        btn_cancelar.setMinimumHeight(45)
        btn_cancelar.clicked.connect(self.reject)

        botoes_layout.addWidget(self.btn_adicionar)
        botoes_layout.addStretch()
        botoes_layout.addWidget(btn_cancelar)

        # Adicionar tudo ao layout
        layout.addWidget(lbl_titulo)
        layout.addWidget(lbl_info_turma)
        layout.addWidget(self.txt_busca_aluno)
        layout.addWidget(lbl_selecionar)
        layout.addWidget(self.tabela_alunos)
        layout.addWidget(self.lbl_info_selecionado)
        layout.addLayout(botoes_layout)

    def carregar_alunos_sem_turma(self):
        """Carrega alunos sem turma atribuÃ­da"""
        try:
            self.alunos_sem_turma = self.db.execute_query('''
                SELECT id, nome, cpf, data_nascimento, serie, status
                FROM alunos
                WHERE (turma IS NULL OR turma = '') AND status = 'Ativo'
                ORDER BY nome
            ''', fetch=True)

            self.atualizar_tabela_alunos(self.alunos_sem_turma)

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar alunos sem turma:\n{str(e)}")

    def atualizar_tabela_alunos(self, alunos):
        """Atualiza a tabela com a lista de alunos fornecida"""
        self.tabela_alunos.setRowCount(0)

        for row, (id_aluno, nome, cpf, data_nasc, serie, status) in enumerate(alunos):
            self.tabela_alunos.insertRow(row)

            # ID (oculto)
            self.tabela_alunos.setItem(row, 0, QTableWidgetItem(str(id_aluno)))

            # Nome
            self.tabela_alunos.setItem(row, 1, QTableWidgetItem(nome))

            # CPF formatado
            cpf_formatado = ValidadorCampos.formatar_cpf(cpf) if cpf else "-"
            self.tabela_alunos.setItem(row, 2, QTableWidgetItem(cpf_formatado))

            # Data de nascimento formatada
            if data_nasc:
                try:
                    data_obj = datetime.strptime(data_nasc, '%Y-%m-%d')
                    data_formatada = data_obj.strftime('%d/%m/%Y')
                except:
                    data_formatada = data_nasc
            else:
                data_formatada = "-"

            self.tabela_alunos.setItem(row, 3, QTableWidgetItem(data_formatada))

            # SÃ©rie
            self.tabela_alunos.setItem(row, 4, QTableWidgetItem(serie if serie else "-"))

            # Status
            item_status = QTableWidgetItem(status if status else "-")

            if status == "Ativo":
                item_status.setForeground(QColor('#27ae60'))
            else:
                item_status.setForeground(QColor('#e74c3c'))

            self.tabela_alunos.setItem(row, 5, item_status)

    def buscar_alunos_sem_turma(self):
        """Busca alunos sem turma baseado no texto da busca"""
        texto = self.txt_busca_aluno.text().strip().lower()

        if not texto:
            self.atualizar_tabela_alunos(self.alunos_sem_turma)
            return

        alunos_filtrados = []

        for aluno in self.alunos_sem_turma:
            # Verificar se o texto estÃ¡ em nome ou CPF
            id_aluno, nome, cpf, data_nasc, serie, status = aluno

            if texto in nome.lower() or (cpf and texto in cpf.lower()):
                alunos_filtrados.append(aluno)

        self.atualizar_tabela_alunos(alunos_filtrados)

    def aluno_selecionado(self):
        """Quando um aluno Ã© selecionado na tabela"""
        selecionados = self.tabela_alunos.selectedItems()

        if not selecionados:
            self.lbl_info_selecionado.setText("Nenhum aluno selecionado.")
            self.btn_adicionar.setEnabled(False)
            return

        # Obter IDs Ãºnicos dos alunos selecionados
        rows_selecionadas = set()

        for item in selecionados:
            rows_selecionadas.add(item.row())

        if len(rows_selecionadas) == 1:
            row = list(rows_selecionadas)[0]
            nome = self.tabela_alunos.item(row, 1).text()
            cpf = self.tabela_alunos.item(row, 2).text()
            serie = self.tabela_alunos.item(row, 4).text()

            self.lbl_info_selecionado.setText(
                f"Aluno selecionado: {nome}\n"
                f"CPF: {cpf} | SÃ©rie: {serie}"
            )
        else:
            self.lbl_info_selecionado.setText(f"{len(rows_selecionadas)} alunos selecionados.")

        self.btn_adicionar.setEnabled(True)

    def adicionar_alunos_selecionados(self):
        """Adiciona alunos selecionados Ã  turma"""
        selecionados = self.tabela_alunos.selectedItems()

        if not selecionados:
            QMessageBox.warning(self, "SeleÃ§Ã£o necessÃ¡ria",
                                "Por favor, selecione um ou mais alunos.")
            return

        # Obter IDs Ãºnicos dos alunos selecionados
        ids_alunos = set()
        rows_selecionadas = set()

        for item in selecionados:
            row = item.row()
            rows_selecionadas.add(row)

        for row in rows_selecionadas:
            id_aluno = int(self.tabela_alunos.item(row, 0).text())
            ids_alunos.add(id_aluno)

        try:
            for id_aluno in ids_alunos:
                self.db.execute_query(
                    "UPDATE alunos SET turma = ? WHERE id = ?",
                    (self.nome_turma, id_aluno)
                )

            QMessageBox.information(self, "Sucesso",
                                    f"{len(ids_alunos)} aluno(s) adicionado(s) Ã  turma {self.nome_turma} com sucesso!")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao adicionar alunos Ã  turma:\n{str(e)}")


# ============================================
# DIÃLOGO DE TRANSFERIR ALUNO
# ============================================

class TransferirAlunoDialog(QDialog):
    """DiÃ¡logo para transferir aluno para outra turma"""

    def __init__(self, parent=None, id_aluno=None, nome_aluno="", turma_atual=""):
        super().__init__(parent)
        self.id_aluno = id_aluno
        self.nome_aluno = nome_aluno
        self.turma_atual = turma_atual
        self.db = DatabaseManager()

        self.setWindowTitle(f"Transferir Aluno - {nome_aluno}")
        self.setFixedSize(500, 400)
        self.setStyleSheet(GLOBAL_STYLESHEET)

        self.init_ui()
        self.carregar_turmas_disponiveis()

    def init_ui(self):
        """Inicializa a interface do diÃ¡logo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # TÃ­tulo
        lbl_titulo = QLabel("TRANSFERIR ALUNO")
        lbl_titulo.setObjectName("title")

        # InformaÃ§Ãµes do aluno
        lbl_info_aluno = QLabel(f"Aluno: {self.nome_aluno}")
        lbl_info_aluno.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 600;
                color: #2c3e50;
                padding: 10px;
                background-color: #fef5e7;
                border-radius: 6px;
                border: 1px solid #f39c12;
            }
        """)

        lbl_turma_atual = QLabel(f"Turma atual: {self.turma_atual if self.turma_atual else 'Nenhuma'}")
        lbl_turma_atual.setStyleSheet("font-weight: 600; color: #f39c12;")

        # Selecionar nova turma
        lbl_selecionar = QLabel("Selecione a nova turma:")
        lbl_selecionar.setStyleSheet("font-weight: 600; color: #2c3e50;")

        self.combo_turmas = QComboBox()

        # ObservaÃ§Ã£o
        self.txt_observacao = QTextEdit()
        self.txt_observacao.setMaximumHeight(80)
        self.txt_observacao.setPlaceholderText("ObservaÃ§Ã£o sobre a transferÃªncia (opcional)...")

        # BotÃµes
        botoes_layout = QHBoxLayout()

        btn_transferir = AnimacaoBotao("TRANSFERIR", cor_normal="#27ae60", cor_hover="#219653", cor_press="#1e874b")
        btn_transferir.setMinimumHeight(45)
        btn_transferir.clicked.connect(self.transferir_aluno)

        btn_cancelar = QPushButton("CANCELAR")
        btn_cancelar.setObjectName("danger")
        btn_cancelar.setMinimumHeight(45)
        btn_cancelar.clicked.connect(self.reject)

        botoes_layout.addWidget(btn_transferir)
        botoes_layout.addStretch()
        botoes_layout.addWidget(btn_cancelar)

        # Adicionar tudo ao layout
        layout.addWidget(lbl_titulo)
        layout.addWidget(lbl_info_aluno)
        layout.addWidget(lbl_turma_atual)
        layout.addWidget(lbl_selecionar)
        layout.addWidget(self.combo_turmas)
        layout.addWidget(QLabel("ObservaÃ§Ã£o:"))
        layout.addWidget(self.txt_observacao)
        layout.addStretch()
        layout.addLayout(botoes_layout)

    def carregar_turmas_disponiveis(self):
        """Carrega turmas disponÃ­veis para transferÃªncia"""
        try:
            turmas = self.db.execute_query('''
                SELECT id, nome, serie, turno, capacidade,
                       (SELECT COUNT(*) FROM alunos WHERE turma = turmas.nome AND status = 'Ativo') as alunos
                FROM turmas
                WHERE ativa = 1
                ORDER BY serie, nome
            ''', fetch=True)

            self.combo_turmas.clear()

            for id_turma, nome, serie, turno, capacidade, alunos in turmas:
                # NÃ£o incluir a turma atual
                if nome == self.turma_atual:
                    continue

                # Verificar se hÃ¡ vagas
                vagas = capacidade - alunos if capacidade else "?"
                texto = f"{nome} - {serie} ({turno}) | Vagas: {vagas}"

                self.combo_turmas.addItem(texto, id_turma)

            if self.combo_turmas.count() == 0:
                self.combo_turmas.addItem("Nenhuma turma disponÃ­vel", -1)

        except Exception as e:
            print(f"Erro ao carregar turmas: {e}")

    def transferir_aluno(self):
        """Realiza a transferÃªncia do aluno"""
        if self.combo_turmas.currentData() == -1:
            QMessageBox.warning(self, "Nenhuma turma disponÃ­vel",
                                "NÃ£o hÃ¡ turmas disponÃ­veis para transferÃªncia.")
            return

        nova_turma_id = self.combo_turmas.currentData()
        nova_turma_nome = self.combo_turmas.currentText().split(" - ")[0]
        observacao = self.txt_observacao.toPlainText().strip()

        resposta = QMessageBox.question(
            self, "Confirmar transferÃªncia",
            f"Transferir aluno {self.nome_aluno} para a turma {nova_turma_nome}?\n\n"
            f"Turma atual: {self.turma_atual}\n"
            f"Nova turma: {nova_turma_nome}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            try:
                # Atualizar turma do aluno
                self.db.execute_query(
                    "UPDATE alunos SET turma = ? WHERE id = ?",
                    (nova_turma_nome, self.id_aluno)
                )

                # Registrar histÃ³rico de transferÃªncia (se houver tabela de histÃ³rico)
                try:
                    self.db.execute_query('''
                        INSERT INTO historico_transferencias 
                        (aluno_id, turma_antiga, turma_nova, data_transferencia, observacao)
                        VALUES (?, ?, ?, CURRENT_TIMESTAMP, ?)
                    ''', (self.id_aluno, self.turma_atual, nova_turma_nome, observacao))
                except:
                    pass  # Tabela de histÃ³rico pode nÃ£o existir

                QMessageBox.information(self, "Sucesso",
                                        f"Aluno transferido com sucesso para {nova_turma_nome}!")
                self.accept()

            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Falha ao transferir aluno:\n{str(e)}")

    # ============================================
    # PÃGINA DE NOTAS (COMPLETA)
    # ============================================

    def criar_pagina_notas(self):
        """Cria a pÃ¡gina de lanÃ§amento de notas - COMPLETA"""
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # CabeÃ§alho
        cabecalho_layout = QHBoxLayout()

        lbl_titulo = QLabel("LANÃ‡AMENTO DE NOTAS")
        lbl_titulo.setObjectName("title")

        # Filtros
        filtros_layout = QGridLayout()
        filtros_layout.setSpacing(15)

        # Filtro por turma
        lbl_turma = QLabel("Turma:")
        self.combo_turma_notas = QComboBox()
        self.combo_turma_notas.addItem("Selecione uma turma")
        self.combo_turma_notas.currentIndexChanged.connect(self.filtrar_por_turma_notas)

        # Filtro por disciplina
        lbl_disciplina = QLabel("Disciplina:")
        self.combo_disciplina_notas = QComboBox()
        self.combo_disciplina_notas.addItem("Selecione uma disciplina")
        self.combo_disciplina_notas.currentIndexChanged.connect(self.filtrar_por_disciplina_notas)

        # Filtro por bimestre
        lbl_bimestre = QLabel("Bimestre:")
        self.combo_bimestre_notas = QComboBox()
        self.combo_bimestre_notas.addItems(["1Âº Bimestre", "2Âº Bimestre", "3Âº Bimestre", "4Âº Bimestre"])
        self.combo_bimestre_notas.currentIndexChanged.connect(self.carregar_notas_turma)

        # BotÃ£o para carregar
        btn_carregar = AnimacaoBotao("Carregar", cor_normal="#3498db", cor_hover="#2980b9", cor_press="#1c6ea4")
        btn_carregar.clicked.connect(self.carregar_notas_turma)

        filtros_layout.addWidget(lbl_turma, 0, 0)
        filtros_layout.addWidget(self.combo_turma_notas, 0, 1)
        filtros_layout.addWidget(lbl_disciplina, 0, 2)
        filtros_layout.addWidget(self.combo_disciplina_notas, 0, 3)
        filtros_layout.addWidget(lbl_bimestre, 1, 0)
        filtros_layout.addWidget(self.combo_bimestre_notas, 1, 1)
        filtros_layout.addWidget(btn_carregar, 1, 3)

        # Tabela de notas
        self.tabela_notas = QTableWidget()
        self.tabela_notas.setColumnCount(10)
        self.tabela_notas.setHorizontalHeaderLabels([
            "ID Aluno", "Nome", "Nota 1", "Nota 2", "Nota 3", "Nota 4",
            "MÃ©dia", "Faltas", "SituaÃ§Ã£o", "ObservaÃ§Ãµes"
        ])

        # Configurar tabela
        self.tabela_notas.setAlternatingRowColors(True)
        self.tabela_notas.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.EditKeyPressed)

        # Ocultar coluna ID
        self.tabela_notas.setColumnHidden(0, True)

        # Ajustar largura das colunas
        header = self.tabela_notas.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Nome
        header.setSectionResizeMode(9, QHeaderView.ResizeToContents)  # ObservaÃ§Ãµes

        # Configurar validadores para campos numÃ©ricos
        for col in [2, 3, 4, 5, 6, 7]:  # Colunas de notas e faltas
            self.tabela_notas.horizontalHeaderItem(col).setToolTip("Clique duas vezes para editar")

        # BotÃµes de aÃ§Ã£o
        botoes_layout = QHBoxLayout()

        btn_salvar = AnimacaoBotao("Salvar Notas", cor_normal="#27ae60", cor_hover="#219653", cor_press="#1e874b")
        btn_salvar.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        btn_salvar.clicked.connect(self.salvar_notas)

        btn_calcular = AnimacaoBotao("Calcular MÃ©dias", cor_normal="#3498db", cor_hover="#2980b9", cor_press="#1c6ea4")
        btn_calcular.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        btn_calcular.clicked.connect(self.calcular_medias)

        btn_limpar = AnimacaoBotao("Limpar", cor_normal="#f39c12", cor_hover="#d68910", cor_press="#b9770e")
        btn_limpar.setIcon(self.style().standardIcon(QStyle.SP_DialogResetButton))
        btn_limpar.clicked.connect(self.limpar_notas)

        btn_exportar = AnimacaoBotao("Exportar", cor_normal="#9b59b6", cor_hover="#8e44ad", cor_press="#7d3c98")
        btn_exportar.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        btn_exportar.clicked.connect(self.exportar_notas)

        botoes_layout.addWidget(btn_salvar)
        botoes_layout.addWidget(btn_calcular)
        botoes_layout.addWidget(btn_limpar)
        botoes_layout.addWidget(btn_exportar)
        botoes_layout.addStretch()

        # EstatÃ­sticas
        self.lbl_estatisticas = QLabel("Selecione uma turma e disciplina para comeÃ§ar")
        self.lbl_estatisticas.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #2c3e50;
                font-weight: 600;
                padding: 10px;
                background-color: #f8f9fa;
                border-radius: 6px;
                border: 1px solid #dce1e6;
            }
        """)

        # Adicionar tudo ao layout
        layout.addWidget(lbl_titulo)
        layout.addLayout(filtros_layout)
        layout.addWidget(self.tabela_notas)
        layout.addWidget(self.lbl_estatisticas)
        layout.addLayout(botoes_layout)

        self.paginas['notas'] = pagina
        self.central_widget.addWidget(pagina)

        # Carregar turmas disponÃ­veis
        self.carregar_turmas_notas()

    def carregar_turmas_notas(self):
        """Carrega turmas disponÃ­veis para lanÃ§amento de notas"""
        try:
            turmas = self.db.execute_query('''
                SELECT id, nome, serie 
                FROM turmas 
                WHERE ativa = 1
                ORDER BY serie, nome
            ''', fetch=True)

            self.combo_turma_notas.clear()
            self.combo_turma_notas.addItem("Selecione uma turma")

            for id_turma, nome, serie in turmas:
                texto = f"{nome} - {serie}" if serie else nome
                self.combo_turma_notas.addItem(texto, id_turma)

        except Exception as e:
            print(f"Erro ao carregar turmas: {e}")

    def filtrar_por_turma_notas(self):
        """Filtra disciplinas quando uma turma Ã© selecionada"""
        turma_id = self.combo_turma_notas.currentData()

        if not turma_id or self.combo_turma_notas.currentIndex() == 0:
            self.combo_disciplina_notas.clear()
            self.combo_disciplina_notas.addItem("Selecione uma disciplina")
            return

        try:
            # Obter disciplinas ministradas para a turma selecionada
            disciplinas = self.db.execute_query('''
                SELECT DISTINCT d.id, d.nome, d.serie
                FROM horarios h
                JOIN disciplinas d ON h.disciplina_id = d.id
                WHERE h.turma_id = ? AND h.ativo = 1 AND d.ativa = 1
                ORDER BY d.nome
            ''', (turma_id,), fetch=True)

            self.combo_disciplina_notas.clear()
            self.combo_disciplina_notas.addItem("Selecione uma disciplina")

            for id_disciplina, nome, serie in disciplinas:
                texto = f"{nome} ({serie})" if serie else nome
                self.combo_disciplina_notas.addItem(texto, id_disciplina)

        except Exception as e:
            print(f"Erro ao carregar disciplinas: {e}")

    def filtrar_por_disciplina_notas(self):
        """Filtra alunos quando uma disciplina Ã© selecionada"""
        if (self.combo_turma_notas.currentIndex() > 0 and
                self.combo_disciplina_notas.currentIndex() > 0):
            self.carregar_notas_turma()

    def carregar_notas_turma(self):
        """Carrega notas dos alunos da turma selecionada"""
        turma_id = self.combo_turma_notas.currentData()
        disciplina_id = self.combo_disciplina_notas.currentData()
        bimestre = self.combo_bimestre_notas.currentIndex() + 1

        if not turma_id or self.combo_turma_notas.currentIndex() == 0:
            return

        if not disciplina_id or self.combo_disciplina_notas.currentIndex() == 0:
            return

        try:
            # Obter nome da turma
            turma_nome_result = self.db.execute_query(
                "SELECT nome FROM turmas WHERE id = ?",
                (turma_id,),
                fetch=True
            )

            if not turma_nome_result:
                return

            turma_nome = turma_nome_result[0][0]

            # Obter alunos da turma
            alunos = self.db.execute_query('''
                SELECT id, nome 
                FROM alunos 
                WHERE turma = ? AND status = 'Ativo'
                ORDER BY nome
            ''', (turma_nome,), fetch=True)

            self.tabela_notas.setRowCount(len(alunos))

            for row, (id_aluno, nome_aluno) in enumerate(alunos):
                # ID Aluno (oculto)
                self.tabela_notas.setItem(row, 0, QTableWidgetItem(str(id_aluno)))

                # Nome
                self.tabela_notas.setItem(row, 1, QTableWidgetItem(nome_aluno))

                # Obter notas existentes
                notas_existentes = self.db.execute_query('''
                    SELECT nota1, nota2, nota3, nota4, media, faltas, situacao, observacoes
                    FROM notas
                    WHERE aluno_id = ? AND disciplina_id = ? AND bimestre = ?
                ''', (id_aluno, disciplina_id, bimestre), fetch=True)

                # Campos de notas (2-5)
                for col in range(2, 6):
                    nota_item = QTableWidgetItem()
                    nota_item.setTextAlignment(Qt.AlignCenter)

                    if notas_existentes and len(notas_existentes) > 0:
                        nota_valor = notas_existentes[0][col - 2]
                        if nota_valor is not None:
                            nota_item.setText(f"{nota_valor:.1f}")

                    self.tabela_notas.setItem(row, col, nota_item)

                # MÃ©dia (6)
                media_item = QTableWidgetItem()
                media_item.setTextAlignment(Qt.AlignCenter)

                if notas_existentes and len(notas_existentes) > 0:
                    media_valor = notas_existentes[0][4]
                    if media_valor is not None:
                        media_item.setText(f"{media_valor:.1f}")

                        # Colorir mÃ©dia
                        if media_valor < 5.0:
                            media_item.setForeground(QColor('#e74c3c'))
                            media_item.setFont(QFont('', weight=QFont.Bold))
                        elif media_valor < 7.0:
                            media_item.setForeground(QColor('#f39c12'))
                        else:
                            media_item.setForeground(QColor('#27ae60'))

                self.tabela_notas.setItem(row, 6, media_item)

                # Faltas (7)
                faltas_item = QTableWidgetItem()
                faltas_item.setTextAlignment(Qt.AlignCenter)

                if notas_existentes and len(notas_existentes) > 0:
                    faltas_valor = notas_existentes[0][5]
                    if faltas_valor is not None:
                        faltas_item.setText(str(faltas_valor))

                self.tabela_notas.setItem(row, 7, faltas_item)

                # SituaÃ§Ã£o (8)
                situacao_item = QTableWidgetItem()
                situacao_item.setTextAlignment(Qt.AlignCenter)

                if notas_existentes and len(notas_existentes) > 0:
                    situacao_valor = notas_existentes[0][6]
                    if situacao_valor:
                        situacao_item.setText(situacao_valor)

                        # Colorir situaÃ§Ã£o
                        if situacao_valor == "Aprovado":
                            situacao_item.setForeground(QColor('#27ae60'))
                            situacao_item.setFont(QFont('', weight=QFont.Bold))
                        elif situacao_valor == "Reprovado":
                            situacao_item.setForeground(QColor('#e74c3c'))
                        else:
                            situacao_item.setForeground(QColor('#f39c12'))

                self.tabela_notas.setItem(row, 8, situacao_item)

                # ObservaÃ§Ãµes (9)
                observacoes_item = QTableWidgetItem()

                if notas_existentes and len(notas_existentes) > 0:
                    obs_valor = notas_existentes[0][7]
                    if obs_valor:
                        observacoes_item.setText(obs_valor)

                self.tabela_notas.setItem(row, 9, observacoes_item)

            # Atualizar estatÃ­sticas
            self.atualizar_estatisticas_notas()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar notas:\n{str(e)}")

    def atualizar_estatisticas_notas(self):
        """Atualiza as estatÃ­sticas das notas carregadas"""
        total_alunos = self.tabela_notas.rowCount()

        if total_alunos == 0:
            self.lbl_estatisticas.setText("Nenhum aluno encontrado para esta turma/disciplina.")
            return

        # Contadores
        notas_preenchidas = 0
        soma_medias = 0
        aprovados = 0
        reprovados = 0
        recuperacao = 0

        for row in range(total_alunos):
            # Verificar mÃ©dia
            media_item = self.tabela_notas.item(row, 6)
            if media_item and media_item.text():
                try:
                    media = float(media_item.text())
                    soma_medias += media
                    notas_preenchidas += 1

                    # Contar por situaÃ§Ã£o
                    situacao_item = self.tabela_notas.item(row, 8)
                    if situacao_item:
                        situacao = situacao_item.text()
                        if situacao == "Aprovado":
                            aprovados += 1
                        elif situacao == "Reprovado":
                            reprovados += 1
                        elif situacao == "RecuperaÃ§Ã£o":
                            recuperacao += 1
                except:
                    pass

        # Calcular mÃ©dia geral
        media_geral = soma_medias / notas_preenchidas if notas_preenchidas > 0 else 0

        # Obter informaÃ§Ãµes da turma e disciplina
        turma_texto = self.combo_turma_notas.currentText()
        disciplina_texto = self.combo_disciplina_notas.currentText()
        bimestre_texto = self.combo_bimestre_notas.currentText()

        self.lbl_estatisticas.setText(
            f"{turma_texto} | {disciplina_texto} | {bimestre_texto} | "
            f"Total de alunos: {total_alunos} | "
            f"MÃ©dia geral: {media_geral:.1f} | "
            f"Aprovados: {aprovados} | RecuperaÃ§Ã£o: {recuperacao} | Reprovados: {reprovados}"
        )

    def calcular_medias(self):
        """Calcula mÃ©dias para todos os alunos na tabela"""
        try:
            for row in range(self.tabela_notas.rowCount()):
                # Obter notas
                notas = []
                for col in range(2, 6):  # Colunas 2-5: Nota1 a Nota4
                    item = self.tabela_notas.item(row, col)
                    if item and item.text().strip():
                        try:
                            nota = float(item.text())
                            notas.append(nota)
                        except:
                            pass

                # Calcular mÃ©dia se houver pelo menos uma nota
                if notas:
                    media = sum(notas) / len(notas)

                    # Atualizar cÃ©lula de mÃ©dia
                    media_item = self.tabela_notas.item(row, 6)
                    if not media_item:
                        media_item = QTableWidgetItem()
                        self.tabela_notas.setItem(row, 6, media_item)

                    media_item.setText(f"{media:.1f}")
                    media_item.setTextAlignment(Qt.AlignCenter)

                    # Colorir mÃ©dia
                    if media < 5.0:
                        media_item.setForeground(QColor('#e74c3c'))
                        media_item.setFont(QFont('', weight=QFont.Bold))

                        # Atualizar situaÃ§Ã£o
                        situacao_item = self.tabela_notas.item(row, 8)
                        if not situacao_item:
                            situacao_item = QTableWidgetItem()
                            self.tabela_notas.setItem(row, 8, situacao_item)

                        situacao_item.setText("Reprovado")
                        situacao_item.setForeground(QColor('#e74c3c'))

                    elif media < 7.0:
                        media_item.setForeground(QColor('#f39c12'))

                        # Atualizar situaÃ§Ã£o
                        situacao_item = self.tabela_notas.item(row, 8)
                        if not situacao_item:
                            situacao_item = QTableWidgetItem()
                            self.tabela_notas.setItem(row, 8, situacao_item)

                        situacao_item.setText("RecuperaÃ§Ã£o")
                        situacao_item.setForeground(QColor('#f39c12'))

                    else:
                        media_item.setForeground(QColor('#27ae60'))

                        # Atualizar situaÃ§Ã£o
                        situacao_item = self.tabela_notas.item(row, 8)
                        if not situacao_item:
                            situacao_item = QTableWidgetItem()
                            self.tabela_notas.setItem(row, 8, situacao_item)

                        situacao_item.setText("Aprovado")
                        situacao_item.setForeground(QColor('#27ae60'))

            # Atualizar estatÃ­sticas
            self.atualizar_estatisticas_notas()

            QMessageBox.information(self, "MÃ©dias calculadas",
                                    "MÃ©dias calculadas com sucesso para todos os alunos!")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao calcular mÃ©dias:\n{str(e)}")

    def salvar_notas(self):
        """Salva todas as notas da tabela no banco de dados"""
        turma_id = self.combo_turma_notas.currentData()
        disciplina_id = self.combo_disciplina_notas.currentData()
        bimestre = self.combo_bimestre_notas.currentIndex() + 1

        if not turma_id or self.combo_turma_notas.currentIndex() == 0:
            QMessageBox.warning(self, "SeleÃ§Ã£o necessÃ¡ria",
                                "Por favor, selecione uma turma.")
            return

        if not disciplina_id or self.combo_disciplina_notas.currentIndex() == 0:
            QMessageBox.warning(self, "SeleÃ§Ã£o necessÃ¡ria",
                                "Por favor, selecione uma disciplina.")
            return

        try:
            total_salvos = 0
            total_atualizados = 0

            for row in range(self.tabela_notas.rowCount()):
                aluno_id = int(self.tabela_notas.item(row, 0).text())

                # Obter valores das cÃ©lulas
                notas = []
                for col in range(2, 6):  # Nota1 a Nota4
                    item = self.tabela_notas.item(row, col)
                    notas.append(float(item.text()) if item and item.text().strip() else None)

                media_item = self.tabela_notas.item(row, 6)
                media = float(media_item.text()) if media_item and media_item.text().strip() else None

                faltas_item = self.tabela_notas.item(row, 7)
                faltas = int(faltas_item.text()) if faltas_item and faltas_item.text().strip() else None

                situacao_item = self.tabela_notas.item(row, 8)
                situacao = situacao_item.text() if situacao_item and situacao_item.text().strip() else None

                observacoes_item = self.tabela_notas.item(row, 9)
                observacoes = observacoes_item.text() if observacoes_item and observacoes_item.text().strip() else None

                # Verificar se jÃ¡ existe registro
                existente = self.db.execute_query('''
                    SELECT id FROM notas 
                    WHERE aluno_id = ? AND disciplina_id = ? AND bimestre = ?
                ''', (aluno_id, disciplina_id, bimestre), fetch=True)

                if existente and len(existente) > 0:
                    # Atualizar registro existente
                    query = '''
                        UPDATE notas SET
                            nota1 = ?, nota2 = ?, nota3 = ?, nota4 = ?,
                            media = ?, faltas = ?, situacao = ?, observacoes = ?
                        WHERE id = ?
                    '''

                    self.db.execute_query(query, (
                        notas[0], notas[1], notas[2], notas[3],
                        media, faltas, situacao, observacoes,
                        existente[0][0]
                    ))

                    total_atualizados += 1
                else:
                    # Inserir novo registro
                    query = '''
                        INSERT INTO notas (
                            aluno_id, disciplina_id, bimestre,
                            nota1, nota2, nota3, nota4,
                            media, faltas, situacao, observacoes,
                            data_lancamento
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    '''

                    self.db.execute_query(query, (
                        aluno_id, disciplina_id, bimestre,
                        notas[0], notas[1], notas[2], notas[3],
                        media, faltas, situacao, observacoes
                    ))

                    total_salvos += 1

            # Atualizar estatÃ­sticas
            self.atualizar_estatisticas_notas()

            QMessageBox.information(self, "Notas salvas",
                                    f"Notas salvas com sucesso!\n\n"
                                    f"Novos registros: {total_salvos}\n"
                                    f"Registros atualizados: {total_atualizados}")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao salvar notas:\n{str(e)}")

    def limpar_notas(self):
        """Limpa todas as notas da tabela"""
        resposta = QMessageBox.question(
            self, "Confirmar limpeza",
            "Tem certeza que deseja limpar todas as notas da tabela?\n\n"
            "Esta aÃ§Ã£o nÃ£o afeta os dados salvos no banco.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            for row in range(self.tabela_notas.rowCount()):
                for col in range(2, 10):  # Colunas 2-9
                    item = self.tabela_notas.item(row, col)
                    if item:
                        item.setText("")

            self.atualizar_estatisticas_notas()

    def exportar_notas(self):
        """Exporta as notas para um arquivo"""
        QMessageBox.information(self, "Funcionalidade em desenvolvimento",
                                "A exportaÃ§Ã£o de notas serÃ¡ implementada na prÃ³xima versÃ£o.")


"""
PROJETO ESCOLA - SISTEMA DE GESTÃƒO ESCOLAR
Parte 6/10 - ContinuaÃ§Ã£o: PÃ¡gina de FrequÃªncia
"""


# ============================================
# PÃGINA DE FREQUÃŠNCIA (COMPLETA)
# ============================================

def criar_pagina_frequencia(self):
    """Cria a pÃ¡gina de registro de frequÃªncia - COMPLETA"""
    pagina = QWidget()
    layout = QVBoxLayout(pagina)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(20)

    # CabeÃ§alho
    cabecalho_layout = QHBoxLayout()

    lbl_titulo = QLabel("REGISTRO DE FREQUÃŠNCIA")
    lbl_titulo.setObjectName("title")

    # Filtros
    filtros_layout = QGridLayout()
    filtros_layout.setSpacing(15)

    # Filtro por data
    lbl_data = QLabel("Data:")
    self.date_frequencia = QDateEdit()
    self.date_frequencia.setCalendarPopup(True)
    self.date_frequencia.setDate(QDate.currentDate())
    self.date_frequencia.setDisplayFormat("dd/MM/yyyy")
    self.date_frequencia.dateChanged.connect(self.carregar_frequencia_data)

    # Filtro por turma
    lbl_turma = QLabel("Turma:")
    self.combo_turma_frequencia = QComboBox()
    self.combo_turma_frequencia.addItem("Selecione uma turma")
    self.combo_turma_frequencia.currentIndexChanged.connect(self.filtrar_por_turma_frequencia)

    # Filtro por disciplina
    lbl_disciplina = QLabel("Disciplina:")
    self.combo_disciplina_frequencia = QComboBox()
    self.combo_disciplina_frequencia.addItem("Selecione uma disciplina")

    # BotÃ£o para carregar
    btn_carregar = AnimacaoBotao("Carregar", cor_normal="#3498db", cor_hover="#2980b9", cor_press="#1c6ea4")
    btn_carregar.clicked.connect(self.carregar_frequencia_turma)

    # BotÃ£o para marcar todos
    btn_marcar_todos = AnimacaoBotao("Marcar Todos", cor_normal="#27ae60", cor_hover="#219653", cor_press="#1e874b")
    btn_marcar_todos.clicked.connect(self.marcar_todos_presentes)

    # BotÃ£o para desmarcar todos
    btn_desmarcar_todos = AnimacaoBotao("Desmarcar Todos", cor_normal="#e74c3c", cor_hover="#c0392b",
                                        cor_press="#a93226")
    btn_desmarcar_todos.clicked.connect(self.desmarcar_todos_presentes)

    filtros_layout.addWidget(lbl_data, 0, 0)
    filtros_layout.addWidget(self.date_frequencia, 0, 1)
    filtros_layout.addWidget(lbl_turma, 0, 2)
    filtros_layout.addWidget(self.combo_turma_frequencia, 0, 3)
    filtros_layout.addWidget(lbl_disciplina, 1, 0)
    filtros_layout.addWidget(self.combo_disciplina_frequencia, 1, 1)
    filtros_layout.addWidget(btn_carregar, 1, 2)
    filtros_layout.addWidget(btn_marcar_todos, 1, 3)
    filtros_layout.addWidget(btn_desmarcar_todos, 1, 4)

    # Tabela de frequÃªncia
    self.tabela_frequencia = QTableWidget()
    self.tabela_frequencia.setColumnCount(7)
    self.tabela_frequencia.setHorizontalHeaderLabels([
        "ID Aluno", "Nome", "Presente", "Chegada", "SaÃ­da", "Justificativa", "ObservaÃ§Ãµes"
    ])

    # Configurar tabela
    self.tabela_frequencia.setAlternatingRowColors(True)

    # Ocultar coluna ID
    self.tabela_frequencia.setColumnHidden(0, True)

    # Ajustar largura das colunas
    header = self.tabela_frequencia.horizontalHeader()
    header.setSectionResizeMode(1, QHeaderView.Stretch)  # Nome
    header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Presente
    header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # ObservaÃ§Ãµes

    # Configurar coluna "Presente" com checkbox
    self.tabela_frequencia.setItemDelegateForColumn(2, CheckBoxDelegate(self.tabela_frequencia))

    # BotÃµes de aÃ§Ã£o
    botoes_layout = QHBoxLayout()

    btn_salvar = AnimacaoBotao("Salvar FrequÃªncia", cor_normal="#27ae60", cor_hover="#219653", cor_press="#1e874b")
    btn_salvar.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
    btn_salvar.clicked.connect(self.salvar_frequencia)

    btn_justificar = AnimacaoBotao("Justificar Faltas", cor_normal="#f39c12", cor_hover="#d68910", cor_press="#b9770e")
    btn_justificar.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation))
    btn_justificar.clicked.connect(self.justificar_faltas)

    btn_relatorio = AnimacaoBotao("RelatÃ³rio", cor_normal="#3498db", cor_hover="#2980b9", cor_press="#1c6ea4")
    btn_relatorio.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
    btn_relatorio.clicked.connect(self.gerar_relatorio_frequencia)

    btn_exportar = AnimacaoBotao("Exportar", cor_normal="#9b59b6", cor_hover="#8e44ad", cor_press="#7d3c98")
    btn_exportar.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
    btn_exportar.clicked.connect(self.exportar_frequencia)

    botoes_layout.addWidget(btn_salvar)
    botoes_layout.addWidget(btn_justificar)
    botoes_layout.addWidget(btn_relatorio)
    botoes_layout.addWidget(btn_exportar)
    botoes_layout.addStretch()

    # EstatÃ­sticas
    self.lbl_estatisticas_freq = QLabel("Selecione uma turma e data para comeÃ§ar")
    self.lbl_estatisticas_freq.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #2c3e50;
                font-weight: 600;
                padding: 10px;
                background-color: #f8f9fa;
                border-radius: 6px;
                border: 1px solid #dce1e6;
            }
        """)

    # Adicionar tudo ao layout
    layout.addWidget(lbl_titulo)
    layout.addLayout(filtros_layout)
    layout.addWidget(self.tabela_frequencia)
    layout.addWidget(self.lbl_estatisticas_freq)
    layout.addLayout(botoes_layout)

    self.paginas['frequencia'] = pagina
    self.central_widget.addWidget(pagina)

    # Carregar turmas disponÃ­veis
    self.carregar_turmas_frequencia()


def carregar_turmas_frequencia(self):
    """Carrega turmas disponÃ­veis para registro de frequÃªncia"""
    try:
        turmas = self.db.execute_query('''
                SELECT id, nome, serie 
                FROM turmas 
                WHERE ativa = 1
                ORDER BY serie, nome
            ''', fetch=True)

        self.combo_turma_frequencia.clear()
        self.combo_turma_frequencia.addItem("Selecione uma turma")

        for id_turma, nome, serie in turmas:
            texto = f"{nome} - {serie}" if serie else nome
            self.combo_turma_frequencia.addItem(texto, id_turma)

    except Exception as e:
        print(f"Erro ao carregar turmas: {e}")


def filtrar_por_turma_frequencia(self):
    """Filtra disciplinas quando uma turma Ã© selecionada"""
    turma_id = self.combo_turma_frequencia.currentData()

    if not turma_id or self.combo_turma_frequencia.currentIndex() == 0:
        self.combo_disciplina_frequencia.clear()
        self.combo_disciplina_frequencia.addItem("Selecione uma disciplina")
        return

    try:
        # Obter disciplinas ministradas para a turma selecionada
        disciplinas = self.db.execute_query('''
                SELECT DISTINCT d.id, d.nome, d.serie
                FROM horarios h
                JOIN disciplinas d ON h.disciplina_id = d.id
                WHERE h.turma_id = ? AND h.ativo = 1 AND d.ativa = 1
                ORDER BY d.nome
            ''', (turma_id,), fetch=True)

        self.combo_disciplina_frequencia.clear()
        self.combo_disciplina_frequencia.addItem("Selecione uma disciplina")
        self.combo_disciplina_frequencia.addItem("Todas as disciplinas", -1)

        for id_disciplina, nome, serie in disciplinas:
            texto = f"{nome} ({serie})" if serie else nome
            self.combo_disciplina_frequencia.addItem(texto, id_disciplina)

    except Exception as e:
        print(f"Erro ao carregar disciplinas: {e}")


def carregar_frequencia_data(self):
    """Carrega frequÃªncia quando a data Ã© alterada"""
    if (self.combo_turma_frequencia.currentIndex() > 0 and
            self.combo_disciplina_frequencia.currentIndex() > 0):
        self.carregar_frequencia_turma()


def carregar_frequencia_turma(self):
    """Carrega frequÃªncia dos alunos da turma selecionada"""
    turma_id = self.combo_turma_frequencia.currentData()
    disciplina_id = self.combo_disciplina_frequencia.currentData()
    data = self.date_frequencia.date().toString("yyyy-MM-dd")

    if not turma_id or self.combo_turma_frequencia.currentIndex() == 0:
        return

    try:
        # Obter nome da turma
        turma_nome_result = self.db.execute_query(
            "SELECT nome FROM turmas WHERE id = ?",
            (turma_id,),
            fetch=True
        )

        if not turma_nome_result:
            return

        turma_nome = turma_nome_result[0][0]

        # Obter alunos da turma
        alunos = self.db.execute_query('''
                SELECT id, nome 
                FROM alunos 
                WHERE turma = ? AND status = 'Ativo'
                ORDER BY nome
            ''', (turma_nome,), fetch=True)

        self.tabela_frequencia.setRowCount(len(alunos))

        for row, (id_aluno, nome_aluno) in enumerate(alunos):
            # ID Aluno (oculto)
            self.tabela_frequencia.setItem(row, 0, QTableWidgetItem(str(id_aluno)))

            # Nome
            nome_item = QTableWidgetItem(nome_aluno)
            self.tabela_frequencia.setItem(row, 1, nome_item)

            # Obter frequÃªncia existente
            frequencia_existente = None

            if disciplina_id != -1:  # Disciplina especÃ­fica
                frequencia_existente = self.db.execute_query('''
                        SELECT presente, hora_chegada, hora_saida, justificativa, observacoes
                        FROM frequencia
                        WHERE aluno_id = ? AND data = ? AND disciplina_id = ?
                    ''', (id_aluno, data, disciplina_id), fetch=True)
            else:  # Todas as disciplinas (buscar qualquer registro do dia)
                frequencia_existente = self.db.execute_query('''
                        SELECT presente, hora_chegada, hora_saida, justificativa, observacoes
                        FROM frequencia
                        WHERE aluno_id = ? AND data = ? 
                        LIMIT 1
                    ''', (id_aluno, data), fetch=True)

            # Presente (Checkbox)
            presente_item = QTableWidgetItem()
            presente_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)

            if frequencia_existente and len(frequencia_existente) > 0:
                presente_valor = frequencia_existente[0][0]
                presente_item.setCheckState(Qt.Checked if presente_valor == 1 else Qt.Unchecked)
            else:
                presente_item.setCheckState(Qt.Checked)  # PadrÃ£o: presente

            self.tabela_frequencia.setItem(row, 2, presente_item)

            # Chegada
            chegada_item = QTableWidgetItem()
            chegada_item.setTextAlignment(Qt.AlignCenter)

            if frequencia_existente and len(frequencia_existente) > 0:
                chegada_valor = frequencia_existente[0][1]
                if chegada_valor:
                    chegada_item.setText(chegada_valor)

            self.tabela_frequencia.setItem(row, 3, chegada_item)

            # SaÃ­da
            saida_item = QTableWidgetItem()
            saida_item.setTextAlignment(Qt.AlignCenter)

            if frequencia_existente and len(frequencia_existente) > 0:
                saida_valor = frequencia_existente[0][2]
                if saida_valor:
                    saida_item.setText(saida_valor)

            self.tabela_frequencia.setItem(row, 4, saida_item)

            # Justificativa
            justificativa_item = QTableWidgetItem()

            if frequencia_existente and len(frequencia_existente) > 0:
                justificativa_valor = frequencia_existente[0][3]
                if justificativa_valor:
                    justificativa_item.setText(justificativa_valor)
                    justificativa_item.setForeground(QColor('#f39c12'))

            self.tabela_frequencia.setItem(row, 5, justificativa_item)

            # ObservaÃ§Ãµes
            observacoes_item = QTableWidgetItem()

            if frequencia_existente and len(frequencia_existente) > 0:
                observacoes_valor = frequencia_existente[0][4]
                if observacoes_valor:
                    observacoes_item.setText(observacoes_valor)

            self.tabela_frequencia.setItem(row, 6, observacoes_item)

        # Atualizar estatÃ­sticas
        self.atualizar_estatisticas_frequencia()

    except Exception as e:
        QMessageBox.critical(self, "Erro", f"Falha ao carregar frequÃªncia:\n{str(e)}")


def atualizar_estatisticas_frequencia(self):
    """Atualiza as estatÃ­sticas da frequÃªncia carregada"""
    total_alunos = self.tabela_frequencia.rowCount()

    if total_alunos == 0:
        self.lbl_estatisticas_freq.setText("Nenhum aluno encontrado para esta turma.")
        return

    # Contadores
    presentes = 0
    faltas = 0
    justificadas = 0

    for row in range(total_alunos):
        presente_item = self.tabela_frequencia.item(row, 2)
        justificativa_item = self.tabela_frequencia.item(row, 5)

        if presente_item and presente_item.checkState() == Qt.Checked:
            presentes += 1
        else:
            faltas += 1

            if justificativa_item and justificativa_item.text().strip():
                justificadas += 1

    # Calcular porcentagens
    percent_presentes = (presentes / total_alunos) * 100 if total_alunos > 0 else 0
    percent_faltas = (faltas / total_alunos) * 100 if total_alunos > 0 else 0

    # Obter informaÃ§Ãµes da turma e data
    turma_texto = self.combo_turma_frequencia.currentText()
    data_texto = self.date_frequencia.date().toString("dd/MM/yyyy")
    disciplina_texto = self.combo_disciplina_frequencia.currentText()

    self.lbl_estatisticas_freq.setText(
        f"{turma_texto} | {data_texto} | {disciplina_texto} | "
        f"Total: {total_alunos} | "
        f"Presentes: {presentes} ({percent_presentes:.1f}%) | "
        f"Faltas: {faltas} ({percent_faltas:.1f}%) | "
        f"Justificadas: {justificadas}"
    )


def marcar_todos_presentes(self):
    """Marca todos os alunos como presentes"""
    for row in range(self.tabela_frequencia.rowCount()):
        item = self.tabela_frequencia.item(row, 2)
        if item:
            item.setCheckState(Qt.Checked)

    self.atualizar_estatisticas_frequencia()


def desmarcar_todos_presentes(self):
    """Desmarca todos os alunos (marca como faltantes)"""
    for row in range(self.tabela_frequencia.rowCount()):
        item = self.tabela_frequencia.item(row, 2)
        if item:
            item.setCheckState(Qt.Unchecked)

    self.atualizar_estatisticas_frequencia()


def justificar_faltas(self):
    """Abre diÃ¡logo para justificar faltas dos alunos selecionados"""
    selecionados = self.tabela_frequencia.selectedItems()

    if not selecionados:
        QMessageBox.warning(self, "SeleÃ§Ã£o necessÃ¡ria",
                            "Por favor, selecione um ou mais alunos para justificar faltas.")
        return

    # Obter linhas Ãºnicas dos alunos selecionados
    rows_selecionadas = set()

    for item in selecionados:
        rows_selecionadas.add(item.row())

    dialog = JustificarFaltasDialog(self, rows_selecionadas)
    if dialog.exec_():
        justificativa = dialog.obter_justificativa()

        for row in rows_selecionadas:
            justificativa_item = self.tabela_frequencia.item(row, 5)
            if not justificativa_item:
                justificativa_item = QTableWidgetItem()
                self.tabela_frequencia.setItem(row, 5, justificativa_item)

            justificativa_item.setText(justificativa)
            justificativa_item.setForeground(QColor('#f39c12'))

            # Marcar como faltante se estiver presente
            presente_item = self.tabela_frequencia.item(row, 2)
            if presente_item and presente_item.checkState() == Qt.Checked:
                presente_item.setCheckState(Qt.Unchecked)

        self.atualizar_estatisticas_frequencia()


def salvar_frequencia(self):
    """Salva todas as frequÃªncias da tabela no banco de dados"""
    turma_id = self.combo_turma_frequencia.currentData()
    disciplina_id = self.combo_disciplina_frequencia.currentData()
    data = self.date_frequencia.date().toString("yyyy-MM-dd")

    if not turma_id or self.combo_turma_frequencia.currentIndex() == 0:
        QMessageBox.warning(self, "SeleÃ§Ã£o necessÃ¡ria",
                            "Por favor, selecione uma turma.")
        return

    if disciplina_id == -1:  # "Todas as disciplinas"
        QMessageBox.warning(self, "Disciplina necessÃ¡ria",
                            "Por favor, selecione uma disciplina especÃ­fica para salvar a frequÃªncia.")
        return

    try:
        total_salvos = 0
        total_atualizados = 0

        for row in range(self.tabela_frequencia.rowCount()):
            aluno_id = int(self.tabela_frequencia.item(row, 0).text())

            # Obter valores das cÃ©lulas
            presente_item = self.tabela_frequencia.item(row, 2)
            presente = 1 if presente_item and presente_item.checkState() == Qt.Checked else 0

            chegada_item = self.tabela_frequencia.item(row, 3)
            chegada = chegada_item.text() if chegada_item and chegada_item.text().strip() else None

            saida_item = self.tabela_frequencia.item(row, 4)
            saida = saida_item.text() if saida_item and saida_item.text().strip() else None

            justificativa_item = self.tabela_frequencia.item(row, 5)
            justificativa = justificativa_item.text() if justificativa_item and justificativa_item.text().strip() else None

            observacoes_item = self.tabela_frequencia.item(row, 6)
            observacoes = observacoes_item.text() if observacoes_item and observacoes_item.text().strip() else None

            # Verificar se jÃ¡ existe registro
            existente = self.db.execute_query('''
                    SELECT id FROM frequencia 
                    WHERE aluno_id = ? AND data = ? AND disciplina_id = ?
                ''', (aluno_id, data, disciplina_id), fetch=True)

            if existente and len(existente) > 0:
                # Atualizar registro existente
                query = '''
                        UPDATE frequencia SET
                            presente = ?, hora_chegada = ?, hora_saida = ?,
                            justificativa = ?, observacoes = ?
                        WHERE id = ?
                    '''

                self.db.execute_query(query, (
                    presente, chegada, saida,
                    justificativa, observacoes,
                    existente[0][0]
                ))

                total_atualizados += 1
            else:
                # Inserir novo registro
                query = '''
                        INSERT INTO frequencia (
                            aluno_id, data, presente, hora_chegada, hora_saida,
                            justificativa, observacoes, disciplina_id
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    '''

                self.db.execute_query(query, (
                    aluno_id, data, presente, chegada, saida,
                    justificativa, observacoes, disciplina_id
                ))

                total_salvos += 1

        # Atualizar estatÃ­sticas
        self.atualizar_estatisticas_frequencia()

        QMessageBox.information(self, "FrequÃªncia salva",
                                f"FrequÃªncia salva com sucesso!\n\n"
                                f"Novos registros: {total_salvos}\n"
                                f"Registros atualizados: {total_atualizados}")

    except Exception as e:
        QMessageBox.critical(self, "Erro", f"Falha ao salvar frequÃªncia:\n{str(e)}")


def gerar_relatorio_frequencia(self):
    """Gera relatÃ³rio de frequÃªncia"""
    QMessageBox.information(self, "Funcionalidade em desenvolvimento",
                            "A geraÃ§Ã£o de relatÃ³rios de frequÃªncia serÃ¡ implementada na prÃ³xima versÃ£o.")


def exportar_frequencia(self):
    """Exporta a frequÃªncia para um arquivo"""
    QMessageBox.information(self, "Funcionalidade em desenvolvimento",
                            "A exportaÃ§Ã£o de frequÃªncia serÃ¡ implementada na prÃ³xima versÃ£o.")


# ============================================
# DELEGATE PARA CHECKBOX NA TABELA
# ============================================

class CheckBoxDelegate(QStyledItemDelegate):
    """Delegate para exibir checkbox em cÃ©lulas de tabela"""

    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        """Cria editor para a cÃ©lula"""
        return None  # NÃ£o cria editor, usamos apenas o checkbox

    def paint(self, painter, option, index):
        """Pinta o checkbox na cÃ©lula"""
        # Obter o estado do checkbox
        checked = index.data(Qt.CheckStateRole) == Qt.Checked

        # Configurar opÃ§Ãµes do checkbox
        checkbox_option = QStyleOptionButton()
        checkbox_option.state |= QStyle.State_Enabled

        if checked:
            checkbox_option.state |= QStyle.State_On
        else:
            checkbox_option.state |= QStyle.State_Off

        # Calcular posiÃ§Ã£o centralizada
        checkbox_rect = QRect(option.rect)
        checkbox_size = QApplication.style().pixelMetric(QStyle.PM_IndicatorWidth)

        checkbox_rect.setLeft(option.rect.left() + (option.rect.width() - checkbox_size) // 2)
        checkbox_rect.setTop(option.rect.top() + (option.rect.height() - checkbox_size) // 2)
        checkbox_rect.setWidth(checkbox_size)
        checkbox_rect.setHeight(checkbox_size)

        checkbox_option.rect = checkbox_rect

        # Desenhar o checkbox
        QApplication.style().drawControl(QStyle.CE_CheckBox, checkbox_option, painter)

    def editorEvent(self, event, model, option, index):
        """Lida com eventos do editor (cliques no checkbox)"""
        if event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
            # Alternar estado do checkbox
            current_state = index.data(Qt.CheckStateRole)
            new_state = Qt.Unchecked if current_state == Qt.Checked else Qt.Checked

            model.setData(index, new_state, Qt.CheckStateRole)
            return True

        return False


# ============================================
# DIÃLOGO DE JUSTIFICAR FALTAS
# ============================================

class JustificarFaltasDialog(QDialog):
    """DiÃ¡logo para justificar faltas de alunos"""

    def __init__(self, parent=None, rows_selecionadas=None):
        super().__init__(parent)
        self.rows_selecionadas = rows_selecionadas or set()

        self.setWindowTitle("Justificar Faltas")
        self.setFixedSize(500, 300)
        self.setStyleSheet(GLOBAL_STYLESHEET)

        self.init_ui()

    def init_ui(self):
        """Inicializa a interface do diÃ¡logo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # TÃ­tulo
        lbl_titulo = QLabel("JUSTIFICAR FALTAS")
        lbl_titulo.setObjectName("title")

        # InformaÃ§Ã£o
        lbl_info = QLabel(f"{len(self.rows_selecionadas)} aluno(s) selecionado(s)")
        lbl_info.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #f39c12;
                font-weight: 600;
                padding: 10px;
                background-color: #fef5e7;
                border-radius: 6px;
                border: 1px solid #f39c12;
            }
        """)

        # Justificativa
        lbl_justificativa = QLabel("Justificativa para a(s) falta(s):")
        lbl_justificativa.setStyleSheet("font-weight: 600; color: #2c3e50;")

        self.txt_justificativa = QTextEdit()
        self.txt_justificativa.setPlaceholderText("Digite a justificativa para a(s) falta(s)...")
        self.txt_justificativa.setMaximumHeight(100)

        # Tipos de justificativa comum
        lbl_tipos = QLabel("Tipos comuns de justificativa:")
        lbl_tipos.setStyleSheet("font-weight: 600; color: #2c3e50;")

        tipos_layout = QHBoxLayout()

        btn_doenca = QPushButton("DoenÃ§a")
        btn_doenca.setObjectName("warning")
        btn_doenca.clicked.connect(lambda: self.adicionar_justificativa("DoenÃ§a"))

        btn_familiar = QPushButton("Problema familiar")
        btn_familiar.setObjectName("warning")
        btn_familiar.clicked.connect(lambda: self.adicionar_justificativa("Problema familiar"))

        btn_consulta = QPushButton("Consulta mÃ©dica")
        btn_consulta.setObjectName("warning")
        btn_consulta.clicked.connect(lambda: self.adicionar_justificativa("Consulta mÃ©dica"))

        btn_outros = QPushButton("Outros")
        btn_outros.setObjectName("warning")
        btn_outros.clicked.connect(lambda: self.adicionar_justificativa(""))

        tipos_layout.addWidget(btn_doenca)
        tipos_layout.addWidget(btn_familiar)
        tipos_layout.addWidget(btn_consulta)
        tipos_layout.addWidget(btn_outros)
        tipos_layout.addStretch()

        # BotÃµes
        botoes_layout = QHBoxLayout()

        btn_aplicar = AnimacaoBotao("APLICAR JUSTIFICATIVA", cor_normal="#27ae60", cor_hover="#219653",
                                    cor_press="#1e874b")
        btn_aplicar.setMinimumHeight(45)
        btn_aplicar.clicked.connect(self.accept)

        btn_cancelar = QPushButton("CANCELAR")
        btn_cancelar.setObjectName("danger")
        btn_cancelar.setMinimumHeight(45)
        btn_cancelar.clicked.connect(self.reject)

        botoes_layout.addWidget(btn_aplicar)
        botoes_layout.addStretch()
        botoes_layout.addWidget(btn_cancelar)

        # Adicionar tudo ao layout
        layout.addWidget(lbl_titulo)
        layout.addWidget(lbl_info)
        layout.addWidget(lbl_justificativa)
        layout.addWidget(self.txt_justificativa)
        layout.addWidget(lbl_tipos)
        layout.addLayout(tipos_layout)
        layout.addStretch()
        layout.addLayout(botoes_layout)

    def adicionar_justificativa(self, texto):
        """Adiciona texto prÃ©-definido Ã  justificativa"""
        if texto:
            self.txt_justificativa.setPlainText(texto)
        else:
            self.txt_justificativa.clear()

    def obter_justificativa(self):
        """Retorna a justificativa digitada"""
        return self.txt_justificativa.toPlainText().strip()

    # ============================================
    # PÃGINA DE RELATÃ“RIOS (COMPLETA)
    # ============================================

    def criar_pagina_relatorios(self):
        """Cria a pÃ¡gina de relatÃ³rios - COMPLETA"""
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # TÃ­tulo
        lbl_titulo = QLabel("RELATÃ“RIOS E ESTATÃSTICAS")
        lbl_titulo.setObjectName("title")

        # Cards de relatÃ³rios
        grid_cards = QGridLayout()
        grid_cards.setSpacing(20)

        # Card: RelatÃ³rio de Alunos
        card_alunos = CardWidget("RELATÃ“RIO DE ALUNOS")
        layout_alunos = QVBoxLayout(card_alunos.conteudo_widget)
        layout_alunos.setSpacing(15)

        lbl_desc_alunos = QLabel("Gere relatÃ³rios detalhados sobre os alunos")
        lbl_desc_alunos.setStyleSheet("color: #7f8c8d; font-size: 13px;")
        lbl_desc_alunos.setWordWrap(True)

        btn_rel_alunos = AnimacaoBotao("Gerar RelatÃ³rio", cor_normal="#3498db", cor_hover="#2980b9",
                                       cor_press="#1c6ea4")
        btn_rel_alunos.clicked.connect(self.gerar_relatorio_alunos_detalhado)

        layout_alunos.addWidget(lbl_desc_alunos)
        layout_alunos.addWidget(btn_rel_alunos)

        # Card: RelatÃ³rio de Notas
        card_notas = CardWidget("RELATÃ“RIO DE NOTAS")
        layout_notas = QVBoxLayout(card_notas.conteudo_widget)

        lbl_desc_notas = QLabel("Analise o desempenho acadÃªmico por turma/disciplina")
        lbl_desc_notas.setStyleSheet("color: #7f8c8d; font-size: 13px;")
        lbl_desc_notas.setWordWrap(True)

        btn_rel_notas = AnimacaoBotao("Gerar RelatÃ³rio", cor_normal="#27ae60", cor_hover="#219653", cor_press="#1e874b")
        btn_rel_notas.clicked.connect(self.gerar_relatorio_notas_detalhado)

        layout_notas.addWidget(lbl_desc_notas)
        layout_notas.addWidget(btn_rel_notas)

        # Card: RelatÃ³rio de FrequÃªncia
        card_frequencia = CardWidget("RELATÃ“RIO DE FREQUÃŠNCIA")
        layout_frequencia = QVBoxLayout(card_frequencia.conteudo_widget)

        lbl_desc_freq = QLabel("Acompanhe a frequÃªncia e faltas dos alunos")
        lbl_desc_freq.setStyleSheet("color: #7f8c8d; font-size: 13px;")
        lbl_desc_freq.setWordWrap(True)

        btn_rel_freq = AnimacaoBotao("Gerar RelatÃ³rio", cor_normal="#f39c12", cor_hover="#d68910", cor_press="#b9770e")
        btn_rel_freq.clicked.connect(self.gerar_relatorio_frequencia_detalhado)

        layout_frequencia.addWidget(lbl_desc_freq)
        layout_frequencia.addWidget(btn_rel_freq)

        # Card: Boletim Individual
        card_boletim = CardWidget("BOLETIM INDIVIDUAL")
        layout_boletim = QVBoxLayout(card_boletim.conteudo_widget)

        lbl_desc_boletim = QLabel("Gere boletins individuais dos alunos")
        lbl_desc_boletim.setStyleSheet("color: #7f8c8d; font-size: 13px;")
        lbl_desc_boletim.setWordWrap(True)

        btn_boletim = AnimacaoBotao("Gerar Boletim", cor_normal="#9b59b6", cor_hover="#8e44ad", cor_press="#7d3c98")
        btn_boletim.clicked.connect(self.gerar_boletim_individual)

        layout_boletim.addWidget(lbl_desc_boletim)
        layout_boletim.addWidget(btn_boletim)

        # Card: EstatÃ­sticas Gerais
        card_stats = CardWidget("ESTATÃSTICAS GERAIS")
        layout_stats = QVBoxLayout(card_stats.conteudo_widget)

        lbl_desc_stats = QLabel("Visualize estatÃ­sticas e indicadores do sistema")
        lbl_desc_stats.setStyleSheet("color: #7f8c8d; font-size: 13px;")
        lbl_desc_stats.setWordWrap(True)

        btn_stats = AnimacaoBotao("Ver EstatÃ­sticas", cor_normal="#e74c3c", cor_hover="#c0392b", cor_press="#a93226")
        btn_stats.clicked.connect(self.ver_estatisticas_gerais)

        layout_stats.addWidget(lbl_desc_stats)
        layout_stats.addWidget(btn_stats)

        # Card: RelatÃ³rio Personalizado
        card_personalizado = CardWidget("RELATÃ“RIO PERSONALIZADO")
        layout_personalizado = QVBoxLayout(card_personalizado.conteudo_widget)

        lbl_desc_personal = QLabel("Crie relatÃ³rios personalizados com filtros avanÃ§ados")
        lbl_desc_personal.setStyleSheet("color: #7f8c8d; font-size: 13px;")
        lbl_desc_personal.setWordWrap(True)

        btn_personal = AnimacaoBotao("Criar RelatÃ³rio", cor_normal="#34495e", cor_hover="#2c3e50", cor_press="#1a252f")
        btn_personal.clicked.connect(self.relatorio_personalizado_detalhado)

        layout_personalizado.addWidget(lbl_desc_personal)
        layout_personalizado.addWidget(btn_personal)

        # Adicionar cards ao grid
        grid_cards.addWidget(card_alunos, 0, 0)
        grid_cards.addWidget(card_notas, 0, 1)
        grid_cards.addWidget(card_frequencia, 0, 2)
        grid_cards.addWidget(card_boletim, 1, 0)
        grid_cards.addWidget(card_stats, 1, 1)
        grid_cards.addWidget(card_personalizado, 1, 2)

        # SeÃ§Ã£o de exportaÃ§Ã£o
        group_exportacao = QGroupBox("EXPORTAÃ‡ÃƒO DE DADOS")
        group_exportacao.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: 700;
                color: #2c3e50;
                border: 2px solid #dce1e6;
                border-radius: 8px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 15px;
                padding: 0 10px;
                background-color: #f5f7fa;
            }
        """)

        layout_exportacao = QHBoxLayout()
        layout_exportacao.setSpacing(15)

        btn_export_excel = AnimacaoBotao("Exportar para Excel", cor_normal="#27ae60", cor_hover="#219653",
                                         cor_press="#1e874b")
        btn_export_excel.setIcon(self.style().standardIcon(QStyle.SP_DriveHDIcon))
        btn_export_excel.clicked.connect(self.exportar_para_excel)

        btn_export_pdf = AnimacaoBotao("Exportar para PDF", cor_normal="#e74c3c", cor_hover="#c0392b",
                                       cor_press="#a93226")
        btn_export_pdf.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
        btn_export_pdf.clicked.connect(self.exportar_para_pdf)

        btn_export_csv = AnimacaoBotao("Exportar para CSV", cor_normal="#3498db", cor_hover="#2980b9",
                                       cor_press="#1c6ea4")
        btn_export_csv.setIcon(self.style().standardIcon(QStyle.SP_FileDialogListView))
        btn_export_csv.clicked.connect(self.exportar_para_csv)

        layout_exportacao.addWidget(btn_export_excel)
        layout_exportacao.addWidget(btn_export_pdf)
        layout_exportacao.addWidget(btn_export_csv)
        layout_exportacao.addStretch()

        group_exportacao.setLayout(layout_exportacao)

        # Adicionar tudo ao layout
        layout.addWidget(lbl_titulo)
        layout.addLayout(grid_cards)
        layout.addWidget(group_exportacao)
        layout.addStretch()

        self.paginas['relatorios'] = pagina
        self.central_widget.addWidget(pagina)

    def gerar_relatorio_alunos_detalhado(self):
        """Abre diÃ¡logo para gerar relatÃ³rio detalhado de alunos"""
        dialog = RelatorioAlunosDialog(self)
        dialog.exec_()

    def gerar_relatorio_notas_detalhado(self):
        """Abre diÃ¡logo para gerar relatÃ³rio detalhado de notas"""
        dialog = RelatorioNotasDialog(self)
        dialog.exec_()

    def gerar_relatorio_frequencia_detalhado(self):
        """Abre diÃ¡logo para gerar relatÃ³rio detalhado de frequÃªncia"""
        dialog = RelatorioFrequenciaDialog(self)
        dialog.exec_()

    def gerar_boletim_individual(self):
        """Abre diÃ¡logo para gerar boletim individual"""
        dialog = BoletimIndividualDialog(self)
        dialog.exec_()

    def ver_estatisticas_gerais(self):
        """Mostra estatÃ­sticas gerais do sistema"""
        dialog = EstatisticasGeraisDialog(self)
        dialog.exec_()

    def relatorio_personalizado_detalhado(self):
        """Abre diÃ¡logo para criar relatÃ³rio personalizado"""
        dialog = RelatorioPersonalizadoDialog(self)
        dialog.exec_()

    def exportar_para_excel(self):
        """Exporta dados para Excel"""
        dialog = ExportarDadosDialog(self, "excel")
        dialog.exec_()

    def exportar_para_pdf(self):
        """Exporta dados para PDF"""
        dialog = ExportarDadosDialog(self, "pdf")
        dialog.exec_()

    def exportar_para_csv(self):
        """Exporta dados para CSV"""
        dialog = ExportarDadosDialog(self, "csv")
        dialog.exec_()


# ============================================
# DIÃLOGO DE RELATÃ“RIO DE ALUNOS
# ============================================

class RelatorioAlunosDialog(QDialog):
    """DiÃ¡logo para gerar relatÃ³rio de alunos"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()

        self.setWindowTitle("RelatÃ³rio de Alunos")
        self.setFixedSize(600, 500)
        self.setStyleSheet(GLOBAL_STYLESHEET)

        self.init_ui()

    def init_ui(self):
        """Inicializa a interface do diÃ¡logo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # TÃ­tulo
        lbl_titulo = QLabel("RELATÃ“RIO DE ALUNOS")
        lbl_titulo.setObjectName("title")

        # Filtros
        group_filtros = QGroupBox("FILTROS DO RELATÃ“RIO")
        group_filtros.setStyleSheet("""
            QGroupBox {
                font-weight: 600;
                border: 2px solid #dce1e6;
                border-radius: 8px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 15px;
                padding: 0 10px;
                background-color: #f5f7fa;
            }
        """)

        layout_filtros = QFormLayout(group_filtros)
        layout_filtros.setSpacing(15)

        # Filtro por status
        self.combo_status_rel = QComboBox()
        self.combo_status_rel.addItems(["Todos", "Ativos", "Inativos", "Transferidos", "Evadidos"])

        # Filtro por turma
        self.combo_turma_rel = QComboBox()
        self.combo_turma_rel.addItem("Todas as turmas")
        self.carregar_turmas_relatorio()

        # Filtro por sÃ©rie
        self.combo_serie_rel = QComboBox()
        self.combo_serie_rel.addItem("Todas as sÃ©ries")
        self.carregar_series_relatorio()

        # Filtro por data de matrÃ­cula
        lbl_periodo = QLabel("PerÃ­odo de matrÃ­cula:")

        periodo_layout = QHBoxLayout()
        self.date_inicio_rel = QDateEdit()
        self.date_inicio_rel.setCalendarPopup(True)
        self.date_inicio_rel.setDate(QDate.currentDate().addYears(-1))
        self.date_inicio_rel.setDisplayFormat("dd/MM/yyyy")

        self.date_fim_rel = QDateEdit()
        self.date_fim_rel.setCalendarPopup(True)
        self.date_fim_rel.setDate(QDate.currentDate())
        self.date_fim_rel.setDisplayFormat("dd/MM/yyyy")

        periodo_layout.addWidget(self.date_inicio_rel)
        periodo_layout.addWidget(QLabel("atÃ©"))
        periodo_layout.addWidget(self.date_fim_rel)

        layout_filtros.addRow("Status:", self.combo_status_rel)
        layout_filtros.addRow("Turma:", self.combo_turma_rel)
        layout_filtros.addRow("SÃ©rie:", self.combo_serie_rel)
        layout_filtros.addRow(lbl_periodo, periodo_layout)

        # OpÃ§Ãµes de exibiÃ§Ã£o
        group_opcoes = QGroupBox("OPÃ‡Ã•ES DE EXIBIÃ‡ÃƒO")
        group_opcoes.setStyleSheet(group_filtros.styleSheet())

        layout_opcoes = QVBoxLayout(group_opcoes)

        self.check_endereco = QCheckBox("Incluir endereÃ§o completo")
        self.check_contato = QCheckBox("Incluir informaÃ§Ãµes de contato")
        self.check_responsavel = QCheckBox("Incluir dados do responsÃ¡vel")
        self.check_observacoes = QCheckBox("Incluir observaÃ§Ãµes")

        layout_opcoes.addWidget(self.check_endereco)
        layout_opcoes.addWidget(self.check_contato)
        layout_opcoes.addWidget(self.check_responsavel)
        layout_opcoes.addWidget(self.check_observacoes)

        # BotÃµes
        botoes_layout = QHBoxLayout()

        btn_gerar = AnimacaoBotao("GERAR RELATÃ“RIO", cor_normal="#27ae60", cor_hover="#219653", cor_press="#1e874b")
        btn_gerar.setMinimumHeight(45)
        btn_gerar.clicked.connect(self.gerar_relatorio)

        btn_visualizar = AnimacaoBotao("VISUALIZAR", cor_normal="#3498db", cor_hover="#2980b9", cor_press="#1c6ea4")
        btn_visualizar.setMinimumHeight(45)
        btn_visualizar.clicked.connect(self.visualizar_relatorio)

        btn_exportar = AnimacaoBotao("EXPORTAR", cor_normal="#f39c12", cor_hover="#d68910", cor_press="#b9770e")
        btn_exportar.setMinimumHeight(45)
        btn_exportar.clicked.connect(self.exportar_relatorio)

        btn_fechar = QPushButton("FECHAR")
        btn_fechar.setObjectName("danger")
        btn_fechar.setMinimumHeight(45)
        btn_fechar.clicked.connect(self.close)

        botoes_layout.addWidget(btn_gerar)
        botoes_layout.addWidget(btn_visualizar)
        botoes_layout.addWidget(btn_exportar)
        botoes_layout.addStretch()
        botoes_layout.addWidget(btn_fechar)

        # Adicionar tudo ao layout
        layout.addWidget(lbl_titulo)
        layout.addWidget(group_filtros)
        layout.addWidget(group_opcoes)
        layout.addStretch()
        layout.addLayout(botoes_layout)

    def carregar_turmas_relatorio(self):
        """Carrega turmas para o relatÃ³rio"""
        try:
            turmas = self.db.execute_query('''
                SELECT DISTINCT turma 
                FROM alunos 
                WHERE turma IS NOT NULL AND turma != ''
                ORDER BY turma
            ''', fetch=True)

            for turma in turmas:
                if turma[0]:
                    self.combo_turma_rel.addItem(turma[0])

        except Exception as e:
            print(f"Erro ao carregar turmas: {e}")

    def carregar_series_relatorio(self):
        """Carrega sÃ©ries para o relatÃ³rio"""
        try:
            series = self.db.execute_query('''
                SELECT DISTINCT serie 
                FROM alunos 
                WHERE serie IS NOT NULL AND serie != ''
                ORDER BY serie
            ''', fetch=True)

            for serie in series:
                if serie[0]:
                    self.combo_serie_rel.addItem(serie[0])

        except Exception as e:
            print(f"Erro ao carregar sÃ©ries: {e}")

    def gerar_relatorio(self):
        """Gera o relatÃ³rio com base nos filtros"""
        # Obter parÃ¢metros dos filtros
        status_filtro = self.combo_status_rel.currentText()
        turma_filtro = self.combo_turma_rel.currentText()
        serie_filtro = self.combo_serie_rel.currentText()
        data_inicio = self.date_inicio_rel.date().toString("yyyy-MM-dd")
        data_fim = self.date_fim_rel.date().toString("yyyy-MM-dd")

        # Construir query
        query = "SELECT COUNT(*) FROM alunos WHERE 1=1"
        params = []

        if status_filtro != "Todos":
            query += " AND status = ?"
            params.append(status_filtro)

        if turma_filtro != "Todas as turmas":
            query += " AND turma = ?"
            params.append(turma_filtro)

        if serie_filtro != "Todas as sÃ©ries":
            query += " AND serie = ?"
            params.append(serie_filtro)

        query += " AND data_matricula BETWEEN ? AND ?"
        params.extend([data_inicio, data_fim])

        try:
            resultado = self.db.execute_query(query, tuple(params), fetch=True)

            if resultado:
                total_alunos = resultado[0][0]

                # Obter dados detalhados
                query_detalhes = query.replace("COUNT(*)", "*")
                alunos = self.db.execute_query(query_detalhes, tuple(params), fetch=True)

                # Criar relatÃ³rio
                relatorio = f"""
                RELATÃ“RIO DE ALUNOS
                ====================
                Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
                Status: {status_filtro}
                Turma: {turma_filtro}
                SÃ©rie: {serie_filtro}
                PerÃ­odo: {self.date_inicio_rel.date().toString('dd/MM/yyyy')} a {self.date_fim_rel.date().toString('dd/MM/yyyy')}
                Total de alunos: {total_alunos}
                ====================

                DETALHES DOS ALUNOS:
                """

                for aluno in alunos:
                    relatorio += f"\nâ€¢ {aluno[1]}"
                    if aluno[17]:  # status
                        relatorio += f" ({aluno[17]})"
                    if aluno[13]:  # sÃ©rie
                        relatorio += f" - {aluno[13]}"
                    if aluno[14]:  # turma
                        relatorio += f" - {aluno[14]}"

                QMessageBox.information(self, "RelatÃ³rio Gerado",
                                        f"RelatÃ³rio gerado com sucesso!\n\n"
                                        f"Total de alunos encontrados: {total_alunos}\n\n"
                                        "Para visualizaÃ§Ã£o completa, use a opÃ§Ã£o VISUALIZAR.")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao gerar relatÃ³rio:\n{str(e)}")

    def visualizar_relatorio(self):
        """Visualiza o relatÃ³rio gerado"""
        QMessageBox.information(self, "Funcionalidade em desenvolvimento",
                                "A visualizaÃ§Ã£o completa do relatÃ³rio serÃ¡ implementada na prÃ³xima versÃ£o.")

    def exportar_relatorio(self):
        """Exporta o relatÃ³rio gerado"""
        QMessageBox.information(self, "Funcionalidade em desenvolvimento",
                                "A exportaÃ§Ã£o do relatÃ³rio serÃ¡ implementada na prÃ³xima versÃ£o.")


"""
PROJETO ESCOLA - SISTEMA DE GESTÃƒO ESCOLAR
Parte 7/10 - ContinuaÃ§Ã£o: RelatÃ³rios, ConfiguraÃ§Ãµes e Sistema
"""


# ============================================
# DIÃLOGO DE RELATÃ“RIO DE NOTAS
# ============================================

class RelatorioNotasDialog(QDialog):
    """DiÃ¡logo para gerar relatÃ³rio de notas"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()

        self.setWindowTitle("RelatÃ³rio de Notas")
        self.setFixedSize(600, 500)
        self.setStyleSheet(GLOBAL_STYLESHEET)

        self.init_ui()
        self.carregar_turmas()
        self.carregar_disciplinas()

    def init_ui(self):
        """Inicializa a interface do diÃ¡logo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # TÃ­tulo
        lbl_titulo = QLabel("RELATÃ“RIO DE NOTAS")
        lbl_titulo.setObjectName("title")

        # Filtros
        group_filtros = QGroupBox("FILTROS DO RELATÃ“RIO")
        group_filtros.setStyleSheet("""
            QGroupBox {
                font-weight: 600;
                border: 2px solid #dce1e6;
                border-radius: 8px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 15px;
                padding: 0 10px;
                background-color: #f5f7fa;
            }
        """)

        layout_filtros = QFormLayout(group_filtros)
        layout_filtros.setSpacing(15)

        # Filtro por turma
        self.combo_turma_notas_rel = QComboBox()
        self.combo_turma_notas_rel.addItem("Todas as turmas")

        # Filtro por disciplina
        self.combo_disciplina_notas_rel = QComboBox()
        self.combo_disciplina_notas_rel.addItem("Todas as disciplinas")

        # Filtro por bimestre
        self.combo_bimestre_notas_rel = QComboBox()
        self.combo_bimestre_notas_rel.addItems(
            ["Todos os bimestres", "1Âº Bimestre", "2Âº Bimestre", "3Âº Bimestre", "4Âº Bimestre"])

        # Filtro por situaÃ§Ã£o
        self.combo_situacao_notas_rel = QComboBox()
        self.combo_situacao_notas_rel.addItems(["Todas as situaÃ§Ãµes", "Aprovado", "RecuperaÃ§Ã£o", "Reprovado"])

        layout_filtros.addRow("Turma:", self.combo_turma_notas_rel)
        layout_filtros.addRow("Disciplina:", self.combo_disciplina_notas_rel)
        layout_filtros.addRow("Bimestre:", self.combo_bimestre_notas_rel)
        layout_filtros.addRow("SituaÃ§Ã£o:", self.combo_situacao_notas_rel)

        # OpÃ§Ãµes de exibiÃ§Ã£o
        group_opcoes = QGroupBox("OPÃ‡Ã•ES DE EXIBIÃ‡ÃƒO")
        group_opcoes.setStyleSheet(group_filtros.styleSheet())

        layout_opcoes = QVBoxLayout(group_opcoes)

        self.check_medias = QCheckBox("Incluir mÃ©dias individuais")
        self.check_medias.setChecked(True)

        self.check_notas_detalhadas = QCheckBox("Incluir notas por bimestre")

        self.check_estatisticas = QCheckBox("Incluir estatÃ­sticas (mÃ©dia geral, desvio padrÃ£o)")
        self.check_estatisticas.setChecked(True)

        self.check_ranking = QCheckBox("Incluir ranking por mÃ©dia")

        layout_opcoes.addWidget(self.check_medias)
        layout_opcoes.addWidget(self.check_notas_detalhadas)
        layout_opcoes.addWidget(self.check_estatisticas)
        layout_opcoes.addWidget(self.check_ranking)

        # BotÃµes
        botoes_layout = QHBoxLayout()

        btn_gerar = AnimacaoBotao("GERAR RELATÃ“RIO", cor_normal="#27ae60", cor_hover="#219653", cor_press="#1e874b")
        btn_gerar.setMinimumHeight(45)
        btn_gerar.clicked.connect(self.gerar_relatorio)

        btn_visualizar = AnimacaoBotao("VISUALIZAR", cor_normal="#3498db", cor_hover="#2980b9", cor_press="#1c6ea4")
        btn_visualizar.setMinimumHeight(45)
        btn_visualizar.clicked.connect(self.visualizar_relatorio)

        btn_fechar = QPushButton("FECHAR")
        btn_fechar.setObjectName("danger")
        btn_fechar.setMinimumHeight(45)
        btn_fechar.clicked.connect(self.close)

        botoes_layout.addWidget(btn_gerar)
        botoes_layout.addWidget(btn_visualizar)
        botoes_layout.addStretch()
        botoes_layout.addWidget(btn_fechar)

        # Adicionar tudo ao layout
        layout.addWidget(lbl_titulo)
        layout.addWidget(group_filtros)
        layout.addWidget(group_opcoes)
        layout.addStretch()
        layout.addLayout(botoes_layout)

    def carregar_turmas(self):
        """Carrega turmas para o relatÃ³rio"""
        try:
            turmas = self.db.execute_query('''
                SELECT DISTINCT nome, serie 
                FROM turmas 
                WHERE ativa = 1
                ORDER BY serie, nome
            ''', fetch=True)

            for nome, serie in turmas:
                texto = f"{nome} - {serie}" if serie else nome
                self.combo_turma_notas_rel.addItem(texto, nome)

        except Exception as e:
            print(f"Erro ao carregar turmas: {e}")

    def carregar_disciplinas(self):
        """Carrega disciplinas para o relatÃ³rio"""
        try:
            disciplinas = self.db.execute_query('''
                SELECT DISTINCT nome, serie 
                FROM disciplinas 
                WHERE ativa = 1
                ORDER BY nome
            ''', fetch=True)

            for nome, serie in disciplinas:
                texto = f"{nome} ({serie})" if serie else nome
                self.combo_disciplina_notas_rel.addItem(texto, nome)

        except Exception as e:
            print(f"Erro ao carregar disciplinas: {e}")

    def gerar_relatorio(self):
        """Gera o relatÃ³rio de notas"""
        # Obter parÃ¢metros dos filtros
        turma_filtro = self.combo_turma_notas_rel.currentText()
        disciplina_filtro = self.combo_disciplina_notas_rel.currentText()
        bimestre_filtro = self.combo_bimestre_notas_rel.currentText()
        situacao_filtro = self.combo_situacao_notas_rel.currentText()

        # Construir query bÃ¡sica
        query = """
            SELECT a.nome as aluno, a.turma, d.nome as disciplina, 
                   n.bimestre, n.nota1, n.nota2, n.nota3, n.nota4,
                   n.media, n.situacao
            FROM notas n
            JOIN alunos a ON n.aluno_id = a.id
            JOIN disciplinas d ON n.disciplina_id = d.id
            WHERE 1=1
        """

        params = []

        if turma_filtro != "Todas as turmas":
            query += " AND a.turma = ?"
            params.append(turma_filtro.split(" - ")[0])  # Extrair apenas o nome da turma

        if disciplina_filtro != "Todas as disciplinas":
            query += " AND d.nome = ?"
            params.append(disciplina_filtro.split(" (")[0])  # Extrair apenas o nome da disciplina

        if bimestre_filtro != "Todos os bimestres":
            bimestre_num = int(bimestre_filtro[0])  # Extrair nÃºmero do bimestre
            query += " AND n.bimestre = ?"
            params.append(bimestre_num)

        if situacao_filtro != "Todas as situaÃ§Ãµes":
            query += " AND n.situacao = ?"
            params.append(situacao_filtro)

        query += " ORDER BY a.turma, a.nome, d.nome, n.bimestre"

        try:
            notas = self.db.execute_query(query, tuple(params), fetch=True)

            if not notas:
                QMessageBox.information(self, "Sem dados",
                                        "Nenhum registro encontrado com os filtros selecionados.")
                return

            # Criar relatÃ³rio
            relatorio = f"""
            RELATÃ“RIO DE NOTAS
            ====================
            Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
            Turma: {turma_filtro}
            Disciplina: {disciplina_filtro}
            Bimestre: {bimestre_filtro}
            SituaÃ§Ã£o: {situacao_filtro}
            Total de registros: {len(notas)}
            ====================

            DETALHES DAS NOTAS:
            """

            turma_atual = None
            aluno_atual = None
            disciplina_atual = None

            for nota in notas:
                aluno, turma, disciplina, bimestre, n1, n2, n3, n4, media, situacao = nota

                # Agrupar por turma
                if turma != turma_atual:
                    turma_atual = turma
                    relatorio += f"\n\nTURMA: {turma_atual}"
                    relatorio += "\n" + "-" * 40

                # Agrupar por aluno
                if aluno != aluno_atual:
                    aluno_atual = aluno
                    relatorio += f"\n\nAluno: {aluno_atual}"

                # Adicionar detalhes da disciplina
                relatorio += f"\n  Disciplina: {disciplina} | Bimestre: {bimestre}"

                if self.check_notas_detalhadas.isChecked():
                    notas_str = []
                    if n1 is not None:
                        notas_str.append(f"N1: {n1:.1f}")
                    if n2 is not None:
                        notas_str.append(f"N2: {n2:.1f}")
                    if n3 is not None:
                        notas_str.append(f"N3: {n3:.1f}")
                    if n4 is not None:
                        notas_str.append(f"N4: {n4:.1f}")

                    if notas_str:
                        relatorio += f" | Notas: {', '.join(notas_str)}"

                if self.check_medias.isChecked() and media is not None:
                    relatorio += f" | MÃ©dia: {media:.1f}"

                if situacao:
                    relatorio += f" | SituaÃ§Ã£o: {situacao}"

            # Adicionar estatÃ­sticas se solicitado
            if self.check_estatisticas.isChecked() and notas:
                medias = [n[8] for n in notas if n[8] is not None]

                if medias:
                    media_geral = sum(medias) / len(medias)
                    relatorio += f"\n\n{'=' * 40}"
                    relatorio += f"\nESTATÃSTICAS:"
                    relatorio += f"\nMÃ©dia geral: {media_geral:.2f}"
                    relatorio += f"\nMaior mÃ©dia: {max(medias):.2f}"
                    relatorio += f"\nMenor mÃ©dia: {min(medias):.2f}"
                    relatorio += f"\nTotal de alunos com mÃ©dia: {len(medias)}"

            # Adicionar ranking se solicitado
            if self.check_ranking.isChecked() and notas:
                # Agrupar mÃ©dias por aluno
                medias_alunos = {}
                for nota in notas:
                    aluno, _, _, _, _, _, _, _, media, _ = nota
                    if media is not None:
                        if aluno not in medias_alunos:
                            medias_alunos[aluno] = []
                        medias_alunos[aluno].append(media)

                # Calcular mÃ©dia por aluno
                medias_finais = {}
                for aluno, notas_aluno in medias_alunos.items():
                    medias_finais[aluno] = sum(notas_aluno) / len(notas_aluno)

                # Ordenar por mÃ©dia
                ranking = sorted(medias_finais.items(), key=lambda x: x[1], reverse=True)

                relatorio += f"\n\n{'=' * 40}"
                relatorio += f"\nRANKING POR MÃ‰DIA:"

                for pos, (aluno, media) in enumerate(ranking[:10], 1):  # Top 10
                    relatorio += f"\n{pos}Âº. {aluno}: {media:.2f}"

            QMessageBox.information(self, "RelatÃ³rio Gerado",
                                    f"RelatÃ³rio gerado com sucesso!\n\n"
                                    f"Total de registros: {len(notas)}\n\n"
                                    "Para visualizaÃ§Ã£o completa, use a opÃ§Ã£o VISUALIZAR.")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao gerar relatÃ³rio:\n{str(e)}")

    def visualizar_relatorio(self):
        """Visualiza o relatÃ³rio gerado"""
        QMessageBox.information(self, "Funcionalidade em desenvolvimento",
                                "A visualizaÃ§Ã£o completa do relatÃ³rio serÃ¡ implementada na prÃ³xima versÃ£o.")


# ============================================
# DIÃLOGO DE RELATÃ“RIO DE FREQUÃŠNCIA
# ============================================

class RelatorioFrequenciaDialog(QDialog):
    """DiÃ¡logo para gerar relatÃ³rio de frequÃªncia"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()

        self.setWindowTitle("RelatÃ³rio de FrequÃªncia")
        self.setFixedSize(600, 500)
        self.setStyleSheet(GLOBAL_STYLESHEET)

        self.init_ui()
        self.carregar_turmas_freq()

    def init_ui(self):
        """Inicializa a interface do diÃ¡logo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # TÃ­tulo
        lbl_titulo = QLabel("RELATÃ“RIO DE FREQUÃŠNCIA")
        lbl_titulo.setObjectName("title")

        # Filtros
        group_filtros = QGroupBox("FILTROS DO RELATÃ“RIO")
        group_filtros.setStyleSheet("""
            QGroupBox {
                font-weight: 600;
                border: 2px solid #dce1e6;
                border-radius: 8px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 15px;
                padding: 0 10px;
                background-color: #f5f7fa;
            }
        """)

        layout_filtros = QFormLayout(group_filtros)
        layout_filtros.setSpacing(15)

        # Filtro por turma
        self.combo_turma_freq_rel = QComboBox()
        self.combo_turma_freq_rel.addItem("Todas as turmas")

        # Filtro por perÃ­odo
        lbl_periodo = QLabel("PerÃ­odo:")

        periodo_layout = QHBoxLayout()
        self.date_inicio_freq = QDateEdit()
        self.date_inicio_freq.setCalendarPopup(True)
        self.date_inicio_freq.setDate(QDate.currentDate().addMonths(-1))
        self.date_inicio_freq.setDisplayFormat("dd/MM/yyyy")

        self.date_fim_freq = QDateEdit()
        self.date_fim_freq.setCalendarPopup(True)
        self.date_fim_freq.setDate(QDate.currentDate())
        self.date_fim_freq.setDisplayFormat("dd/MM/yyyy")

        periodo_layout.addWidget(self.date_inicio_freq)
        periodo_layout.addWidget(QLabel("atÃ©"))
        periodo_layout.addWidget(self.date_fim_freq)

        # Filtro por disciplina
        self.combo_disciplina_freq_rel = QComboBox()
        self.combo_disciplina_freq_rel.addItem("Todas as disciplinas")

        # Filtro por presenÃ§a
        self.combo_presenca_freq_rel = QComboBox()
        self.combo_presenca_freq_rel.addItems(
            ["Todas", "Apenas presentes", "Apenas faltas", "Apenas faltas justificadas"])

        layout_filtros.addRow("Turma:", self.combo_turma_freq_rel)
        layout_filtros.addRow(lbl_periodo, periodo_layout)
        layout_filtros.addRow("Disciplina:", self.combo_disciplina_freq_rel)
        layout_filtros.addRow("PresenÃ§a:", self.combo_presenca_freq_rel)

        # OpÃ§Ãµes de exibiÃ§Ã£o
        group_opcoes = QGroupBox("OPÃ‡Ã•ES DE EXIBIÃ‡ÃƒO")
        group_opcoes.setStyleSheet(group_filtros.styleSheet())

        layout_opcoes = QVBoxLayout(group_opcoes)

        self.check_detalhado = QCheckBox("RelatÃ³rio detalhado (por dia)")
        self.check_detalhado.setChecked(True)

        self.check_resumido = QCheckBox("RelatÃ³rio resumido (totais)")

        self.check_porcentagens = QCheckBox("Incluir porcentagens")
        self.check_porcentagens.setChecked(True)

        self.check_justificativas = QCheckBox("Incluir justificativas de faltas")

        layout_opcoes.addWidget(self.check_detalhado)
        layout_opcoes.addWidget(self.check_resumido)
        layout_opcoes.addWidget(self.check_porcentagens)
        layout_opcoes.addWidget(self.check_justificativas)

        # BotÃµes
        botoes_layout = QHBoxLayout()

        btn_gerar = AnimacaoBotao("GERAR RELATÃ“RIO", cor_normal="#27ae60", cor_hover="#219653", cor_press="#1e874b")
        btn_gerar.setMinimumHeight(45)
        btn_gerar.clicked.connect(self.gerar_relatorio)

        btn_visualizar = AnimacaoBotao("VISUALIZAR", cor_normal="#3498db", cor_hover="#2980b9", cor_press="#1c6ea4")
        btn_visualizar.setMinimumHeight(45)
        btn_visualizar.clicked.connect(self.visualizar_relatorio)

        btn_fechar = QPushButton("FECHAR")
        btn_fechar.setObjectName("danger")
        btn_fechar.setMinimumHeight(45)
        btn_fechar.clicked.connect(self.close)

        botoes_layout.addWidget(btn_gerar)
        botoes_layout.addWidget(btn_visualizar)
        botoes_layout.addStretch()
        botoes_layout.addWidget(btn_fechar)

        # Adicionar tudo ao layout
        layout.addWidget(lbl_titulo)
        layout.addWidget(group_filtros)
        layout.addWidget(group_opcoes)
        layout.addStretch()
        layout.addLayout(botoes_layout)

    def carregar_turmas_freq(self):
        """Carrega turmas para o relatÃ³rio de frequÃªncia"""
        try:
            turmas = self.db.execute_query('''
                SELECT DISTINCT nome, serie 
                FROM turmas 
                WHERE ativa = 1
                ORDER BY serie, nome
            ''', fetch=True)

            for nome, serie in turmas:
                texto = f"{nome} - {serie}" if serie else nome
                self.combo_turma_freq_rel.addItem(texto, nome)

        except Exception as e:
            print(f"Erro ao carregar turmas: {e}")

    def gerar_relatorio(self):
        """Gera o relatÃ³rio de frequÃªncia"""
        # Obter parÃ¢metros dos filtros
        turma_filtro = self.combo_turma_freq_rel.currentText()
        data_inicio = self.date_inicio_freq.date().toString("yyyy-MM-dd")
        data_fim = self.date_fim_freq.date().toString("yyyy-MM-dd")
        disciplina_filtro = self.combo_disciplina_freq_rel.currentText()
        presenca_filtro = self.combo_presenca_freq_rel.currentText()

        # Construir query
        query = """
            SELECT a.nome as aluno, a.turma, f.data, 
                   d.nome as disciplina, f.presente, f.justificativa
            FROM frequencia f
            JOIN alunos a ON f.aluno_id = a.id
            LEFT JOIN disciplinas d ON f.disciplina_id = d.id
            WHERE f.data BETWEEN ? AND ?
        """

        params = [data_inicio, data_fim]

        if turma_filtro != "Todas as turmas":
            query += " AND a.turma = ?"
            params.append(turma_filtro.split(" - ")[0])

        if disciplina_filtro != "Todas as disciplinas":
            query += " AND d.nome = ?"
            params.append(disciplina_filtro.split(" (")[0])

        if presenca_filtro == "Apenas presentes":
            query += " AND f.presente = 1"
        elif presenca_filtro == "Apenas faltas":
            query += " AND f.presente = 0"
        elif presenca_filtro == "Apenas faltas justificadas":
            query += " AND f.presente = 0 AND f.justificativa IS NOT NULL"

        query += " ORDER BY a.turma, a.nome, f.data"

        try:
            frequencias = self.db.execute_query(query, tuple(params), fetch=True)

            if not frequencias:
                QMessageBox.information(self, "Sem dados",
                                        "Nenhum registro encontrado com os filtros selecionados.")
                return

            # Criar relatÃ³rio
            relatorio = f"""
            RELATÃ“RIO DE FREQUÃŠNCIA
            ========================
            Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
            PerÃ­odo: {self.date_inicio_freq.date().toString('dd/MM/yyyy')} a {self.date_fim_freq.date().toString('dd/MM/yyyy')}
            Turma: {turma_filtro}
            Disciplina: {disciplina_filtro}
            Tipo: {presenca_filtro}
            Total de registros: {len(frequencias)}
            ========================
            """

            # RelatÃ³rio detalhado
            if self.check_detalhado.isChecked():
                turma_atual = None
                aluno_atual = None

                for freq in frequencias:
                    aluno, turma, data, disciplina, presente, justificativa = freq

                    # Formatar data
                    try:
                        data_obj = datetime.strptime(data, '%Y-%m-%d')
                        data_formatada = data_obj.strftime('%d/%m/%Y')
                    except:
                        data_formatada = data

                    # Agrupar por turma
                    if turma != turma_atual:
                        turma_atual = turma
                        relatorio += f"\n\nTURMA: {turma_atual}"
                        relatorio += "\n" + "-" * 50

                    # Agrupar por aluno
                    if aluno != aluno_atual:
                        aluno_atual = aluno
                        relatorio += f"\n\nAluno: {aluno_atual}"

                    # Adicionar registro
                    status = "PRESENTE" if presente == 1 else "FALTA"
                    status_cor = "âœ“" if presente == 1 else "âœ—"

                    linha = f"\n  {data_formatada} | {disciplina or 'Geral'} | {status_cor} {status}"

                    if not presente and justificativa and self.check_justificativas.isChecked():
                        linha += f" | Justificativa: {justificativa}"

                    relatorio += linha

            # RelatÃ³rio resumido
            if self.check_resumido.isChecked():
                # Calcular totais
                total_registros = len(frequencias)
                presentes = sum(1 for f in frequencias if f[4] == 1)
                faltas = total_registros - presentes
                faltas_justificadas = sum(1 for f in frequencias if f[4] == 0 and f[5])

                relatorio += f"\n\n{'=' * 50}"
                relatorio += f"\nRESUMO ESTATÃSTICO:"
                relatorio += f"\nTotal de registros: {total_registros}"
                relatorio += f"\nPresenÃ§as: {presentes}"
                relatorio += f"\nFaltas: {faltas}"
                relatorio += f"\nFaltas justificadas: {faltas_justificadas}"

                if self.check_porcentagens.isChecked() and total_registros > 0:
                    percent_presentes = (presentes / total_registros) * 100
                    percent_faltas = (faltas / total_registros) * 100

                    relatorio += f"\n\nPorcentagens:"
                    relatorio += f"\nPresenÃ§as: {percent_presentes:.1f}%"
                    relatorio += f"\nFaltas: {percent_faltas:.1f}%"

                    if faltas > 0:
                        percent_justificadas = (faltas_justificadas / faltas) * 100
                        relatorio += f"\nFaltas justificadas: {percent_justificadas:.1f}% do total de faltas"

            QMessageBox.information(self, "RelatÃ³rio Gerado",
                                    f"RelatÃ³rio gerado com sucesso!\n\n"
                                    f"Total de registros: {len(frequencias)}\n\n"
                                    "Para visualizaÃ§Ã£o completa, use a opÃ§Ã£o VISUALIZAR.")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao gerar relatÃ³rio:\n{str(e)}")

    def visualizar_relatorio(self):
        """Visualiza o relatÃ³rio gerado"""
        QMessageBox.information(self, "Funcionalidade em desenvolvimento",
                                "A visualizaÃ§Ã£o completa do relatÃ³rio serÃ¡ implementada na prÃ³xima versÃ£o.")


# ============================================
# DIÃLOGO DE BOLETIM INDIVIDUAL
# ============================================

class BoletimIndividualDialog(QDialog):
    """DiÃ¡logo para gerar boletim individual"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()

        self.setWindowTitle("Boletim Individual")
        self.setFixedSize(500, 400)
        self.setStyleSheet(GLOBAL_STYLESHEET)

        self.init_ui()
        self.carregar_alunos()

    def init_ui(self):
        """Inicializa a interface do diÃ¡logo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # TÃ­tulo
        lbl_titulo = QLabel("BOLETIM INDIVIDUAL")
        lbl_titulo.setObjectName("title")

        # SeleÃ§Ã£o do aluno
        group_selecao = QGroupBox("SELECIONE O ALUNO")
        group_selecao.setStyleSheet("""
            QGroupBox {
                font-weight: 600;
                border: 2px solid #dce1e6;
                border-radius: 8px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 15px;
                padding: 0 10px;
                background-color: #f5f7fa;
            }
        """)

        layout_selecao = QFormLayout(group_selecao)
        layout_selecao.setSpacing(15)

        # Combo para selecionar aluno
        lbl_aluno = QLabel("Aluno:")
        self.combo_aluno_boletim = QComboBox()
        self.combo_aluno_boletim.addItem("Selecione um aluno")

        # Combo para selecionar ano/semestre
        lbl_periodo = QLabel("Ano letivo:")
        self.combo_ano_boletim = QComboBox()

        # Carregar anos disponÃ­veis
        anos = list(range(date.today().year - 5, date.today().year + 1))
        for ano in reversed(anos):
            self.combo_ano_boletim.addItem(str(ano))

        self.combo_ano_boletim.setCurrentText(str(date.today().year))

        layout_selecao.addRow(lbl_aluno, self.combo_aluno_boletim)
        layout_selecao.addRow(lbl_periodo, self.combo_ano_boletim)

        # OpÃ§Ãµes
        group_opcoes = QGroupBox("OPÃ‡Ã•ES DO BOLETIM")
        group_opcoes.setStyleSheet(group_selecao.styleSheet())

        layout_opcoes = QVBoxLayout(group_opcoes)

        self.check_todas_disciplinas = QCheckBox("Incluir todas as disciplinas")
        self.check_todas_disciplinas.setChecked(True)

        self.check_frequencia = QCheckBox("Incluir registro de frequÃªncia")
        self.check_frequencia.setChecked(True)

        self.check_observacoes = QCheckBox("Incluir observaÃ§Ãµes dos professores")

        self.check_assinatura = QCheckBox("Incluir espaÃ§o para assinatura")
        self.check_assinatura.setChecked(True)

        layout_opcoes.addWidget(self.check_todas_disciplinas)
        layout_opcoes.addWidget(self.check_frequencia)
        layout_opcoes.addWidget(self.check_observacoes)
        layout_opcoes.addWidget(self.check_assinatura)

        # BotÃµes
        botoes_layout = QHBoxLayout()

        btn_gerar = AnimacaoBotao("GERAR BOLETIM", cor_normal="#27ae60", cor_hover="#219653", cor_press="#1e874b")
        btn_gerar.setMinimumHeight(45)
        btn_gerar.clicked.connect(self.gerar_boletim)

        btn_preview = AnimacaoBotao("PRÃ‰-VISUALIZAR", cor_normal="#3498db", cor_hover="#2980b9", cor_press="#1c6ea4")
        btn_preview.setMinimumHeight(45)
        btn_preview.clicked.connect(self.previsualizar_boletim)

        btn_fechar = QPushButton("FECHAR")
        btn_fechar.setObjectName("danger")
        btn_fechar.setMinimumHeight(45)
        btn_fechar.clicked.connect(self.close)

        botoes_layout.addWidget(btn_gerar)
        botoes_layout.addWidget(btn_preview)
        botoes_layout.addStretch()
        botoes_layout.addWidget(btn_fechar)

        # Adicionar tudo ao layout
        layout.addWidget(lbl_titulo)
        layout.addWidget(group_selecao)
        layout.addWidget(group_opcoes)
        layout.addStretch()
        layout.addLayout(botoes_layout)

    def carregar_alunos(self):
        """Carrega alunos ativos para o boletim"""
        try:
            alunos = self.db.execute_query('''
                SELECT id, nome, turma, serie 
                FROM alunos 
                WHERE status = 'Ativo'
                ORDER BY nome
            ''', fetch=True)

            for id_aluno, nome, turma, serie in alunos:
                texto = f"{nome}"
                if turma:
                    texto += f" - {turma}"
                if serie:
                    texto += f" ({serie})"

                self.combo_aluno_boletim.addItem(texto, id_aluno)

        except Exception as e:
            print(f"Erro ao carregar alunos: {e}")

    def gerar_boletim(self):
        """Gera o boletim individual"""
        if self.combo_aluno_boletim.currentIndex() == 0:
            QMessageBox.warning(self, "SeleÃ§Ã£o necessÃ¡ria",
                                "Por favor, selecione um aluno.")
            return

        aluno_id = self.combo_aluno_boletim.currentData()
        ano_letivo = self.combo_ano_boletim.currentText()

        try:
            # Obter dados do aluno
            aluno = self.db.execute_query('''
                SELECT nome, turma, serie, data_nascimento
                FROM alunos 
                WHERE id = ?
            ''', (aluno_id,), fetch=True)

            if not aluno:
                QMessageBox.warning(self, "Aluno nÃ£o encontrado",
                                    "NÃ£o foi possÃ­vel encontrar os dados do aluno.")
                return

            nome_aluno, turma, serie, data_nasc = aluno[0]

            # Obter notas do aluno
            notas = self.db.execute_query('''
                SELECT d.nome as disciplina, n.bimestre, 
                       n.nota1, n.nota2, n.nota3, n.nota4,
                       n.media, n.situacao, n.observacoes
                FROM notas n
                JOIN disciplinas d ON n.disciplina_id = d.id
                WHERE n.aluno_id = ? 
                ORDER BY d.nome, n.bimestre
            ''', (aluno_id,), fetch=True)

            # Obter frequÃªncia do aluno
            frequencia = self.db.execute_query('''
                SELECT COUNT(*) as total_aulas,
                       SUM(CASE WHEN presente = 1 THEN 1 ELSE 0 END) as presencas,
                       SUM(CASE WHEN presente = 0 AND justificativa IS NOT NULL THEN 1 ELSE 0 END) as faltas_justificadas,
                       SUM(CASE WHEN presente = 0 AND justificativa IS NULL THEN 1 ELSE 0 END) as faltas_nao_justificadas
                FROM frequencia
                WHERE aluno_id = ? AND strftime('%Y', data) = ?
            ''', (aluno_id, ano_letivo), fetch=True)

            # Criar boletim
            boletim = f"""
            {'=' * 60}
            BOLETIM ESCOLAR - {ano_letivo}
            {'=' * 60}

            DADOS DO ALUNO:
            Nome: {nome_aluno}
            Turma: {turma if turma else 'NÃ£o informada'}
            SÃ©rie: {serie if serie else 'NÃ£o informada'}

            {'=' * 60}
            DESEMPENHO ACADÃŠMICO:
            {'=' * 60}
            """

            if not notas:
                boletim += "\nNenhuma nota registrada para este aluno.\n"
            else:
                # Agrupar por disciplina
                disciplinas = {}
                for nota in notas:
                    disciplina, bimestre, n1, n2, n3, n4, media, situacao, obs = nota

                    if disciplina not in disciplinas:
                        disciplinas[disciplina] = []

                    disciplinas[disciplina].append({
                        'bimestre': bimestre,
                        'notas': [n1, n2, n3, n4],
                        'media': media,
                        'situacao': situacao,
                        'observacoes': obs
                    })

                # Adicionar notas por disciplina
                for disciplina, dados in disciplinas.items():
                    boletim += f"\nDisciplina: {disciplina}"
                    boletim += "\n" + "-" * 40

                    for dado in dados:
                        boletim += f"\nBimestre {dado['bimestre']}: "

                        # Adicionar notas
                        notas_str = []
                        for i, nota in enumerate(dado['notas'], 1):
                            if nota is not None:
                                notas_str.append(f"N{i}: {nota:.1f}")

                        if notas_str:
                            boletim += f"{', '.join(notas_str)}"

                        # Adicionar mÃ©dia
                        if dado['media'] is not None:
                            boletim += f" | MÃ©dia: {dado['media']:.1f}"

                        # Adicionar situaÃ§Ã£o
                        if dado['situacao']:
                            boletim += f" | SituaÃ§Ã£o: {dado['situacao']}"

                    boletim += "\n"

            # Adicionar frequÃªncia
            if self.check_frequencia.isChecked() and frequencia:
                total, presencas, faltas_just, faltas_nao_just = frequencia[0]

                boletim += f"\n{'=' * 60}"
                boletim += f"\nFREQUÃŠNCIA - {ano_letivo}:"
                boletim += f"\n{'=' * 60}"

                if total and total > 0:
                    percent_presenca = (presencas / total) * 100

                    boletim += f"\nTotal de aulas: {total or 0}"
                    boletim += f"\nPresenÃ§as: {presencas or 0}"
                    boletim += f"\nFaltas justificadas: {faltas_just or 0}"
                    boletim += f"\nFaltas nÃ£o justificadas: {faltas_nao_just or 0}"
                    boletim += f"\nPercentual de presenÃ§a: {percent_presenca:.1f}%"
                else:
                    boletim += "\nNenhum registro de frequÃªncia encontrado."

            # Adicionar espaÃ§o para assinatura
            if self.check_assinatura.isChecked():
                boletim += f"\n\n{'=' * 60}"
                boletim += f"\n\nASSINATURAS:"
                boletim += f"\n\nResponsÃ¡vel pelo aluno: ___________________________"
                boletim += f"\n\nCoordenador(a): ___________________________"
                boletim += f"\n\nData: ___/___/_______"

            QMessageBox.information(self, "Boletim Gerado",
                                    f"Boletim gerado com sucesso para {nome_aluno}!\n\n"
                                    f"Ano letivo: {ano_letivo}\n\n"
                                    "Para visualizaÃ§Ã£o completa, use a opÃ§Ã£o PRÃ‰-VISUALIZAR.")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao gerar boletim:\n{str(e)}")

    def previsualizar_boletim(self):
        """PrÃ©-visualiza o boletim gerado"""
        QMessageBox.information(self, "Funcionalidade em desenvolvimento",
                                "A prÃ©-visualizaÃ§Ã£o do boletim serÃ¡ implementada na prÃ³xima versÃ£o.")


# ============================================
# DIÃLOGO DE ESTATÃSTICAS GERAIS
# ============================================

class EstatisticasGeraisDialog(QDialog):
    """DiÃ¡logo para exibir estatÃ­sticas gerais do sistema"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()

        self.setWindowTitle("EstatÃ­sticas Gerais")
        self.setFixedSize(800, 600)
        self.setStyleSheet(GLOBAL_STYLESHEET)

        self.init_ui()
        self.carregar_estatisticas()

    def init_ui(self):
        """Inicializa a interface do diÃ¡logo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # TÃ­tulo
        lbl_titulo = QLabel("ESTATÃSTICAS GERAIS DO SISTEMA")
        lbl_titulo.setObjectName("title")

        # Abas
        tab_widget = QTabWidget()

        # Aba: VisÃ£o Geral
        aba_geral = QWidget()
        self.layout_geral = QFormLayout(aba_geral)
        self.layout_geral.setContentsMargins(20, 20, 20, 20)
        self.layout_geral.setSpacing(10)

        # Aba: Alunos
        aba_alunos = QWidget()
        self.layout_alunos = QFormLayout(aba_alunos)
        self.layout_alunos.setContentsMargins(20, 20, 20, 20)
        self.layout_alunos.setSpacing(10)

        # Aba: Desempenho
        aba_desempenho = QWidget()
        self.layout_desempenho = QFormLayout(aba_desempenho)
        self.layout_desempenho.setContentsMargins(20, 20, 20, 20)
        self.layout_desempenho.setSpacing(10)

        # Aba: FrequÃªncia
        aba_frequencia = QWidget()
        self.layout_frequencia = QFormLayout(aba_frequencia)
        self.layout_frequencia.setContentsMargins(20, 20, 20, 20)
        self.layout_frequencia.setSpacing(10)

        # Adicionar abas
        tab_widget.addTab(aba_geral, "VisÃ£o Geral")
        tab_widget.addTab(aba_alunos, "Alunos")
        tab_widget.addTab(aba_desempenho, "Desempenho")
        tab_widget.addTab(aba_frequencia, "FrequÃªncia")

        # BotÃµes
        botoes_layout = QHBoxLayout()

        btn_atualizar = AnimacaoBotao("ATUALIZAR", cor_normal="#3498db", cor_hover="#2980b9", cor_press="#1c6ea4")
        btn_atualizar.setMinimumHeight(45)
        btn_atualizar.clicked.connect(self.carregar_estatisticas)

        btn_exportar = AnimacaoBotao("EXPORTAR", cor_normal="#27ae60", cor_hover="#219653", cor_press="#1e874b")
        btn_exportar.setMinimumHeight(45)
        btn_exportar.clicked.connect(self.exportar_estatisticas)

        btn_fechar = QPushButton("FECHAR")
        btn_fechar.setObjectName("danger")
        btn_fechar.setMinimumHeight(45)
        btn_fechar.clicked.connect(self.close)

        botoes_layout.addWidget(btn_atualizar)
        botoes_layout.addWidget(btn_exportar)
        botoes_layout.addStretch()
        botoes_layout.addWidget(btn_fechar)

        # Adicionar tudo ao layout
        layout.addWidget(lbl_titulo)
        layout.addWidget(tab_widget)
        layout.addLayout(botoes_layout)

    def carregar_estatisticas(self):
        """Carrega as estatÃ­sticas do sistema"""
        try:
            # Limpar layouts
            self.limpar_layout(self.layout_geral)
            self.limpar_layout(self.layout_alunos)
            self.limpar_layout(self.layout_desempenho)
            self.limpar_layout(self.layout_frequencia)

            # VisÃ£o Geral
            self.adicionar_estatistica(self.layout_geral, "Data da consulta:",
                                       datetime.now().strftime('%d/%m/%Y %H:%M'))

            # Total de registros
            total_alunos = self.db.execute_query("SELECT COUNT(*) FROM alunos", fetch=True)[0][0]
            total_professores = \
            self.db.execute_query("SELECT COUNT(*) FROM professores WHERE ativo = 1", fetch=True)[0][0]
            total_disciplinas = \
            self.db.execute_query("SELECT COUNT(*) FROM disciplinas WHERE ativa = 1", fetch=True)[0][0]
            total_turmas = self.db.execute_query("SELECT COUNT(*) FROM turmas WHERE ativa = 1", fetch=True)[0][0]

            self.adicionar_estatistica(self.layout_geral, "Total de alunos:", str(total_alunos))
            self.adicionar_estatistica(self.layout_geral, "Total de professores:", str(total_professores))
            self.adicionar_estatistica(self.layout_geral, "Total de disciplinas:", str(total_disciplinas))
            self.adicionar_estatistica(self.layout_geral, "Total de turmas:", str(total_turmas))

            # EstatÃ­sticas de Alunos
            alunos_ativos = self.db.execute_query(
                "SELECT COUNT(*) FROM alunos WHERE status = 'Ativo'",
                fetch=True
            )[0][0]

            alunos_inativos = self.db.execute_query(
                "SELECT COUNT(*) FROM alunos WHERE status != 'Ativo'",
                fetch=True
            )[0][0]

            alunos_por_serie = self.db.execute_query('''
                SELECT serie, COUNT(*) 
                FROM alunos 
                WHERE status = 'Ativo' AND serie IS NOT NULL
                GROUP BY serie 
                ORDER BY serie
            ''', fetch=True)

            self.adicionar_estatistica(self.layout_alunos, "Alunos ativos:", str(alunos_ativos))
            self.adicionar_estatistica(self.layout_alunos, "Alunos inativos:", str(alunos_inativos))

            percent_ativo = (alunos_ativos / total_alunos * 100) if total_alunos > 0 else 0
            self.adicionar_estatistica_colorida(
                self.layout_alunos, "Percentual ativo:",
                f"{percent_ativo:.1f}%",
                "#27ae60" if percent_ativo > 90 else "#f39c12" if percent_ativo > 70 else "#e74c3c"
            )

            for serie, quantidade in alunos_por_serie:
                self.adicionar_estatistica(self.layout_alunos, f"SÃ©rie {serie}:", str(quantidade))

            # EstatÃ­sticas de Desempenho
            media_geral = self.db.execute_query(
                "SELECT AVG(media) FROM notas WHERE media IS NOT NULL",
                fetch=True
            )[0][0]

            total_notas = self.db.execute_query("SELECT COUNT(*) FROM notas", fetch=True)[0][0]
            aprovados = self.db.execute_query(
                "SELECT COUNT(*) FROM notas WHERE situacao = 'Aprovado'",
                fetch=True
            )[0][0]

            recuperacao = self.db.execute_query(
                "SELECT COUNT(*) FROM notas WHERE situacao = 'RecuperaÃ§Ã£o'",
                fetch=True
            )[0][0]

            reprovados = self.db.execute_query(
                "SELECT COUNT(*) FROM notas WHERE situacao = 'Reprovado'",
                fetch=True
            )[0][0]

            self.adicionar_estatistica(self.layout_desempenho, "MÃ©dia geral:",
                                       f"{media_geral:.2f}" if media_geral else "N/A")

            self.adicionar_estatistica(self.layout_desempenho, "Total de notas:", str(total_notas))

            if total_notas > 0:
                percent_aprovados = (aprovados / total_notas) * 100
                percent_recuperacao = (recuperacao / total_notas) * 100
                percent_reprovados = (reprovados / total_notas) * 100

                self.adicionar_estatistica_colorida(
                    self.layout_desempenho, "Aprovados:",
                    f"{aprovados} ({percent_aprovados:.1f}%)", "#27ae60"
                )
                self.adicionar_estatistica_colorida(
                    self.layout_desempenho, "RecuperaÃ§Ã£o:",
                    f"{recuperacao} ({percent_recuperacao:.1f}%)", "#f39c12"
                )
                self.adicionar_estatistica_colorida(
                    self.layout_desempenho, "Reprovados:",
                    f"{reprovados} ({percent_reprovados:.1f}%)", "#e74c3c"
                )

            # EstatÃ­sticas de FrequÃªncia
            total_registros_freq = self.db.execute_query(
                "SELECT COUNT(*) FROM frequencia",
                fetch=True
            )[0][0]

            presencas = self.db.execute_query(
                "SELECT COUNT(*) FROM frequencia WHERE presente = 1",
                fetch=True
            )[0][0]

            faltas = self.db.execute_query(
                "SELECT COUNT(*) FROM frequencia WHERE presente = 0",
                fetch=True
            )[0][0]

            faltas_justificadas = self.db.execute_query(
                "SELECT COUNT(*) FROM frequencia WHERE presente = 0 AND justificativa IS NOT NULL",
                fetch=True
            )[0][0]

            self.adicionar_estatistica(self.layout_frequencia, "Total de registros:", str(total_registros_freq))
            self.adicionar_estatistica(self.layout_frequencia, "PresenÃ§as:", str(presencas))
            self.adicionar_estatistica(self.layout_frequencia, "Faltas:", str(faltas))
            self.adicionar_estatistica(self.layout_frequencia, "Faltas justificadas:", str(faltas_justificadas))

            if total_registros_freq > 0:
                percent_presenca = (presencas / total_registros_freq) * 100
                percent_falta = (faltas / total_registros_freq) * 100

                self.adicionar_estatistica_colorida(
                    self.layout_frequencia, "Taxa de presenÃ§a:",
                    f"{percent_presenca:.1f}%",
                    "#27ae60" if percent_presenca > 90 else "#f39c12" if percent_presenca > 80 else "#e74c3c"
                )

                if faltas > 0:
                    percent_justificadas = (faltas_justificadas / faltas) * 100
                    self.adicionar_estatistica(
                        self.layout_frequencia, "Faltas justificadas:",
                        f"{percent_justificadas:.1f}% das faltas"
                    )

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar estatÃ­sticas:\n{str(e)}")

    def limpar_layout(self, layout):
        """Limpa todos os widgets de um layout"""
        while layout.rowCount() > 0:
            layout.removeRow(0)

    def adicionar_estatistica(self, layout, label, valor):
        """Adiciona uma estatÃ­stica ao layout"""
        lbl_label = QLabel(label)
        lbl_label.setStyleSheet("font-weight: 600; color: #2c3e50; font-size: 13px;")

        lbl_valor = QLabel(valor)
        lbl_valor.setStyleSheet("color: #34495e; font-size: 13px;")

        layout.addRow(lbl_label, lbl_valor)

    def adicionar_estatistica_colorida(self, layout, label, valor, cor):
        """Adiciona uma estatÃ­stica colorida ao layout"""
        lbl_label = QLabel(label)
        lbl_label.setStyleSheet("font-weight: 600; color: #2c3e50; font-size: 13px;")

        lbl_valor = QLabel(valor)
        lbl_valor.setStyleSheet(f"color: {cor}; font-weight: 600; font-size: 13px;")

        layout.addRow(lbl_label, lbl_valor)

    def exportar_estatisticas(self):
        """Exporta as estatÃ­sticas para um arquivo"""
        QMessageBox.information(self, "Funcionalidade em desenvolvimento",
                                "A exportaÃ§Ã£o de estatÃ­sticas serÃ¡ implementada na prÃ³xima versÃ£o.")


"""
PROJETO ESCOLA - SISTEMA DE GESTÃƒO ESCOLAR
Parte 8/10 - ContinuaÃ§Ã£o: RelatÃ³rio Personalizado, ExportaÃ§Ã£o e ConfiguraÃ§Ãµes
"""


# ============================================
# DIÃLOGO DE RELATÃ“RIO PERSONALIZADO
# ============================================

class RelatorioPersonalizadoDialog(QDialog):
    """DiÃ¡logo para criar relatÃ³rio personalizado"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()

        self.setWindowTitle("RelatÃ³rio Personalizado")
        self.setFixedSize(700, 600)
        self.setStyleSheet(GLOBAL_STYLESHEET)

        self.init_ui()

    def init_ui(self):
        """Inicializa a interface do diÃ¡logo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # TÃ­tulo
        lbl_titulo = QLabel("RELATÃ“RIO PERSONALIZADO")
        lbl_titulo.setObjectName("title")

        # SeÃ§Ã£o: Tipo de RelatÃ³rio
        group_tipo = QGroupBox("TIPO DE RELATÃ“RIO")
        group_tipo.setStyleSheet("""
            QGroupBox {
                font-weight: 600;
                border: 2px solid #dce1e6;
                border-radius: 8px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 15px;
                padding: 0 10px;
                background-color: #f5f7fa;
            }
        """)

        layout_tipo = QVBoxLayout(group_tipo)

        self.radio_alunos = QRadioButton("RelatÃ³rio de Alunos")
        self.radio_alunos.setChecked(True)
        self.radio_alunos.toggled.connect(self.atualizar_opcoes)

        self.radio_notas = QRadioButton("RelatÃ³rio de Notas")
        self.radio_notas.toggled.connect(self.atualizar_opcoes)

        self.radio_frequencia = QRadioButton("RelatÃ³rio de FrequÃªncia")
        self.radio_frequencia.toggled.connect(self.atualizar_opcoes)

        self.radio_financeiro = QRadioButton("RelatÃ³rio Financeiro")
        self.radio_financeiro.toggled.connect(self.atualizar_opcoes)

        layout_tipo.addWidget(self.radio_alunos)
        layout_tipo.addWidget(self.radio_notas)
        layout_tipo.addWidget(self.radio_frequencia)
        layout_tipo.addWidget(self.radio_financeiro)

        # SeÃ§Ã£o: Filtros (dinÃ¢mica)
        self.group_filtros = QGroupBox("FILTROS")
        self.group_filtros.setStyleSheet(group_tipo.styleSheet())

        self.layout_filtros = QVBoxLayout(self.group_filtros)

        # SeÃ§Ã£o: Campos a Incluir
        group_campos = QGroupBox("CAMPOS A INCLUIR")
        group_campos.setStyleSheet(group_tipo.styleSheet())

        self.layout_campos = QVBoxLayout(group_campos)

        # Inicializar opÃ§Ãµes
        self.atualizar_opcoes()

        # SeÃ§Ã£o: Formato de SaÃ­da
        group_formato = QGroupBox("FORMATO DE SAÃDA")
        group_formato.setStyleSheet(group_tipo.styleSheet())

        layout_formato = QVBoxLayout(group_formato)

        self.check_pdf = QCheckBox("Gerar em PDF")
        self.check_pdf.setChecked(True)

        self.check_excel = QCheckBox("Gerar em Excel")
        self.check_excel.setChecked(True)

        self.check_tela = QCheckBox("Exibir na tela")

        layout_formato.addWidget(self.check_pdf)
        layout_formato.addWidget(self.check_excel)
        layout_formato.addWidget(self.check_tela)

        # BotÃµes
        botoes_layout = QHBoxLayout()

        btn_gerar = AnimacaoBotao("GERAR RELATÃ“RIO", cor_normal="#27ae60", cor_hover="#219653", cor_press="#1e874b")
        btn_gerar.setMinimumHeight(45)
        btn_gerar.clicked.connect(self.gerar_relatorio)

        btn_salvar_template = AnimacaoBotao("SALVAR TEMPLATE", cor_normal="#3498db", cor_hover="#2980b9",
                                            cor_press="#1c6ea4")
        btn_salvar_template.setMinimumHeight(45)
        btn_salvar_template.clicked.connect(self.salvar_template)

        btn_fechar = QPushButton("FECHAR")
        btn_fechar.setObjectName("danger")
        btn_fechar.setMinimumHeight(45)
        btn_fechar.clicked.connect(self.close)

        botoes_layout.addWidget(btn_gerar)
        botoes_layout.addWidget(btn_salvar_template)
        botoes_layout.addStretch()
        botoes_layout.addWidget(btn_fechar)

        # Adicionar tudo ao layout
        layout.addWidget(lbl_titulo)
        layout.addWidget(group_tipo)
        layout.addWidget(self.group_filtros)
        layout.addWidget(group_campos)
        layout.addWidget(group_formato)
        layout.addStretch()
        layout.addLayout(botoes_layout)

    def atualizar_opcoes(self):
        """Atualiza as opÃ§Ãµes de filtros e campos baseado no tipo selecionado"""
        # Limpar layouts
        self.limpar_layout(self.layout_filtros)
        self.limpar_layout(self.layout_campos)

        if self.radio_alunos.isChecked():
            self.configurar_opcoes_alunos()
        elif self.radio_notas.isChecked():
            self.configurar_opcoes_notas()
        elif self.radio_frequencia.isChecked():
            self.configurar_opcoes_frequencia()
        elif self.radio_financeiro.isChecked():
            self.configurar_opcoes_financeiro()

    def limpar_layout(self, layout):
        """Limpa todos os widgets de um layout"""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def configurar_opcoes_alunos(self):
        """Configura opÃ§Ãµes para relatÃ³rio de alunos"""
        # Filtros
        lbl_status = QLabel("Status:")
        self.combo_status_personalizado = QComboBox()
        self.combo_status_personalizado.addItems(["Todos", "Ativos", "Inativos", "Transferidos", "Evadidos"])

        lbl_turma = QLabel("Turma:")
        self.combo_turma_personalizado = QComboBox()
        self.combo_turma_personalizado.addItem("Todas as turmas")
        self.carregar_turmas_combo(self.combo_turma_personalizado)

        lbl_serie = QLabel("SÃ©rie:")
        self.combo_serie_personalizado = QComboBox()
        self.combo_serie_personalizado.addItem("Todas as sÃ©ries")
        self.carregar_series_combo(self.combo_serie_personalizado)

        # Layout de filtros
        form_filtros = QFormLayout()
        form_filtros.addRow(lbl_status, self.combo_status_personalizado)
        form_filtros.addRow(lbl_turma, self.combo_turma_personalizado)
        form_filtros.addRow(lbl_serie, self.combo_serie_personalizado)

        self.layout_filtros.addLayout(form_filtros)

        # Campos a incluir
        self.check_nome = QCheckBox("Nome")
        self.check_nome.setChecked(True)

        self.check_cpf = QCheckBox("CPF")

        self.check_data_nasc = QCheckBox("Data de Nascimento")

        self.check_turma = QCheckBox("Turma")
        self.check_turma.setChecked(True)

        self.check_serie = QCheckBox("SÃ©rie")
        self.check_serie.setChecked(True)

        self.check_responsavel = QCheckBox("ResponsÃ¡vel")

        self.check_telefone = QCheckBox("Telefone")

        self.check_endereco = QCheckBox("EndereÃ§o")

        self.check_status = QCheckBox("Status")
        self.check_status.setChecked(True)

        # Layout de campos
        grid_campos = QGridLayout()
        grid_campos.addWidget(self.check_nome, 0, 0)
        grid_campos.addWidget(self.check_cpf, 0, 1)
        grid_campos.addWidget(self.check_data_nasc, 0, 2)
        grid_campos.addWidget(self.check_turma, 1, 0)
        grid_campos.addWidget(self.check_serie, 1, 1)
        grid_campos.addWidget(self.check_responsavel, 1, 2)
        grid_campos.addWidget(self.check_telefone, 2, 0)
        grid_campos.addWidget(self.check_endereco, 2, 1)
        grid_campos.addWidget(self.check_status, 2, 2)

        self.layout_campos.addLayout(grid_campos)

    def configurar_opcoes_notas(self):
        """Configura opÃ§Ãµes para relatÃ³rio de notas"""
        # Filtros
        lbl_turma = QLabel("Turma:")
        self.combo_turma_notas_personalizado = QComboBox()
        self.combo_turma_notas_personalizado.addItem("Todas as turmas")
        self.carregar_turmas_combo(self.combo_turma_notas_personalizado)

        lbl_disciplina = QLabel("Disciplina:")
        self.combo_disciplina_personalizado = QComboBox()
        self.combo_disciplina_personalizado.addItem("Todas as disciplinas")
        self.carregar_disciplinas_combo(self.combo_disciplina_personalizado)

        lbl_bimestre = QLabel("Bimestre:")
        self.combo_bimestre_personalizado = QComboBox()
        self.combo_bimestre_personalizado.addItems(
            ["Todos", "1Âº Bimestre", "2Âº Bimestre", "3Âº Bimestre", "4Âº Bimestre"])

        # Layout de filtros
        form_filtros = QFormLayout()
        form_filtros.addRow(lbl_turma, self.combo_turma_notas_personalizado)
        form_filtros.addRow(lbl_disciplina, self.combo_disciplina_personalizado)
        form_filtros.addRow(lbl_bimestre, self.combo_bimestre_personalizado)

        self.layout_filtros.addLayout(form_filtros)

        # Campos a incluir
        self.check_aluno = QCheckBox("Nome do Aluno")
        self.check_aluno.setChecked(True)

        self.check_turma_nota = QCheckBox("Turma")
        self.check_turma_nota.setChecked(True)

        self.check_disciplina = QCheckBox("Disciplina")
        self.check_disciplina.setChecked(True)

        self.check_bimestre = QCheckBox("Bimestre")
        self.check_bimestre.setChecked(True)

        self.check_nota1 = QCheckBox("Nota 1")

        self.check_nota2 = QCheckBox("Nota 2")

        self.check_nota3 = QCheckBox("Nota 3")

        self.check_nota4 = QCheckBox("Nota 4")

        self.check_media = QCheckBox("MÃ©dia")
        self.check_media.setChecked(True)

        self.check_situacao = QCheckBox("SituaÃ§Ã£o")
        self.check_situacao.setChecked(True)

        # Layout de campos
        grid_campos = QGridLayout()
        grid_campos.addWidget(self.check_aluno, 0, 0)
        grid_campos.addWidget(self.check_turma_nota, 0, 1)
        grid_campos.addWidget(self.check_disciplina, 0, 2)
        grid_campos.addWidget(self.check_bimestre, 1, 0)
        grid_campos.addWidget(self.check_nota1, 1, 1)
        grid_campos.addWidget(self.check_nota2, 1, 2)
        grid_campos.addWidget(self.check_nota3, 2, 0)
        grid_campos.addWidget(self.check_nota4, 2, 1)
        grid_campos.addWidget(self.check_media, 2, 2)
        grid_campos.addWidget(self.check_situacao, 3, 0)

        self.layout_campos.addLayout(grid_campos)

    def configurar_opcoes_frequencia(self):
        """Configura opÃ§Ãµes para relatÃ³rio de frequÃªncia"""
        # Filtros
        lbl_turma = QLabel("Turma:")
        self.combo_turma_freq_personalizado = QComboBox()
        self.combo_turma_freq_personalizado.addItem("Todas as turmas")
        self.carregar_turmas_combo(self.combo_turma_freq_personalizado)

        lbl_periodo = QLabel("PerÃ­odo:")

        periodo_layout = QHBoxLayout()
        self.date_inicio_personalizado = QDateEdit()
        self.date_inicio_personalizado.setCalendarPopup(True)
        self.date_inicio_personalizado.setDate(QDate.currentDate().addMonths(-1))
        self.date_inicio_personalizado.setDisplayFormat("dd/MM/yyyy")

        self.date_fim_personalizado = QDateEdit()
        self.date_fim_personalizado.setCalendarPopup(True)
        self.date_fim_personalizado.setDate(QDate.currentDate())
        self.date_fim_personalizado.setDisplayFormat("dd/MM/yyyy")

        periodo_layout.addWidget(self.date_inicio_personalizado)
        periodo_layout.addWidget(QLabel("atÃ©"))
        periodo_layout.addWidget(self.date_fim_personalizado)

        # Layout de filtros
        form_filtros = QFormLayout()
        form_filtros.addRow(lbl_turma, self.combo_turma_freq_personalizado)
        form_filtros.addRow(lbl_periodo, periodo_layout)

        self.layout_filtros.addLayout(form_filtros)

        # Campos a incluir
        self.check_aluno_freq = QCheckBox("Nome do Aluno")
        self.check_aluno_freq.setChecked(True)

        self.check_turma_freq = QCheckBox("Turma")
        self.check_turma_freq.setChecked(True)

        self.check_data = QCheckBox("Data")
        self.check_data.setChecked(True)

        self.check_disciplina_freq = QCheckBox("Disciplina")

        self.check_presente = QCheckBox("Presente")
        self.check_presente.setChecked(True)

        self.check_justificativa = QCheckBox("Justificativa")

        self.check_observacoes_freq = QCheckBox("ObservaÃ§Ãµes")

        # Layout de campos
        grid_campos = QGridLayout()
        grid_campos.addWidget(self.check_aluno_freq, 0, 0)
        grid_campos.addWidget(self.check_turma_freq, 0, 1)
        grid_campos.addWidget(self.check_data, 0, 2)
        grid_campos.addWidget(self.check_disciplina_freq, 1, 0)
        grid_campos.addWidget(self.check_presente, 1, 1)
        grid_campos.addWidget(self.check_justificativa, 1, 2)
        grid_campos.addWidget(self.check_observacoes_freq, 2, 0)

        self.layout_campos.addLayout(grid_campos)

    def configurar_opcoes_financeiro(self):
        """Configura opÃ§Ãµes para relatÃ³rio financeiro (simplificado)"""
        lbl_info = QLabel("MÃ³dulo financeiro nÃ£o implementado nesta versÃ£o.")
        lbl_info.setStyleSheet("color: #f39c12; font-weight: 600; padding: 10px;")

        self.layout_filtros.addWidget(lbl_info)

        lbl_campos = QLabel("Nenhum campo disponÃ­vel para este mÃ³dulo.")
        lbl_campos.setStyleSheet("color: #95a5a6; padding: 10px;")

        self.layout_campos.addWidget(lbl_campos)

    def carregar_turmas_combo(self, combo):
        """Carrega turmas em um combobox"""
        try:
            turmas = self.db.execute_query('''
                SELECT DISTINCT nome 
                FROM turmas 
                WHERE ativa = 1
                ORDER BY nome
            ''', fetch=True)

            for turma in turmas:
                if turma[0]:
                    combo.addItem(turma[0])

        except Exception as e:
            print(f"Erro ao carregar turmas: {e}")

    def carregar_series_combo(self, combo):
        """Carrega sÃ©ries em um combobox"""
        try:
            series = self.db.execute_query('''
                SELECT DISTINCT serie 
                FROM alunos 
                WHERE serie IS NOT NULL AND serie != ''
                ORDER BY serie
            ''', fetch=True)

            for serie in series:
                if serie[0]:
                    combo.addItem(serie[0])

        except Exception as e:
            print(f"Erro ao carregar sÃ©ries: {e}")

    def carregar_disciplinas_combo(self, combo):
        """Carrega disciplinas em um combobox"""
        try:
            disciplinas = self.db.execute_query('''
                SELECT DISTINCT nome 
                FROM disciplinas 
                WHERE ativa = 1
                ORDER BY nome
            ''', fetch=True)

            for disciplina in disciplinas:
                if disciplina[0]:
                    combo.addItem(disciplina[0])

        except Exception as e:
            print(f"Erro ao carregar disciplinas: {e}")

    def gerar_relatorio(self):
        """Gera o relatÃ³rio personalizado"""
        if self.radio_financeiro.isChecked():
            QMessageBox.information(self, "MÃ³dulo nÃ£o implementado",
                                    "O mÃ³dulo financeiro nÃ£o estÃ¡ implementado nesta versÃ£o.")
            return

        # Coletar parÃ¢metros
        tipo_relatorio = ""
        if self.radio_alunos.isChecked():
            tipo_relatorio = "alunos"
        elif self.radio_notas.isChecked():
            tipo_relatorio = "notas"
        elif self.radio_frequencia.isChecked():
            tipo_relatorio = "frequencia"

        # Coletar filtros
        filtros = {}
        if tipo_relatorio == "alunos":
            filtros['status'] = self.combo_status_personalizado.currentText()
            filtros['turma'] = self.combo_turma_personalizado.currentText()
            filtros['serie'] = self.combo_serie_personalizado.currentText()

        elif tipo_relatorio == "notas":
            filtros['turma'] = self.combo_turma_notas_personalizado.currentText()
            filtros['disciplina'] = self.combo_disciplina_personalizado.currentText()
            filtros['bimestre'] = self.combo_bimestre_personalizado.currentText()

        elif tipo_relatorio == "frequencia":
            filtros['turma'] = self.combo_turma_freq_personalizado.currentText()
            filtros['data_inicio'] = self.date_inicio_personalizado.date().toString("yyyy-MM-dd")
            filtros['data_fim'] = self.date_fim_personalizado.date().toString("yyyy-MM-dd")

        # Coletar campos selecionados
        campos = []
        if tipo_relatorio == "alunos":
            if self.check_nome.isChecked(): campos.append("nome")
            if self.check_cpf.isChecked(): campos.append("cpf")
            if self.check_data_nasc.isChecked(): campos.append("data_nascimento")
            if self.check_turma.isChecked(): campos.append("turma")
            if self.check_serie.isChecked(): campos.append("serie")
            if self.check_responsavel.isChecked(): campos.append("responsavel")
            if self.check_telefone.isChecked(): campos.append("telefone")
            if self.check_endereco.isChecked(): campos.append("endereco")
            if self.check_status.isChecked(): campos.append("status")

        elif tipo_relatorio == "notas":
            if self.check_aluno.isChecked(): campos.append("aluno")
            if self.check_turma_nota.isChecked(): campos.append("turma")
            if self.check_disciplina.isChecked(): campos.append("disciplina")
            if self.check_bimestre.isChecked(): campos.append("bimestre")
            if self.check_nota1.isChecked(): campos.append("nota1")
            if self.check_nota2.isChecked(): campos.append("nota2")
            if self.check_nota3.isChecked(): campos.append("nota3")
            if self.check_nota4.isChecked(): campos.append("nota4")
            if self.check_media.isChecked(): campos.append("media")
            if self.check_situacao.isChecked(): campos.append("situacao")

        elif tipo_relatorio == "frequencia":
            if self.check_aluno_freq.isChecked(): campos.append("aluno")
            if self.check_turma_freq.isChecked(): campos.append("turma")
            if self.check_data.isChecked(): campos.append("data")
            if self.check_disciplina_freq.isChecked(): campos.append("disciplina")
            if self.check_presente.isChecked(): campos.append("presente")
            if self.check_justificativa.isChecked(): campos.append("justificativa")
            if self.check_observacoes_freq.isChecked(): campos.append("observacoes")

        if not campos:
            QMessageBox.warning(self, "Campos necessÃ¡rios",
                                "Selecione pelo menos um campo para incluir no relatÃ³rio.")
            return

        # Gerar relatÃ³rio
        try:
            # Construir query baseada no tipo e filtros
            query = self.construir_query(tipo_relatorio, filtros, campos)

            if not query:
                QMessageBox.warning(self, "Erro na query",
                                    "NÃ£o foi possÃ­vel construir a query para o relatÃ³rio.")
                return

            # Executar query
            dados = self.db.execute_query(query, fetch=True)

            if not dados:
                QMessageBox.information(self, "Sem dados",
                                        "Nenhum registro encontrado com os filtros selecionados.")
                return

            # Preparar formato de saÃ­da
            formatos = []
            if self.check_pdf.isChecked():
                formatos.append("PDF")
            if self.check_excel.isChecked():
                formatos.append("Excel")
            if self.check_tela.isChecked():
                formatos.append("Tela")

            if not formatos:
                QMessageBox.warning(self, "Formato necessÃ¡rio",
                                    "Selecione pelo menos um formato de saÃ­da.")
                return

            # Gerar relatÃ³rio nos formatos selecionados
            for formato in formatos:
                if formato == "Tela":
                    self.exibir_relatorio_tela(tipo_relatorio, dados, campos)
                elif formato == "Excel":
                    self.exportar_relatorio_excel(tipo_relatorio, dados, campos, filtros)
                elif formato == "PDF":
                    self.exportar_relatorio_pdf(tipo_relatorio, dados, campos, filtros)

            QMessageBox.information(self, "RelatÃ³rio Gerado",
                                    f"RelatÃ³rio gerado com sucesso!\n\n"
                                    f"Tipo: {tipo_relatorio.capitalize()}\n"
                                    f"Registros: {len(dados)}\n"
                                    f"Formatos: {', '.join(formatos)}")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao gerar relatÃ³rio:\n{str(e)}")

    def construir_query(self, tipo, filtros, campos):
        """Constroi a query SQL baseada no tipo e filtros"""
        if tipo == "alunos":
            query = "SELECT "

            # Mapear campos para colunas do banco
            campos_map = {
                'nome': 'nome',
                'cpf': 'cpf',
                'data_nascimento': 'data_nascimento',
                'turma': 'turma',
                'serie': 'serie',
                'responsavel': 'nome_mae',
                'telefone': 'telefone_responsavel',
                'endereco': 'endereco',
                'status': 'status'
            }

            campos_sql = []
            for campo in campos:
                if campo in campos_map:
                    campos_sql.append(campos_map[campo])

            if not campos_sql:
                return None

            query += ', '.join(campos_sql) + " FROM alunos WHERE 1=1"

            # Aplicar filtros
            if filtros['status'] != "Todos":
                query += f" AND status = '{filtros['status']}'"

            if filtros['turma'] != "Todas as turmas":
                query += f" AND turma = '{filtros['turma']}'"

            if filtros['serie'] != "Todas as sÃ©ries":
                query += f" AND serie = '{filtros['serie']}'"

            query += " ORDER BY nome"

            return query

        elif tipo == "notas":
            query = """
                SELECT a.nome as aluno, a.turma, d.nome as disciplina, 
                       n.bimestre, n.nota1, n.nota2, n.nota3, n.nota4,
                       n.media, n.situacao
                FROM notas n
                JOIN alunos a ON n.aluno_id = a.id
                JOIN disciplinas d ON n.disciplina_id = d.id
                WHERE 1=1
            """

            # Aplicar filtros
            if filtros['turma'] != "Todas as turmas":
                query += f" AND a.turma = '{filtros['turma']}'"

            if filtros['disciplina'] != "Todas as disciplinas":
                query += f" AND d.nome = '{filtros['disciplina']}'"

            if filtros['bimestre'] != "Todos":
                bimestre_num = int(filtros['bimestre'][0])
                query += f" AND n.bimestre = {bimestre_num}"

            query += " ORDER BY a.turma, a.nome, d.nome, n.bimestre"

            return query

        elif tipo == "frequencia":
            query = """
                SELECT a.nome as aluno, a.turma, f.data, 
                       d.nome as disciplina, f.presente, f.justificativa, f.observacoes
                FROM frequencia f
                JOIN alunos a ON f.aluno_id = a.id
                LEFT JOIN disciplinas d ON f.disciplina_id = d.id
                WHERE f.data BETWEEN ? AND ?
            """

            # Aplicar filtro de turma
            if filtros['turma'] != "Todas as turmas":
                query += f" AND a.turma = '{filtros['turma']}'"

            query += " ORDER BY a.turma, a.nome, f.data"

            return query

        return None

    def exibir_relatorio_tela(self, tipo, dados, campos):
        """Exibe o relatÃ³rio em uma nova janela"""
        dialog = VisualizadorRelatorioDialog(self, tipo, dados, campos)
        dialog.exec_()

    def exportar_relatorio_excel(self, tipo, dados, campos, filtros):
        """Exporta o relatÃ³rio para Excel"""
        try:
            exportador = ExportadorDados(self.db)

            # Converter dados para DataFrame
            df = pd.DataFrame(dados, columns=campos[:len(dados[0])] if dados else [])

            # Criar nome do arquivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"relatorio_{tipo}_{timestamp}"

            # Exportar
            sucesso, caminho = exportador.exportar_para_excel(
                "",  # Query vazia pois jÃ¡ temos os dados
                nome_arquivo,
                cabecalhos=campos[:len(dados[0])] if dados else []
            )

            if sucesso:
                QMessageBox.information(self, "Exportado com sucesso",
                                        f"RelatÃ³rio exportado para Excel:\n{caminho}")
            else:
                QMessageBox.warning(self, "Erro na exportaÃ§Ã£o", caminho)

        except Exception as e:
            QMessageBox.warning(self, "Erro na exportaÃ§Ã£o", f"Erro ao exportar para Excel:\n{str(e)}")

    def exportar_relatorio_pdf(self, tipo, dados, campos, filtros):
        """Exporta o relatÃ³rio para PDF"""
        QMessageBox.information(self, "Funcionalidade em desenvolvimento",
                                "A exportaÃ§Ã£o para PDF serÃ¡ implementada na prÃ³xima versÃ£o.")

    def salvar_template(self):
        """Salva o template do relatÃ³rio personalizado"""
        QMessageBox.information(self, "Funcionalidade em desenvolvimento",
                                "O salvamento de templates serÃ¡ implementado na prÃ³xima versÃ£o.")


# ============================================
# DIÃLOGO DE VISUALIZADOR DE RELATÃ“RIO
# ============================================

class VisualizadorRelatorioDialog(QDialog):
    """DiÃ¡logo para visualizar relatÃ³rios na tela"""

    def __init__(self, parent=None, tipo="", dados=None, campos=None):
        super().__init__(parent)
        self.tipo = tipo
        self.dados = dados or []
        self.campos = campos or []

        self.setWindowTitle(f"RelatÃ³rio - {tipo.capitalize()}")
        self.setFixedSize(1000, 700)
        self.setStyleSheet(GLOBAL_STYLESHEET)

        self.init_ui()

    def init_ui(self):
        """Inicializa a interface do diÃ¡logo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # TÃ­tulo
        lbl_titulo = QLabel(f"RELATÃ“RIO - {self.tipo.upper()}")
        lbl_titulo.setObjectName("title")

        # InformaÃ§Ãµes
        lbl_info = QLabel(f"Total de registros: {len(self.dados)} | Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        lbl_info.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #7f8c8d;
                font-weight: 600;
                padding: 10px;
                background-color: #f8f9fa;
                border-radius: 6px;
                border: 1px solid #dce1e6;
            }
        """)

        # Tabela de dados
        self.tabela_relatorio = QTableWidget()

        # Configurar tabela
        self.tabela_relatorio.setAlternatingRowColors(True)
        self.tabela_relatorio.setEditTriggers(QTableWidget.NoEditTriggers)

        # Popular tabela
        self.popular_tabela()

        # BotÃµes
        botoes_layout = QHBoxLayout()

        btn_exportar = AnimacaoBotao("EXPORTAR", cor_normal="#27ae60", cor_hover="#219653", cor_press="#1e874b")
        btn_exportar.setMinimumHeight(45)
        btn_exportar.clicked.connect(self.exportar_dados)

        btn_imprimir = AnimacaoBotao("IMPRIMIR", cor_normal="#3498db", cor_hover="#2980b9", cor_press="#1c6ea4")
        btn_imprimir.setMinimumHeight(45)
        btn_imprimir.clicked.connect(self.imprimir_relatorio)

        btn_fechar = QPushButton("FECHAR")
        btn_fechar.setObjectName("danger")
        btn_fechar.setMinimumHeight(45)
        btn_fechar.clicked.connect(self.close)

        botoes_layout.addWidget(btn_exportar)
        botoes_layout.addWidget(btn_imprimir)
        botoes_layout.addStretch()
        botoes_layout.addWidget(btn_fechar)

        # Adicionar tudo ao layout
        layout.addWidget(lbl_titulo)
        layout.addWidget(lbl_info)
        layout.addWidget(self.tabela_relatorio)
        layout.addLayout(botoes_layout)

    def popular_tabela(self):
        """Popula a tabela com os dados do relatÃ³rio"""
        if not self.dados:
            self.tabela_relatorio.setRowCount(0)
            self.tabela_relatorio.setColumnCount(1)
            self.tabela_relatorio.setHorizontalHeaderLabels(["Mensagem"])

            item = QTableWidgetItem("Nenhum dado disponÃ­vel para exibiÃ§Ã£o.")
            item.setTextAlignment(Qt.AlignCenter)
            self.tabela_relatorio.setItem(0, 0, item)
            return

        # Configurar colunas
        num_colunas = len(self.dados[0]) if self.dados else 0
        num_colunas = min(num_colunas, len(self.campos))

        self.tabela_relatorio.setColumnCount(num_colunas)
        self.tabela_relatorio.setHorizontalHeaderLabels(self.campos[:num_colunas])

        # Configurar linhas
        self.tabela_relatorio.setRowCount(len(self.dados))

        # Popular dados
        for row, linha_dados in enumerate(self.dados):
            for col in range(num_colunas):
                valor = linha_dados[col] if col < len(linha_dados) else ""

                # Formatar valores especÃ­ficos
                if isinstance(valor, float):
                    valor_texto = f"{valor:.2f}"
                elif isinstance(valor, datetime):
                    valor_texto = valor.strftime('%d/%m/%Y %H:%M')
                elif valor is None:
                    valor_texto = ""
                else:
                    valor_texto = str(valor)

                item = QTableWidgetItem(valor_texto)

                # Colorir valores especÃ­ficos baseado no tipo de relatÃ³rio
                if self.tipo == "notas" and col == num_colunas - 2:  # Coluna de mÃ©dia
                    try:
                        media = float(valor) if valor else 0
                        if media < 5.0:
                            item.setForeground(QColor('#e74c3c'))
                            item.setFont(QFont('', weight=QFont.Bold))
                        elif media < 7.0:
                            item.setForeground(QColor('#f39c12'))
                        else:
                            item.setForeground(QColor('#27ae60'))
                    except:
                        pass

                elif self.tipo == "notas" and col == num_colunas - 1:  # Coluna de situaÃ§Ã£o
                    if valor == "Aprovado":
                        item.setForeground(QColor('#27ae60'))
                        item.setFont(QFont('', weight=QFont.Bold))
                    elif valor == "Reprovado":
                        item.setForeground(QColor('#e74c3c'))
                    elif valor == "RecuperaÃ§Ã£o":
                        item.setForeground(QColor('#f39c12'))

                elif self.tipo == "frequencia" and "presente" in self.campos[col].lower():
                    if valor == 1 or str(valor).lower() == "true":
                        item.setText("Presente")
                        item.setForeground(QColor('#27ae60'))
                        item.setFont(QFont('', weight=QFont.Bold))
                    else:
                        item.setText("Falta")
                        item.setForeground(QColor('#e74c3c'))

                self.tabela_relatorio.setItem(row, col, item)

        # Ajustar largura das colunas
        self.tabela_relatorio.resizeColumnsToContents()

        # Adicionar numeraÃ§Ã£o das linhas
        self.tabela_relatorio.setRowCount(len(self.dados))
        for row in range(len(self.dados)):
            self.tabela_relatorio.setVerticalHeaderItem(row, QTableWidgetItem(str(row + 1)))

    def exportar_dados(self):
        """Exporta os dados exibidos"""
        QMessageBox.information(self, "Funcionalidade em desenvolvimento",
                                "A exportaÃ§Ã£o direta serÃ¡ implementada na prÃ³xima versÃ£o.")

    def imprimir_relatorio(self):
        """Imprime o relatÃ³rio"""
        QMessageBox.information(self, "Funcionalidade em desenvolvimento",
                                "A impressÃ£o serÃ¡ implementada na prÃ³xima versÃ£o.")


# ============================================
# DIÃLOGO DE EXPORTAÃ‡ÃƒO DE DADOS
# ============================================

class ExportarDadosDialog(QDialog):
    """DiÃ¡logo para exportaÃ§Ã£o de dados em diferentes formatos"""

    def __init__(self, parent=None, formato="excel"):
        super().__init__(parent)
        self.formato = formato
        self.db = DatabaseManager()
        self.exportador = ExportadorDados(self.db)

        self.setWindowTitle(f"Exportar Dados - {formato.upper()}")
        self.setFixedSize(600, 500)
        self.setStyleSheet(GLOBAL_STYLESHEET)

        self.init_ui()

    def init_ui(self):
        """Inicializa a interface do diÃ¡logo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # TÃ­tulo
        lbl_titulo = QLabel(f"EXPORTAR DADOS - {self.formato.upper()}")
        lbl_titulo.setObjectName("title")

        # SeleÃ§Ã£o de dados
        group_selecao = QGroupBox("SELECIONAR DADOS PARA EXPORTAR")
        group_selecao.setStyleSheet("""
            QGroupBox {
                font-weight: 600;
                border: 2px solid #dce1e6;
                border-radius: 8px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 15px;
                padding: 0 10px;
                background-color: #f5f7fa;
            }
        """)

        layout_selecao = QVBoxLayout(group_selecao)

        self.radio_alunos_exp = QRadioButton("Dados de Alunos")
        self.radio_alunos_exp.setChecked(True)

        self.radio_professores = QRadioButton("Dados de Professores")

        self.radio_notas_exp = QRadioButton("Dados de Notas")

        self.radio_frequencia_exp = QRadioButton("Dados de FrequÃªncia")

        self.radio_turmas = QRadioButton("Dados de Turmas")

        self.radio_disciplinas = QRadioButton("Dados de Disciplinas")

        self.radio_tudo = QRadioButton("Todos os dados (Backup completo)")

        layout_selecao.addWidget(self.radio_alunos_exp)
        layout_selecao.addWidget(self.radio_professores)
        layout_selecao.addWidget(self.radio_notas_exp)
        layout_selecao.addWidget(self.radio_frequencia_exp)
        layout_selecao.addWidget(self.radio_turmas)
        layout_selecao.addWidget(self.radio_disciplinas)
        layout_selecao.addWidget(self.radio_tudo)

        # OpÃ§Ãµes de exportaÃ§Ã£o
        group_opcoes = QGroupBox("OPÃ‡Ã•ES DE EXPORTAÃ‡ÃƒO")
        group_opcoes.setStyleSheet(group_selecao.styleSheet())

        layout_opcoes = QVBoxLayout(group_opcoes)

        if self.formato == "excel":
            self.check_formatar = QCheckBox("Aplicar formataÃ§Ã£o Ã s cÃ©lulas")
            self.check_formatar.setChecked(True)

            self.check_filtros = QCheckBox("Incluir filtros nas colunas")
            self.check_filtros.setChecked(True)

            self.check_auto_ajuste = QCheckBox("Ajustar automaticamente largura das colunas")
            self.check_auto_ajuste.setChecked(True)

            layout_opcoes.addWidget(self.check_formatar)
            layout_opcoes.addWidget(self.check_filtros)
            layout_opcoes.addWidget(self.check_auto_ajuste)

        elif self.formato == "csv":
            lbl_delimitador = QLabel("Delimitador:")
            self.combo_delimitador = QComboBox()
            self.combo_delimitador.addItems(["; (ponto e vÃ­rgula)", ", (vÃ­rgula)", "| (pipe)", "\\t (tab)"])

            self.check_cabecalho = QCheckBox("Incluir linha de cabeÃ§alho")
            self.check_cabecalho.setChecked(True)

            self.check_utf8 = QCheckBox("Usar codificaÃ§Ã£o UTF-8")
            self.check_utf8.setChecked(True)

            layout_opcoes.addWidget(lbl_delimitador)
            layout_opcoes.addWidget(self.combo_delimitador)
            layout_opcoes.addWidget(self.check_cabecalho)
            layout_opcoes.addWidget(self.check_utf8)

        elif self.formato == "pdf":
            self.check_cabecalho_pdf = QCheckBox("Incluir cabeÃ§alho com data e hora")
            self.check_cabecalho_pdf.setChecked(True)

            self.check_rodape = QCheckBox("Incluir rodapÃ© com nÃºmero de pÃ¡ginas")
            self.check_rodape.setChecked(True)

            self.check_colorir = QCheckBox("Manter cores da tabela")
            self.check_colorir.setChecked(True)

            layout_opcoes.addWidget(self.check_cabecalho_pdf)
            layout_opcoes.addWidget(self.check_rodape)
            layout_opcoes.addWidget(self.check_colorir)

        # BotÃµes
        botoes_layout = QHBoxLayout()

        btn_exportar = AnimacaoBotao("EXPORTAR", cor_normal="#27ae60", cor_hover="#219653", cor_press="#1e874b")
        btn_exportar.setMinimumHeight(45)
        btn_exportar.clicked.connect(self.executar_exportacao)

        btn_fechar = QPushButton("CANCELAR")
        btn_fechar.setObjectName("danger")
        btn_fechar.setMinimumHeight(45)
        btn_fechar.clicked.connect(self.close)

        botoes_layout.addWidget(btn_exportar)
        botoes_layout.addStretch()
        botoes_layout.addWidget(btn_fechar)

        # Adicionar tudo ao layout
        layout.addWidget(lbl_titulo)
        layout.addWidget(group_selecao)
        layout.addWidget(group_opcoes)
        layout.addStretch()
        layout.addLayout(botoes_layout)

    def executar_exportacao(self):
        """Executa a exportaÃ§Ã£o dos dados"""
        # Determinar qual conjunto de dados exportar
        dataset = ""
        query = ""
        nome_arquivo = ""

        if self.radio_alunos_exp.isChecked():
            dataset = "alunos"
            query = "SELECT * FROM alunos ORDER BY nome"
            nome_arquivo = "alunos"

        elif self.radio_professores.isChecked():
            dataset = "professores"
            query = "SELECT * FROM professores ORDER BY nome"
            nome_arquivo = "professores"

        elif self.radio_notas_exp.isChecked():
            dataset = "notas"
            query = """
                SELECT a.nome as aluno, d.nome as disciplina, n.bimestre,
                       n.nota1, n.nota2, n.nota3, n.nota4, n.media, n.situacao,
                       n.faltas, n.observacoes, n.data_lancamento
                FROM notas n
                JOIN alunos a ON n.aluno_id = a.id
                JOIN disciplinas d ON n.disciplina_id = d.id
                ORDER BY a.nome, d.nome, n.bimestre
            """
            nome_arquivo = "notas"

        elif self.radio_frequencia_exp.isChecked():
            dataset = "frequencia"
            query = """
                SELECT a.nome as aluno, f.data, d.nome as disciplina,
                       f.presente, f.justificativa, f.observacoes
                FROM frequencia f
                JOIN alunos a ON f.aluno_id = a.id
                LEFT JOIN disciplinas d ON f.disciplina_id = d.id
                ORDER BY f.data, a.nome
            """
            nome_arquivo = "frequencia"

        elif self.radio_turmas.isChecked():
            dataset = "turmas"
            query = "SELECT * FROM turmas ORDER BY serie, nome"
            nome_arquivo = "turmas"

        elif self.radio_disciplinas.isChecked():
            dataset = "disciplinas"
            query = "SELECT * FROM disciplinas ORDER BY nome"
            nome_arquivo = "disciplinas"

        elif self.radio_tudo.isChecked():
            dataset = "completo"
            nome_arquivo = "backup_completo"

        if not dataset:
            QMessageBox.warning(self, "SeleÃ§Ã£o necessÃ¡ria",
                                "Por favor, selecione um conjunto de dados para exportar.")
            return

        try:
            if dataset == "completo":
                # Exportar todos os dados
                self.exportar_todos_dados()
            else:
                # Exportar dataset especÃ­fico
                if self.formato == "excel":
                    sucesso, caminho = self.exportador.exportar_para_excel(query, nome_arquivo)
                elif self.formato == "csv":
                    delimitador = self.obter_delimitador()
                    sucesso, caminho = self.exportador.exportar_para_csv(query, nome_arquivo, delimitador)
                elif self.formato == "pdf":
                    # Obter dados primeiro
                    dados = self.db.execute_query(query, fetch=True)
                    cabecalhos = self.obter_cabecalhos(query)
                    sucesso, caminho = self.exportador.exportar_para_pdf(
                        f"RelatÃ³rio de {dataset}",
                        dados,
                        cabecalhos,
                        nome_arquivo
                    )
                else:
                    QMessageBox.warning(self, "Formato nÃ£o suportado",
                                        f"Formato {self.formato} nÃ£o Ã© suportado.")
                    return

                if sucesso:
                    QMessageBox.information(self, "ExportaÃ§Ã£o concluÃ­da",
                                            f"Dados exportados com sucesso para:\n{caminho}")
                    self.accept()
                else:
                    QMessageBox.warning(self, "Erro na exportaÃ§Ã£o", caminho)

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao exportar dados:\n{str(e)}")

    def obter_delimitador(self):
        """ObtÃ©m o delimitador selecionado para CSV"""
        texto = self.combo_delimitador.currentText()

        if "ponto e vÃ­rgula" in texto:
            return ";"
        elif "vÃ­rgula" in texto:
            return ","
        elif "pipe" in texto:
            return "|"
        elif "tab" in texto:
            return "\t"
        else:
            return ";"

    def obter_cabecalhos(self, query):
        """ObtÃ©m os cabeÃ§alhos das colunas a partir da query"""
        try:
            self.db.connect()
            self.db.cursor.execute(query)
            descricao = self.db.cursor.description

            if descricao:
                return [col[0] for col in descricao]

            return []
        except:
            return []
        finally:
            self.db.disconnect()

    def exportar_todos_dados(self):
        """Exporta todos os dados do sistema"""
        try:
            # Criar diretÃ³rio de exportaÃ§Ã£o
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_dir = os.path.join(os.path.expanduser("~"), f"BackupEscola_{timestamp}")
            os.makedirs(export_dir, exist_ok=True)

            # Lista de tabelas para exportar
            tabelas = [
                ("alunos", "SELECT * FROM alunos ORDER BY nome"),
                ("professores", "SELECT * FROM professores ORDER BY nome"),
                ("disciplinas", "SELECT * FROM disciplinas ORDER BY nome"),
                ("turmas", "SELECT * FROM turmas ORDER BY serie, nome"),
                ("notas", """
                    SELECT a.nome as aluno, d.nome as disciplina, n.*
                    FROM notas n
                    JOIN alunos a ON n.aluno_id = a.id
                    JOIN disciplinas d ON n.disciplina_id = d.id
                    ORDER BY a.nome, d.nome, n.bimestre
                """),
                ("frequencia", """
                    SELECT a.nome as aluno, d.nome as disciplina, f.*
                    FROM frequencia f
                    JOIN alunos a ON f.aluno_id = a.id
                    LEFT JOIN disciplinas d ON f.disciplina_id = d.id
                    ORDER BY f.data, a.nome
                """),
                ("horarios", """
                    SELECT t.nome as turma, d.nome as disciplina, p.nome as professor, h.*
                    FROM horarios h
                    JOIN turmas t ON h.turma_id = t.id
                    JOIN disciplinas d ON h.disciplina_id = d.id
                    JOIN professores p ON h.professor_id = p.id
                    ORDER BY h.dia_semana, h.hora_inicio
                """),
                ("configuracoes", "SELECT * FROM configuracoes ORDER BY categoria, chave"),
                ("administradores", "SELECT id, usuario, nome, email, data_cadastro FROM administradores")
            ]

            # Exportar cada tabela
            for nome_tabela, query in tabelas:
                if self.formato == "excel":
                    sucesso, caminho = self.exportador.exportar_para_excel(
                        query,
                        f"{nome_tabela}_{timestamp}",
                        cabecalhos=self.obter_cabecalhos(query)
                    )
                elif self.formato == "csv":
                    sucesso, caminho = self.exportador.exportar_para_csv(
                        query,
                        f"{nome_tabela}_{timestamp}",
                        delimitador=";"
                    )

            # Criar arquivo README
            readme_path = os.path.join(export_dir, "README.txt")
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(f"BACKUP COMPLETO DO SISTEMA ESCOLAR\n")
                f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"Total de tabelas exportadas: {len(tabelas)}\n")
                f.write(f"Formato: {self.formato.upper()}\n")
                f.write("\nTabelas incluÃ­das:\n")
                for nome_tabela, _ in tabelas:
                    f.write(f"- {nome_tabela}\n")

            QMessageBox.information(self, "Backup completo",
                                    f"Backup completo realizado com sucesso!\n\n"
                                    f"DiretÃ³rio: {export_dir}\n"
                                    f"Total de tabelas: {len(tabelas)}\n\n"
                                    "Todos os dados foram exportados com sucesso.")

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Erro no backup", f"Falha ao realizar backup completo:\n{str(e)}")

    def criar_menu_contextual_tabela(self, posicao):
        """Cria menu contextual para tabelas"""
        try:
            # Identificar qual tabela estÃ¡ solicitando o menu
            tabela = self.sender()
            if not isinstance(tabela, QTableWidget):
                return

            menu = QMenu()

            # AÃ§Ãµes comuns
            acao_copiar = QAction("ðŸ“‹ Copiar", self)
            acao_copiar.triggered.connect(lambda: self.copiar_celula_tabela(tabela))

            acao_colar = QAction("ðŸ“ Colar", self)
            acao_colar.triggered.connect(lambda: self.colar_celula_tabela(tabela))

            acao_exportar = QAction("ðŸ“¤ Exportar Linha", self)
            acao_exportar.triggered.connect(lambda: self.exportar_linha_tabela(tabela))

            acao_deletar = QAction("ðŸ—‘ï¸ Deletar Linha", self)
            acao_deletar.triggered.connect(lambda: self.deletar_linha_tabela(tabela))

            acao_formatar = QAction("ðŸŽ¨ Formatar CÃ©lulas", self)
            acao_formatar.triggered.connect(lambda: self.formatar_celulas_tabela(tabela))

            menu.addAction(acao_copiar)
            menu.addAction(acao_colar)
            menu.addSeparator()
            menu.addAction(acao_exportar)
            menu.addAction(acao_deletar)
            menu.addSeparator()
            menu.addAction(acao_formatar)

            # Mostrar menu na posiÃ§Ã£o do clique
            menu.exec_(tabela.viewport().mapToGlobal(posicao))

        except Exception as e:
            print(f"Erro ao criar menu contextual: {e}")

    def copiar_celula_tabela(self, tabela):
        """Copia conteÃºdo da cÃ©lula selecionada"""
        try:
            itens_selecionados = tabela.selectedItems()
            if itens_selecionados:
                texto = itens_selecionados[0].text()
                clipboard = QApplication.clipboard()
                clipboard.setText(texto)
        except Exception as e:
            print(f"Erro ao copiar cÃ©lula: {e}")

    def colar_celula_tabela(self, tabela):
        """Cola conteÃºdo na cÃ©lula selecionada"""
        try:
            itens_selecionados = tabela.selectedItems()
            if itens_selecionados:
                clipboard = QApplication.clipboard()
                texto = clipboard.text()
                itens_selecionados[0].setText(texto)
        except Exception as e:
            print(f"Erro ao colar cÃ©lula: {e}")

    def exportar_linha_tabela(self, tabela):
        """Exporta linha selecionada para CSV"""
        try:
            linhas_selecionadas = set()
            for item in tabela.selectedItems():
                linhas_selecionadas.add(item.row())

            if not linhas_selecionadas:
                QMessageBox.warning(self, "Aviso", "Selecione pelo menos uma linha!")
                return

            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Exportar Linhas",
                f"exportacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "Arquivos CSV (*.csv)"
            )

            if file_path:
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)

                    # Escrever cabeÃ§alho
                    headers = []
                    for col in range(tabela.columnCount()):
                        headers.append(tabela.horizontalHeaderItem(col).text())
                    writer.writerow(headers)

                    # Escrever linhas selecionadas
                    for linha in sorted(linhas_selecionadas):
                        row_data = []
                        for col in range(tabela.columnCount()):
                            item = tabela.item(linha, col)
                            row_data.append(item.text() if item else "")
                        writer.writerow(row_data)

                QMessageBox.information(self, "Sucesso", f"Linhas exportadas para:\n{file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao exportar linhas: {str(e)}")

    def deletar_linha_tabela(self, tabela):
        """Deleta linha selecionada da tabela"""
        try:
            linhas_selecionadas = set()
            for item in tabela.selectedItems():
                linhas_selecionadas.add(item.row())

            if not linhas_selecionadas:
                QMessageBox.warning(self, "Aviso", "Selecione pelo menos uma linha!")
                return

            resposta = QMessageBox.question(
                self,
                "Confirmar ExclusÃ£o",
                f"Deseja excluir {len(linhas_selecionadas)} linha(s) selecionada(s)?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if resposta == QMessageBox.Yes:
                # Deletar em ordem decrescente para manter Ã­ndices corretos
                for linha in sorted(linhas_selecionadas, reverse=True):
                    tabela.removeRow(linha)

                QMessageBox.information(self, "Sucesso",
                                        f"{len(linhas_selecionadas)} linha(s) excluÃ­da(s)!")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao deletar linhas: {str(e)}")

    def formatar_celulas_tabela(self, tabela):
        """Abre diÃ¡logo para formataÃ§Ã£o de cÃ©lulas"""
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("FormataÃ§Ã£o de CÃ©lulas")
            dialog.setFixedSize(400, 300)

            layout = QVBoxLayout()

            # OpÃ§Ãµes de formataÃ§Ã£o
            grupo_fonte = QGroupBox("ConfiguraÃ§Ãµes de Fonte")
            fonte_layout = QFormLayout()

            cb_negrito = QCheckBox("Negrito")
            cb_italico = QCheckBox("ItÃ¡lico")
            cb_sublinhado = QCheckBox("Sublinhado")

            combo_tamanho = QComboBox()
            combo_tamanho.addItems(["8", "9", "10", "11", "12", "14", "16", "18", "20"])
            combo_tamanho.setCurrentText("11")

            combo_cor = QComboBox()
            combo_cor.addItems(["Preto", "Vermelho", "Verde", "Azul", "Laranja", "Roxo"])
            combo_cor.setCurrentText("Preto")

            fonte_layout.addRow("Negrito:", cb_negrito)
            fonte_layout.addRow("ItÃ¡lico:", cb_italico)
            fonte_layout.addRow("Sublinhado:", cb_sublinhado)
            fonte_layout.addRow("Tamanho:", combo_tamanho)
            fonte_layout.addRow("Cor:", combo_cor)

            grupo_fonte.setLayout(fonte_layout)

            # OpÃ§Ãµes de alinhamento
            grupo_alinhamento = QGroupBox("Alinhamento")
            alinhamento_layout = QHBoxLayout()

            rb_esquerda = QRadioButton("Esquerda")
            rb_centro = QRadioButton("Centro")
            rb_direita = QRadioButton("Direita")
            rb_centro.setChecked(True)

            alinhamento_layout.addWidget(rb_esquerda)
            alinhamento_layout.addWidget(rb_centro)
            alinhamento_layout.addWidget(rb_direita)
            grupo_alinhamento.setLayout(alinhamento_layout)

            # BotÃµes
            button_box = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel
            )
            button_box.accepted.connect(dialog.accept)
            button_box.rejected.connect(dialog.reject)

            layout.addWidget(grupo_fonte)
            layout.addWidget(grupo_alinhamento)
            layout.addWidget(button_box)

            dialog.setLayout(layout)

            if dialog.exec_() == QDialog.Acepted:
                # Aplicar formataÃ§Ã£o Ã s cÃ©lulas selecionadas
                for item in tabela.selectedItems():
                    font = item.font()
                    font.setBold(cb_negrito.isChecked())
                    font.setItalic(cb_italico.isChecked())
                    font.setUnderline(cb_sublinhado.isChecked())
                    font.setPointSize(int(combo_tamanho.currentText()))
                    item.setFont(font)

                    # Aplicar cor
                    cores = {
                        "Preto": QColor(0, 0, 0),
                        "Vermelho": QColor(255, 0, 0),
                        "Verde": QColor(0, 128, 0),
                        "Azul": QColor(0, 0, 255),
                        "Laranja": QColor(255, 165, 0),
                        "Roxo": QColor(128, 0, 128)
                    }
                    item.setForeground(cores[combo_cor.currentText()])

                    # Aplicar alinhamento
                    alinhamentos = {
                        "Esquerda": Qt.AlignLeft,
                        "Centro": Qt.AlignCenter,
                        "Direita": Qt.AlignRight
                    }
                    item.setTextAlignment(alinhamentos[
                                              rb_esquerda.isChecked() and "Esquerda" or
                                              rb_centro.isChecked() and "Centro" or
                                              "Direita"
                                              ])

                QMessageBox.information(self, "Sucesso", "FormataÃ§Ã£o aplicada Ã s cÃ©lulas selecionadas!")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao formatar cÃ©lulas: {str(e)}")

    def configurar_atalhos_teclado(self):
        """Configura atalhos de teclado globais"""
        # Atalhos jÃ¡ configurados no __init__
        # Esta funÃ§Ã£o pode ser expandida para personalizaÃ§Ã£o de atalhos
        pass

    def mostrar_ajuda_contexto(self):
        """Mostra ajuda contextual baseada no widget atual"""
        try:
            widget_focado = QApplication.focusWidget()

            if isinstance(widget_focado, QLineEdit):
                mensagem = "Campo de texto. Digite a informaÃ§Ã£o solicitada."
            elif isinstance(widget_focado, QComboBox):
                mensagem = "Menu suspenso. Selecione uma opÃ§Ã£o da lista."
            elif isinstance(widget_focado, QTableWidget):
                mensagem = "Tabela de dados. Clique com botÃ£o direito para mais opÃ§Ãµes."
            elif isinstance(widget_focado, QPushButton):
                mensagem = "BotÃ£o. Clique para executar a aÃ§Ã£o."
            elif isinstance(widget_focado, QDateEdit):
                mensagem = "Seletor de data. Use as setas ou clique para selecionar data."
            else:
                mensagem = "Widget ativo. Consulte a documentaÃ§Ã£o para mais informaÃ§Ãµes."

            QMessageBox.information(self, "Ajuda Contexto", mensagem)

        except Exception as e:
            print(f"Erro ao mostrar ajuda: {e}")

    def alternar_tema_escuro(self):
        """Alterna entre tema claro e escuro"""
        try:
            if not hasattr(self, 'tema_escuro'):
                self.tema_escuro = False

            self.tema_escuro = not self.tema_escuro

            if self.tema_escuro:
                # Tema escuro
                estilo_escuro = """
                    QMainWindow {
                        background-color: #2c3e50;
                    }
                    QWidget {
                        background-color: #34495e;
                        color: #ecf0f1;
                    }
                    QPushButton {
                        background-color: #3498db;
                        color: white;
                        border-radius: 6px;
                        padding: 10px;
                    }
                    QPushButton:hover {
                        background-color: #2980b9;
                    }
                    QLineEdit, QTextEdit, QComboBox {
                        background-color: #4a6572;
                        color: #ecf0f1;
                        border: 1px solid #5d6d7e;
                        border-radius: 4px;
                        padding: 6px;
                    }
                    QTableWidget {
                        background-color: #4a6572;
                        color: #ecf0f1;
                        gridline-color: #5d6d7e;
                    }
                    QHeaderView::section {
                        background-color: #2c3e50;
                        color: #ecf0f1;
                        padding: 8px;
                    }
                """
                self.setStyleSheet(estilo_escuro)
                QMessageBox.information(self, "Tema Alterado", "Tema escuro ativado!")
            else:
                # Restaurar tema original
                self.setStyleSheet(GLOBAL_STYLESHEET)
                QMessageBox.information(self, "Tema Alterado", "Tema claro ativado!")

        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao alternar tema: {str(e)}")

    def verificar_integridade_dados(self):
        """Verifica integridade dos dados no banco"""
        try:
            if not self.db.conn:
                QMessageBox.warning(self, "Erro", "Banco de dados nÃ£o conectado!")
                return

            cursor = self.db.conn.cursor()
            problemas = []

            # Verificar alunos sem turma
            cursor.execute("""
                SELECT COUNT(*) 
                FROM alunos 
                WHERE turma_id IS NULL OR turma_id = ''
            """)
            alunos_sem_turma = cursor.fetchone()[0]
            if alunos_sem_turma > 0:
                problemas.append(f"{alunos_sem_turma} aluno(s) sem turma atribuÃ­da")

            # Verificar notas invÃ¡lidas
            cursor.execute("""
                SELECT COUNT(*) 
                FROM notas 
                WHERE nota < 0 OR nota > 10
            """)
            notas_invalidas = cursor.fetchone()[0]
            if notas_invalidas > 0:
                problemas.append(f"{notas_invalidas} nota(s) fora do intervalo 0-10")

            # Verificar datas inconsistentes
            cursor.execute("""
                SELECT COUNT(*) 
                FROM alunos 
                WHERE data_nascimento > date('now') 
                OR data_matricula > date('now')
            """)
            datas_inconsistentes = cursor.fetchone()[0]
            if datas_inconsistentes > 0:
                problemas.append(f"{datas_inconsistentes} data(s) no futuro")

            # Verificar turmas sem alunos
            cursor.execute("""
                SELECT t.nome_turma 
                FROM turmas t 
                LEFT JOIN alunos a ON t.id = a.turma_id 
                WHERE a.id IS NULL
            """)
            turmas_sem_alunos = cursor.fetchall()
            if turmas_sem_alunos:
                problemas.append(f"{len(turmas_sem_alunos)} turma(s) sem alunos: " +
                                 ", ".join([t[0] for t in turmas_sem_alunos]))

            # Mostrar resultados
            if problemas:
                mensagem = "âš ï¸ PROBLEMAS ENCONTRADOS:\n\n" + "\nâ€¢ ".join(problemas)
                QMessageBox.warning(self, "VerificaÃ§Ã£o de Integridade", mensagem)
            else:
                QMessageBox.information(self, "VerificaÃ§Ã£o de Integridade",
                                        "âœ… Todos os dados estÃ£o Ã­ntegros!")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro na verificaÃ§Ã£o: {str(e)}")

    def otimizar_banco_dados(self):
        """Otimiza o banco de dados SQLite"""
        try:
            if not self.db.conn:
                QMessageBox.warning(self, "Erro", "Banco de dados nÃ£o conectado!")
                return

            resposta = QMessageBox.question(
                self,
                "Otimizar Banco de Dados",
                "Esta operaÃ§Ã£o otimizarÃ¡ o banco de dados para melhor desempenho.\n"
                "Pode demorar alguns segundos. Continuar?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if resposta == QMessageBox.Yes:
                cursor = self.db.conn.cursor()

                # Executar VACUUM para otimizar espaÃ§o
                cursor.execute("VACUUM")

                # Executar ANALYZE para otimizar consultas
                cursor.execute("ANALYZE")

                # Reconstruir Ã­ndices
                cursor.execute("REINDEX")

                self.db.conn.commit()

                QMessageBox.information(self, "Sucesso",
                                        "Banco de dados otimizado com sucesso!\n"
                                        "Desempenho melhorado.")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao otimizar banco: {str(e)}")

    def criar_relatorio_personalizado(self):
        """Cria relatÃ³rio personalizado com filtros"""
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("RelatÃ³rio Personalizado")
            dialog.setMinimumSize(600, 500)

            layout = QVBoxLayout()

            # SeÃ§Ã£o de filtros
            grupo_filtros = QGroupBox("ðŸ” Filtros do RelatÃ³rio")
            grupo_filtros.setStyleSheet("""
                QGroupBox {
                    font-weight: bold;
                    font-size: 14px;
                    padding-top: 10px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                }
            """)

            filtros_layout = QFormLayout()

            # Filtro por data
            lbl_data_inicio = QLabel("Data InÃ­cio:")
            date_inicio = QDateEdit()
            date_inicio.setDate(QDate.currentDate().addMonths(-1))
            date_inicio.setCalendarPopup(True)

            lbl_data_fim = QLabel("Data Fim:")
            date_fim = QDateEdit()
            date_fim.setDate(QDate.currentDate())
            date_fim.setCalendarPopup(True)

            # Filtro por turma
            lbl_turma = QLabel("Turma:")
            combo_turma = QComboBox()
            combo_turma.addItem("Todas as Turmas")
            if self.db.conn:
                cursor = self.db.conn.cursor()
                cursor.execute("SELECT nome_turma FROM turmas ORDER BY nome_turma")
                for turma in cursor.fetchall():
                    combo_turma.addItem(turma[0])

            # Filtro por tipo de relatÃ³rio
            lbl_tipo = QLabel("Tipo de RelatÃ³rio:")
            combo_tipo = QComboBox()
            combo_tipo.addItems([
                "Notas e Desempenho",
                "FrequÃªncia e PresenÃ§a",
                "InformaÃ§Ãµes de Alunos",
                "InformaÃ§Ãµes de Professores",
                "Resumo Financeiro"
            ])

            # Formato de saÃ­da
            lbl_formato = QLabel("Formato de SaÃ­da:")
            combo_formato = QComboBox()
            combo_formato.addItems(["Excel (.xlsx)", "PDF (.pdf)", "CSV (.csv)", "HTML (.html)"])

            filtros_layout.addRow(lbl_data_inicio, date_inicio)
            filtros_layout.addRow(lbl_data_fim, date_fim)
            filtros_layout.addRow(lbl_turma, combo_turma)
            filtros_layout.addRow(lbl_tipo, combo_tipo)
            filtros_layout.addRow(lbl_formato, combo_formato)

            grupo_filtros.setLayout(filtros_layout)

            # OpÃ§Ãµes avanÃ§adas
            grupo_opcoes = QGroupBox("âš™ï¸ OpÃ§Ãµes AvanÃ§adas")
            opcoes_layout = QVBoxLayout()

            cb_incluir_cabecalho = QCheckBox("Incluir cabeÃ§alho")
            cb_incluir_cabecalho.setChecked(True)

            cb_incluir_graficos = QCheckBox("Incluir grÃ¡ficos (se disponÃ­vel)")
            cb_incluir_graficos.setChecked(True)

            cb_incluir_sumario = QCheckBox("Incluir sumÃ¡rio executivo")
            cb_incluir_sumario.setChecked(True)

            opcoes_layout.addWidget(cb_incluir_cabecalho)
            opcoes_layout.addWidget(cb_incluir_graficos)
            opcoes_layout.addWidget(cb_incluir_sumario)
            grupo_opcoes.setLayout(opcoes_layout)

            # BotÃµes
            button_box = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel
            )
            button_box.accepted.connect(dialog.accept)
            button_box.rejected.connect(dialog.reject)

            layout.addWidget(grupo_filtros)
            layout.addWidget(grupo_opcoes)
            layout.addWidget(button_box)

            dialog.setLayout(layout)

            if dialog.exec_() == QDialog.Accepted:
                # Coletar parÃ¢metros
                parametros = {
                    'data_inicio': date_inicio.date().toString("yyyy-MM-dd"),
                    'data_fim': date_fim.date().toString("yyyy-MM-dd"),
                    'turma': combo_turma.currentText(),
                    'tipo': combo_tipo.currentText(),
                    'formato': combo_formato.currentText(),
                    'incluir_cabecalho': cb_incluir_cabecalho.isChecked(),
                    'incluir_graficos': cb_incluir_graficos.isChecked(),
                    'incluir_sumario': cb_incluir_sumario.isChecked()
                }

                # Gerar relatÃ³rio
                self.gerar_relatorio_com_parametros(parametros)

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao criar relatÃ³rio: {str(e)}")

    def gerar_relatorio_com_parametros(self, parametros):
        """Gera relatÃ³rio baseado nos parÃ¢metros fornecidos"""
        try:
            QMessageBox.information(
                self,
                "RelatÃ³rio em Processamento",
                f"Gerando relatÃ³rio '{parametros['tipo']}'...\n"
                f"PerÃ­odo: {parametros['data_inicio']} a {parametros['data_fim']}\n"
                f"Turma: {parametros['turma']}\n"
                f"Formato: {parametros['formato']}\n\n"
                "Esta funcionalidade serÃ¡ completamente implementada na versÃ£o web Django."
            )

            # Aqui seria a implementaÃ§Ã£o real da geraÃ§Ã£o de relatÃ³rio
            # Por enquanto, apenas demonstraÃ§Ã£o

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao gerar relatÃ³rio: {str(e)}")

    def configurar_notificacoes(self):
        """Configura sistema de notificaÃ§Ãµes"""
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("ðŸ”” ConfiguraÃ§Ãµes de NotificaÃ§Ãµes")
            dialog.setFixedSize(500, 400)

            layout = QVBoxLayout()

            # TÃ­tulo
            titulo = QLabel("Configurar NotificaÃ§Ãµes do Sistema")
            titulo.setStyleSheet("""
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
                border-bottom: 2px solid #3498db;
                margin-bottom: 20px;
            """)
            titulo.setAlignment(Qt.AlignCenter)

            # Tipos de notificaÃ§Ã£o
            grupo_notificacoes = QGroupBox("Tipos de NotificaÃ§Ã£o")
            notif_layout = QVBoxLayout()

            cb_notas_baixas = QCheckBox("Alertas de notas baixas")
            cb_notas_baixas.setChecked(True)

            cb_aniversarios = QCheckBox("Lembretes de aniversÃ¡rios")
            cb_aniversarios.setChecked(True)

            cb_pagamentos = QCheckBox("Lembretes de pagamentos")
            cb_pagamentos.setChecked(True)

            cb_faltas = QCheckBox("Alertas de faltas excessivas")
            cb_faltas.setChecked(True)

            cb_atualizacoes = QCheckBox("AtualizaÃ§Ãµes do sistema")
            cb_atualizacoes.setChecked(True)

            notif_layout.addWidget(cb_notas_baixas)
            notif_layout.addWidget(cb_aniversarios)
            notif_layout.addWidget(cb_pagamentos)
            notif_layout.addWidget(cb_faltas)
            notif_layout.addWidget(cb_atualizacoes)
            grupo_notificacoes.setLayout(notif_layout)

            # FrequÃªncia
            grupo_frequencia = QGroupBox("FrequÃªncia das NotificaÃ§Ãµes")
            freq_layout = QFormLayout()

            combo_frequencia = QComboBox()
            combo_frequencia.addItems([
                "Diariamente",
                "Semanalmente",
                "Mensalmente",
                "Apenas quando necessÃ¡rio"
            ])
            combo_frequencia.setCurrentText("Diariamente")

            cb_email = QCheckBox("Enviar notificaÃ§Ãµes por e-mail")
            cb_popup = QCheckBox("Mostrar popup no sistema")
            cb_popup.setChecked(True)

            freq_layout.addRow("FrequÃªncia:", combo_frequencia)
            freq_layout.addRow(cb_email)
            freq_layout.addRow(cb_popup)
            grupo_frequencia.setLayout(freq_layout)

            # BotÃµes
            button_box = QDialogButtonBox(
                QDialogButtonBox.Save | QDialogButtonBox.Cancel
            )
            button_box.accepted.connect(dialog.accept)
            button_box.rejected.connect(dialog.reject)

            layout.addWidget(titulo)
            layout.addWidget(grupo_notificacoes)
            layout.addWidget(grupo_frequencia)
            layout.addWidget(button_box)

            dialog.setLayout(layout)

            if dialog.exec_() == QDialog.Accepted:
                # Salvar configuraÃ§Ãµes
                config = {
                    'notas_baixas': cb_notas_baixas.isChecked(),
                    'aniversarios': cb_aniversarios.isChecked(),
                    'pagamentos': cb_pagamentos.isChecked(),
                    'faltas': cb_faltas.isChecked(),
                    'atualizacoes': cb_atualizacoes.isChecked(),
                    'frequencia': combo_frequencia.currentText(),
                    'enviar_email': cb_email.isChecked(),
                    'mostrar_popup': cb_popup.isChecked()
                }

                # Salvar em arquivo de configuraÃ§Ã£o
                config_file = os.path.join(os.path.expanduser("~"), ".escola_notificacoes.json")
                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=4)

                QMessageBox.information(self, "Sucesso", "ConfiguraÃ§Ãµes salvas com sucesso!")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao configurar notificaÃ§Ãµes: {str(e)}")

    def verificar_notificacoes_pendentes(self):
        """Verifica e mostra notificaÃ§Ãµes pendentes"""
        try:
            if not self.db.conn:
                return

            notificacoes = []
            cursor = self.db.conn.cursor()

            # Verificar notas baixas
            cursor.execute("""
                SELECT a.nome_completo, d.nome_disciplina, n.nota
                FROM alunos a
                JOIN notas n ON a.id = n.aluno_id
                JOIN disciplinas d ON n.disciplina_id = d.id
                WHERE n.nota < 6
                AND n.data >= date('now', '-30 days')
            """)
            notas_baixas = cursor.fetchall()

            if notas_baixas:
                notificacoes.append(f"âš ï¸ {len(notas_baixas)} aluno(s) com nota abaixo de 6")

            # Verificar aniversariantes do dia
            cursor.execute("""
                SELECT nome_completo
                FROM alunos
                WHERE strftime('%m-%d', data_nascimento) = strftime('%m-%d', 'now')
            """)
            aniversariantes = cursor.fetchall()

            if aniversariantes:
                nomes = ", ".join([a[0] for a in aniversariantes[:3]])  # Limitar a 3 nomes
                if len(aniversariantes) > 3:
                    nomes += f" e mais {len(aniversariantes) - 3}"
                notificacoes.append(f"ðŸŽ‚ Aniversariantes hoje: {nomes}")

            # Verificar pagamentos atrasados
            cursor.execute("""
                SELECT COUNT(*)
                FROM financeiro
                WHERE strftime('%Y-%m-%d', data_vencimento) < date('now')
                AND status_pagamento = 'Pendente'
            """)
            pagamentos_atrasados = cursor.fetchone()[0]

            if pagamentos_atrasados > 0:
                notificacoes.append(f"ðŸ’° {pagamentos_atrasados} pagamento(s) atrasado(s)")

            # Mostrar notificaÃ§Ãµes se houver
            if notificacoes:
                mensagem = "ðŸ“¢ NOTIFICAÃ‡Ã•ES:\n\n" + "\n\n".join(notificacoes)

                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("NotificaÃ§Ãµes do Sistema")
                msg_box.setText(mensagem)
                msg_box.setIcon(QMessageBox.Information)
                msg_box.addButton("Marcar como Lidas", QMessageBox.AcceptRole)
                msg_box.addButton("Mais Tarde", QMessageBox.RejectRole)

                # Adicionar Ã­cone personalizado
                msg_box.setStyleSheet("""
                    QMessageBox {
                        background-color: white;
                        font-size: 13px;
                    }
                    QMessageBox QLabel {
                        color: #2c3e50;
                        font-weight: normal;
                    }
                """)

                resposta = msg_box.exec_()

                if resposta == QMessageBox.AcceptRole:
                    print("NotificaÃ§Ãµes marcadas como lidas")

        except Exception as e:
            print(f"Erro ao verificar notificaÃ§Ãµes: {e}")

    def criar_copia_seguranca_automatica(self):
        """Cria cÃ³pia de seguranÃ§a automÃ¡tica"""
        try:
            if not hasattr(self, 'ultimo_backup'):
                self.ultimo_backup = None

            agora = datetime.now()

            # Verificar se passou 24 horas desde o Ãºltimo backup
            if self.ultimo_backup and (agora - self.ultimo_backup).days < 1:
                return

            # Criar diretÃ³rio de backups se nÃ£o existir
            backup_dir = os.path.join(os.path.expanduser("~"), "BackupsEscola")
            os.makedirs(backup_dir, exist_ok=True)

            # Nome do arquivo com data/hora
            nome_arquivo = f"backup_auto_{agora.strftime('%Y%m%d_%H%M%S')}.db"
            caminho_backup = os.path.join(backup_dir, nome_arquivo)

            # Criar backup
            if self.db.conn and hasattr(self.db, 'db_path'):
                import shutil
                shutil.copy2(self.db.db_path, caminho_backup)

                # Manter apenas os 10 backups mais recentes
                backups = sorted([f for f in os.listdir(backup_dir) if f.startswith('backup_auto_')])
                if len(backups) > 10:
                    for arquivo_antigo in backups[:-10]:
                        os.remove(os.path.join(backup_dir, arquivo_antigo))

                self.ultimo_backup = agora
                print(f"Backup automÃ¡tico criado: {caminho_backup}")

        except Exception as e:
            print(f"Erro ao criar backup automÃ¡tico: {e}")

    def monitorar_recursos_sistema(self):
        """Monitora uso de recursos do sistema"""
        try:
            import psutil
            import platform

            info = {
                'sistema': platform.system(),
                'processador': platform.processor(),
                'ram_total': psutil.virtual_memory().total / (1024 ** 3),  # GB
                'ram_usada': psutil.virtual_memory().used / (1024 ** 3),  # GB
                'ram_percent': psutil.virtual_memory().percent,
                'cpu_percent': psutil.cpu_percent(interval=1),
                'disco_total': psutil.disk_usage('/').total / (1024 ** 3),  # GB
                'disco_usado': psutil.disk_usage('/').used / (1024 ** 3),  # GB
                'disco_percent': psutil.disk_usage('/').percent
            }

            # Mostrar informaÃ§Ãµes em uma janela
            dialog = QDialog(self)
            dialog.setWindowTitle("ðŸ“Š Monitor de Recursos")
            dialog.setFixedSize(400, 300)

            layout = QVBoxLayout()

            texto_info = QTextEdit()
            texto_info.setReadOnly(True)
            texto_info.setHtml(f"""
                <div style='font-family: Consolas, monospace; font-size: 12px;'>
                    <h3 style='color: #2c3e50;'>SISTEMA DE MONITORAMENTO</h3>
                    <hr>
                    <p><b>Sistema Operacional:</b> {info['sistema']}</p>
                    <p><b>Processador:</b> {info['processador']}</p>

                    <h4 style='color: #3498db;'>MEMÃ“RIA RAM</h4>
                    <p>Total: {info['ram_total']:.2f} GB</p>
                    <p>Usada: {info['ram_usada']:.2f} GB ({info['ram_percent']:.1f}%)</p>

                    <h4 style='color: #27ae60;'>CPU</h4>
                    <p>Uso: {info['cpu_percent']:.1f}%</p>

                    <h4 style='color: #e74c3c;'>DISCO</h4>
                    <p>Total: {info['disco_total']:.2f} GB</p>
                    <p>Usado: {info['disco_usado']:.2f} GB ({info['disco_percent']:.1f}%)</p>

                    <hr>
                    <p style='color: #7f8c8d; font-size: 10px;'>
                        Monitorado em: {datetime.now().strftime('%H:%M:%S')}
                    </p>
                </div>
            """)

            btn_fechar = QPushButton("Fechar")
            btn_fechar.clicked.connect(dialog.accept)
            btn_fechar.setStyleSheet("""
                QPushButton {
                    background-color: #95a5a6;
                    color: white;
                    padding: 8px 20px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #7f8c8d;
                }
            """)

            layout.addWidget(texto_info)
            layout.addWidget(btn_fechar, alignment=Qt.AlignCenter)

            dialog.setLayout(layout)
            dialog.exec_()

        except ImportError:
            QMessageBox.warning(self, "Aviso",
                                "Biblioteca psutil nÃ£o instalada.\n"
                                "Instale com: pip install psutil")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao monitorar recursos: {str(e)}")

    def configurar_logs_sistema(self):
        """Configura sistema de logs"""
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle("ðŸ“ ConfiguraÃ§Ã£o de Logs")
            dialog.setFixedSize(500, 400)

            layout = QVBoxLayout()

            # NÃ­veis de log
            grupo_nivel = QGroupBox("NÃ­vel de Log")
            nivel_layout = QVBoxLayout()

            rb_debug = QRadioButton("Debug (Todas as informaÃ§Ãµes)")
            rb_info = QRadioButton("Info (Apenas informaÃ§Ãµes importantes)")
            rb_warning = QRadioButton("Warning (Apenas avisos e erros)")
            rb_error = QRadioButton("Error (Apenas erros crÃ­ticos)")
            rb_info.setChecked(True)

            nivel_layout.addWidget(rb_debug)
            nivel_layout.addWidget(rb_info)
            nivel_layout.addWidget(rb_warning)
            nivel_layout.addWidget(rb_error)
            grupo_nivel.setLayout(nivel_layout)

            # Destinos de log
            grupo_destino = QGroupBox("Destino dos Logs")
            destino_layout = QVBoxLayout()

            cb_arquivo = QCheckBox("Salvar em arquivo")
            cb_arquivo.setChecked(True)

            cb_console = QCheckBox("Mostrar no console")

            cb_banco = QCheckBox("Salvar no banco de dados")

            destino_layout.addWidget(cb_arquivo)
            destino_layout.addWidget(cb_console)
            destino_layout.addWidget(cb_banco)
            grupo_destino.setLayout(destino_layout)

            # RotaÃ§Ã£o de logs
            grupo_rotacao = QGroupBox("RotaÃ§Ã£o de Logs")
            rotacao_layout = QFormLayout()

            spin_tamanho = QSpinBox()
            spin_tamanho.setRange(1, 100)
            spin_tamanho.setValue(10)
            spin_tamanho.setSuffix(" MB")

            spin_backups = QSpinBox()
            spin_backups.setRange(1, 50)
            spin_backups.setValue(5)

            rotacao_layout.addRow("Tamanho mÃ¡ximo por arquivo:", spin_tamanho)
            rotacao_layout.addRow("NÃºmero de backups mantidos:", spin_backups)
            grupo_rotacao.setLayout(rotacao_layout)

            # BotÃµes
            button_box = QDialogButtonBox(
                QDialogButtonBox.Save | QDialogButtonBox.Cancel | QDialogButtonBox.Reset
            )
            button_box.accepted.connect(dialog.accept)
            button_box.rejected.connect(dialog.reject)
            button_box.button(QDialogButtonBox.Reset).clicked.connect(
                lambda: self.restaurar_configuracoes_logs_padrao()
            )

            layout.addWidget(grupo_nivel)
            layout.addWidget(grupo_destino)
            layout.addWidget(grupo_rotacao)
            layout.addWidget(button_box)

            dialog.setLayout(layout)

            if dialog.exec_() == QDialog.Accepted:
                # Salvar configuraÃ§Ãµes
                config_logs = {
                    'nivel': 'DEBUG' if rb_debug.isChecked() else
                    'INFO' if rb_info.isChecked() else
                    'WARNING' if rb_warning.isChecked() else 'ERROR',
                    'salvar_arquivo': cb_arquivo.isChecked(),
                    'mostrar_console': cb_console.isChecked(),
                    'salvar_banco': cb_banco.isChecked(),
                    'tamanho_max_mb': spin_tamanho.value(),
                    'backups_mantidos': spin_backups.value()
                }

                # Salvar em arquivo de configuraÃ§Ã£o
                config_file = os.path.join(os.path.expanduser("~"), ".escola_logs_config.json")
                with open(config_file, 'w') as f:
                    json.dump(config_logs, f, indent=4)

                QMessageBox.information(self, "Sucesso", "ConfiguraÃ§Ãµes de logs salvas!")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao configurar logs: {str(e)}")

    def restaurar_configuracoes_logs_padrao(self):
        """Restaura configuraÃ§Ãµes padrÃ£o de logs"""
        try:
            config_file = os.path.join(os.path.expanduser("~"), ".escola_logs_config.json")
            if os.path.exists(config_file):
                os.remove(config_file)

            QMessageBox.information(self, "Sucesso",
                                    "ConfiguraÃ§Ãµes de logs restauradas para os padrÃµes!")

        except Exception as e:
            QMessageBox.warning(self, "Aviso", f"Erro ao restaurar configuraÃ§Ãµes: {str(e)}")

    def visualizar_logs_sistema(self):
        """Visualiza logs do sistema"""
        try:
            log_file = os.path.join(os.path.expanduser("~"), "escola_system.log")

            if not os.path.exists(log_file):
                QMessageBox.information(self, "InformaÃ§Ã£o",
                                        "Nenhum arquivo de log encontrado.")
                return

            dialog = QDialog(self)
            dialog.setWindowTitle("ðŸ“‹ Visualizador de Logs")
            dialog.setMinimumSize(800, 600)

            layout = QVBoxLayout()

            # Controles
            controls_layout = QHBoxLayout()

            btn_atualizar = QPushButton("ðŸ”„ Atualizar")
            btn_atualizar.clicked.connect(lambda: self.carregar_logs_na_visualizacao(text_edit, log_file))

            btn_limpar = QPushButton("ðŸ—‘ï¸ Limpar Logs")
            btn_limpar.clicked.connect(lambda: self.limpar_arquivo_logs(log_file, text_edit))

            btn_exportar = QPushButton("ðŸ“¤ Exportar")
            btn_exportar.clicked.connect(lambda: self.exportar_logs(log_file))

            controls_layout.addWidget(btn_atualizar)
            controls_layout.addWidget(btn_limpar)
            controls_layout.addWidget(btn_exportar)
            controls_layout.addStretch()

            # Ãrea de texto para logs
            text_edit = QTextEdit()
            text_edit.setReadOnly(True)
            text_edit.setFont(QFont("Courier", 10))

            # Carregar logs inicialmente
            self.carregar_logs_na_visualizacao(text_edit, log_file)

            # BotÃ£o fechar
            btn_fechar = QPushButton("Fechar")
            btn_fechar.clicked.connect(dialog.accept)

            layout.addLayout(controls_layout)
            layout.addWidget(text_edit)
            layout.addWidget(btn_fechar, alignment=Qt.AlignCenter)

            dialog.setLayout(layout)
            dialog.exec_()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao visualizar logs: {str(e)}")

    def carregar_logs_na_visualizacao(self, text_edit, log_file):
        """Carrega logs na visualizaÃ§Ã£o"""
        try:
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = f.read()

                text_edit.clear()

                # Adicionar com formataÃ§Ã£o de cores
                for linha in logs.split('\n'):
                    if 'ERROR' in linha:
                        text_edit.setTextColor(QColor(231, 76, 60))  # Vermelho
                    elif 'WARNING' in linha:
                        text_edit.setTextColor(QColor(241, 196, 15))  # Amarelo
                    elif 'INFO' in linha:
                        text_edit.setTextColor(QColor(52, 152, 219))  # Azul
                    elif 'DEBUG' in linha:
                        text_edit.setTextColor(QColor(46, 204, 113))  # Verde
                    else:
                        text_edit.setTextColor(QColor(44, 62, 80))  # Preto

                    text_edit.append(linha)

                # Rolar para o final
                text_edit.moveCursor(QTextCursor.End)
            else:
                text_edit.setText("Nenhum log encontrado.")

        except Exception as e:
            text_edit.setText(f"Erro ao carregar logs: {str(e)}")

    def limpar_arquivo_logs(self, log_file, text_edit):
        """Limpa o arquivo de logs"""
        try:
            resposta = QMessageBox.question(
                self,
                "Confirmar Limpeza",
                "Deseja limpar todos os logs do sistema?\n"
                "Esta aÃ§Ã£o nÃ£o pode ser desfeita.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if resposta == QMessageBox.Yes:
                open(log_file, 'w').close()
                text_edit.clear()
                text_edit.setText("Logs limpos com sucesso.")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao limpar logs: {str(e)}")

    def exportar_logs(self, log_file):
        """Exporta logs para um arquivo"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Exportar Logs",
                f"logs_escola_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                "Arquivos de Texto (*.txt)"
            )

            if file_path and os.path.exists(log_file):
                import shutil
                shutil.copy2(log_file, file_path)
                QMessageBox.information(self, "Sucesso", f"Logs exportados para:\n{file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao exportar logs: {str(e)}")

    def encerrar_sistema(self):
        """Procedimento de encerramento do sistema"""
        try:
            resposta = QMessageBox.question(
                self,
                "Encerrar Sistema",
                "Deseja realmente encerrar o sistema de gestÃ£o escolar?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if resposta == QMessageBox.Yes:
                # Criar backup automÃ¡tico antes de sair
                self.criar_copia_seguranca_automatica()

                # Salvar configuraÃ§Ãµes da janela
                settings = QSettings("EscolaSystem", "GestaoEscolar")
                settings.setValue("geometry", self.saveGeometry())
                settings.setValue("windowState", self.saveState())

                # Fechar conexÃ£o com banco de dados
                if hasattr(self, 'db') and self.db.conn:
                    self.db.conn.close()

                # Registrar log de encerramento
                print(f"Sistema encerrado em: {datetime.now()}")

                # Encerrar aplicaÃ§Ã£o
                QApplication.quit()

        except Exception as e:
            QMessageBox.critical(self, "Erro CrÃ­tico",
                                 f"Erro ao encerrar sistema: {str(e)}\n"
                                 "O sistema serÃ¡ forÃ§ado a fechar.")
            sys.exit(1)

    def closeEvent(self, event):
        """Evento de fechamento da janela principal"""
        try:
            # Perguntar se quer salvar antes de sair
            resposta = QMessageBox.question(
                self,
                "Confirmar SaÃ­da",
                "Deseja realmente sair do sistema?",
                QMessageBox.Yes | QButton.No,
                QButton.No
            )

            if resposta == QMessageBox.Yes:
                # Executar procedimento de encerramento
                self.encerrar_sistema()
                event.accept()
            else:
                event.ignore()

        except Exception as e:
            print(f"Erro no closeEvent: {e}")
            event.accept()


# ============================================
# CLASSE DATABASE - MELHORADA E PROFISSIONAL
# ============================================
class DatabaseManager:
    """Gerencia todas as operaÃ§Ãµes de banco de dados"""

    def __init__(self, db_path="escola.db"):
        self.db_path = db_path
        self.conn = None
        self.connect()
        self.criar_tabelas()

    def connect(self):
        """Estabelece conexÃ£o com o banco de dados"""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            print(f"ConexÃ£o estabelecida com: {self.db_path}")
            return True
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco: {e}")
            return False

    def criar_tabelas(self):
        """Cria todas as tabelas necessÃ¡rias se nÃ£o existirem"""
        try:
            cursor = self.conn.cursor()

            # Tabela de turmas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS turmas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_turma TEXT NOT NULL UNIQUE,
                    ano_letivo TEXT NOT NULL,
                    periodo TEXT NOT NULL,
                    sala TEXT,
                    capacidade INTEGER DEFAULT 30,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ativa BOOLEAN DEFAULT 1
                )
            ''')

            # Tabela de alunos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alunos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_completo TEXT NOT NULL,
                    data_nascimento DATE NOT NULL,
                    cpf TEXT UNIQUE,
                    rg TEXT,
                    nome_mae TEXT,
                    nome_pai TEXT,
                    telefone TEXT,
                    email TEXT,
                    endereco TEXT,
                    cidade TEXT,
                    estado TEXT,
                    cep TEXT,
                    turma_id INTEGER,
                    data_matricula DATE DEFAULT CURRENT_DATE,
                    status TEXT DEFAULT 'Ativo',
                    observacoes TEXT,
                    foto BLOB,
                    FOREIGN KEY (turma_id) REFERENCES turmas (id) ON DELETE SET NULL
                )
            ''')

            # Tabela de professores
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS professores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_completo TEXT NOT NULL,
                    data_nascimento DATE,
                    cpf TEXT UNIQUE,
                    rg TEXT,
                    telefone TEXT,
                    email TEXT UNIQUE,
                    formacao TEXT,
                    disciplina_principal TEXT,
                    data_admissao DATE DEFAULT CURRENT_DATE,
                    salario DECIMAL(10,2),
                    status TEXT DEFAULT 'Ativo',
                    observacoes TEXT
                )
            ''')

            # Tabela de disciplinas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS disciplinas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_disciplina TEXT NOT NULL UNIQUE,
                    carga_horaria INTEGER,
                    professor_id INTEGER,
                    turma_id INTEGER,
                    dia_semana TEXT,
                    horario_inicio TIME,
                    horario_fim TIME,
                    sala TEXT,
                    ativa BOOLEAN DEFAULT 1,
                    FOREIGN KEY (professor_id) REFERENCES professores (id) ON DELETE SET NULL,
                    FOREIGN KEY (turma_id) REFERENCES turmas (id) ON DELETE CASCADE
                )
            ''')

            # Tabela de notas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    aluno_id INTEGER NOT NULL,
                    disciplina_id INTEGER NOT NULL,
                    nota DECIMAL(4,2) CHECK (nota >= 0 AND nota <= 10),
                    bimestre INTEGER CHECK (bimestre BETWEEN 1 AND 4),
                    ano_letivo TEXT,
                    data_avaliacao DATE DEFAULT CURRENT_DATE,
                    tipo_avaliacao TEXT,
                    peso DECIMAL(3,2) DEFAULT 1.0,
                    observacoes TEXT,
                    FOREIGN KEY (aluno_id) REFERENCES alunos (id) ON DELETE CASCADE,
                    FOREIGN KEY (disciplina_id) REFERENCES disciplinas (id) ON DELETE CASCADE,
                    UNIQUE(aluno_id, disciplina_id, bimestre, ano_letivo)
                )
            ''')

            # Tabela de frequÃªncia
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS frequencia (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    aluno_id INTEGER NOT NULL,
                    disciplina_id INTEGER NOT NULL,
                    data DATE NOT NULL,
                    presenca BOOLEAN DEFAULT 1,
                    justificativa TEXT,
                    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (aluno_id) REFERENCES alunos (id) ON DELETE CASCADE,
                    FOREIGN KEY (disciplina_id) REFERENCES disciplinas (id) ON DELETE CASCADE,
                    UNIQUE(aluno_id, disciplina_id, data)
                )
            ''')

            # Tabela de usuÃ¡rios (para login)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    email TEXT UNIQUE,
                    tipo_usuario TEXT DEFAULT 'professor',
                    professor_id INTEGER UNIQUE,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ultimo_login TIMESTAMP,
                    ativo BOOLEAN DEFAULT 1,
                    FOREIGN KEY (professor_id) REFERENCES professores (id) ON DELETE CASCADE
                )
            ''')

            # Tabela financeira (se necessÃ¡rio)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS financeiro (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    aluno_id INTEGER,
                    descricao TEXT NOT NULL,
                    valor DECIMAL(10,2) NOT NULL,
                    data_vencimento DATE,
                    data_pagamento DATE,
                    status_pagamento TEXT DEFAULT 'Pendente',
                    forma_pagamento TEXT,
                    observacoes TEXT,
                    FOREIGN KEY (aluno_id) REFERENCES alunos (id) ON DELETE SET NULL
                )
            ''')

            # Tabela de eventos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS eventos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    descricao TEXT,
                    data_inicio DATETIME NOT NULL,
                    data_fim DATETIME,
                    local TEXT,
                    tipo_evento TEXT,
                    participantes TEXT,
                    cor_evento TEXT DEFAULT '#3498db',
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Tabela de logs do sistema
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS logs_sistema (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nivel TEXT NOT NULL,
                    mensagem TEXT NOT NULL,
                    modulo TEXT,
                    usuario TEXT,
                    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ip_address TEXT
                )
            ''')

            self.conn.commit()
            print("Tabelas criadas/verificadas com sucesso!")

            # Criar usuÃ¡rio admin padrÃ£o se nÃ£o existir
            self.criar_usuario_admin_padrao()

        except sqlite3.Error as e:
            print(f"Erro ao criar tabelas: {e}")

    def criar_usuario_admin_padrao(self):
        """Cria usuÃ¡rio administrador padrÃ£o"""
        try:
            cursor = self.conn.cursor()

            # Verificar se jÃ¡ existe admin
            cursor.execute("SELECT COUNT(*) FROM usuarios WHERE username = 'admin'")
            if cursor.fetchone()[0] == 0:
                # Hash da senha padrÃ£o
                senha_hash = hashlib.sha256("admin123".encode()).hexdigest()

                cursor.execute('''
                    INSERT INTO usuarios (username, password_hash, email, tipo_usuario)
                    VALUES (?, ?, ?, ?)
                ''', ('admin', senha_hash, 'admin@escola.com', 'administrador'))

                self.conn.commit()
                print("UsuÃ¡rio admin padrÃ£o criado (senha: admin123)")

        except sqlite3.Error as e:
            print(f"Erro ao criar usuÃ¡rio admin: {e}")

    def executar_consulta(self, query, params=()):
        """Executa uma consulta SQL"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)

            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            else:
                self.conn.commit()
                return cursor.rowcount

        except sqlite3.Error as e:
            print(f"Erro na consulta: {e}")
            return None

    def buscar_um(self, query, params=()):
        """Busca um Ãºnico registro"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Erro na busca: {e}")
            return None

    def inserir_registro(self, tabela, dados):
        """Insere um registro em uma tabela"""
        try:
            cursor = self.conn.cursor()

            colunas = ', '.join(dados.keys())
            placeholders = ', '.join(['?' for _ in dados])

            query = f"INSERT INTO {tabela} ({colunas}) VALUES ({placeholders})"
            cursor.execute(query, list(dados.values()))

            self.conn.commit()
            return cursor.lastrowid

        except sqlite3.Error as e:
            print(f"Erro ao inserir registro: {e}")
            return None

    def atualizar_registro(self, tabela, id_registro, dados):
        """Atualiza um registro existente"""
        try:
            cursor = self.conn.cursor()

            sets = ', '.join([f"{k} = ?" for k in dados.keys()])
            query = f"UPDATE {tabela} SET {sets} WHERE id = ?"

            params = list(dados.values()) + [id_registro]
            cursor.execute(query, params)

            self.conn.commit()
            return cursor.rowcount

        except sqlite3.Error as e:
            print(f"Erro ao atualizar registro: {e}")
            return None

    def deletar_registro(self, tabela, id_registro):
        """Deleta um registro"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"DELETE FROM {tabela} WHERE id = ?", (id_registro,))
            self.conn.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            print(f"Erro ao deletar registro: {e}")
            return None

    def buscar_todos(self, tabela, condicao="", params=()):
        """Busca todos os registros de uma tabela"""
        try:
            cursor = self.conn.cursor()

            query = f"SELECT * FROM {tabela}"
            if condicao:
                query += f" WHERE {condicao}"

            cursor.execute(query, params)
            return cursor.fetchall()

        except sqlite3.Error as e:
            print(f"Erro ao buscar registros: {e}")
            return []

    def contar_registros(self, tabela, condicao="", params=()):
        """Conta registros em uma tabela"""
        try:
            cursor = self.conn.cursor()

            query = f"SELECT COUNT(*) FROM {tabela}"
            if condicao:
                query += f" WHERE {condicao}"

            cursor.execute(query, params)
            return cursor.fetchone()[0]

        except sqlite3.Error as e:
            print(f"Erro ao contar registros: {e}")
            return 0

    def verificar_login(self, username, password):
        """Verifica credenciais de login"""
        try:
            cursor = self.conn.cursor()

            # Buscar hash da senha
            cursor.execute(
                "SELECT password_hash, tipo_usuario, professor_id FROM usuarios WHERE username = ? AND ativo = 1",
                (username,)
            )

            resultado = cursor.fetchone()
            if resultado:
                senha_hash_armazenada = resultado['password_hash']
                senha_hash_input = hashlib.sha256(password.encode()).hexdigest()

                if senha_hash_input == senha_hash_armazenada:
                    # Atualizar Ãºltimo login
                    cursor.execute(
                        "UPDATE usuarios SET ultimo_login = CURRENT_TIMESTAMP WHERE username = ?",
                        (username,)
                    )
                    self.conn.commit()

                    return {
                        'tipo_usuario': resultado['tipo_usuario'],
                        'professor_id': resultado['professor_id']
                    }

            return None

        except sqlite3.Error as e:
            print(f"Erro ao verificar login: {e}")
            return None

    def registrar_log(self, nivel, mensagem, modulo="", usuario=""):
        """Registra log no banco de dados"""
        try:
            cursor = self.conn.cursor()

            cursor.execute('''
                INSERT INTO logs_sistema (nivel, mensagem, modulo, usuario)
                VALUES (?, ?, ?, ?)
            ''', (nivel, mensagem, modulo, usuario))

            self.conn.commit()

        except sqlite3.Error as e:
            print(f"Erro ao registrar log: {e}")

    def fazer_backup(self, caminho_backup):
        """Faz backup do banco de dados"""
        try:
            backup_conn = sqlite3.connect(caminho_backup)
            self.conn.backup(backup_conn)
            backup_conn.close()
            return True
        except Exception as e:
            print(f"Erro ao fazer backup: {e}")
            return False

    def verificar_integridade(self):
        """Verifica integridade do banco de dados"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("PRAGMA integrity_check")
            resultado = cursor.fetchone()
            return resultado[0] == "ok"
        except sqlite3.Error as e:
            print(f"Erro ao verificar integridade: {e}")
            return False

    def otimizar(self):
        """Otimiza o banco de dados"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("VACUUM")
            cursor.execute("ANALYZE")
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao otimizar: {e}")
            return False

    def fechar_conexao(self):
        """Fecha a conexÃ£o com o banco de dados"""
        try:
            if self.conn:
                self.conn.close()
                print("ConexÃ£o com banco de dados fechada.")
        except Exception as e:
            print(f"Erro ao fechar conexÃ£o: {e}")


# ============================================
# FUNÃ‡ÃƒO PRINCIPAL
# ============================================
def main():
    """FunÃ§Ã£o principal que inicia a aplicaÃ§Ã£o"""
    try:
        # Configurar aplicaÃ§Ã£o
        app = QApplication(sys.argv)
        app.setApplicationName("Sistema de GestÃ£o Escolar")
        app.setOrganizationName("EscolaSystem")

        # Aplicar estilo global
        app.setStyleSheet(GLOBAL_STYLESHEET)

        # Criar e mostrar janela principal
        window = EscolaApp()
        window.show()

        # Executar aplicaÃ§Ã£o
        sys.exit(app.exec_())

    except Exception as e:
        print(f"Erro fatal na aplicaÃ§Ã£o: {e}")
        QMessageBox.critical(None, "Erro Fatal",
                             f"Ocorreu um erro fatal na aplicaÃ§Ã£o:\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()


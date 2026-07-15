# database/db_manager.py
import sqlite3

def conectar_banco():
    """Estabelece a conexão com o banco de dados do Avalia+"""
    return sqlite3.connect("avalia_mais.db", check_same_thread=False)

def inicializar_tabelas():
    """Cria a estrutura de tabelas se elas não existirem"""
    conn = conectar_banco()
    cursor = conn.cursor()
    
    # 1. Tabela de Pacientes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pacientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        data_nascimento TEXT NOT NULL,
        dias_atividade TEXT NOT NULL,
        nome_responsavel TEXT,
        telefone TEXT
    )
    """)
    
    # 2. Tabela de Avaliações e Reavaliações (Histórico)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS avaliacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        data_avaliacao TEXT NOT NULL,
        teste_sentar_levantar REAL,
        teste_tug REAL,
        teste_tandem REAL,
        teste_taf REAL,
        observacoes TEXT,
        FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
    )
    """)
    
    conn.commit()
    conn.close()

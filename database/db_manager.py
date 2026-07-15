# database/db_manager.py
import sqlite3

def conectar_banco():
    """Conecta de forma rápida e segura ao banco de dados interno do Avalia+"""
    return sqlite3.connect("avalia_mais.db", check_same_thread=False)

def inicializar_tabelas():
    """Faz a limpeza automática de duplicados antigos e aplica a trava de Nome Único"""
    conn = conectar_banco()
    cursor = conn.cursor()
    
    # 1. Cria a tabela padrão se ela não existir (sem a trava ainda, caso seja antiga)
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
    
    # 2. FAXINA AUTOMÁTICA: Apaga os nomes duplicados se houver algum, mantendo sempre o de menor ID (o primeiro criado)
    try:
        cursor.execute("""
        DELETE FROM pacientes 
        WHERE id NOT IN (
            SELECT MIN(id) 
            FROM pacientes 
            GROUP BY nome
        )
        """)
        conn.commit()
    except:
        pass

    # 3. Tabela de Avaliações
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS avaliacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        data_avaliacao TEXT NOT NULL,
        tipo_consulta TEXT DEFAULT 'Avaliação',
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

# database/db_manager.py
import sqlite3

def conectar_banco():
    """Conecta de forma rápida e segura ao banco de dados interno do Avalia+"""
    return sqlite3.connect("avalia_mais.db", check_same_thread=False)

def inicializar_tabelas():
    """Cria a estrutura de tabelas local e garante que a coluna nova exista"""
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
    
    # 2. Tabela de Avaliações
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
    
    # 3. ADEQUAÇÃO FORÇADA: Tenta injetar a coluna se ela não existir no arquivo .db
    try:
        cursor.execute("ALTER TABLE avaliacoes ADD COLUMN tipo_consulta TEXT DEFAULT 'Avaliação'")
    except sqlite3.OperationalError:
        # Se der esse erro, significa que a coluna já existe, então podemos ignorar com segurança
        pass
        
    conn.commit()
    conn.close()

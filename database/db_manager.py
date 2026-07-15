# database/db_manager.py
import psycopg2

def conectar_banco():
    """Estabelece conexão com o Supabase usando o formato clássico de autenticação do pooler"""
    # CORRIGIDO: O usuário volta a ser apenas 'postgres' e injetamos o ID do projeto na linha de conexão (options)
    return psycopg2.connect(
        host="aws-0-sa-east-1.pooler.supabase.com",
        port=6543,
        database="postgres",
        user="postgres",
        password="EwZS+V.DY#8wkYD",
        options="-c project=oybfpmbpengfhmxkkrxn"  # <-- Ajuste cirúrgico que faltava!
    )

def inicializar_tabelas():
    """Cria as tabelas direto na nuvem do Supabase se elas não existirem"""
    conn = conectar_banco()
    cursor = conn.cursor()
    
    # 1. Tabela de Pacientes (com trava de nome único)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS public.pacientes (
        id SERIAL PRIMARY KEY,
        nome TEXT NOT NULL UNIQUE,
        data_nascimento TEXT NOT NULL,
        dias_atividade TEXT NOT NULL,
        nome_responsavel TEXT,
        telefone TEXT
    );
    """)
    
    # 2. Tabela de Avaliações
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS public.avaliacoes (
        id SERIAL PRIMARY KEY,
        paciente_id INTEGER NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
        data_avaliacao TEXT NOT NULL,
        tipo_consulta TEXT DEFAULT 'Avaliação',
        teste_sentar_levantar REAL,
        teste_tug REAL,
        teste_tandem REAL,
        teste_taf REAL,
        observacoes TEXT
    );
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

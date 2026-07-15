# database/db_manager.py
import psycopg2

# Conexão direta e nativa com o banco de dados Postgres do seu Supabase
CONEXAO_URI = "postgresql://postgres:EwZS+V.DY#8wkYD@db.oybfpmbpengfhmxkkrxn.supabase.co:5432/postgres"

def conectar_banco():
    """Estabelece conexão direta e nativa com o banco de dados Postgres do Supabase"""
    return psycopg2.connect(CONEXAO_URI)

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
        paciente_id INTEGER NOT NULL REFERENCES public.pacientes(id) ON DELETE CASCADE,
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

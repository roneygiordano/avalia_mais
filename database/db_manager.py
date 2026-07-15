# database/db_manager.py
import psycopg2

def conectar_banco():
    """Estabelece conexão com o Supabase usando o Host e a Porta estáveis de Connection Pooling"""
    # CORRIGIDO: Atualizado o host real do servidor atual e a porta estável 6543
    return psycopg2.connect(
        host="://supabase.com",
        port=6543,
        database="postgres",
        user="postgres.oybfpmbpengfhmxkkrxn", # O ID do projeto é embutido no usuário para autenticação segura
        password="EwZS+V.DY#8wkYD"
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

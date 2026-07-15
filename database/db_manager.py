# database/db_manager.py
from supabase import create_client, Client

# CORRIGIDO: Agora aponta direto para o seu servidor privado, e não para o site público!
SUPABASE_URL = "https://rxginxtkxarpectwbemz.supabase.co"

# Sua chave Publishable permanece exatamente a mesma
SUPABASE_KEY = "sb_publishable_inzZh573U_sXX0qnVMLcPw_7hp6Hzw1"

def conectar_banco() -> Client:
    """Estabelece a conexão direta com o banco de dados em nuvem do Supabase"""
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def inicializar_tabelas():
    """Valida se a conexão com o Supabase está ativa e funcional"""
    try:
        supabase = conectar_banco()
        supabase.table("pacientes").select("id").limit(1).execute()
    except Exception as e:
        raise Exception(f"Falha ao conectar ao Supabase. Verifique as chaves. Erro: {e}")

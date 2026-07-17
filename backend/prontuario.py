# backend/prontuario.py
import streamlit as st
from supabase import create_client

# Inicializa o cliente do Supabase de forma isolada e segura
@st.cache_resource
def obter_conexao_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = obter_conexao_supabase()

def salvar_nova_observacao(paciente_id, data_texto, observacao_texto):
    """Insere a observação clínica vinculada ao ID do paciente no Supabase"""
    try:
        dados = {
            "paciente_id": paciente_id,
            "data_atendimento": data_texto,
            "observacao": observacao_texto
        }
        supabase.table("prontuarios").insert(dados).execute()
        return True, "✅ Observação gravada com sucesso no prontuário!"
    except Exception as e:
        return False, f"Erro ao salvar no Supabase: {e}"

def listar_prontuario_por_paciente(paciente_id):
    """Busca o histórico de observações do paciente do mais recente ao mais antigo"""
    try:
        resposta = supabase.table("prontuarios") \
                       .select("data_atendimento, observacao") \
                       .eq("paciente_id", paciente_id) \
                       .execute()
        return resposta.data
    except Exception as e:
        st.error(f"Erro ao carregar histórico: {e}")
        return []

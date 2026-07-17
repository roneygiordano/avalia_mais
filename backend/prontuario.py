# backend/prontuario.py
import streamlit as st
from st_supabase_connection import SupabaseConnection

def salvar_nova_observacao(paciente_id, data_texto, observacao_texto):
    """Insere a observação clínica vinculada ao ID do paciente no Supabase"""
    try:
        conn = st.connection("supabase", type=SupabaseConnection)
        dados = {
            "paciente_id": int(paciente_id),
            "data_atendimento": str(data_texto),
            "observacao": observacao_texto
        }
        conn.table("prontuarios").insert(dados).execute()
        return True, "✅ Observação gravada com sucesso no prontuário!"
    except Exception as e:
        return False, f"Erro ao salvar no Supabase: {e}"

def listar_prontuario_por_paciente(paciente_id):
    """Busca o histórico de observações do paciente"""
    try:
        conn = st.connection("supabase", type=SupabaseConnection)
        resposta = conn.table("prontuarios") \
                       .select("data_atendimento, observacao") \
                       .eq("paciente_id", int(paciente_id)) \
                       .execute()
        return resposta.data
    except Exception:
        return []

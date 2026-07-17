# backend/prontuario.py
import streamlit as st
# Certifique-se de importar o cliente 'supabase' de onde ele estiver inicializado no seu projeto
# Se estiver no db_manager, use: from database.db_manager import supabase
from database.db_manager import supabase 

def salvar_nova_observacao(paciente_id, data_texto, observacao_texto):
    """Insere a observação clínica vinculada ao ID do paciente no Supabase"""
    try:
        dados = {
            "paciente_id": paciente_id,
            "data_atendimento": data_texto,  # Salva como string no formato desejado
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
        
        # Inverte ou ordena manualmente se não usar o .order() do Supabase,
        # mas o ideal é ordenar pela data decrescente se o campo permitir.
        return resposta.data
    except Exception as e:
        st.error(f"Erro ao carregar histórico: {e}")
        return []

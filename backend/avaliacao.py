# backend/avaliacao.py
import streamlit as st
from st_supabase_connection import SupabaseConnection

def buscar_pacientes_por_dia(dia_semana):
    try:
        conn = st.connection("supabase", type=SupabaseConnection)
        resposta = conn.table("pacientes").select("id, nome").eq("dias_atividade", dia_semana).order("nome").execute()
        dados = [(p["id"], p["nome"]) for p in resposta.data]
        return dados
    except Exception:
        return []

def salvar_nova_avaliacao(paciente_id, data_aval, tipo_consulta, t1, t2, t3, t4, obs):
    try:
        conn = st.connection("supabase", type=SupabaseConnection)
        
        # Verifica se já existe avaliação para o mesmo paciente nesta data
        resultado = conn.table("avaliacoes").select("id").eq("paciente_id", int(paciente_id)).eq("data_avaliacao", str(data_aval)).execute()
        
        dados_avaliacao = {
            "paciente_id": int(paciente_id),
            "data_avaliacao": str(data_aval),
            "tipo_consulta": tipo_consulta,
            "teste_sentar_levantar": float(t1),
            "teste_tug": float(t2),
            "teste_tandem": float(t3),
            "teste_taf": float(t4),
            "observacoes": obs
        }
        
        if resultado.data:
            id_registro = resultado.data[0]["id"]
            conn.table("avaliacoes").update(dados_avaliacao).eq("id", id_registro).execute()
            mensagem_retorno = "Dados da data atualizados com sucesso no Supabase!"
        else:
            conn.table("avaliacoes").insert(dados_avaliacao).execute()
            mensagem_retorno = "Nova avaliação gravada com sucesso no Supabase!"
            
        return True, mensagem_retorno
    except Exception as e:
        return False, f"Erro ao processar gravação: {e}"

def buscar_historico_paciente(paciente_id):
    try:
        conn = st.connection("supabase", type=SupabaseConnection)
        
        # Busca o histórico ordenando por data
        resposta = conn.table("avaliacoes").select(
            "data_avaliacao, tipo_consulta, teste_sentar_levantar, teste_tug, teste_tandem, teste_taf, observacoes"
        ).eq("paciente_id", int(paciente_id)).execute()
        
        # Converte em formato de tuplas para manter total compatibilidade com o backend/analise_view.py
        dados = [
            (
                a["data_avaliacao"],
                a["tipo_consulta"],
                a["teste_sentar_levantar"],
                a["teste_tug"],
                a["teste_tandem"],
                a["teste_taf"],
                a["observacoes"]
            )
            for a in resposta.data
        ]
        return dados
    except Exception as e:
        st.error(f"Erro ao buscar histórico: {e}")
        return []

def zerar_historico_do_paciente(paciente_id):
    try:
        conn = st.connection("supabase", type=SupabaseConnection)
        
        # Correção de segurança: deleta apenas as avaliações deste paciente específico
        conn.table("avaliacoes").delete().eq("paciente_id", int(paciente_id)).execute()
        return True, "Todos os dados do Paciente foram apagados da nuvem"
    except Exception as e:
        return False, f"Erro ao limpar tabela: {e}"

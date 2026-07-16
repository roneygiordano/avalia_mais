# backend/paciente.py
import streamlit as st
from st_supabase_connection import SupabaseConnection

def salvar_novo_paciente(nome, data_nasc, dias_atividade, responsavel, telefone):
    try:
        conn = st.connection("supabase", type=SupabaseConnection)
        
        dados = {
            "nome": nome,
            "data_nascimento": str(data_nasc),
            "dias_atividade": dias_atividade,
            "nome_responsavel": responsavel,
            "telefone": telefone
        }
        
        # Insere direto no Supabase em nuvem em tempo real
        conn.table("pacientes").insert(dados).execute()
        return True, "Paciente cadastrado e salvo na nuvem com sucesso!"
    except Exception as e:
        return False, f"Erro ao salvar no Supabase: {e}"

def listar_todos_pacientes():
    try:
        conn = st.connection("supabase", type=SupabaseConnection)
        
        # Busca todas as colunas da tabela de pacientes ordenando por nome
        resposta = conn.table("pacientes").select("*").order("nome").execute()
        
        if not resposta.data:
            return []
            
        # Monta a lista usando .get() seguro, garantindo as posições exatas esperadas pelo frontend:
        # Posição 0: ID, Posição 1: Nome, Posição 2: Data Nasc, Posição 3: Dias Atividade
        dados = []
        for p in resposta.data:
            dados.append((
                p.get("id"),
                p.get("nome"),
                p.get("data_nascimento"),
                p.get("dias_atividade")
            ))
        return dados
    except Exception as e:
        st.error(f"Erro ao listar pacientes do Supabase: {e}")
        return []

def atualizar_dados_paciente(id_paciente, nome, data_nasc, dias_atividade, responsavel, telefone):
    try:
        conn = st.connection("supabase", type=SupabaseConnection)
        
        dados_atualizados = {
            "nome": nome,
            "data_nascimento": str(data_nasc),
            "dias_atividade": dias_atividade,
            "nome_responsavel": responsavel,
            "telefone": telefone
        }
        
        # Atualiza o registro específico usando o ID como filtro
        conn.table("pacientes").update(dados_atualizados).eq("id", id_paciente).execute()
        return True, "Dados updated na nuvem!"
    except Exception as e:
        return False, f"Erro ao atualizar: {e}"

def excluir_paciente_do_banco(id_paciente):
    try:
        conn = st.connection("supabase", type=SupabaseConnection)
        
        # Remove primeiro as avaliações ligadas ao paciente e depois o paciente (para não dar erro de chave estrangeira)
        try:
            conn.table("avaliacoes").delete().eq("paciente_id", id_paciente).execute()
        except:
            conn.table("avaliacoes").delete().eq("id_paciente", id_paciente).execute()
            
        conn.table("pacientes").delete().eq("id", id_paciente).execute()
        return True, "Paciente removido da nuvem!"
    except Exception as e:
        return False, f"Erro ao deletar: {e}"

# frontend/cadastro_view.py
import streamlit as st
import pandas as pd
from datetime import datetime, date
from backend.paciente import (
    salvar_novo_paciente, 
    listar_todos_pacientes, 
    atualizar_dados_paciente,
    excluir_paciente_do_banco
)

def renderizar_tela_cadastro():
    st.subheader("📋 Gestão de Pacientes")
    
    # Busca todos os pacientes do banco de dados no início
    todos_pacientes = listar_todos_pacientes()

    # Lista de Pacientes Compacta no Topo
    with st.expander("👥 Visualizar Lista de Pacientes Cadastrados (Clique para abrir/fechar)", expanded=False):
        if todos_pacientes:
            df_pacientes = pd.DataFrame(todos_pacientes, columns=["ID", "Nome do Paciente", "Data de Nascimento", "Dias de Atendimento"])
            st.dataframe(df_pacientes, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum paciente cadastrado no sistema.")

    st.write("---")

    # Opções de ação do sistema
    acao = st.radio(
        "O que você deseja fazer?", 
        ["Cadastrar", "Editar", "Excluir"], 
        horizontal=True
    )
    
    if acao in ["Editar Paciente Existente", "Excluir Paciente"] and not todos_pacientes:
        st.warning("Nenhum paciente cadastrado no sistema para realizar esta ação.")
        return

    # --- LÓGICA DE EXCLUSÃO ---
    if acao == "Excluir Paciente":
        opcoes_exclusao = {f"{p[1]} (ID: {p[0]})": p[0] for p in todos_pacientes}
        paciente_selecionado = st.selectbox("Selecione o paciente que deseja REMOVER permanentemente:", list(opcoes_exclusao.keys()))
        id_paciente_exclusao = opcoes_exclusao[paciente_selecionado]
        
        st.warning("⚠️ Atenção: Excluir o paciente também apagará todas as avaliações e reavaliações ligadas a ele de forma definitiva!")
        confirmar = st.checkbox("Estou ciente e quero prosseguir com a exclusão definitiva.")
        
        if st.button("❌ Confirmar Exclusão", type="primary", disabled=not confirmar):
            sucesso, mensagem = excluir_paciente_do_banco(id_paciente_exclusao)
            if sucesso:
                st.success(mensagem)
                st.rerun()
            else:
                st.error(mensagem)
        return

    # --- CONFIGURAÇÃO DOS VALORES PADRÃO ---
    id_paciente_edicao = None
    nome_padrao = ""
    data_padrao = date(1950, 1, 1)
    dias_padrao_idx = 0
    responsavel_padrao = ""
    telefone_padrao = ""
    
    if acao == "Editar Paciente Existente":
        opcoes_edicao = {f"{p[1]} (ID: {p[0]})": p[0] for p in todos_pacientes}
        paciente_selecionado = st.selectbox("Selecione o paciente que deseja modificar:", list(opcoes_edicao.keys()))
        id_paciente_edicao = opcoes_edicao[paciente_selecionado]
        
        # Encontra o paciente selecionado na lista para preencher os dados
        for p in todos_pacientes:
            if p[0] == id_paciente_edicao:
                nome_padrao = p[1]
                try:
                    data_padrao = datetime.strptime(p[2].split(" ")[0], "%Y-%m-%d").date()
                except:
                    try:
                        data_padrao = datetime.strptime(p[2], "%d/%m/%Y").date()
                    except:
                        data_padrao = date(1950, 1, 1)
                dias_padrao_idx = 1 if p[3] == "Terça e Quinta" else 0
                break
        
        # Busca responsável e telefone adicionais
        from database.db_manager import conectar_banco
        try:
            conn = conectar_banco()
            c = conn.cursor()
            c.execute("SELECT nome_responsavel, telefone FROM pacientes WHERE id = ?", (id_paciente_edicao,))
            extra = c.fetchone()
            conn.close()
            if extra:
                responsavel_padrao = extra[0] if extra[0] else ""
                telefone_padrao = extra[1] if extra[1] else ""
        except:
            pass

    # --- FORMULÁRIO (CADASTRO / EDIÇÃO) ---
    with st.form("form_paciente", clear_on_submit=False):
        st.markdown("### Dados do Paciente")
        nome_paciente = st.text_input("Nome Completo do Paciente *", value=nome_padrao)
        data_nasc = st.date_input("Data de Nascimento", value=data_padrao, min_value=date(1900, 1, 1), format="DD/MM/YYYY")
        dias_atividade = st.selectbox("Dia da semana de atividades *", ["Segunda e Quarta", "Terça e Quinta"], index=dias_padrao_idx)
        nome_responsavel = st.text_input("Nome do Responsável", value=responsavel_padrao)
        telefone_contato = st.text_input("Telefone de Contato (com DDD)", value=telefone_padrao)
        
        texto_botao = "Salvar Alterações" if acao == "Editar Paciente Existente" else "Cadastrar Paciente"
        botao_submeter = st.form_submit_button(texto_botao)
        
        if botao_submeter:
            if nome_paciente.strip() == "":
                st.error("O campo 'Nome Completo do Paciente' é obrigatório!")
            else:
                if acao == "Editar Paciente Existente":
                    sucesso, mensagem = atualizar_dados_paciente(
                        id_paciente_edicao, nome_paciente, data_nasc, dias_atividade, nome_responsavel, telefone_contato
                    )
                else:
                    sucesso, mensagem = salvar_novo_paciente(
                        nome_paciente, data_nasc, dias_atividade, nome_responsavel, telefone_contato
                    )
                
                if sucesso:
                    st.success(mensagem)
                    st.rerun()
                else:
                    st.error(mensagem)

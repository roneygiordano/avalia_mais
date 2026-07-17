# frontend/prontuario_view.py
import streamlit as st
from datetime import date
from backend.avaliacao import buscar_pacientes_por_dia
# Importa todas as funções necessárias do seu backend
from backend.prontuario import (
    salvar_nova_observacao, 
    listar_prontuario_por_paciente, 
    deletar_registro_prontuario  # 🗑️ Nova importação inclusa
)

def renderizar_tela_prontuario():
    """Desenha a interface de Prontuário e Evolução Clínica com filtro por dia"""
    st.subheader("📋 Prontuário Clínico e Evoluções")
    
    # 1. Filtro por dia de atendimento (Mantém o padrão da avaliação)
    dia_selecionado = st.selectbox(
        "Filtrar pacientes pelo dia de atendimento:", 
        ["Segunda e Quarta", "Terça e Quinta"],
        key="sb_dia_prontuario"
    )
    
    pacientes_filtrados = buscar_pacientes_por_dia(dia_semana=dia_selecionado)
    
    if not pacientes_filtrados:
        st.warning(f"Nenhum paciente cadastrado para os dias de: {dia_selecionado}.")
        return

    # 2. Organiza os pacientes encontrados no Selectbox
    opcoes_pacientes = {nome: id_banco for id_banco, nome in pacientes_filtrados}
    paciente_escolhido = st.selectbox(
        "Selecione o Paciente para abrir o prontuário:", 
        list(opcoes_pacientes.keys()), 
        key="sb_paciente_prontuario"
    )
    id_paciente_alvo = opcoes_pacientes[paciente_escolhido]
    
    st.write("---")
    st.markdown(f"### Paciente:\n**{paciente_escolhido}**")
    
    # 3. Formulário de lançamento da Nova Observação/Evolução
    with st.form("form_evolucao_clinica", clear_on_submit=True):
        
        # Campo de data exibindo o calendário no formato brasileiro DD/MM/AAAA
        data_atend = st.date_input("Data do Atendimento", value=date.today(), format="DD/MM/YYYY")
        
        nova_obs = st.text_area(
            "Observações Clínicas / Evolução do Paciente", 
            placeholder="Digite aqui o relato do atendimento de hoje..."
        )
        
        botao_salvar = st.form_submit_button("💾 Gravar Dados", type="primary")
            
        if botao_salvar:
            if nova_obs.strip() == "":
                st.warning("⚠️ Por favor, preencha o campo de observações antes de salvar.")
            else:
                # Transforma a data no padrão brasileiro texto igual você fez na avaliação
                data_ptbr = data_atend.strftime("%d/%m/%Y")
                
                sucesso, message = salvar_nova_observacao(id_paciente_alvo, data_ptbr, nova_obs)
                if sucesso:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
                    
    st.write("---")
    
    # 4. Exibição do Histórico Acumulado (Linha do Tempo) com Botão de Excluir por Linha
    st.markdown("### 📄 Linha do Tempo / Evoluções Anteriores")
    
    historico = listar_prontuario_por_paciente(id_paciente_alvo)
    
    if historico:
        for registro in historico:
            data_exibicao = registro.get("data_atendimento", "Sem data")
            texto_obs = registro.get("observacao", "")
            
            # Desenha o balão de histórico usando o chat_message do Streamlit
            with st.chat_message("user", avatar="📝"):
                # Cria duas colunas: uma larga para o texto e uma fina para o botão alinhado à direita
                col_texto, col_botao = st.columns([0.85, 0.15])
                
                with col_texto:
                    st.caption(f"**Atendimento em:** {data_exibicao}")
                    st.write(texto_obs)
                    
                with col_botao:
                    # Gera uma chave única combinando o ID e a data para evitar conflitos no Streamlit
                    chave_botao = f"del_{id_paciente_alvo}_{data_exibicao}"
                    
                    # Adiciona o botão vermelho "Excluir"
                    if st.button("🗑️ Excluir", key=chave_botao, type="secondary", help=f"Excluir registro de {data_exibicao}"):
                        sucesso_del, msg_del = deletar_registro_prontuario(id_paciente_alvo, data_exibicao)
                        if sucesso_del:
                            st.success(msg_del)
                            st.rerun()  # Recarrega a página para atualizar o histórico imediatamente
                        else:
                            st.error(msg_del)
    else:
        st.info("ℹ️ Nenhuma observação anterior registrada para este paciente.")

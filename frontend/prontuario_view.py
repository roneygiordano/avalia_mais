# frontend/prontuario_view.py
import streamlit as st
from datetime import date
# Importa a função que você já tem pronta no seu backend de avaliação para listar os pacientes
from backend.avaliacao import buscar_pacientes_por_dia
# Importa as novas funções criadas para o prontuário
from backend.prontuario import salvar_nova_observacao, listar_prontuario_por_paciente

def renderizar_tela_prontuario():
    """Desenha a interface de Prontuário e Evolução Clínica com filtro por dia"""
    st.subheader("📋 Prontuário Clínico e Evoluções")
    
    # 1. Filtro por dia de atendimento (Igual ao seu padrão da avaliação)
    dia_selecionado = st.selectbox(
        "Filtrar pacientes pelo dia de atendimento:", 
        ["Segunda e Quarta", "Terça e Quinta"],
        key="sb_dia_prontuario"
    )
    
    pacientes_filtrados = buscar_pacientes_por_dia(dia_selecionado)
    
    if not pacientes_filtrados:
        st.warning(f"Nenhum paciente cadastrado para os dias de: {dia_selecionado}.")
        return

    # 2. Organiza os pacientes encontrados no Selectbox
    opcoes_pacientes = {nome: id_banco for id_banco, nome in pacientes_filtrados}
    paciente_escolhido = st.selectbox("Selecione o Paciente para abrir o prontuário:", list(opcoes_pacientes.keys()), key="sb_paciente_prontuario")
    id_paciente_alvo = opcoes_pacientes[paciente_escolhido]
    
    st.write("---")
    st.markdown(f"### Paciente:\n**{paciente_escolhido}**")
    
    # 3. Formulário de lançamento da Nova Observação/Evolução
    with st.form("form_evolucao_clinica", clear_on_submit=True):
        
        # Campo de data exibindo o calendário forçando o formato brasileiro DD/MM/AAAA na tela
        data_atend = st.date_input("Data do Atendimento", value=date.today(), format="DD/MM/YYYY")
        
        nova_obs = st.text_area("Observações Clínicas / Evolução do Paciente", placeholder="Digite aqui o relato do atendimento de hoje...")
        
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
    
    # 4. Exibição do Histórico Acumulado (Linha do Tempo) logo abaixo do formulário
    st.markdown("### 📄 Linha do Tempo / Evoluções Anteriores")
    
    historico = listar_prontuario_por_paciente(id_paciente_alvo)
    
    if historico:
        # Exibe os registros acumulados. Como você usa string pt-br, 
        # eles aparecem exatamente como foram gravados
        for registro in historico:
            data_exibicao = registro.get("data_atendimento", "Sem data")
            texto_obs = registro.get("observacao", "")
            
            with st.chat_message("user", avatar="📝"):
                st.caption(f"**Atendimento em:** {data_exibicao}")
                st.write(texto_obs)
    else:
        st.info("ℹ️ Nenhuma observação anterior registrada para este paciente.")

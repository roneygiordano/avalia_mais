# frontend/avaliacao_view.py
import streamlit as st
from datetime import date
from backend.avaliacao import (
    buscar_pacientes_por_dia, 
    salvar_nova_avaliacao, 
    zerar_historico_do_paciente
)

def renderizar_tela_avaliacao():
    """Desenha a interface de lançamentos de Testes com o filtro por dia de atendimento"""
    st.subheader("⏱️ Registro de Avaliações e Reavaliações")
    
    # Filtro por dia de atendimento
    dia_selecionado = st.selectbox(
        "Filtrar pacientes pelo dia de atendimento:", 
        ["Segunda e Quarta", "Terça e Quinta"]
    )
    
    # Busca apenas os pacientes daquele dia específico
    pacientes_filtrados = buscar_pacientes_por_dia(dia_selecionado)
    
    if not pacientes_filtrados:
        st.warning(f"Nenhum paciente cadastrado para os dias de: {dia_selecionado}.")
        return

    # Organiza os pacientes encontrados em um formato amigável para o Selectbox
    opcoes_pacientes = {nome: id_banco for id_banco, nome in pacientes_filtrados}
    paciente_escolhido = st.selectbox("Selecione o Paciente para avaliar:", list(opcoes_pacientes.keys()))
    id_paciente_alvo = opcoes_pacientes[paciente_escolhido]
    
    st.write("---")
    st.markdown(f"### Paciente: **{paciente_escolhido}**")
    
    # Formulário de lançamento estruturado na ordem exata solicitada
    with st.form("form_testes_funcionais", clear_on_submit=True):
        
        # 1. Tipo de verificação aparece acima da data
        tipo_consulta = st.selectbox("Tipo de Verificação *", ["Avaliação", "Reavaliação"])
        
        # 2. O campo de data exibe o calendário forçando o formato brasileiro DD/MM/AAAA na tela
        data_aval = st.date_input("Data da Consulta", value=date.today(), format="DD/MM/YYYY")
        
        st.write("---")
        st.markdown("#### Testes Aplicados")
        
        col1, col2 = st.columns(2)
        with col1:
            t1 = st.number_input("Teste 1 — Sentar e Levantar (Repetições ou seg)", min_value=0.0, step=0.1, value=0.0)
            t2 = st.number_input("Teste 2 — Time Up and Go (Segundos)", min_value=0.0, step=0.1, value=0.0)
        with col2:
            t3 = st.number_input("Teste 3 — Tandem Stand Test (Segundos)", min_value=0.0, step=0.1, value=0.0)
            t4 = st.number_input("Teste 4 — Alcance Funcional Anterior - TAF (cm)", min_value=0.0, step=0.1, value=0.0)
            
        obs = st.text_area("Observações Clínicas / Evolutivas")
        
        botao_salvar = st.form_submit_button("💾 Gravar no Histórico", type="primary")
            
        if botao_salvar:
            data_ptbr = data_aval.strftime("%d/%m/%Y")
            sucesso, message = salvar_nova_avaliacao(id_paciente_alvo, data_ptbr, tipo_consulta, t1, t2, t3, t4, obs)
            if sucesso:
                st.success(message)
                st.rerun()
            else:
                st.error(message)
                
    # --- BLOCO VISUAL: PERMISSÃO PARA ZERAR A TABELA INTEIRA ---
    st.write("---")
    st.markdown("### 🧹 Zona de Perigo — Limpeza Geral da Tabela")
    st.markdown("Deseja apagar permanentemente **todos** os testes e avaliações já registrados na tabela do sistema?")
    
    confirmar_limpeza = st.checkbox("Confirmo que quero APAGAR TODOS os históricos de testes cadastrados no sistema.", key="chk_limpar_global")
    
    if st.button("❌ Apagar Todos os Testes Gravados", type="primary", disabled=not confirmar_limpeza, key="btn_limpar_global"):
        sucesso, msg = zerar_historico_do_paciente(id_paciente_alvo)
        if sucesso:
            st.success(msg)
            st.rerun()
        else:
            st.error(msg)

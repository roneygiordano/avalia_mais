# frontend/avaliacao_view.py
import streamlit as st
from datetime import date
from backend.avaliacao import buscar_pacientes_por_dia, salvar_nova_avaliacao

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
    st.markdown(f"### Ficha de Lançamento: **{paciente_escolhido}**")
    
    # Formulário de lançamento estruturado na ordem exata solicitada
    with st.form("form_testes_funcionais", clear_on_submit=True):
        
        # 1. ADEQUAÇÃO: O tipo de verificação aparece ACIMA da data
        tipo_consulta = st.selectbox("Tipo de Verificação *", ["Avaliação", "Reavaliação"])
        
        # 2. ADEQUAÇÃO: O campo de data agora exibe rigorosamente o formato DD/MM/AAAA (com barras)
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
        
        botao_salvar = st.form_submit_button("Gravar no Histórico")
        
        if botao_salvar:
            # Transforma o objeto de data no texto brasileiro 'DD/MM/AAAA' para salvar no banco
            data_ptbr = data_aval.strftime("%d/%m/%Y")
            
            sucesso, message = salvar_nova_avaliacao(id_paciente_alvo, data_ptbr, tipo_consulta, t1, t2, t3, t4, obs)
            if sucesso:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

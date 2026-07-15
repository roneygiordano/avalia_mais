# frontend/login_view.py

import streamlit as st
from backend.auth import gerenciar_sessao_login

def renderizar_tela_login():
    """Desenha a interface visual de login do Avalia+"""
    st.subheader("🔐 Área de Acesso")
    
    # Cria o formulário para organizar os campos e capturar o clique do botão
    with st.form("form_login"):
        usuario = st.text_input("Usuário / Login")
        senha = st.text_input("Senha", type="password")
        botao_entrar = st.form_submit_button("Entrar no Sistema")
        
        if botao_entrar:
            # Envia os dados para a nossa regra de negócio no backend
            if gerenciar_sessao_login(usuario, senha):
                st.success("Acesso liberado com sucesso!")
                st.rerun()  # Atualiza a tela para carregar o sistema principal
            else:
                st.error("Usuário ou senha inválidos. Tente novamente.")

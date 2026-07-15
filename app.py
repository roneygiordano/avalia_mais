# app.py
import os
import sys

# Garante que o Python encontre as pastas locais do projeto de forma absoluta
CAMINHO_RAIZ = os.path.dirname(os.path.abspath(__file__))
if CAMINHO_RAIZ not in sys.path:
    sys.path.insert(0, CAMINHO_RAIZ)

import streamlit as st
from database.db_manager import inicializar_tabelas
from frontend.login_view import renderizar_tela_login
from frontend.cadastro_view import renderizar_tela_cadastro
from frontend.avaliacao_view import renderizar_tela_avaliacao
from frontend.analise_view import renderizar_tela_analise  # IMPORTAÇÃO DA NOVA TELA
from backend.auth import realizar_logout

# 1. Configuração Inicial e Criação do Banco de Dados
st.set_page_config(page_title="Avalia+", layout="wide", page_icon="📈")

try:
    inicializar_tabelas()
except Exception as e:
    st.error(f"Erro crítico ao iniciar o banco de dados: {e}")

# 2. Gerenciamento do Estado de Sessão (Login)
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
if 'usuario_logado' not in st.session_state:
    st.session_state.usuario_logado = None

# --- CENÁRIO A: USUÁRIO NÃO LOGADO ---
if not st.session_state.autenticado:
    st.title("📈 Avalia+ — Controle de Acesso")
    renderizar_tela_login()

# --- CENÁRIO B: USUÁRIO AUTENTICADO ---
else:
    st.title("📈 Avalia+ — Painel de Controle")
    
    st.sidebar.success(f"Profissional: {st.session_state.usuario_logado}")
    if st.sidebar.button("🚪 Sair do Sistema"):
        realizar_logout()
        st.rerun()
        
    st.sidebar.write("---")
    
    # Menu lateral de Navegação do Avalia+
    menu = st.sidebar.radio(
        "Menu Principal:",
        ["1. Cadastro de Pacientes", "2. Avaliações e Reavaliações", "3. Análise Gráfica e PDF"]
    )

    # Roteamento das telas
    if menu == "1. Cadastro de Pacientes":
        renderizar_tela_cadastro()
        
    elif menu == "2. Avaliações e Reavaliações":
        renderizar_tela_avaliacao()
        
    elif menu == "3. Análise Gráfica e PDF":
        # ATIVANDO A TELA DE GRÁFICOS E IMPRESSÃO
        renderizar_tela_analise()

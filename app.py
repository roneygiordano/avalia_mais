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
from frontend.analise_view import renderizar_tela_analise
from frontend.prontuario_view import renderizar_tela_prontuario  # 📋 Importação da nova tela
from backend.auth import realizar_logout

# 1. Configuração Inicial e Criação do Banco de Dados
st.set_page_config(page_title="Avalia+", layout="wide", page_icon="📈")

# ADEQUAÇÃO RESPONSIVA: Garante que o título se adapte perfeitamente ao celular e computador
st.markdown("""
    <style>
        @import url('https://googleapis.com');
        
        html, body, [data-testid="stMarkdownContainer"], .stText, .stSidebar {
            font-family: 'Inter', 'Segoe UI', Helvetica, Arial, sans-serif !important;
        }
        
        /* Configuração Padrão para Computadores e Tablets */
        .topo-painel-controle {
            font-family: 'Inter', sans-serif;
            font-weight: 700;
            color: #0F172A;
            font-size: 32px;
            margin-bottom: 25px;
            margin-top: -10px;
        }
        
        /* Configuração Exclusiva para Celulares (Telas de até 768px de largura) */
        @media (max-width: 768px) {
            .topo-painel-controle {
                font-size: 22px !important; /* Diminui o texto para caber na tela do celular */
                margin-bottom: 15px !important;
                margin-top: 0px !important;
                line-height: 1.3 !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

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
    st.title("📈 Avalia+ ")
    renderizar_tela_login()

# --- CENÁRIO B: USUÁRIO AUTENTICADO ---
else:
    st.markdown('<div class="topo-painel-controle">📈 Avalia+ </div>', unsafe_allow_html=True)
    
    # Identificação do Profissional Logado e Botão de Logout na Barra Lateral
    st.sidebar.success(f"Profissional: {st.session_state.usuario_logado}")
    if st.sidebar.button("🚪 Sair do Sistema"):
        realizar_logout()
        st.rerun()
        
    st.sidebar.write("---")
    
    # Menu lateral de Navegação do Avalia+
    menu = st.sidebar.radio(
        "Menu Principal:",
        [
            "1. Cadastro de Pacientes", 
            "2. Avaliações e Reavaliações", 
            "3. Análise Gráfica e PDF",
            "4. Prontuários"  # 📋 Novo item adicionado aqui
        ]
    )

    # Roteamento das telas com base na escolha do menu
    if menu == "1. Cadastro de Pacientes":
        renderizar_tela_cadastro()
        
    elif menu == "2. Avaliações e Reavaliações":
        renderizar_tela_avaliacao()
        
    elif menu == "3. Análise Gráfica e PDF":
        renderizar_tela_analise()
        
    elif menu == "4. Prontuários":
        renderizar_tela_prontuario()  # 📋 Direciona para a nova view criada

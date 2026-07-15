# backend/auth.py

import streamlit as st

def obter_usuarios_cadastrados():
    """
    Retorna o dicionário de usuários válidos do sistema.
    Em uma etapa futura, isso pode ser migrado para uma tabela do banco de dados.
    """
    return {
        "admin": "admin123",      # Perfil Administrador
        "usuario1": "senha123",   # Segundo usuário cadastrado
        "usuario2": "senha456"    # Terceiro usuário cadastrado
    }

def validar_login(usuario, senha):
    """
    Verifica se as credenciais digitadas correspondem a um usuário válido.
    """
    usuarios = obter_usuarios_cadastrados()
    
    # Valida se o usuário existe e se a senha está correta
    if usuario in usuarios and usuarios[usuario] == senha:
        return True
    return False

def gerenciar_sessao_login(usuario, senha):
    """
    Altera o estado da sessão do Streamlit se o login for bem-sucedido.
    """
    if validar_login(usuario, senha):
        st.session_state.autenticado = True
        st.session_state.usuario_logado = usuario
        return True
    return False

def realizar_logout():
    """
    Limpa os dados da sessão do usuário atual.
    """
    st.session_state.autenticado = False
    st.session_state.usuario_logado = None

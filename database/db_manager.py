# database/db_manager.py
import sqlite3
import os
import requests
import base64
import streamlit as st

NOME_BANCO = "avalia_mais.db"

def buscar_dados_do_github():
    """Baixa a versão mais recente do banco de dados do GitHub se o Streamlit Cloud reiniciar"""
    if "TOKEN_GITHUB" not in st.secrets:
        return
        
    token = st.secrets["TOKEN_GITHUB"]
    repo = st.secrets["REPOSITORIO"]
    url = f"https://github.com{repo}/contents/{NOME_BANCO}"
    headers = {"Authorization": f"token {token}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        dados_json = response.json()
        conteudo_binario = base64.b64decode(dados_json["content"])
        with open(NOME_BANCO, "wb") as f:
            f.write(conteudo_binario)

def salvar_dados_no_github():
    """Faz o upload invisível e automático do banco de dados atualizado para o GitHub"""
    if "TOKEN_GITHUB" not in st.secrets or not os.path.exists(NOME_BANCO):
        return
        
    token = st.secrets["TOKEN_GITHUB"]
    repo = st.secrets["REPOSITORIO"]
    url = f"https://github.com{repo}/contents/{NOME_BANCO}"
    headers = {"Authorization": f"token {token}"}
    
    # Lê o arquivo do banco local
    with open(NOME_BANCO, "rb") as f:
        conteudo_banco = f.read()
    conteudo_base64 = base64.b64encode(conteudo_banco).decode("utf-8")
    
    # Verifica se o arquivo já existe no GitHub para pegar o código SHA de atualização
    sha = None
    response_get = requests.get(url, headers=headers)
    if response_get.status_code == 200:
        sha = response_get.json()["sha"]
        
    payload = {
        "message": "🔄 Atualização automática do banco de dados (Avalia+)",
        "content": conteudo_base64
    }
    if sha:
        payload["sha"] = sha
        
    # Envia o arquivo atualizado para o cofre do GitHub
    requests.put(url, json=payload, headers=headers)

def conectar_banco():
    """Conecta de forma rápida e segura ao banco de dados interno"""
    return sqlite3.connect(NOME_BANCO, check_same_thread=False)

def inicializar_tabelas():
    """Cria a estrutura de tabelas e puxa o backup do GitHub se necessário"""
    # 1. Tenta resgatar os dados salvos no GitHub antes de iniciar
    if not os.path.exists(NOME_BANCO):
        try: buscar_dados_do_github()
        except: pass

    conn = conectar_banco()
    cursor = conn.cursor()
    
    # Tabela de Pacientes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pacientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        data_nascimento TEXT NOT NULL,
        dias_atividade TEXT NOT NULL,
        nome_responsavel TEXT,
        telefone TEXT
    )
    """)
    
    # Tabela de Avaliações
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS avaliacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        data_avaliacao TEXT NOT NULL,
        tipo_consulta TEXT DEFAULT 'Avaliação',
        teste_sentar_levantar REAL,
        teste_tug REAL,
        teste_tandem REAL,
        teste_taf REAL,
        observacoes TEXT,
        FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
    )
    """)
    
    conn.commit()
    conn.close()

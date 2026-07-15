# frontend/analise_view.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from fpdf import FPDF
from backend.paciente import listar_todos_pacientes
from backend.avaliacao import buscar_historico_paciente

def renderizar_tela_analise():
    st.subheader("📊 Análise Gráfica e Relatórios (PDF)")
    
    todos_pacientes = listar_todos_pacientes()
    if not todos_pacientes:
        st.warning("Nenhum paciente cadastrado no sistema para análise.")
        return
        
    opcoes_pacientes = {f"{p[1]} (ID: {p[0]})": p[0] for p in todos_pacientes}
    paciente_selecionado = st.selectbox("Selecione o Paciente para visualizar a evolução:", list(opcoes_pacientes.keys()))
    id_paciente = opcoes_pacientes[paciente_selecionado]
    nome_paciente = paciente_selecionado.split(" (ID:")[0]
    
    historico = buscar_historico_paciente(id_paciente)
    
    if not historico:
        st.info(f"O paciente {nome_paciente} ainda não possui nenhuma avaliação registrada.")
        return
        
    # --- PROCESSAMENTO SEGURO DOS DADOS ---
    dados_limpos = []
    for reg in historico:
        lista_reg = list(reg)
        
        # Tratamento para registros antigos (com 6 colunas) injetando o tipo padrão
        if len(lista_reg) == 6:
            lista_reg.insert(1, "Avaliação")
            
        data_orig = str(lista_reg[0])
        
        # Converte qualquer formato de data do banco para ordenar no tempo
        data_objeto = None
        for formato in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                data_objeto = datetime.strptime(data_orig.split(" ")[0], formato)
                break
            except:
                pass
                
        if data_objeto is None:
            data_objeto = datetime(2000, 1, 1)
            
        lista_reg.append(data_objeto)
        dados_limpos.append(lista_reg)
        
    # Criamos o DataFrame bruto e ordenamos cronologicamente de forma estrita
    colunas_bruto = ["Data_Texto", "Tipo", "Sentar_Levantar", "TUG", "Tandem", "TAF", "Obs", "Data_Objeto"]
    df_bruto = pd.DataFrame(dados_limpos, columns=colunas_bruto)
    df_bruto = df_bruto.sort_values(by="Data_Objeto")
    
    # --- MONTAGEM DA MATRIZ DA TABELA HORIZONTAL ---
    # O primeiro item da lista abaixo dita o nome da linha 1 fixa!
    matriz_dados = {
        "Testes Aplicados": [
            "Avaliação / Reavaliação",  # <-- Linha 1 Fixa!
            "Sentar / Levantar (Força, Equilíbrio e Transição)",
            "Time Up and Go (Equilíbrio dinâmico e mobilidade funcional)",
            "Tandem Stand Test (Equilíbrio Estático)",
            "Alcance Funcional Anterior (TAF - Deslocar / Estabilidade anterior)"
        ]
    }
    
    # Varre as consultas ordenadas e adiciona cada data no formato DD/MM/AAAA como coluna
    for _, linha in df_bruto.iterrows():
        # Força o cabeçalho da coluna a ser estritamente DD/MM/AAAA com barras
        data_cabecalho_br = linha["Data_Objeto"].strftime("%d/%m/%Y")
        
        # Formatações das strings com vírgula e aspas/centímetros
        try: s_l = f"{float(linha['Sentar_Levantar']):,.2f}\"".replace(".", ",")
        except: s_l = str(linha['Sentar_Levantar'])
        
        try: tug = f"{float(linha['TUG']):,.2f}\"".replace(".", ",")
        except: tug = str(linha['TUG'])
        
        try: tandem = f"{int(float(linha['Tandem']))}\""
        except: tandem = str(linha['Tandem'])
        
        try: taf = f"{int(float(linha['TAF']))} cm"
        except: taf = str(linha['TAF'])
        
        # Associa os dados à coluna de data na ordem vertical exata da planilha
        matriz_dados[data_cabecalho_br] = [
            str(linha["Tipo"]), # Vai para a Linha 1 (Avaliação / Reavaliação)
            s_l,                # Linha 2
            tug,                # Linha 3
            tandem,             # Linha 4
            taf                 # Linha 5
        ]
        
    df_planilha = pd.DataFrame(matriz_dados)
    
    # --- RENDERIZAÇÃO NA TELA ---
    st.markdown(f"### 📋 Ficha de Avaliações/Reavliações — Beneficiário: **{nome_paciente}**")
    st.dataframe(df_planilha, use_container_width=True, hide_index=True)
    
    st.write("---")
    
    # --- BLOCO DE GRÁFICOS ---
    st.markdown("### 📈 Gráfico Comparativo de Evolução")
    testes_grafico = {
        "Teste 1 — Sentar e Levantar": "Sentar_Levantar",
        "Teste 2 — Time Up and Go": "TUG",
        "Teste 3 — Tandem Stand Test": "Tandem",
        "Teste 4 — Alcance Funcional Anterior": "TAF"
    }
    teste_escolhido = st.selectbox("Escolha o teste para projetar no gráfico:", list(testes_grafico.keys()))
    coluna_grafico = testes_grafico[teste_escolhido]
    
    df_bruto[coluna_grafico] = pd.to_numeric(df_bruto[coluna_grafico], errors='coerce')
    
    fig = px.line(df_bruto, x="Data_Objeto", y=coluna_grafico, markers=True,
                  title=f"Evolução Temporal: {teste_escolhido}",
                  labels={"Data_Objeto": "Linha do Tempo (Cronológica)", coluna_grafico: "Resultado Obtido"})
    fig.update_layout(xaxis=dict(tickformat="%d/%m/%Y"))
    st.plotly_chart(fig, use_container_width=True)

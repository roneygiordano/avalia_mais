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
        
    # --- AJUSTE DE COMPATIBILIDADE PARA DADOS ANTIGOS E NOVOS ---
    dados_ajustados = []
    for registro in historico:
        lista_reg = list(registro)
        # Se o registro tiver apenas 6 elementos (antigo, sem o campo Tipo)
        if len(lista_reg) == 6:
            # Injeta 'Avaliação' como padrão na segunda posição
            lista_reg.insert(1, "Avaliação")
        dados_ajustados.append(lista_reg)
        
    colunas = ["Data", "Tipo", "Sentar / Levantar", "Time Up and Go", "Tandem Stand Test", "Alcance Funcional Anterior", "Observações"]
    df_bruto = pd.DataFrame(dados_ajustados, columns=colunas)
    
    # Ordenação cronológica
    def tentar_converter_data(d_str):
        for f in ("%d/%m/%Y", "%Y-%m-%d"):
            try: return datetime.strptime(d_str, f)
            except: pass
        return datetime(2000, 1, 1)
    df_bruto["Data_Ordenacao"] = df_bruto["Data"].apply(tentar_converter_data)
    df_bruto = df_bruto.sort_values(by="Data_Ordenacao")
    
    # --- TRANSPOSIÇÃO HORIZONTAL ---
    matriz_dados = {
        "Testes Aplicados": [
            "Avaliação / Reavaliação",
            "Sentar / Levantar (Força, Equilíbrio e Transição)",
            "Time Up and Go (Equilíbrio dinâmico e mobilidade funcional)",
            "Tandem Stand Test (Equilíbrio Estático)",
            "Alcance Funcional Anterior (TAF - Deslocar / Estabilidade anterior)"
        ]
    }
    
    for _, linha in df_bruto.iterrows():
        data_coluna = linha["Data"]
        matriz_dados[data_coluna] = [
            str(linha["Tipo"]),
            f"{linha['Sentar / Levantar']:,.2f}\"".replace(".", ","),
            f"{linha['Time Up and Go']:,.2f}\"".replace(".", ","),
            f"{int(linha['Tandem Stand Test'])}\"",
            f"{int(linha['Alcance Funcional Anterior'])} cm"
        ]
        
    df_planilha = pd.DataFrame(matriz_dados)
    
    st.markdown(f"### 📋 Ficha de Avaliações/Reavaliações — Beneficiário: **{nome_paciente}**")
    st.dataframe(df_planilha, use_container_width=True, hide_index=True)
    
    st.write("---")
    
    # --- BLOCO DE GRÁFICOS ---
    st.markdown("### 📈 Gráfico Comparativo de Evolução")
    testes_grafico = {
        "Teste 1 — Sentar e Levantar": "Sentar / Levantar",
        "Teste 2 — Time Up and Go": "Time Up and Go",
        "Teste 3 — Tandem Stand Test": "Tandem Stand Test",
        "Teste 4 — Alcance Funcional Anterior": "Alcance Funcional Anterior"
    }
    teste_escolhido = st.selectbox("Escolha o teste para projetar no gráfico:", list(testes_grafico.keys()))
    coluna_grafico = testes_grafico[teste_escolhido]
    
    fig = px.line(df_bruto, x="Data_Ordenacao", y=coluna_grafico, markers=True,
                  title=f"Evolução Temporal: {teste_escolhido}",
                  labels={"Data_Ordenacao": "Datas das Avaliações", coluna_grafico: "Resultado"})
    fig.update_layout(xaxis=dict(tickformat="%d/%m/%Y"))
    st.plotly_chart(fig, use_container_width=True)

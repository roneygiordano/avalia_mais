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
        
    colunas = ["Data_Original", "Sentar / Levantar", "Time Up and Go", "Tandem Stand Test", "Alcance Funcional Anterior", "Observações"]
    df_bruto = pd.DataFrame(historico, columns=colunas)
    
    # --- FUNÇÃO INTELIGENTE PARA CONVERTER E ORDENAR AS DATAS ---
    def tentar_converter_para_data_real(d_str):
        for f in ("%d/%m/%Y", "%Y-%m-%d"):
            try: return datetime.strptime(d_str, f)
            except: pass
        return datetime(2000, 1, 1)
        
    # Cria uma coluna de data real apenas para ordenação interna do banco
    df_bruto["Data_Ordenacao"] = df_bruto["Data_Original"].apply(tentar_converter_para_data_real)
    df_bruto = df_bruto.sort_values(by="Data_Ordenacao")
    
    # Cria a coluna de texto no formato definitivo DD/MM/AAAA
    df_bruto["Data_BR"] = df_bruto["Data_Ordenacao"].apply(lambda x: x.strftime("%d/%m/%Y"))
    
    # --- MONTAGEM DA TABELA HORIZONTAL IDENTICA À PLANILHA ---
    matriz_dados = {
        "Testes Aplicados": [
            "Sentar / Levantar (Força, Equilíbrio e Transição)",
            "Time Up and Go (Equilíbrio dinâmico e mobilidade funcional)",
            "Tandem Stand Test (Equilíbrio Estático)",
            "Alcance Funcional Anterior (TAF - Deslocar / Estabilidade anterior)"
        ]
    }
    
    # Adiciona cada data formatada como uma coluna horizontal na tabela
    for _, linha in df_bruto.iterrows():
        data_coluna = linha["Data_BR"]
        matriz_dados[data_coluna] = [
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
                  labels={"Data_Ordenacao": "Linha do Tempo (Cronológica)", coluna_grafico: "Resultado Obtido"})
    
    # Força as marcações do gráfico a exibirem no formato brasileiro
    fig.update_layout(xaxis=dict(tickformat="%d/%m/%Y"))
    st.plotly_chart(fig, use_container_width=True)
    
    # --- BLOCO DE PDF ---
    st.write("---")
    if st.button("📄 Gerar Relatório em PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(190, 10, "SISTEMA AVALIA+ — FICHA EVOLUTIVA", ln=True, align="C")
        pdf.set_font("Arial", "", 11)
        pdf.cell(190, 8, f"Beneficiario: {nome_paciente}", ln=True)
        pdf.ln(5)
        
        for _, col in df_planilha.iterrows():
            texto_linha = f"{col['Testes Aplicados']}: "
            for data in list(df_planilha.columns)[1:]:
                texto_linha += f"[{data}: {col[data]}] "
            pdf.multi_cell(190, 6, texto_linha)
            pdf.ln(2)
            
        pdf_output = pdf.output(dest='S').encode('latin1', errors='ignore')
        st.download_button(label="⬇️ Baixar Ficha PDF", data=pdf_output, 
                           file_name=f"Ficha_{nome_paciente.replace(' ', '_')}.pdf", mime="application/pdf")

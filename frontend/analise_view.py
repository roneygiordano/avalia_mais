# frontend/analise_view.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from backend.paciente import listar_todos_pacientes
from backend.avaliacao import buscar_historico_paciente

def renderizar_tela_analise():
    st.subheader("📊 Análise Gráfica e Relatórios")
    
    todos_pacientes = listar_todos_pacientes()
    if not todos_pacientes:
        st.warning("Nenhum paciente cadastrado no sistema para análise.")
        return
        
    opcoes_pacientes = {f"{p[1]} (ID: {p[0]})": p[0] for p in todos_pacientes}
    paciente_selecionado = st.selectbox("Selecione o Paciente para visualizar a evolução:", list(opcoes_pacientes.keys()))
    id_paciente = opcoes_pacientes[paciente_selecionado]
    nome_paciente = paciente_selecionado.split(" (ID:")
    
    historico = buscar_historico_paciente(id_paciente)
    
    if not historico:
        st.info(f"O paciente {nome_paciente} ainda não possui nenhuma avaliação registrada.")
        return
        
    # --- PROCESSAMENTO SEGURO POR POSIÇÃO DOS DADOS ---
    dados_limpos = []
    for reg in historico:
        lista_reg = list(reg)
        
        # Tratamento para registros antigos (com 6 colunas) injetando o Tipo na posição 1
        if len(lista_reg) == 6:
            lista_reg.insert(1, "Avaliação")
            
        data_texto = str(lista_reg[0]).strip()
        
        # Converte a data de texto para objeto real para ordenar no tempo
        data_objeto = None
        for formato in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                data_objeto = datetime.strptime(data_texto, formato)
                break
            except:
                pass
                
        if data_objeto is None:
            data_objeto = datetime(2000, 1, 1)
            
        # Adiciona os itens de suporte no final do registro
        lista_reg.append(data_objeto.strftime("%d/%m/%Y")) # Data_BR
        lista_reg.append(data_objeto)                      # Data_Objeto
        dados_limpos.append(lista_reg)
        
    colunas_bruto = ["Data_Texto", "Tipo", "Sentar_Levantar", "TUG", "Tandem", "TAF", "Obs", "Data_BR", "Data_Objeto"]
    df_bruto = pd.DataFrame(dados_limpos, columns=colunas_bruto)
    df_bruto = df_bruto.sort_values(by="Data_Objeto")
    
    # --- MONTAGEM DA MATRIZ DA TABELA HORIZONTAL ---
    matriz_dados = {
        "Testes Aplicados": [
            "Avaliação / Reavaliação",
            "Sentar / Levantar (Força, Equilíbrio e Transição)",
            "Time Up and Go (Equilíbrio dinâmico e mobilidade funcional)",
            "Tandem Stand Test (Equilíbrio Estático)",
            "Alcance Funcional Anterior (TAF - Deslocar / Estabilidade anterior)"
        ]
    }
    
    for _, column_data in df_bruto.iterrows():
        data_cabecalho_br = str(column_data["Data_BR"])
        
        try: s_l = f"{float(column_data['Sentar_Levantar']):,.2f}\"".replace(".", ",")
        except: s_l = str(column_data['Sentar_Levantar'])
        
        try: tug = f"{float(column_data['TUG']):,.2f}\"".replace(".", ",")
        except: tug = str(column_data['TUG'])
        
        try: tandem = f"{int(float(column_data['Tandem']))}\""
        except: tandem = str(column_data['Tandem'])
        
        try: taf = f"{int(float(column_data['TAF']))} cm"
        except: taf = str(column_data['TAF'])
        
        matriz_dados[data_cabecalho_br] = [
            str(column_data["Tipo"]),
            s_l,
            tug,
            tandem,
            taf
        ]
        
    df_planilha = pd.DataFrame(matriz_dados)
    
    st.markdown(f"### 📋 Ficha de Avaliações/Reavaliações — Beneficiário: **{nome_paciente}**")
    st.dataframe(df_planilha, use_container_width=True, hide_index=True)
    
    # --- PAINEL DE EVOLUÇÃO (OBSERVAÇÕES CLÍNICAS INTELIGENTES) ---
    st.write("---")
    st.markdown("### 📝 Prontuário / Observações Clínicas por Data")
    
    # Ordena as observações textuais mostrando as consultas mais recentes no topo
    df_obs_invertido = df_bruto.sort_values(by="Data_Objeto", ascending=False)
    
    # Variável para controlar se alguma observação válida foi exibida
    exibiu_alguma_obs = False
    
    for _, column_data in df_obs_invertido.iterrows():
        data_card = str(column_data["Data_BR"])
        tipo_card = str(column_data["Tipo"])
        texto_obs = str(column_data["Obs"]).strip()
        
        # ADEQUAÇÃO: O bloco IF agora descarta textos vazios, nulos ou a palavra 'None'
        if texto_obs and texto_obs != "None" and texto_obs != "":
            exibiu_alguma_obs = True
            # Só desenha a caixa de texto azul se houver conteúdo real!
            st.info(f"📅 **{data_card} — {tipo_card}**\n\n{texto_obs}")
            
    # Se o laço terminou e nenhuma data possuía observações escritas
    if not exibiu_alguma_obs:
        st.write("*Nenhuma anotação clínica foi registrada no histórico deste paciente.*")
            
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

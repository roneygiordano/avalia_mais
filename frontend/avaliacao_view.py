# Trecho final do arquivo frontend/avaliacao_view.py

    # --- BLOCO VISUAL: PERMISSÃO PARA ZERAR A TABELA INTEIRA ---
    st.write("---")
    st.markdown("### 🧹 Zona de Perigo — Limpeza Geral da Tabela")
    st.markdown("Deseja apagar permanentemente **todos** os testes e avaliações já registrados na tabela do sistema?")
    
    confirmar_limpeza = st.checkbox("Confirmo que quero APAGAR TODOS os históricos de testes cadastrados no sistema.", key="chk_limpar_global")
    
    if st.button("❌ Apagar Todos os Testes Gravados", type="primary", disabled=not confirmar_limpeza, key="btn_limpar_global"):
        # Passamos o ID apenas por compatibilidade, a função vai limpar a tabela inteira
        sucesso, msg = zerar_historico_do_paciente(id_paciente_alvo)
        if sucesso:
            st.success(msg)
            st.rerun()
        else:
            st.error(msg)

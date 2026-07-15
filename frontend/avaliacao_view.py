# Trecho final do arquivo frontend/avaliacao_view.py

    # --- BLOCO VISUAL: PERMISSÃO PARA APAGAR TODOS OS DADOS JÁ INSERIDOS ---
    st.write("---")
    st.markdown("### 🧹 Zona de Perigo — Limpeza de Histórico")
    st.markdown(f"Deseja apagar permanentemente **todas** as avaliações registradas para **{paciente_escolhido}**?")
    
    # Trava de segurança para evitar cliques acidentais
    confirmar_limpeza = st.checkbox(f"Confirmo que quero APAGAR todo o histórico de testes de {paciente_escolhido}.", key="chk_limpar")
    
    # Botão com tipo de ação forçada e chave única (key) para destravar o clique
    if st.button("❌ Apagar Todos os Testes Gravados", type="primary", disabled=not confirmar_limpeza, key="btn_limpar_definitivo"):
        sucesso, msg = zerar_historico_do_paciente(id_paciente_alvo)
        if sucesso:
            # Exibe a mensagem de sucesso na tela de forma destacada
            st.success(msg)
            # Aguarda um milissegundo e força a atualização limpa da página
            st.rerun()
        else:
            st.error(msg)

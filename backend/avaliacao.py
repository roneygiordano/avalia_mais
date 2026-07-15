# Trecho final do arquivo backend/avaliacao.py

def zerar_historico_do_paciente(paciente_id):
    """Apaga todas as avaliações e reavaliações gravadas para o paciente, limpando sua ficha"""
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM avaliacoes WHERE paciente_id = ?", (int(paciente_id),))
        conn.commit()
        conn.close()
        # ADEQUAÇÃO: Mensagem exata solicitada por você!
        return True, "Todos os dados do Paciente foram apagados"
    except Exception as e:
        return False, f"Erro ao limpar histórico: {e}"

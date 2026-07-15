# Adicione isso no final do arquivo backend/avaliacao.py

def zerar_historico_do_paciente(paciente_id):
    """Apaga todas as avaliações e reavaliações gravadas para o paciente, limpando sua ficha"""
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        
        # Remove apenas as linhas de testes ligadas ao ID deste paciente
        cursor.execute("DELETE FROM avaliacoes WHERE paciente_id = ?", (int(paciente_id),))
        
        conn.commit()
        conn.close()
        return True, "Todo o histórico de testes do paciente foi apagado com sucesso!"
    except Exception as e:
        return False, f"Erro ao limpar histórico: {e}"

# backend/avaliacao.py
from database.db_manager import conectar_banco, salvar_dados_no_github

def buscar_pacientes_por_dia(dia_semana):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM pacientes WHERE dias_atividade = ? ORDER BY nome ASC", (dia_semana,))
        dados = cursor.fetchall()
        conn.close()
        return dados
    except Exception:
        return []

def salvar_nova_avaliacao(paciente_id, data_aval, tipo_consulta, t1, t2, t3, t4, obs):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id FROM avaliacoes WHERE paciente_id = ? AND data_avaliacao = ?
        """, (int(paciente_id), str(data_aval)))
        resultado = cursor.fetchone()
        
        if resultado:
            cursor.execute("""
                UPDATE avaliacoes 
                SET tipo_consulta = ?, teste_sentar_levantar = ?, teste_tug = ?, 
                    teste_tandem = ?, teste_taf = ?, observacoes = ?
                WHERE id = ?
            """, (tipo_consulta, float(t1), float(t2), float(t3), float(t4), obs, resultado[0]))
            mensagem_retorno = "Dados da data atualizados com sucesso!"
        else:
            cursor.execute("""
                INSERT INTO avaliacoes (
                    paciente_id, data_avaliacao, tipo_consulta,
                    teste_sentar_levantar, teste_tug, teste_tandem, teste_taf, observacoes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (int(paciente_id), str(data_aval), tipo_consulta, float(t1), float(t2), float(t3), float(t4), obs))
            mensagem_retorno = "Nova avaliação gravada com sucesso!"
            
        conn.commit()
        conn.close()
        salvar_dados_no_github()
        return True, mensagem_retorno
    except Exception as e:
        return False, f"Erro ao processar gravação: {e}"

def buscar_historico_paciente(paciente_id):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT data_avaliacao, tipo_consulta, teste_sentar_levantar, teste_tug, teste_tandem, teste_taf, observacoes
            FROM avaliacoes WHERE paciente_id = ? ORDER BY data_avaliacao ASC
        """, (int(paciente_id),))
        dados = cursor.fetchall()
        conn.close()
        return dados
    except Exception:
        return []

def zerar_historico_do_paciente(paciente_id):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM avaliacoes")
        conn.commit()
        conn.close()
        salvar_dados_no_github()
        return True, "Todos os dados do Paciente foram apagados"
    except Exception as e:
        return False, f"Erro ao limpar tabela: {e}"

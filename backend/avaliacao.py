# backend/avaliacao.py
from database.db_manager import conectar_banco

def buscar_pacientes_por_dia(dia_semana):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM public.pacientes WHERE dias_atividade = %s ORDER BY nome ASC", (dia_semana,))
        dados = cursor.fetchall()
        cursor.close()
        conn.close()
        return dados
    except Exception:
        return []

def salvar_nova_avaliacao(paciente_id, data_aval, tipo_consulta, t1, t2, t3, t4, obs):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        
        # Verifica se já existe o registro na mesma data
        cursor.execute("""
            SELECT id FROM public.avaliacoes 
            WHERE paciente_id = %s AND data_avaliacao = %s
        """, (int(paciente_id), str(data_aval)))
        resultado = cursor.fetchone()
        
        if resultado:
            id_reg = resultado[0]
            cursor.execute("""
                UPDATE public.avaliacoes 
                SET tipo_consulta = %s, teste_sentar_levantar = %s, teste_tug = %s, 
                    teste_tandem = %s, teste_taf = %s, observacoes = %s
                WHERE id = %s
            """, (tipo_consulta, float(t1), float(t2), float(t3), float(t4), obs, id_reg))
            mensagem_retorno = "Dados atualizados na nuvem!"
        else:
            cursor.execute("""
                INSERT INTO public.avaliacoes (
                    paciente_id, data_avaliacao, tipo_consulta,
                    teste_sentar_levantar, teste_tug, teste_tandem, teste_taf, observacoes
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (int(paciente_id), str(data_aval), tipo_consulta, float(t1), float(t2), float(t3), float(t4), obs))
            mensagem_retorno = "Nova avaliação gravada na nuvem!"
            
        conn.commit()
        cursor.close()
        conn.close()
        return True, mensagem_retorno
    except Exception as e:
        return False, f"Erro ao processar gravação: {e}"

def buscar_historico_paciente(paciente_id):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT data_avaliacao, tipo_consulta, teste_sentar_levantar, teste_tug, teste_tandem, teste_taf, observacoes
            FROM public.avaliacoes WHERE paciente_id = %s ORDER BY data_avaliacao ASC
        """, (int(paciente_id),))
        dados = cursor.fetchall()
        cursor.close()
        conn.close()
        return dados
    except Exception:
        return []

def zerar_historico_do_paciente(paciente_id):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM public.avaliacoes")
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Todos os dados do Paciente foram apagados"
    except Exception as e:
        return False, f"Erro ao limpar tabela: {e}"

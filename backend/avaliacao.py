# backend/avaliacao.py
from database.db_manager import conectar_banco

def buscar_pacientes_por_dia(dia_semana):
    """Busca os pacientes filtrados pelo dia de atendimento"""
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
    """
    Grava os resultados dos testes. 
    Se a data já existir para este paciente, atualiza os dados existentes (não duplica a coluna).
    """
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        
        # Garante a compatibilidade da coluna caso seja o SQLite local
        try:
            cursor.execute("ALTER TABLE avaliacoes ADD COLUMN tipo_consulta TEXT DEFAULT 'Avaliação'")
        except:
            pass
            
        # 1. ADEQUAÇÃO: Verifica se já existe um registro para este PACIENTE nesta DATA
        cursor.execute("""
            SELECT id FROM avaliacoes 
            WHERE paciente_id = ? AND data_avaliacao = ?
        """, (int(paciente_id), str(data_aval)))
        registro_existente = cursor.fetchone()
        
        if registro_existente:
            # Se já existe, faz a ALTERAÇÃO dos dados na mesma coluna
            id_registro = registro_existente[0]
            cursor.execute("""
                UPDATE avaliacoes 
                SET tipo_consulta = ?, teste_sentar_levantar = ?, teste_tug = ?, 
                    teste_tandem = ?, teste_taf = ?, observacoes = ?
                WHERE id = ?
            """, (tipo_consulta, float(t1), float(t2), float(t3), float(t4), obs, id_registro))
            mensagem_retorno = "Dados da data atualizados com sucesso (coluna mantida)!"
        else:
            # Se não existe, INSERE dados novos gerando uma nova coluna
            cursor.execute("""
                INSERT INTO avaliacoes (
                    paciente_id, data_avaliacao, tipo_consulta,
                    teste_sentar_levantar, teste_tug, teste_tandem, teste_taf, observacoes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (paciente_id, str(data_aval), tipo_consulta, float(t1), float(t2), float(t3), float(t4), obs))
            mensagem_retorno = "Nova avaliação gravada com sucesso (nova coluna criada)!"
            
        conn.commit()
        conn.close()
        return True, mensagem_retorno
    except Exception as e:
        return False, f"Erro ao processar gravação: {e}"

def buscar_historico_paciente(paciente_id):
    """Busca o histórico completo incluindo a coluna tipo_consulta"""
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        
        try:
            cursor.execute("ALTER TABLE avaliacoes ADD COLUMN tipo_consulta TEXT DEFAULT 'Avaliação'")
            conn.commit()
        except:
            pass
            
        cursor.execute("""
            SELECT data_avaliacao, tipo_consulta, teste_sentar_levantar, teste_tug, teste_tandem, teste_taf, observacoes
            FROM avaliacoes WHERE paciente_id = ? ORDER BY data_avaliacao ASC
        """, (paciente_id,))
        dados = cursor.fetchall()
        conn.close()
        return dados
    except Exception:
        return []

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
    """Grava os resultados incluindo explicitamente o tipo_consulta"""
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        
        # Garante que a tabela tenha a coluna tipo_consulta (caso use SQLite local)
        try:
            cursor.execute("ALTER TABLE avaliacoes ADD COLUMN tipo_consulta TEXT DEFAULT 'Avaliação'")
        except:
            pass # Se a coluna já existir, ignora o erro e continua
            
        cursor.execute("""
            INSERT INTO avaliacoes (
                paciente_id, data_avaliacao, tipo_consulta,
                teste_sentar_levantar, teste_tug, teste_tandem, teste_taf, observacoes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (paciente_id, str(data_aval), tipo_consulta, float(t1), float(t2), float(t3), float(t4), obs))
        conn.commit()
        conn.close()
        return True, "Registro salvo com sucesso!"
    except Exception as e:
        return False, f"Erro ao salvar no banco: {e}"

def buscar_historico_paciente(paciente_id):
    """Busca o histórico completo incluindo a coluna tipo_consulta"""
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        
        # Tentativa de garantir compatibilidade estrutural
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

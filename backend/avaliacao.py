# backend/avaliacao.py
from database.db_manager import conectar_banco

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

def salvar_nova_avaliacao(paciente_id, data_aval, t1, t2, t3, t4, obs):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO avaliacoes (paciente_id, data_avaliacao, teste_sentar_levantar, teste_tug, teste_tandem, teste_taf, observacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (paciente_id, str(data_aval), t1, t2, t3, t4, obs))
        conn.commit()
        conn.close()
        return True, "Avaliação registrada!"
    except Exception as e:
        return False, f"Erro: {e}"

def buscar_historico_paciente(paciente_id):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT data_avaliacao, teste_sentar_levantar, teste_tug, teste_tandem, teste_taf, observacoes
            FROM avaliacoes WHERE paciente_id = ? ORDER BY data_avaliacao ASC
        """, (paciente_id,))
        dados = cursor.fetchall()
        conn.close()
        return dados
    except Exception:
        return []

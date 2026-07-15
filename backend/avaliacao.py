# backend/avaliacao.py
from database.db_manager import conectar_banco

def buscar_pacientes_por_dia(dia_semana):
    """Busca no banco de dados apenas os pacientes matriculados no dia selecionado"""
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, nome FROM pacientes WHERE dias_atividade = ? ORDER BY nome ASC", 
            (dia_semana,)
        )
        dados = cursor.fetchall()
        conn.close()
        return dados # Retorna uma lista de tuplas [(id, nome), (id, nome)...]
    except Exception:
        return []

def salvar_nova_avaliacao(paciente_id, data_aval, t1, t2, t3, t4, obs):
    """Grava os resultados dos 4 testes funcionais no histórico do paciente"""
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO avaliacoes (
                paciente_id, data_avaliacao, teste_sentar_levantar, 
                teste_tug, teste_tandem, teste_taf, observacoes
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (paciente_id, str(data_aval), t1, t2, t3, t4, obs))
        
        conn.commit()
        conn.close()
        return True, "Avaliação registrada com sucesso!"
    except Exception as e:
        return False, f"Erro ao salvar avaliação: {e}"

def buscar_historico_paciente(paciente_id):
    """Busca todas as avaliações de um paciente específico ordenadas por data"""
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT data_avaliacao, teste_sentar_levantar, teste_tug, teste_tandem, teste_taf, observacoes
            FROM avaliacoes 
            WHERE paciente_id = ? 
            ORDER BY data_avaliacao ASC
        """, (paciente_id,))
        dados = cursor.fetchall()
        conn.close()
        return dados # Retorna lista de avaliações [(data, t1, t2, t3, t4, obs)...]
    except Exception:
        return []

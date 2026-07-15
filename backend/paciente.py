# backend/paciente.py
from database.db_manager import conectar_banco

def salvar_novo_paciente(nome, data_nasc, dias_atividade, responsavel, telefone):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        # No Postgres usamos %s no lugar das interrogações (?)
        cursor.execute("""
            INSERT INTO public.pacientes (nome, data_nascimento, dias_atividade, nome_responsavel, telefone)
            VALUES (%s, %s, %s, %s, %s)
        """, (nome, str(data_nasc), dias_atividade, responsavel, telefone))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Paciente cadastrado na nuvem com sucesso!"
    except Exception as e:
        return False, f"Erro ao salvar paciente: {e}"

def listar_todos_pacientes():
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, data_nascimento, dias_atividade FROM public.pacientes ORDER BY nome ASC")
        dados = cursor.fetchall()
        cursor.close()
        conn.close()
        return dados
    except Exception:
        return []

def atualizar_dados_paciente(id_paciente, nome, data_nasc, dias_atividade, responsavel, telefone):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE public.pacientes 
            SET nome=%s, data_nascimento=%s, dias_atividade=%s, nome_responsavel=%s, telefone=%s 
            WHERE id=%s
        """, (nome, str(data_nasc), dias_atividade, responsavel, telefone, int(id_paciente)))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Dados atualizados na nuvem!"
    except Exception as e:
        return False, f"Erro ao atualizar: {e}"

def excluir_paciente_do_banco(id_paciente):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM public.pacientes WHERE id = %s", (int(id_paciente),))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Paciente removido da nuvem!"
    except Exception as e:
        return False, f"Erro ao excluir: {e}"

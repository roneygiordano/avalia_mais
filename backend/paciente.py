# backend/paciente.py
from database.db_manager import conectar_banco, salvar_dados_no_github

def salvar_novo_paciente(nome, data_nasc, dias_atividade, responsavel, telefone):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pacientes (nome, data_nascimento, dias_atividade, nome_responsavel, telefone)
            VALUES (?, ?, ?, ?, ?)
        """, (nome, str(data_nasc), dias_atividade, responsavel, telefone))
        conn.commit()
        conn.close()
        
        # Sincroniza o arquivo com o GitHub imediatamente
        salvar_dados_no_github()
        return True, "Paciente cadastrado e sincronizado com sucesso!"
    except Exception as e:
        return False, f"Erro: {e}"

def listar_todos_pacientes():
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, data_nascimento, dias_atividade FROM pacientes ORDER BY nome ASC")
        dados = cursor.fetchall()
        conn.close()
        return dados
    except Exception:
        return []

def atualizar_dados_paciente(id_paciente, nome, data_nasc, dias_atividade, responsavel, telefone):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE pacientes SET nome=?, data_nascimento=?, dias_atividade=?, nome_responsavel=?, telefone=? WHERE id=?
        """, (nome, str(data_nasc), dias_atividade, responsavel, telefone, id_paciente))
        conn.commit()
        conn.close()
        salvar_dados_no_github()
        return True, "Dados atualizados!"
    except Exception as e:
        return False, f"Erro: {e}"

def excluir_paciente_do_banco(id_paciente):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM avaliacoes WHERE paciente_id = ?", (id_paciente,))
        cursor.execute("DELETE FROM pacientes WHERE id = ?", (id_paciente,))
        conn.commit()
        conn.close()
        salvar_dados_no_github()
        return True, "Paciente removido!"
    except Exception as e:
        return False, f"Erro: {e}"

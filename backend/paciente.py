# backend/paciente.py
from database.db_manager import conectar_banco

def salvar_novo_paciente(nome, data_nasc, dias_atividade, responsavel, telefone):
    """Insere um novo paciente no banco de dados SQLite"""
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO pacientes (nome, data_nascimento, dias_atividade, nome_responsavel, telefone)
            VALUES (?, ?, ?, ?, ?)
        """, (nome, str(data_nasc), dias_atividade, responsavel, telefone))
        
        conn.commit()
        conn.close()
        return True, "Paciente cadastrado com sucesso!"
    except Exception as e:
        return False, f"Erro ao salvar no banco de dados: {e}"

def listar_todos_pacientes():
    """Busca a lista de todos os pacientes para exibição"""
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, data_nascimento, dias_atividade FROM pacientes ORDER BY nome ASC")
        dados = cursor.fetchall()
        conn.close()
        return dados # Retorna a lista de tuplas [(id, nome, data_nasc, dias)...]
    except Exception:
        return []

def atualizar_dados_paciente(id_paciente, nome, data_nasc, dias_atividade, responsavel, telefone):
    """Atualiza as informações de um paciente existente no banco de dados"""
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE pacientes 
            SET nome = ?, data_nascimento = ?, dias_atividade = ?, nome_responsavel = ?, telefone = ?
            WHERE id = ?
        """, (nome, str(data_nasc), dias_atividade, responsavel, telefone, id_paciente))
        
        conn.commit()
        conn.close()
        return True, "Dados do paciente atualizados com sucesso!"
    except Exception as e:
        return False, f"Erro ao atualizar dados: {e}"

def excluir_paciente_do_banco(id_paciente):
    """Remove um paciente e todo o seu histórico de avaliações do banco de dados"""
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        
        # 1. Primeiro remove as avaliações para manter a integridade dos dados
        cursor.execute("DELETE FROM avaliacoes WHERE paciente_id = ?", (id_paciente,))
        
        # 2. Depois remove o paciente
        cursor.execute("DELETE FROM pacientes WHERE id = ?", (id_paciente,))
        
        conn.commit()
        conn.close()
        return True, "Paciente e histórico excluídos com sucesso!"
    except Exception as e:
        return False, f"Erro ao excluir paciente: {e}"

import sqlite3
from supabase import create_client

# 1. Configurações de Conexão do Supabase
SUPABASE_URL = "https://supabase.co"
SUPABASE_KEY = "sb_publishable_inzZh573U_sXX0qnVMLcPw_7hp6Hzw1"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def migrar_banco():
    print("🔄 Iniciando migração de dados adaptativa...")
    
    conn_sqlite = sqlite3.connect("avalia_mais.db")
    cursor = conn_sqlite.cursor()
    
    # --- MIGRANDO OS PACIENTES ---
    print("\n👥 Copiando Pacientes...")
    try:
        cursor.execute("SELECT id, nome, data_nascimento, dias_atividade, nome_responsavel, telefone FROM pacientes")
        pacientes_sqlite = cursor.fetchall()
        
        for p in pacientes_sqlite:
            dados_paciente = {
                "id": p[0],
                "nome": p[1],
                "data_nascimento": str(p[2]),
                "dias_atividade": p[3],
                "nome_responsavel": p[4],
                "telefone": p[5]
            }
            supabase.table("pacientes").insert(dados_paciente).execute()
            print(f"  ✅ Paciente '{p[1]}' migrado.")
    except Exception as e:
        print(f"  ❌ Erro ao migrar pacientes: {e}")

    # --- MIGRANDO AS AVALIAÇÕES ---
    print("\n📋 Copiando Avaliações (Detectando estrutura antiga)...")
    try:
        # Descobre quantas colunas a sua tabela de avaliações realmente tem no SQLite
        cursor.execute("SELECT * FROM avaliacoes LIMIT 1")
        colunas_reais = [desc[0] for desc in cursor.description]
        print(f"  🔍 Colunas encontradas no seu SQLite: {colunas_reais}")
        
        # Busca todos os dados da tabela
        cursor.execute("SELECT * FROM avaliacoes")
        avaliacoes_sqlite = cursor.fetchall()
        
        for a in avaliacoes_sqlite:
            # Transforma a linha do banco em um dicionário mapeando o nome da coluna ao valor
            registro = dict(zip(colunas_reais, a))
            
            # Mapeia os dados tratando as variações de nomes e colunas que podem faltar
            paciente_id = registro.get("paciente_id")
            data_aval = registro.get("data_avaliacao") or registro.get("data") or "01/01/2000"
            
            # Se não existir a coluna tipo_consulta no seu SQLite, define como "Avaliação" padrão
            tipo_consulta = registro.get("tipo_consulta") or registro.get("tipo") or "Avaliação"
            
            # Captura os testes tratando os nomes originais (com ou teste_ na frente)
            t1 = registro.get("teste_sentar_levantar") or registro.get("sentar_levantar") or 0.0
            t2 = registro.get("teste_tug") or registro.get("tug") or 0.0
            t3 = registro.get("teste_tandem") or registro.get("tandem") or 0.0
            t4 = registro.get("teste_taf") or registro.get("taf") or 0.0
            
            obs = registro.get("observacoes") or registro.get("obs") or ""

            dados_avaliacao = {
                "paciente_id": int(paciente_id),
                "data_avaliacao": str(data_aval),
                "tipo_consulta": str(tipo_consulta),
                "teste_sentar_levantar": float(t1) if t1 is not None else 0.0,
                "teste_tug": float(t2) if t2 is not None else 0.0,
                "teste_tandem": float(t3) if t3 is not None else 0.0,
                "teste_taf": float(t4) if t4 is not None else 0.0,
                "observacoes": str(obs)
            }
            
            supabase.table("avaliacoes").insert(dados_avaliacao).execute()
            print(f"  ✅ Avaliação da data {data_aval} migrada.")
            
    except Exception as e:
        print(f"  ❌ Erro ao migrar avaliações: {e}")

    conn_sqlite.close()
    print("\n🎉 Processo de migração concluído!")

if __name__ == "__main__":
    migrar_banco()

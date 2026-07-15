# frontend/cadastro_view.py (Trecho da Lista Geral no rodapé)
st.write("---")
st.subheader("👥 Lista Geral de Pacientes Registrados")
if todos_pacientes:
    for p in todos_pacientes:
        # p[2] é a data de nascimento vinda do banco (YYYY-MM-DD)
        try:
            data_formatada = datetime.strptime(p[2], "%Y-%m-%d").strftime("%d/%m/%Y")
        except:
            data_formatada = p[2] # Caso já esteja formatada
            
        st.text(f"🆔 {p[0]} | 👤 Nome: {p[1]} | 📅 Nasc: {data_formatada} | 🗓️ Atividades: {p[3]}")
else:
    st.info("Nenhum paciente cadastrado.")

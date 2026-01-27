import streamlit as st
import pandas as pd
from supabase import create_client, Client

# --- CONEXÃO (Mantenha suas chaves) ---
URL = "https://zfwdjpklemkuvwizdoly.supabase.co"
KEY = "sb_publishable_qMi5vxWp54WVmmQuoDHkdg_YeaRbiW_" 
supabase = create_client(URL, KEY)

st.title("🔍 Gestão de Leads - CRM")

# 1. BUSCA OS DADOS
resposta = supabase.table("VENDAS").select("*").order("created_at", desc=True).execute()

if resposta.data:
    df = pd.DataFrame(resposta.data)
    df['Data'] = pd.to_datetime(df['created_at']).dt.strftime('%d/%m/%Y %H:%M')
    
    # Exibe a tabela (incluindo Observações se houver)
    st.dataframe(df[["Data", "Nome", "Telefone", "Status", "Observacoes"]], use_container_width=True)

    st.divider()
    st.subheader("📝 Editar Registro")

    lista_nomes = df['Nome'].tolist()
    nome_selecionado = st.selectbox("Selecione quem deseja alterar:", [""] + lista_nomes)

    if nome_selecionado != "":
        # Puxa os dados atuais do banco para preencher o formulário
        dados_cliente = df[df['Nome'] == nome_selecionado].iloc[0]
        id_cliente = dados_cliente['id']

        with st.form("form_edicao"):
            col1, col2 = st.columns(2)
            with col1:
                novo_nome = st.text_input("Nome", value=dados_cliente['Nome'])
                novo_tel = st.text_input("Telefone", value=dados_cliente['Telefone'])
            with col2:
                # Garante que o selectbox comece no status atual do cliente
                status_atual = dados_cliente['Status'] if dados_cliente['Status'] in ["Novo", "Pendente", "Fechado", "Cancelado"] else "Novo"
                novo_status = st.selectbox("Status", ["Novo", "Pendente", "Fechado", "Cancelado"], 
                                          index=["Novo", "Pendente", "Fechado", "Cancelado"].index(status_atual))
            
            # CAMPO DE OBSERVAÇÃO (Onde estava o erro)
            # Se a observação for nula no banco, ele coloca um texto vazio
            obs_atual = dados_cliente['Observacoes'] if dados_cliente['Observacoes'] else ""
            nova_obs = st.text_area("Anotações / Observações", value=str(obs_atual))
            
            botao_salvar = st.form_submit_button("Confirmar Alterações")

        if botao_salvar:
            try:
                # AQUI É ONDE SALVAMOS TUDO DE VOLTA NO SUPABASE
                supabase.table("VENDAS").update({
                    "Nome": novo_nome,
                    "Telefone": novo_tel,
                    "Status": novo_status,
                    "Observacoes": nova_obs  # Salvando a nova observação
                }).eq("id", id_cliente).execute()
                
                st.success(f"✅ Alterações para {nome_selecionado} salvas com sucesso!")
                st.rerun() # Atualiza a página para mostrar os dados novos
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")

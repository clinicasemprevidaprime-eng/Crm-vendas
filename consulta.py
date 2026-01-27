import streamlit as st
from supabase import create_client, Client
import pandas as pd

# 1. Conexão
URL = "https://zfwdjpklemkuvwizdoly.supabase.co"
KEY = "sb_publishable_qMi5vxWp54WVmmQuoDHkdg_YeaRbiW_" 
supabase = create_client(URL, KEY)

st.title("🔍 CRM Med Card - Consulta e Gestão")

# --- PARTE 1: VISUALIZAÇÃO ---
resposta = supabase.table("VENDAS").select("*").order("created_at", desc=True).execute()

if resposta.data:
    df = pd.DataFrame(resposta.data)
    df['Data'] = pd.to_datetime(df['created_at']).dt.strftime('%d/%m/%Y %H:%M')
    
    # Adicionamos 'Observacoes' na lista de colunas para exibir
    st.dataframe(df[["Data", "Nome", "Telefone", "Status", "Observacoes"]], use_container_width=True)

    st.divider()

    # --- PARTE 2: EDIÇÃO ---
    st.subheader("📝 Editar Informações")
    lista_nomes = df['Nome'].tolist()
    nome_selecionado = st.selectbox("Selecione para editar:", [""] + lista_nomes)

    if nome_selecionado != "":
        dados_cliente = df[df['Nome'] == nome_selecionado].iloc[0]
        id_cliente = dados_cliente['id']

        with st.form("form_edicao"):
            col1, col2 = st.columns(2)
            with col1:
                novo_nome = st.text_input("Nome", value=dados_cliente['Nome'])
                novo_tel = st.text_input("Telefone", value=dados_cliente['Telefone'])
            with col2:
                novo_status = st.selectbox("Status", ["Novo", "Pendente", "Fechado", "Cancelado"], 
                                          index=["Novo", "Pendente", "Fechado", "Cancelado"].index(dados_cliente['Status']))
            
            # Campo de Observações (Área de texto maior)
            nova_obs = st.text_area("Observações", value=str(dados_cliente['Observacoes']) if dados_cliente['Observacoes'] else "")
            
            botao_editar = st.form_submit_button("Salvar Alterações")

        if botao_editar:
            supabase.table("VENDAS").update({
                "Nome": novo_nome,
                "Telefone": novo_tel,
                "Status": novo_status,
                "Observacoes": nova_obs
            }).eq("id", id_cliente).execute()
            
            st.success(f"✅ Registro de {nome_selecionado} atualizado!")
            st.rerun()

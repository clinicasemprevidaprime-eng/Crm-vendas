import streamlit as st
from supabase import create_client, Client
import pandas as pd

# 1. Conexão (Mantenha suas chaves reais)
URL = "https://zfwdjpklemkuvwizdoly.supabase.co"
KEY = "sb_publishable_qMi5vxWp54WVmmQuoDHkdg_YeaRbiW_" 
supabase = create_client(URL, KEY)

st.set_page_config(page_title="CRM Clínica Sempre Vida", layout="wide")

# --- MENU LATERAL ---
st.sidebar.title("🏥 SISTEMA GESTÃO")
categoria = st.sidebar.selectbox("O que deseja gerenciar?", ["👤 Leads (PF)", "🤝 Parceiros"])
opcao = st.sidebar.radio("Ação:", ["📝 Cadastro", "📊 Gestão"])

# ==========================================
# SEÇÃO 1: LEADS (PESSOA FÍSICA)
# ==========================================
if categoria == "👤 Leads (PF)":
    if opcao == "📝 Cadastro":
        st.title("🚀 Novo Lead - Med Card")
        with st.form("form_pf", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome do Cliente")
                tel = st.text_input("WhatsApp")
            with col2:
                status = st.selectbox("Status", ["Novo", "Pendente", "Em Negociação", "Fechado", "Cancelado"])
            obs = st.text_area("Anotações")
            if st.form_submit_button("Salvar Lead"):
                supabase.table("VENDAS").insert({"Nome": nome, "Telefone": tel, "Status": status, "Observacoes": obs}).execute()
                st.success("Lead salvo!")

    elif opcao == "📊 Gestão":
        st.title("📊 Gestão de Leads")
        res = supabase.table("VENDAS").select("*").order("created_at", desc=True).execute()
        if res.data:
            df = pd.DataFrame(res.data)
            st.dataframe(df[["Nome", "Telefone", "Status", "Observacoes"]], use_container_width=True)
            # (Aqui você pode manter aquele código de edição que já temos se quiser)

# ==========================================
# SEÇÃO 2: PARCEIROS (CLÍNICAS/EMPRESAS)
# ==========================================
elif categoria == "🤝 Parceiros":
    if opcao == "📝 Cadastro":
        st.title("🤝 Cadastro de Novo Parceiro")
        with st.form("form_parceiro", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                empresa = st.text_input("Nome da Clínica/Parceiro")
                contato = st.text_input("Telefone de Contato")
            with col2:
                especialidade = st.text_input("Especialidade (ex: Dentista, Lab)")
                email = st.text_input("E-mail")
            obs_p = st.text_area("Detalhes da Parceria")
            if st.form_submit_button("Cadastrar Parceiro"):
                supabase.table("PARCEIROS").insert({
                    "Nome_Parceiro": empresa, 
                    "Especialidade": especialidade, 
                    "Telefone": contato, 
                    "Email": email, 
                    "Observacoes": obs_p
                }).execute()
                st.success(f"Parceria com {empresa} registrada!")

    elif opcao == "📊 Gestão":
        st.title("📋 Lista de Parceiros")
        res_p = supabase.table("PARCEIROS").select("*").order("Nome_Parceiro").execute()
        if res_p.data:
            df_p = pd.DataFrame(res_p.data)
            st.dataframe(df_p[["Nome_Parceiro", "Especialidade", "Telefone", "Email", "Observacoes"]], use_container_width=True)
        else:
            st.info("Nenhum parceiro cadastrado.")

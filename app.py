import streamlit as st
from supabase import create_client, Client
import pandas as pd

# 1. Configurações de Conexão (Mantenha as suas chaves reais)
URL = "https://zfwdjpklemkuvwizdoly.supabase.co"
KEY = "sb_publishable_qMi5vxWp54WVmmQuoDHkdg_YeaRbiW_" 
supabase = create_client(URL, KEY)

st.set_page_config(page_title="CRM Clínica Sempre Vida", layout="wide")

# --- MENU LATERAL ---
st.sidebar.title("🏥 SISTEMA GESTÃO")
categoria = st.sidebar.selectbox("O que deseja gerenciar?", ["👤 Leads (PF)", "🤝 Parceiros (PJ)"])
opcao = st.sidebar.radio("Ação:", ["📝 Cadastro", "📊 Gestão Completa"])

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
                if nome and tel:
                    supabase.table("VENDAS").insert({"Nome": nome, "Telefone": tel, "Status": status, "Observacoes": obs}).execute()
                    st.success("Lead salvo!")
                    st.balloons()
                else:
                    st.warning("Preencha Nome e Telefone.")

    elif opcao == "📊 Gestão Completa":
        st.title("📊 Painel de Leads (PF)")
        res = supabase.table("VENDAS").select("*").order("created_at", desc=True).execute()
        if res.data:
            df = pd.DataFrame(res.data)
            st.dataframe(df[["Nome", "Telefone", "Status", "Observacoes"]], use_container_width=True)
            
            st.divider()
            col_ed, col_del = st.columns([2, 1])
            
            with col_ed:
                st.subheader("📝 Editar Lead")
                sel = st.selectbox("Selecionar para editar:", [""] + df['Nome'].tolist(), key="sel_pf")
                if sel:
                    d = df[df['Nome'] == sel].iloc[0]
                    with st.form("ed_pf"):
                        en = st.text_input("Nome", value=str(d['Nome']))
                        et = st.text_input("Telefone", value=str(d['Telefone']))
                        es = st.selectbox("Status", ["Novo", "Pendente", "Em Negociação", "Fechado", "Cancelado"], index=["Novo", "Pendente", "Em Negociação", "Fechado", "Cancelado"].index(d['Status']))
                        eo = st.text_area("Obs", value=str(d['Observacoes']) if d['Observacoes'] != 'None' else "")
                        if st.form_submit_button("Salvar Alterações"):
                            supabase.table("VENDAS").update({"Nome": en, "Telefone": et, "Status": es, "Observacoes": eo}).eq("Nome", sel).execute()
                            st.rerun()
            with col_del:
                st.subheader("🗑️ Apagar")
                del_sel = st.selectbox("Eliminar:", [""] + df['Nome'].tolist(), key="del_pf")
                conf = st.checkbox("Confirmar exclusão (PF)")
                if st.button("❌ APAGAR LEAD") and conf and del_sel:
                    supabase.table("VENDAS").delete().eq("Nome", del_sel).execute()
                    st.rerun()

# ==========================================
# SEÇÃO 2: PARCEIROS (PESSOA JURÍDICA / PJ)
# ==========================================
elif categoria == "🤝 Parceiros (PJ)":
    if opcao == "📝 Cadastro":
        st.title("🤝 Cadastro de Parceiro PJ")
        with st.form("form_pj", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                pj_nome = st.text_input("Nome da Clínica/Empresa")
                pj_tel = st.text_input("Telefone")
            with col2:
                pj_esp = st.text_input("Especialidade")
                pj_mail = st.text_input("E-mail")
            pj_obs = st.text_area("Notas da Parceria")
            if st.form_submit_button("Cadastrar Parceiro"):
                if pj_nome:
                    supabase.table("PARCEIROS").insert({"Nome_Parceiro": pj_nome, "Especialidade": pj_esp, "Telefone": pj_tel, "Email": pj_mail, "Observacoes": pj_obs}).execute()
                    st.success("Parceiro cadastrado!")
                else:
                    st.warning("O nome da empresa é obrigatório.")

    elif opcao == "📊 Gestão Completa":
        st.title("📋 Painel de Parceiros PJ")
        res_p = supabase.table("PARCEIROS").select("*").order("Nome_Parceiro").execute()
        
        if res_p.data:
            df_p = pd.DataFrame(res_p.data)
            st.dataframe(df_p[["Nome_Parceiro", "Especialidade", "Telefone", "Email", "Observacoes"]], use_container_width=True)
            
            st.divider()
            ced, cdel = st.columns([2, 1])
            
            with ced:
                st.subheader("📝 Editar Parceiro")
                sel_p = st.selectbox("Selecionar Parceiro:", [""] + df_p['Nome_Parceiro'].tolist())
                if sel_p:
                    dp = df_p[df_p['Nome_Parceiro'] == sel_p].iloc[0]
                    with st.form("ed_pj"):
                        epn = st.text_input("Nome", value=str(dp['Nome_Parceiro']))
                        epe = st.text_input("Especialidade", value=str(dp['Especialidade']))
                        ept = st.text_input("Telefone", value=str(dp['Telefone']))
                        epm = st.text_input("Email", value=str(dp['Email']))
                        epo = st.text_area("Obs", value=str(dp['Observacoes']) if dp['Observacoes'] != 'None' else "")
                        if st.form_submit_button("Atualizar Parceiro"):
                            supabase.table("PARCEIROS").update({"Nome_Parceiro": epn, "Especialidade": epe, "Telefone": ept, "Email": epm, "Observacoes": epo}).eq("Nome_Parceiro", sel_p).execute()
                            st.rerun()
            
            with cdel:
                st.subheader("🗑️ Remover")
                p_del = st.selectbox("Remover Parceiro:", [""] + df_p['Nome_Parceiro'].tolist())
                p_conf = st.checkbox("Confirmar exclusão (PJ)")
                if st.button("❌ APAGAR PARCEIRO") and p_conf and p_del:
                    supabase.table("PARCEIROS").delete().eq("Nome_Parceiro", p_del).execute()
                    st.rerun()
        else:
            st.info("Nenhum parceiro registado.")

import streamlit as st
from supabase import create_client, Client
import pandas as pd

# 1. Suas chaves (Mantenha as que você já usa)
URL = "https://zfwdjpklemkuvwizdoly.supabase.co"
KEY = "sb_publishable_qMi5vxWp54WVmmQuoDHkdg_YeaRbiW_" 
supabase = create_client(URL, KEY)

st.title("🔍 Gestão Med Card - Consulta e Edição")

# --- BUSCA DE DADOS ---
resposta = supabase.table("VENDAS").select("*").order("created_at", desc=True).execute()

if resposta.data:
    df = pd.DataFrame(resposta.data)
    
    # Criamos a data legível
    df['Data'] = pd.to_datetime(df['created_at']).dt.strftime('%d/%m/%Y %H:%M')
    
    # TABELA PRINCIPAL (Vai reaparecer tudo aqui!)
    st.subheader("📋 Lista de Leads")
    st.dataframe(df[["Data", "Nome", "Telefone", "Status", "Observacoes"]], use_container_width=True)

    st.divider()

    # --- ÁREA DE EDIÇÃO ---
    st.subheader("📝 Editar Informações")
    
    # Criamos a lista de nomes simples (sem IDs complicados no texto)
    lista_nomes = df['Nome'].astype(str).tolist()
    nome_selecionado = st.selectbox("Escolha o cliente para alterar:", [""] + lista_nomes)

    if nome_selecionado:
        # Localizamos os dados do cliente pelo Nome
        dados = df[df['Nome'] == nome_selecionado].iloc[0]
        id_real = dados['id']

        with st.form("form_edicao_recuperacao"):
            col1, col2 = st.columns(2)
            with col1:
                n_nome = st.text_input("Nome", value=str(dados['Nome']))
                n_tel = st.text_input("Telefone", value=str(dados['Telefone']))
            with col2:
                status_opcoes = ["Novo", "Pendente", "Em Negociação", "Fechado", "Cancelado"]
                idx = status_opcoes.index(dados['Status']) if dados['Status'] in status_opcoes else 0
                n_status = st.selectbox("Status", status_opcoes, index=idx)
            
            # Limpeza do campo de Observação
            obs_texto = str(dados['Observacoes']) if dados['Observacoes'] and str(dados['Observacoes']) != 'None' else ""
            n_obs = st.text_area("Observações", value=obs_texto)
            
            btn_salvar = st.form_submit_button("Salvar Alterações")

        if btn_salvar:
            try:
                # O segredo: usamos o id_real que o código localizou internamente
                supabase.table("VENDAS").update({
                    "Nome": n_nome,
                    "Telefone": n_tel,
                    "Status": n_status,
                    "Observacoes": n_obs
                }).eq("id", id_real).execute()
                
                st.success(f"✅ {nome_selecionado} atualizado!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")
else:
    st.info("O banco de dados está vazio ou não carregou.")

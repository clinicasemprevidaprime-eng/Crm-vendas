import streamlit as st
from supabase import create_client, Client
import pandas as pd

# 1. Suas chaves (Mantenha as suas originais aqui)
URL = "https://zfwdjpklemkuvwizdoly.supabase.co"
KEY = "sb_publishable_qMi5vxWp54WVmmQuoDHkdg_YeaRbiW_" 
supabase = create_client(URL, KEY)

# Configuração da Página
st.set_page_config(page_title="Portal CRM", layout="wide")

# --- BARRA LATERAL (MENU) ---
st.sidebar.title("🏥 Gestão CRM")
opcao = st.sidebar.radio("Escolha uma opção:", ["📝 Novo Cadastro", "🔍 Consulta e Edição"])

# --- PÁGINA 1: NOVO CADASTRO ---
if opcao == "📝 Novo Cadastro":
    st.title("🚀 Cadastrar Novo Lead - Crm")
    
    with st.form("form_novo_lead", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome do Cliente")
            telefone = st.text_input("WhatsApp")
        with col2:
            status = st.selectbox("Status Inicial", ["Novo", "Pendente", "Em Negociação", "Fechado", "Cancelado"])
        
        obs = st.text_area("Observações Iniciais")
        botao_cadastrar = st.form_submit_button("Salvar no Banco de Dados")

    if botao_cadastrar:
        if nome and telefone:
            try:
                supabase.table("VENDAS").insert({
                    "Nome": nome, 
                    "Telefone": telefone, 
                    "Status": status, 
                    "Observacoes": obs
                }).execute()
                st.success(f"✅ {nome} cadastrado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")
        else:
            st.warning("⚠️ Preencha pelo menos Nome e Telefone!")

# --- PÁGINA 2: CONSULTA E EDIÇÃO ---
elif opcao == "🔍 Consulta e Edição":
    st.title("📊 Painel de Controle e Gestão")

    # Busca os dados
    resposta = supabase.table("VENDAS").select("*").order("created_at", desc=True).execute()

    if resposta.data:
        df = pd.DataFrame(resposta.data)
        df['Data'] = pd.to_datetime(df['created_at']).dt.strftime('%d/%m/%Y %H:%M')
        
        # Tabela de Visualização
        st.subheader("📋 Lista de Clientes Atuais")
        st.dataframe(df[["Data", "Nome", "Telefone", "Status", "Observacoes"]], use_container_width=True)

        st.divider()

        # Formulário de Edição
        st.subheader("📝 Editar Registro Selecionado")
        lista_nomes = df['Nome'].tolist()
        nome_sel = st.selectbox("Selecione para alterar:", [""] + lista_nomes)

        if nome_sel:
            dados = df[df['Nome'] == nome_sel].iloc[0]

            with st.form("form_edicao_painel"):
                c1, c2 = st.columns(2)
                with c1:
                    ed_nome = st.text_input("Nome", value=str(dados['Nome']))
                    ed_tel = st.text_input("Telefone", value=str(dados['Telefone']))
                with c2:
                    st_opcoes = ["Novo", "Pendente", "Em Negociação", "Fechado", "Cancelado"]
                    st_atual = dados['Status'] if dados['Status'] in st_opcoes else "Novo"
                    ed_status = st.selectbox("Status", st_opcoes, index=st_opcoes.index(st_atual))
                
                obs_v = str(dados['Observacoes']) if dados['Observacoes'] and str(dados['Observacoes']) != 'None' else ""
                ed_obs = st.text_area("Observações", value=obs_v)
                
                if st.form_submit_button("Salvar Alterações"):
                    try:
                        supabase.table("VENDAS").update({
                            "Nome": ed_nome,
                            "Telefone": ed_tel,
                            "Status": ed_status,
                            "Observacoes": ed_obs
                        }).eq("Nome", nome_sel).execute()
                        st.success("✅ Atualizado!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro: {e}")
    else:
        st.info("Nenhum dado encontrado.")

import streamlit as st
from supabase import create_client, Client
import pandas as pd

# 1. Suas chaves (Mantenha as suas originais aqui)
URL = "https://zfwdjpklemkuvwizdoly.supabase.co"
KEY = "sb_publishable_qMi5vxWp54WVmmQuoDHkdg_YeaRbiW_" 
supabase = create_client(URL, KEY)

st.set_page_config(page_title="Portal Clínica Sempre Vida", layout="wide")

# --- BARRA LATERAL (MENU) ---
st.sidebar.title("🏥 Gestão CRM")
opcao = st.sidebar.radio("Escolha uma opção:", ["📝 Novo Cadastro", "🔍 Consulta e Gestão"])

# --- PÁGINA 1: NOVO CADASTRO ---
if opcao == "📝 Novo Cadastro":
    st.title("🚀 Cadastrar Novo Lead - Med Card")
    with st.form("form_novo", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome do Cliente")
            telefone = st.text_input("WhatsApp")
        with col2:
            status = st.selectbox("Status Inicial", ["Novo", "Pendente", "Em Negociação", "Fechado", "Cancelado"])
        obs = st.text_area("Observações Iniciais")
        if st.form_submit_button("Salvar no Banco de Dados"):
            if nome and telefone:
                try:
                    supabase.table("VENDAS").insert({"Nome": nome, "Telefone": telefone, "Status": status, "Observacoes": obs}).execute()
                    st.success(f"✅ {nome} cadastrado!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Erro ao salvar: {e}")
            else:
                st.warning("⚠️ Preencha Nome e Telefone!")

# --- PÁGINA 2: CONSULTA E GESTÃO ---
elif opcao == "🔍 Consulta e Gestão":
    st.title("📊 Painel de Controle e Performance")

    # Busca os dados
    resposta = supabase.table("VENDAS").select("*").order("created_at", desc=True).execute()

    if resposta.data:
        df = pd.DataFrame(resposta.data)
        df['Data'] = pd.to_datetime(df['created_at']).dt.strftime('%d/%m/%Y %H:%M')
        
        # --- INDICADORES (CARDS) ---
        c1, c2, c3, c4 = st.columns(4)
        total = len(df)
        fechados = len(df[df['Status'] == 'Fechado'])
        pendentes = len(df[df['Status'] == 'Pendente'])
        negociacao = len(df[df['Status'] == 'Em Negociação'])

        c1.metric("Total de Leads", total)
        c2.metric("✅ Fechados", fechados)
        c3.metric("⏳ Pendentes", pendentes)
        c4.metric("🤝 Em Negociação", negociacao)
        
        st.divider()

        # --- BUSCA E TABELA ---
        st.subheader("🔎 Pesquisar Cliente")
        termo_busca = st.text_input("Filtrar por nome:", "")
        df_filtrado = df[df['Nome'].str.contains(termo_busca, case=False, na=False)] if termo_busca else df
        st.dataframe(df_filtrado[["Data", "Nome", "Telefone", "Status", "Observacoes"]], use_container_width=True)

        st.divider()

        # --- EDIÇÃO ---
        col_ed, col_del = st.columns([2, 1]) # Coluna de edição maior que a de exclusão
        
        with col_ed:
            st.subheader("📝 Editar Registro")
            lista_edicao = df_filtrado['Nome'].tolist()
            nome_sel = st.selectbox("Selecione para alterar:", [""] + lista_edicao)

            if nome_sel:
                dados = df[df['Nome'] == nome_sel].iloc[0]
                with st.form("form_edicao"):
                    e_nome = st.text_input("Nome", value=str(dados['Nome']))
                    e_tel = st.text_input("Telefone", value=str(dados['Telefone']))
                    opcoes = ["Novo", "Pendente", "Em Negociação", "Fechado", "Cancelado"]
                    idx = opcoes.index(dados['Status']) if dados['Status'] in opcoes else 0
                    e_status = st.selectbox("Status", opcoes, index=idx)
                    e_obs = st.text_area("Observações", value=str(dados['Observacoes']) if dados['Observacoes'] != 'None' else "")
                    
                    if st.form_submit_button("Confirmar Alterações"):
                        supabase.table("VENDAS").update({"Nome": e_nome, "Telefone": e_tel, "Status": e_status, "Observacoes": e_obs}).eq("Nome", nome_sel).execute()
                        st.success("✅ Atualizado!")
                        st.rerun()

        # --- APAGAR DADOS (COM PROTEÇÃO) ---
        with col_del:
            st.subheader("🗑️ Zona de Perigo")
            nome_del = st.selectbox("Selecione para APAGAR:", [""] + df_filtrado['Nome'].tolist())
            confirmar = st.checkbox("Eu tenho certeza que desejo excluir")
            
            if st.button("❌ EXCLUIR REGISTRO"):
                if nome_del and confirmar:
                    try:
                        supabase.table("VENDAS").delete().eq("Nome", nome_del).execute()
                        st.warning(f"🗑️ Registro de {nome_del} removido.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao apagar: {e}")
                elif not confirmar:
                    st.info("Marque o 'check' para confirmar a exclusão.")
    else:
        st.info("O banco de dados está vazio.")

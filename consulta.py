import streamlit as st
from supabase import create_client, Client
import pandas as pd

# 1. Conexão (Mantenha suas chaves reais)
URL = "https://zfwdjpklemkuvwizdoly.supabase.co"
KEY = "sb_publishable_qMi5vxWp54WVmmQuoDHkdg_YeaRbiW_" 
supabase = create_client(URL, KEY)

st.title("🔍 Gestão Med Card - Consulta e Edição")

# --- PARTE 1: BUSCA E EXIBIÇÃO ---
# Buscamos todas as colunas, incluindo ID e Observacoes
resposta = supabase.table("VENDAS").select("*").order("created_at", desc=True).execute()

if resposta.data:
    df = pd.DataFrame(resposta.data)
    
    # Formatação da Data para exibição
    df['Data_Formatada'] = pd.to_datetime(df['created_at']).dt.strftime('%d/%m/%Y %H:%M')
    
    # Exibe a tabela principal
    st.dataframe(df[["Data_Formatada", "Nome", "Telefone", "Status", "Observacoes"]], use_container_width=True)

    st.divider()

    # --- PARTE 2: EDIÇÃO ---
    st.subheader("📝 Editar Informações")
    
    # Criamos a lista de nomes
    lista_nomes = df['Nome'].tolist()
    nome_selecionado = st.selectbox("Escolha o cliente para alterar:", [""] + lista_nomes)

    if nome_selecionado != "":
        # PUXANDO OS DADOS COM SEGURANÇA
        dados_cliente = df[df['Nome'] == nome_selecionado].iloc[0]
        
        # O ID é crucial aqui para evitar o erro de 'bigint'
        id_cliente = int(dados_cliente['id']) 

        with st.form("form_edicao_final"):
            col1, col2 = st.columns(2)
            with col1:
                novo_nome = st.text_input("Nome", value=str(dados_cliente['Nome']))
                novo_tel = st.text_input("Telefone", value=str(dados_cliente['Telefone']))
            with col2:
                status_lista = ["Novo", "Pendente", "Fechado", "Cancelado", "Em Negociação"]
                # Verifica se o status atual existe na lista, senão usa 'Novo'
                try:
                    idx_status = status_lista.index(dados_cliente['Status'])
                except:
                    idx_status = 0
                novo_status = st.selectbox("Status", status_lista, index=idx_status)
            
            # Tratando a observação para nunca ser 'None'
            obs_inicial = dados_cliente['Observacoes'] if dados_cliente['Observacoes'] else ""
            nova_obs = st.text_area("Anotações / Observações", value=str(obs_inicial))
            
            botao_salvar = st.form_submit_button("Confirmar Alterações")

        if botao_salvar:
            try:
                # O comando .eq("id", id_cliente) agora usará um número real, não 'None'
                supabase.table("VENDAS").update({
                    "Nome": novo_nome,
                    "Telefone": novo_tel,
                    "Status": novo_status,
                    "Observacoes": nova_obs
                }).eq("id", id_cliente).execute()
                
                st.success(f"✅ Dados de {nome_selecionado} atualizados!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")
else:
    st.info("O banco de dados está vazio.")

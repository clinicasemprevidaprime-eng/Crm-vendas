import streamlit as st
from supabase import create_client, Client
import pandas as pd

# 1. Conexão (Suas chaves reais)
URL = "https://zfwdjpklemkuvwizdoly.supabase.co"
KEY = "sb_publishable_qMi5vxWp54WVmmQuoDHkdg_YeaRbiW_" 
supabase = create_client(URL, KEY)

st.title("🔍 Consulta e Edição de Leads")

# --- PARTE 1: VISUALIZAÇÃO ---
if st.button("🔄 Atualizar Lista"):
    st.rerun()

resposta = supabase.table("VENDAS").select("*").order("created_at", desc=True).execute()

if resposta.data:
    df = pd.DataFrame(resposta.data)
    df['Data'] = pd.to_datetime(df['created_at']).dt.strftime('%d/%m/%Y %H:%M')
    st.dataframe(df[["Data", "Nome", "Telefone", "Status"]], use_container_width=True)

    st.divider() # Linha divisória

    # --- PARTE 2: FORMULÁRIO DE EDIÇÃO ---
    st.subheader("📝 Editar Cliente")
    
    # Criamos uma lista com os nomes para você escolher quem editar
    lista_nomes = df['Nome'].tolist()
    nome_selecionado = st.selectbox("Selecione o cliente para alterar:", [""] + lista_nomes)

    if nome_selecionado != "":
        # Puxa os dados atuais do cliente escolhido
        dados_cliente = df[df['Nome'] == nome_selecionado].iloc[0]
        id_cliente = dados_cliente['id']

        with st.form("form_edicao"):
            novo_nome = st.text_input("Nome", value=dados_cliente['Nome'])
            novo_tel = st.text_input("Telefone", value=dados_cliente['Telefone'])
            novo_status = st.selectbox("Status", ["Novo", "Pendente", "Fechado", "Cancelado"], 
                                      index=["Novo", "Pendente", "Fechado", "Cancelado"].index(dados_cliente['Status']))
            
            botao_editar = st.form_submit_button("Confirmar Alterações")

        if botao_editar:
            try:
                # Comando para atualizar no Supabase
                supabase.table("VENDAS").update({
                    "Nome": novo_nome,
                    "Telefone": novo_tel,
                    "Status": novo_status
                }).eq("id", id_cliente).execute()
                
                st.success(f"✅ Dados de {nome_selecionado} atualizados!")
                st.rerun() # Atualiza a tela para mostrar a mudança na tabela
            except Exception as e:
                st.error(f"Erro ao atualizar: {e}")
else:
    st.info("Nenhum dado encontrado.")

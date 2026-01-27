import streamlit as st
from supabase import create_client, Client
import pandas as pd

# 1. Suas chaves (Mantenha as que você já usa)
URL = "https://zfwdjpklemkuvwizdoly.supabase.co"
KEY = "sb_publishable_qMi5vxWp54WVmmQuoDHkdg_YeaRbiW_" 
supabase = create_client(URL, KEY)

st.title("🔍 Gestão Crm - Consulta e Edição")

# --- BUSCA DE DADOS ---
resposta = supabase.table("VENDAS").select("*").order("created_at", desc=True).execute()

if resposta.data:
    df = pd.DataFrame(resposta.data)
    df['Data'] = pd.to_datetime(df['created_at']).dt.strftime('%d/%m/%Y %H:%M')
    
    # EXIBIÇÃO DA TABELA
    st.subheader("📋 Lista de Clientes")
    st.dataframe(df[["Data", "Nome", "Telefone", "Status", "Observacoes"]], use_container_width=True)

    st.divider()

    # --- ÁREA DE EDIÇÃO SIMPLIFICADA ---
    st.subheader("📝 Editar Informações")
    
    # Criamos a lista apenas com os nomes
    lista_nomes = df['Nome'].tolist()
    nome_selecionado = st.selectbox("Selecione o cliente para alterar:", [""] + lista_nomes)

    if nome_selecionado:
        # Puxa os dados atuais do cliente escolhido
        dados = df[df['Nome'] == nome_selecionado].iloc[0]

        with st.form("form_edicao_v6"):
            c1, c2 = st.columns(2)
            with c1:
                n_nome = st.text_input("Nome", value=str(dados['Nome']))
                n_tel = st.text_input("Telefone", value=str(dados['Telefone']))
            with c2:
                status_opcoes = ["Novo", "Pendente", "Em Negociação", "Fechado", "Cancelado"]
                # Tenta achar o status atual na lista
                status_atual = dados['Status'] if dados['Status'] in status_opcoes else "Novo"
                n_status = st.selectbox("Status", status_opcoes, index=status_opcoes.index(status_atual))
            
            # Limpeza do campo Observações
            obs_v = str(dados['Observacoes']) if dados['Observacoes'] and str(dados['Observacoes']) != 'None' else ""
            n_obs = st.text_area("Observações", value=obs_v)
            
            btn_salvar = st.form_submit_button("Salvar Alterações")

        if btn_salvar:
            try:
                # O segredo: usamos o NOME ORIGINAL para localizar a linha e atualizar
                supabase.table("VENDAS").update({
                    "Nome": n_nome,
                    "Telefone": n_tel,
                    "Status": n_status,
                    "Observacoes": n_obs
                }).eq("Nome", nome_selecionado).execute()
                
                st.success(f"✅ Dados de {nome_selecionado} salvos!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")
else:
    st.info("Banco de dados vazio.")

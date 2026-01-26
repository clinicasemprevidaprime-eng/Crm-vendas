import streamlit as st
from supabase import create_client, Client
import pandas as pd

# Use suas credenciais REAIS aqui
URL = "https://zfwdjpklemkuvwizdoly.supabase.co"
KEY = "COLE_AQUI_SUA_CHAVE_SERVICE_ROLE" 

supabase = create_client(URL, KEY)

st.title("🔍 Consulta de Leads - CRM")

if st.button("Atualizar Lista de Clientes"):
    try:
        # Busca os dados
        resposta = supabase.table("VENDAS").select("*").execute()
        
        if resposta.data:
            df = pd.DataFrame(resposta.data)
            # Mostra a tabela organizada
            st.dataframe(df[["Nome", "Telefone", "Status"]])
        else:
            st.info("Nenhum dado encontrado na tabela VENDAS.")
    except Exception as e:
        st.error(f"Erro na conexão: {e}")

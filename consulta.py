import streamlit as st
from supabase import create_client, Client
import pandas as pd

# Conexão com o seu banco
URL = "https://zfwdjpklemkuvwizdoly.supabase.co"
KEY = "SUA_CHAVE_AQUI" 
supabase = create_client(URL, KEY)

st.title("🔍 Consulta de Leads - CRM")

# Botão para buscar os dados
if st.button("Atualizar Lista de Clientes"):
    resposta = supabase.table("VENDAS").select("*").execute()
    
    if resposta.data:
        df = pd.DataFrame(resposta.data)
        # Mostra apenas as colunas que você quer
        st.dataframe(df[["Nome", "Telefone", "Status"]])
    else:
        st.info("Nenhum dado encontrado no banco.")

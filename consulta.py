import streamlit as st
from supabase import create_client, Client
import pandas as pd

# 1. Suas chaves (Mantenha as que já estão funcionando)
URL = "https://zfwdjpklemkuvwizdoly.supabase.co"
KEY = "sb_publishable_qMi5vxWp54WVmmQuoDHkdg_YeaRbiW_" 
supabase = create_client(URL, KEY)

st.title("🔍 Consulta de Leads - CRM")

if st.button("Atualizar Lista de Clientes"):
    try:
        # Buscamos os dados ordenando pelo mais recente
        resposta = supabase.table("VENDAS").select("*").order("created_at", desc=True).execute()
        
        if resposta.data:
            df = pd.DataFrame(resposta.data)
            
            # --- ESSA LINHA CRIA A COLUNA DE DATA ---
            # Ela pega o 'created_at' e transforma em dia/mês/ano
            df['Data'] = pd.to_datetime(df['created_at']).dt.strftime('%d/%m/%Y %H:%M')
            
            # Escolhemos as colunas que vão aparecer (incluindo a nova 'Data')
            colunas_visiveis = ["Data", "Nome", "Telefone", "Status"]
            
            # Mostra a tabela organizada
            st.dataframe(df[colunas_visiveis], use_container_width=True)
            
            st.success(f"Lista atualizada com {len(df)} registros!")
        else:
            st.info("Nenhum dado encontrado.")
    except Exception as e:
        st.error(f"Erro ao processar dados: {e}")

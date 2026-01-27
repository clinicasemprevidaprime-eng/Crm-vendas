import streamlit as st
from supabase import create_client, Client
import pandas as pd

# 1. Suas chaves (Mantenha as que já estão funcionando)
URL = "https://zfwdjpklemkuvwizdoly.supabase.co"
KEY = "sb_publishable_qMi5vxWp54WVmmQuoDHkdg_YeaRbiW_" 
supabase = create_client(URL, KEY)

st.title("🔍 Consulta Organizada - CRM")

if st.button("Atualizar e Ordenar Lista"):
    try:
        # O segredo está aqui: .order("created_at", desc=True) 
        # Isso coloca o mais novo no topo!
        resposta = supabase.table("VENDAS").select("*").order("created_at", desc=True).execute()
        
        if resposta.data:
            df = pd.DataFrame(resposta.data)
            
            # Ajustando a data para o formato brasileiro
            df['Data'] = pd.to_datetime(df['created_at']).dt.strftime('%d/%m/%Y %H:%M')
            
            # Mostra a tabela com a Data agora incluída e ordenada
            st.dataframe(df[["Data", "Nome", "Telefone", "Status"]], use_container_width=True)
            
            st.success(f"Mostrando {len(df)} clientes (mais recentes primeiro).")
        else:
            st.info("Nenhum dado encontrado.")
    except Exception as e:
        st.error(f"Erro ao carregar: {e}")

import streamlit as st
from supabase import create_client, Client
import pandas as pd

# 1. Conexão (Mantenha suas chaves reais)
URL = "https://zfwdjpklemkuvwizdoly.supabase.co"
KEY = "sb_publishable_qMi5vxWp54WVmmQuoDHkdg_YeaRbiW_" 
supabase = create_client(URL, KEY)

st.title("🔍 Gestão Med Card - Consulta e Edição")

# --- PARTE 1: BUSCA TOTAL ---
# O asterisco '*' garante que pegamos o ID, Nome, Telefone, Status e Observacoes
resposta = supabase.table("VENDAS").select("*").order("created_at", desc=True).execute()

if resposta.data:
    df = pd.DataFrame(resposta.data)
    
    # Criamos a data formatada para a tabela
    df['Data'] = pd.to_datetime(df['created_at']).dt.strftime('%d/%m/%Y %H:%M')
    
    # Exibe a tabela (mostrando as observações reais, não 'None')
    st.subheader("📋 Lista de Leads")
    st.dataframe(df[["Data", "Nome", "Telefone", "Status", "Observacoes"]], use_container_width=True)

    st.divider()

    # --- PARTE 2: EDIÇÃO SEGURA ---
    st.subheader("📝 Editar Informações")
    
    lista_nomes = df['Nome'].tolist()
    nome_selecionado = st.selectbox("Escolha o cliente para alterar:", [""] + lista_nomes)

    if nome_selecionado != "":
        # Localiza os dados do cliente selecionado
        dados_cliente = df[df['Nome'] == nome_selecionado].iloc[0]
        
        # AQUI ESTAVA O ERRO: Agora garantimos que o ID existe antes de converter
        id_cliente = dados_cliente.get('id')

        if id_cliente is not None:
            with st.form("form_edicao_v3"):
                col1, col2 = st.columns(2)
                with col1:
                    novo_nome = st.text_input("Nome", value=str(dados_cliente['Nome']))
                    novo_tel = st.text_input("Telefone", value=str(dados_cliente['Telefone']))
                with col2:
                    status_opcoes = ["Novo", "Pendente", "Em Negociação", "Fechado", "Cancelado"]
                    # Tenta encontrar a posição do status atual na lista
                    try:
                        idx_status = status_opcoes.index(dados_cliente['Status'])
                    except:
                        idx_status = 0
                    novo_status = st.selectbox("Status", status_opcoes, index=idx_status)
                
                # Tratando a observação para não aparecer 'None' na caixa de texto
                obs_valor = dados_cliente['Observacoes'] if dados_cliente['Observacoes'] and str(dados_cliente['Observacoes']) != 'None' else ""
                nova_obs = st.text_area("Anotações / Observações", value=str(obs_valor))
                
                botao_salvar = st.form_submit_button("Confirmar Alterações")

            if botao_salvar:
                try:
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
            st.error("Erro: Não foi possível localizar o ID deste cliente no banco.")
else:
    st.info("O banco de dados está vazio.")

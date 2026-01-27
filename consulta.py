import streamlit as st
from supabase import create_client, Client
import pandas as pd

# 1. Suas chaves (Mantenha as que você já usa)
URL = "https://zfwdjpklemkuvwizdoly.supabase.co"
KEY = "sb_publishable_qMi5vxWp54WVmmQuoDHkdg_YeaRbiW_" 
supabase = create_client(URL, KEY)

st.title("🔍 Gestão Med Card - Consulta e Edição")

# --- BUSCA DE DADOS ---
resposta = supabase.table("VENDAS").select("*").order("created_at", desc=True).execute()

if resposta.data:
    df = pd.DataFrame(resposta.data)
    
    # Criamos a coluna de data legível
    df['Data'] = pd.to_datetime(df['created_at']).dt.strftime('%d/%m/%Y %H:%M')
    
    # LIMPEZA DE DADOS (IMPEDE O ERRO DO 'NONE')
    # Se o ID ou Nome estiverem vazios por algum erro, nós removemos da lista de edição
    df = df.dropna(subset=['id', 'Nome'])
    
    # TABELA PRINCIPAL
    st.subheader("📋 Lista de Leads")
    st.dataframe(df[["Data", "Nome", "Telefone", "Status", "Observacoes"]], use_container_width=True)

    st.divider()

    # --- ÁREA DE EDIÇÃO ---
    st.subheader("📝 Editar Informações")
    
    # Criamos a lista de seleção garantindo que o ID seja um texto limpo
    df['opcao_selecao'] = df['id'].astype(int).astype(str) + " - " + df['Nome'].astype(str)
    
    escolha = st.selectbox("Selecione o cliente:", [""] + df['opcao_selecao'].tolist())

    if escolha and " - " in escolha:
        try:
            # Extraímos o ID com segurança
            id_escolhido = int(escolha.split(" - ")[0])
            
            # Localizamos os dados exatos desse ID
            dados = df[df['id'] == id_escolhido].iloc[0]

            with st.form("form_edicao_v5"):
                c1, c2 = st.columns(2)
                with c1:
                    nome_ed = st.text_input("Nome", value=str(dados['Nome']))
                    tel_ed = st.text_input("Telefone", value=str(dados['Telefone']))
                with c2:
                    status_opcoes = ["Novo", "Pendente", "Em Negociação", "Fechado", "Cancelado"]
                    try:
                        idx = status_opcoes.index(dados['Status'])
                    except:
                        idx = 0
                    status_ed = st.selectbox("Status", status_opcoes, index=idx)
                
                # Tratamento para Observação (Mostra vazio em vez de 'None')
                obs_v = dados['Observacoes'] if dados['Observacoes'] and str(dados['Observacoes']) != 'None' else ""
                obs_ed = st.text_area("Observações", value=str(obs_v))
                
                btn_salvar = st.form_submit_button("Salvar Alterações")

            if btn_salvar:
                supabase.table("VENDAS").update({
                    "Nome": nome_ed,
                    "Telefone": tel_ed,
                    "Status": status_ed,
                    "Observacoes": obs_ed
                }).eq("id", id_escolhido).execute()
                
                st.success("✅ Atualizado com sucesso!")
                st.rerun()
        except Exception as e:
            st.error(f"Erro ao processar seleção: {e}")
else:
    st.info("Banco de dados vazio.")

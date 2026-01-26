app.py
import streamlit as st
from supabase import create_client, Client

# 1. Configuração visual da página
st.set_page_config(page_title="CRM Douglas - Vendas", page_icon="🚀")

# 2. Dados de Conexão (Use os seus dados do Supabase)
# Dica: No futuro, usaremos 'st.secrets' para maior segurança
URL_PROJETO = "https://zfwdjpklemkuvwizdoly.supabase.co"
CHAVE_API = "sb_publishable_qMi5vxWp54WVmmQuoDHkdg_YeaRbiW_" 

supabase: Client = create_client(URL_PROJETO, CHAVE_API)

# 3. Interface do Site
st.title("📋 Cadastro de Leads")
st.write("Preencha os dados abaixo para salvar diretamente no banco de dados.")

# Criando o formulário
with st.form("form_vendas", clear_on_submit=True):
    nome_cliente = st.text_input("Nome Completo")
    telefone_cliente = st.text_input("Telefone / WhatsApp")
    status_venda = st.selectbox("Status da Negociação", ["Novo", "Em Negociação", "Pendente", "Fechado"])
    
    # Botão de envio
    botao_cadastrar = st.form_submit_button("Cadastrar no CRM")

# 4. Lógica para salvar no Supabase
if botao_cadastrar:
    if nome_cliente and telefone_cliente:
        try:
            # Organizando os dados para a tabela VENDAS
            dados_para_salvar = {
                "Nome": nome_cliente,
                "Telefone": telefone_cliente,
                "Status": status_venda
            }
            
            # Executando o comando de inserção
            supabase.table("VENDAS").insert(dados_para_salvar).execute()
            
            st.success(f"✅ Sucesso! {nome_cliente} foi adicionado à lista.")
        except Exception as e:
            st.error(f"❌ Erro ao salvar no banco de dados: {e}")
    else:
        st.warning("⚠️ Por favor, preencha o Nome e o Telefone antes de salvar.")

# Rodapé simples
st.markdown("---")
st.caption("Sistema desenvolvido para Consultoria Financeira e Plano Med Card.") 

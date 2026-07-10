import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Calculadora de Gaxetas", layout="wide", page_icon="🧮")

st.title("📊 Calculadora de Preços - Peças Soldadas")
st.markdown("---")

# Inicializar o carrinho de orçamento no estado da sessão se não existir
if "orcamento" not in st.session_state:
    st.session_state.orcamento = []

# --- PAINEL LATERAL: CADASTRO / CONFIGURAÇÃO DE PREÇOS ---
# (Em um cenário real, isso poderia vir de um banco de dados ou planilha)
st.sidebar.header("⚙️ Configuração de Preço por Metro")
perfil_selecionado = st.sidebar.selectbox("Selecione o Perfil", ["P001", "P002", "P003"])

# Baseado na sua imagem:
# Preço Consumidor (R$ 30,00/m) | Preço Instalador/Revenda (R$ 25,00/m) | Preço de Compra (R$ 10,00/m)
preco_compra_m = st.sidebar.number_input("Preço de Compra por Metro (R$)", value=10.00, step=1.00)
preco_instalador_m = st.sidebar.number_input("Preço Ideal/Instalador por Metro (R$)", value=25.00, step=1.00)
preco_consumidor_m = st.sidebar.number_input("Preço Negociável/Consumidor por Metro (R$)", value=30.00, step=1.00)

st.sidebar.markdown("---")

# --- FORMULÁRIO DE ENTRADA DO ITEM ---
st.subheader("➕ Adicionar Item ao Orçamento")

col1, col2, col3, col4 = st.columns(4)

with col1:
    altura = st.number_input("MEDIDA - A (Altura em mm)", min_value=0, value=1150, step=10)
with col2:
    largura = st.number_input("MEDIDA - B (Largura em mm)", min_value=0, value=560, step=10)
with col3:
    quantidade = st.number_input("Quantidade", min_value=1, value=2, step=1)
with col4:
    tipo_preco = st.selectbox("Tabela de Preço", ["Consumidor (Balcão)", "Instalador (Revenda)"])

# --- CÁLCULOS METRO LINEAR ---
# Perímetro em metros: (A + A + B + B) / 1000
perimetro_metros = ((altura * 2) + (largura * 2)) / 1000

# Definindo o preço por metro com base na seleção
if tipo_preco == "Consumidor (Balcão)":
    preco_metro_atual = preco_consumidor_m
else:
    preco_metro_atual = preco_instalador_m

# Valor Unitário e Valor Total
valor_unitario = perimetro_metros * preco_metro_atual
valor_total_item = valor_unitario * quantidade

# Exibição rápida do cálculo atual
st.info(f"**Cálculo Atual:** Unidade: R$ {valor_unitario:.2f} | Total ({quantidade}x): R$ {valor_total_item:.2f} *(Metragem por peça: {perimetro_metros:.2f}m)*")

# Botão para adicionar ao orçamento
if st.button("🛒 Adicionar ao Orçamento"):
    item = {
        "Perfil": perfil_selecionado,
        "Medidas": f"{altura}x{largura} mm",
        "Qtd": quantidade,
        "Tipo": tipo_preco,
        "Val. Unitário (R$)": round(valor_unitario, 2),
        "Total (R$)": round(valor_total_item, 2)
    }
    st.session_state.orcamento.append(item)
    st.success("Item adicionado com sucesso!")
    st.rerun()

# --- TABELA DE ORÇAMENTO ---
st.markdown("---")
st.subheader("📋 Detalhes do Orçamento")

if st.session_state.orcamento:
    # Converter a lista de dicionários em um DataFrame do Pandas para exibir bonito
    df_orcamento = pd.DataFrame(st.session_state.orcamento)
    
    # Exibir a tabela
    st.dataframe(df_orcamento, use_container_width=True)
    
    # Resumo financeiro do orçamento
    total_geral = df_orcamento["Total (R$)"].sum()
    
    col_tot1, col_tot2 = st.columns([3, 1])
    with col_tot2:
        st.markdown(f"### **Total Geral: R$ {total_geral:.2f}**")
    
    # Botão para limpar orçamento
    if st.button("🗑️ Limpar Orçamento"):
        st.session_state.orcamento = []
        st.rerun()
else:
    st.write("Nenhum item adicionado ao orçamento ainda.")

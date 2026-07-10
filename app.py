import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Calculadora de Gaxetas", layout="wide", page_icon="🧮")

st.title("📊 Calculadora de Preços - Peças Soldadas")
st.markdown("---")

# Inicializar o carrinho de orçamento no estado da sessão se não existir
if "orcamento" not in st.session_state:
    st.session_state.orcamento = []

# --- PAINEL LATERAL: CONFIGURAÇÃO DE PREÇO POR METRO ---
st.sidebar.header("⚙️ Valores de Referência (por Metro)")
preco_compra_m = st.sidebar.number_input("Preço de Compra (R$)", value=10.00, step=1.00)
preco_instalador_m = st.sidebar.number_input("Preço Instalador / Revenda (R$)", value=25.00, step=1.00)
preco_consumidor_m = st.sidebar.number_input("Preço Consumidor / Balcão (R$)", value=30.00, step=1.00)

st.sidebar.markdown("---")
st.sidebar.write("💡 Altere os valores acima para ajustar a base de cálculo global do metro linear.")

# --- FORMULÁRIO DE ENTRADA DO ITEM (CENTRO DA TELA) ---
st.subheader("➕ Adicionar Item ao Orçamento")

# Lista completa de perfis enviada por você
lista_perfis = [
    "P001", "P002", "P004", "P005", "P006", "P007", "P008", "P010", "P012", "P015",
    "P016", "P017", "P018", "P019", "P022", "P023", "P026", "P027", "P030", "P032",
    "P035", "P045", "P096", "P099", "P121", "P171", "P170", "P390", "P391", "P392",
    "P380", "P560", "P172", "P173", "P393", "P033", "P029", "P394", "P086", "P087",
    "P088", "P083", "P084", "P082"
]

# Grid de inputs no centro da tela dividido em 5 colunas
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    perfil_selecionado = st.selectbox("Selecione o Perfil", lista_perfis)
with col2:
    altura = st.number_input("MEDIDA - A (Altura em mm)", min_value=0, value=1150, step=10)
with col3:
    largura = st.number_input("MEDIDA - B (Largura em mm)", min_value=0, value=560, step=10)
with col4:
    quantidade = st.number_input("Quantidade", min_value=1, value=2, step=1)
with col5:
    tipo_preco = st.selectbox("Tabela de Preço", ["Consumidor (Balcão)", "Instalador (Revenda)"])

# --- CÁLCULOS METRO LINEAR ---
# Perímetro em metros: (A + A + B + B) / 1000
perimetro_metros = ((altura * 2) + (largura * 2)) / 1000

# Definindo o preço por metro com base na seleção da tabela
if tipo_preco == "Consumidor (Balcão)":
    preco_metro_atual = preco_consumidor_m
else:
    preco_metro_atual = preco_instalador_m

# Valor Unitário e Valor Total do Item atual
valor_unitario = perimetro_metros * preco_metro_atual
valor_total_item = valor_unitario * quantidade

# Exibição do cálculo rápido em tempo real antes de adicionar
st.info(
    f"**Visualização do Item:** Perfil: {perfil_selecionado} | "
    f"Metragem: {perimetro_metros:.2f}m | "
    f"Preço Unitário: R$ {valor_unitario:.2f} | "
    f"Total ({quantidade}x): R$ {valor_total_item:.2f}"
)

# Botão para adicionar ao orçamento
if st.button("🛒 Adicionar ao Orçamento", use_container_width=True):
    item = {
        "Perfil": perfil_selecionado,
        "Medidas (mm)": f"{altura}x{largura}",
        "Qtd": quantidade,
        "Tabela": tipo_preco,
        "Val. Unitário (R$)": round(valor_unitario, 2),
        "Total (R$)": round(valor_total_item, 2)
    }
    st.session_state.orcamento.append(item)
    st.success(f"Perfil {perfil_selecionado} adicionado ao orçamento!")
    st.rerun()

# --- TABELA DE ORÇAMENTO ---
st.markdown("---")
st.subheader("📋 Detalhes do Orçamento Multitens")

if st.session_state.orcamento:
    # Converter a lista de itens armazenada em um DataFrame do Pandas
    df_orcamento = pd.DataFrame(st.session_state.orcamento)
    
    # Exibir a tabela com todos os itens adicionados (cada um pode ter seu perfil)
    st.dataframe(df_orcamento, use_container_width=True, hide_index=True)
    
    # Resumo financeiro final
    total_geral = df_orcamento["Total (R$)"].sum()
    
    col_tot1, col_tot2 = st.columns([3, 1])
    with col_tot2:
        st.markdown(f"### **Total Geral: R$ {total_geral:.2f}**")
    
    # Opção para limpar a lista e começar de novo
    if st.button("🗑️ Limpar Todo o Orçamento"):
        st.session_state.orcamento = []
        st.rerun()
else:
    st.write("Nenhum item adicionado ao orçamento ainda. Selecione o perfil e medidas acima para começar.")

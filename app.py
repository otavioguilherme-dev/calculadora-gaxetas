import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Calculadora Ognet-Shop", layout="wide", page_icon="🧮")

# --- ESTILIZAÇÃO DO LOGOTIPO E DADOS DA EMPRESA (image_79ef50.png) ---
st.markdown(
    """
    <div style="display: flex; flex-direction: row; justify-content: space-between; align-items: center; 
                background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #e2e8f0; margin-bottom: 25px; gap: 20px;">
        <div style="display: flex; align-items: center; gap: 20px;">
            <svg width="85" height="85" viewBox="0 0 120 120">
                <rect x="10" y="10" width="100" height="100" rx="15" fill="#f8fafc" stroke="#1e3a8a" stroke-width="2"/>
                <circle cx="55" cy="55" r="35" fill="none" stroke="#1e3a8a" stroke-width="7"/>
                <circle cx="55" cy="55" r="28" fill="#c2410c" opacity="0.15"/>
                <text x="55" y="67" font-family="sans-serif" font-weight="bold" font-size="34" fill="#1e3a8a" text-anchor="middle">G</text>
                <text x="55" y="102" font-family="sans-serif" font-weight="900" font-size="12" fill="#1e3a8a" letter-spacing="2" text-anchor="middle">SHOP</text>
                <rect x="92" y="15" width="18" height="90" rx="4" fill="#c2410c"/>
                <text x="101" y="30" font-family="sans-serif" font-weight="bold" font-size="11" fill="#ffffff" text-anchor="middle">O</text>
                <text x="101" y="47" font-family="sans-serif" font-weight="bold" font-size="11" fill="#ffffff" text-anchor="middle">G</text>
                <text x="101" y="64" font-family="sans-serif" font-weight="bold" font-size="11" fill="#ffffff" text-anchor="middle">N</text>
                <text x="101" y="81" font-family="sans-serif" font-weight="bold" font-size="11" fill="#ffffff" text-anchor="middle">E</text>
                <text x="101" y="98" font-family="sans-serif" font-weight="bold" font-size="11" fill="#ffffff" text-anchor="middle">T</text>
            </svg>
            <div>
                <h2 style="margin: 0; color: #1e3a8a; font-family: sans-serif; font-size: 22px; font-weight: 700;">REFRIGERAÇÃO OGNET-SHOP</h2>
                <p style="margin: 2px 0; color: #64748b; font-family: sans-serif; font-size: 11px; font-weight: 600; text-transform: uppercase;">Otavio Guilherme Teixeira de Souza Neto</p>
                <p style="margin: 0; color: #334155; font-family: sans-serif; font-size: 12px;">
                    <strong>CNPJ:</strong> 38.233.044/0001-34 | <strong>I.E.:</strong> 799.313.829.119 | <strong>Tel:</strong> 11 994251306<br>
                    <strong>Endereço:</strong> Rua João Basso n 20, Sala 1 Centro São Bernardo do Campo-SP | <strong>E-mail:</strong> vendas@ognet.com.br
                </p>
            </div>
        </div>
        <div style="text-align: right; border-left: 1px solid #e2e8f0; padding-left: 20px;">
            <span style="background-color: #dbeafe; color: #1e40af; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 12px;">ORÇAMENTO DIGITAL</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Inicializar o carrinho de orçamento no estado da sessão se não existir
if "orcamento" not in st.session_state:
    st.session_state.orcamento = []

# --- PAINEL LATERAL: CONFIGURAÇÃO DE PREÇO POR METRO ---
st.sidebar.header("⚙️ Valores Globais (por Metro)")
preco_instalador_m = st.sidebar.number_input("Preço Instalador / Revenda (R$)", value=25.00, step=1.00)
preco_consumidor_m = st.sidebar.number_input("Preço Consumidor / Balcão (R$)", value=30.00, step=1.00)

# --- CAMPOS DO CLIENTE ---
st.subheader("👤 Dados do Cliente e Envio")
col_c1, col_c2, col_c3, col_c4 = st.columns([2, 1, 1, 1])
with col_c1:
    nome_cliente = st.text_input("Razão Social / Nome", placeholder="Digite o nome do cliente", value="")
with col_c2:
    cnpj_cliente = st.text_input("CPF / CNPJ", placeholder="00.000.000/0001-00", value="")
with col_c3:
    data_emissao = st.date_input("Data de Geração", datetime.now())
with col_c4:
    valor_frete = st.number_input("Valor do Frete (R$)", min_value=0.00, value=0.00, step=5.00)

st.markdown("---")

# --- FORMULÁRIO DE ENTRADA DO ITEM ---
st.subheader("➕ Adicionar Item")

lista_perfis = [
    "P001", "P002", "P004", "P005", "P006", "P007", "P008", "P010", "P012", "P015",
    "P016", "P017", "P018", "P019", "P022", "P023", "P026", "P027", "P030", "P032",
    "P035", "P045", "P096", "P099", "P121", "P171", "P170", "P390", "P391", "P392",
    "P380", "P560", "P172", "P173", "P393", "P033", "P029", "P394", "P086", "P087",
    "P088", "P083", "P084", "P082"
]

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    quantidade = st.number_input("QTD", min_value=1, value=2, step=1)
with col2:
    altura = st.number_input("MEDIDA A (Altura mm)", min_value=0, value=1150, step=10)
with col3:
    largura = st.number_input("MEDIDA B (Largura mm)", min_value=0, value=560, step=10)
with col4:
    perfil_selecionado = st.selectbox("PERFIL", lista_perfis)
with col5:
    cor_selecionada = st.selectbox("COR", ["PRETO", "CINZA CLARO", "CINZA GRAFITE"])
with col6:
    tipo_preco = st.selectbox("TABELA", ["Consumidor", "Instalador"])

# --- CÁLCULOS ---
perimetro_metros = ((altura * 2) + (largura * 2)) / 1000

if tipo_preco == "Consumidor":
    preco_metro_atual = preco_consumidor_m
else:
    preco_metro_atual = preco_instalador_m

valor_unitario = perimetro_metros * preco_metro_atual
valor_total_item = valor_unitario * quantidade

# Botão para adicionar
if st.button("🛒 Adicionar Item ao Orçamento", use_container_width=True):
    item = {
        "QTD": quantidade,
        "MEDIDAS": f"{altura}x{largura} mm",
        "PERFIL": perfil_selecionado,
        "COR": cor_selecionada,
        "VALOR UNITARIO": round(valor_unitario, 2),
        "VALOR TOTAL": round(valor_total_item, 2)
    }
    st.session_state.orcamento.append(item)
    st.rerun()

# --- DETALHE DO ORÇAMENTO ---
st.markdown("---")
st.subheader("📋 Detalhes do Orçamento")

if st.session_state.orcamento:
    df_orcamento = pd.DataFrame(st.session_state.orcamento)
    
    ordem_colunas = ["QTD", "MEDIDAS", "PERFIL", "COR", "VALOR UNITARIO", "VALOR TOTAL"]
    df_orcamento = df_orcamento[ordem_colunas]
    
    df_exibicao = df_orcamento.copy()
    df_exibicao["VALOR UNITARIO"] = df_exibicao["VALOR UNITARIO"].map("R$ {:.2f}".format)
    df_exibicao["VALOR TOTAL"] = df_exibicao["VALOR TOTAL"].map("R$ {:.2f}".format)
    
    st.dataframe(df_exibicao, use_container_width=True, hide_index=True)
    
    # Cálculos Finais
    subtotal = df_orcamento["VALOR TOTAL"].sum()
    total_geral = subtotal + valor_frete
    
    col_t1, col_t2 = st.columns([2, 1])
    with col_t2:
        st.markdown(f"**Subtotal dos Itens:** R$ {subtotal:.2f}")
        st.markdown(f"**Frete:** R$ {valor_frete:.2f}")
        st.markdown(f"### **TOTAL GERAL: R$ {total_geral:.2f}**")
    
    # --- CONSTRUÇÃO DO DOCUMENTO PARA DOWNLOAD E PRÉVIA ---
    data_formatada = data_emissao.strftime('%d/%m/%Y')
    
    # Monta as linhas da tabela em HTML
    linhas_html = ""
    for _, row in df_orcamento.iterrows():
        linhas_html += f"""
        <tr>
            <td style="padding: 8px; text-align: center; border-bottom: 1px solid #e2e8f0;">{row['QTD']}</td>
            <td style="padding: 8px; border-bottom: 1px solid #e2e8f0;">{row['MEDIDAS']}</td>
            <td style="padding: 8px; border-bottom: 1px solid #e2e8f0;"><strong>{row['PERFIL']}</strong></td>
            <td style="padding: 8px; border-bottom: 1px solid #e2e8f0;">{row['COR']}</td>
            <td style="padding: 8px; text-align: right; border-bottom: 1px solid #e2e8f0;">R$ {row['VALOR UNITARIO']:.2f}</td>
            <td style="padding: 8px; text-align: right; border-bottom: 1px solid #e2e8f0;"><strong>R$ {row['VALOR TOTAL']:.2f}</strong></td>
        </tr>
        """
    
    html_template = f"""
    <div style="font-family: sans-serif; color: #334155; padding: 25px; background: white; border: 1px solid #cbd5e1; border-radius: 8px; max-width: 800px; margin: auto;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #1e3a8a; padding-bottom: 15px; margin-bottom: 20px;">
            <div>
                <h2 style="margin:0; color:#1e3a8a; font-size: 20px;">REFRIGERAÇÃO OGNET-SHOP</h2>
                <div style="font-size: 11px; margin-top:5px; line-height: 1.4; color: #475569;">
                    Otavio Guilherme Teixeira de Souza Neto<br>
                    <strong>CNPJ:</strong> 38.233.044/0001-34 | <strong>I.E.:</strong> 799.313.829.119<br>
                    Rua João Basso n 20, Sala 1 Centro São Bernardo do Campo-SP<br>
                    <strong>Tel:</strong> 11 994251306 | <strong>E-mail:</strong> vendas@ognet.com.br
                </div>
            </div>
            <div style="text-align: right;">
                <span style="background-color: #1e3a8a; color: white; padding: 4px 10px; font-weight: bold; border-radius: 4px; font-size: 11px;">ORÇAMENTO</span>
            </div>
        </div>

        <div style="background-color: #f8fafc; padding: 12px; border-radius: 6px; border: 1px solid #e2e8f0; margin-bottom: 20px; font-size: 12px; line-height: 1.5;">
            <h4 style="margin: 0 0 5px 0; color: #1e3a8a; font-size: 13px;">DADOS DO CLIENTE</h4>
            <strong>Cliente / Razão Social:</strong> {nome_cliente if nome_cliente else 'Não Informado'}<br>
            <strong>CPF / CNPJ:</strong> {cnpj_cliente if cnpj_cliente else 'Não Informado'}<br>
            <strong>Data de Emissão:</strong> {data_formatada}
        </div>

        <table style="width: 100%; border-collapse: collapse; font-size: 12px; margin-bottom: 20px;">
            <thead>
                <tr style="background-color: #f1f5f9; text-align: left;">
                    <th style="padding: 8px; text-align: center; border-bottom: 2px solid #cbd5e1;">QTD</th>
                    <th style="padding: 8px; border-bottom: 2px solid #cbd5e1;">MEDIDAS</th>
                    <th style="padding: 8px; border-bottom: 2px solid #cbd5e1;">PERFIL</th>
                    <th style="padding: 8px; border-bottom: 2px solid #cbd5e1;">COR</th>
                    <th style="padding: 8px; text-align: right; border-bottom: 2px solid #cbd5e1;">VALOR UNITÁRIO</th>
                    <th style="padding: 8px; text-align: right; border-bottom: 2px solid #cbd5e1;">VALOR TOTAL</th>
                </tr>
            </thead>
            <tbody>
                {linhas_html}
            </tbody>
        </table>

        <div style="text-align: right; font-size: 13px; margin-top: 15px; line-height: 1.5;">
            <span>Subtotal dos Itens: R$ {subtotal:.2f}</span><br>
            <span>Valor do Frete: R$ {valor_frete:.2f}</span><br>
            <strong style="font-size: 16px; color: #1e3a8a;">TOTAL GERAL: R$ {total_geral:.2f}</strong>
        </div>

        <div style="margin-top: 35px; text-align: center; font-size: 10px; color: #94a3b8; border-top: 1px solid #e2e8f0; padding-top: 10px;">
            * Peças fabricadas sob medida. Orçamento válido por 10 dias.<br>
            Obrigado pela preferência!
        </div>
    </div>
    """

    # Layout de botões de controle
    col_b1, col_b2 = st.columns([1, 4])
    with col_b1:
        if st.button("🗑️ Limpar Lista", use_container_width=True):
            st.session_state.orcamento = []
            st.rerun()
            
    with col_b2:
        # Usa o recurso nativo do Streamlit para baixar arquivos HTML que abrem e imprimem direto de qualquer PC/Celular
        st.download_button(
            label="💾 Baixar Documento de Orçamento (HTML/PDF)",
            data=html_template,
            file_name=f"Orcamento_{nome_cliente.replace(' ', '_') if nome_cliente else 'Cliente'}_{datetime.now().strftime('%d%m%Y')}.html",
            mime="text/html",
            use_container_width=True,
            type="primary"
        )
        
    # --- ÁREA DE PRÉ-VISUALIZAÇÃO FISCAL NA TELA ---
    st.markdown("---")
    st.subheader("👁️ Espelho do Orçamento para Envio")
    st.markdown("Abaixo está a visualização exata de como o arquivo salvo vai abrir para o cliente:")

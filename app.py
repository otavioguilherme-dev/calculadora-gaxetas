import streamlit as st
import pandas as pd
from datetime import datetime
import requests
import base64
from io import BytesIO
from xhtml2pdf import pisa

st.set_page_config(page_title="OGNET BORRACHAS", layout="wide", page_icon="🧮")

# --- FUNÇÕES DE APOIO ---
def format_brl(valor):
    """Formata os números para o padrão de moeda brasileiro (R$ 1.500,00)"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

@st.cache_data
def get_logo_base64():
    """Baixa o logo para a memória do servidor para o PDF não quebrar"""
    url = "https://agent-whatsapp.streamlit.app/~/+/media/a3d2d8b206613ad841cb11e9bf12f484.jpg"
    try:
        response = requests.get(url)
        return base64.b64encode(response.content).decode()
    except:
        return ""

logo_b64 = get_logo_base64()
logo_src = f"data:image/jpeg;base64,{logo_b64}" if logo_b64 else ""

logo_html = f"""
<div style='display: flex; justify-content: center; align-items: center; margin-bottom: 10px;'>
    <img src='{logo_src}' style='max-height: 85px; width: auto; object-fit: contain;'>
</div>
"""

# Renderização do cabeçalho da loja na tela do sistema
st.markdown(
    f"""
    <div style='display: flex; flex-direction: row; justify-content: space-between; align-items: center; 
                background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #e2e8f0; margin-bottom: 25px; gap: 20px;'>
        <div style='display: flex; align-items: center; gap: 25px; flex-wrap: wrap;'>
            <div>{logo_html}</div>
            <div style='border-left: 2px solid #e2e8f0; padding-left: 25px; min-width: 280px;'>
                <h3 style='margin: 0; color: #1e3a8a; font-family: sans-serif; font-size: 16px; font-weight: 700;'>OTAVIO GUILHERME TEIXEIRA DE SOUZA NETO</h3>
                <p style='margin: 4px 0 0 0; color: #475569; font-family: sans-serif; font-size: 12px; line-height: 1.5;'>
                    <strong>CNPJ:</strong> 38.233.044/0001-34 | <strong>I.E.:</strong> 799.313.829.119<br>
                    <strong>Endereço:</strong> Rua João Basso, nº 20, Sala 1 Centro - São Bernardo do Campo-SP<br>
                    <strong>Contato:</strong> (11) 99425-1306 | <strong>E-mail:</strong> vendas@ognet.com.br
                </p>
            </div>
        </div>
        <div style='text-align: right;'>
            <span style='background-color: #f1f5f9; color: #1e2b7a; font-size: 11px; font-weight: 800; padding: 6px 12px; border-radius: 8px; border: 1px solid #cbd5e1; letter-spacing: 0.5px;'>SISTEMA DE ORÇAMENTOS</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

if "orcamento" not in st.session_state:
    st.session_state.orcamento = []

# --- PAINEL LATERAL ---
st.sidebar.header("⚙️ Valores Globais (por Metro)")
preco_instalador_m = st.sidebar.number_input("Preço Instalador / Revenda (R$)", value=25.00, step=1.00)
preco_consumidor_m = st.sidebar.number_input("Preço Consumidor / Balcão (R$)", value=30.00, step=1.00)

# --- CAMPOS DO CLIENTE ---
st.subheader("👤 Dados do Cliente e Envio")
col_c1, col_c2, col_c3, col_c4 = st.columns([2, 1, 1, 1])
with col_c1:
    nome_cliente = st.text_input("Razão Social / Nome", placeholder="Digite o nome do cliente")
with col_c2:
    cnpj_cliente = st.text_input("CPF / CNPJ", placeholder="00.000.000/0001-00")
with col_c3:
    data_emissao = st.date_input("Data de Geração", datetime.now())
with col_c4:
    valor_frete = st.number_input("Valor do Frete (R$)", min_value=0.00, value=0.00, step=5.00)

st.markdown("---")

# --- FORMULÁRIO DE ENTRADA DE ITENS (ABAS) ---
st.subheader("➕ Adicionar Item ao Orçamento")

aba_gaxetas, aba_outros = st.tabs(["🔲 Gaxetas / Borrachas Sob Medida", "📦 Outros Produtos (Inclusão Manual)"])

# ABA 1: GAXETAS E BORRACHAS
with aba_gaxetas:
    lista_perfis = [
        "P001", "P002", "P004", "P005", "P006", "P007", "P008", "P010", "P012", "P015",
        "P016", "P017", "P018", "P019", "P022", "P023", "P026", "P027", "P030", "P032",
        "P035", "P045", "P096", "P099", "P121", "P171", "P170", "P390", "P391", "P392",
        "P380", "P560", "P172", "P173", "P393", "P033", "P029", "P394", "P086", "P087",
        "P088", "P083", "P084", "P082"
    ]

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        quantidade_gaxeta = st.number_input("QTD", min_value=1, value=2, step=1, key="qtd_gaxeta")
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

    perimetro_metros = ((altura * 2) + (largura * 2)) / 1000
    preco_metro_atual = preco_consumidor_m if tipo_preco == "Consumidor" else preco_instalador_m

    valor_unitario_gaxeta = perimetro_metros * preco_metro_atual
    valor_total_gaxeta = valor_unitario_gaxeta * quantidade_gaxeta

    if st.button("🛒 Adicionar Borracha/Gaxeta", use_container_width=True):
        item = {
            "QTD": quantidade_gaxeta,
            "MEDIDAS": f"{altura}x{largura} mm",
            "PERFIL": perfil_selecionado,
            "COR": cor_selecionada,
            "VALOR UNITARIO": valor_unitario_gaxeta,
            "VALOR TOTAL": valor_total_gaxeta
        }
        st.session_state.orcamento.append(item)
        st.rerun()

# ABA 2: OUTROS PRODUTOS (MANUAL)
with aba_outros:
    st.markdown("Preencha os dados abaixo para adicionar qualquer outro produto ao orçamento:")
    col_m1, col_m2, col_m3 = st.columns([1, 3, 1])
    with col_m1:
        qtd_manual = st.number_input("QTD", min_value=1, value=1, step=1, key="qtd_manual")
    with col_m2:
        desc_manual = st.text_input("Descrição / Modelo do Produto", placeholder="Ex: Cola Especial, Bandeja Náutica, etc.")
    with col_m3:
        preco_manual = st.number_input("Preço Unitário (R$)", min_value=0.00, value=0.00, step=1.00)

    valor_total_manual = qtd_manual * preco_manual

    if st.button("➕ Adicionar Produto Diversos", use_container_width=True, type="secondary"):
        if desc_manual.strip() == "":
            st.warning("⚠️ Por favor, digite uma descrição para o produto.")
        else:
            item_manual = {
                "QTD": qtd_manual,
                "MEDIDAS": "-",
                "PERFIL": desc_manual,
                "COR": "-",
                "VALOR UNITARIO": preco_manual,
                "VALOR TOTAL": valor_total_manual
            }
            st.session_state.orcamento.append(item_manual)
            st.rerun()

# --- DETALHE DO ORÇAMENTO ---
st.markdown("---")
st.subheader("📋 Detalhes do Orçamento")

if st.session_state.orcamento:
    df_orcamento = pd.DataFrame(st.session_state.orcamento)
    ordem_colunas = ["QTD", "MEDIDAS", "PERFIL", "COR", "VALOR UNITARIO", "VALOR TOTAL"]
    df_orcamento = df_orcamento[ordem_colunas]
    
    # Formatação apenas para a exibição na tela
    df_exibicao = df_orcamento.copy()
    df_exibicao["VALOR UNITARIO"] = df_exibicao["VALOR UNITARIO"].apply(format_brl)
    df_exibicao["VALOR TOTAL"] = df_exibicao["VALOR TOTAL"].apply(format_brl)
    
    st.dataframe(df_exibicao, use_container_width=True, hide_index=True)
    
    subtotal = df_orcamento["VALOR TOTAL"].sum()
    total_geral = subtotal + valor_frete
    
    col_t1, col_t2 = st.columns([2, 1])
    with col_t2:
        st.markdown(f"**Subtotal dos Itens:** {format_brl(subtotal)}")
        st.markdown(f"**Frete de Envio:** {format_brl(valor_frete)}")
        st.markdown(f"### **TOTAL GERAL: {format_brl(total_geral)}**")
    
    # --- CONSTRUÇÃO DO PDF NATIVO VIA XHTML2PDF ---
    data_formatada = data_emissao.strftime('%d/%m/%Y')
    
    linhas_html = ""
    for _, row in df_orcamento.iterrows():
        linhas_html += f"""
        <tr>
            <td align="center">{row['QTD']}</td>
            <td>{row['MEDIDAS']}</td>
            <td style="color:#1e2b7a; font-weight:bold;">{row['PERFIL']}</td>
            <td>{row['COR']}</td>
            <td align="right">{format_brl(row['VALOR UNITARIO'])}</td>
            <td align="right" style="font-weight:bold;">{format_brl(row['VALOR TOTAL'])}</td>
        </tr>
        """

    img_tag = f'<img src="{logo_src}" style="height: 60px;"><br>' if logo_src else ''

    # Template HTML estruturado especificamente para a biblioteca xhtml2pdf
    html_template = f"""
    <html>
    <head>
    <style>
        @page {{ size: A4; margin: 1cm; }}
        body {{ font-family: Helvetica, sans-serif; font-size: 12px; color: #334155; }}
        .center {{ text-align: center; }}
        .right {{ text-align: right; }}
        .title-box {{ background-color: #1e2b7a; color: white; padding: 8px; font-weight: bold; font-size: 13px; text-align: center; border-radius: 4px; }}
        .client-box {{ background-color: #f8fafc; padding: 12px; border: 1px solid #e2e8f0; border-radius: 4px; }}
        
        .table-items {{ width: 100%; border-collapse: collapse; margin-bottom: 25px; }}
        .table-items th {{ background-color: #f1f5f9; padding: 8px; border-bottom: 2px solid #cbd5e1; color: #475569; text-align: left; }}
        .table-items td {{ padding: 8px; border-bottom: 1px solid #e2e8f0; }}
    </style>
    </head>
    <body>

    <table width="100%" style="border-bottom: 2px solid #1e2b7a; padding-bottom: 15px; margin-bottom: 20px;">
        <tr>
            <td width="65%" valign="middle">
                {img_tag}
                <div style="font-size: 10px; color: #475569; margin-top: 10px; line-height: 1.4;">
                    <strong>Razão Social:</strong> OTAVIO GUILHERME TEIXEIRA DE SOUZA NETO<br>
                    <strong>CNPJ:</strong> 38.233.044/0001-34 | <strong>I.E.:</strong> 799.313.829.119<br>
                    Rua João Basso, nº 20, Sala 1 Centro - São Bernardo do Campo-SP<br>
                    <strong>Telefone:</strong> (11) 99425-1306 | <strong>E-mail:</strong> vendas@ognet.com.br
                </div>
            </td>
            <td width="35%" valign="top" align="right">
                <div class="title-box">ORÇAMENTO COMERCIAL</div>
            </td>
        </tr>
    </table>

    <div class="client-box" style="margin-bottom: 20px;">
        <div style="color: #1e2b7a; font-size: 13px; font-weight: bold; margin-bottom: 8px; border-bottom: 1px solid #e2e8f0; padding-bottom: 4px;">DADOS DO CLIENTE</div>
        <strong>Cliente / Razão Social:</strong> {nome_cliente if nome_cliente else 'Não Informado'}<br>
        <strong>CPF / CNPJ:</strong> {cnpj_cliente if cnpj_cliente else 'Não Informado'}<br>
        <strong>Data de Emissão:</strong> {data_formatada}
    </div>

    <table class="table-items">
        <tr>
            <th width="8%" class="center">QTD</th>
            <th width="22%">MEDIDAS</th>
            <th width="35%">PRODUTO / PERFIL</th>
            <th width="10%">COR</th>
            <th width="12%" class="right">UNITÁRIO</th>
            <th width="13%" class="right">TOTAL</th>
        </tr>
        {linhas_html}
    </table>

    <table width="100%" border="0">
        <tr>
            <td width="50%"></td>
            <td width="50%" class="right" style="line-height: 1.6;">
                <span style="color: #64748b;">Subtotal dos Itens:</span> {format_brl(subtotal)}<br>
                <span style="color: #64748b;">Valor do Frete:</span> {format_brl(valor_frete)}<br>
                <br>
                <span style="font-size: 18px; color: #1e2b7a; font-weight: bold;">TOTAL GERAL: {format_brl(total_geral)}</span>
            </td>
        </tr>
    </table>

    <div class="center" style="font-size: 10px; color: #94a3b8; margin-top: 50px; border-top: 1px solid #e2e8f0; padding-top: 15px;">
        * Peças industriais fabricadas sob medida e especificações técnicas solicitadas.<br>
        <strong>Prazo de Validade deste documento:</strong> 10 dias a contar da data de emissão.
    </div>

    </body>
    </html>
    """

    # Função que transforma o HTML estruturado acima em um arquivo PDF real
    def criar_pdf(html_content):
        pdf_buffer = BytesIO()
        pisa.CreatePDF(BytesIO(html_content.encode('utf-8')), dest=pdf_buffer)
        return pdf_buffer.getvalue()

    col_b1, col_b2 = st.columns([1, 4])
    with col_b1:
        if st.button("🗑️ Limpar Lista", use_container_width=True):
            st.session_state.orcamento = []
            st.rerun()
            
    with col_b2:
        # Lógica para nome do arquivo: Usa o nome do cliente se preenchido, senão 'Cliente'
        nome_arquivo = nome_cliente.strip().replace(" ", "_") if nome_cliente.strip() else "Cliente"
        data_arquivo = datetime.now().strftime('%d%m%Y')
        nome_completo_arquivo = f"Orcamento_{nome_arquivo}_{data_arquivo}.pdf"

        # Botão de download
        st.download_button(
            label=f"💾 Baixar Documento ({nome_completo_arquivo})",
            data=criar_pdf(html_template),
            file_name=nome_completo_arquivo,
            mime="application/pdf",
            use_container_width=True,
            type="primary"
        )

else:
    st.info("Nenhum item adicionado ao orçamento.")

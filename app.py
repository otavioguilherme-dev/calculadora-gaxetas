import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="OGNET BORRACHAS", layout="wide", page_icon="🧮")

# --- LOGOTIPO HOSPEDADO NO STREAMLIT ---
logo_url = "https://agent-whatsapp.streamlit.app/~/+/media/a3d2d8b206613ad841cb11e9bf12f484.jpg"

logo_html = f"""
<div style='display: flex; justify-content: center; align-items: center; margin-bottom: 10px;'>
    <img src='{logo_url}' style='max-height: 85px; width: auto; object-fit: contain;'>
</div>
"""

# Renderização do cabeçalho da loja (OGNET BORRACHAS)
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

# Criação de duas abas para separar os tipos de produtos
aba_gaxetas, aba_outros = st.tabs(["🔲 Gaxetas / Borrachas Sob Medida", "📦 Outros Produtos (Inclusão Manual)"])

# ABA 1: LÓGICA ORIGINAL DE GAXETAS E BORRACHAS
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
            "VALOR UNITARIO": round(valor_unitario_gaxeta, 2),
            "VALOR TOTAL": round(valor_total_gaxeta, 2)
        }
        st.session_state.orcamento.append(item)
        st.rerun()

# ABA 2: NOVO PRODUTO MANUAL (Colas, bandejas, etc)
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
                "VALOR UNITARIO": round(preco_manual, 2),
                "VALOR TOTAL": round(valor_total_manual, 2)
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
    
    df_exibicao = df_orcamento.copy()
    df_exibicao["VALOR UNITARIO"] = df_exibicao["VALOR UNITARIO"].map("R$ {:.2f}".format)
    df_exibicao["VALOR TOTAL"] = df_exibicao["VALOR TOTAL"].map("R$ {:.2f}".format)
    
    st.dataframe(df_exibicao, use_container_width=True, hide_index=True)
    
    subtotal = df_orcamento["VALOR TOTAL"].sum()
    total_geral = subtotal + valor_frete
    
    col_t1, col_t2 = st.columns([2, 1])
    with col_t2:
        st.markdown(f"**Subtotal dos Itens:** R$ {subtotal:.2f}")
        st.markdown(f"**Frete de Envio:** R$ {valor_frete:.2f}")
        st.markdown(f"### **TOTAL GERAL: R$ {total_geral:.2f}**")
    
    data_formatada = data_emissao.strftime('%d/%m/%Y')
    
    linhas_html = ""
    for _, row in df_orcamento.iterrows():
        linhas_html += f"""
        <tr>
            <td style='padding: 10px; text-align: center; border-bottom: 1px solid #e2e8f0;'>{row['QTD']}</td>
            <td style='padding: 10px; border-bottom: 1px solid #e2e8f0;'>{row['MEDIDAS']}</td>
            <td style='padding: 10px; border-bottom: 1px solid #e2e8f0; color:#1e2b7a;'><strong>{row['PERFIL']}</strong></td>
            <td style='padding: 10px; border-bottom: 1px solid #e2e8f0;'>{row['COR']}</td>
            <td style='padding: 10px; text-align: right; border-bottom: 1px solid #e2e8f0;'>R$ {row['VALOR UNITARIO']:.2f}</td>
            <td style='padding: 10px; text-align: right; border-bottom: 1px solid #e2e8f0;'><strong>R$ {row['VALOR TOTAL']:.2f}</strong></td>
        </tr>
        """

    html_template = f"""
    <div style='font-family: system-ui, sans-serif; color: #334155; padding: 30px; background: white; border: 1px solid #cbd5e1; border-radius: 12px; max-width: 850px; margin: 20px auto; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05);'>
        <div style='display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #1e2b7a; padding-bottom: 20px; margin-bottom: 25px;'>
            <div>
                <div style='margin-bottom: 10px;'><img src='{logo_url}' style='max-height: 85px; width: auto;'></div>
                <div style='font-size: 11px; line-height: 1.5; color: #475569;'>
                    <strong>Razão Social:</strong> OTAVIO GUILHERME TEIXEIRA DE SOUZA NETO<br>
                    <strong>CNPJ:</strong> 38.233.044/0001-34 | <strong>I.E.:</strong> 799.313.829.119<br>
                    Rua João Basso, nº 20, Sala 1 Centro - São Bernardo do Campo-SP<br>
                    <strong>Telefone:</strong> (11) 99425-1306 | <strong>E-mail:</strong> vendas@ognet.com.br
                </div>
            </div>
            <div style='text-align: right;'>
                <span style='background-color: #1e2b7a; color: white; padding: 6px 16px; font-weight: bold; border-radius: 6px; font-size: 13px; letter-spacing: 1px;'>ORÇAMENTO COMERCIAL</span>
            </div>
        </div>

        <div style='background-color: #f8fafc; padding: 16px; border-radius: 8px; border: 1px solid #e2e8f0; margin-bottom: 25px; font-size: 13px; line-height: 1.6;'>
            <h4 style='margin: 0 0 8px 0; color: #1e2b7a; font-size: 14px; border-bottom: 1px solid #e2e8f0; padding-bottom: 4px;'>DADOS DO CLIENTE</h4>
            <strong>Cliente / Razão Social:</strong> {nome_cliente if nome_cliente else 'Não Informado'}<br>
            <strong>CPF / CNPJ:</strong> {cnpj_cliente if cnpj_cliente else 'Não Informado'}<br>
            <strong>Data de Emissão:</strong> {data_formatada}
        </div>

        <table style='width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 25px;'>
            <thead>
                <tr style='background-color: #f1f5f9; text-align: left; color: #475569;'>
                    <th style='padding: 10px; text-align: center; border-bottom: 2px solid #cbd5e1; width: 8%;'>QTD</th>
                    <th style='padding: 10px; border-bottom: 2px solid #cbd5e1; width: 25%;'>MEDIDAS</th>
                    <th style='padding: 10px; border-bottom: 2px solid #cbd5e1; width: 32%;'>PRODUTO / PERFIL</th>
                    <th style='padding: 10px; border-bottom: 2px solid #cbd5e1; width: 10%;'>COR</th>
                    <th style='padding: 10px; text-align: right; border-bottom: 2px solid #cbd5e1; width: 12%;'>UNITÁRIO</th>
                    <th style='padding: 10px; text-align: right; border-bottom: 2px solid #cbd5e1; width: 13%;'>TOTAL</th>
                </tr>
            </thead>
            <tbody>
                {linhas_html}
            </tbody>
        </table>

        <div style='text-align: right; font-size: 14px; margin-top: 20px; line-height: 1.6; border-top: 1px solid #f1f5f9; padding-top: 15px;'>
            <span style='color: #64748b;'>Subtotal dos Itens:</span> R$ {subtotal:.2f}<br>
            <span style='color: #64748b;'>Valor do Frete:</span> R$ {valor_frete:.2f}<br>
            <div style='margin-top: 5px; font-size: 18px; color: #1e2b7a;'><strong>TOTAL GERAL: R$ {total_geral:.2f}</strong></div>
        </div>

        <div style='margin-top: 40px; text-align: center; font-size: 11px; color: #94a3b8; border-top: 1px solid #e2e8f0; padding-top: 15px; line-height: 1.5;'>
            * Peças industriais fabricadas sob medida e especificações técnicas solicitadas.<br>
            <strong>Prazo de Validade deste documento:</strong> 10 dias a contar da data de emissão.
        </div>
    </div>
    """

    col_b1, col_b2 = st.columns([1, 4])
    with col_b1:
        if st.button("🗑️ Limpar Lista", use_container_width=True):
            st.session_state.orcamento = []
            st.rerun()
            
    with col_b2:
        st.download_button(
            label="💾 Baixar Documento de Orçamento (HTML/PDF)",
            data=html_template,
            file_name=f"Orcamento_OGNET_{datetime.now().strftime('%d%m%Y')}.html",
            mime="text/html",
            use_container_width=True,
            type="primary"
        )

else:
    st.info("Nenhum item adicionado ao orçamento.")

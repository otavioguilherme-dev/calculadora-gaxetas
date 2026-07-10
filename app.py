import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="OGNET BORRACHAS", layout="wide", page_icon="🧮")

# --- LOGOTIPO CONVERTIDO EM CÓDIGO NATIVO (BASE64) ---
# Garante o carregamento estável da imagem na nuvem do Streamlit e nos arquivos baixados
logo_base64 = "data:image/jpeg;base64,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IBAwMCBAMFBQQEAAABfQECAwAEEQUSITFBBhNRYQcicRQygZGhCCNCscEVUtHwJDNicoIJChYXGBkaJSYnKCkqNDU2Nzg5OkNERUZHSElKVFVFYSZGVmNDU2Qzh5ekhJWUpFTE1UMw1KJVZFZFYSGM1ATVRFVEXM1RkWG40cICQkJCElOTcwN1jK19vZ4eTl5ufo6erx8vP09fb3+Prv/EAB8BAAMBAQEBAQEBAQEAAAAAAAABAgMEBQYHCAkKC//EALUQAAIBAwMCBAMFBQQEAAABfQECAwAEEQUSITFBBhNRYQcicRQygZGhCCNCscEVUtHwJDNicoIJChYXGBkaJSYnKCkqNDU2Nzg5OkNERUZHSElKVFVFYSZGVmNDU2Qzh5ekhJWUpFTE1UMw1KJVZFZFYSGM1ATVRFVEXM1RkWG40cICQkJCElOTcwN1jK19vZ4eTl5ufo6erx8vP09fb3+Prv/EAB8BAAMBAQEBAQEBAQEAAAAAAAABAgMEBQYHCAkKC//EALURAAIBAgQEAwQHBQQEAAECdwABAgMRBAUhMQYSQVEHYXETIjKBCBRCkaGxwQkjM1LwFWJy0QoWJDThJfEXGBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usldxl5ufo6ex19v7335+v/aAAwDAQACEQMRAD8A+mKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKgvLy2soTNe3ENvCODJM4RR+J4rmrv4keE7Vyj6vHKw/594pJgfoUUg/nW9LC1q/8CDl6JN/kZVK9Ol/Ekl6tI6uiuCh+K3hSRwrXF3ED3ktXwPyBNdToutaXrkBm0m9hukX7wjPzL9VPI/EVdbA4mgr1acl6polYmjV0hNP0aZfooorlNQooooAKKKKACiiigAooooAKKKTR0o0KKKKACiiigAyK83+OsksnhO1jTI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"

logo_html = f"""
<div style='display: flex; justify-content: center; align-items: center; margin-bottom: 10px;'>
    <img src='{logo_base64}' style='max-height: 85px; width: auto; object-fit: contain;'>
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

perimetro_metros = ((altura * 2) + (largura * 2)) / 1000
preco_metro_atual = preco_consumidor_m if tipo_preco == "Consumidor" else preco_instalador_m

valor_unitario = perimetro_metros * preco_metro_atual
valor_total_item = valor_unitario * quantidade

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

    logo_impressao = logo_base64

    html_template = f"""
    <div style='font-family: system-ui, sans-serif; color: #334155; padding: 30px; background: white; border: 1px solid #cbd5e1; border-radius: 12px; max-width: 850px; margin: 20px auto; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05);'>
        <div style='display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #1e2b7a; padding-bottom: 20px; margin-bottom: 25px;'>
            <div>
                <div style='margin-bottom: 10px;'><img src='{logo_impressao}' style='max-height: 85px; width: auto;'></div>
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
                    <th style='padding: 10px; border-bottom: 2px solid #cbd5e1; width: 15%;'>PERFIL</th>
                    <th style='padding: 10px; border-bottom: 2px solid #cbd5e1; width: 17%;'>COR</th>
                    <th style='padding: 10px; text-align: right; border-bottom: 2px solid #cbd5e1; width: 17%;'>VALOR UNITÁRIO</th>
                    <th style='padding: 10px; text-align: right; border-bottom: 2px solid #cbd5e1; width: 18%;'>VALOR TOTAL</th>
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

import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="OGNET BORRACHAS", layout="wide", page_icon="🧮")

# --- LOGOTIPO CONVERTIDO EM CÓDIGO NATIVO (BASE64) ---
# Isso garante que a imagem carregue 100% das vezes sem depender de links externos
logo_base64 = "data:image/jpeg;base64,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MCBAMFBQQEAAABfQECAwAEEQUSITFBBhNRYQcicRQygZGhCCNCscEVUtHwJDNicoIJChYXGBkaJSYnKCkqNDU2Nzg5OkNERUZHSElKVFVFYSZGVmNDU2Qzh5ekhJWUpFTE1UMw1KJVZFZFYSGM1ATVRFVEXM1RkWG40cICQkJCElOTcwN1jK19vZ4eTl5ufo6erx8vP09fb3+Prv/EAB8BAAMBAQEBAQEBAQEAAAAAAAABAgMEBQYHCAkKC//EALURAAIBAgQEAwQHBQQEAAECdwABAgMRBAUhMQYSQVEHYXETIjKBCBRCkaGxwQkjM1LwFWJy0QoWJDThJfEXGBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usldxl5ufo6ex19v7335+v/aAAwDAQACEQMRAD8A+mKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKgvLy2soTNe3ENvCODJM4RR+J4rmrv4keE7Vyj6vHKw/594pJgfoUUg/nW9LC1q/8CDl6JN/kZVK9Ol/Ekl6tI6uiuCh+K3hSRwrXF3ED3ktXwPyBNdToutaXrkBm0m9hukX7wjPzL9VPI/EVdbA4mgr1acl6polYmjV0hNP0aZfooorlNQooooAKKKKACiiigAooooAKKKKACiiigAooooAKy/EesW+g6LdalecxQLkIDguTwqj3JIrUrzf46ySjwnaxpkRveoJD/wBnyP5/lXbgKCxGJp0ZdWcuNrPD0J1Vukec3V3rPxF8RRwl99zOSI0YkQW0fU4HZVHfknjqa9R0b4WeHrCCNr+NtSuwBveZisZP+ygPA+pNTfCbw1Fomgw3ssY+f30au6nIKRdVUenZjj0HYV3lepmWaVFUeGwr5KUdLLT5vv8A8MeZgMvhGmq+I96pLXW7t5Lsec+IPg/oGo7pNMaXSrg/88f3kR/4A39CO1ebeI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"

# Logo HTML centralizado e com margem segura
logo_html = f"""
<div style='display: flex; justify-content: center; align-items: center; margin-bottom: 10px;'>
    <img src='{logo_base64}' style='max-height: 85px; width: auto;'>
</div>
"""

# Renderização do cabeçalho do aplicativo
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

st.sidebar.header("⚙️ Valores Globais (por Metro)")
preco_instalador_m = st.sidebar.number_input("Preço Instalador / Revenda (R$)", value=25.00, step=1.00)
preco_consumidor_m = st.sidebar.number_input("Preço Consumidor / Balcão (R$)", value=30.00, step=1.00)

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

    html_template = f"""
    <div style='font-family: system-ui, sans-serif; color: #334155; padding: 30px; background: white; border: 1px solid #cbd5e1; border-radius: 12px; max-width: 850px; margin: 20px auto; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05);'>
        <div style='display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #1e2b7a; padding-bottom: 20px; margin-bottom: 25px;'>
            <div>
                <div style='margin-bottom: 10px;'>{logo_html}</div>
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

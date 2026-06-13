import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Case Dados Analytics",
    layout="wide"
)

# =========================
# LEITURA DOS DADOS
# =========================

df = pd.read_excel("base_tratada.xlsx")

# =========================
# TÍTULO
# =========================

st.title("📊 Dashboard - Case Dados Analytics")

st.write(
    "Visualização dos principais indicadores gerados após o tratamento da base de dados."
)

# =========================
# KPIs
# =========================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Registros", len(df))

with col2:
    st.metric(
        "Tempo Médio",
        round(df["tempo_espera_seg"].mean(), 1)
    )

with col3:
    st.metric(
        "Motivos",
        df["motivo_contato"].nunique()
    )

st.markdown("---")

# =========================
# GRÁFICO 1
# =========================

st.subheader("Quantidade de contatos por motivo")

fig, ax = plt.subplots()

df["motivo_contato"].value_counts().plot(
    kind="bar",
    ax=ax
)

plt.tight_layout()

st.pyplot(fig)

# =========================
# GRÁFICO 2
# =========================

st.subheader("Tempo médio de espera por motivo")

fig, ax = plt.subplots()

df.groupby("motivo_contato")["tempo_espera_seg"].mean().plot(
    kind="bar",
    ax=ax
)

plt.tight_layout()

st.pyplot(fig)

# =========================
# GRÁFICO 3
# =========================

st.subheader("Quantidade de atendimentos por data")

df["data"] = pd.to_datetime(df["data"])

atendimentos_por_data = (
    df.groupby("data")
      .size()
      .reset_index(name="quantidade")
)

st.line_chart(
    atendimentos_por_data,
    x="data",
    y="quantidade"
)

# =========================
# RESUMO EXECUTIVO
# =========================

st.markdown("---")

st.subheader("Resumo Executivo")

st.success(
    """
    ✅ 48 registros analisados

    ✅ 0 datas inválidas após padronização

    ✅ 0 motivos não mapeados

    ✅ 0 valores nulos restantes

    ✅ IDs duplicados corrigidos

    ✅ Base pronta para análise
    """
)

# =========================
# BASE TRATADA
# =========================

st.markdown("---")

st.subheader("Base Tratada")

st.dataframe(
    df,
    use_container_width=True,
    height=400
)
import streamlit as st
import pandas as pd

# ✅ Configuración de la página (debe ir primero)
st.set_page_config(page_title="Centro de Atención al Cliente", layout="wide")

# Cargar datos desde GitHub
@st.cache_data
def cargar_datos():
    url = "https://raw.githubusercontent.com/ivan-emv/acceso-agentes/main/ACCESOS%20AGENTES.xlsx"
    xls = pd.ExcelFile(url)
    accesos_df = xls.parse('ACCESOS')
    plantillas_df = xls.parse('Plantillas CallBell')
    return accesos_df, plantillas_df

accesos_df, plantillas_df = cargar_datos()

# Título principal
st.title("Centro de Atención al Cliente")

# Sección de accesos rápidos
st.header("🔗 Accesos Rápidos")
for _, row in accesos_df.iterrows():
    if pd.notna(row[0]):
        st.markdown(f"**{row[0]}**")
    if pd.notna(row[1]):
        st.markdown(f"[Acceder]({row[1]})")

# Sección de calculadora de reembolsos
st.header("💰 Calculadora de Reembolsos")
monto = st.number_input("Monto a devolver", min_value=0.0, format="%.2f")
porcentaje = st.number_input("% Comisión del proveedor", min_value=0.0, max_value=100.0, format="%.2f")
if st.button("Calcular"):
    total_a_devolver = monto * (1 - porcentaje / 100)
    st.success(f"Total a devolver: ${total_a_devolver:.2f}")

# Sección de plantillas predefinidas
st.header("✉️ Plantillas de Atención")
opciones = plantillas_df.iloc[:, 0].dropna().unique()
seleccion = st.selectbox("Selecciona una plantilla", opciones)
plantilla = plantillas_df[plantillas_df.iloc[:, 0] == seleccion].iloc[:, 2].values[0]
st.text_area("Texto de la plantilla", plantilla, height=150)

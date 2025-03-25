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
    return accesos_df

accesos_df = cargar_datos()

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
porcentaje = st.number_input("% Comisión del proveedor", min_value=0.01, max_value=100.0, format="%.2f")
if st.button("Calcular"):
    cuenta1 = porcentaje / 100  # Calculamos el porcentaje como decimal
    total_a_devolver = monto / cuenta1  # Aplicamos la fórmula correcta
    
    # 🔎 Depuración: Mostrar valores intermedios
    st.write(f"### 📊 Valores intermedios")
    st.write(f"Cuenta1 (Porcentaje en decimal): {cuenta1}")
    st.write(f"Monto ingresado: {monto}")
    st.write(f"Total a devolver calculado: {total_a_devolver}")
    
    st.success(f"Total a devolver: ${total_a_devolver:.2f}")

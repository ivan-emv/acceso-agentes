import json
import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ✅ Configuración de la página
st.set_page_config(page_title="Centro de Atención al Cliente", layout="wide")

# 🔐 Autenticación con Google Sheets desde Streamlit Secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
service_account_info = st.secrets["gcp_service_account"]  # ✅ Corrección: Accedemos directamente al diccionario
credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)

# 🔹 Autenticación con Google Sheets
client = gspread.authorize(credentials)

# 📂 Cargar datos desde Google Sheets
SHEET_ID = "1kBLQAdhYbnP8HTUgpr_rmmGEaOdyMU2tI97ogegrGxY"
SHEET_NAME = "Enlaces"
sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

def cargar_enlaces():
    data = sheet.get_all_records()
    return pd.DataFrame(data)

enlaces_df = cargar_enlaces()

# 🔐 Modo Administrador con usuario y contraseña
USERS = {"admin": "ivan.amador"}  # 🔒 Cambia o añade más usuarios aquí
modo_admin = False
if st.sidebar.checkbox("Modo Administrador"):
    usuario = st.sidebar.text_input("👤 Usuario")
    password = st.sidebar.text_input("🔑 Contraseña", type="EMVac1997-")
    
    if usuario in USERS and USERS[usuario] == password:
        modo_admin = True
        st.sidebar.success("🔓 Acceso concedido al modo administrador")
    elif usuario or password:
        st.sidebar.error("❌ Usuario o contraseña incorrectos")

# 🏠 Título principal
st.title("Centro de Atención al Cliente")

# 🔗 Sección de accesos rápidos
st.header("🔗 Accesos Rápidos")

# 📋 Mostrar enlaces
for _, row in enlaces_df.iterrows():
    if pd.notna(row["Nombre del Enlace"]):
        st.markdown(f"**{row['Nombre del Enlace']}**")
    if pd.notna(row["URL"]):
        st.markdown(f"[Acceder]({row['URL']})")

# 🛠️ Modo Administrador: Agregar/Editar Enlaces
if modo_admin:
    st.sidebar.header("🔧 Gestión de Enlaces")
    with st.sidebar.form("Agregar Enlace"):
        nombre = st.text_input("Nombre del Enlace")
        url = st.text_input("URL")
        ano = st.text_input("Año (Opcional, si aplica)")
        permanente = st.selectbox("¿Permanente?", ["Sí", "No"])
        enviar = st.form_submit_button("Guardar Enlace")
        
        if enviar:
            nuevo_enlace = [ano, nombre, url, permanente]
            sheet.append_row(nuevo_enlace)
            st.success("✅ Enlace agregado exitosamente. Recarga la página para ver los cambios.")

# 💰 Calculadora de Reembolsos
st.header("💰 Calculadora de Reembolsos")
monto = st.number_input("Monto a devolver", min_value=0.0, format="%.2f")
porcentaje = st.number_input("% Comisión del proveedor", min_value=0.01, max_value=100.0, format="%.2f")
if st.button("Calcular"):
    cuenta1 = (100 - porcentaje) / 100  # Factor de ajuste
    total_a_devolver = monto / cuenta1  # ✅ Multiplicamos en lugar de dividir
    
    # 🔎 Depuración: Mostrar valores intermedios
    st.write(f"### 📊 Valores intermedios")
    st.write(f"Cuenta1 (Factor de ajuste): {cuenta1}")
    st.write(f"Monto ingresado: {monto}")
    st.write(f"Total a devolver calculado: {total_a_devolver}")
    
    st.success(f"Total a devolver: ${total_a_devolver:.2f}")

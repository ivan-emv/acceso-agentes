import json
import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ✅ Configuración de la página
st.set_page_config(page_title="Centro de Atención al Cliente", layout="wide")

# 🔐 Autenticación con Google Sheets desde Streamlit Secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
service_account_info = st.secrets["gcp_service_account"]
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
USERS = {"admin": "admin123"}  # 🔒 Cambia o añade más usuarios aquí
modo_admin = False
if st.sidebar.checkbox("Modo Administrador"):
    usuario = st.sidebar.text_input("👤 Usuario")
    password = st.sidebar.text_input("🔑 Contraseña", type="password")
    
    if usuario in USERS and USERS[usuario] == password:
        modo_admin = True
        st.sidebar.success("🔓 Acceso concedido al modo administrador")
    elif usuario or password:
        st.sidebar.error("❌ Usuario o contraseña incorrectos")

# 🏠 Título principal
st.title("Centro de Atención al Cliente")

# 🏗️ Dividir la pantalla en 2 columnas
col1, col2 = st.columns([2, 1])

# 🔗 Sección de accesos rápidos organizados en 4 columnas
with col1:
    st.header("🔗 Accesos Rápidos")
    categorias = {"Sistemas EMV": [], "EMV - SIRE": [], "Datos por Agente": [], "Otros enlaces": []}
    
    for _, row in enlaces_df.iterrows():
        if pd.notna(row["Categoría"]) and pd.notna(row["URL"]):
            texto_boton = row["Nombre del Enlace"] if row["Categoría"] not in ["EMV - SIRE", "Datos por Agente"] else row["Año"]
            categorias[row["Categoría"]].append((texto_boton, row["URL"]))
    
    col1, col2, col3, col4 = st.columns(4)
    columnas = [col1, col2, col3, col4]
    nombres_columnas = ["Sistemas EMV", "EMV - SIRE", "Datos por Agente", "Otros enlaces"]
    
    for i, categoria in enumerate(nombres_columnas):
        with columnas[i]:
            st.subheader(categoria)
            for nombre, url in categorias[categoria]:
                st.button(nombre, on_click=lambda url=url: st.markdown(f'<meta http-equiv="refresh" content="0; url={url}">', unsafe_allow_html=True))

# 💰 Calculadora de Reembolsos y botones adicionales
with col2:
    st.header("💰 Calculadora de Reembolsos")
    monto = st.number_input("Monto a devolver", min_value=0.0, format="%.2f")
    porcentaje = st.number_input("% Comisión del proveedor", min_value=0.01, max_value=100.0, format="%.2f")
    if st.button("Calcular"):
        total_a_devolver = monto / ((100 - porcentaje) / 100)
        st.success(f"Total a devolver: ${total_a_devolver:.2f}")
    
    st.markdown("---")
    st.markdown("### [INFO EMV](https://esuezhg4oon.typeform.com/InfoCC)", unsafe_allow_html=True)
    
    localizador = st.text_input("Inserte Localizador")
    if st.button("Ver Reserva"):
        st.markdown(f'<meta http-equiv="refresh" content="0; url=https://www.europamundo-online.com/reservas/buscarreserva2.asp?coreserva={localizador}">', unsafe_allow_html=True)
    
    tr = st.text_input("Inserte TR")
    if st.button("Ver Traslado"):
        st.markdown(f'<meta http-equiv="refresh" content="0; url=https://www.europamundo-online.com/Individuales/ExcursionDetalle.ASP?CORESERVA={tr}">', unsafe_allow_html=True)

# 🛠️ Modo Administrador: Agregar/Editar Enlaces
if modo_admin:
    st.sidebar.header("🔧 Gestión de Enlaces")
    with st.sidebar.form("Agregar Enlace"):
        nombre = st.text_input("Nombre del Enlace")
        url = st.text_input("URL")
        ano = st.text_input("Año (Opcional, si aplica)")
        categoria = st.selectbox("Categoría", ["Sistemas EMV", "EMV - SIRE", "Datos por Agente", "Otros enlaces"])
        enviar = st.form_submit_button("Guardar Enlace")
        
        if enviar:
            nuevo_enlace = [ano, nombre, url, categoria]
            sheet.append_row(nuevo_enlace)
            st.success("✅ Enlace agregado exitosamente.")
            st.rerun()

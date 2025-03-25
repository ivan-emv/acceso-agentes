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

# 🔐 Modo Administrador con usuario y contraseña en la barra lateral
USERS = {"admin": "admin123"}  # 🔒 Cambia o añade más usuarios aquí
modo_admin = False
with st.sidebar:
    st.header("🔧 Modo Administrador")
    if st.checkbox("Activar Modo Administrador"):
        usuario = st.text_input("👤 Usuario")
        password = st.text_input("🔑 Contraseña", type="password")
        if usuario in USERS and USERS[usuario] == password:
            modo_admin = True
            st.success("🔓 Acceso concedido al modo administrador")
            
            # 🛠️ Panel de carga de enlaces justo debajo de la autenticación
            st.header("📥 Agregar Enlace")
            with st.form("Agregar Enlace"):
                nombre = st.text_input("Nombre del Enlace")
                url = st.text_input("URL")
                categoria = st.selectbox("Categoría", ["Sistemas EMV", "EMV - SIRE", "Datos Agente", "Otros enlaces"])
                enviar = st.form_submit_button("Guardar Enlace")
                
                if enviar:
                    nuevo_enlace = [nombre, url, categoria]
                    sheet.append_row(nuevo_enlace)
                    st.success("✅ Enlace agregado exitosamente.")
                    st.rerun()

# 🏗️ Dividir la pantalla en 2 columnas (Enlaces - Calculadora)
col_enlaces, col_calculadora = st.columns([2, 1])

# 🔗 Sección de accesos rápidos organizados en 4 columnas (Columna central)
with col_enlaces:
    st.header("🔗 Accesos Rápidos")
    categorias_validas = ["Sistemas EMV", "EMV - SIRE", "Datos Agente", "Otros enlaces"]
    categorias = {cat: [] for cat in categorias_validas}
    
    for _, row in enlaces_df.iterrows():
        categoria = str(row.get("Categoría", "Otros enlaces")).strip()
        nombre = str(row.get("Nombre del Enlace", "")).strip()
        url = str(row.get("URL", "")).strip()
        
        if categoria in categorias and nombre and url:
            categorias[categoria].append((nombre, url))
    
    col1, col2, col3, col4 = st.columns(4)
    columnas = [col1, col2, col3, col4]
    
    for i, categoria in enumerate(categorias_validas):
        with columnas[i]:
            st.subheader(categoria)
            for nombre, url in categorias[categoria]:
                if nombre and url:
                    st.link_button(nombre, url, use_container_width=True)

# 💰 Calculadora de Reembolsos y botones adicionales (Columna derecha, siempre visible)
with col_calculadora:
    st.header("💰 Calculadora de Reembolsos")
    monto = st.number_input("Monto a devolver", min_value=0.0, format="%.2f")
    porcentaje = st.number_input("% Comisión del proveedor", min_value=0.01, max_value=100.0, format="%.2f")
    if st.button("Calcular"):
        total_a_devolver = monto / ((100 - porcentaje) / 100)
        st.success(f"Total a devolver: ${total_a_devolver:.2f}")
    
    st.markdown("---")
    st.link_button("INFO EMV", "https://esuezhg4oon.typeform.com/InfoCC", use_container_width=True)
    
    localizador = st.text_input("Inserte Localizador")
    if st.link_button("Ver Reserva", "https://www.europamundo-online.com/reservas/buscarreserva2.asp?coreserva={localizador}", use_container_width=True):
    
    tr = st.text_input("Inserte TR")
    if st.button("Ver Traslado") and tr:
        st.markdown(f'<script>window.open("https://www.europamundo-online.com/Individuales/ExcursionDetalle.ASP?CORESERVA={tr}", "_blank");</script>', unsafe_allow_html=True)

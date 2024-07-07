import streamlit as st
from datetime import datetime, timedelta
import json
import os

# Nombre de los archivos de datos
DATA_FILE = 'reservas_data.json'
USERS_FILE = 'users.txt'

# Función para cargar las reservas desde un archivo
def cargar_reservas():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

# Función para guardar las reservas en un archivo
def guardar_reservas(reservas):
    with open(DATA_FILE, 'w') as file:
        json.dump(reservas, file)

# Función para cargar usuarios autorizados desde el archivo
def load_users(filename=USERS_FILE):
    users = {}
    with open(filename, 'r') as f:
        for line in f:
            login, password = line.strip().split(':')
            users[login] = password
    return users

# Función para autenticar usuarios
def authenticate(login, password, users):
    if login in users and users[login] == password:
        return True
    return False

# Estructura de datos para las reservas
reservas = cargar_reservas()

# Función para agregar una reserva
def agregar_reserva(nombre, fecha, hora):
    formato = "%Y-%m-%d %H:%M"
    try:
        inicio_reserva = datetime.strptime(f"{fecha} {hora}", formato)
    except ValueError:
        return "Error: Formato de fecha u hora incorrecto. Use YYYY-MM-DD HH:MM."
    
    # Validar que la hora esté dentro del rango permitido
    if inicio_reserva.time() < datetime.strptime('08:00', '%H:%M').time() or inicio_reserva.time() >= datetime.strptime('16:00', '%H:%M').time():
        return "Error: La hora debe estar entre las 08:00 AM y las 03:00 PM para asegurar una duración de una hora."
    
    fin_reserva = inicio_reserva + timedelta(hours=1)
    
    # Verificar conflictos con otras reservas
    for reserva in reservas.values():
        inicio_existente = datetime.strptime(reserva['inicio'], formato)
        fin_existente = datetime.strptime(reserva['fin'], formato)
        if inicio_existente < fin_reserva and inicio_reserva < fin_existente:
            return f"Error: Ya hay una reserva para ese horario ({fecha} {hora})"
    
    reservas[nombre] = {'inicio': inicio_reserva.strftime(formato), 'fin': fin_reserva.strftime(formato)}
    guardar_reservas(reservas)
    return f"Reserva realizada para {nombre} el {fecha} a las {hora}."

# Función para mostrar las reservas
def mostrar_reservas():
    if not reservas:
        st.write("No hay reservas.")
    for nombre, tiempo in reservas.items():
        st.write(f"{nombre}: {tiempo['inicio']} - {tiempo['fin']}")

# Función para borrar una reserva
def borrar_reserva(nombre):
    if nombre in reservas:
        del reservas[nombre]
        guardar_reservas(reservas)
        return f"Reserva de {nombre} eliminada."
    return f"No se encontró una reserva a nombre de {nombre}."

# Interfaz de Streamlit
st.set_page_config(layout="wide")

# Cargar usuarios autorizados
users = load_users()

# Autenticación
st.sidebar.title("Autenticación")
login = st.sidebar.text_input("Login")
password = st.sidebar.text_input("Password", type="password")
if st.sidebar.button("Iniciar sesión"):
    if authenticate(login, password, users):
        st.sidebar.success("Acceso concedido.")
        
        # Cargar el logo
        logo_izquierda = "8f2bdf63-f8ce-412e-9c57-df40744f44dd.png"  # Ruta al archivo del logo

        col1, col2 = st.columns([1, 9])
        with col1:
            st.image(logo_izquierda, width=100)
        with col2:
            st.title('Sistema de Reservas')

        opcion = st.selectbox('Selecciona una opción', ['Agregar Reserva', 'Mostrar Reservas', 'Borrar Reserva'])

        if opcion == 'Agregar Reserva':
            nombre = st.text_input('Nombre')
            fecha = st.date_input('Fecha')
            hora = st.time_input('Hora', value=datetime.strptime('08:00', '%H:%M').time())

            if hora < datetime.strptime('08:00', '%H:%M').time() or hora >= datetime.strptime('16:00', '%H:%M').time():
                st.warning("Por favor seleccione una hora entre las 08:00 AM y las 03:00 PM para asegurar una duración de una hora.")
            else:
                if st.button('Agregar'):
                    fecha_str = fecha.strftime('%Y-%m-%d')
                    hora_str = hora.strftime('%H:%M')
                    resultado = agregar_reserva(nombre, fecha_str, hora_str)
                    st.write(resultado)

        elif opcion == 'Mostrar Reservas':
            mostrar_reservas()

        elif opcion == 'Borrar Reserva':
            nombre = st.text_input('Nombre de la reserva a borrar')
            if st.button('Borrar'):
                resultado = borrar_reserva(nombre)
                st.write(resultado)
                mostrar_reservas()
    else:
        st.sidebar.error("Acceso denegado. Login o password incorrectos.")

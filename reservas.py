import streamlit as st
from datetime import datetime
import pandas as pd
import os

# Función para cargar usuarios autorizados desde el archivo
def load_users(filename='users.txt'):
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

# Funciones de reserva
reservas = []

def agregar_reserva(nombre, fecha_hora):
    for reserva in reservas:
        if reserva['nombre'] == nombre and reserva['fecha_hora'] == fecha_hora:
            st.error("La reserva ya existe.")
            return
    reservas.append({'nombre': nombre, 'fecha_hora': fecha_hora})
    st.success("Reserva agregada correctamente.")

def mostrar_reservas():
    if reservas:
        df = pd.DataFrame(reservas)
        st.write(df)
    else:
        st.write("No hay reservas.")

def borrar_reservas():
    reservas.clear()
    st.success("Todas las reservas han sido borradas.")

# Interfaz de Streamlit
st.title("Sistema de Gestión de Reservas")

# Cargar usuarios autorizados
users = load_users()

# Autenticación
st.sidebar.title("Autenticación")
login = st.sidebar.text_input("Login")
password = st.sidebar.text_input("Password", type="password")
if st.sidebar.button("Iniciar sesión"):
    if authenticate(login, password, users):
        st.sidebar.success("Acceso concedido.")
        
        # Opciones de funcionalidad
        option = st.selectbox("Seleccione una opción", ["Agregar Reserva", "Mostrar Reservas", "Borrar Reservas"])
        
        if option == "Agregar Reserva":
            nombre = st.text_input("Nombre completo:")
            fecha_hora = st.date_input("Seleccione la fecha") + pd.to_timedelta(st.time_input("Seleccione la hora"))
            if st.button("Agregar"):
                agregar_reserva(nombre, fecha_hora)
                
        elif option == "Mostrar Reservas":
            mostrar_reservas()
            
        elif option == "Borrar Reservas":
            if st.button("Borrar todas las reservas"):
                borrar_reservas()
    else:
        st.sidebar.error("Acceso denegado. Login o password incorrectos.")

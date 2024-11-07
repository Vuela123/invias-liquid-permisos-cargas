import streamlit as st
from db.client import MongoDBClient
from datetime import datetime
from services.liquidaciones import calcular_dias_liquidacion

def main():    
    mongo_client = MongoDBClient()
    db = mongo_client.get_database()
    LIQUIDACIONES = db["liquidaciones_permisos_cargas"]
    
    # Título y subtítulo del formulario
    st.title("Formulario de Ingreso de Datos")
    st.subheader("Para las Liquidaciones de Permisos de Cargas para Transportes Técnicos Pesados")

    # Sección de Datos del Peticionario y Documentación
    st.header("Datos del Peticionario y Documentación")
    nombre_empresa = st.text_input("Nombre de la Empresa")
    nit_empresa = st.text_input("NIT Empresa")
    constitucion = st.text_input("Constitución")
    num_vehiculos = st.number_input("No. Vehículos", min_value=1, step=1)
    primera_placa = st.text_input("Primera Placa")
    placa = st.text_input("Placa")
    anio = st.number_input("Año", min_value=1900, step=1, value=datetime.now().year)

    # Sección de Valor Vigencia
    st.header("Valor Vigencia")
    carga_iee = st.number_input("Carga IEE ($)", min_value=0.0, format="%.2f")
    vcc = st.number_input("VCC ($)", min_value=0.0, format="%.2f")

    # Sección de Tipo de Permiso
    st.header("Tipo de Permiso")
    tipo_permiso = st.selectbox("Tipo de Permiso", ["VCC", "Carga IEE"])
    valor_dia_vehiculo = st.number_input("Valor/Día - Vehículo ($)", min_value=0.0, format="%.2f")

    # Sección de Intervalo de Liquidación
    st.header("Intervalo de Liquidación")
    fecha_inicio = st.date_input("Fecha Inicio")
    fecha_fin = st.date_input("Fecha Fin")
    numero_dias_liquidar = calcular_dias_liquidacion(fecha_inicio, fecha_fin, tipo_permiso)

    # Mostrar número de días a liquidar
    st.write(f"Número de Días a Liquidar: {numero_dias_liquidar}")

    # Valor del Permiso
    valor_permiso = st.number_input("Valor del Permiso ($)", min_value=0.0, format="%.2f")

    # Botón para enviar el formulario
    if st.button("Guardar"):
        # Verificar que todos los campos de texto estén completos y no contengan solo espacios en blanco
        if not all([
            nombre_empresa.strip(), 
            nit_empresa.strip(), 
            constitucion.strip(), 
            primera_placa.strip(), 
            placa.strip()
        ]) or any([
            carga_iee == 0.0, 
            vcc == 0.0, 
            valor_dia_vehiculo == 0.0, 
            valor_permiso == 0.0
        ]):
            st.error("Por favor, completa todos los campos obligatorios.")
        else:
            # Preparar datos para la verificación
            query = {
                "nombre_empresa": nombre_empresa,
                "nit_empresa": nit_empresa,
                "constitucion": constitucion,
                "num_vehiculos": num_vehiculos,
                "primera_placa": primera_placa,
                "placa": placa,
                "anio": anio,
                "valor_vigencia": {
                    "carga_iee": carga_iee,
                    "vcc": vcc
                },
                "tipo_permiso": tipo_permiso,
                "valor_dia_vehiculo": valor_dia_vehiculo,
                "intervalo_liquidacion": {
                    "fecha_inicio": datetime.combine(fecha_inicio, datetime.min.time()),
                    "fecha_fin": datetime.combine(fecha_fin, datetime.min.time()), 
                    "numero_dias_liquidar": numero_dias_liquidar
                },
                "valor_permiso": valor_permiso
            }
            
            # Verificar si ya existe un registro duplicado
            if LIQUIDACIONES.find_one(query):
                st.error("Ya existe un registro exactamente igual en la base de datos.")
            else:
                # Agregar fecha de creación y guardar el registro
                data = query.copy()
                data["fecha_creacion"] = datetime.now()
                
                # Guardar en MongoDB directamente
                LIQUIDACIONES.insert_one(data)
                st.success("Formulario guardado exitosamente.")

if __name__ == "__main__":
    main()

# streamlit run app.py
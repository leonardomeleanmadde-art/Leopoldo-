import streamlit as st
import pandas as pd
import random

st.title("Simulación de Eventos Discretos - Sistema de Atención de Pacientes")

st.write("Este simulador muestra paso a paso la atención de pacientes en una cola simple (un servidor).")

st.header("Definición del Modelo")

st.subheader("a) Estado del sistema")
st.write("Número de pacientes en el sistema y estado del servidor (ocupado/libre)")

st.subheader("b) Eventos")
st.write("1. Llegada de paciente")
st.write("2. Fin de atención")

st.subheader("c) Lista de Eventos Futuros (FEL)")
st.write("- Próxima llegada")
st.write("- Próximo fin de servicio")

st.subheader("d) Variables estadísticas acumulativas")
st.write("- Tiempo total en cola")
st.write("- Tiempo total en sistema")
st.write("- Pacientes atendidos")

st.header("Parámetros del sistema")

num_pacientes = st.slider("Número de pacientes a simular",10,100,10)
media_llegadas = st.number_input("Media tiempo entre llegadas",value=5.0)
media_servicio = st.number_input("Media tiempo de servicio",value=4.0)

if st.button("Ejecutar simulación"):

    llegadas = []
    servicios = []
    inicio = []
    fin = []
    cola = []
    sistema = []

    tiempo_llegada_actual = 0
    fin_anterior = 0

    for i in range(num_pacientes):

        interarrival = random.expovariate(1/media_llegadas)
        servicio = random.expovariate(1/media_servicio)

        tiempo_llegada_actual += interarrival

        inicio_servicio = max(tiempo_llegada_actual, fin_anterior)
        fin_servicio = inicio_servicio + servicio

        tiempo_cola = inicio_servicio - tiempo_llegada_actual
        tiempo_sistema = fin_servicio - tiempo_llegada_actual

        llegadas.append(round(tiempo_llegada_actual,2))
        servicios.append(round(servicio,2))
        inicio.append(round(inicio_servicio,2))
        fin.append(round(fin_servicio,2))
        cola.append(round(tiempo_cola,2))
        sistema.append(round(tiempo_sistema,2))

        fin_anterior = fin_servicio

    df = pd.DataFrame({
        "Paciente": range(1,num_pacientes+1),
        "Llegada": llegadas,
        "Servicio": servicios,
        "Inicio Atención": inicio,
        "Fin Atención": fin,
        "Tiempo en Cola": cola,
        "Tiempo en Sistema": sistema
    })

    st.subheader("Tabla de simulación paso a paso")
    st.dataframe(df)

    promedio_cola = sum(cola)/num_pacientes
    promedio_sistema = sum(sistema)/num_pacientes

    st.subheader("Métricas simuladas")
    st.write("Tiempo promedio en cola:",round(promedio_cola,2))
    st.write("Tiempo promedio en sistema:",round(promedio_sistema,2))

    st.header("Comparación con resultados analíticos (modelo M/M/1)")

    lam = 1/media_llegadas
    mu = 1/media_servicio

    if lam < mu:
        W = 1/(mu-lam)
        Wq = lam/(mu*(mu-lam))

        st.write("Tiempo promedio en sistema analítico:",round(W,2))
        st.write("Tiempo promedio en cola analítico:",round(Wq,2))
    else:
        st.write("El sistema es inestable porque λ ≥ μ")

    st.header("Comportamiento Transitorio vs Estacionario")

    st.write("El comportamiento transitorio ocurre al inicio de la simulación cuando el sistema aún no ha alcanzado estabilidad.")
    st.write("El comportamiento estacionario ocurre después de que el sistema se estabiliza y las métricas se mantienen alrededor de valores constantes.")

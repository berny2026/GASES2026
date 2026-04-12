import streamlit as st
import math

# 1. IDENTIFICACIÓN (Punto 1 y 2)
st.set_page_config(page_title="Gases Arteriales - Dr. Bernal", layout="wide")
st.markdown("<h1 style='text-align: center;'>🫁 Gases Arteriales 2600m</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Gonzalo Bernal Ferreira - Médico Familiar</h3>", unsafe_allow_html=True)
st.divider()

# 2. ENTRADA DE DATOS
col1, col2, col3 = st.columns(3)
with col1:
    ph_med = st.number_input("pH Arterial", 6.80, 7.80, 7.40, 0.01)
    pco2 = st.number_input("pCO2 (mmHg)", 10.0, 90.0, 30.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 5.0, 50.0, 20.0, 0.1)
with col2:
    na = st.number_input("Sodio (Na)", 110.0, 170.0, 140.0, 0.1)
    cl = st.number_input("Cloro (Cl)", 70.0, 130.0, 105.0, 0.1)
    alb = st.number_input("Albúmina (g/dL)", 1.0, 5.0, 4.0, 0.1)
with col3:
    pa02 = st.number_input("PaO2 (mmHg)", 20.0, 200.0, 60.0, 0.1)
    fio2 = st.number_input("FiO2", 0.21, 1.00, 0.21, 0.01)
    edad = st.number_input("Edad (años)", 0, 115, 45)
    fr = st.number_input("Frecuencia Resp. (FR)", 8, 60, 20)
    spo2 = st.number_input("SpO2 (%)", 50, 100, 94)

cl_u = st.number_input("Cloro Urinario (mEq/L) - Solo para Alcalosis Metabólica", 0, 100, 0)

# --- PROCESAMIENTO ---

# PASO 1: CONSISTENCIA (Puntos 4 y 5)
st.header

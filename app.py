import streamlit as st

# 1. ENCABEZADO
st.set_page_config(page_title="Gases 2600", layout="wide")
st.title("🫁 Gases 2600")
st.markdown("### Autor: Dr. Gonzalo Bernal - Médico Familiar")
st.divider()

# 2. ENTRADA DE DATOS
c1, c2, c3 = st.columns(3)
with c1:
    ph = st.number_input("pH Arterial", 6.80, 7.80, 7.24, 0.01)
    pco2 = st.number_input("pCO2 (mmHg)", 10.0, 90.0, 24.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 5.0, 50.0, 10.0, 0.1)
with c2:
    na = st.number_input("

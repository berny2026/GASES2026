import streamlit as st

# CONFIGURACIÓN
st.set_page_config(page_title="Gases 2600 - Dr. Bernal", layout="wide")
st.markdown("<h1 style='text-align: center;'>🫁 Gases 2600</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Dr. Gonzalo Bernal - Médico Familiar</h3>", unsafe_allow_html=True)
st.divider()

# ENTRADA DE DATOS
c1, c2, c3 = st.columns(3)
with c1:
    ph = st.number_input("pH Arterial", 6.80, 7.80, 7.24, 0.01)
    pco2 = st.number_input("pCO2 (mmHg)", 10.0, 90.0, 24.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 5.0, 50.0, 10.0, 0.1)
with c2:
    na = st.number_input("Sodio (Na)", 110.0, 160.0, 140.0, 0.1)
    cl = st.number_input("Cloro (Cl)", 70.0, 130.0, 102.0, 0.1)
    alb = st.number_input("Albúmina (g/dL)", 1.0, 5.0, 3.0, 0.1)
with c3:
    pa02 = st.number_input("PaO2 (mmHg)", 20.0, 200.0, 55.0, 0.1)
    fio2 = st.number_input("FiO2 (0.21-1.0)", 0.21, 1.0, 0.35, 0.01)
    edad = st.number_input("Edad (años)", 0, 115, 45)
    fr = st.number_input("FR (resp/min)", 8, 60, 24)
    spo2 = st.number_input("SatO2 (%)", 50, 100, 90)

# PASO 1: CONSISTENCIA
st.header("🔍 Paso 1: Consistencia")
h_calc = 24 * (pco2 / hco3)
h_ph = 10**(9 - ph)
st.write(f"H+ calculado: {h_calc:.1f} | H+ real: {h_ph:.1f}")

# PASO 2 Y 3: ESTADO Y WINTER
st.header("🔬 Paso 2 y 3: Estado y Winter")
st.write(f"Interpretación: {'ACIDEMIA' if ph < 7.36 else 'ALCALEMIA' if ph > 7.44 else 'NORMAL'}")
winter = (1.5 * hco3) + 8
st.write(f"pCO2 Esperada (Winter): {winter:.1f} (+/- 2)")

# PASO 4, 5 Y 6: ANION GAP Y DELTA
st.header("⚖️ Paso 4, 5 y 6: Anion Gap y Delta")
ag_c = (na - (cl + hco3)) + (2.5 * (4 - alb))
delta = (ag_c - 10) - (20 - hco3)
st.write(f"Anion Gap Corregido: **{ag_c:.1f}**")
st.write(f"Delta del Gap: **{delta:.1f}**")
if ag_c > 12: st.warning("Causas: GOLDMARCC")

# PASO 7: OXIGENACIÓN COMPLETA
st.header("📊 Paso 7: Oxigenación")
pa_alv = (fio2 * (513)) - (pco2 / 0.8) # 560-47 = 513
grad_p = pa_alv - pa02
grad_i = (edad / 4) + 4
st.write(f"Gradiente Aa Paciente: **{grad_p:.1f}**")
st.write(f"Gradiente Aa Ideal: **{grad_i:.1f}**")
st.write(f"PAFI: {pa02/fio2:.1f} | ROX: {(spo2/fio2)/fr:.2f}")

st.divider()
st.caption("Gases 2600 - Dr. Gonzalo Bernal")

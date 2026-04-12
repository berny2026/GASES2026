import streamlit as st

# 1. ENCABEZADO FIJO
st.set_page_config(page_title="Gases 2600 - Dr. Bernal", layout="wide")
st.markdown("<h1 style='text-align: center;'>🫁 Gases 2600</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Autor: Dr. Gonzalo Bernal - Médico Familiar</h3>", unsafe_allow_html=True)
st.divider()

# 2. ENTRADA DE DATOS (Sin cambios, para no errar)
c1, c2, c3 = st.columns(3)
with c1:
    ph = st.number_input("pH Arterial", 6.80, 7.80, 7.24, 0.01)
    pco2 = st.number_input("pCO2 (mmHg)", 10.0, 90.0, 24.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 5.0, 50.0, 10.0, 0.1)
with c2:
    na = st.number_input("Sodio (Na)", 110.0, 170.0, 140.0, 0.1)
    cl = st.number_input("Cloro (Cl)", 70.0, 130.0, 102.0, 0.1)
    alb = st.number_input("Albúmina (g/dL)", 1.0, 5.0, 3.0, 0.1)
with c3:
    pa02 = st.number_input("PaO2 (mmHg)", 20.0, 200.0, 55.0, 0.1)
    fio2 = st.number_input("FiO2 (0.21-1.0)", 0.21, 1.0, 0.35, 0.01)
    edad = st.number_input("Edad (años)", 0, 115, 45)
    fr = st.number_input("FR (resp/min)", 8, 60, 24)
    spo2 = st.number_input("SatO2 (%)", 50, 100, 90)

# --- SECUENCIA EXACTA PASO A PASO ---
st.divider()

# PASO 1: CONSISTENCIA
h_calc = 24 * (pco2 / hco3)
h_ph = 10**(9 - ph)
st.subheader("Paso 1: Consistencia Interna")
st.write(f"H+ calculado: {h_calc:.1f} | H+ por pH: {h_ph:.1f}")
if abs(h_calc - h_ph) < 5: st.success("✅ Gases Consistentes")
else: st.error("⚠️ Gases Inconsistentes")

# PASO 2: ESTADO
st.subheader("Paso 2: Estado Ácido-Base")
if ph < 7.36: st.error("ACIDEMIA")
elif ph > 7.44: st.success("ALCALEMIA")
else: st.info("pH NORMAL")

# PASO 3: TRASTORNO Y COMPENSACIÓN
st.subheader("Paso 3: Trastorno y Compensación (Winter)")
winter = (1.5 * hco3) + 8
st.write(f"pCO2 Esperada (Winter): {winter:.1f} (+/- 2)")
if pco2 > winter + 2: st.warning("Acidosis Respiratoria Asociada")
elif pco2 < winter - 2: st.warning("Alcalosis Respiratoria Asociada")
else: st.success("Compensación adecuada")

# PASO 4 Y 5: ANION GAP Y CAUSAS
st.subheader("Paso 4 y 5: Anion Gap y Causas")
ag_c = (na - (cl + hco3)) + (2.5 * (4 - alb))
st.metric("Anion Gap Corregido", f"{ag_c:.1f}")
if ag_c > 12:
    st.warning("Causas (GOLDMARCC): Glicoles, Oxoproline, L-Lactato, D-Lactato, Metanol, Aspirina, Renal (Uremia), Cetoacidosis.")
else:
    st.info("Causas AG Normal: Diarrea, ATR, Hipercloremia.")

# PASO 6: DELTA DEL GAP (SU IMAGEN)
st.subheader("Paso 6: Delta del Gap")
delta = (ag_c - 10) - (20 - hco3)
st.metric("Delta del Gap", f"{delta:.1f}")
if -5 <= delta <= 5: st.write("Resultado: Acidosis Metabólica Pura")
elif delta > 5: st.write("Resultado: Alcalosis Metabólica Sobreagregada")
else: st.write("Resultado: Acidosis Metabólica Hiperclorémica")

# PASO 7: OXIGENACIÓN Y RELACIÓN DA-a
st.subheader("Paso 7: Oxigenación (Relación DA-a)")
pa_alv = (fio2 * (560 - 47)) - (pco2 / 0.8)
grad_p = pa_alv - pa02
grad_i = (edad / 4) + 4
st.write(f"Gradiente Aa Paciente: **{grad_p:.1f}** | Gradiente Ideal: **{grad_i:.1f}**")

if grad_p > grad_i + 5:
    st.error("INTERPRETACIÓN: GRADIENTE ELEVADO (Causa Parenquimatosa)")
    st.write("**Mecanismos:** Shunt, Desequilibrio V/Q, Alteración de difusión.")
else:
    st.success("INTERPRETACIÓN: GRADIENTE NORMAL (Causa Extrapulmonar)")
    st.write("**Mecanismos:** Hipoventilación, FiO2 baja.")

st.divider()
st.caption("Gases 2600 - Propiedad Intelectual del Dr. Gonzalo Bernal")

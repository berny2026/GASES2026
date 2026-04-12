import streamlit as st

# 1. ENCABEZADO Y TÍTULOS
st.set_page_config(page_title="Gases 2600 - Dr. Bernal", layout="wide")
st.markdown("<h1 style='text-align: center;'>🫁 Gases 2600</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Autor: Dr. Gonzalo Bernal - Médico Familiar</h3>", unsafe_allow_html=True)
st.divider()

# 2. ENTRADA DE DATOS
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

# --- PROCESAMIENTO SECUENCIAL (EXACTO AL EXCEL) ---
st.divider()

# Paso 1: Consistencia
h_calc = 24 * (pco2 / hco3)
h_ph = 10**(9 - ph)
st.subheader("🔍 Paso 1: Consistencia Interna")
if abs(h_calc - h_ph) < 5:
    st.success(f"Gases Consistentes (H+ calc: {h_calc:.1f})")
else:
    st.error("Gases Inconsistentes. Revisar valores.")

# Paso 2 y 3: Estado y Winter
st.subheader("🔬 Paso 2 y 3: Estado y Compensación")
if ph < 7.36: st.error("Estado: ACIDEMIA")
elif ph > 7.44: st.success("Estado: ALCALEMIA")
else: st.info("Estado: pH NORMAL")

winter = (1.5 * hco3) + 8
st.info(f"pCO2 Esperada (Winter): {winter:.1f} (+/- 2)")

# Paso 4, 5 y 6: Anion Gap y Delta del Gap (SU IMAGEN)
st.subheader("⚖️ Paso 4, 5 y 6: Brechas y Causas")
ag_c = (na - (cl + hco3)) + (2.5 * (4 - alb))
delta = (ag_c - 10) - (20 - hco3)

col_a, col_b = st.columns(2)
col_a.metric("Anion Gap Corregido", f"{ag_c:.1f}")
col_b.metric("Delta del Gap", f"{delta:.1f}")

if ag_c > 12:
    st.warning("**Causas (GOLDMARCC):** Glicoles, Oxoproline, L-Lactato, D-Lactato, Metanol, Aspirina, Renal (Uremia), Cetoacidosis.")

if -5 <= delta <= 5:
    st.write("Interpretación Delta: **Acidosis Metabólica Pura**")
elif delta > 5:
    st.write("Interpretación Delta: **Alcalosis Metabólica Sobreagregada**")
else:
    st.write("Interpretación Delta: **Acidosis Metabólica Hiperclorémica**")

# Paso 7: Oxigenación Detallada
st.subheader("📊 Paso 7: Oxigenación y Causas")
pa_alv = (fio2 * 513) - (pco2 / 0.8)
grad_p = pa_alv - pa02
grad_i = (edad / 4) + 4

st.write(f"Gradiente Aa Paciente: **{grad_p:.1f}** | Gradiente Ideal: **{grad_i:.1f}**")

if grad_p > grad_i + 5:
    st.error("🚨 INTERPRETACIÓN: GRADIENTE ELEVADO (Causa Parenquimatosa)")
    st.write("**Mecanismos:** Shunt, Desequilibrio V/Q, Alteración de difusión.")
else:
    st.success("✅ INTERPRETACIÓN: GRADIENTE NORMAL (Causa Extrapulmonar)")
    st.write("**Mecanismos:** Hipoventilación, FiO2 baja.")

st.divider()
st.caption("Gases 2600 - Propiedad Intelectual del Dr. Gonzalo Bernal")

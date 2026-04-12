import streamlit as st

# --- 1. DERECHOS DE AUTOR Y NOMBRE ---
st.set_page_config(page_title="Gases 2600 - Dr. Bernal", page_icon="🫁", layout="wide")

st.markdown("<h1 style='text-align: center;'>🫁 Gases 2600</h1>", unsafe_allow_status=True)
st.markdown("<h3 style='text-align: center;'>Autor: Dr. Gonzalo Bernal</h3>", unsafe_allow_html=True)
st.write("---")

# --- 2. ENTRADA DE DATOS DEL EXCEL ---
col1, col2, col3 = st.columns(3)

with col1:
    st.header("🧪 Arteriales")
    ph = st.number_input("pH", 6.80, 7.80, 7.40, 0.01)
    pco2 = st.number_input("pCO2 (mmHg)", 10.0, 90.0, 30.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 5.0, 50.0, 20.0, 0.1)

with col2:
    st.header("🩸 Electrolitos")
    na = st.number_input("Sodio (Na)", 110.0, 170.0, 140.0, 0.1)
    cl = st.number_input("Cloro (Cl)", 70.0, 130.0, 105.0, 0.1)
    alb = st.number_input("Albúmina (g/dL)", 1.0, 5.0, 4.0, 0.1)

with col3:
    st.header("🫁 Oxigenación")
    pa02 = st.number_input("PaO2 (mmHg)", 20.0, 200.0, 60.0, 0.1)
    fio2 = st.number_input("FiO2", 0.21, 1.0, 0.21, 0.01)

# --- 3. CONSISTENCIA INTERNA (HENDERSON) ---
st.divider()
st.header("🔍 Consistencia Interna")
h_calc = 24 * (pco2 / hco3)
h_ph = 10**(9 - ph)
if abs(h_calc - h_ph) < 4:
    st.success(f"✅ Gases Consistentes. (H+ calc: {h_calc:.1f} vs pH: {h_ph:.1f})")
else:
    st.error(f"⚠️ Gases Inconsistentes. Sugerido repetir toma.")

# --- 4. DIAGNÓSTICO ÁCIDO-BASE Y FÓRMULAS SECUNDARIAS ---
st.header("🔬 Diagnóstico y Trastornos")
ag_corr = (na - (cl + hco3)) + 2.5 * (4 - alb)

if ph < 7.36:
    st.error("ESTADO: ACIDEMIA")
    if pco2 <= 30:
        st.subheader("Trastorno Primario: Acidosis Metabólica")
        p_esp = (1.5 * hco3) + 8
        st.info(f"Fórmula de Winter (pCO2 esperada): {p_esp:.1f}")
        if ag_corr > 12:
            st.warning("**Causas Posibles (GOLDMARCC):** Glicoles, Oxoproline, Lactato, Metanol, Aspirina, Renal, Cetoacidosis.")
    else:
        st.subheader("Trastorno Primario: Acidosis Respiratoria")
elif ph > 7.44:
    st.success("ESTADO: ALCALEMIA")
    if pco2 < 30: st.subheader("Trastorno Primario: Alcalosis Respiratoria")
    else: st.subheader("Trastorno Primario: Alcalosis Metabólica")
else:
    st.info("ESTADO: pH en Rango Normal")

# --- 5. EXPLICACIÓN DE OXIGENACIÓN ---
st.divider()
st.header("📊 Análisis de Oxigenación")
grad_aa = ((fio2 * (560 - 47)) - (pco2 / 0.8)) - pa02
pafi = pa02 / fio2

c1, c2 = st.columns(2)
with c1:
    st.metric("PAFI", f"{pafi:.1f}")
    st.write("Interpretación: >300 Normal, <200 moderada, <100 severa.")
with c2:
    st.metric("Gradiente Aa", f"{grad_aa:.1f}")
    st.write("Diferencia entre el oxígeno alveolar y arterial. Elevado indica problema de intercambio.")

st.write("---")
st.caption("Gases 2600 - Herramienta gratuita bajo autoría del Dr. Gonzalo Bernal.")

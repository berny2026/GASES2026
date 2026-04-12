import streamlit as st

st.set_page_config(page_title="Gases 2600 - Dr. Bernal", page_icon="🫁")

st.title("🫁 Gases 2600")
st.markdown("### Herramienta Médica Integral (Bogotá - 2600 msnm)")

# --- ENTRADA DE DATOS ---
col1, col2 = st.columns(2)
with col1:
    ph = st.number_input("pH arterial", 6.80, 7.80, 7.40, 0.01)
    pco2 = st.number_input("pCO2 (mmHg)", 10.0, 80.0, 30.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 5.0, 50.0, 20.0, 0.1)
    na = st.number_input("Sodio (Na+)", 100.0, 160.0, 140.0, 0.1)
with col2:
    pa02 = st.number_input("PaO2 (mmHg)", 30.0, 200.0, 60.0, 0.1)
    fio2 = st.number_input("FiO2 (Ej: 0.21)", 0.21, 1.0, 0.21, 0.01)
    cl = st.number_input("Cloro (Cl-)", 70.0, 130.0, 104.0, 0.1)
    fr = st.number_input("Frec. Respiratoria", 8, 60, 20)

# --- ANÁLISIS MÉDICO ---
st.divider()
ag = na - (cl + hco3)
st.subheader(f"Anion Gap: {ag:.1f}")

if ph < 7.36:
    if pco2 <= 30:
        st.error("DIAGNÓSTICO: ACIDOSIS METABÓLICA")
        winter = (1.5 * hco3) + 8
        st.info(f"pCO2 esperada (Winter): {winter:.1f}")
        if ag > 12: st.warning("Causas (GOLDMARCC): Glicoles, Oxoproline, L-Lactato, D-Lactato, Metanol, Aspirina, Renal, Cetoacidosis.")
    else: st.error("DIAGNÓSTICO: ACIDOSIS RESPIRATORIA")
elif ph > 7.44:
    if pco2 < 30: st.success("DIAGNÓSTICO: ALCALOSIS RESPIRATORIA")
    else: st.success("DIAGNÓSTICO: ALCALOSIS METABÓLICA")

# --- OXIGENACIÓN ---
st.divider()
gradiente = ((fio2 * (560 - 47)) - (pco2 / 0.8)) - pa02
st.write(f"**Gradiente Aa Real:** {gradiente:.1f}")

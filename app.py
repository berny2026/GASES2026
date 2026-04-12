import streamlit as st

# 1. IDENTIFICACIÓN PROFESIONAL
st.set_page_config(page_title="Gases 2600 - Dr. Bernal", page_icon="🫁")

st.markdown("<h1 style='text-align: center;'>🫁 Gases 2600</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Autor: Dr. Gonzalo Bernal</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>Médico Familiar</b></p>", unsafe_allow_html=True)
st.divider()

# 2. ENTRADA DE DATOS
col1, col2 = st.columns(2)
with col1:
    ph = st.number_input("pH Arterial", 6.80, 7.80, 7.40, 0.01)
    pco2 = st.number_input("pCO2 (mmHg)", 10.0, 90.0, 30.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 5.0, 50.0, 20.0, 0.1)
    na = st.number_input("Sodio (Na)", 110.0, 170.0, 140.0, 0.1)
    spo2 = st.number_input("Saturación O2 (%)", 50, 100, 94)
with col2:
    cl = st.number_input("Cloro (Cl)", 70.0, 130.0, 105.0, 0.1)
    alb = st.number_input("Albúmina (g/dL)", 1.0, 5.0, 4.0, 0.1)
    pa02 = st.number_input("PaO2 (mmHg)", 20.0, 200.0, 60.0, 0.1)
    fio2 = st.number_input("FiO2 (0.21 - 1.0)", 0.21, 1.0, 0.21, 0.01)
    fr = st.number_input("Frecuencia Resp. (rpm)", 8, 60, 20)

# 3. CONSISTENCIA (HENDERSON)
h_calc = 24 * (pco2 / hco3)
h_ph = 10**(9 - ph)
st.divider()
if abs(h_calc - h_ph) < 4:
    st.success(f"✅ Gases Consistentes (Henderson)")
else:
    st.error(f"⚠️ Gases Inconsistentes (Revisar muestra)")

# 4. DIAGNÓSTICO ÁCIDO-BASE (JERARQUÍA MÉDICA)
st.header("🔬 Interpretación Ácido-Base")

if ph < 7.36:
    st.error("ESTADO: ACIDEMIA")
    if pco2 <= 30:
        # A. EL DIAGNÓSTICO PRIMERO
        st.subheader("Trastorno Primario: ACIDOSIS METABÓLICA")
        
        # B. FORMULA DE WINTER Y SU INTERPRETACIÓN
        p_esp = (1.5 * hco3) + 8
        st.info(f"Fórmula de Winter (pCO2 esperada): {p_esp:.1f} (+/- 2)")
        
        if pco2 < (p_esp - 2): st.warning("Interpretación de Winter: Alcalosis respiratoria asociada (Sobrecompensación).")
        elif pco2 > (p_esp + 2): st.warning("Interpretación de Winter: Acidosis respiratoria asociada (Falla ventilatoria).")
        else: st.success("Interpretación de Winter: Compensación respiratoria adecuada.")
        
        # C. ANION GAP Y CAUSAS
        ag_corr = (na - (cl + hco3)) + 2.5 * (4 - alb)
        st.metric("Anion Gap Corregido", f"{ag_corr:.1f}")
        
        if ag_corr > 12:
            st.warning("**Causas (GOLDMARCC):** Glicoles, Oxoproline, Lactato, Metanol, Aspirina, Renal, Cetoacidosis.")
        else:
            st.info("**Causas:** Diarrea, ATR, Hipercloremia.")
    else:
        st.subheader("Trastorno Primario: ACIDOSIS RESPIRATORIA")
elif ph > 7.44:
    st.success("ESTADO: ALCALEMIA")
    if pco2 < 30: st.subheader("Alcalosis Respiratoria")
    else: st.subheader("Alcalosis Metabólica")
else:
    st.info("ESTADO: pH Normal o Trastorno Mixto")

# 5. OXIGENACIÓN COMPLETA (PAFI, SAFI, ROX)
st.divider()
st.header("📊 Perfil de Oxigenación")
grad = ((fio2 * (560 - 47)) - (pco2 / 0.8)) - pa02
pafi = pa02 / fio2
safi = spo2 / fio2
rox = (safi / fr)

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("PAFI", f"{pafi:.1f}")
    st.write("Interpretación: <200 SDRA Mod.")
with c2:
    st.metric("SAFI", f"{safi:.1f}")
    st.write("Interpretación: <264 Neumonía/SDRA")
with c3:
    st.metric("Índice de ROX", f"{rox:.2f}")
    if rox < 4.88: st.write("🚨 Riesgo de falla de VMNI")
    else: st.write("✅ Estable")

st.subheader(f"Gradiente Aa: {grad:.1f}")
if grad > 20: st.write("Interpretación: Alteración del parénquima pulmonar.")
else: st.write("Interpretación: Gradiente normal (Causa extrapulmonar).")

st.write("---")
st.caption("Gases 2600 - Propiedad Intelectual del Dr. Gonzalo Bernal - Médico Familiar")

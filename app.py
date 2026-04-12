import streamlit as st

# 1. IDENTIFICACIÓN PROFESIONAL
st.set_page_config(page_title="Gases 2600 - Dr. Bernal", page_icon="🫁", layout="wide")

st.markdown("<h1 style='text-align: center;'>🫁 Gases 2600</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Autor: Dr. Gonzalo Bernal</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>Médico Familiar</b></p>", unsafe_allow_html=True)
st.divider()

# 2. ENTRADA DE DATOS (CON EDAD)
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("👤 Paciente")
    edad = st.number_input("Edad (años)", 0, 115, 45)
    fr = st.number_input("Frecuencia Resp. (rpm)", 8, 60, 20)
    spo2 = st.number_input("Saturación O2 (%)", 50, 100, 94)

with col2:
    st.subheader("🧪 Gases y Electrolitos")
    ph = st.number_input("pH Arterial", 6.80, 7.80, 7.40, 0.01)
    pco2 = st.number_input("pCO2 (mmHg)", 10.0, 90.0, 30.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 5.0, 50.0, 20.0, 0.1)
    na = st.number_input("Sodio (Na)", 110.0, 170.0, 140.0, 0.1)
    cl = st.number_input("Cloro (Cl)", 70.0, 130.0, 105.0, 0.1)

with col3:
    st.subheader("🫁 Oxigenación")
    pa02 = st.number_input("PaO2 (mmHg)", 20.0, 200.0, 60.0, 0.1)
    fio2 = st.number_input("FiO2 (0.21 - 1.0)", 0.21, 1.0, 0.21, 0.01)
    alb = st.number_input("Albúmina (g/dL)", 1.0, 5.0, 4.0, 0.1)

# 3. CONSISTENCIA (HENDERSON)
st.divider()
h_calc = 24 * (pco2 / hco3)
h_ph = 10**(9 - ph)
st.subheader("🔍 Análisis de Consistencia")
if abs(h_calc - h_ph) < 5: # Tolerancia ligeramente mayor
    st.success(f"✅ Gases Consistentes. (H+ calc: {h_calc:.1f} vs pH: {h_ph:.1f})")
else:
    st.error(f"⚠️ Gases Inconsistentes. Diferencia elevada entre pH y el equilibrio químico.")

# 4. DIAGNÓSTICO ÁCIDO-BASE JERARQUIZADO
st.header("🔬 Interpretación Clínica")
ag_corr = (na - (cl + hco3)) + 2.5 * (4 - alb)

if ph < 7.36:
    st.error(f"ESTADO: ACIDEMIA (Paciente de {edad} años)")
    
    # CASO ACIDOSIS METABÓLICA
    if pco2 <= 30: 
        st.subheader("Trastorno Primario: ACIDOSIS METABÓLICA")
        p_esp = (1.5 * hco3) + 8
        st.info(f"Fórmula de Winter (pCO2 esperada): {p_esp:.1f} (+/- 2)")
        
        if pco2 < (p_esp - 2): st.warning("Interpretación: Alcalosis respiratoria asociada.")
        elif pco2 > (p_esp + 2): st.warning("Interpretación: Acidosis respiratoria asociada.")
        else: st.success("Interpretación: Compensación respiratoria adecuada.")
        
        st.metric("Anion Gap Corregido", f"{ag_corr:.1f}")
        if ag_corr > 12:
            st.warning("**Causas (GOLDMARCC):** Glicoles, Oxoproline, Lactato, Metanol, Aspirina, Renal, Cetoacidosis.")
        else:
            st.info("**Causas AG Normal:** Diarrea, Acidosis Tubular Renal, Hipercloremia.")

    # CASO ACIDOSIS RESPIRATORIA
    else:
        st.subheader("Trastorno Primario: ACIDOSIS RESPIRATORIA")
        st.warning("**Causas:** EPOC, Obesidad-Hipoventilación, Depresión del SNC, Enfermedad Neuromuscular.")
        hco3_esp = 24 + ((pco2 - 30) / 10) # Ajuste para Bogotá
        st.info(f"HCO3 esperado (Agudo): {hco3_esp:.1f}")

elif ph > 7.44:
    st.success("ESTADO: ALCALEMIA")
    if pco2 < 30: st.subheader("Primario: Alcalosis Respiratoria")
    else: st.subheader("Primario: Alcalosis Metabólica")

# 5. OXIGENACIÓN COMPLETA
st.divider()
st.header("📊 Perfil de Oxigenación")
grad = ((fio2 * (560 - 47)) - (pco2 / 0.8)) - pa02
pafi = pa02 / fio2
safi = spo2 / fio2
rox = (safi / fr)

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("PAFI", f"{pafi:.1f}")
    if pafi < 200: st.write("🚨 SDRA Moderado/Severo")
with c2:
    st.metric("SAFI", f"{safi:.1f}")
    if safi < 264: st.write("🚨 Riesgo de Lesión Pulmonar")
with c3:
    st.metric("Índice de ROX", f"{rox:.2f}")
    if rox < 4.88: st.write("🚨 Riesgo falla de Cánula Alto Flujo")

st.subheader(f"Gradiente Aa: {grad:.1f}")
if grad > 20: st.write("Interpretación: Alteración del parénquima pulmonar (shunt, V/Q).")
else: st.write("Interpretación: Gradiente normal (Causa extrapulmonar/Hipoventilación).")

st.caption(f"Gases 2600 - Dr. Gonzalo Bernal - Médico Familiar. Bogotá, PB 560 mmHg.")

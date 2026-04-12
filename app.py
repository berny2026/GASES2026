import streamlit as st

# 1. IDENTIFICACIÓN Y DERECHOS
st.set_page_config(page_title="Gases 2600 - Dr. Bernal", page_icon="🫁", layout="wide")

st.markdown("<h1 style='text-align: center;'>🫁 Gases 2600</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Autor: Dr. Gonzalo Bernal</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>Médico Familiar</b></p>", unsafe_allow_html=True)
st.divider()

# 2. ENTRADA DE DATOS (EXACTA AL EXCEL)
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("👤 Paciente")
    edad = st.number_input("Edad (años)", 0, 115, 45)
    fr = st.number_input("Frecuencia Resp. (rpm)", 8, 60, 20)
    spo2 = st.number_input("Saturación O2 (%)", 50, 100, 94)

with col2:
    st.subheader("🧪 Bioquímica")
    ph = st.number_input("pH Arterial", 6.80, 7.80, 7.40, 0.01)
    pco2 = st.number_input("pCO2 (mmHg)", 10.0, 90.0, 30.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 5.0, 50.0, 20.0, 0.1)
    na = st.number_input("Sodio (Na)", 110.0, 170.0, 140.0, 0.1)
    cl = st.number_input("Cloro (Cl)", 70.0, 130.0, 105.0, 0.1)

with col3:
    st.subheader("🫁 Oxigenación")
    pa02 = st.number_input("PaO2 (mmHg)", 20.0, 200.0, 60.0, 0.1)
    fio2 = st.number_input("FiO2 (fracción)", 0.21, 1.0, 0.21, 0.01)
    alb = st.number_input("Albúmina (g/dL)", 1.0, 5.0, 4.0, 0.1)

# --- LÓGICA DE ANÁLISIS (EL CORAZÓN DEL EXCEL) ---
st.divider()

# A. CONSISTENCIA INTERNA (HENDERSON)
h_calc = 24 * (pco2 / hco3)
h_ph = 10**(9 - ph)
st.subheader("🔍 Consistencia Interna")
if abs(h_calc - h_ph) < 4:
    st.success(f"✅ Gases Consistentes (H+ calc: {h_calc:.1f})")
else:
    st.error(f"⚠️ Gases Inconsistentes. El equilibrio químico no coincide con el pH.")

# B. INTERPRETACIÓN ÁCIDO-BASE
st.header("🔬 Interpretación Clínica")
ag_corr = (na - (cl + hco3)) + 2.5 * (4 - alb)

# 1. Acidosis Metabólica (Primario si pH < 7.36 y HCO3 < 17 en Bogotá)
if ph < 7.36 and hco3 < 18:
    st.error(f"DIAGNÓSTICO: ACIDEMIA METABÓLICA")
    
    # Winter
    p_esp = (1.5 * hco3) + 8
    st.info(f"Fórmula de Winter (pCO2 esperada): {p_esp:.1f} (+/- 2)")
    if pco2 < (p_esp - 2): st.warning("Trastorno Secundario: Alcalosis Respiratoria Asociada")
    elif pco2 > (p_esp + 2): st.warning("Trastorno Secundario: Acidosis Respiratoria Asociada")
    else: st.success("Estado: Acidosis Metabólica Compensada")
    
    # Anion Gap y Causas
    st.metric("Anion Gap Corregido", f"{ag_corr:.1f}")
    if ag_corr > 12:
        st.warning("**Causas (GOLDMARCC):** Glicoles, Oxoproline, Lactato, Metanol, Aspirina, Renal, Cetoacidosis.")
        # Delta-Delta
        delta_ag = ag_corr - 12
        delta_hco3 = 24 - hco3
        if (delta_ag / delta_hco3) > 1.6: st.info("Sugerencia: Alcalosis Metabólica pre-existente.")
    else:
        st.info("**Causas:** Diarrea, ATR, Hipercloremia.")

# 2. Acidosis Respiratoria (Primario si pH < 7.36 y pCO2 > 32)
elif ph < 7.36 and pco2 > 32:
    st.error("DIAGNÓSTICO: ACIDEMIA RESPIRATORIA")
    st.warning("**Causas:** EPOC, Obesidad, Depresión SNC, Enfermedad Neuromuscular.")
    h_esp = 20 + (0.1 * (pco2 - 30)) # Ajuste agudo Bogotá
    st.info(f"HCO3 Esperado (Agudo): {h_esp:.1f}")

# 3. Alcalosis
elif ph > 7.44:
    st.success("DIAGNÓSTICO: ALCALEMIA")
    if pco2 < 28: st.subheader("Primario: Alcalosis Respiratoria")
    else: st.subheader("Primario: Alcalosis Metabólica")

# 4. Otros casos
else:
    st.info("ESTADO: pH en rango normal. Analizar posibles trastornos mixtos compensados.")

# C. OXIGENACIÓN COMPLETA
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
with c3:
    st.metric("Índice de ROX", f"{rox:.2f}")

st.subheader(f"Gradiente Aa: {grad:.1f}")
if grad > (0.25 * edad + 8): # Fórmula de gradiente esperado según edad
    st.write("Interpretación: Gradiente Elevado (Alteración parenquimatosa).")
else:
    st.write("Interpretación: Gradiente Normal para la edad.")

st.caption("Gases 2600 - Dr. Gonzalo Bernal - Médico Familiar")

import streamlit as st

# 1. IDENTIFICACIÓN PROFESIONAL Y ESTUDIANTE
st.set_page_config(page_title="Gases 2600 - Dr. Bernal", page_icon="🫁", layout="wide")

st.markdown("<h1 style='text-align: center;'>🫁 Gases 2600</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Autor: Dr. Gonzalo Bernal</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>Médico Familiar</b></p>", unsafe_allow_html=True)
st.divider()

# 2. ENTRADA DE DATOS (IDENTIFICACIÓN)
st.sidebar.header("📝 Registro de Uso")
estudiante = st.sidebar.text_input("Nombre del Estudiante / Usuario")
id_estudiante = st.sidebar.text_input("ID / Cédula")
# Nota: Streamlit Cloud Analytics rastrea automáticamente el número de sesiones en su panel.

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("👤 Datos Paciente")
    edad = st.number_input("Edad (años)", 0, 115, 45)
    fr = st.number_input("Frecuencia Resp. (rpm)", 8, 60, 20)
    spo2 = st.number_input("Saturación O2 (%)", 50, 100, 94)

with col2:
    st.subheader("🧪 Bioquímica")
    ph = st.number_input("pH Arterial", 6.80, 7.80, 7.40, 0.01)
    pco2 = st.number_input("pCO2 (mmHg)", 10.0, 90.0, 30.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 5.0, 50.0, 20.0, 0.1)
    na = st.number_input("Sodio (Na)", 110.0, 160.0, 140.0, 0.1)
    cl = st.number_input("Cloro (Cl)", 70.0, 130.0, 105.0, 0.1)

with col3:
    st.subheader("🫁 Oxigenación")
    pa02 = st.number_input("PaO2 (mmHg)", 20.0, 200.0, 60.0, 0.1)
    fio2 = st.number_input("FiO2 (fracción)", 0.21, 1.0, 0.21, 0.01)
    alb = st.number_input("Albúmina (g/dL)", 1.0, 5.0, 4.0, 0.1)

# --- PROCESAMIENTO LÓGICO ---
if ph and pco2 and hco3:
    st.divider()
    
    # A. CONSISTENCIA (HENDERSON)
    h_calc = 24 * (pco2 / hco3)
    h_ph = 10**(9 - ph)
    st.subheader("🔍 Consistencia Interna")
    if abs(h_calc - h_ph) < 5:
        st.success(f"✅ Gases Consistentes (H+ calc: {h_calc:.1f})")
    else:
        st.error(f"⚠️ Gases Inconsistentes. El equilibrio químico no coincide con el pH medido.")

    # B. INTERPRETACIÓN ÁCIDO-BASE (ORDEN EXCEL)
    st.header("🔬 Interpretación Clínica")
    ag_obs = na - (cl + hco3)
    ag_corr = ag_obs + 2.5 * (4 - alb)
    delta_ag = ag_corr - 12
    delta_hco3 = 24 - hco3
    delta_ratio = delta_ag / delta_hco3 if delta_hco3 != 0 else 0

    if ph < 7.36:
        st.error(f"ESTADO: ACIDEMIA")
        if hco3 < 18:
            st.subheader("1. Trastorno Primario: ACIDOSIS METABÓLICA")
            p_esp = (1.5 * hco3) + 8
            st.info(f"2. Fórmula de Winter (pCO2 esperada): {p_esp:.1f} (+/- 2)")
            
            if pco2 < (p_esp - 2): st.warning("3. Interpretación: Alcalosis Respiratoria Asociada (Sobrecompensación)")
            elif pco2 > (p_esp + 2): st.warning("3. Interpretación: Acidosis Respiratoria Asociada (Falla ventilatoria)")
            else: st.success("3. Interpretación: Compensación respiratoria adecuada.")

            st.metric("4. Anion Gap Corregido", f"{ag_corr:.1f}")
            if ag_corr > 12:
                st.warning("5. Causas (GOLDMARCC): Glicoles, Oxoproline, Lactato, Metanol, Aspirina, Renal, Cetoacidosis.")
                st.write(f"**Delta Ratio:** {delta_ratio:.2f}")
            else:
                st.info("5. Causas AG Normal: Diarrea, ATR, Hipercloremia.")
        else:
            st.subheader("1. Trastorno Primario: ACIDOSIS RESPIRATORIA")
            st.warning("Causas: Obstrucción, Depresión SNC, EPOC.")

    # C. OXIGENACIÓN COMPLETA
    st.divider()
    st.header("📊 Perfil de Oxigenación")
    grad = ((fio2 * (560 - 47)) - (pco2 / 0.8)) - pa02
    pafi = pa02 / fio2
    safi = spo2 / fio2
    rox = (safi / fr)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("PAFI", f"{pafi:.1f}")
    c2.metric("SAFI", f"{safi:.1f}")
    c3.metric("Índice de ROX", f"{rox:.2f}")
    c4.metric("Gradiente Aa", f"{grad:.1f}")

    grad_esp = 0.25 * edad + 8
    if grad > grad_esp:
        st.write(f"Interpretación: **Gradiente Elevado** (Esperado: {grad_esp:.1f}). Alteración del parénquima.")
    else:
        st.write("Interpretación: **Gradiente Normal**. Causa extrapulmonar.")

st.caption(f"Reporte generado para: {estudiante if estudiante else 'Sin nombre'} | ID: {id_estudiante}")
st.caption("Gases 2600 - Propiedad Intelectual del Dr. Gonzalo Bernal")

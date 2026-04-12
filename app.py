import streamlit as st

# 1. IDENTIFICACIÓN
st.set_page_config(page_title="Gases 2600 - Dr. Bernal", page_icon="🫁")

st.markdown("<h1 style='text-align: center;'>🫁 Gases 2600</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Autor: Dr. Gonzalo Bernal</h3>", unsafe_allow_html=True)
st.divider()

# 2. ENTRADA DE DATOS
col1, col2 = st.columns(2)
with col1:
    ph = st.number_input("pH Arterial", 6.80, 7.80, 7.40, 0.01)
    pco2 = st.number_input("pCO2 (mmHg)", 10.0, 90.0, 30.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 5.0, 50.0, 20.0, 0.1)
    na = st.number_input("Sodio (Na)", 110.0, 170.0, 140.0, 0.1)
with col2:
    cl = st.number_input("Cloro (Cl)", 70.0, 130.0, 105.0, 0.1)
    alb = st.number_input("Albúmina (g/dL)", 1.0, 5.0, 4.0, 0.1)
    pa02 = st.number_input("PaO2 (mmHg)", 20.0, 200.0, 60.0, 0.1)
    fio2 = st.number_input("FiO2", 0.21, 1.0, 0.21, 0.01)

# 3. CONSISTENCIA (HENDERSON)
st.divider()
h_calc = 24 * (pco2 / hco3)
h_ph = 10**(9 - ph)
st.subheader("🔍 Consistencia Interna")
if abs(h_calc - h_ph) < 4:
    st.success(f"✅ Gases Consistentes. H+ calc: {h_calc:.1f} | H+ ph: {h_ph:.1f}")
else:
    st.error(f"⚠️ Gases Inconsistentes. Sugerido revisar técnica.")

# 4. DIAGNÓSTICO ÁCIDO-BASE E INTERPRETACIÓN
st.divider()
st.header("🔬 Interpretación Ácido-Base")
ag_corr = (na - (cl + hco3)) + 2.5 * (4 - alb)

# Mostrar Anion Gap explícitamente
st.metric("Anion Gap Corregido", f"{ag_corr:.1f}", delta="Normal: 12")

if ph < 7.36:
    st.error("ESTADO: ACIDEMIA")
    if pco2 <= 30:
        st.subheader("Primario: Acidosis Metabólica")
        p_esp = (1.5 * hco3) + 8
        st.info(f"Winter (pCO2 esperada): {p_esp:.1f} (+/- 2)")
        # Interpretación de la compensación
        if pco2 < (p_esp - 2): st.warning("Interpretación: Alcalosis respiratoria asociada.")
        elif pco2 > (p_esp + 2): st.warning("Interpretación: Acidosis respiratoria asociada.")
        else: st.success("Interpretación: Compensación respiratoria adecuada.")
        
        if ag_corr > 12:
            st.warning("**Causas (GOLDMARCC):** Glicoles, Oxoproline, Lactato, Metanol, Aspirina, Renal, Cetoacidosis.")
    else:
        st.subheader("Primario: Acidosis Respiratoria")
elif ph > 7.44:
    st.success("ESTADO: ALCALEMIA")
    if pco2 < 30: st.subheader("Primario: Alcalosis Respiratoria")
    else: st.subheader("Primario: Alcalosis Metabólica")

# 5. OXIGENACIÓN CON INTERPRETACIÓN
st.divider()
st.header("📊 Análisis de Oxigenación")
grad = ((fio2 * (560 - 47)) - (pco2 / 0.8)) - pa02
pafi = pa02 / fio2

c1, c2 = st.columns(2)
with c1:
    st.metric("PAFI", f"{pafi:.1f}")
    if pafi > 300: st.write("✅ **Normal**")
    elif pafi > 200: st.write("⚠️ **Disfunción leve (SDRA leve)**")
    elif pafi > 100: st.write("❌ **Disfunción moderada (SDRA moderado)**")
    else: st.write("🚨 **Disfunción severa (SDRA severo)**")

with c2:
    st.metric("Gradiente Aa", f"{grad:.1f}")
    if grad > 20: st.write("❌ **Elevado**: Sugiere problema en parénquima pulmonar.")
    else: st.write("✅ **Normal**: Sugiere hipoventilación o causas extrapulmonares.")

st.write("---")
st.caption("Gases 2600 - Propiedad intelectual del Dr. Gonzalo Bernal")

import streamlit as st

# Configuración profesional
st.set_page_config(page_title="Gases 2600 - Dr. Bernal", page_icon="🫁", layout="wide")

st.title("🫁 Gases 2600: Herramienta de Diagnóstico Avanzado")
st.markdown("---")

# --- 1. ENTRADA DE DATOS (EDAD Y ELECTROLITOS) ---
with st.sidebar:
    st.header("👤 Datos del Paciente")
    nombre = st.text_input("Nombre/ID")
    edad = st.number_input("Edad (años)", 0, 110, 45)
    peso = st.number_input("Peso (kg)", 1.0, 200.0, 70.0)
    st.divider()
    st.info("Configurado para Bogotá (PB: 560 mmHg)")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🧪 Gases Arteriales")
    ph = st.number_input("pH", 6.80, 7.80, 7.40, 0.01)
    pco2 = st.number_input("pCO2 (mmHg)", 10.0, 90.0, 30.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 5.0, 50.0, 20.0, 0.1)
    pa02 = st.number_input("PaO2 (mmHg)", 20.0, 200.0, 60.0, 0.1)
    fio2 = st.number_input("FiO2 (Ej: 0.21)", 0.21, 1.0, 0.21)

with col2:
    st.subheader("🩸 Electrolitos y Química")
    na = st.number_input("Sodio (Na)", 110.0, 170.0, 140.0)
    cl = st.number_input("Cloro (Cl)", 70.0, 130.0, 105.0)
    k = st.number_input("Potasio (K)", 1.0, 10.0, 4.0)
    alb = st.number_input("Albúmina (g/dL)", 1.0, 5.5, 4.0)

# --- 2. CONSISTENCIA INTERNA (HENDERSON) ---
st.divider()
h_calculado = 24 * (pco2 / hco3)
h_por_ph = 10**(9 - ph)
diferencia = abs(h_calculado - h_por_ph)

st.header("🔍 Análisis de Consistencia")
if diferencia < 4:
    st.success(f"✅ Gases Consistentes (Dif: {diferencia:.2f}). H+ calc: {h_calculado:.1f}")
else:
    st.error(f"⚠️ Gases Inconsistentes (Dif: {diferencia:.2f}). Verificar datos.")

# --- 3. DIAGNÓSTICO ÁCIDO-BASE ---
st.header("🔬 Interpretación Médica")

# Anion Gap Corregido
ag_obs = na - (cl + hco3)
ag_corr = ag_obs + 2.5 * (4.5 - alb)

# Trastorno Primario
if ph < 7.36:
    tipo = "Acidemia"
    if pco2 <= 30:
        primario = "Acidosis Metabólica"
        # Winter
        p_esp = (1.5 * hco3) + 8
        rango = (p_esp - 2, p_esp + 2)
        estado_comp = "Compensada" if rango[0] <= pco2 <= rango[1] else "No compensada"
    else:
        primario = "Acidosis Respiratoria"
elif ph > 7.44:
    tipo = "Alcalemia"
    if pco2 < 30: primario = "Alcalosis Respiratoria"
    else: primario = "Alcalosis Metabólica"
else:
    tipo = "Equilibrio/Mixto"
    primario = "Normal o Trastorno Mixto"

st.subheader(f"Estado: {tipo} | Primario: {primario}")

# --- 4. CAUSAS (GOLDMARCC) Y DELTA-DELTA ---
if "Metabólica" in primario:
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.metric("Anion Gap Corregido", f"{ag_corr:.1f}")
        if ag_corr > 12:
            st.warning("**Causas GOLDMARCC:** Glicoles, Oxoproline, L-Lactato, D-Lactato, Metanol, Aspirina, Renal (Uremia), Cetoacidosis.")
        else:
            st.info("**Causas AG Normal:** Diarrea, ATR, Fístulas, Hipercloremia.")
    
    with col_res2:
        if ag_corr > 12:
            delta_ag = ag_corr - 12
            delta_hco3 = 24 - hco3
            ratio = delta_ag / delta_hco3
            st.metric("Ratio Delta/Delta", f"{ratio:.2f}")
            if ratio < 0.4: st.write("Acidosis metabólica de AG normal asociada.")
            elif ratio > 2: st.write("Alcalosis metabólica asociada.")

# --- 5. OXIGENACIÓN ---
st.divider()
paafi = pa02 / fio2
grad_aa = ((fio2 * (560 - 47)) - (pco2 / 0.8)) - pa02
st.header("🫁 Función Respiratoria")
c1, c2 = st.columns(2)
c1.metric("PAFI", f"{paafi:.1f}")
c2.metric("Gradiente Aa", f"{grad_aa:.1f}")

st.caption("Fórmulas aplicadas: Winter (compensación), Henderson (consistencia), Figueras (AG corregido).")

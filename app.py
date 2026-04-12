import streamlit as st
import datetime

# 1. IDENTIFICACIÓN PROFESIONAL
st.set_page_config(page_title="Gases 2600 - Dr. Bernal", layout="wide")

st.markdown("<h1 style='text-align: center;'>🫁 Gases 2600</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Autor: Dr. Gonzalo Bernal - Médico Familiar</h3>", unsafe_allow_html=True)
st.divider()

# --- SISTEMA DE ESTADÍSTICA SIMPLE ---
if 'contador_uso' not in st.session_state:
    st.session_state['contador_uso'] = 1
else:
    st.session_state['contador_uso'] += 1

# 2. ENTRADA DE DATOS
c1, c2, c3 = st.columns(3)
with c1:
    st.subheader("🧪 Bioquímica")
    ph = st.number_input("pH Arterial", 6.80, 7.80, 7.24, 0.01)
    pco2 = st.number_input("pCO2 (mmHg)", 10.0, 90.0, 24.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 5.0, 50.0, 10.0, 0.1)
with c2:
    st.subheader("🩸 Electrolitos")
    na = st.number_input("Sodio (Na)", 110.0, 160.0, 140.0, 0.1)
    cl = st.number_input("Cloro (Cl)", 70.0, 130.0, 102.0, 0.1)
    alb = st.number_input("Albúmina (g/dL)", 1.0, 5.0, 3.0, 0.1)
with c3:
    st.subheader("🫁 Oxigenación")
    pa02 = st.number_input("PaO2 (mmHg)", 20.0, 200.0, 55.0, 0.1)
    fio2 = st.number_input("FiO2 (0.21-1.0)", 0.21, 1.0, 0.35, 0.01)
    edad = st.number_input("Edad (años)", 0, 115, 45)
    fr = st.number_input("FR (resp/min)", 8, 60, 24)
    spo2 = st.number_input("SatO2 (%)", 50, 100, 90)

# --- PROCESAMIENTO ÁCIDO-BASE ---
st.divider()
h_calc = 24 * (pco2 / hco3)
h_ph = 10**(9 - ph)

# Paso 1: Consistencia
st.subheader("🔍 Paso 1: Consistencia Interna")
if abs(h_calc - h_ph) < 5:
    st.success(f"✅ Gases Consistentes (H+ calc: {h_calc:.1f})")
else:
    st.error("⚠️ Gases Inconsistentes.")

# Paso 2 al 6: Ácido-Base
ag_corr = (na - (cl + hco3)) + (2.5 * (4 - alb))
if ph < 7.36 and hco3 < 19:
    st.header("🔬 Análisis de Acidosis Metabólica")
    st.info(f"pCO2 Esperada (Winter): {(1.5 * hco3) + 8:.1f}")
    st.metric("Anion Gap Corregido", f"{ag_corr:.1f}")
    
    # Delta del Gap (Paso 6)
    delta_gap = (ag_corr - 10) - (20 - hco3)
    st.subheader(f"Paso 6: Delta del Gap: {delta_gap:.1f}")
    if -5 <= delta_gap <= 5: st.write("Interpretación: Acidosis Metabólica Pura")
    elif delta_gap > 5: st.write("Interpretación: Alcalosis Metabólica Sobreagregada")
    else: st.write("Interpretación: Acidosis Metabólica Hiperclorémica")
    
    if ag_corr > 12:
        st.warning("**Causas (GOLDMARCC):** Glicoles, Oxoproline, L-Lactato, D-Lactato, Metanol, Aspirina, Renal (Uremia), Cetoacidosis.")

# --- PASO 7: OXIGENACIÓN DETALLADA (SU PETICIÓN) ---
st.divider()
st.header("📊 Paso 7: Perfil de Oxigenación y Causas")

# Cálculos de Oxigenación
pa_alveolar = (fio2 * (560 - 47)) - (pco2 / 0.8)
grad_paciente = pa_alveolar - pa02
grad_ideal = (edad / 4) + 4
diferencia_grad = grad_paciente - grad_ideal

pafi = pa02 / fio2
safi = spo2 / fio2
rox = (safi / fr)

col_ox1, col_ox2 = st.columns(2)
with col_ox1:
    st.metric("Gradiente Aa Paciente", f"{grad_paciente:.1f} mmHg")
    st.metric("Gradiente Aa Ideal (Edad)", f"{grad_ideal:.1f} mmHg")
    st.write(f"**Desviación del Ideal:** {diferencia_grad:.1f} mmHg")

with col_ox2:
    st.metric("PAFI", f"{pafi:.1f}")
    st.metric("Índice de ROX", f"{rox:.2f}")

# CAUSAS DE OXIGENACIÓN SEGÚN EL GRADIENTE
st.subheader("🧐 Interpretación de la Oxigenación")
if grad_paciente > grad_ideal + 5:
    st.error("🚨 GRADIENTE ELEVADO: El problema está en el PARÉNQUIMA PULMONAR.")
    st.write("**Causas Posibles:**")
    st.write("* **Desequilibrio V/Q:** Neumonía, Asma, EPOC, TEP.")
    st.write("* **Shunt Derecha-Izquierda:** Edema agudo de pulmón, SDRA, Colapso alveolar.")
    st.write("* **Trastorno de Difusión:** Fibrosis pulmonar.")
else:
    st.success("✅ GRADIENTE NORMAL: El pulmón está sano, el problema es EXTRAPULMONAR.")
    st.write("**Causas Posibles:**")
    st.write("* **Hipoventilación Pura:** Depresión del SNC, sobredosis, enfermedad neuromuscular.")
    st.write("* **Disminución de FiO2:** Grandes alturas (aunque estamos en Bogotá, evaluar si es mayor la altura).")

# 3. ESTADÍSTICAS DE USO
st.divider()
st.caption(f"Registro de actividad: Esta aplicación ha procesado {st.session_state['contador_uso']} análisis en esta sesión.")
st.caption(f"Fecha del análisis: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.caption("Gases 2600 - Propiedad Intelectual del Dr. Gonzalo Bernal")

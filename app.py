import streamlit as st

# 1. CONFIGURACIÓN E IDENTIFICACIÓN PROFESIONAL
st.set_page_config(page_title="Gases 2600 - Dr. Bernal", page_icon="🫁", layout="wide")

st.markdown("<h1 style='text-align: center;'>🫁 Gases 2600</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Autor: Dr. Gonzalo Bernal</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'><b>Médico Familiar</b></p>", unsafe_allow_html=True)
st.divider()

# 2. CAMPOS DE REGISTRO (AHORA VISIBLES AL PRINCIPIO)
st.subheader("📝 Registro de Usuario (Opcional)")
col_reg1, col_reg2 = st.columns(2)
with col_reg1:
    nombre_estudiante = st.text_input("Nombre del Estudiante / Médico", placeholder="Ej: Juan Pérez")
with col_reg2:
    id_estudiante = st.text_input("ID / Cédula", placeholder="Opcional")

st.divider()

# 3. ENTRADA DE DATOS CLÍNICOS
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("👤 Paciente")
    edad = st.number_input("Edad (años)", 0, 115, 45)
    fr = st.number_input("Frecuencia Resp. (rpm)", 8, 60, 24)
    spo2 = st.number_input("Saturación O2 (%)", 50, 100, 94)

with col2:
    st.subheader("🧪 Bioquímica")
    ph = st.number_input("pH Arterial", 6.80, 7.80, 7.24, 0.01)
    pco2 = st.number_input("pCO2 (mmHg)", 10.0, 90.0, 24.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 5.0, 50.0, 10.0, 0.1)
    na = st.number_input("Sodio (Na)", 110.0, 160.0, 140.0, 0.1)
    cl = st.number_input("Cloro (Cl)", 70.0, 130.0, 102.0, 0.1)

with col3:
    st.subheader("🫁 Oxigenación")
    pa02 = st.number_input("PaO2 (mmHg)", 20.0, 200.0, 55.0, 0.1)
    fio2 = st.number_input("FiO2 (0.21 - 1.0)", 0.21, 1.0, 0.35, 0.01)
    alb = st.number_input("Albúmina (g/dL)", 1.0, 5.0, 3.0, 0.1)

# --- PROCESAMIENTO ---
st.divider()

# A. CONSISTENCIA
h_calc = 24 * (pco2 / hco3)
h_ph = 10**(9 - ph)
st.subheader("🔍 Consistencia Interna")
if abs(h_calc - h_ph) < 5:
    st.success(f"✅ Gases Consistentes (H+ calc: {h_calc:.1f})")
else:
    st.error(f"⚠️ Gases Inconsistentes. Revisar técnica.")

# B. ANÁLISIS ÁCIDO-BASE
st.header("🔬 Interpretación Ácido-Base")

ag_medido = na - (cl + hco3)
ag_corr = ag_medido + (2.5 * (4 - alb))
delta_del_gap = (ag_corr - 10) - (20 - hco3)

if ph < 7.36:
    st.error("ESTADO: ACIDEMIA")
    if hco3 < 19:
        st.subheader("Trastorno Primario: ACIDOSIS METABÓLICA")
        p_esp = (1.5 * hco3) + 8
        st.info(f"Fórmula de Winter (pCO2 esperada): {p_esp:.1f} (+/- 2)")
        
        # Delta del Gap (Paso 6 del Excel)
        st.markdown(f"### **⚖️ Delta del Gap: {delta_del_gap:.1f}**")
        if -5 <= delta_del_gap <= 5:
            st.success("Interpretación: Acidosis Metabólica Pura")
        elif delta_del_gap > 5:
            st.warning("Interpretación: Alcalosis Metabólica Sobreagregada")
        else:
            st.warning("Interpretación: Acidosis Metabólica Hiperclorémica")

        st.metric("Anion Gap Corregido", f"{ag_corr:.1f}")
        if ag_corr > 12:
            st.warning("**Causas (GOLDMARCC):** Glicoles, Oxoproline, L-Lactato, D-Lactato, Metanol, Aspirina, Renal (Uremia), Cetoacidosis.")
        else:
            st.info("**Causas AG Normal:** Diarrea, ATR, Fístulas.")
    else:
        st.subheader("Trastorno Primario: ACIDOSIS RESPIRATORIA")

# C. OXIGENACIÓN
st.divider()
st.header("📊 Perfil de Oxigenación")
grad = ((fio2 * (560 - 47)) - (pco2 / 0.8)) - pa02
pafi = pa02 / fio2
safi = spo2 / fio2
rox = (safi / fr)

c1, c2, c3, c4 = st.columns(4)
c1.metric("PAFI", f"{pafi:.1f}")
c2.metric("SAFI", f"{safi:.1f}")
c3.metric("ROX", f"{rox:.2f}")
c4.metric("Grad. Aa", f"{grad:.1f}")

grad_esp = (edad / 4) + 4
if grad > grad_esp:
    st.write(f"Interpretación: **Gradiente Elevado** (Límite: {grad_esp:.1f}).")
else:
    st.write("Interpretación: **Gradiente Normal**.")

st.divider()
user_final = nombre_estudiante if nombre_estudiante else "Usuario Anónimo"
st.write(f"**Reporte para:** {user_final}")
if id_estudiante: st.write(f"**ID:** {id_estudiante}")
st.caption("Gases 2600 - Propiedad Intelectual del Dr. Gonzalo Bernal")

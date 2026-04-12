import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Gases 2600 - Dr. Bernal", page_icon="🫁", layout="centered")

st.title("🫁 Gases 2600")
st.markdown("### Herramienta Médica Integral (Bogotá - 2600 msnm)")

# --- ENTRADA DE DATOS ---
st.header("⌨️ Ingreso de Datos")
col1, col2 = st.columns(2)

with col1:
    ph = st.number_input("pH Arterial", 6.80, 7.80, 7.40, 0.01)
    pco2 = st.number_input("pCO2 (mmHg)", 10.0, 80.0, 30.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 5.0, 50.0, 20.0, 0.1)
    na = st.number_input("Sodio Sérico (Na+)", 100.0, 160.0, 140.0, 0.1)

with col2:
    pa02 = st.number_input("PaO2 (mmHg)", 30.0, 200.0, 60.0, 0.1)
    fio2 = st.number_input("FiO2 (Ej: 0.21)", 0.21, 1.0, 0.21, 0.01)
    cl = st.number_input("Cloro Sérico (Cl-)", 70.0, 130.0, 104.0, 0.1)
    fr = st.number_input("Frecuencia Resp. (bpm)", 8, 60, 20)

# --- ANÁLISIS ÁCIDO-BASE ---
st.divider()
st.header("🔬 Diagnóstico Ácido-Base")

# Trastorno Primario
if ph < 7.36:
    trastorno = "Acidemia"
    primario = "Acidosis Metabólica" if pco2 <= 30 else "Acidosis Respiratoria"
elif ph > 7.44:
    trastorno = "Alcalemia"
    primario = "Alcalosis Respiratoria" if pco2 <= 30 else "Alcalosis Metabólica"
else:
    trastorno = "Equilibrio"
    primario = "Normal o Mixto"

st.subheader(f"Estado: {trastorno} / Primario: {primario}")

# Cálculos de Compensación y Causas
if "Metabólica" in primario:
    pco2_esp = (1.5 * hco3) + 8
    ag = na - (cl + hco3)
    st.write(f"**pCO2 Esperada (Winter):** {pco2_esp:.1f} mmHg")
    st.write(f"**Anion Gap:** {ag:.1f}")
    if ag > 12:
        st.error("⚠️ CAUSAS (GOLDMARCC): Glicoles, Oxoproline, L-Lactato, D-Lactato, Metanol, Aspirina, Renal (Uremia), Cetoacidosis.")
    else:
        st.warning("⚠️ CAUSAS (Hiperclorémica): Diarrea, Fístulas, Acidosis Tubular Renal.")

if "Respiratoria" in primario:
    if "Acidosis" in primario:
        st.error("⚠️ CAUSAS: EPOC, Asma grave, Obstrucción vía aérea, Depresión del SNC, Enfermedad Neuromuscular.")
    else:
        st.success("⚠️ CAUSAS: Ansiedad, Dolor, Fiebre, TEP, Altitud, Embarazo, Sepsis temprana.")

# --- OXIGENACIÓN ---
st.divider()
st.header("🫁 Resultados de Oxigenación")
gradiente = ( (fio2 * (560 - 47)) - (pco2 / 0.8) ) - pa02
rox = (pa02 / fio2) / fr
st.write(f"**Gradiente Alveolo-Arterial (Aa):** {gradiente:.1f}")
st.write(f"**Índice de ROX:** {rox:.1f}")

st.info("Nota: Cálculos ajustados para presión barométrica de 560 mmHg (Bogotá).")

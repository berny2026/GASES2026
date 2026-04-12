import streamlit as st

# Configuración visual de la App
st.set_page_config(page_title="Gases 2600", page_icon="🫁", layout="centered")

# Estilo personalizado Modo Oscuro y Footer
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stNumberInput label { color: #00d4ff !important; font-weight: bold; }
    footer { visibility: hidden; }
    .custom-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0e1117;
        color: #888;
        text-align: center;
        padding: 10px;
        font-size: 12px;
        border-top: 1px solid #333;
    }
    </style>
    <div class="custom-footer">
        © 2026 - Algoritmo Original y Propiedad Intelectual: <b>Dr. Gonzalo Bernal Ferreira, Médico Familiar</b>. <br>
        Optimizado para la altitud de Bogotá (2600 msnm).
    </div>
    """, unsafe_allow_html=True)

st.title("🫁 Gases 2600")
st.write("---")

# --- ENTRADA DE DATOS ---
st.subheader("⌨️ Ingreso de Datos del Paciente")
col1, col2 = st.columns(2)

with col1:
    ph = st.number_input("pH Arterial", min_value=6.5, max_value=8.0, value=7.28, step=0.01)
    pco2 = st.number_input("pCO2 (mmHg)", value=30.0)
    hco3 = st.number_input("HCO3 (mEq/L)", value=14.0)
    edad = st.number_input("Edad del Paciente", value=50)

with col2:
    pao2 = st.number_input("PaO2 (mmHg)", value=55.0)
    fio2 = st.number_input("FiO2 (Ej: 0.21)", value=0.21, step=0.01)
    fr = st.number_input("Frecuencia Respiratoria", value=24)
    sat = st.number_input("Saturación SpO2 (%)", value=88.0)

# --- CÁLCULOS INTERNOS (El cerebro del Excel) ---
# Gradiente Alveolo-arterial
pao2_alv = (513 * fio2) - (pco2 / 0.8)
grad_real = pao2_alv - pao2
grad_ideal = (edad / 4) + 4
diferencia_grad = grad_real - grad_ideal

# ROX Index
rox = (sat / fio2) / fr if (fr > 0 and fio2 > 0) else 0

# --- LÓGICA DE DIAGNÓSTICO (Columna AY del Excel) ---
if diferencia_grad < 10:
    if pco2 > 32:
        dx_oxigenacion = "Hipoventilación Pura (SNC, Sedación, Neuromuscular)"
    else:
        dx_oxigenacion = "FiO2 baja (Altitud) o Error en muestra"
else:
    if pco2 > 32:
        dx_oxigenacion = "Causa Mixta (EPOC, Asma grave, Obstrucción)"
    else:
        dx_oxigenacion = "Alteración V/Q o Shunt (Neumonía, TEP, SDRA, Sepsis)"

# --- MOSTRAR RESULTADOS ---
st.write("---")
st.subheader("📊 Resultados de Oxigenación")

res_col1, res_col2 = st.columns(2)
with res_col1:
    st.metric("Gradiente A-a Real", f"{grad_real:.1f}")
    st.metric("Diferencia (R-I)", f"{diferencia_grad:.1f}")

with res_col2:
    st.metric("Índice de ROX", f"{rox:.1f}")
    pulmon_estado = "🟢 Pulmón Sano" if diferencia_grad < 10 else "🔴 Pulmón Lesionado"
    st.info(pulmon_estado)

st.success(f"**Diagnóstico Sugerido:** {dx_oxigenacion}")

# --- BOTÓN DE COMPARTIR ---
st.write("---")
if st.button("🔗 Generar link para compartir"):
    st.write("Copia este link y envíalo a tus colegas: https://gases2600.streamlit.app")

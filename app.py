import streamlit as st
import streamlit.components.v1 as components

# --- 1. GOOGLE ANALYTICS ---
components.html("""
<script async src="https://www.googletagmanager.com/gtag/js?id=G-KF0W30KFST"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-KF0W30KFST');
</script>
""", height=0)

# --- 2. CONFIGURACIÓN ---
st.set_page_config(page_title="Gases 2600 PRO - Bogotá", layout="wide")
st.markdown("<h1 style='text-align: center; color: #D32F2F;'>🏔️ Gases Arteriales Bogotá (2600m)</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Dr. Gonzalo Bernal Ferreira</h3>", unsafe_allow_html=True)

# --- 3. ENTRADA DE DATOS ---
with st.sidebar:
    st.header("⌨️ Parámetros Clínicos")
    ph = st.number_input("pH Arterial", 6.80, 7.80, 7.18, 0.01)
    pco2 = st.number_input("PaCO2 (mmHg)", 10.0, 100.0, 55.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 2.0, 50.0, 20.0, 0.1)
    st.divider()
    na = st.number_input("Sodio (Na)", 110.0, 170.0, 140.0, 0.1)
    cl = st.number_input("Cloro (Cl)", 60.0, 140.0, 105.0, 0.1)
    alb = st.number_input("Albúmina (g/dL)", 0.5, 6.0, 4.0, 0.1)
    st.divider()
    pa02 = st.number_input("PaO2 (mmHg)", 10.0, 300.0, 48.0, 0.1)
    spo2 = st.number_input("SpO2 (%)", 30, 100, 78)
    fio2 = st.number_input("FiO2 (decimal)", 0.21, 1.00, 0.21, 0.01)
    edad = st.number_input("Edad (años)", 0, 110, 40)
    fr = st.number_input("FR (resp/min)", 4, 70, 8)

# --- 4. CÁLCULOS ---
h_ion = 24 * (pco2 / hco3)
r80 = 80 - float(f"{ph:.2f}"[-2:])
ag_c = (na - (cl + hco3)) + (2.5 * (4 - alb))
pao2_calc = (fio2 * 513) - (pco2 / 0.8)
g_real = pao2_calc - pa02
g_id = (edad / 4) + 4
pafi, safi = pa02/fio2, spo2/fio2
rox = (safi / fr) if fr > 0 else 0

# --- 5. RESULTADOS ---

# I. CONSISTENCIA
st.subheader("✅ I. Consistencia Interna")
if 0.8 <= (h_ion / r80) <= 1.2:
    st.success(f"MUESTRA VÁLIDA: H+ ({h_ion:.1f})")
else:
    st.error("❌ MUESTRA NO CONFIABLE")

# II. EQUILIBRIO ÁCIDO-BASE
st.subheader("⚖️ II. Equilibrio Ácido-Base")
col1, col2 = st.columns(2)
with col1:
    if pco2 > 32:
        st.error("🛑 ACIDOSIS RESPIRATORIA")
        with st.expander("🔍 CAUSAS (Centro a Periferia)", expanded=True):
            st.markdown("""
            * **SNC:** Sedación, ACV, Trauma, Apnea central.
            * **SNP:** Guillain-Barré, Polineuropatía.
            * **Placa NM:** Miastenia Gravis, Bloqueantes NM, Botulismo.
            * **Músculo:** Fatiga diafragmática, Distrofias.
            * **Caja/Columna:** Cifoescoliosis, Tórax inestable, Obesidad.
            * **Alvéolo:** EPOC, Asma (Atrapamiento), Obstrucción VA.
            """)
with col2:
    st.metric("Anión Gap Corregido", f"{ag_c:.1f}")
    if ag_c > 12:
        with st.expander("🔍 GOLDMARCC"):
            st.write("Glicoles, Oxiprolina, Lactato, D-Lactato, Metanol, Aspirina, Renal, Cetoacidosis, Creatinina.")

# III. OXIGENACIÓN Y CAUSAS DE HIPOXEMIA
st.subheader("☁️ III. Oxigenación y Causas de Hipoxemia")
o1, o2, o3, o4 = st.columns(4)
o1.metric("PAFI", f"{pafi:.0f}")
o2.metric("SAFI", f"{safi:.0f}")
o3.metric("ROX Index", f"{rox:.2f}")
o4.metric("Gradiente A-a", f"{g_real:.1f}", f"Ideal: {g_id:.1f}")

# PANEL CRÍTICO DE HIPOXEMIA
if pa02 < 60:
    st.error(f"🚨 HIPOXEMIA DETECTADA (PaO2: {pa02} mmHg)")
    
    # Clasificación por Gradiente
    if g_real > (g_id + 10):
        st.warning("⚠️ GRADIENTE ELEVADO: La causa es INTRAPULMONAR (Falla de transferencia)")
        with st.expander("🔍 VER CAUSAS DE HIPOXEMIA (Gradiente A-a Alto)", expanded=True):
            st.markdown("""
            1. **Shunt (Cortocircuito):** Alvéolos ocupados (Pus, agua, sangre) o colapsados. No responde a O2.
            2. **Desequilibrio V/Q:** La causa más común (EPOC, Asma, Neumonía, TEP). Responde a O2.
            3. **Trastorno de Difusión:** Engrosamiento de la membrana (Fibrosis, Intersticiopatías).
            """)
    else:
        st.success("✅ GRADIENTE NORMAL: La causa es EXTRAPULMONAR (Pulmón sano)")
        with st.expander("🔍 VER CAUSAS DE HIPOXEMIA (Gradiente A-a Normal)", expanded=True):
            st.markdown("""
            1. **Disminución de la PiO2:** Grandes alturas (Bogotá 2600m).
            2. **Hipoventilación Alveolar:** PaCO2 elevada (falla de bomba, sedación, etc.).
            """)
    
    with st.expander("🔍 OTRAS CAUSAS (No dependen del Gradiente)"):
        st.markdown("""
        1. **Disminución del Contenido Venoso de O2:** Bajo gasto cardíaco, anemia severa.
        2. **Hemoglobinas Anómalas:** Carboxihemoglobina, Metahemoglobina.
        """)

st.caption("Gases 2600 PRO - Bogotá v7.0 | Dr. Gonzalo Bernal Ferreira")

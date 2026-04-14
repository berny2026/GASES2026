import streamlit as st
import streamlit.components.v1 as components

# --- 1. GOOGLE ANALYTICS (ID: G-KF0W30KFST) ---
components.html("""
<script async src="https://www.googletagmanager.com/gtag/js?id=G-KF0W30KFST"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-KF0W30KFST');
</script>
""", height=0)

# --- 2. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Gases 2600 PRO - Bogotá", layout="wide")
st.markdown("<h1 style='text-align: center; color: #D32F2F;'>🏔️ Gases Arteriales Bogotá (2600m)</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Dr. Gonzalo Bernal Ferreira</h3>", unsafe_allow_html=True)

# --- 3. ENTRADA DE DATOS ---
with st.sidebar:
    st.header("⌨️ Parámetros Clínicos")
    ph = st.number_input("pH Arterial", 6.80, 7.80, 7.15, 0.01)
    pco2 = st.number_input("PaCO2 (mmHg)", 10.0, 100.0, 60.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 2.0, 50.0, 20.0, 0.1)
    st.divider()
    na = st.number_input("Sodio (Na)", 110.0, 170.0, 140.0, 0.1)
    cl = st.number_input("Cloro (Cl)", 60.0, 140.0, 105.0, 0.1)
    alb = st.number_input("Albúmina (g/dL)", 0.5, 6.0, 4.0, 0.1)
    st.divider()
    pa02 = st.number_input("PaO2 (mmHg)", 10.0, 300.0, 45.0, 0.1)
    spo2 = st.number_input("SpO2 (%)", 30, 100, 78)
    fio2 = st.number_input("FiO2 (decimal)", 0.21, 1.00, 0.21, 0.01)
    edad = st.number_input("Edad (años)", 0, 110, 65)
    fr = st.number_input("FR (resp/min)", 4, 70, 8)

# --- 4. CÁLCULOS TÉCNICOS ---
h_ion = 24 * (pco2 / hco3)
r80 = 80 - float(f"{ph:.2f}"[-2:])
ag_c = (na - (cl + hco3)) + (2.5 * (4 - alb))
# Bogotá: (560 - 47) = 513
pao2_calc = (fio2 * 513) - (pco2 / 0.8)
g_real = pao2_calc - pa02
g_id = (edad / 4) + 4
pafi = pa02 / fio2
safi = spo2 / fio2
rox = (safi / fr) if fr > 0 else 0

# --- 5. VISUALIZACIÓN DE RESULTADOS ---

# A. BLOQUE DE CONSISTENCIA
st.subheader("✅ I. Consistencia Interna")
if 0.8 <= (h_ion / r80) <= 1.2:
    st.success(f"MUESTRA VÁLIDA: H+ calculado ({h_ion:.1f}) es congruente con el pH.")
else:
    st.error(f"❌ MUESTRA NO CONFIABLE: H+ {h_ion:.1f} no coincide con pH. ¿Muestra venosa o error?")

# B. BLOQUE ÁCIDO-BASE (MULTIDETECT)
st.subheader("⚖️ II. Diagnóstico del Equilibrio Ácido-Base")
col_base1, col_base2 = st.columns(2)

with col_base1:
    # Diagnóstico Respiratorio
    if pco2 > 32:
        st.error("🛑 ACIDOSIS RESPIRATORIA (Retención de CO2)")
        with st.expander("🔍 Causas VITAMINS", expanded=True):
            st.write("**V:** Vascular (ACV, TEP) | **I:** Sepsis, Neumonía | **T:** Opioides, BZD | **A:** Miastenia, GB | **M:** Hipopotasemia | **S:** Apnea, Obesidad.")
    elif pco2 < 28:
        st.success("🚨 ALCALOSIS RESPIRATORIA")

    # Diagnóstico Metabólico
    if hco3 < 19:
        st.error("🛑 ACIDOSIS METABÓLICA")
        win = (1.5 * hco3) + 8
        st.info(f"Compensación esperada (Winters): PaCO2 {win:.1f} ± 2")
        if pco2 > win + 2: st.warning("⚠️ Acidosis Respiratoria Sobreagregada")
    elif hco3 > 24:
        st.success("🚨 ALCALOSIS METABÓLICA")

with col_base2:
    # Análisis de Brechas (Obligatorio en Acidosis Metabólica o Gap Alto)
    st.metric("Anión Gap Corregido (Alb)", f"{ag_c:.1f}", delta="Corte: 12", delta_color="inverse")
    if ag_c > 12:
        with st.expander("🔍 Causas GOLDMARCC", expanded=True):
            st.write("**G:** Glicoles | **O:** Oxiprolina | **L:** Lactato | **D:** D-Lactato | **M:** Metanol | **A:** Aspirina | **R:** Renal | **C:** Cetoacidosis | **C:** Creatinina")
        
        delta_gap = (ag_c - 12) - (24 - hco3)
        if delta_gap > 6: st.success(f"🔍 Delta Gap ({delta_gap:.1f}): ALCALOSIS METABÓLICA ASOCIADA")
        elif delta_gap < -6: st.warning(f"🔍 Delta Gap ({delta_gap:.1f}): ACIDOSIS NO GAP ASOCIADA")

# C. BLOQUE DE OXIGENACIÓN BOGOTÁ
st.subheader("☁️ III. Oxigenación y Gradiente (2600m)")
o1, o2, o3, o4 = st.columns(4)

def cat_sdra(v):
    if v < 100: return "🔴 SEVERO"
    if v < 200: return "🟠 MODERADO"
    if v < 300: return "🟡 LEVE"
    return "🟢 NORMAL"

o1.metric("PAFI", f"{pafi:.0f}", cat_sdra(pafi))
o2.metric("SAFI", f"{safi:.0f}", cat_sdra(safi))
o3.metric("ROX Index", f"{rox:.2f}", "Falla VNI" if rox < 4.88 else "Estable")
o4.metric("Gradiente A-a", f"{g_real:.1f}", f"Ideal: {g_id:.1f}")

if g_real > (g_id + 10):
    st.error(f"DIAGNÓSTICO: LESIÓN INTRAPULMONAR (Gradiente {g_real:.1f} > {g_id:.1f})")
    with st.expander("🔍 Las 7 Causas de Hipoxemia"):
        st.write("1. Altura | 2. Hipoventilación | 3. Shunt | 4. V/Q desigual | 5. Difusión | 6. ↓Gasto | 7. Hb anómala")
else:
    st.success("DIAGNÓSTICO: PULMÓN SANO / CAUSA EXTRAPULMONAR")

st.caption("Gases 2600 PRO - Bogotá v6.0 | Dr. Gonzalo Bernal Ferreira")

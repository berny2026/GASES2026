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
st.set_page_config(page_title="Gases 2600 PRO - Final", layout="wide")
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

# --- 4. CÁLCULOS EXPERTOS ---
h_ion = 24 * (pco2 / hco3)
r80 = 80 - float(f"{ph:.2f}"[-2:])
ag_c = (na - (cl + hco3)) + (2.5 * (4 - alb))
# Bogotá: FiO2 * (560 - 47)
pao2_calc = (fio2 * 513) - (pco2 / 0.8)
g_real = pao2_calc - pa02
g_id = (edad / 4) + 4
pafi, safi = pa02/fio2, spo2/fio2
rox = (safi / fr) if fr > 0 else 0

# --- 5. RESULTADOS ---

# I. CONSISTENCIA
st.subheader("✅ I. Consistencia Interna")
if 0.8 <= (h_ion / r80) <= 1.2:
    st.success(f"MUESTRA VÁLIDA: H+ calculado ({h_ion:.1f}) es consistente con pH.")
else:
    st.error(f"❌ MUESTRA NO CONFIABLE: H+ {h_ion:.1f} no correlaciona. Revisar pre-analítica.")

# II. ANÁLISIS ÁCIDO-BASE (Módulos Independientes)
st.subheader("⚖️ II. Equilibrio Ácido-Base")
col1, col2 = st.columns(2)

with col1:
    # Módulo Respiratorio
    if pco2 > 32:
        st.error("🛑 ACIDOSIS RESPIRATORIA")
        with st.expander("🔍 Causas VITAMINS", expanded=True):
            st.write("**V:** Vascular (ACV, TEP) | **I:** Sepsis, Neumonía | **T:** Opioides, BZD | **A:** Miastenia, GB | **M:** Metabólico | **S:** Apnea, Obesidad.")
    elif pco2 < 28:
        st.success("🚨 ALCALOSIS RESPIRATORIA")

    # Módulo Metabólico
    if hco3 < 19:
        st.error("🛑 ACIDOSIS METABÓLICA")
        win = (1.5 * hco3) + 8
        st.info(f"Winters (PaCO2 esperada): {win:.1f} ± 2")
    elif hco3 > 24:
        st.success("🚨 ALCALOSIS METABÓLICA")

with col2:
    # Módulo de Brechas (GAP y Delta)
    st.metric("Anión Gap Corregido", f"{ag_c:.1f}", delta="Corte: 12", delta_color="inverse")
    if ag_c > 12:
        with st.expander("🔍 Causas GOLDMARCC", expanded=True):
            st.write("**G:** Glicoles | **O:** Oxiprolina | **L:** Lactato | **D:** D-Lactato | **M:** Metanol | **A:** Aspirina | **R:** Renal | **C:** Cetoacidosis | **C:** Creatinina")
        
        delta_gap = (ag_c - 12) - (24 - hco3)
        if delta_gap > 6: st.success(f"🔍 Delta Gap ({delta_gap:.1f}): ALCALOSIS METABÓLICA ASOCIADA")
        elif delta_gap < -6: st.warning(f"🔍 Delta Gap ({delta_gap:.1f}): ACIDOSIS NO GAP ASOCIADA")

# III. OXIGENACIÓN BOGOTÁ
st.subheader("☁️ III. Oxigenación y Gradiente (2600m)")
o1, o2, o3, o4 = st.columns(4)

def cat_sdra(v):
    if v < 100: return "🔴 SEVERO"
    if v < 200: return "🟠 MODERADO"
    return "🟡 LEVE" if v < 300 else "🟢 NORMAL"

o1.metric("PAFI", f"{pafi:.0f}", cat_sdra(pafi))
o2.metric("SAFI", f"{safi:.0f}", cat_sdra(safi))
o3.metric("ROX Index", f"{rox:.2f}", "Riesgo VNI" if rox < 4.88 else "Estable")
o4.metric("Gradiente A-a", f"{g_real:.1f}", f"Ideal: {g_id:.1f}")

if g_real > (g_id + 10):
    st.error(f"DIAGNÓSTICO: LESIÓN INTRAPULMONAR")
else:
    st.success("DIAGNÓSTICO: PULMÓN SANO / CAUSA EXTRAPULMONAR")

st.caption("Gases 2600 PRO - Bogotá v6.0 Final | Dr. Gonzalo Bernal Ferreira")

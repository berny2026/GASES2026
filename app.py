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
st.set_page_config(page_title="Gases 2600", layout="wide")
st.markdown("<h1 style='text-align: center;'>🫁 Gases Arteriales 2600</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Dr. Gonzalo Bernal Ferreira</h3>", unsafe_allow_html=True)

# --- 3. ENTRADA DE DATOS ---
c1, c2, c3, c4 = st.columns(4)
with c1:
    ph = st.number_input("pH Arterial", 6.80, 7.80, 7.20, 0.01)
    pco2 = st.number_input("PaCO2 (mmHg)", 10.0, 90.0, 40.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 5.0, 50.0, 15.0, 0.1)
with c2:
    na = st.number_input("Sodio (Na)", 110.0, 170.0, 145.0, 0.1)
    cl = st.number_input("Cloro (Cl)", 70.0, 130.0, 95.0, 0.1)
    alb = st.number_input("Albúmina (g/dL)", 1.0, 5.0, 4.0, 0.1)
with c3:
    pa02 = st.number_input("PaO2 (mmHg)", 20.0, 200.0, 55.0, 0.1)
    fio2 = st.number_input("FiO2 (decimal)", 0.21, 1.00, 0.21, 0.01)
    cloro_u = st.number_input("Cloro Urinario", 0, 150, 0)
with c4:
    edad = st.number_input("Edad (años)", 0, 115, 50)
    fr = st.number_input("FR (resp/min)", 5, 60, 28)
    spo2 = st.number_input("SpO2 (%)", 40, 100, 88)

st.divider()

# --- 4. CONSISTENCIA ---
h_ion = 24 * (pco2 / hco3)
st.write(f"**H+ calculado:** {h_ion:.1f}")

# --- 5. TRASTORNOS ---
st.header("Análisis de Trastornos")
ag_c = (na - (cl + hco3)) + (2.5 * (4 - alb))

if ph < 7.4 and hco3 < 18:
    st.error("🛑 ACIDOSIS METABÓLICA DETECTADA")
    win = (1.5 * hco3) + 8
    if pco2 > win + 2: st.error(f"⚠️ PaCO2 {pco2} > {win+2}: ACIDOSIS RESPIRATORIA SOBREAGREGADA")
    
    if ag_c > 12:
        st.error(f"Anión Gap Elevado ({ag_c:.1f})")
        delta_gap = (ag_c - 12) - (24 - hco3)
        if delta_gap > 6: st.success(f"🔍 DELTA GAP ({delta_gap:.1f}): ALCALOSIS METABÓLICA ASOCIADA")
        elif delta_gap < -6: st.warning(f"🔍 DELTA GAP ({delta_gap:.1f}): ACIDOSIS METABÓLICA NO GAP ASOCIADA")
        st.info("Causas (GOLDMARCC): Glicoles, Lactato, Cetoacidosis, Falla Renal.")

# --- 6. OXIGENACIÓN ---
st.header("Oxigenación")
pao2_calc = (fio2 * 513) - (pco2 / 0.8)
g_real = pao2_calc - pa02
g_id = (edad / 4) + 4

col1, col2 = st.columns(2)
col1.metric("Gradiente A-a Real", f"{g_real:.1f}")
col2.metric("Gradiente Ideal", f"{g_id:.1f}")

if g_real > (g_id + 10): st.error("DIAGNÓSTICO: LESIÓN INTRAPULMONAR")
else: st.success("DIAGNÓSTICO: PULMÓN SANO (Causa Extra-pulmonar / Hipoventilación)")

st.caption("Gases 2600 - Dr. Gonzalo Bernal Ferreira")

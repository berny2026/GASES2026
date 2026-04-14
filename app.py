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
with st.expander("📝 INGRESAR DATOS DEL PACIENTE", expanded=True):
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

# --- 4. CÁLCULOS INTERMEDIOS ---
h_ion = 24 * (pco2 / hco3)
ag_c = (na - (cl + hco3)) + (2.5 * (4 - alb))
win = (1.5 * hco3) + 8
delta_gap = (ag_c - 12) - (24 - hco3)

# --- 5. RESULTADOS DETALLADOS ---
st.header("🔬 Análisis Fisiopatológico")

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("H+ Calculado", f"{h_ion:.1f} nEq/L")
    st.caption("Consistencia interna (Equación Henderson)")
with col_b:
    st.metric("Anión Gap Corregido", f"{ag_c:.1f}")
    st.caption(f"Corregido por Albúmina ({alb} g/dL)")
with col_c:
    st.metric("PaCO2 Winters", f"{win:.1f} ± 2")
    st.caption("Compensación respiratoria esperada")

# Diagnósticos de Trastornos
if ph < 7.4 and hco3 < 18:
    st.error("🛑 ACIDOSIS METABÓLICA DETECTADA")
    if pco2 > win + 2: 
        st.error(f"⚠️ PaCO2 Real ({pco2}) > Límite Winters ({win+2:.1f}): ACIDOSIS RESPIRATORIA SOBREAGREGADA")
    
    if ag_c > 12:
        st.warning(f"Anión Gap Elevado: Sugiere GOLDMARCC")
        if delta_gap > 6: 
            st.success(f"🔍 DELTA GAP: {delta_gap:.1f} -> ALCALOSIS METABÓLICA ASOCIADA")
        elif delta_gap < -6:
            st.warning(f"🔍 DELTA GAP: {delta_gap:.1f} -> ACIDOSIS NO GAP ASOCIADA")

# --- 6. OXIGENACIÓN ---
st.header("🫁 Oxigenación y Mecánica")
pao2_calc = (fio2 * 513) - (pco2 / 0.8)
g_real = pao2_calc - pa02
g_id = (edad / 4) + 4
rox = ((spo2/fio2)/fr)

res1, res2, res3, res4 = st.columns(4)
res1.metric("PAFI", f"{(pa02/fio2):.0f}")
res2.metric("SAFI", f"{(spo2/fio2):.0f}")
res3.metric("ROX Index", f"{rox:.2f}")
res4.metric("Gradiente A-a", f"{g_real:.1f}")

st.info(f"Interpretación ROX: {'> 4.88 (Bajo riesgo)' if rox > 4.88 else '< 4.88 (Riesgo de falla de VNI)'}")

if g_real > (g_id + 10):
    st.error(f"DIAGNÓSTICO: LESIÓN INTRAPULMONAR (Gradiente Real {g_real:.1f} > Ideal {g_id:.1f})")
else:
    st.success(f"DIAGNÓSTICO: PULMÓN SANO (Gradiente Real {g_real:.1f} acorde a edad)")

st.caption("Gases 2600 - Dr. Gonzalo Bernal Ferreira | Versión PRO 2.0")

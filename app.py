import streamlit as st
import streamlit.components.v1 as components
import math

# --- 1. GOOGLE ANALYTICS (CON SU ID REAL) ---
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
st.divider()

# --- 3. ENTRADA DE DATOS ---
c1, c2, c3, c4 = st.columns(4)
with c1:
    ph = st.number_input("pH Arterial", 6.80, 7.80, 7.40, 0.01)
    pco2 = st.number_input("PaCO2 (mmHg)", 10.0, 90.0, 30.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 5.0, 50.0, 20.0, 0.1)
with c2:
    na = st.number_input("Sodio (Na)", 110.0, 170.0, 140.0, 0.1)
    cl = st.number_input("Cloro (Cl)", 70.0, 130.0, 105.0, 0.1)
    cloro_u = st.number_input("Cloro Urinario", 0, 150, 0)
with c3:
    pa02 = st.number_input("PaO2 (mmHg)", 20.0, 200.0, 60.0, 0.1)
    fio2 = st.number_input("FiO2 (decimal)", 0.21, 1.00, 0.21, 0.01)
    alb = st.number_input("Albúmina (g/dL)", 1.0, 5.0, 4.0, 0.1)
with c4:
    edad = st.number_input("Edad (años)", 0, 115, 45)
    fr = st.number_input("FR (resp/min)", 5, 60, 20)
    spo2 = st.number_input("SpO2 (%)", 40, 100, 94)

# --- 4. CONSISTENCIA ---
h_ion = 24 * (pco2 / hco3)
r80 = 80 - float(f"{ph:.2f}"[-2:])
div_80 = h_ion / r80 if r80 != 0 else 0
if 0.7 <= div_80 <= 1.2: 
    st.success(f"✅ CONSISTENCIA OK (H+: {h_ion:.1f})")
else: 
    st.error(f"❌ REVISAR MUESTRA")

# --- 5. TRASTORNOS ---
ag_c = (na - (cl + hco3)) + (2.5 * (4 - alb))

if ph < 7.4 and hco3 < 18:
    st.error("🛑 ACIDOSIS METABÓLICA")
    win = (1.5 * hco3) + 8
    st.write(f"**PaCO2 Winters:** {win:.1f} ± 2")
    if ag_c > 12:
        st.error("CAUSA: AG ELEVADO (GOLDMARCC)")
        st.write("G: Glicoles | O: Oxiprolina | L: Lactato | D: D-Lactato | M: Metanol | A: Aspirina | R: Rabdomiólisis | C: Cetoacidosis | C: Creatinina")
    else: st.info("CAUSA: AG NORMAL (Diarrea, ATR)")

if ph > 7.4 and hco3 > 22:
    st.success("🛑 ALCALOSIS METABÓLICA")
    if cloro_u > 0:
        st.info("TIPO: CLORO-SENSIBLE" if cloro_u < 20 else "TIPO: CLORO-RESISTENTE")

# --- 6. OXIGENACIÓN ---
st.divider()
pao2_calc = (fio2 * 513) - (pco2 / 0.8)
g_real = pao2_calc - pa02
g_id = (edad / 4) + 4

if pa02 < 60:
    st.error(f"HIPOXEMIA ({pa02} mmHg)")
    st.write("Causas: 1-PB baja, 2-OVACE, 3-Laringe, 4-Vía aérea, 5-Alvéolo, 6-Intersticio, 7-Vaso (TEP)")

ca, cb, cc = st.columns(3)
ca.metric("PAFI", f"{(pa02/fio2):.1f}")
cb.metric("Gradiente Real", f"{g_real:.1f}")
cc.metric("Gradiente Ideal", f"{g_id:.1f}")

if g_real > (g_id + 10):
    st.error("DIAGNÓSTICO: LESIÓN INTRAPULMONAR")
else:
    st.success("DIAGNÓSTICO: PULMÓN SANO (Extra-pulmonar)")

st.caption("Gases 2600 - Propiedad Dr. Gonzalo Bernal Ferreira")

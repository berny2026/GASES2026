import streamlit as st
import streamlit.components.v1 as components
import math

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

# --- 2. CONFIGURACIÓN ---
st.set_page_config(page_title="Gases 2600", layout="wide")
st.markdown("<h1 style='text-align: center;'>🫁 Gases Arteriales 2600</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Dr. Gonzalo Bernal Ferreira</h3>", unsafe_allow_html=True)
st.divider()

# --- 3. ENTRADA DE DATOS ---
with st.container():
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        ph = st.number_input("pH Arterial", 6.80, 7.80, 7.40, 0.01)
        pco2 = st.number_input("PaCO2 (mmHg)", 10.0, 90.0, 30.0, 0.1)
        hco3 = st.number_input("HCO3 (mEq/L)", 5.0, 50.0, 20.0, 0.1)
    with c2:
        na = st.number_input("Sodio (Na)", 110.0, 170.0, 140.0, 0.1)
        cl = st.number_input("Cloro (Cl)", 70.0, 130.0, 105.0, 0.1)
        alb = st.number_input("Albúmina (g/dL)", 1.0, 5.0, 4.0, 0.1)
    with c3:
        pa02 = st.number_input("PaO2 (mmHg)", 20.0, 200.0, 60.0, 0.1)
        fio2 = st.number_input("FiO2 (decimal)", 0.21, 1.00, 0.21, 0.01)
        cloro_u = st.number_input("Cloro Urinario", 0, 150, 0)
    with c4:
        edad = st.number_input("Edad (años)", 0, 115, 45)
        fr = st.number_input("FR (resp/min)", 5, 60, 20)
        spo2 = st.number_input("SpO2 (%)", 40, 100, 94)

# --- 4. CONSISTENCIA ---
h_ion = 24 * (pco2 / hco3)
r80 = 80 - float(f"{ph:.2f}"[-2:])
div_80 = h_ion / r80 if r80 != 0 else 0
st.header("I. Consistencia Interna")
if 0.7 <= div_80 <= 1.2: 
    st.success(f"✅ MUESTRA CONFIABLE (H+: {h_ion:.1f})")
else: 
    st.error(f"❌ REVISAR MUESTRA (H+ calc: {h_ion:.1f} vs pH)")

# --- 5. TRASTORNOS ---
st.header("II. Trastornos y Compensación")
ag_c = (na - (cl + hco3)) + (2.5 * (4 - alb))

# Acidosis Metabólica
if ph < 7.4 and hco3 < 18:
    st.error("🛑 ACIDOSIS METABÓLICA")
    win = (1.5 * hco3) + 8
    st.info(f"Winters: PaCO2 esperada = {win:.1f} ± 2")
    if pco2 > win + 2: st.error("➡️ INTERPRETACIÓN: Acidosis Respiratoria Sobreagregada")
    elif pco2 < win - 2: st.warning("➡️ INTERPRETACIÓN: Alcalosis Respiratoria Asociada")
    
    if ag_c > 12:
        st.error(f"CAUSA: ANION GAP ELEVADO ({ag_c:.1f}) - GOLDMARCC")
        st.write("G: Glicoles | O: Oxiprolina | L: Lactato | D: D-Lactato | M: Metanol | A: Aspirina | R: Rabdomiólisis | C: Cetoacidosis | C: Creatinina")
    else: st.info("CAUSA: ANION GAP NORMAL (Hipercloremia, Diarrea, ATR)")

# Acidosis Respiratoria
if ph < 7.4 and pco2 > 32:
    st.warning("🛑 ACIDOSIS RESPIRATORIA")
    h_esp_aguda = 24 + ((pco2 - 30) * 0.1)
    if abs(hco3 - h_esp_aguda) < 2: st.write("➡️ ESTADO: AGUDA (Compensación renal incipiente)")
    else: st.write("➡️ ESTADO: CRÓNICA (Compensación renal presente)")

# Alcalosis Metabólica
if ph > 7.4 and hco3 > 22:
    st.success("🛑 ALCALOSIS METABÓLICA")
    p_esp = (0.7 * hco3) + 20
    st.write(f"PaCO2 esperada: {p_esp:.1f} ± 5")
    if cloro_u > 0:
        st.info("TIPO: CLORO-SENSIBLE" if cloro_u < 20 else "TIPO: CLORO-RESISTENTE")

# --- 6. OXIGENACIÓN ---
st.divider()
st.header("III. Oxigenación (Bogotá 2600m)")
pao2_calc = (fio2 * 513) - (pco2 / 0.8)
g_real = pao2_calc - pa02
g_id = (edad / 4) + 4

ca, cb, cc, cd = st.columns(4)
ca.metric("PAFI", f"{(pa02/fio2):.1f}")
cb.metric("SAFI", f"{(spo2/fio2):.1f}")
cc.metric("ROX Index", f"{((spo2/fio2)/fr):.2f}")
cd.metric("Gradiente A-a Real", f"{g_real:.1f}")

if pa02 < 60:
    st.error(f"HIPOXEMIA: 1-PB baja, 2-OVACE, 3-Laringe, 4-Vía aérea, 5-Alvéolo, 6-Intersticio, 7-Vaso (TEP)")

if g_real > (g_id + 10):
    st.error(f"DIAGNÓSTICO: LESIÓN INTRAPULMONAR (Real {g_real:.1f} > Ideal {g_id:.1f})")
else:
    st.success(f"DIAGNÓSTICO: PULMÓN SANO (Real {g_real:.1f} acorde a Ideal {g_id:.1f})")

st.caption("Gases 2600 - Dr. Gonzalo Bernal Ferreira")

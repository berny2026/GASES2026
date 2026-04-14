import streamlit as st
import streamlit.components.v1 as components
import math

# --- 1. CONFIGURACIÓN Y ANALYTICS ---
st.set_page_config(page_title="Gases 2600 - Dr. Bernal", layout="wide")
components.html("<script async src='https://www.googletagmanager.com/gtag/js?id=G-GFRWYE6S9W'></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-GFRWYE6S9W');</script>", height=0)

st.markdown("<h1 style='text-align: center;'>🫁 App Gases Arteriales 2600</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>DR. GONZALO BERNAL FERREIRA - MEDICO FAMILIAR</h2>", unsafe_allow_html=True)
st.divider()

# --- 2. ENTRADA DE DATOS (Módulo Completo) ---
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
    fio2 = st.number_input("FiO2 (ej. 0.21)", 0.21, 1.00, 0.21, 0.01)
    alb = st.number_input("Albúmina (g/dL)", 1.0, 5.0, 4.0, 0.1)
with c4:
    edad = st.number_input("Edad (años)", 0, 115, 45)
    fr = st.number_input("FR (resp/min)", 5, 60, 20)
    spo2 = st.number_input("SpO2 (%)", 40, 100, 94)

# --- 3. CONSISTENCIA INTERNA ---
st.header("I. Evaluación de la Consistencia Interna")
h_ion = 24 * (pco2 / hco3)
if ph < 7.2 or ph > 7.4:
    ph_hh = 6.1 + math.log10(hco3 / (pco2 * 0.03))
    dif = abs(ph_hh - ph)
    if dif <= 0.05: st.success(f"HAY CONSISTENCIA INTERNA (pH HH: {ph_hh:.3f})")
    else: st.error(f"NO HAY CONSISTENCIA: pH medido {ph} vs calculado {ph_hh:.3f}")
else:
    r80 = 80 - float(f"{ph:.2f}"[-2:])
    div_80 = h_ion / r80 if r80 != 0 else 0
    if 0.7 <= div_80 <= 1.2: st.success(f"HAY CONSISTENCIA INTERNA (H+: {h_ion:.1f})")
    else: st.error(f"NO HAY CONSISTENCIA (Relación H+/R80: {div_80:.2f})")

# --- 4. TRASTORNOS ---
st.header("II. Análisis de Trastornos y Compensaciones")
ag_c = (na - (cl + hco3)) + (2.5 * (4 - alb))

# ACIDOSIS METABÓLICA
if ph < 7.4 and hco3 < 18:
    st.subheader("🛑 ACIDOSIS METABÓLICA")
    win = (1.5 * hco3) + 8
    st.write(f"**PaCO2 esperada (Winters):** {win:.1f} ± 2")
    if pco2 > win + 2: st.error("INTERPRETACIÓN: Acidosis Respiratoria Sobreagregada (No compensa)")
    elif pco2 < win - 2: st.success("INTERPRETACIÓN: Alcalosis Respiratoria Asociada")
    else: st.info("INTERPRETACIÓN: Acidosis Metabólica Compensada")
    
    st.write(f"**Anión GAP Corregido:** {ag_c:.1f}")
    if ag_c > 12:
        st.error("CAUSA: ANION GAP ELEVADO - GOLDMARCC:")
        st.markdown("G: Glicoles | O: Oxiprolina | L: Lactato (>4) | D: D-Lactato | M: Metanol | A: Aspirina | R: Rabdomiólisis | C: Cetoacidosis | C: Creatinina.")
        dg = (ag_c - 10) - (20 - hco3)
        st.info(f"Delta Gap: {dg:.1f}")
    else: st.info("CAUSA: AG NORMAL (Hipercloremia, Diarrea, ATR).")

# ACIDOSIS RESPIRATORIA
if ph < 7.4 and pco2 > 32:
    st.subheader("🛑 ACIDOSIS RESPIRATORIA")
    dp = pco2 - 30
    h_esp = 20 + (1 * (dp/10))
    st.warning("ESTADO: AGUDA" if hco3 <= h_esp + 1 else "ESTADO: CRÓNICA")
    st.markdown("**CAUSAS (VITAMINS):** V: Vascular, I: Infección, T: Trauma, A: Autoinmune, M: Metabólico, I: Iatrogenia, N: Neoplasia, S: SNC.")

# ALCALOSIS RESPIRATORIA
if ph > 7.4 and pco2 < 28:
    st.subheader("🛑 ALCALOSIS RESPIRATORIA")
    st.markdown("**CAUSAS (VINDICATE):** Vascular, Inflamación, Neoplasia, Degenerativo, Idiopático, Congénito, Autoinmune, Trauma, Endocrino.")

# ALCALOSIS METABÓLICA
if ph > 7.4 and hco3 > 22:
    st.subheader("🛑 ALCALOSIS METABÓLICA")
    p_esp = (0.7 * hco3) + 20
    st.write(f"**PaCO2 esperada:** {p_esp:.1f} ± 5")
    if cloro_u > 0:
        if cloro_u < 20: st.info("TIPO: CLORO-SENSIBLE (Vómitos, drenaje NG, diuréticos)")
        else: st.info("TIPO: CLORO-RESISTENTE (Cushing, Bartter, Hipopotasemia)")

# --- 5. OXIGENACIÓN ---
st.divider()
st.header("III. Evaluación de la Oxigenación (Bogotá)")

pao2_calc = (fio2 * 513) - (pco2 / 0.8)
gradiente_real = pao2_calc - pa02
gradiente_ideal = (edad / 4) + 4

if pa02 < 60:
    st.error(f"HIPOXEMIA (PaO2: {pa02} mmHg)")
    st.markdown("**CAUSAS DE HIPOXEMIA:** 1. PB baja | 2. OVACE | 3. Laringe | 4. Vía Aérea | 5. Alvéolo | 6. Intersticio | 7. Vaso (TEP).")

ca, cb, cc = st.columns(3)
ca.metric("PAFI", f"{(pa02/fio2):.1f}")
cb.metric("Diferencia A-a Real", f"{gradiente_real:.1f}")
cc.metric("Diferencia A-a Ideal", f"{gradiente_ideal:.1f}")

st.subheader("Interpretación de la Diferencia Alveolo-Arterial:")
if gradiente_real > (gradiente_ideal + 10):
    st.error(f"La Diferencia Real ({gradiente_real:.1f}) supera la Ideal ({gradiente_ideal:.1f}).")
    st.error("DIAGNÓSTICO: LESIÓN INTRAPULMONAR (Pulmón Enfermo)")
else:
    st.success(f"La Diferencia Real ({gradiente_real:.1f}) es normal respecto a la Ideal ({gradiente_ideal:.1f}).")
    st.success("DIAGNÓSTICO: PULMÓN SANO (Causa Extra-pulmonar)")

st.subheader("Interpretación Clínica Cruzada:")
if pco2 > 32:
    if gradiente_real > (gradiente_ideal + 10): st.info("Acidosis Resp + Pulmón Enfermo: Asma, Neumonía o EPOC.")
    else: st.info("Acidosis Resp + Pulmón Sano: Depresión SNC o Neuromuscular.")
elif pco2 < 28:
    if gradiente_real > (gradiente_ideal + 10): st.info("Alcalosis Resp + Pulmón Enfermo: TEP, Sepsis, Edema Pulmonar.")
    else: st.info("Alcalosis Resp + Pulmón Sano: Dolor, Ansiedad, Embarazo.")

st.caption("Dr. Gonzalo Bernal Ferreira - Gases 2600")

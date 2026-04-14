import streamlit as st
import streamlit.components.v1 as components
import math

# --- 1. CONFIGURACIÓN Y ANALYTICS ---
st.set_page_config(page_title="Gases 2600 - Dr. Bernal", layout="wide")
components.html("<script async src='https://www.googletagmanager.com/gtag/js?id=G-GFRWYE6S9W'></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-GFRWYE6S9W');</script>", height=0)

st.markdown("<h1 style='text-align: center;'>🫁 App Gases Arteriales 2600</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>DR. GONZALO BERNAL FERREIRA</h2>", unsafe_allow_html=True)
st.divider()

# --- 2. ENTRADA DE DATOS ---
c1, c2, c3 = st.columns(3)
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
    fio2 = st.number_input("FiO2 (decimal ej. 0.21)", 0.21, 1.00, 0.21, 0.01)
    edad = st.number_input("Edad (años)", 0, 115, 45)
    fr = st.number_input("FR (resp/min)", 5, 60, 20)
    spo2 = st.number_input("SpO2 (%)", 40, 100, 94)

# --- 3. CONSISTENCIA INTERNA ---
st.header("I. Consistencia Interna")
h_ion = 24 * (pco2 / hco3)
if ph < 7.2 or ph > 7.4:
    ph_hh = 6.1 + math.log10(hco3 / (pco2 * 0.03))
    dif = abs(ph_hh - ph)
    if dif <= 0.05: st.success(f"CONSISTENTE (pH HH: {ph_hh:.3f})")
    else: st.error("NO CONSISTENTE: Revisar muestra.")
else:
    r80 = 80 - float(f"{ph:.2f}"[-2:])
    div_80 = h_ion / r80 if r80 != 0 else 0
    if 0.7 <= div_80 <= 1.2: st.success("CONSISTENTE (Regla 80)")
    else: st.error("NO CONSISTENTE")

# --- 4. TRASTORNOS ---
st.header("II. Análisis de Trastornos")
ag_c = (na - (cl + hco3)) + (2.5 * (4 - alb))

# ACIDOSIS METABÓLICA
if ph < 7.4 and hco3 < 18:
    st.subheader("🛑 ACIDOSIS METABÓLICA")
    win = (1.5 * hco3) + 8
    st.write(f"**PaCO2 esperada (Winters):** {win:.1f} ± 2")
    if pco2 > win + 2: st.error("INTERPRETACIÓN: Acidosis Respiratoria Sobreagregada (No compensa)")
    elif pco2 < win - 2: st.success("INTERPRETACIÓN: Alcalosis Respiratoria Asociada")
    else: st.info("INTERPRETACIÓN: Acidosis Metabólica Compensada")
    
    if ag_c > 12:
        st.error(f"ANION GAP ELEVADO ({ag_c:.1f}) - GOLDMARCC:")
        st.markdown("G: Glicoles | O: Oxiprolina | L: Lactato (>4) | D: D-Lactato | M: Metanol | A: Aspirina | R: Rabdomiólisis | C: Cetoacidosis | C: Creatinina (IR).")
        dg = (ag_c - 10) - (20 - hco3)
        st.info(f"Delta Gap: {dg:.1f}")
    else:
        st.info("ANION GAP NORMAL: Hipercloremia, Diarrea, ATR.")

# ACIDOSIS RESPIRATORIA
if ph < 7.4 and pco2 > 32:
    st.subheader("🛑 ACIDOSIS RESPIRATORIA")
    dp = pco2 - 30
    h_esp = 20 + (1 * (dp/10))
    st.warning("ESTADO: AGUDA" if hco3 <= h_esp + 1 else "ESTADO: CRÓNICA")
    st.markdown("**CAUSAS (VITAMINS):** SNC, SNP (Guillain Barré), Placa (Miastenia), Muscular (Fatiga), Alvéolo (EPOC), Tórax.")

# ALCALOSIS RESPIRATORIA
if ph > 7.4 and pco2 < 28:
    st.subheader("🛑 ALCALOSIS RESPIRATORIA")
    st.markdown("**CAUSAS (VINDICATE):** Vascular, Infección, Neoplasia, Drogas, Idiopático, Autoinmune, Trauma.")

# --- 5. OXIGENACIÓN (GRADIENTE Y COMPARACIÓN) ---
st.divider()
st.header("III. Evaluación de la Oxigenación")

# Cálculo PAO2 y Diferencia (Gradiente Real)
pao2_calculada = (fio2 * 513) - (pco2 / 0.8)
gradiente_real = pao2_calculada - pa02
gradiente_ideal = (edad / 4) + 4

if pa02 < 60:
    st.error(f"HIPOXEMIA (PaO2: {pa02} mmHg)")
    st.markdown("**CAUSAS:** 1. PB baja | 2. OVACE | 3. Laringe | 4. Vía Aérea | 5. Alvéolo | 6. Intersticio | 7. Vaso (TEP).")

c_a, c_b, c_c = st.columns(3)
c_a.metric("PAFI", f"{(pa02/fio2):.1f}")
c_b.metric("Gradiente Real", f"{gradiente_real:.1f}")
c_c.metric("Gradiente Ideal", f"{gradiente_ideal:.1f}")

# COMPARACIÓN LÓGICA
st.subheader("Resultado de la Diferencia Alveolo-Arterial:")
if gradiente_real > (gradiente_ideal + 10):
    st.error(f"Diferencia de {gradiente_real:.1f} es SUPERIOR a la ideal de {gradiente_ideal:.1f}")
    st.error("DIAGNÓSTICO: LESIÓN INTRAPULMONAR (Pulmón enfermo)")
else:
    st.success(f"Diferencia de {gradiente_real:.1f} es acorde a la ideal de {gradiente_ideal:.1f}")
    st.success("DIAGNÓSTICO: PULMÓN SANO (Causa extra-pulmonar)")

# INTERPRETACIÓN CRUZADA FINAL
st.subheader("Interpretación Clínica Cruzada:")
if pco2 > 32: # Acidosis Resp
    if gradiente_real > (gradiente_ideal + 10): st.info("Acidosis Resp + Gradiente Alto: Neumonía, EPOC, Asma.")
    else: st.info("Acidosis Resp + Gradiente Normal: Depresión SNC, Guillain-Barré.")
elif pco2 < 28: # Alcalosis Resp
    if gradiente_real > (gradiente_ideal + 10): st.info("Alcalosis Resp + Gradiente Alto: TEP, Sepsis, Edema Pulmonar.")
    else: st.info("Alcalosis Resp + Gradiente Normal: Ansiedad, Dolor, Embarazo.")

st.caption("Dr. Gonzalo Bernal Ferreira - Gases 2600")

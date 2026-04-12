import streamlit as st
import streamlit.components.v1 as components
import math

# 2. IDENTIFICADOR
components.html(
    """
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-GFRWYE6S9W"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-GFRWYE6S9W');
    </script>
    """,
    height=0,
)

# 1. IDENTIFICACIÓN
st.set_page_config(page_title="Gases 2600 - Dr. Bernal", layout="wide")
st.markdown("<h1 style='text-align: center;'>🫁 App Gases Arteriales</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>GONZALO BERNAL FERREIRA. MEDICO FAMILIAR</h2>", unsafe_allow_html=True)
st.divider()

# ENTRADA DE DATOS (Puntos 7, 11 y 13)
col1, col2, col3 = st.columns(3)
with col1:
    ph = st.number_input("pH Arterial", 6.80, 7.80, 7.40, 0.01)
    pco2 = st.number_input("PaCO2 (mmHg)", 10.0, 90.0, 30.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 5.0, 50.0, 20.0, 0.1)
with col2:
    na = st.number_input("Sodio (Na)", 110.0, 170.0, 140.0, 0.1)
    cl = st.number_input("Cloro (Cl)", 70.0, 130.0, 105.0, 0.1)
    alb = st.number_input("Albúmina (g/dL)", 1.0, 5.0, 4.0, 0.1)
with col3:
    pa02 = st.number_input("PaO2 (mmHg)", 20.0, 200.0, 60.0, 0.1)
    fio2 = st.number_input("FiO2 (0.21 - 1.0)", 0.21, 1.00, 0.21, 0.01)
    edad = st.number_input("Edad (años)", 0, 115, 45)
    fr = st.number_input("Frecuencia Respiratoria (FR)", 5, 60, 20)
    spo2 = st.number_input("SpO2 (%)", 40, 100, 94)

cl_u = st.sidebar.number_input("Cloro Urinario (mEq/L)", 0, 150, 0)

# --- PASO 1: CONSISTENCIA (Puntos 4 y 5) ---
st.header("Paso 1: Consistencia Interna")
if ph < 7.2 or ph > 7.4:
    ph_hh = 6.1 + math.log10(hco3 / (pco2 * 0.03))
    dif = abs(ph_hh - ph)
    st.write(f"Diferencia HH: {dif:.3f}")
    if dif <= 0.05: st.success("HAY CONSISTENCIA INTERNA")
    else: st.error("NO HAY CONSISTENCIA INTERNA")
else:
    h_ion = 24 * (pco2 / hco3)
    regla_80 = 80 - float(f"{ph:.2f}"[-2:])
    res = h_ion / regla_80 if regla_80 != 0 else 0
    if 0.7 <= res <= 1.2: st.success(f"HAY CONSISTENCIA (H+:{h_ion:.1f} / R80:{regla_80})")
    else: st.error("NO HAY CONSISTENCIA INTERNA")

# --- PASO 2: ESTADO (Puntos 3 y 6) ---
st.header("Paso 2: Estado Ácido-Base (Bogotá)")
if ph < 7.4: st.error("ACIDOSIS (pH < 7.4)")
elif ph > 7.4: st.success("ALCALOSIS (pH > 7.4)")
else: st.info("NEUTRO (pH 7.4)")

# --- PASO 3: TRASTORNOS (Puntos 8-13) ---
st.header("Paso 3: Análisis del Trastorno")
ag_c = (na - (cl + hco3)) + (2.5 * (4 - alb))

# ACIDOSIS RESPIRATORIA
if ph < 7.4 and pco2 > 32:
    st.subheader("ACIDOSIS RESPIRATORIA")
    dif_p = pco2 - 30
    h_ag = 20 + (1 * (dif_p/10))
    h_cr = 20 + (4 * (dif_p/10))
    if hco3 <= h_ag + 1: st.warning("AGUDA")
    elif hco3 >= h_cr - 1: st.warning("CRÓNICA")
    else: st.warning("CRÓNICA AGUDIZADA")
    with st.expander("Ver Causas (VITAMINS, SNP, PLACA, MUSCULAR, ALVEOLO, TORAX)"):
        st.write("V: Vascular, I: Infección, T: Trauma, A: Autoinmune, M: Metabólica, I: Intoxicación, N: Neoplasia, S: Psiquiátrica. SNP: Guillain Barre. Placa: Miastenia. Muscular: Fatiga por hipoxemia.")

# ACIDOSIS METABÓLICA
if ph < 7.4 and hco3 < 18:
    st.subheader("ACIDOSIS METABÓLICA")
    winter = (1.5 * hco3) + 8
    st.write(f"PaCO2 esperada: {winter:.1f} +/- 2")
    if pco2 > winter + 2: st.warning("Acidosis respiratoria sobreagregada")
    elif pco2 < winter - 2: st.warning("Alcalosis respiratoria")
    
    st.write(f"Anión GAP Corregido: {ag_c:.1f}")
    if ag_c > 12:
        st.error("AG ELEVADO (GOLDMARCC)")
        delta = (ag_c - 10) - (20 - hco3)
        if -5 <= delta <= 5: st.info("PURA")
        elif delta > 5: st.info("Alcalosis Metabólica Sobreagregada")
        else: st.info("Acidosis Metabólica Hiperclorémica")
    else: st.info("AG NORMAL: Hipercloremia, Diarrea, ATR.")

# ALCALOSIS RESPIRATORIA
if ph > 7.4 and pco2 < 28:
    st.subheader("ALCALOSIS RESPIRATORIA")
    dif_p = 30 - pco2
    if hco3 <= 20 - (2*(dif_p/10)): st.warning("AGUDA")
    elif hco3 <= 20 - (4*(dif_p/10)): st.warning("CRÓNICA")
    with st.expander("Ver Causas (VINDICATE)"):
        st.write("V: Vascular, I: Inflamación, N: Neoplasia, D: Drogas, I: Idiopático, C: Congénito, A: Autoinmune, T: Traumático, E: Endocrino.")

# ALCALOSIS METABÓLICA
if ph > 7.4 and hco3 > 22:
    st.subheader("ALCALOSIS METABÓLICA")
    p_esp = 0.7 * hco3 + 20
    st.write(f"PaCO2 esperada: {p_esp:.1f} +/- 5")
    if cl_u > 0:
        if cl_u < 20: st.info("CLORO-SENSIBLE (Vómitos, Diuréticos)")
        else: st.info("CLORO-RESISTENTE (Cushing, Bartter)")

# --- PASO 4: OXIGENACIÓN (Punto 13) ---
st.divider()
st.header("Paso 4: Oxigenación (FR y SpO2)")
pafi = pa02 / fio2
safi = spo2 / fio2
rox = (spo2 / fio2) / fr
grad_r = ((fio2 * 513) - (pco2 / 0.8)) - pa02
grad_i = (edad / 4) + 4

# Interpretación según Punto 13
st.subheader(f"PaO2: {pa02} mmHg")
if pa02 < 60:
    if pa02 >= 40: st.warning("Hipoxemia MODERADA")
    else: st.error("Hipoxemia SEVERA")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("PAFI", f"{pafi:.1f}")
    if pafi < 300: st.write("Alterada")
with c2:
    st.metric("SAFI", f"{safi:.1f}")
    if safi < 315: st.write("Alterada")
with c3:
    st.metric("ROX Index", f"{rox:.2f}")
    if rox < 3.85: st.error("Alto riesgo de falla")
    elif rox < 4.88: st.warning("Riesgo intermedio")

st.write(f"D(A-a)O2 Real: {grad_r:.1f} | Ideal: {grad_ideal:.1f}")
if grad_r > grad_i + 10: st.error("LESIÓN INTRAPULMONAR")
else: st.success("PULMÓN SANO")

st.caption("Propiedad: Dr. Gonzalo Bernal Ferreira - Gases 2600")

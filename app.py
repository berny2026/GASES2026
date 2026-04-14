import streamlit as st
import streamlit.components.v1 as components
import math

# --- 1. ANALYTICS ---
components.html("<script async src='https://www.googletagmanager.com/gtag/js?id=G-GFRWYE6S9W'></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-GFRWYE6S9W');</script>", height=0)

# --- 2. CONFIGURACIÓN ---
st.set_page_config(page_title="Gases 2600 - Dr. Bernal", layout="wide")
st.markdown("<h1 style='text-align: center;'>🫁 Gases Arteriales 2600</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>GONZALO BERNAL FERREIRA. MEDICO FAMILIAR</h2>", unsafe_allow_html=True)
st.divider()

# --- 3. ENTRADA DE DATOS ---
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
    fio2 = st.number_input("FiO2 (ej. 0.21)", 0.21, 1.00, 0.21, 0.01)
    edad = st.number_input("Edad (años)", 0, 115, 45)
    fr = st.number_input("FR (resp/min)", 5, 60, 20)
    spo2 = st.number_input("SpO2 (%)", 40, 100, 94)

cloro_u = st.sidebar.number_input("Cloro Urinario (mEq/L)", 0, 150, 0)

# --- I. CONSISTENCIA INTERNA ---
st.header("I. Evaluación de la Consistencia Interna")
h_ion = 24 * (pco2 / hco3)
if ph < 7.2 or ph > 7.4:
    ph_hh = 6.1 + math.log10(hco3 / (pco2 * 0.03))
    dif = abs(ph_hh - ph)
    st.write(f"pH Calculado (HH): {ph_hh:.3f} | Diferencia: {dif:.3f}")
    if dif <= 0.05: st.success("HAY CONSISTENCIA INTERNA")
    else: st.error("NO HAY CONSISTENCIA: Repetir por posible contaminación.")
else:
    r80 = 80 - float(f"{ph:.2f}"[-2:])
    div_80 = h_ion / r80 if r80 != 0 else 0
    st.write(f"H+: {h_ion:.1f} | R80: {r80}")
    if 0.7 <= div_80 <= 1.2: st.success("HAY CONSISTENCIA INTERNA")
    else: st.error("NO HAY CONSISTENCIA")

# --- II. ESTADO PH ---
st.header("II. Estado Ácido-Base")
if ph < 7.4: st.error("ACIDOSIS")
elif ph > 7.4: st.success("ALCALOSIS")
else: st.info("NEUTRO")

# --- III. TRASTORNOS ---
st.header("III. Trastornos y Compensaciones")
ag_c = (na - (cl + hco3)) + (2.5 * (4 - alb))

# Acidosis Respiratoria
if ph < 7.4 and pco2 > 32:
    st.subheader("🛑 ACIDOSIS RESPIRATORIA")
    dp = pco2 - 30
    h_esp = 20 + (dp/10)
    if hco3 <= h_esp + 1: st.warning("ESTADO: AGUDA")
    else: st.warning("ESTADO: CRÓNICA")
    st.markdown("**Causas:** SNC (VITAMINS), SNP (Guillain Barré), Placa (Miastenia), Muscular (Fatiga), Alvéolo (EPOC/SDRA), Tórax.")

# Acidosis Metabólica
if ph < 7.4 and hco3 < 18:
    st.subheader("🛑 ACIDOSIS METABÓLICA")
    win = (1.5 * hco3) + 8
    st.write(f"PaCO2 esperada (Winters): {win:.1f} +/- 2")
    if pco2 > win + 2: st.warning("Acidosis respiratoria sobreagregada")
    elif pco2 < win - 2: st.warning("Alcalosis respiratoria asociada")
    
    st.write(f"Anión GAP Corregido: {ag_c:.1f}")
    if ag_c > 12:
        st.error("GOLDMARCC: Glicoles, Oxiprolina, Lactato, D-Lactato, Metanol, Aspirina, Rabdomiólisis, Cetoacidosis, Creatinina.")
        dg = (ag_c - 10) - (20 - hco3)
        if -5 <= dg <= 5: st.info(f"Delta Gap {dg:.1f}: Pura")
        elif dg > 5: st.info(f"Delta Gap {dg:.1f}: Alcalosis Met. Sobreagregada")
        else: st.info(f"Delta Gap {dg:.1f}: Acidosis Met. Hiperclorémica")

# Alcalosis Respiratoria
if ph > 7.4 and pco2 < 28:
    st.subheader("🛑 ALCALOSIS RESPIRATORIA")
    st.markdown("**Causas (VINDICATE):** Vascular, Infección, Neoplasia, Drogas, Idiopático, Congénito, Autoinmune, Trauma, Endocrino.")

# Alcalosis Metabólica
if ph > 7.4 and hco3 > 22:
    st.subheader("🛑 ALCALOSIS METABÓLICA")
    p_esp = (0.7 * hco3) + 20
    st.write(f"PaCO2 esperada: {p_esp:.1f} +/- 5")
    if cloro_u > 0:
        if cloro_u < 20: st.info("CLORO-SENSIBLE: Vómitos, drenaje NG, diuréticos.")
        else: st.info("CLORO-RESISTENTE: Cushing, Bartter, Hipopotasemia.")

# --- IV. OXIGENACIÓN ---
st.divider()
st.header("IV. Evaluación de la Oxigenación")

pao2_calc = (fio2 * 513) - (pco2 / 0.8)
g_real = pao2_calc - pa02
g_id = (edad / 4) + 4

if pa02 < 60:
    st.error(f"HIPOXEMIA (PaO2: {pa02} mmHg)")
    st.markdown("**Causas:** 1. PB baja, 2. OVACE, 3. Laringe, 4. Tráquea/Bronquios, 5. Alvéolo (Pus/Sangre/Agua), 6. Intersticio, 7. Vaso (TEP).")

ca, cb, cc = st.columns(3)
ca.metric("PAFI", f"{(pa02/fio2):.1f}")
cb.metric("SAFI", f"{(spo2/fio2):.1f}")
cc.metric("ROX Index", f"{((spo2/fio2)/fr):.2f}")

st.write(f"Gradiente A-a Real: {g_real:.1f} | Ideal: {g_id:.1f}")
es_grad_elevado = g_real > (g_id + 10)
if es_grad_elevado: st.error("Diferencia Elevada: LESIÓN INTRAPULMONAR")
else: st.success("Diferencia Normal: PULMÓN SANO (Extra-pulmonar)")

st.subheader("Interpretación por Gradiente:")
if ph < 7.4 and pco2 > 32:
    if not es_grad_elevado: st.info("Interpretación: Depresión SNC o Enfermedad Neuromuscular.")
    else: st.info("Interpretación: Asma, Neumonía o EPOC.")
elif ph > 7.4 and pco2 < 28:
    if not es_grad_elevado: st.info("Interpretación: Dolor, ansiedad, AVC, embarazo.")
    else: st.info("Interpretación: Neumonía, Edema pulmonar, TEP, Sepsis.")

st.caption("Propiedad: Dr. Gonzalo Bernal Ferreira - Gases 2600")

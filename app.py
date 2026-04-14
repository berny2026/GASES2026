import streamlit as st
import streamlit.components.v1 as components
import math

# --- 1. IDENTIFICADOR (Google Analytics) ---
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

# --- 2. CONFIGURACIÓN Y NOMBRE ---
st.set_page_config(page_title="Gases Arteriales 2600 - Dr. Bernal", layout="wide")
st.markdown("<h1 style='text-align: center;'>🫁 App Gases Arteriales</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>NOMBRE. GONZALO BERNAL FERREIRA. MEDICO FAMILIAR</h2>", unsafe_allow_html=True)
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

cloro_u = st.sidebar.number_input("Cloro Urinario (Opcional)", 0, 150, 0)

# --- 4. PASO 1: CONSISTENCIA INTERNA ---
st.header("I. Consistencia Interna")
if ph < 7.2 or ph > 7.4:
    ph_hh = 6.1 + math.log10(hco3 / (pco2 * 0.03))
    dif = abs(ph_hh - ph)
    st.write(f"pH calculado (HH): {ph_hh:.3f} | Diferencia: {dif:.3f}")
    if dif <= 0.05: st.success("HAY CONSISTENCIA INTERNA")
    else: st.error("NO HAY CONSISTENCIA INTERNA (Posible contaminación)")
else:
    h_ion = 24 * (pco2 / hco3)
    r80 = 80 - float(f"{ph:.2f}"[-2:])
    div_80 = h_ion / r80 if r80 != 0 else 0
    st.write(f"H+: {h_ion:.1f} | R80: {r80} | División: {div_80:.2f}")
    if 0.7 <= div_80 <= 1.2: st.success("HAY CONSISTENCIA INTERNA")
    else: st.error("NO HAY CONSISTENCIA INTERNA")

# --- 5. PASO 2: ESTADO pH ---
st.header("II. Estado Ácido-Base (Bogotá)")
if ph < 7.4: st.error("ACIDOSIS (pH < 7.4)")
elif ph > 7.4: st.success("ALCALOSIS (pH > 7.4)")
else: st.info("NEUTRO (pH 7.4)")

# --- 6. PASO 3: TRASTORNOS Y COMPENSACIONES ---
st.header("III. Análisis del Trastorno")
ag_c = (na - (cl + hco3)) + (2.5 * (4 - alb))

# --- ACIDOSIS RESPIRATORIA ---
if ph < 7.4 and pco2 > 32:
    st.subheader("🛑 ACIDOSIS RESPIRATORIA")
    dif_p = pco2 - 30
    h_ag = 20 + (1 * (dif_p/10))
    h_cr = 20 + (4 * (dif_p/10))
    if hco3 <= h_ag + 1: st.warning("ESTADO: AGUDA")
    elif hco3 >= h_cr - 1: st.warning("ESTADO: CRÓNICA")
    else: st.warning("ESTADO: CRÓNICA AGUDIZADA")
    
    st.markdown("**Causas (VITAMINS / SNP / PLACA / MUSCULAR / ALVEOLO / TORAX):**")
    st.write("1. SNC: V: Vasculares, I: Infecciones, T: Trauma, A: Autoinmune, M: Metabólica, I: Intoxicación, N: Neoplasia, S: Psiquiátrica.")
    st.write("2. SNP: Guillain barre, VIH, neuropatia periférica, trauma raquimedular.")
    st.write("3. PLACA: Miastenia gravis, Eaton Lambert, botulismo, organofosforados.")
    st.write("4. MUSCULAR: Fatiga por hipoxemia, miopatías.")
    st.write("5. ALVEOLO: EPOC, Edema Pulmonar, SDRA.")
    st.write("6. TORAX: Tórax inestable, cifoescoliosis, fracturas.")

# --- ACIDOSIS METABÓLICA ---
if ph < 7.4 and hco3 < 18:
    st.subheader("🛑 ACIDOSIS METABÓLICA")
    win = (1.5 * hco3) + 8
    st.write(f"PaCO2 esperada (Winters): {win:.1f} +/- 2")
    if pco2 > win + 2: st.warning("Trastorno: Acidosis respiratoria sobreagregada")
    elif pco2 < win - 2: st.warning("Trastorno: Alcalosis respiratoria asociada")
    
    st.write(f"Anión GAP Corregido: {ag_c:.1f}")
    if ag_c > 12:
        st.error("CAUSA: ANION GAP ELEVADO - GOLDMARCC:")
        st.write("- **G**: Glicoles, **O**: Oxiprolina, **L**: Lactato (>4), **D**: D-Lactato, **M**: Metanol, **A**: Aspirina, **R**: Rabdomiólisis, **C**: Cetoacidosis, **C**: Creatinina (IR).")
        dg = (ag_c - 10) - (20 - hco3)
        if -5 <= dg <= 5: st.info(f"Delta Gap {dg:.1f}: Acidosis Metabólica Pura")
        elif dg > 5: st.info(f"Delta Gap {dg:.1f}: Alcalosis Metabólica Sobreagregada")
        else: st.info(f"Delta Gap {dg:.1f}: Acidosis Metabólica Hiperclorémica")
    else: st.info("AG NORMAL/BAJO: Hipercloremia, Diarrea, ATR, Laxantes, etc.")

# --- ALCALOSIS RESPIRATORIA ---
if ph > 7.4 and pco2 < 28:
    st.subheader("🛑 ALCALOSIS RESPIRATORIA")
    dif_p = 30 - pco2
    ratio = (20 - hco3) / (dif_p / 10) if dif_p != 0 else 0
    if 1.9 <= ratio <= 2.1: st.warning("ESTADO: AGUDA")
    elif ratio < 2: st.warning("Alcalosis metabólica adicional")
    elif 3 <= ratio <= 5: st.warning("ESTADO: CRÓNICA")
    elif ratio > 5: st.warning("Acidosis metabólica adicional")
    st.markdown("**Causas (VINDICATE):** Vascular, Inflamatorio, Neoplásico, Degenerativo/Drogas, Idiopático/Intoxicación, Congénito, Autoinmune, Traumático, Endocrino.")

# --- ALCALOSIS METABÓLICA ---
if ph > 7.4 and hco3 > 22:
    st.subheader("🛑 ALCALOSIS METABÓLICA")
    p_esp = (0.7 * hco3) + 20
    st.write(f"PaCO2 esperada: {p_esp:.1f} +/- 5")
    if pco2 < p_esp - 5: st.warning("Alcalosis respiratoria adicional")
    elif pco2 > p_esp + 5: st.warning("Acidosis respiratoria adicional")
    if cloro_u > 0:
        if cloro_u < 20: st.info("CLORO-SENSIBLE: Vómitos, diuréticos, drenaje NG.")
        else: st.info("CLORO-RESISTENTE: Cushing, Bartter, Hipopotasemia.")

# --- 7. PASO 4: OXIGENACIÓN ---
st.divider()
st.header("IV. Perfil de Oxigenación")
pafi = pa02 / fio2
safi = spo2 / fio2
rox = (spo2 / fio2) / fr
g_real = ((560 - 47) * fio2) - (pco2 / 0.8) - pa02
g_ideal = (edad / 4) + 4

if pa02 < 60:
    st.error(f"PaO2 {pa02}: HIPOXEMIA (" + ("Leve" if pa02>=60 else "Moderada" if pa02>=40 else "Severa") + ")")
    st.write("**Causas:** 1. PB baja, 2. OVACE, 3. Laringe, 4. Vía aérea, 5. Alvéolo (Agua, Pus, Sangre), 6. Intersticio, 7. Vaso (TEP).")

c1, c2, c3 = st.columns(3)
c1.metric("PAFI", f"{pafi:.1f}", delta="Normal >300" if pafi>300 else "Alterada")
c2.metric("SAFI", f"{safi:.1f}", delta="Normal >315" if safi>315 else "Alterada")
c3.metric("ROX Index", f"{rox:.2f}", delta="Bajo riesgo" if rox>4.88 else "ALTO RIESGO" if rox<3.85 else "Riesgo Medio")

st.write(f"Gradiente A-a Real: {g_real:.1f} | Ideal: {g_ideal:.1f}")
es_grad_elevado = g_real > (g_ideal + 10)
if es_grad_elevado: st.error("Diferencia Elevada: LESIÓN INTRAPULMONAR")
else: st.success("Diferencia Normal: PULMÓN SANO (Extra-pulmonar)")

# --- CAUSAS CRUZADAS (PUNTO 13 FINAL) ---
if ph < 7.4 and pco2 > 32: # Acidosis Resp
    if not es_grad_elevado: st.info("Causa: Depresión SNC, fármacos, Guillain-Barré, Cifoescoliosis.")
    else: st.info("Causa: Asma grave, Neumonía o EPOC.")
elif ph > 7.4 and pco2 < 28: # Alcalosis Resp
    if not es_grad_elevado: st.info("Causa: Dolor, ansiedad, fiebre, AVC, hipertiroidismo, embarazo.")
    else: st.info("Causa: Neumonía, Edema pulmonar, TEP, Sepsis.")

st.caption("Propiedad Intelectual: Dr. Gonzalo Bernal Ferreira - Gases 2600")

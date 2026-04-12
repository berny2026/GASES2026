import streamlit as st
import streamlit.components.v1 as components
import math

# 2. IDENTIFICADOR (Google Analytics para saber quién entra)
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

# 1. NOMBRE Y CONFIGURACIÓN
st.set_page_config(page_title="Gases Arteriales - Dr. Bernal", layout="wide")
st.markdown("<h1 style='text-align: center;'>🫁 App Gases Arteriales</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>GONZALO BERNAL FERREIRA. MEDICO FAMILIAR</h2>", unsafe_allow_html=True)
st.divider()

# ENTRADA DE DATOS (Punto 7 y 11)
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
    fio2 = st.number_input("FiO2", 0.21, 1.00, 0.21, 0.01)
    edad = st.number_input("Edad (años)", 0, 115, 45)
    fr = st.number_input("Frecuencia Resp. (FR)", 5, 60, 20)
    spo2 = st.number_input("SpO2 (%)", 40, 100, 94)

cl_u = st.sidebar.number_input("Cloro Urinario (Solo Alcalosis Met.)", 0, 150, 0)

# --- PASO 1: CONSISTENCIA INTERNA (Puntos 4 y 5) ---
st.header("Paso 1: Evaluación de Consistencia Interna")
if ph < 7.2 or ph > 7.4:
    ph_hh = 6.1 + math.log10(hco3 / (pco2 * 0.03))
    dif_hh = abs(ph_hh - ph)
    st.write(f"Fórmula Henderson-Hasselbalch: {ph_hh:.3f}")
    st.write(f"Diferencia: {dif_hh:.3f}")
    if dif_hh <= 0.05: st.success("HAY CONSISTENCIA INTERNA")
    else: st.error("NO HAY CONSISTENCIA INTERNA")
else:
    h_ion = 24 * (pco2 / hco3)
    regla_80 = 80 - float(str(f"{ph:.2f}")[-2:])
    division = h_ion / regla_80 if regla_80 != 0 else 0
    st.write(f"H+: {h_ion:.1f} | Regla del 80: {regla_80}")
    st.write(f"Resultado División: {division:.2f}")
    if 0.7 <= division <= 1.2: st.success("HAY CONSISTENCIA INTERNA")
    else: st.error("NO HAY CONSISTENCIA INTERNA")

# --- PASO 2: ESTADO (Puntos 3 y 6: Bogotá 7.4) ---
st.header("Paso 2: Estado Ácido-Base (Bogotá)")
if ph < 7.4: 
    estado = "ACIDOSIS"
    st.error(f"{estado} (pH {ph} < 7.4)")
elif ph > 7.4: 
    estado = "ALCALOSIS"
    st.success(f"{estado} (pH {ph} > 7.4)")
else: 
    estado = "NEUTRO"
    st.info("NEUTRO (pH 7.4)")

# --- PASO 3: ANÁLISIS DE TRASTORNOS (Puntos 8 a 13) ---
st.header("Paso 3: Análisis de Trastornos y Causas")
ag_medido = na - (cl + hco3)
ag_corr = ag_medido + (2.5 * (4 - alb))

# ACIDOSIS RESPIRATORIA (Puntos 8, 9, 10)
if ph < 7.4 and pco2 > 32:
    st.subheader("ACIDOSIS RESPIRATORIA")
    dif_pco2 = pco2 - 30
    hco3_aguda = 20 + (1 * (dif_pco2/10))
    hco3_cronica = 20 + (4 * (dif_pco2/10))
    
    if hco3 <= hco3_aguda + 0.5: st.warning("CLASIFICACIÓN: AGUDA")
    elif hco3 >= hco3_cronica - 0.5: st.warning("CLASIFICACIÓN: CRÓNICA (>48h)")
    else: st.warning("CLASIFICACIÓN: CRÓNICA AGUDIZADA")

    with st.expander("CAUSAS (Punto 10)"):
        st.write("**1- SNC (VITAMINS):** V: Vasculares (Hematomas, EVC), I: Infecciones (Meningitis, Neumonías), T: Traumáticas, A: Autoinmunes (LES, AR), M: Metabólicas (IR, DM, Electrolitos), I: Intoxicaciones, N: Neoplasias, S: Psiquiátricas.")
        st.write("**2- SNP:** Guillain-Barré, VIH, Trauma raquimedular.")
        st.write("**3- PLACA NM:** Miastenia Gravis, Botulismo, Organofosforados.")
        st.write("**4- MUSCULAR:** Fatiga por hipoxemia, Miopatías.")
        st.write("**5- ALVÉOLO:** EPOC, EPA, SDRA.")
        st.write("**6- ÓSEO:** Tórax inestable, Cifoescoliosis.")

# ACIDOSIS METABÓLICA (Punto 11)
if ph < 7.4 and hco3 < 18:
    st.subheader("ACIDOSIS METABÓLICA")
    p_winters = (1.5 * hco3) + 8
    st.write(f"PaCO2 esperada (Winters): {p_winters:.1f} +/- 2")
    if pco2 > p_winters + 2: st.warning("TRASTORNO SECUNDARIO: Acidosis respiratoria sobreagregada")
    elif pco2 < p_winters - 2: st.warning("TRASTORNO SECUNDARIO: Alcalosis respiratoria")
    else: st.success("Estado: COMPENSADO")

    st.write(f"Anión GAP Corregido: {ag_corr:.1f}")
    if ag_corr > 12:
        st.error("ANION GAP ELEVADO (GOLDMARCC)")
        st.write("G: Glicoles, O: Oxiprolina, L: Lactato (>4), D: D-Lactato, M: Metanol, A: Aspirina, R: Rabdomiolisis, C: Cetoacidosis, C: Creatinina elevada.")
        # Delta GAP
        delta_gap = (ag_corr - 10) - (20 - hco3)
        st.write(f"Delta GAP: {delta_gap:.1f}")
        if -5 <= delta_gap <= 5: st.info("Interpretación: Acidosis Metabólica PURA")
        elif delta_gap > 5: st.info("Interpretación: Alcalosis Metabólica SOBREAGREGADA")
        else: st.info("Interpretación: Acidosis Metabólica HIPERCLORÉMICA")
    else:
        st.info("ANION GAP NORMAL/BAJO: Hipercloremia, Diarrea, ATR, Laxantes, etc.")

# ALCALOSIS RESPIRATORIA (Punto 12)
if ph > 7.4 and pco2 < 28:
    st.subheader("ALCALOSIS RESPIRATORIA")
    dif_p_alc = 30 - pco2
    # Compensación
    if hco3 <= 20 - (2 * (dif_p_alc/10)): st.warning("AGUDA")
    elif hco3 <= 20 - (3.5 * (dif_p_alc/10)): st.warning("CRÓNICA")
    
    with st.expander("CAUSAS (VINDICATE)"):
        st.write("V: Infartos, I: Inflamación/Sepsis, N: Neoplasia, D: Drogas/Degenerativo, I: Idiopático/Intoxicación, C: Congénito, A: Autoinmune, T: Traumático, E: Endocrino.")

# ALCALOSIS METABÓLICA (Punto 13)
if ph > 7.4 and hco3 > 22:
    st.subheader("ALCALOSIS METABÓLICA")
    p_esp_met = 0.7 * hco3 + 20
    st.write(f"PaCO2 esperada: {p_esp_met:.1f} +/- 5")
    if pco2 < p_esp_met - 5: st.warning("Alcalosis respiratoria adicional")
    elif pco2 > p_esp_met + 5: st.warning("Acidosis respiratoria adicional")
    
    if cl_u > 0:
        if cl_u < 20: st.info("CLORO-SENSIBLE: Vómitos, diuréticos. Responde a NaCl 0.9%")
        else: st.info("CLORO-RESISTENTE: Hiperaldosteronismo, Cushing, Bartter.")

# --- OXIGENACIÓN (Independiente) ---
st.divider()
st.header("Evaluación de la Oxigenación")
pafi = pa02 / fio2
safi = spo2 / fio2
rox = (spo2 / fio2) / fr
grad_real = ((fio2 * 513) - (pco2 / 0.8)) - pa02
grad_ideal = (edad / 4) + 4

col_o1, col_o2 = st.columns(2)
with col_o1:
    st.metric("PaO2", f"{pa02} mmHg")
    if pa02 < 60:
        if pa02 < 40: st.error("Hipoxemia SEVERA")
        elif pa02 < 60: st.warning("Hipoxemia MODERADA")
    st.write(f"PAFI: {pafi:.1f} | SAFI: {safi:.1f} | ROX: {rox:.2f}")

with col_o2:
    st.write(f"Gradiente (D(A-a)O2) REAL: {grad_real:.1f}")
    st.write(f"Gradiente (D(A-a)O2) IDEAL: {grad_ideal:.1f}")
    if abs(grad_real - grad_ideal) <= 10:
        st.success("PULMÓN SANO (Causa Extrapulmonar)")
    else:
        st.error("LESIÓN INTRAPULMONAR")

with st.expander("Ver Causas de Hipoxemia"):
    st.write("1. Bajada Presión Barométrica | 2. OVACE | 3. Laringe (Estridor) | 4. Traquea/Bronquios (Asma/EPOC) | 5. Alvéolo (Agua, Pus, Sangre, Células) | 6. Intersticio | 7. Vasos (TEP).")

st.caption("Gases 2600 - Propiedad Intelectual Dr. Gonzalo Bernal Ferreira")

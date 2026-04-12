import streamlit as st
import streamlit.components.v1 as components
import math

# --- 2. IDENTIFICADOR (Google Analytics) ---
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

# --- 1. IDENTIFICACIÓN ---
st.set_page_config(page_title="Gases 2600 - Dr. Bernal", layout="wide")
st.markdown("<h1 style='text-align: center;'>🫁 App Gases Arteriales</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>GONZALO BERNAL FERREIRA. MEDICO FAMILIAR</h2>", unsafe_allow_html=True)
st.divider()

# --- ENTRADA DE DATOS (Puntos 7, 11 y 13) ---
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

cl_u = st.sidebar.number_input("Cloro Urinario (Opcional)", 0, 150, 0)

# --- PASO 1: CONSISTENCIA (Puntos 4 y 5) ---
st.header("1. Consistencia Interna")
if ph < 7.2 or ph > 7.4:
    ph_hh = 6.1 + math.log10(hco3 / (pco2 * 0.03))
    dif = abs(ph_hh - ph)
    st.write(f"pH Henderson-Hasselbalch: {ph_hh:.3f} | Diferencia: {dif:.3f}")
    if dif <= 0.05: st.success("HAY CONSISTENCIA INTERNA")
    else: st.error("NO HAY CONSISTENCIA INTERNA")
else:
    h_ion = 24 * (pco2 / hco3)
    r80 = 80 - float(f"{ph:.2f}"[-2:])
    div = h_ion / r80 if r80 != 0 else 0
    st.write(f"H+: {h_ion:.1f} | Regla 80: {r80} | Resultado: {div:.2f}")
    if 0.7 <= div <= 1.2: st.success("HAY CONSISTENCIA INTERNA")
    else: st.error("NO HAY CONSISTENCIA INTERNA")

# --- PASO 2: ESTADO (Puntos 3 y 6) ---
st.header("2. Estado Ácido-Base (Bogotá)")
if ph < 7.4: st.error("ACIDOSIS")
elif ph > 7.4: st.success("ALCALOSIS")
else: st.info("NEUTRO (7.4)")

# --- PASO 3: TRASTORNOS Y CAUSAS (Puntos 8-13) ---
st.header("3. Análisis de Trastornos y Causas")
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
    
    st.markdown("""
    **Causas de Acidosis Respiratoria:**
    1. **SNC (VITAMINS):** V: Vasculares (Hematomas, EVC), I: Infecciones (Meningitis, Neumonía), T: Trauma, A: Autoinmune (LES, AR), M: Metabólica (IR, DM), I: Intoxicaciones, N: Neoplasia, S: Psiquiátrica.
    2. **SNP:** Guillain Barré, VIH, Neuropatía, Trauma raquimedular.
    3. **Placa NM:** Miastenia Gravis, Eaton Lambert, Botulismo, Organofosforados.
    4. **Musculares:** Fatiga por hipoxemia, Miopatías.
    5. **Alvéolo:** EPOC, Edema Pulmonar, SDRA.
    6. **Caja Torácica:** Tórax inestable, Cifoescoliosis, Fracturas.
    """)

# --- ACIDOSIS METABÓLICA ---
if ph < 7.4 and hco3 < 18:
    st.subheader("🛑 ACIDOSIS METABÓLICA")
    win = (1.5 * hco3) + 8
    st.write(f"PaCO2 esperada (Winters): {win:.1f} +/- 2")
    if pco2 > win + 2: st.warning("TRASTORNO: Acidosis respiratoria sobreagregada")
    elif pco2 < win - 2: st.warning("TRASTORNO: Alcalosis respiratoria")
    else: st.success("Compensado")

    st.write(f"Anión GAP Corregido: {ag_c:.1f}")
    if ag_c > 12:
        st.error("CAUSA: ANION GAP ELEVADO (GOLDMARCC)")
        st.write("**G:** Glicoles, **O:** Oxiprolina (Acetaminofén), **L:** Lactato (>4), **D:** D-Lactato, **M:** Metanol, **A:** Aspirina, **R:** Rabdomiolisis, **C:** Cetoacidosis, **C:** Creatinina (IR).")
        dg = (ag_c - 10) - (20 - hco3)
        if -5 <= dg <= 5: st.info("Delta Gap: Acidosis Metabólica Pura")
        elif dg > 5: st.info("Delta Gap: Alcalosis Metabólica Sobreagregada")
        else: st.info("Delta Gap: Acidosis Metabólica Hiperclorémica")
    else:
        st.info("CAUSA: AG NORMAL (Hipercloremia, Diarrea, ATR, Laxantes).")

# --- ALCALOSIS RESPIRATORIA ---
if ph > 7.4 and pco2 < 28:
    st.subheader("🛑 ALCALOSIS RESPIRATORIA")
    dif_p = 30 - pco2
    if hco3 <= 20 - (2*(dif_p/10)): st.warning("AGUDA")
    elif hco3 <= 20 - (4*(dif_p/10)): st.warning("CRÓNICA")
    st.markdown("**Causas (VINDICATE):** Vascular, Inflamatorio, Neoplásico, Degenerativo/Drogas, Idiopático/Intoxicación, Congénito, Autoinmune, Traumático, Endocrino.")

# --- ALCALOSIS METABÓLICA ---
if ph > 7.4 and hco3 > 22:
    st.subheader("🛑 ALCALOSIS METABÓLICA")
    p_win = 0.7 * hco3 + 20
    st.write(f"PaCO2 esperada: {p_win:.1f} +/- 5")
    if cl_u > 0:
        if cl_u < 20: st.info("CLORO-SENSIBLE: Vómitos, diuréticos.")
        else: st.info("CLORO-RESISTENTE: Cushing, Bartter, Hipopotasemia.")

# --- PASO 4: OXIGENACIÓN ---
st.divider()
st.header("4. Perfil de Oxigenación (Punto 13)")
pafi = pa02 / fio2
safi = spo2 / fio2
rox = (spo2 / fio2) / fr
g_real = ((fio2 * 513) - (pco2 / 0.8)) - pa02
g_ideal = (edad / 4) + 4

if pa02 < 60:
    if pa02 < 40: st.error(f"PaO2 {pa02}: Hipoxemia SEVERA")
    else: st.warning(f"PaO2 {pa02}: Hipoxemia MODERADA")

col1, col2, col3 = st.columns(3)
col1.metric("PAFI", f"{pafi:.1f}")
col2.metric("SAFI", f"{safi:.1f}")
col3.metric("ROX Index", f"{rox:.2f}")

st.write(f"D(A-a)O2 Real: {g_real:.1f} | D(A-a)O2 Ideal: {g_ideal:.1f}")
if g_real > g_ideal + 10: st.error("LESIÓN INTRAPULMONAR")
else: st.success("PULMÓN SANO (Extra-pulmonar)")

st.markdown("""
**Causas de Hipoxemia:** 1. Presión barométrica baja, 2. OVACE, 3. Laringe, 4. Tráquea/Bronquios (Asma/EPOC), 5. Ocupación alveolar (Pus, Sangre, Agua), 6. Intersticio, 7. Vasos (TEP).
""")

st.caption("Gases 2600 - Propiedad Intelectual Dr. Gonzalo Bernal Ferreira")

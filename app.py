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

# --- 4. CONSISTENCIA INTERNA ---
st.header("I. Consistencia Interna")
if ph < 7.2 or ph > 7.4:
    ph_hh = 6.1 + math.log10(hco3 / (pco2 * 0.03))
    dif = abs(ph_hh - ph)
    st.write(f"pH Henderson-Hasselbalch: {ph_hh:.3f} | Diferencia: {dif:.3f}")
    if dif <= 0.05: st.success("HAY CONSISTENCIA INTERNA")
    else: st.error("NO HAY CONSISTENCIA INTERNA. Sugerir repetir por posible contaminación con burbujas, anticoagulante o son venosos.")
else:
    h_ion = 24 * (pco2 / hco3)
    r80 = 80 - float(f"{ph:.2f}"[-2:])
    div_80 = h_ion / r80 if r80 != 0 else 0
    st.write(f"Hidrogeniones (H+): {h_ion:.1f} | Regla del 80: {r80} | Resultado: {div_80:.2f}")
    if 0.7 <= div_80 <= 1.2: st.success("HAY CONSISTENCIA INTERNA")
    else: st.error("NO HAY CONSISTENCIA INTERNA")

# --- 5. ESTADO pH ---
st.header("II. Estado Ácido-Base (Bogotá)")
if ph < 7.4: st.error("ACIDOSIS (pH < 7.4)")
elif ph > 7.4: st.success("ALCALOSIS (pH > 7.4)")
else: st.info("NEUTRO (pH 7.4)")

# --- 6. ANÁLISIS DEL TRASTORNO ---
st.header("III. Análisis del Trastorno Primario y Secundario")
ag_c = (na - (cl + hco3)) + (2.5 * (4 - alb))

# ACIDOSIS RESPIRATORIA
if ph < 7.4 and pco2 > 32:
    st.subheader("🛑 ACIDOSIS RESPIRATORIA")
    dif_p = pco2 - 30
    h_ag = 20 + (1 * (dif_p/10))
    h_cr = 20 + (4 * (dif_p/10))
    if hco3 <= h_ag + 1: st.warning("ESTADO: AGUDA")
    elif hco3 >= h_cr - 1: st.warning("ESTADO: CRÓNICA")
    else: st.warning("ESTADO: CRÓNICA AGUDIZADA")
    
    st.markdown("""
    **CAUSAS DE ACIDOSIS RESPIRATORIA:**
    1. **SNC (VITAMINS):** V: Vasculares (Hematomas, EVC), I: Infecciones (Meningitis, abscesos, neumonías), T: Traumáticas, A: Autoinmunes (LES, AR), M: Metabólicas (IR, DM, falla hepática), I: Intoxicaciones, N: Neoplasias, S: Psiquiátricas.
    2. **SNP:** Guillain barre, VIH, neuropatía periférica, trauma raquimedular.
    3. **PLACA NEUROMUSCULAR:** Miastenia gravis, Eaton Lambert, botulismo, organofosforados, accidente ofídico.
    4. **MUSCULARES:** FATIGA MUSCULAR por Hipoxemia (Diafragma, intercostales), miopatías.
    5. **ALVEOLO:** EPOC, Edema pulmonar agudo grave, SDRA.
    6. **COSTILLAS/COLUMNA:** Tórax inestable, cifoescoliosis, espondilitis, fracturas.
    """)

# ACIDOSIS METABÓLICA
if ph < 7.4 and hco3 < 18:
    st.subheader("🛑 ACIDOSIS METABÓLICA")
    win = (1.5 * hco3) + 8
    st.write(f"PaCO2 esperada (Winters): {win:.1f} +/- 2")
    if pco2 > win + 2: st.error("TRASTORNO: Acidosis respiratoria sobreagregada")
    elif pco2 < win - 2: st.success("TRASTORNO: Alcalosis respiratoria")
    else: st.info("ESTADO: Compensado")
    
    st.write(f"Anión GAP Corregido: {ag_c:.1f}")
    if ag_c > 12:
        st.error("CAUSA: ANION GAP ELEVADO - MNEMOTECNIA GOLDMARCC:")
        st.markdown("""
        * **G:** Glicoles (refrigerantes para neveras, industriales o automóviles).
        * **O:** Oxiprolina (intoxicación por acetaminofén).
        * **L:** Lactato (acidosis láctica con lactato mayor a 4).
        * **D:** D-lactato (como en intestino corto).
        * **M:** Metanol.
        * **A:** Aspirina (intoxicación por ácido acetilsalicílico), anticonvulsivantes.
        * **R:** Rabdomiólisis.
        * **C:** Cetoacidosis diabética o no diabética.
        * **C:** Creatinina elevada o injuria renal aguda o crónica.
        """)
        dg = (ag_c - 10) - (20 - hco3)
        st.write(f"Delta Gap: {dg:.1f}")
        if -5 <= dg <= 5: st.info("INTERPRETACIÓN: Acidosis Metabólica Pura")
        elif dg > 5: st.info("INTERPRETACIÓN: Alcalosis Metabólica Sobreagregada")
        else: st.info("INTERPRETACIÓN: Acidosis Metabólica Hiperclorémica")
    else:
        st.info("CAUSA: AG NORMAL O BAJO (8-12). 1. Hipercloremia, 2. Diarrea, 3. ATR, 4. Hipofosfatemia, 5. Laxantes, 6. Acetazolamida.")

# ALCALOSIS RESPIRATORIA
if ph > 7.4 and pco2 < 28:
    st.subheader("🛑 ALCALOSIS RESPIRATORIA")
    dif_p = 30 - pco2
    dec_hco3 = 20 - hco3
    ratio = dec_hco3 / (dif_p / 10) if dif_p != 0 else 0
    if 1.9 <= ratio <= 2.1: st.warning("ALCALOSIS RESPIRATORIA AGUDA")
    elif ratio < 2: st.error("Alcalosis metabólica adicional")
    elif 3 <= ratio <= 5: st.warning("ALCALOSIS RESPIRATORIA CRÓNICA")

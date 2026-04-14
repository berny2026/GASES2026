import streamlit as st
import streamlit.components.v1 as components
import math

# 2. IDENTIFICADOR (Google Analytics)
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
st.markdown("<h2 style='text-align: center;'>NOMBRE. GONZALO BERNAL FERREIRA. MEDICO FAMILIAR</h2>", unsafe_allow_html=True)
st.divider()

# ENTRADA DE DATOS
col1, col2, col3 = st.columns(3)
with col1:
    ph = st.number_input("pH Arterial", 6.80, 7.80, 7.40, 0.01)
    pco2 = st.number_input("PaCO2 (mmHg)", 10.0, 90.0, 30.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 5.0, 50.0, 20.0, 0.1)
with col2:
    na = st.number_input("Sodio (Na)", 110.0, 170.0, 140.0, 0.1)
    cl = st.number_input("Cloro (Cl)", 70.0, 130.0, 105.0, 0.1)
    alb = st.number_input("Albúmina (g/dL)", 1.0, 5.0, 4.0, 0.1)
    lactato = st.number_input("Lactato (mmol/L)", 0.0, 20.0, 1.0, 0.1)
with col3:
    pa02 = st.number_input("PaO2 (mmHg)", 20.0, 200.0, 60.0, 0.1)
    fio2 = st.number_input("FiO2 (ej. 0.21)", 0.21, 1.00, 0.21, 0.01)
    edad = st.number_input("Edad (años)", 0, 115, 45)
    fr = st.number_input("Frecuencia Respiratoria (FR)", 5, 60, 20)
    spo2 = st.number_input("SpO2 (%)", 40, 100, 94)

cloro_u = st.sidebar.number_input("Cloro Urinario (mEq/L)", 0, 150, 0)

# #PRIMERO: CONSISTENCIA INTERNA (Punto 4 y 5)
st.header("I. Evaluación de la Consistencia Interna")
if ph < 7.2 or ph > 7.4:
    # PASO 1: Henderson-Hasselbalch
    ph_calc = 6.1 + math.log10(hco3 / (pco2 * 0.03))
    dif = abs(ph_calc - ph)
    st.write(f"pH calculado (HH): {ph_calc:.3f} | Diferencia: {dif:.3f}")
    if dif <= 0.05:
        st.success("HAY CONSISTENCIA INTERNA")
    else:
        st.error("NO HAY CONSISTENCIA INTERNA. Sugerir repetir por posible contaminación.")
else:
    # PASO 2: Regla del 80
    h_ion = 24 * (pco2 / hco3)
    ph_decimales = float(f"{ph:.2f}"[-2:])
    regla_80 = 80 - ph_decimales
    division = h_ion / regla_80 if regla_80 != 0 else 0
    st.write(f"H+: {h_ion:.1f} | Regla 80 (80 - {ph_decimales}): {regla_80} | División: {division:.2f}")
    if 0.7 <= division <= 1.2:
        st.success("HAY CONSISTENCIA INTERNA")
    else:
        st.error("NO HAY CONSISTENCIA INTERNA")

# ##SEGUNDO: EVALUACIÓN DEL pH (Punto 6)
st.header("II. Evaluación del pH (Bogotá)")
if ph < 7.4:
    st.error("ACIDOSIS")
    diag_base = "ACIDOSIS"
elif ph > 7.4:
    st.success("ALCALOSIS")
    diag_base = "ALCALOSIS"
else:
    st.info("NEUTRO (7.4)")
    diag_base = "NEUTRO"

# ### TERCERO: TRASTORNO PRIMARIO (Puntos 8 a 13)
st.header("III. Trastorno Primario y Compensación")

# Cálculo de Anion Gap (AG) - Se usa en varios puntos
ag_medido = na - (cl + hco3)
ag_corregido = ag_medido + (2.5 * (4 - alb))

# --- ACIDOSIS RESPIRATORIA ---
if ph < 7.4 and pco2 > 32:
    st.subheader("Acidosis Respiratoria")
    dif_pco2 = pco2 - 30
    hco3_aguda = 20 + (1 * (dif_pco2/10))
    hco3_cronica = 20 + (4 * (dif_pco2/10))
    st.write(f"HCO3 esperado Agudo: {hco3_aguda:.1f} | Crónico: {hco3_cronica:.1f}")
    
    if hco3 <= hco3_aguda + 1: st.warning("Tipo: AGUDA")
    elif hco3 >= hco3_cronica - 1: st.warning("Tipo: CRÓNICA (>48 horas)")
    else: st.warning("Tipo: CRÓNICA AGUDIZADA")
    
    st.markdown("**Causas de Acidosis Respiratoria:**")
    st.write("1- SNC (VITAMINS): V: Vasculares, I: Infecciones, T: Traumáticas, A: Autoinmunes, M: Metabólicas, I: Intoxicaciones, N: Neoplasias, S: Psiquiátricas.")
    st.write("2- SNP: Guillain barre, VIH, Neuropatía, Trauma raquimedular.")
    st.write("3- PLACA NM: Miastenia gravis, Eaton Lambert, Botulismo, Organofosforados.")
    st.write("4- MUSCULARES: Fatiga muscular (Diafragma, Intercostales).")
    st.write("5- ALVEOLO: EPOC, Edema pulmonar, SDRA.")
    st.write("6- COSTILLAS/COLUMNA: Tórax inestable, Cifoescoliosis.")

# --- ACIDOSIS METABÓLICA ---
if ph < 7.4 and hco3 < 18:
    st.subheader("Acidosis Metabólica")
    pco2_winters = (1.5 * hco3) + 8
    st.write(f"PaCO2 esperada (Winters): {pco2_winters:.1f} +/- 2")
    if pco2 > pco2_winters + 2: st.warning("Trastorno secundario: ACIDOSIS RESPIRATORIA SOBREAGREGADA")
    elif pco2 < pco2_winters - 2: st.warning("Trastorno secundario: ALCALOSIS RESPIRATORIA")
    else: st.success("Estado: COMPENSADO")

    st.write(f"Anion Gap Corregido: {ag_corregido:.1f}")
    if ag_corregido > 12:
        st.error("CAUSA: ANION GAP ELEVADO (>12) - Mnemotecnia GOLDMARCC:")
        st.write("**G:** Glicoles (refrigerantes para neveras, industriales o automóviles).")
        st.write("**O:** Oxiprolina (intoxicación por acetaminofén).")
        st.write("**L:** Lactato (acidosis láctica con lactato mayor a 4).")
        st.write("**D:** D-lactato (como en el síndrome de intestino corto).")
        st.write("**M:** Metanol.")
        st.write("**A:** Aspirina (ácido acetilsalicilico), anticonvulsivantes, ansiolíticos.")
        st.write("**R:** Rabdomiólisis.")
        st.write("**C:** Cetoacidosis diabética o no diabética.")
        st.write("**C:** Creatinina elevada o injuria renal aguda o crónica.")

# --- ALCALOSIS RESPIRATORIA ---
if ph > 7.4 and pco2 < 28:
    st.subheader("Alcalosis Respiratoria")
    dif_pco2_alc = 30 - pco2
    delta_hco3 = 20 - hco3
    ratio = delta_hco3 / (dif_pco2_alc / 10) if dif_pco2_alc != 0 else 0
    st.write(f"Ratio de descenso HCO3: {ratio:.2f}")
    if 1.9 <= ratio <= 2.1: st.warning("Alcalosis Respiratoria AGUDA")
    elif ratio < 2: st.warning("Alcalosis Metabólica Adicional")
    elif 3 <= ratio <= 5: st.warning("Alcalosis Respiratoria CRÓNICA")
    elif ratio > 5: st.warning("Acidosis Metabólica Adicional")

    st.markdown("**Causas (VINDICATE):**")
    st.write("V: Vascular, I: Infeccioso, N: Neoplásico, D: Drogas, I: Intoxicación, C: Congénito, A: Autoinmune, T: Traumático, E: Endocrino.")

# --- ALCALOSIS METABÓLICA ---
if ph > 7.4 and hco3 > 22:
    st.subheader("Alcalosis Metabólica")
    pco2_esp = (0.7 * hco3) + 20
    st.write(f"PaCO2 esperada: {pco2_esp:.1f} +/- 5")
    if pco2 < pco2_esp - 5: st.warning("Alcalosis respiratoria adicional")
    elif pco2 > pco2_esp + 5: st.warning("Acidosis respiratoria adicional")
    
    if cloro_u > 0:
        if cloro_u < 20: st.info("CLORO-SENSIBLE: Vómitos, diuréticos. Responde a NaCl 0.9%")
        else: st.info("CLORO-RESISTENTE: Hiperaldosteronismo, Cushing, Bartter.")

# EVALUAR AG SIEMPRE QUE SEA > 12
if ag_corregido > 12 and not (ph < 7.4 and hco3 < 18):
    st.warning(f"Anion Gap Elevado detectado ({ag_corregido:.1f}): Sospechar aumento de ácidos (GOLDMARCC).")

# ####### OXIGENACIÓN (Independiente)
st.divider()
st.header("IV. Evaluación de la Oxigenación")
st.write(f"PaO2 Normal Bogotá: ≥ 60 mmHg (FiO2 0.21)")

if pa02 < 60:
    st.error("HIPOXEMIA detectada")
    if pa02 >= 60: st.write("Clasificación: Normal/Leve (60-80)") # Ajuste según su rango
    elif 40 <= pa02 < 60: st.warning("Clasificación: MODERADA")
    else: st.error("Clasificación: SEVERA (<40)")
    
    st.markdown("**Causas de Hipoxemia:**")
    st.write("1- PB baja, 2- OVACE, 3- Laringe, 4- Vía aérea (Asma, EPOC), 5- Alvéolo (Agua, Pus, Sangre, Células), 6- Intersticio, 7- Vasos.")

# ÍNDICES
pafi = pa02 / fio2
safi = spo2 / fio2
rox = (spo2 / fio2) / fr
# Gradiente (D(A-a)O2)
pb_bogota = 560 # Presión barométrica promedio Bogotá
pv_h2o = 47
grad_real = ((pb_bogota - pv_h2o) * fio2) - (pco2 / 0.8) - pa02
grad_ideal = (edad / 4) + 4

col_i1, col_i2, col_i3 = st.columns(3)
col_i1.metric("PAFI", f"{pafi:.1f}")
col_i2.metric("SAFI", f"{safi:.1f}")
col_i3.metric("ROX Index", f"{rox:.2f}")

st.write(f"Gradiente A-a Real: {grad_real:.1f} | Ideal: {grad_ideal:.1f}")
if abs(grad_real - grad_ideal) <= 10:
    st.success("Diferencia Normal (≤ 10): PULMÓN SANO")
else:
    st.error("Diferencia Elevada (> 10): LESIÓN INTRAPULMONAR")

with st.expander("Ver Interpretación de Oxigenación por trastorno"):
    st.write("- Acidosis Resp. Aguda + G-Aa normal: Depresión SNC, fármacos.")
    st.write("- Acidosis Resp. Aguda + G-Aa elevado: Obstrucción, Asma, Neumonía.")
    st.write("- Alcalosis Resp. Aguda + G-Aa elevado: TEP, Neumonía, Sepsis.")

st.caption("Gases 2600 - Propiedad Intelectual Dr. Gonzalo Bernal Ferreira")

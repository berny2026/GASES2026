import streamlit as st
import streamlit.components.v1 as components
import math

# 1. RASTREADOR DE VISITAS (Google Analytics)
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

# 2. IDENTIFICACIÓN Y TÍTULO
st.set_page_config(page_title="Gases 2600 - Dr. Bernal", layout="wide")
st.markdown("<h1 style='text-align: center;'>🫁 Gases Arteriales 2600m</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Gonzalo Bernal Ferreira - Médico Familiar</h3>", unsafe_allow_html=True)
st.divider()

# 3. ENTRADA DE DATOS (Puntos 1 al 13 de su instructivo)
c1, c2, c3 = st.columns(3)
with c1:
    ph = st.number_input("pH Arterial", 6.80, 7.80, 7.40, 0.01)
    pco2 = st.number_input("pCO2 (mmHg)", 10.0, 90.0, 30.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 5.0, 50.0, 20.0, 0.1)
with c2:
    na = st.number_input("Sodio (Na)", 110.0, 170.0, 140.0, 0.1)
    cl = st.number_input("Cloro (Cl)", 70.0, 130.0, 105.0, 0.1)
    alb = st.number_input("Albúmina (g/dL)", 1.0, 5.0, 4.0, 0.1)
with c3:
    pa02 = st.number_input("PaO2 (mmHg)", 20.0, 200.0, 60.0, 0.1)
    fio2 = st.number_input("FiO2 (ej. 0.21)", 0.21, 1.00, 0.21, 0.01)
    edad = st.number_input("Edad (años)", 0, 115, 45)
    fr = st.number_input("FR (resp/min)", 8, 60, 20)
    spo2 = st.number_input("SpO2 (%)", 50, 100, 94)

# --- PROCESAMIENTO MÉDICO ---

# Paso 1: Consistencia Interna (Puntos 4 y 5)
st.header("Paso 1: Consistencia Interna")
if ph < 7.2 or ph > 7.4:
    ph_calc = 6.1 + math.log10(hco3 / (pco2 * 0.03))
    dif = abs(ph_calc - ph)
    st.write(f"Henderson-Hasselbalch Diferencia: {dif:.3f}")
    if dif <= 0.05: st.success("HAY CONSISTENCIA INTERNA")
    else: st.error("NO HAY CONSISTENCIA INTERNA")
else:
    h_ion = 24 * (pco2 / hco3)
    regla_80 = 80 - float(str(f"{ph:.2f}")[-2:])
    res_div = h_ion / regla_80 if regla_80 != 0 else 0
    if 0.7 <= res_div <= 1.2: st.success("HAY CONSISTENCIA INTERNA")
    else: st.error("NO HAY CONSISTENCIA INTERNA")

# Paso 2: Estado (Punto 6)
st.header("Paso 2: Determinación del Estado (Bogotá)")
if ph < 7.4:
    estado = "ACIDOSIS"
    st.error(f"{estado} (pH {ph} < 7.4)")
elif ph > 7.4:
    estado = "ALCALOSIS"
    st.success(f"{estado} (pH {ph} > 7.4)")
else:
    estado = "NEUTRO"
    st.info("NEUTRO (pH 7.4)")

# Paso 3: Análisis (Puntos 7-13)
st.header("Paso 3: Análisis del Trastorno")
ag_c = (na - (cl + hco3)) + (2.5 * (4 - alb))

if ph < 7.4:
    if pco2 > 32: # Acidosis Respiratoria
        st.subheader("Acidosis Respiratoria")
        # Lógica aguda vs crónica
        dif_p = pco2 - 30
        esp_h_ag = 20 + (1 * (dif_p/10))
        esp_h_cr = 20 + (4 * (dif_p/10))
        if hco3 <= esp_h_ag + 1: st.warning("Tipo: AGUDA")
        elif hco3 >= esp_h_cr - 1: st.warning("Tipo: CRÓNICA")
        else: st.warning("Tipo: CRÓNICA AGUDIZADA")
    elif hco3 < 18: # Acidosis Metabólica
        st.subheader("Acidosis Metabólica")
        winter = (1.5 * hco3) + 8
        st.write(f"pCO2 esperada: {winter:.1f} +/- 2")
        st.write(f"Anion Gap Corregido: {ag_c:.1f}")
        if ag_c > 12: st.error("AG ELEVADO (GOLDMARCC)")
        else: st.info("AG NORMAL (Hiperclorémica)")

# Paso 4: Oxigenación
st.divider()
st.header("Paso 4: Perfil de Oxigenación")
grad_p = ((fio2 * 513) - (pco2 / 0.8)) - pa02
grad_i = (edad / 4) + 4
st.write(f"D(A-a)O2: {grad_p:.1f} (Límite ideal: {grad_i:.1f})")
if grad_p > grad_i + 10: st.error("LESIÓN INTRAPULMONAR")
else: st.success("PULMÓN SANO (Extrapulmonar)")

st.caption("Gases 2600 - Propiedad del Dr. Gonzalo Bernal Ferreira")

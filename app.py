import streamlit as st
import streamlit.components.v1 as components
import math

# --- GOOGLE ANALYTICS ---
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

st.set_page_config(page_title="Gases 2600 - Dr. Bernal", layout="wide")
st.markdown("<h1 style='text-align: center;'>🫁 Gases Arteriales 2600m</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Gonzalo Bernal Ferreira - Médico Familiar</h3>", unsafe_allow_html=True)
st.divider()

# ENTRADA DE DATOS
c1, c2, c3 = st.columns(3)
with c1:
    ph = st.number_input("pH Arterial", 6.80, 7.80, 7.15, 0.01)
    pco2 = st.number_input("pCO2 (mmHg)", 10.0, 90.0, 45.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 5.0, 50.0, 15.0, 0.1)
with c2:
    na = st.number_input("Sodio (Na)", 110.0, 170.0, 140.0, 0.1)
    cl = st.number_input("Cloro (Cl)", 70.0, 130.0, 100.0, 0.1)
    alb = st.number_input("Albúmina (g/dL)", 1.0, 5.0, 4.0, 0.1)
with c3:
    pa02 = st.number_input("PaO2 (mmHg)", 20.0, 200.0, 50.0, 0.1)
    fio2 = st.number_input("FiO2", 0.21, 1.00, 0.35, 0.01)
    edad = st.number_input("Edad", 0, 115, 60)

# 1. CONSISTENCIA
st.header("Paso 1: Consistencia Interna")
h_ion = 24 * (pco2 / hco3)
regla_80 = 80 - float(str(f"{ph:.2f}")[-2:])
res = h_ion / regla_80 if regla_80 != 0 else 0
if 0.7 <= res <= 1.2: st.success(f"HAY CONSISTENCIA (H+: {h_ion:.1f})")
else: st.error("NO HAY CONSISTENCIA")

# 2. ESTADO
st.header("Paso 2: Estado Ácido-Base")
if ph < 7.4: st.error(f"ACIDOSIS (pH {ph} < 7.4)")
else: st.success(f"ALCALOSIS (pH {ph} > 7.4)")

# 3. ANÁLISIS MIXTO (Corregido para mostrar ambos)
st.header("Paso 3: Análisis de Trastornos")
ag_c = (na - (cl + hco3)) + (2.5 * (4 - alb))

# Evaluar Acidosis Respiratoria
if pco2 > 32:
    st.subheader("🛑 Trastorno: ACIDOSIS RESPIRATORIA")
    st.write("Causas: Ver VITAMINS (SNC, Obstrucción, Neuromuscular)")

# Evaluar Acidosis Metabólica
if hco3 < 18:
    st.subheader("🛑 Trastorno: ACIDOSIS METABÓLICA")
    winter = (1.5 * hco3) + 8
    st.write(f"pCO2 esperada por Winters: {winter:.1f} +/- 2")
    if pco2 > winter + 2: 
        st.warning("Confirmado: Acidosis Respiratoria Sobreagregada (No compensada)")
    
    st.metric("Anion Gap Corregido", f"{ag_c:.1f}")
    if ag_c > 12:
        st.error("ANION GAP ELEVADO: Pensar en GOLDMARCC (Cetoacidosis, Lactato, Falla Renal)")
        dg = (ag_c - 10) - (20 - hco3)
        if dg > 5: st.warning("Asociado: Alcalosis Metabólica Terciaria")

# 4. OXIGENACIÓN
st.header("Paso 4: Perfil de Oxigenación")
pafi = pa02 / fio2
grad_p = ((fio2 * 513) - (pco2 / 0.8)) - pa02
grad_i = (edad / 4) + 4

col1, col2 = st.columns(2)
col1.metric("PAFI", f"{pafi:.1f}")
col2.write(f"Gradiente A-a Real: {grad_p:.1f} (Ideal: {grad_i:.1f})")

if grad_p > grad_i + 10:
    st.error("INTERPRETACIÓN: LESIÓN INTRAPULMONAR (Etiología Parenquimatosa)")
else:
    st.success("INTERPRETACIÓN: PULMÓN SANO (Etiología Extrapulmonar)")

st.caption("Gases 2600 - Dr. Gonzalo Bernal Ferreira")

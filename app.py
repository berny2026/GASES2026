import streamlit as st
import streamlit.components.v1 as components
import math

# --- GOOGLE ANALYTICS ---
components.html("""
<script async src="https://www.googletagmanager.com/gtag/js?id=G-KF0W30KFST"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-KF0W30KFST');
</script>
""", height=0)

# --- CONFIG ---
st.set_page_config(page_title="Gases Bogotá PRO", layout="wide")

st.markdown("<h1 style='text-align: center; color: #D32F2F;'>🏔️ Gases Arteriales Bogotá</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Dr. Gonzalo Bernal Ferreira</h4>", unsafe_allow_html=True)

# --- INPUTS ---
with st.sidebar:
    st.header("📥 Datos clínicos")

    ph = st.number_input("pH", 6.8, 7.8, 7.18, 0.01)
    pco2 = st.number_input("PaCO2", 10.0, 100.0, 55.0)
    hco3 = st.number_input("HCO3", 2.0, 50.0, 20.0)

    st.divider()

    na = st.number_input("Na", 100.0, 170.0, 140.0)
    cl = st.number_input("Cl", 60.0, 140.0, 105.0)
    alb = st.number_input("Albúmina", 0.5, 6.0, 4.0)

    st.divider()

    pao2 = st.number_input("PaO2", 10.0, 300.0, 48.0)
    spo2 = st.number_input("SpO2 (%)", 30, 100, 85)
    fio2 = st.number_input("FiO2", 0.21, 1.0, 0.21)
    edad = st.number_input("Edad", 0, 100, 40)
    fr = st.number_input("FR", 4, 60, 12)

# =========================
# CÁLCULOS
# =========================
henderson = 6.1 + math.log10(hco3 / (pco2 * 0.03))
diff = abs(henderson - ph)

ag = na - (cl + hco3)
ag_corr = ag + (2.5 * (4 - alb))

pao2_calc = (fio2 * 513) - (pco2 / 0.8)
grad = pao2_calc - pao2
grad_ideal = (edad / 4) + 4

pafi = pao2 / fio2
safi = spo2 / fio2
rox = safi / fr if fr > 0 else 0

# =========================
# RESULTADOS
# =========================

# CONSISTENCIA
st.subheader("✅ Consistencia interna")
st.write(f"pH calculado: {henderson:.3f}")
st.write(f"Diferencia: {diff:.3f}")

if diff <= 0.05:
    st.success("Muestra válida")
else:
    st.error("Muestra NO confiable")

# ESTADO
st.subheader("⚖️ Estado ácido-base")

if ph > 7.4:
    estado = "Alcalosis"
elif ph < 7.4:
    estado = "Acidosis"
else:
    estado = "Normal"

st.write(f"Estado: **{estado}**")

# DIAGNÓSTICO
if ph < 7.4 and pco2 > 32:
    dx = "Acidosis respiratoria"
elif ph < 7.4 and hco3 < 18:
    dx = "Acidosis metabólica"
elif ph > 7.4 and pco2 < 28:
    dx = "Alcalosis respiratoria"
elif ph > 7.4 and hco3 > 22:
    dx = "Alcalosis metabólica"
else:
    dx = "Trastorno mixto"

st.markdown(f"### 🧠 Diagnóstico: {dx}")

# =========================
# ACIDOSIS RESPIRATORIA
# =========================
if dx == "Acidosis respiratoria":

    delta_co2 = pco2 - 30
    hco3_agudo = 20 + (delta_co2/10)*1
    hco3_cronico = 20 + (delta_co2/10)*4

    st.write(f"HCO3 esperado agudo: {hco3_agudo:.1f}")
    st.write(f"HCO3 esperado crónico: {hco3_cronico:.1f}")

    if abs(hco3 - hco3_agudo) < 2:
        st.error("Aguda")
    elif abs(hco3 - hco3_cronico) < 3:
        st.warning("Crónica")
    else:
        st.warning("Crónica agudizada")

    with st.expander("🔍 Causas (VITAMINS)", expanded=True):
        st.markdown("""
        SNC: ACV, infecciones, trauma, fármacos  
        SNP: Guillain-Barré  
        Placa NM: Miastenia, botulismo  
        Músculo: fatiga diafragmática  
        Pulmón: EPOC, asma, SDRA  
        Caja torácica: cifoescoliosis  
        """)

# =========================
# ACIDOSIS METABÓLICA
# =========================
elif dx == "Acidosis metabólica":

    st.subheader("🔄 Compensación (Winter)")
    esperado = 1.5 * hco3 + 8
    st.write(f"PaCO2 esperada: {esperado:.1f} ±2")

    if pco2 > esperado + 2:
        st.error("Acidosis respiratoria agregada")
    elif pco2 < esperado - 2:
        st.warning("Alcalosis respiratoria agregada")
    else:
        st.success("Compensación adecuada")

    st.subheader("🧪 Anion Gap")
    st.write(f"AG corregido: {ag_corr:.1f}")

    if ag_corr > 12:

        with st.expander("🔬 GOLDMARK", expanded=True):
            st.markdown("""
            Glicoles  
            Oxiprolina  
            Lactato  
            D-lactato  
            Metanol  
            Aspirina  
            Renal  
            Cetoacidosis  
            """)

        delta_gap = (ag_corr - 10) - (20 - hco3)
        st.write(f"Delta Gap: {delta_gap:.1f}")

        if -5 <= delta_gap <= 5:
            st.success("Acidosis pura")
        elif delta_gap > 5:
            st.warning("Alcalosis metabólica agregada")
        else:
            st.error("Acidosis hiperclorémica")

# =========================
# ALCALOSIS RESPIRATORIA
# =========================
elif dx == "Alcalosis respiratoria":

    delta = 30 - pco2
    hco3_agudo = 20 - (delta/10)*2
    hco3_cronico = 20 - (delta/10)*4

    st.write(f"HCO3 esperado agudo: {hco3_agudo:.1f}")
    st.write(f"HCO3 esperado crónico: {hco3_cronico:.1f}")

# =========================
# ALCALOSIS METABÓLICA
# =========================
elif dx == "Alcalosis metabólica":

    esperado = 0.7 * hco3 + 20
    st.write(f"PaCO2 esperada: {esperado:.1f} ±5")

# =========================
# OXIGENACIÓN
# =========================
st.subheader("☁️ Oxigenación")

col1, col2, col3 = st.columns(3)
col1.metric("PAFI", f"{pafi:.0f}")
col2.metric("SAFI", f"{safi:.0f}")
col3.metric("ROX", f"{rox:.2f}")

st.write(f"Gradiente A-a: {grad:.1f} (Ideal {grad_ideal:.1f})")

# CLASIFICACIÓN
if pafi > 300:
    st.success("PAFI normal")
elif 200 <= pafi <= 300:
    st.warning("PAFI leve")
elif 100 <= pafi < 200:
    st.error("PAFI moderado")
else:
    st.error("PAFI severo")

if safi < 150:
    st.error("SAFI severo")

if rox < 3.85:
    st.error("Alto riesgo de falla respiratoria")

# HIPOXEMIA
if pao2 < 60:

    st.error(f"HIPOXEMIA ({pao2} mmHg)")

    if grad > grad_ideal + 10:
        with st.expander("Causas intrapulmonares"):
            st.write("Neumonía, SDRA, edema pulmonar, TEP")
    else:
        with st.expander("Causas extrapulmonares"):
            st.write("Hipoventilación, altitud, depresión respiratoria")

st.caption("Gases Bogotá PRO v1.0")

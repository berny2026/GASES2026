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

    ph = st.number_input("pH", 6.8, 7.8, 7.30, 0.01)
    pco2 = st.number_input("PaCO2", 10.0, 100.0, 30.0)
    hco3 = st.number_input("HCO3", 2.0, 50.0, 20.0)

    st.divider()

    na = st.number_input("Na", 100.0, 170.0, 140.0)
    cl = st.number_input("Cl", 60.0, 140.0, 105.0)
    alb = st.number_input("Albúmina", 0.5, 6.0, 4.0)

    st.divider()

    pao2 = st.number_input("PaO2", 10.0, 300.0, 60.0)
    spo2 = st.number_input("SpO2 (%)", 30, 100, 90)
    fio2 = st.number_input("FiO2", 0.21, 1.0, 0.21)
    edad = st.number_input("Edad", 0, 100, 40)
    fr = st.number_input("FR", 4, 60, 16)

# =========================
# PASO 1 CONSISTENCIA
# =========================
st.subheader("1️⃣ Consistencia interna")

henderson = 6.1 + math.log10(hco3 / (pco2 * 0.03))
diff = abs(henderson - ph)

if ph < 7.2 or ph > 7.4:
    st.write(f"pH calculado: {henderson:.3f}")
    st.write(f"Diferencia: {diff:.3f}")

    if diff <= 0.05:
        st.success("Consistencia adecuada")
        consistente = True
    else:
        st.error("NO consistente → posible error de muestra")
        consistente = False

else:
    h_ion = 24 * (pco2 / hco3)
    regla80 = 80 - int((ph * 100) % 100)
    relacion = h_ion / regla80

    st.write(f"H+: {h_ion:.1f}")
    st.write(f"Regla 80: {regla80}")
    st.write(f"Relación: {relacion:.2f}")

    if 0.7 <= relacion <= 1.2:
        st.success("Consistencia adecuada")
        consistente = True
    else:
        st.error("NO consistente")
        consistente = False

# ⚠️ NO SE DETIENE LA APP
if not consistente:
    st.warning("Interpretar con precaución")

# =========================
# PASO 2 ESTADO
# =========================
st.subheader("2️⃣ Estado ácido-base")

if ph > 7.4:
    estado = "Alcalosis"
elif ph < 7.4:
    estado = "Acidosis"
else:
    estado = "Neutro"

st.write(estado)

# =========================
# PASO 3 DIAGNÓSTICO
# =========================
st.subheader("3️⃣ Trastorno primario")

if ph < 7.4 and pco2 > 32:
    dx = "Acidosis respiratoria"
elif ph < 7.4 and hco3 < 18:
    dx = "Acidosis metabólica"
elif ph > 7.4 and pco2 < 28:
    dx = "Alcalosis respiratoria"
elif ph > 7.4 and hco3 > 22:
    dx = "Alcalosis metabólica"
else:
    dx = "Trastorno mixto o compensado"

st.markdown(f"### {dx}")

# =========================
# ACIDOSIS METABÓLICA
# =========================
if dx == "Acidosis metabólica":

    st.subheader("Compensación (Winter)")
    esperado = 1.5 * hco3 + 8
    st.write(f"PaCO2 esperada: {esperado:.1f} ±2")

    if pco2 > esperado + 2:
        st.error("Acidosis respiratoria agregada")
    elif pco2 < esperado - 2:
        st.warning("Alcalosis respiratoria agregada")
    else:
        st.success("Compensación adecuada")

    # ANION GAP
    ag = na - (cl + hco3)
    ag_corr = ag + (2.5 * (4 - alb))

    st.subheader("Anion Gap")
    st.write(f"AG corregido: {ag_corr:.1f}")

    if ag_corr > 12:

        with st.expander("Causas GOLDMARCC", expanded=True):
            st.markdown("""
            G: Glicoles  
            O: Oxiprolina  
            L: Lactato  
            D: D-lactato  
            M: Metanol  
            A: ASA / fármacos  
            R: Rabdomiólisis  
            C: Cetoacidosis  
            C: Creatinina elevada  
            """)

        delta = (ag_corr - 10) - (20 - hco3)
        st.write(f"Delta GAP: {delta:.1f}")

        if -5 <= delta <= 5:
            st.success("Acidosis metabólica pura")
        elif delta > 5:
            st.warning("Alcalosis metabólica agregada")
        else:
            st.error("Acidosis hiperclorémica")

# =========================
# ACIDOSIS RESPIRATORIA
# =========================
if dx == "Acidosis respiratoria":

    delta_co2 = pco2 - 30
    hco3_agudo = 20 + (delta_co2/10)
    hco3_cronico = 20 + (delta_co2/10)*4

    st.write(f"HCO3 agudo esperado: {hco3_agudo:.1f}")
    st.write(f"HCO3 crónico esperado: {hco3_cronico:.1f}")

    with st.expander("Causas (VITAMINS)", expanded=True):
        st.markdown("""
        SNC: ACV, infecciones, trauma, fármacos  
        SNP: Guillain-Barré  
        Placa NM: Miastenia, botulismo  
        Músculo: fatiga  
        Pulmón: EPOC, asma, SDRA  
        Caja torácica: cifoescoliosis  
        """)

# =========================
# OXIGENACIÓN
# =========================
st.subheader("5️⃣ Oxigenación")

PAO2 = (513 * fio2) - (pco2 / 0.8)
grad = PAO2 - pao2
ideal = (edad / 4) + 4

pafi = pao2 / fio2
safi = spo2 / fio2
rox = safi / fr if fr > 0 else 0

st.write(f"Gradiente A-a: {grad:.1f} (Ideal {ideal:.1f})")

st.write(f"PAFI: {pafi:.0f}")
st.write(f"SAFI: {safi:.0f}")
st.write(f"ROX: {rox:.2f}")

if pao2 < 60:
    st.error("Hipoxemia")

    if grad > ideal + 10:
        st.warning("Origen intrapulmonar")
    else:
        st.success("Origen extrapulmonar")

st.caption("Algoritmo clínico Bogotá - versión funcional")

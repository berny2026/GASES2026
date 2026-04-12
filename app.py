import streamlit as st

# 1. IDENTIFICACIÓN Y TÍTULOS
st.set_page_config(page_title="Gases 2600 - Dr. Bernal", layout="wide")

st.markdown("<h1 style='text-align: center;'>🫁 Gases 2600</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Interpretación Clínica: Dr. Gonzalo Bernal</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Médico Familiar</p>", unsafe_allow_html=True)
st.divider()

# 2. ENTRADA DE DATOS (Organización por columnas)
c1, c2, c3 = st.columns(3)
with c1:
    st.subheader("🧪 Bioquímica")
    ph = st.number_input("pH Arterial", 6.80, 7.80, 7.24, 0.01)
    pco2 = st.number_input("pCO2 (mmHg)", 10.0, 90.0, 24.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 5.0, 50.0, 10.0, 0.1)
with c2:
    st.subheader("🩸 Electrolitos")
    na = st.number_input("Sodio (Na)", 110.0, 160.0, 140.0, 0.1)
    cl = st.number_input("Cloro (Cl)", 70.0, 130.0, 102.0, 0.1)
    alb = st.number_input("Albúmina (g/dL)", 1.0, 5.0, 3.0, 0.1)
with c3:
    st.subheader("🫁 Oxigenación / Otros")
    pa02 = st.number_input("PaO2 (mmHg)", 20.0, 200.0, 55.0, 0.1)
    fio2 = st.number_input("FiO2 (0.21-1.0)", 0.21, 1.0, 0.35, 0.01)
    edad = st.number_input("Edad (años)", 0, 115, 45)
    fr = st.number_input("FR (resp/min)", 8, 60, 24)
    spo2 = st.number_input("SatO2 (%)", 50, 100, 90)

# --- SECUENCIA LÓGICA ESTRICTA ---

# PASO 1: CONSISTENCIA
st.divider()
h_calc = 24 * (pco2 / hco3)
h_ph = 10**(9 - ph)
st.header("🔍 Paso 1: Consistencia Interna")
if abs(h_calc - h_ph) < 5:
    st.success(f"✅ Gases Consistentes (H+ calc: {h_calc:.1f})")
else:
    st.error(f"⚠️ Gases Inconsistentes. El equilibrio químico no coincide con el pH.")

# PASO 2: DIAGNÓSTICO PRIMARIO
st.header("🔬 Paso 2: Análisis Ácido-Base")

ag_medido = na - (cl + hco3)
ag_corr = ag_medido + (2.5 * (4 - alb))

if ph < 7.36:
    st.error("ESTADO: ACIDEMIA")
    # LÓGICA METABÓLICA (Uso de HCO3 < 19 para Bogotá)
    if hco3 < 19:
        st.subheader("Trastorno Primario: ACIDOSIS METABÓLICA")
        
        # PASO 3: WINTER
        p_esp = (1.5 * hco3) + 8
        st.info(f"Paso 3: pCO2 Esperada (Winter): {p_esp:.1f} (+/- 2)")
        if pco2 < (p_esp - 2): st.warning("Interpretación: Alcalosis respiratoria sobreagregada.")
        elif pco2 > (p_esp + 2): st.warning("Interpretación: Acidosis respiratoria sobreagregada.")
        else: st.success("Interpretación: Compensación respiratoria adecuada.")

        # PASO 4: ANION GAP
        st.metric("Paso 4: Anion Gap Corregido", f"{ag_corr:.1f}")

        # PASO 5: CAUSAS (GOLDMARCC)
        if ag_corr > 12:
            st.warning("**Paso 5: Causas (GOLDMARCC):** Glicoles, Oxoproline, L-Lactato, D-Lactato, Metanol, Aspirina, Renal (Uremia), Cetoacidosis.")
            
            # PASO 6: DELTA DEL GAP (Fórmula de su imagen)
            delta_gap = (ag_corr - 10) - (20 - hco3)
            st.subheader(f"Paso 6: Delta del Gap: {delta_gap:.1f}")
            if -5 <= delta_gap <= 5:
                st.info("Resultado: Acidosis Metabólica Pura")
            elif delta_gap > 5:
                st.info("Resultado: Alcalosis Metabólica Sobreagregada")
            else:
                st.info("Resultado: Acidosis Metabólica Hiperclorémica")
        else:
            st.info("Paso 5: Causas AG Normal: Diarrea, Fístulas, ATR, Hipercloremia.")
    else:
        st.subheader("Trastorno Primario: ACIDOSIS RESPIRATORIA")
        st.warning("Causas: Obstrucción aérea, EPOC, Depresión SNC.")

elif ph > 7.44:
    st.success("ESTADO: ALCALEMIA")
    if pco2 < 28: st.subheader("Trastorno: Alcalosis Respiratoria")
    else: st.subheader("Trastorno: Alcalosis Metabólica")

# PASO 7: OXIGENACIÓN
st.divider()
st.header("📊 Paso 7: Perfil de Oxigenación")
grad = ((fio2 * (560 - 47)) - (pco2 / 0.8)) - pa02
pafi = pa02 / fio2
safi = spo2 / fio2
rox = (safi / fr)

res1, res2, res3, res4 = st.columns(4)
res1.metric("PAFI", f"{pafi:.1f}")
res2.metric("SAFI", f"{safi:.1f}")
res3.metric("ROX", f"{rox:.2f}")
res4.metric("Grad. Aa", f"{grad:.1f}")

grad_esp = (edad / 4) + 4
if grad > grad_esp:
    st.write(f"Interpretación: **Gradiente Elevado** (Límite para la edad: {grad_esp:.1f}).")
else:
    st.write("Interpretación: **Gradiente Normal**.")

st.divider()
st.caption("Gases 2600 - Propiedad Intelectual del Dr. Gonzalo Bernal")

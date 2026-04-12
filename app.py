import streamlit as st

# 1. MATRIZ DE CONFIGURACIÓN
st.set_page_config(page_title="Gases 2600 - Matriz Clínica", layout="wide")
st.markdown("<h1 style='text-align: center;'>🫁 Gases 2600</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Interpretación: Dr. Gonzalo Bernal</h3>", unsafe_allow_html=True)
st.divider()

# 2. ENTRADA DE DATOS
c1, c2, c3 = st.columns(3)
with c1:
    ph = st.number_input("pH Arterial", 6.80, 7.80, 7.40, 0.01)
    pco2 = st.number_input("pCO2 (mmHg)", 10.0, 90.0, 30.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 5.0, 50.0, 20.0, 0.1)
with c2:
    na = st.number_input("Sodio (Na)", 110.0, 160.0, 140.0, 0.1)
    cl = st.number_input("Cloro (Cl)", 70.0, 130.0, 105.0, 0.1)
    alb = st.number_input("Albúmina (g/dL)", 1.0, 5.0, 4.0, 0.1)
with c3:
    pa02 = st.number_input("PaO2 (mmHg)", 20.0, 200.0, 60.0, 0.1)
    fio2 = st.number_input("FiO2 (0.21-1.0)", 0.21, 1.0, 0.21, 0.01)
    edad = st.number_input("Edad (años)", 0, 115, 45)
    fr = st.number_input("FR (resp/min)", 8, 60, 20)
    spo2 = st.number_input("SatO2 (%)", 50, 100, 94)

# --- PROCESAMIENTO ANALÍTICO ---
st.divider()

# PASO 1: CONSISTENCIA
h_calc = 24 * (pco2 / hco3)
h_ph = 10**(9 - ph)
st.subheader("Paso 1: Consistencia Interna")
if abs(h_calc - h_ph) < 5:
    st.success(f"✅ Gases Consistentes (H+ calc: {h_calc:.1f})")
else:
    st.error("⚠️ Gases Inconsistentes.")

# PASO 2: ESTADO
if ph < 7.36: estado = "ACIDEMIA"
elif ph > 7.44: estado = "ALCALEMIA"
else: estado = "NORMAL"
st.subheader(f"Paso 2: Estado -> {estado}")

# PASOS 3-6: ANÁLISIS DE TRASTORNOS
ag_c = (na - (cl + hco3)) + (2.5 * (4 - alb))

if estado == "ACIDEMIA":
    if hco3 < 19:
        st.header("Acidosis Metabólica")
        winter = (1.5 * hco3) + 8
        st.info(f"pCO2 Esperada (Winter): {winter:.1f} (+/- 2)")
        if pco2 > winter + 2: st.warning("Interpretación: Acidosis Respiratoria Sobreagregada")
        elif pco2 < winter - 2: st.warning("Interpretación: Alcalosis Respiratoria Sobreagregada")
        
        st.metric("Anion Gap Corregido", f"{ag_c:.1f}")
        if ag_c > 12:
            delta = (ag_c - 10) - (20 - hco3)
            st.write(f"**Paso 6: Delta del Gap: {delta:.1f}**")
            if -5 <= delta <= 5: st.info("Interpretación: Pura")
            elif delta > 5: st.info("Interpretación: Alcalosis Metabólica Sobreagregada")
            else: st.info("Interpretación: Acidosis Metabólica AG Normal Asociada")
    else:
        st.header("Acidosis Respiratoria")

elif estado == "ALCALEMIA":
    if hco3 > 22:
        st.header("Alcalosis Metabólica")
        p_esp = 30 + (0.7 * (hco3 - 20))
        st.info(f"pCO2 Esperada: {p_esp:.1f}")
    else:
        st.header("Alcalosis Respiratoria")

# PASO 7: OXIGENACIÓN
st.divider()
st.header("Paso 7: Oxigenación")
grad_p = ((fio2 * 513) - (pco2 / 0.8)) - pa02
grad_i = (edad / 4) + 4
st.write(f"Gradiente Aa Paciente: **{grad_p:.1f}** | Gradiente Ideal (Edad): **{grad_i:.1f}**")
if grad_p > grad_i + 5:
    st.error("Interpretación: Causa Parenquimatosa (Shunt, V/Q, Difusión)")
else:
    st.success("Interpretación: Causa Extrapulmonar (Hipoventilación)")

st.caption("Gases 2600 - Propiedad Intelectual del Dr. Gonzalo Bernal")

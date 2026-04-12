import streamlit as st

# 1. MATRIZ DE CONFIGURACIÓN
st.set_page_config(page_title="Gases 2600 - Matriz Clínica", layout="wide")
st.markdown("<h1 style='text-align: center;'>🫁 Gases 2600</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Matriz de Decisión Clínica: Dr. Gonzalo Bernal</h3>", unsafe_allow_html=True)
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

# --- MATRIZ LÓGICA PASO A PASO ---
st.divider()

# PASO 1: CONSISTENCIA
h_calc = 24 * (pco2 / hco3)
h_ph = 10**(9 - ph)
st.subheader("Paso 1: Consistencia Interna")
if abs(h_calc - h_ph) < 5:
    st.success(f"✅ Gases Consistentes (H+ calc: {h_calc:.1f})")
else:
    st.error("⚠️ Gases Inconsistentes. Revisar técnica.")

# PASO 2: DETERMINACIÓN DEL ESTADO
st.subheader("Paso 2: Estado del pH")
if ph < 7.36:
    estado = "ACIDEMIA"
    st.error(estado)
elif ph > 7.44:
    estado = "ALCALEMIA"
    st.success(estado)
else:
    estado = "NORMAL"
    st.info("pH Neutro o Trastorno Mixto")

# PASO 3 A 6: MATRIZ DE TRASTORNOS
st.header("Análisis del Trastorno Primario")

if estado == "ACIDEMIA":
    # ¿Metabólica o Respiratoria?
    if hco3 < 19: # Umbral Bogotá
        st.subheader("Trastorno: Acidosis Metabólica")
        # Compensación Winter
        p_esp = (1.5 * hco3) + 8
        st.info(f"pCO2 Esperada: {p_esp:.1f} (+/- 2)")
        if pco2 > p_esp + 2: st.warning("Asociado: Acidosis Respiratoria")
        elif pco2 < p_esp - 2: st.warning("Asociado: Alcalosis Respiratoria")
        
        # Anion Gap y Delta (Su imagen)
        ag_c = (na - (cl + hco3)) + (2.5 * (4 - alb))
        delta = (ag_c - 10) - (20 - hco3)
        st.write(f"Anion Gap Corregido: **{ag_c:.1f}**")
        if ag_c > 12: 
            st.warning("Causas: GOLDMARCC")
            st.write(f"**Delta del Gap: {delta:.1f}**")
            if -5 <= delta <= 5: st.info("Interpretación: Pura")
            elif delta > 5: st.info("Interpretación: Alcalosis Metabólica Asociada")
            else: st.info("Interpretación: Acidosis Metabólica AG Normal Asociada")
    else:
        st.subheader("Trastorno: Acidosis Respiratoria")
        h_esp = 20 + (0.1 * (pco2 - 30)) # Aguda
        st.info(f"HCO3 Esperado (Agudo): {h_esp:.1f}")

elif estado == "ALCALEMIA":
    if hco3 > 22:
        st.subheader("Trastorno: Alcalosis Metabólica")
        p_esp = 30 + (0.7 * (hco3 - 20))
        st.info(f"pCO2 Esperada: {p_esp:.1f}")
        if pco2 > p_esp + 2: st.warning("Asociado: Acidosis Respiratoria")
    else:
        st.subheader("Trastorno: Alcalosis Respiratoria")
        h_esp = 20 - (0.2 * (30 - pco2))
        st.info(f"HCO3 Esperado: {h_esp:.1f}")

# PASO 7: MATRIZ DE OXIGENACIÓN
st.divider()
st.header("Paso 7: Perfil de Oxigenación")
pa_alv = (fio2 * 513) - (pco2 / 0.8)
grad_p = pa_alv - pa02
grad_i = (edad / 4) + 4

col_res1, col_res2 = st.columns(2)
with col_res1:
    st.write(f"Gradiente Aa Paciente: **{grad_p:.1f}**")
    st.write(f"Gradiente Aa Ideal: **{grad_i:.1f}**")
with col_res2:
    st.write(f"PAFI: **{pa02/fio2:.1f}**")
    st.write(f"Índice de ROX: **{(spo2/fio2)/fr:.2f}**")

if grad_p > grad_i + 5:
    st.error("Interpretación: Gradiente Elevado (Parenquimatosa)")
    st.write("Causas: Shunt, V/Q, Difusión")
else:
    st.success("Interpretación: Gradiente Normal (Extrapulmonar)")
    st.write("Causas: Hipoventilación, FiO2 baja")

st.divider()
st.caption("Gases 2600 - Estructura Blindada Dr. Gonzalo Bernal")

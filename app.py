import streamlit as st
import math

# 1. IDENTIFICACIÓN Y TÍTULO
st.set_page_config(page_title="Gases Arteriales - Dr. Bernal", layout="wide")
st.markdown("<h1 style='text-align: center;'>🫁 Gases Arteriales 2600m</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Gonzalo Bernal Ferreira - Médico Familiar</h3>", unsafe_allow_html=True)
st.divider()

# 2. IDENTIFICADOR DE USO
if 'count' not in st.session_state: st.session_state.count = 1
st.sidebar.info(f"App en uso. Sesión ID: {st.session_state.count}")

# 3. ENTRADA DE DATOS
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
    fr = st.number_input("Frecuencia Resp.", 8, 60, 20)
    spo2 = st.number_input("SpO2 (%)", 50, 100, 94)

cl_u = st.sidebar.number_input("Cloro Urinario (mEq/L)", 0, 150, 0)

# --- INICIO DE PROCESAMIENTO ---
st.divider()

# 4 y 5. CONSISTENCIA INTERNA
st.header("Paso 1: Consistencia Interna")
if ph < 7.2 or ph > 7.4:
    ph_calc = 6.1 + math.log10(hco3 / (pco2 * 0.03))
    dif = abs(ph_calc - ph)
    st.write(f"Diferencia Henderson-Hasselbalch: {dif:.3f}")
    if dif <= 0.05: st.success("HAY CONSISTENCIA INTERNA")
    else: st.error("NO HAY CONSISTENCIA INTERNA")
else:
    h_ion = 24 * (pco2 / hco3)
    regla_80 = 80 - float(str(f"{ph:.2f}")[-2:])
    res_div = h_ion / regla_80 if regla_80 != 0 else 0
    st.write(f"Resultado Regla del 80: {res_div:.2f}")
    if 0.7 <= res_div <= 1.2: st.success("HAY CONSISTENCIA INTERNA")
    else: st.error("NO HAY CONSISTENCIA INTERNA")

# 6. ESTADO (Bogotá pH 7.4)
st.header("Paso 2: Estado del pH")
if ph < 7.4:
    estado = "ACIDOSIS"
    st.error(f"{estado} (pH {ph} < 7.4)")
elif ph > 7.4:
    estado = "ALCALOSIS"
    st.success(f"{estado} (pH {ph} > 7.4)")
else:
    estado = "NEUTRO"
    st.info("NEUTRO (pH 7.4)")

# 7-13. ANÁLISIS DE TRASTORNOS
st.header("Paso 3: Análisis del Trastorno")
ag_c = (na - (cl + hco3)) + (2.5 * (4 - alb))

if ph < 7.4: # RUTAS DE ACIDOSIS
    if pco2 > 32: # RESPIRATORIA
        st.subheader("ACIDOSIS RESPIRATORIA")
        dif_p = pco2 - 30
        esp_h = 20 + (dif_p / 10) # Aguda: 1 mEq por cada 10 mmHg
        esp_h_c = 20 + (4 * (dif_p / 10)) # Crónica: 4 mEq por cada 10 mmHg
        if hco3 <= esp_h + 1: st.warning("Tipo: AGUDA")
        elif hco3 >= esp_h_c - 1: st.warning("Tipo: CRÓNICA")
        else: st.warning("Tipo: CRÓNICA AGUDIZADA")
        with st.expander("Ver Causas (VITAMINS)"):
            st.write("SNC, SNP, Placa Neuromuscular, Músculo, Alvéolo, Caja Torácica.")
    elif hco3 < 18: # METABÓLICA
        st.subheader("ACIDOSIS METABÓLICA")
        winter = (1.5 * hco3) + 8
        st.write(f"pCO2 esperada (Winters): {winter:.1f} +/- 2")
        if pco2 > winter + 2: st.warning("Acidosis Respiratoria Sobreagregada")
        elif pco2 < winter - 2: st.warning("Alcalosis Respiratoria Sobreagregada")
        else: st.success("Compensada")
        
        st.write(f"Anion Gap Corregido: {ag_c:.1f}")
        if ag_c > 12:
            st.error("AG ELEVADO (GOLDMARCC)")
            dg = (ag_c - 10) - (20 - hco3)
            st.write(f"Delta Gap: {dg:.1f}")
            if -5 <= dg <= 5: st.info("Pura")
            elif dg > 5: st.info("Alcalosis Metabólica Sobreagregada")
            else: st.info("Acidosis Metabólica Hiperclorémica")
        else:
            st.info("AG NORMAL (Hiperclorémica, Diarrea, ATR)")

elif ph > 7.4: # RUTAS DE ALCALOSIS
    if pco2 < 28: # RESPIRATORIA
        st.subheader("ALCALOSIS RESPIRATORIA")
        dif_p = 30 - pco2
        h_esp_ag = 20 - (2 * (dif_p/10))
        h_esp_cr = 20 - (5 * (dif_p/10))
        if hco3 >= h_esp_ag: st.warning("Tipo: AGUDA")
        elif hco3 <= h_esp_cr: st.warning("Tipo: CRÓNICA")
        with st.expander("Ver Causas (VINDICATE)"):
            st.write("Vascular, Inflamatorio, Neoplásico, Drogas, Idiopático, Congénito, Autoinmune, Trauma, Endocrino.")
    elif hco3 > 22: # METABÓLICA
        st.subheader("ALCALOSIS METABÓLICA")
        p_esp = 0.7 * hco3 + 20
        st.write(f"pCO2 esperada: {p_esp:.1f} +/- 5")
        if cl_u > 0:
            if cl_u < 20: st.info("CLORO-SENSIBLE (Vómitos, Diuréticos)")
            else: st.info("CLORO-RESISTENTE (Cushing, Bartter, Aldosteronismo)")

# PASO FINAL: OXIGENACIÓN
st.divider()
st.header("Paso 4: Oxigenación")
grad_p = ((fio2 * 513) - (pco2 / 0.8)) - pa02
grad_i = (edad / 4) + 4
st.write(f"Gradiente Aa: {grad_p:.1f} (Ideal: {grad_i:.1f})")
if grad_p > grad_i + 10: st.error("LESIÓN INTRAPULMONAR")
else: st.success("PULMÓN SANO (Causa Extrapulmonar)")

st.caption("Gases 2600 - Propiedad Intelectual Dr. Gonzalo Bernal Ferreira")

import streamlit as st
import streamlit.components.v1 as components

# --- 1. GOOGLE ANALYTICS (G-KF0W30KFST) ---
components.html("""
<script async src="https://www.googletagmanager.com/gtag/js?id=G-KF0W30KFST"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-KF0W30KFST');
</script>
""", height=0)

# --- 2. CONFIGURACIÓN ---
st.set_page_config(page_title="Gases 2600 PRO - Bogotá", layout="wide")
st.markdown("<h1 style='text-align: center; color: #D32F2F;'>🏔️ Gases Arteriales Bogotá (2600m)</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Dr. Gonzalo Bernal Ferreira</h3>", unsafe_allow_html=True)

# --- 3. ENTRADA DE DATOS (SIDEBAR) ---
with st.sidebar:
    st.header("⌨️ Parámetros Clínicos")
    ph = st.number_input("pH Arterial", 6.80, 7.80, 7.40, 0.01)
    pco2 = st.number_input("PaCO2 (mmHg)", 10.0, 100.0, 30.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 2.0, 60.0, 20.0, 0.1)
    st.divider()
    na = st.number_input("Sodio (Na)", 110.0, 170.0, 140.0, 0.1)
    cl = st.number_input("Cloro (Cl)", 60.0, 140.0, 105.0, 0.1)
    alb = st.number_input("Albúmina (g/dL)", 0.5, 6.0, 4.0, 0.1)
    st.divider()
    pa02 = st.number_input("PaO2 (mmHg)", 10.0, 300.0, 65.0, 0.1)
    spo2 = st.number_input("SpO2 (%)", 30, 100, 92)
    fio2 = st.number_input("FiO2 (decimal)", 0.21, 1.00, 0.21, 0.01)
    edad = st.number_input("Edad (años)", 0, 110, 45)
    fr = st.number_input("FR (resp/min)", 4, 70, 18)

# --- 4. MOTOR LÓGICO ---
h_ion = 24 * (pco2 / hco3)
r80 = 80 - float(f"{ph:.2f}"[-2:])
ag_c = (na - (cl + hco3)) + (2.5 * (4 - alb))
# Ecuación Aire Alveolar Bogotá: (560 - 47) = 513
pao2_calc = (fio2 * 513) - (pco2 / 0.8)
g_real = pao2_calc - pa02
g_id = (edad / 4) + 4
pafi, safi = pa02/fio2, spo2/fio2
rox = (safi / fr) if fr > 0 else 0

# --- 5. VISUALIZACIÓN DE RESULTADOS ---

# I. Módulo de Consistencia
st.subheader("✅ I. Consistencia Interna")
if 0.8 <= (h_ion / r80) <= 1.2:
    st.success(f"MUESTRA VÁLIDA: H+ ({h_ion:.1f})")
else:
    st.error(f"❌ MUESTRA NO CONFIABLE (H+ calculada: {h_ion:.1f})")

# II. Análisis Ácido-Base (JERARQUÍA ESTRICTA)
st.subheader("⚖️ II. Equilibrio Ácido-Base")
col1, col2 = st.columns(2)

with col1:
    # --- BLOQUE ALCALEMIA (pH > 7.45) ---
    if ph > 7.45:
        if hco3 > 24:
            st.success("🚨 ALCALOSIS METABÓLICA")
            pco2_esp = 30 + (0.7 * (hco3 - 20))
            st.info(f"Compensación esperada (PaCO2): {pco2_esp:.1f} mmHg")
            with st.expander("🔍 Causas de Alcalosis Metabólica", expanded=True):
                st.markdown("""
                * **Cloro-Sensible (Vómitos, Diuréticos fase tardía).**
                * **Cloro-Resistente (Hiperaldosteronismo, Hipopotasemia severa).**
                """)
        if pco2 < 28:
            st.success("🚨 ALCALOSIS RESPIRATORIA")
            with st.expander("🔍 Causas"):
                st.write("Ansiedad, Fiebre, TEP, Hipoxia (Altura), Estímulo central.")

    # --- BLOQUE ACIDEMIA (pH < 7.35) ---
    elif ph < 7.35:
        if pco2 > 32:
            st.error("🛑 ACIDOSIS RESPIRATORIA")
            with st.expander("🔍 CAUSAS (Anatómicas)", expanded=True):
                st.markdown("""
                * **Centro/SNC:** Sedación, ACV, Trauma.
                * **Conducción/SNP/Placa:** Guillain-Barré, Miastenia Gravis, Bloqueantes NM.
                * **Efector/Músculo:** Fatiga, Distrofias.
                * **Caja/Columna:** Cifoescoliosis, Obesidad-Hipoventilación.
                * **Alvéolo:** EPOC, Asma, Obstrucción.
                """)
        if hco3 < 19:
            st.error("🛑 ACIDOSIS METABÓLICA")
            win = (1.5 * hco3) + 8
            st.info(f"Winters (PaCO2 esperada): {win:.1f} ± 2")

with col2:
    # --- Módulo de Brechas (Gap / Delta) ---
    st.metric("Anión Gap Corregido", f"{ag_c:.1f}", delta="Corte: 12", delta_color="inverse")
    if ag_c > 12:
        with st.expander("🔍 Causas GAP (GOLDMARCC)", expanded=True):
            st.write("Glicoles, Oxiprolina, Lactato, D-Lactato, Metanol, Aspirina, Renal, Cetoacidosis, Creatinina.")
        
        # Delta Gap solo si hay acidosis metabólica
        if hco3 < 19:
            delta_gap = (ag_c - 12) - (24 - hco3)
            if delta_gap > 6: st.success(f"➕ Alcalosis Metabólica Asociada (Delta: {delta_gap:.1f})")
            elif delta_gap < -6: st.warning(f"➕ Acidosis No Gap Asociada (Delta: {delta_gap:.1f})")

# III. Oxigenación Bogotá
st.subheader("☁️ III. Oxigenación y Causas de Hipoxemia")
o1, o2, o3, o4 = st.columns(4)
o1.metric("PAFI", f"{pafi:.0f}")
o2.metric("SAFI", f"{safi:.0f}")
o3.metric("ROX Index", f"{rox:.2f}")
o4.metric("Gradiente A-a", f"{g_real:.1f}", f"Ideal: {g_id:.1f}")

if pa02 < 60:
    st.error(f"🚨 HIPOXEMIA DETECTADA (PaO2: {pa02:.1f})")
    if g_real > (g_id + 10):
        st.warning("⚠️ GRADIENTE ELEVADO: Causa INTRAPULMONAR")
        with st.expander("🔍 Causas Intrapulmonares", expanded=True):
            st.markdown("1. Shunt (Alvéolo ocupado) | 2. V/Q desigual | 3. Difusión.")
    else:
        st.success("✅ GRADIENTE NORMAL: Causa EXTRAPULMONAR")
        with st.expander("🔍 Causas Extrapulmonares", expanded=True):
            st.markdown("1. Altura (Bogotá) | 2. Hipoventilación Alveolar (Falla de bomba o compensación).")

st.caption("Gases 2600 PRO - Bogotá v9.0 | Dr. Gonzalo Bernal Ferreira")

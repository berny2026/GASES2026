import streamlit as st
import streamlit.components.v1 as components

# --- 1. GOOGLE ANALYTICS (Rastreo Profesional) ---
components.html("""
<script async src="https://www.googletagmanager.com/gtag/js?id=G-KF0W30KFST"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-KF0W30KFST');
</script>
""", height=0)

# --- 2. CONFIGURACIÓN DE INTERFAZ ---
st.set_page_config(page_title="Gases 2600 PRO", layout="wide", page_icon="🫁")
st.markdown("<h1 style='text-align: center; color: #1E88E5;'>🫁 Gases Arteriales 2600 PRO</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Dr. Gonzalo Bernal Ferreira - Intensivista</h3>", unsafe_allow_html=True)
st.divider()

# --- 3. ENTRADA DE DATOS (SIDEBAR PARA LIMPIEZA VISUAL) ---
with st.sidebar:
    st.header("📊 Parámetros de Entrada")
    ph = st.number_input("pH Arterial", 6.80, 7.80, 7.40, 0.01)
    pco2 = st.number_input("PaCO2 (mmHg)", 5.0, 100.0, 30.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 2.0, 60.0, 20.0, 0.1)
    st.divider()
    na = st.number_input("Sodio (Na+)", 100.0, 180.0, 140.0, 0.1)
    cl = st.number_input("Cloro (Cl-)", 60.0, 140.0, 105.0, 0.1)
    alb = st.number_input("Albúmina (g/dL)", 0.5, 6.0, 4.0, 0.1)
    st.divider()
    pa02 = st.number_input("PaO2 (mmHg)", 10.0, 300.0, 65.0, 0.1)
    spo2 = st.number_input("SpO2 (%)", 30, 100, 94)
    fio2 = st.number_input("FiO2 (decimal, ej: 0.21)", 0.21, 1.00, 0.21, 0.01)
    edad = st.number_input("Edad (años)", 0, 110, 45)
    fr = st.number_input("FR (resp/min)", 4, 70, 18)

# --- 4. MOTOR DE CÁLCULO ---
h_ion = 24 * (pco2 / hco3)
r80 = 80 - float(f"{ph:.2f}"[-2:])
ag_c = (na - (cl + hco3)) + (2.5 * (4 - alb))
pao2_calc = (fio2 * 513) - (pco2 / 0.8) # Constante Bogotá (560-47)
g_real = pao2_calc - pa02
g_id = (edad / 4) + 4
pafi = pa02 / fio2
safi = spo2 / fio2
rox = (safi / fr) if fr > 0 else 0

# --- 5. RESULTADOS E INTERPRETACIÓN ---

# A. MÓDULO DE CONSISTENCIA
st.subheader("✅ I. Consistencia Interna")
c_ratio = h_ion / r80 if r80 != 0 else 0
if 0.8 <= c_ratio <= 1.2:
    st.success(f"MUESTRA VÁLIDA: H+ ({h_ion:.1f}) correlaciona con pH ({ph}).")
else:
    st.error(f"MUESTRA NO CONFIABLE: Discrepancia matemática detectada (H+: {h_ion:.1f}).")

# B. MÓDULO ÁCIDO-BASE
st.subheader("⚖️ II. Equilibrio Ácido-Base")
col1, col2 = st.columns(2)

with col1:
    # --- Diagnóstico Primario ---
    if ph < 7.35: # Acidemia
        if pco2 > 32:
            st.error("🚨 TRASTORNO: ACIDOSIS RESPIRATORIA")
            with st.expander("🔍 Causas (VITAMINS)"):
                st.write("**V:** Vascular (ACV, TEP) | **I:** Infección (Sepsis) | **T:** Toxinas (Opioides) | **A:** Autoimmune (MG, GB) | **M:** Metabólico | **I:** Iatrogenia | **N:** Neoplasia | **S:** SNC / Sueño")
        if hco3 < 19:
            st.error("🚨 TRASTORNO: ACIDOSIS METABÓLICA")
            win = (1.5 * hco3) + 8
            st.info(f"Winters: PaCO2 esperada {win:.1f} ± 2")
            if pco2 > win + 2: st.warning("⚠️ Acidosis Respiratoria Sobreagregada")
            elif pco2 < win - 2: st.warning("⚠️ Alcalosis Respiratoria Asociada")
    
    elif ph > 7.45: # Alcalemia
        if pco2 < 28:
            st.success("🚨 TRASTORNO: ALCALOSIS RESPIRATORIA")
        if hco3 > 24:
            st.success("🚨 TRASTORNO: ALCALOSIS METABÓLICA")

with col2:
    # --- Análisis de Brechas (Solo si hay Acidosis Metabólica o Gap Alto) ---
    if hco3 < 19 or ag_c > 12:
        st.metric("Anión Gap Corregido", f"{ag_c:.1f}", delta="Corte: 12")
        if ag_c > 12:
            with st.expander("🔍 Causas GAP ELEVADO (GOLDMARCC)"):
                st.write("**G:** Glicoles | **O:** Oxiprolina | **L:** Lactato | **D:** D-Lactato | **M:** Metanol | **A:** Aspirina | **R:** Renal/Rabdo | **C:** Cetoacidosis | **C:** Creatinina")
            delta_gap = (ag_c - 12) - (24 - hco3)
            if delta_gap > 6: st.success(f"➕ Alcalosis Metabólica Asociada (Delta: {delta_gap:.1f})")
            elif delta_gap < -6: st.warning(f"➕ Acidosis NO GAP Asociada (Delta: {delta_gap:.1f})")

# C. MÓDULO DE OXIGENACIÓN
st.subheader("☁️ III. Oxigenación (Ajustado a 2600m)")
def cat_sdra(v):
    if v < 100: return "🔴 SEVERO"
    if v < 200: return "🟠 MODERADO"
    if v < 300: return "🟡 LEVE"
    return "🟢 NORMAL"

o1, o2, o3, o4 = st.columns(4)
o1.metric("PAFI", f"{pafi:.0f}", cat_sdra(pafi))
o2.metric("SAFI", f"{safi:.0f}", cat_sdra(safi))
o3.metric("ROX Index", f"{rox:.2f}", "Riesgo VNI" if rox < 4.88 else "Estable")
o4.metric("Gradiente A-a", f"{g_real:.1f}", f"Ideal: {g_id:.1f}")

if g_real > (g_id + 10):
    st.error(f"DIAGNÓSTICO: LESIÓN INTRAPULMONAR")
    with st.expander("🔍 Las 7 Causas de Hipoxemia"):
        st.write("1. Altura | 2. Hipoventilación | 3. Shunt | 4. V/Q | 5. Difusión | 6. ↓Gasto | 7. Hb anómala")
else:
    st.success("DIAGNÓSTICO: PULMÓN SANO / CAUSA EXTRAPULMONAR")

st.caption("Gases 2600 PRO - v5.0 | Desarrollado para el Dr. Gonzalo Bernal Ferreira")

import streamlit as st
import streamlit.components.v1 as components

# --- 1. GOOGLE ANALYTICS ---
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
st.set_page_config(page_title="Gases 2600 PRO v3", layout="wide")
st.markdown("<h1 style='text-align: center;'>🫁 Gases Arteriales 2600 PRO</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Dr. Gonzalo Bernal Ferreira</h3>", unsafe_allow_html=True)

# --- 3. ENTRADA DE DATOS ---
with st.sidebar:
    st.header("⌨️ Datos del Paciente")
    ph = st.number_input("pH Arterial", 6.80, 7.80, 7.15, 0.01)
    pco2 = st.number_input("PaCO2 (mmHg)", 10.0, 90.0, 60.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 5.0, 50.0, 20.0, 0.1)
    st.divider()
    na = st.number_input("Sodio (Na)", 110.0, 170.0, 140.0, 0.1)
    cl = st.number_input("Cloro (Cl)", 70.0, 130.0, 105.0, 0.1)
    alb = st.number_input("Albúmina (g/dL)", 1.0, 5.0, 4.0, 0.1)
    st.divider()
    pa02 = st.number_input("PaO2 (mmHg)", 20.0, 200.0, 45.0, 0.1)
    spo2 = st.number_input("SpO2 (%)", 40, 100, 78)
    fio2 = st.number_input("FiO2 (decimal)", 0.21, 1.00, 0.21, 0.01)
    edad = st.number_input("Edad (años)", 0, 115, 65)
    fr = st.number_input("FR (resp/min)", 5, 60, 8)

# --- 4. LÓGICA DE DIAGNÓSTICO ---
h_ion = 24 * (pco2 / hco3)
r80 = 80 - float(f"{ph:.2f}"[-2:])
ag_c = (na - (cl + hco3)) + (2.5 * (4 - alb))
pao2_calc = (fio2 * 513) - (pco2 / 0.8)
g_real = pao2_calc - pa02
g_id = (edad / 4) + 4

# --- 5. RESULTADOS ---

# A. CONSISTENCIA
st.subheader("1. Consistencia Interna")
consis_ratio = h_ion / r80 if r80 != 0 else 0
if 0.7 <= consis_ratio <= 1.2:
    st.success(f"✅ MUESTRA VÁLIDA: H+ calculado ({h_ion:.1f}) es congruente con el pH.")
else:
    st.error(f"❌ MUESTRA NO CONFIABLE: Discrepancia entre H+ ({h_ion:.1f}) y pH.")

# B. ANÁLISIS ÁCIDO-BASE (JERARQUÍA CORREGIDA)
st.subheader("2. Diagnóstico Ácido-Base")
col1, col2 = st.columns(2)

with col1:
    # --- CASO ACIDEMIA (pH < 7.35) ---
    if ph < 7.35:
        # ¿Es Respiratoria? (CO2 > 32 en Bogotá)
        if pco2 > 32:
            st.error("🚨 TRASTORNO PRIMARIO: ACIDOSIS RESPIRATORIA")
            h_esp_aguda = 24 + ((pco2 - 30) * 0.1)
            if hco3 < h_esp_aguda - 2:
                st.warning("⚠️ ASOCIADO: ACIDOSIS METABÓLICA CONCOMITANTE")
            elif hco3 > h_esp_aguda + 3:
                st.success("⚠️ ASOCIADO: ALCALOSIS METABÓLICA (Compensación crónica o mixta)")
            
            with st.expander("🔍 CAUSAS (VITAMINS)"):
                st.write("**V:** ACV, TEP | **I:** Sepsis, Neumonía | **T:** Opioides, BZD | **A:** Miastenia, GB | **M:** Hipopotasemia | **S:** Apnea, Obesidad.")

        # ¿Es Metabólica? (HCO3 < 19 y CO2 normal o bajo)
        elif hco3 < 19:
            st.error("🚨 TRASTORNO PRIMARIO: ACIDOSIS METABÓLICA")
            win = (1.5 * hco3) + 8
            st.info(f"Winters (PaCO2 esperada): {win:.1f} ± 2")
            if pco2 > win + 2: st.warning("⚠️ ASOCIADO: ACIDOSIS RESPIRATORIA SOBREAGREGADA")
            
            if ag_c > 12:
                with st.expander("🔍 CAUSAS ANION GAP (GOLDMARCC)"):
                    st.write("Glicoles, Oxiprolina, Lactato, D-Lactato, Metanol, Aspirina, Renal, Cetoacidosis.")

with col2:
    # --- ANÁLISIS DE BRECHAS ---
    if ag_c > 12:
        st.warning(f"Anión Gap Elevado Corregido: {ag_c:.1f}")
        delta_gap = (ag_c - 12) - (24 - hco3)
        if delta_gap > 6: st.success(f"➕ DELTA GAP ({delta_gap:.1f}): ALCALOSIS METABÓLICA ASOCIADA")
        elif delta_gap < -6: st.info(f"➕ DELTA GAP ({delta_gap:.1f}): ACIDOSIS NO GAP ASOCIADA")

# C. OXIGENACIÓN
st.subheader("3. Oxigenación (Bogotá 2600m)")
c1, c2, c3, c4 = st.columns(4)
pafi, safi = pa02/fio2, spo2/fio2
rox = safi/fr

def color_sdra(v):
    if v < 100: return "🔴 SEVERO"
    if v < 200: return "🟠 MODERADO"
    return "🟡 LEVE" if v < 300 else "🟢 NORMAL"

c1.metric("PAFI", f"{pafi:.0f}", color_sdra(pafi))
c2.metric("SAFI", f"{safi:.0f}", color_sdra(safi))
c3.metric("ROX INDEX", f"{rox:.2f}", "Riesgo VNI" if rox < 4.88 else "Estable")
c4.metric("Gradiente A-a", f"{g_real:.1f}")

if g_real > (g_id + 10):
    st.error(f"DIAGNÓSTICO: LESIÓN INTRAPULMONAR (Gradiente {g_real:.1f} > Ideal {g_id:.1f})")
    with st.expander("🔍 LAS 7 CAUSAS DE HIPOXEMIA"):
        st.write("1. Altura | 2. Hipoventilación | 3. Shunt | 4. V/Q | 5. Difusión | 6. ↓Gasto | 7. Hb anómala")
else:
    st.success("DIAGNÓSTICO: PULMÓN SANO (Causa Extrapulmonar / Hipoventilación)")

st.caption("Gases 2600 PRO - Dr. Gonzalo Bernal Ferreira")

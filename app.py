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
st.set_page_config(page_title="Gases 2600 PRO v4", layout="wide")
st.markdown("<h1 style='text-align: center;'>🫁 Gases Arteriales 2600 PRO</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Dr. Gonzalo Bernal Ferreira</h3>", unsafe_allow_html=True)

# --- 3. ENTRADA DE DATOS ---
with st.sidebar:
    st.header("⌨️ Parámetros Clínicos")
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

# --- 4. CÁLCULOS LÓGICOS ---
h_ion = 24 * (pco2 / hco3)
r80 = 80 - float(f"{ph:.2f}"[-2:])
ag_c = (na - (cl + hco3)) + (2.5 * (4 - alb))
pao2_calc = (fio2 * 513) - (pco2 / 0.8) # Fórmula Bogotá
g_real = max(0, pao2_calc - pa02)
g_id = (edad / 4) + 4
pafi = pa02 / fio2
safi = spo2 / fio2
rox = (safi / fr) if fr > 0 else 0

# --- 5. INTERFAZ DE RESULTADOS ---

# A. CONSISTENCIA
st.subheader("1. Evaluación de Consistencia")
if 0.7 <= (h_ion / r80) <= 1.2:
    st.success(f"✅ MUESTRA VÁLIDA: H+ calculado ({h_ion:.1f}) es congruente con el pH.")
else:
    st.error(f"❌ MUESTRA NO CONFIABLE: H+ ({h_ion:.1f}) no coincide con el pH medido.")

# B. DIAGNÓSTICO ÁCIDO-BASE
st.subheader("2. Análisis Ácido-Base")

# --- BLOQUE RESPIRATORIO ---
if (ph < 7.35 and pco2 > 32) or (ph > 7.45 and pco2 < 28):
    tipo_resp = "ACIDOSIS" if pco2 > 32 else "ALCALOSIS"
    st.error(f"🚨 TRASTORNO RESPIRATORIO: {tipo_resp} RESPIRATORIA")
    with st.expander(f"➕ VER CAUSAS {tipo_resp} RESPIRATORIA (VITAMINS)", expanded=True):
        st.write("**V:** Vascular (ACV, TEP) | **I:** Infección (Sepsis, Neumonía)")
        st.write("**T:** Toxinas/Trauma (Opioides, BZD, Trauma Tórax) | **A:** Autoimmune (Miastenia, GB)")
        st.write("**M:** Metabólico (Hipopotasemia) | **I:** Iatrogenia (Mal ajuste VM)")
        st.write("**N:** Neoplasia (Tumores SNC) | **S:** SNC / Sueño (Apnea, Hipoventilación)")

# --- BLOQUE METABÓLICO ---
if (ph < 7.35 and hco3 < 19) or (ph > 7.45 and hco3 > 24):
    tipo_meta = "ACIDOSIS" if hco3 < 19 else "ALCALOSIS"
    st.warning(f"🚨 TRASTORNO METABÓLICO: {tipo_meta} METABÓLICA")
    
    if hco3 < 19: # Si es acidosis metabólica, desglosar AG y Delta
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Anión Gap Corregido", f"{ag_c:.1f}")
            if ag_c > 12:
                with st.expander("🔍 CAUSAS ANION GAP (GOLDMARCC)", expanded=True):
                    st.write("**G:** Glicoles | **O:** Oxiprolina | **L:** Lactato | **D:** D-Lactato")
                    st.write("**M:** Metanol | **A:** Aspirina | **R:** Renal/Rabdo | **C:** Cetoacidosis | **C:** Creatinina")
        with c2:
            delta_gap = (ag_c - 12) - (24 - hco3)
            st.metric("Delta Gap", f"{delta_gap:.1f}")
            if delta_gap > 6: st.success("🔍 ALCALOSIS METABÓLICA ASOCIADA")
            elif delta_gap < -6: st.info("🔍 ACIDOSIS NO GAP ASOCIADA")

# C. OXIGENACIÓN
st.subheader("3. Perfil de Oxigenación (Bogotá 2600m)")
def color_berlin(v):
    if v < 100: return "🔴 SEVERO"
    if v < 200: return "🟠 MODERADO"
    return "🟡 LEVE" if v < 300 else "🟢 NORMAL"

o1, o2, o3, o4 = st.columns(4)
o1.metric("PAFI", f"{pafi:.0f}", color_berlin(pafi))
o2.metric("SAFI", f"{safi:.0f}", color_berlin(safi))
o3.metric("ROX INDEX", f"{rox:.2f}", "Riesgo VNI" if rox < 4.88 else "Estable")
o4.metric("Gradiente A-a", f"{g_real:.1f}")

if g_real > (g_id + 10):
    st.error(f"DIAGNÓSTICO: LESIÓN INTRAPULMONAR (Gradiente {g_real:.1f} > Ideal {g_id:.1f})")
    with st.expander("🔍 LAS 7 CAUSAS DE HIPOXEMIA", expanded=False):
        st.write("1. Altura | 2. Hipoventilación | 3. Shunt | 4. V/Q desigual | 5. Difusión | 6. ↓Gasto | 7. Hb anómala")
else:
    st.success(f"DIAGNÓSTICO: PULMÓN SANO (Gradiente {g_real:.1f} acorde a edad). Causa es Extrapulmonar.")

st.caption("Gases 2600 PRO v4 - Dr. Gonzalo Bernal Ferreira")

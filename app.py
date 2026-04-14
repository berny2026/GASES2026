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
st.set_page_config(page_title="Gases 2600 PRO", layout="wide")
st.markdown("<h1 style='text-align: center;'>🫁 Gases Arteriales 2600 PRO</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Dr. Gonzalo Bernal Ferreira</h3>", unsafe_allow_html=True)

# --- 3. ENTRADA DE DATOS ---
with st.sidebar:
    st.header("⌨️ Parámetros")
    ph = st.number_input("pH Arterial", 6.80, 7.80, 7.20, 0.01)
    pco2 = st.number_input("PaCO2 (mmHg)", 10.0, 90.0, 40.0, 0.1)
    hco3 = st.number_input("HCO3 (mEq/L)", 5.0, 50.0, 15.0, 0.1)
    st.divider()
    na = st.number_input("Sodio (Na)", 110.0, 170.0, 145.0, 0.1)
    cl = st.number_input("Cloro (Cl)", 70.0, 130.0, 95.0, 0.1)
    alb = st.number_input("Albúmina (g/dL)", 1.0, 5.0, 4.0, 0.1)
    st.divider()
    pa02 = st.number_input("PaO2 (mmHg)", 20.0, 200.0, 55.0, 0.1)
    spo2 = st.number_input("SpO2 (%)", 40, 100, 88)
    fio2 = st.number_input("FiO2 (decimal)", 0.21, 1.00, 0.21, 0.01)
    edad = st.number_input("Edad (años)", 0, 115, 50)
    fr = st.number_input("FR (resp/min)", 5, 60, 28)

# --- 4. CÁLCULOS ---
h_ion = 24 * (pco2 / hco3)
r80 = 80 - float(f"{ph:.2f}"[-2:])
ag_c = (na - (cl + hco3)) + (2.5 * (4 - alb))
win = (1.5 * hco3) + 8
pao2_calc = (fio2 * 513) - (pco2 / 0.8)
g_real = pao2_calc - pa02
g_id = (edad / 4) + 4
pafi = pa02 / fio2
safi = spo2 / fio2

# --- 5. RESULTADOS ---

# A. CONSISTENCIA
st.subheader("1. Consistencia Interna")
if 0.7 <= (h_ion / r80) <= 1.2:
    st.success(f"✅ MUESTRA VÁLIDA: H+ calculado ({h_ion:.1f}) correlaciona con pH.")
else:
    st.error(f"❌ MUESTRA NO CONFIABLE: H+ ({h_ion:.1f}) no coincide con pH. ¿Error de laboratorio?")

# B. TRASTORNOS METABÓLICOS
st.subheader("2. Análisis Ácido-Base")
col1, col2 = st.columns(2)

with col1:
    if ph < 7.35:
        st.error(f"🚨 ACIDEMIA METABÓLICA (HCO3: {hco3})")
        st.write(f"**Compensación:** PaCO2 esperada (Winters) es **{win:.1f} ± 2**")
        if pco2 > win + 2:
            st.warning("⚠️ TRASTORNO MIXTO: ACIDOSIS RESPIRATORIA SOBREAGREGADA")
            st.info("**Causas (VITAMINS):** Vascular (ACV), Infección (Sepsis), Toxinas (Opioides), Autoimmune, Metabólico, Neoplasia, S (SNC/Trauma).")
        
        if ag_c > 12:
            with st.expander("🔍 CAUSAS ANION GAP ELEVADO (GOLDMARCC)", expanded=True):
                st.write("**G:** Glicoles (Etileno/Propileno)")
                st.write("**O:** Oxiprolina (Paracetamol crónico)")
                st.write("**L:** L-Lactato (Sepsis/Hipoxia)")
                st.write("**D:** D-Lactato (Intestino corto)")
                st.write("**M:** Metanol")
                st.write("**A:** Aspirina (Salicilatos)")
                st.write("**R:** Rabdomiólisis / Renal (Falla)")
                st.write("**C:** Cetoacidosis (Diabética/Alcohólica)")
                st.write("**C:** Creatinina (Uremia elevada)")

with col2:
    delta_gap = (ag_c - 12) - (24 - hco3)
    if ag_c > 12 and delta_gap > 6:
        st.success(f"➕ ALCALOSIS METABÓLICA ASOCIADA (Delta Gap: {delta_gap:.1f})")
        st.write("**Causas:** Vómitos, diuréticos, succión nasogástrica.")

# C. OXIGENACIÓN
st.subheader("3. Oxigenación y Mecánica")
c_ox1, c_ox2, c_ox3 = st.columns(3)

def clasificar_sdra(valor):
    if valor < 100: return "🔴 SEVERO"
    if valor < 200: return "🟠 MODERADO"
    if valor < 300: return "🟡 LEVE"
    return "🟢 NORMAL"

with c_ox1:
    st.metric("PAFI", f"{pafi:.0f}", clasificar_sdra(pafi))
with c_ox2:
    st.metric("SAFI", f"{safi:.0f}", clasificar_sdra(safi))
with c_ox3:
    rox = (safi/fr)
    st.metric("ROX INDEX", f"{rox:.2f}", "Riesgo VNI" if rox < 4.88 else "Seguro")

if g_real > (g_id + 10):
    st.error(f"DIAGNÓSTICO: LESIÓN INTRAPULMONAR (Gradiente {g_real:.1f} > Ideal {g_id:.1f})")
    st.write("**7 Causas de Hipoxemia:** 1. ↓ PiO2 (Altura), 2. Hipoventilación, 3. Shunt, 4. V/Q desigual, 5. Difusión, 6. ↓ Sat Venosa, 7. Hb anómala.")
else:
    st.success(f"DIAGNÓSTICO: PULMÓN SANO (Gradiente {g_real:.1f} acorde a edad). Causa es Extrapulmonar.")

st.caption("Gases 2600 PRO - Dr. Gonzalo Bernal Ferreira")

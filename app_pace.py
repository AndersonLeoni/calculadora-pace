import streamlit as st

st.set_page_config(page_title="Calculadora de Pace", layout="centered")

st.markdown("""
    <style>
        /* Estilo base do botão */
        .stButton button {
            background-color: #0066cc;
            color: white !important;
            padding: 0.6em 1.5em;
            font-size: 18px;
            border-radius: 8px;
            font-weight: 600;
            border: none;
            transition: background-color 0.3s ease, color 0.3s ease;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        /* Hover do botão */
        .stButton button:hover {
            background-color: #0052a3;
            color: white !important;
        }

        /* Responsividade para fontes pequenas */
        @media (max-width: 600px) {
            .stButton button {
                font-size: 16px;
                padding: 0.5em 1em;
            }
        }

        /* Estilo de título */
        .main h1 {
            font-size: 2em;
            font-weight: bold;
            color: #003366;
        }

        /* Estilo dos inputs */
        input {
            border: 1px solid #ccc;
            border-radius: 6px;
            padding: 0.5em;
            font-size: 16px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🏃‍♂️ Calculadora de Pace e Velocidade")

aba = st.tabs(["📟 Calculadora", "🔁 Conversor"])

# ----------------------------
# ABA 1 - Calculadora de Pace
# ----------------------------
with aba[0]:
    st.markdown("### ⏱️ Calcule seu *pace* com base no tempo e distância")

    col1, col2, col3 = st.columns(3)
    with col1:
        horas = st.number_input("Horas", min_value=0, step=1, value=0)
    with col2:
        minutos = st.number_input("Minutos", min_value=0, max_value=59, step=1, value=0)
    with col3:
        segundos = st.number_input("Segundos", min_value=0, max_value=59, step=1, value=0)

    distancia = st.number_input("Distância (em km)", min_value=0.1, step=0.1, value=5.0)

    def calcular_pace(h, m, s, d):
        total_segundos = h * 3600 + m * 60 + s
        if d == 0:
            return None
        pace_seg = total_segundos / d
        pace_min = int(pace_seg // 60)
        pace_sec_restante = int(pace_seg % 60)
        velocidade = round(3600 / pace_seg, 2)
        return pace_min, pace_sec_restante, velocidade

    if st.button("📊 Calcular Pace"):
        resultado = calcular_pace(horas, minutos, segundos, distancia)
        if resultado:
            st.success(f"🧮 **Pace:** `{resultado[0]}:{resultado[1]:02d} min/km`")
            st.info(f"🚀 **Velocidade:** `{resultado[2]} km/h`")
        else:
            st.error("❌ A distância deve ser maior que zero.")

# ----------------------------
# ABA 2 - Conversor de Pace
# ----------------------------
with aba[1]:
    st.markdown("### 🔁 Converter Pace para Velocidade (km/h)")

    col1, col2 = st.columns(2)
    with col1:
        pace_min = st.number_input("Minutos por km", min_value=0, value=7)
    with col2:
        pace_sec = st.number_input("Segundos por km", min_value=0, max_value=59, value=0)

    def pace_para_kmh(mins, secs):
        total_min = mins + secs / 60
        if total_min == 0:
            return None
        return round(60 / total_min, 2)

    if st.button("🔄 Converter Pace"):
        velocidade = pace_para_kmh(pace_min, pace_sec)
        if velocidade:
            st.success(f"🚀 **Velocidade:** `{velocidade} km/h`")
        else:
            st.error("❌ O tempo deve ser maior que zero.")

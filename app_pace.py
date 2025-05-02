import streamlit as st

# ----- CSS MODERNO + MOBILE FIRST -----
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Segoe UI', sans-serif;
            font-size: 18px;
            color: #222;
            background-color: #f5f5f5;
        }

        .stButton button {
            width: 100%;
            background-color: #0066cc;
            color: white !important;
            padding: 1em;
            font-size: 1.1rem;
            border-radius: 8px;
            font-weight: 600;
            border: none;
            transition: background-color 0.3s ease;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        .stButton button:hover {
            background-color: #0052a3;
            color: white !important;
        }

        .stTextInput > div > div > input {
            padding: 0.75em;
            border-radius: 6px;
            font-size: 1.1rem;
        }

        .resultado {
            background-color: #003366;
            color: #ffffff;
            font-size: 2.4rem;
            font-weight: bold;
            text-align: center;
            padding: 1.5rem;
            border-radius: 10px;
            margin-top: 1.5rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }

        @media (min-width: 768px) {
            html, body, [class*="css"] {
                font-size: 17px;
            }

            .stButton button {
                font-size: 18px;
                width: auto;
                padding: 0.75em 2em;
            }

            .resultado {
                font-size: 2rem;
                padding: 1rem;
            }
        }
    </style>
""", unsafe_allow_html=True)

# ----- APP -----
st.title("🏃 Calculadora de Pace")

abas = st.tabs(["📏 Calcular Pace", "⚡ Converter Pace para km/h"])

# --- ABA 1: Calcular Pace + Velocidade ---
with abas[0]:
    st.subheader("Informe os dados do seu treino")

    tempo = st.time_input("Tempo total", value=None)
    distancia = st.number_input("Distância (em km)", min_value=0.01, format="%.2f")

    if st.button("Calcular Pace"):
        if tempo and distancia > 0:
            segundos_totais = tempo.hour * 3600 + tempo.minute * 60 + tempo.second
            pace_segundos = int(segundos_totais / distancia)
            minutos = pace_segundos // 60
            segundos = pace_segundos % 60
            pace_formatado = f"{minutos:02d}:{segundos:02d} min/km"
            km_h = round(3600 / pace_segundos, 2)
            
            st.markdown(f'''
                <div class="resultado">
                    Pace: {pace_formatado}<br>
                    Velocidade: {km_h} km/h
                </div>
            ''', unsafe_allow_html=True)
        else:
            st.warning("Por favor, preencha todos os campos corretamente.")

# --- ABA 2: Converter Pace para km/h ---
with abas[1]:
    st.subheader("Digite o pace (min/km) para converter em km/h")

    col1, col2 = st.columns(2)
    with col1:
        min_pace = st.number_input("Minutos", min_value=0, step=1)
    with col2:
        seg_pace = st.number_input("Segundos", min_value=0, max_value=59, step=1)

    if st.button("Converter para km/h"):
        total_min = min_pace + seg_pace / 60
        if total_min > 0:
            km_h = round(60 / total_min, 2)
            st.markdown(f'<div class="resultado">{km_h} km/h</div>', unsafe_allow_html=True)
        else:
            st.warning("Informe um pace válido.")

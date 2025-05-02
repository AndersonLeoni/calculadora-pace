import streamlit as st

# CSS MOBILE FIRST
st.markdown("""
    <style>
        /* RESET e mobile first */
       html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
        font-size: 18px; /* Aumentado de 16px para 18px no mobile */
        color: #222;
    }

    .stButton button {
        width: 100%;
        background-color: #0066cc;
        color: white !important;
        padding: 1em;
        font-size: 1.1rem; /* texto maior no botão */
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

    .big-font {
        font-size: 2.2rem;
        font-weight: bold;
        color: #003366;
        margin-bottom: 1rem;
    }

    @media (min-width: 768px) {
        html, body, [class*="css"] {
            font-size: 17px; /* volta para tamanho padrão em telas maiores */
        }

        .stButton button {
            font-size: 18px;
            width: auto;
            padding: 0.75em 2em;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Título
st.markdown('<div class="big-font">Calculadora de Pace e Velocidade</div>', unsafe_allow_html=True)

# Abas de navegação
aba = st.radio("Escolha a função:", ["Calcular Pace", "Converter Pace para Km/h"], horizontal=True)

# Função 1: Calcular Pace
if aba == "Calcular Pace":
    tempo_min = st.number_input("Minutos", min_value=0, step=1, format="%d")
    tempo_seg = st.number_input("Segundos", min_value=0, max_value=59, step=1, format="%d")
    distancia = st.number_input("Distância (km)", min_value=0.1, step=0.1, format="%.1f")
    
    if st.button("Calcular Pace"):
        tempo_total_segundos = tempo_min * 60 + tempo_seg
        pace = tempo_total_segundos / distancia
        pace_min = int(pace // 60)
        pace_seg = int(pace % 60)
        st.success(f"Pace: {pace_min:02d}:{pace_seg:02d} por km")

# Função 2: Converter Pace para Km/h
elif aba == "Converter Pace para Km/h":
    pace_min = st.number_input("Minutos por km", min_value=0, step=1, format="%d", key="min")
    pace_seg = st.number_input("Segundos por km", min_value=0, max_value=59, step=1, format="%d", key="seg")
    
    if st.button("Converter para km/h"):
        pace_total = pace_min * 60 + pace_seg
        if pace_total > 0:
            velocidade = 3600 / pace_total
            st.success(f"Velocidade: {velocidade:.2f} km/h")
        else:
            st.warning("O pace deve ser maior que 00:00.")

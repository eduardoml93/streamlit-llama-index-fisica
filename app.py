import streamlit as st
from llama_index.llms.groq import Groq
import base64

# 🚀 Configuração da página
st.set_page_config(page_title="Assistente de Tópicos de Física", layout="wide")

# ----------------------------
# Funções para background
# ----------------------------
def get_base64_of_image(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

def set_background(image_file="bg.jpg", darkness=0.5):
    base64_str = get_base64_of_image(image_file)
    css = f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0,{darkness}), rgba(0,0,0,{darkness})), 
                          url("data:image/jpeg;base64,{base64_str}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .title-box {{
        background: rgba(0, 0, 0, 0.3);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-size: 28px;
        font-weight: bold;
        width: 70%;
        margin: auto;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ----------------------------
# Dicionário de Tópicos de Física (PT-BR)
# ----------------------------
TOPICS_PHYSICS = {
    "1": [
        "Introdução à Física", "Grandezas físicas e unidades", "Notação científica",
        "Medição e incerteza", "Vetores e escalares", 
        "Movimento em uma dimensão", "Velocidade, rapidez e aceleração",
        "Gráficos de movimento", "Leis de Newton (visão geral)",
        "Forças e diagramas de corpo livre", "Massa e peso", "Atrito",
        "Trabalho e energia", "Energia cinética e potencial", "Potência",
        "Lei da conservação da energia", "Máquinas simples e eficiência",
        "Densidade e pressão", "Lei de Hooke e elasticidade",
        "Movimento circular (básico)", "Quantidade de movimento linear e impulso",
        "Colisões (elásticas e inelásticas)", "Gravidade (conceito introdutório)"
    ],
    "2": [
        "Leis de Newton em detalhe", "Aplicações das leis de Newton",
        "Lançamento oblíquo", "Movimento circular uniforme",
        "Teorema trabalho-energia", "Conservação da quantidade de movimento",
        "Movimento rotacional", "Torque e momento angular",
        "Equilíbrio de corpos rígidos", "Movimento harmônico simples",
        "Ondas mecânicas", "Ondas sonoras e ressonância",
        "Dilatação térmica", "Temperatura e transferência de calor",
        "Calor específico", "Mudança de estado físico e calor latente",
        "Leis da termodinâmica", "Máquinas térmicas e eficiência",
        "Lei dos gases ideais", "Teoria cinética dos gases"
    ],
    "3": [
        "Carga elétrica e campo elétrico", "Lei de Coulomb",
        "Potencial elétrico e energia potencial elétrica", "Capacitância e dielétricos",
        "Corrente, tensão e resistência", "Lei de Ohm e circuitos elétricos",
        "Leis de Kirchhoff", "Potência e energia elétrica",
        "Magnetismo e campos magnéticos", "Indução eletromagnética",
        "Lei de Faraday e Lei de Lenz", "Corrente alternada (CA) e corrente contínua (CC)",
        "Transformadores e transmissão de energia", "Ondas eletromagnéticas",
        "A luz como onda", "Reflexão e refração", 
        "Lentes e espelhos", "Interferência e difração",
        "Polarização", "Efeito Doppler"
    ],
    "4": [
        "Teoria quântica e fótons", "Efeito fotoelétrico",
        "Dualidade onda-partícula", "Modelos atômicos (Bohr e posteriores)",
        "Níveis de energia e espectros", "Estrutura nuclear e radioatividade",
        "Meia-vida e decaimento nuclear", "Fissão e fusão nuclear",
        "Relatividade (restrita e geral)", "Dilatação do tempo e contração do espaço",
        "Equivalência massa-energia (E = mc²)", "Forças fundamentais da natureza",
        "Física de partículas e Modelo Padrão", "Partículas subatômicas",
        "Cosmologia e teoria do Big Bang", "Buracos negros e curvatura do espaço-tempo",
        "Semicondutores e eletrônica moderna", "Supercondutividade",
        "Aplicações da física na tecnologia", "Energia renovável e sustentabilidade"
    ]
}

# ----------------------------
# Função para gerar explicação
# ----------------------------
def explicar_topico(topico):
    if not topico:
        return "Por favor, insira um tópico de Física."

    prompt = f"""
Você é um professor de Física experiente. Explique detalhadamente o seguinte tópico de Física: "{topico}".

Use o seguinte formato na resposta:

1. **Conceito fundamental e teoria**
2. **Fórmulas principais e explicação**
3. **Exemplos práticos e aplicações**
4. **Observações e dicas importantes**
5. **Exercícios resolvidos de exemplo**

Use Markdown e LaTeX para formatar títulos, listas e fórmulas matemáticas.
"""
    try:
        resposta = st.session_state.llm.complete(prompt)
        if not resposta:
            return "Não foi possível gerar a resposta. Tente novamente."
        return resposta
    except Exception as e:
        return f"Erro ao processar a pergunta: {e}"

# ----------------------------
# Interface
# ----------------------------
set_background("bg.jpg", darkness=0.8)  # controle escuro/claro do BG

# Inicializa sessão
if "api_key" not in st.session_state:
    st.session_state.api_key = None
    st.session_state.llm = None

# Página 1: Login
if not st.session_state.api_key:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("🔑 Login para Assistente de Física")

        st.markdown(
            """
            Para gerar sua **API Key da Groq**, acesse:  
            👉 [https://console.groq.com/keys](https://console.groq.com/keys)
            """,
            unsafe_allow_html=True,
        )
        api_key_input = st.text_input("Insira sua API Key da Groq:", type="password")
        if st.button("Entrar"):
            if api_key_input.strip():
                try:
                    llm = Groq(model="llama-3.1-8b-instant", api_key=api_key_input.strip())
                    _ = llm.complete("Teste rápido.")
                    st.session_state.api_key = api_key_input.strip()
                    st.session_state.llm = llm
                    st.success("✅ Login realizado com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao validar a chave: {e}")
            else:
                st.warning("⚠️ Digite sua chave de API para continuar.")

# Página 2: Aplicação principal
else:
    st.markdown('<div class="title-box">⚛️ Assistente de Tópicos de Física</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.subheader("Selecione o nível e o tópico desejado:")

        nivel = st.selectbox("Nível", options=["1", "2", "3", "4"], format_func=lambda x: f"Física {x}")
        topico = st.selectbox("Tópico", options=TOPICS_PHYSICS[nivel])

        if st.button("📘 Explicar Tópico"):
            with st.spinner("Gerando explicação detalhada..."):
                resposta = explicar_topico(topico)
                st.markdown(resposta, unsafe_allow_html=True)

        if st.button("🚪 Sair"):
            st.session_state.api_key = None
            st.session_state.llm = None
            st.rerun()

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
# Funções do app
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
set_background("bg.jpg", darkness=0.5)

# Inicializa sessão
if "api_key" not in st.session_state:
    st.session_state.api_key = None
    st.session_state.llm = None

# Página 1: Login
if not st.session_state.api_key:
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
                # Testa o LLM antes de liberar
                llm = Groq(model="llama-3.1-8b-instant", api_key=api_key_input.strip())
                _ = llm.complete("Teste rápido.")
                st.session_state.api_key = api_key_input.strip()
                st.session_state.llm = llm
                st.success("✅ Login realizado com sucesso!")
                st.rerun()   # 🔄 Atualiza a tela
            except Exception as e:
                st.error(f"Erro ao validar a chave: {e}")
        else:
            st.warning("⚠️ Digite sua chave de API para continuar.")

# Página 2: Aplicação principal
else:
    col1, col2, col3 = st.columns([1, 1.7, 1]) 

    with col2:
        st.title("⚛️ Assistente de Tópicos de Física")  
        topico = st.text_input(
            "Insira o tópico de Física", 
            placeholder="Ex: Lei da Gravitação Universal"
        )

        if st.button("Explicar"):
            with st.spinner("Gerando explicação..."):
                resposta = explicar_topico(topico)
                st.markdown(resposta, unsafe_allow_html=True)

    # Botão de logout
    if st.button("🚪 Sair"):
        st.session_state.api_key = None
        st.session_state.llm = None
        st.rerun()   # 🔄 Atualiza a tela

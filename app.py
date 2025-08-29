import streamlit as st
from llama_index.llms.groq import Groq
import base64

# 🚀 Configuração da página (primeiro comando Streamlit)
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

# 🔑 Coloque sua chave aqui
key = "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"
llm = Groq(model="llama3-70b-8192", api_key=key)

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
        resposta = llm.complete(prompt)
        if not resposta:  # Caso venha None ou string vazia
            return "Não foi possível gerar a resposta. Tente novamente."
        return resposta
    except Exception as e:
        return f"Erro ao processar a pergunta: {e}"

# 🚀 Interface Streamlit
set_background("bg.jpg", darkness=0.5)  # <- aplica fundo
st.title("⚛️ Assistente de Tópicos de Física")

# Cria 3 colunas (esquerda, centro, direita)
col1, col2, col3 = st.columns([2, 1, 2]) 

with col1:  
    topico = st.text_input(
        "Insira o tópico de Física", 
        placeholder="Ex: Lei da Gravitação Universal"
    )

if st.button("Explicar"):
    with st.spinner("Gerando explicação..."):
        resposta = explicar_topico(topico)
        st.markdown(resposta, unsafe_allow_html=True)  # Markdown + LaTeX renderizado

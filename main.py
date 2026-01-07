import streamlit as st
from utils import (
    calcular_juros_compostos,
    calcular_emprestimo,
    calcular_aposentadoria,
    calcular_fire
)

# Configuração da página
st.set_page_config(
    page_title="Calculadora Financeira Completa",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<h1 class="main-header">💰 Calculadora Financeira Completa</h1>', unsafe_allow_html=True)

# Sidebar para seleção de calculadora
st.sidebar.title("📊 Menu")
calculadora = st.sidebar.selectbox(
    "Escolha a Calculadora:",
    ["Juros Compostos", "Empréstimos e Financiamentos", "Planejamento de Aposentadoria", "Calculadora FI/RE"]
)

# Roteamento para as calculadoras
if calculadora == "Juros Compostos":
    calcular_juros_compostos()
elif calculadora == "Empréstimos e Financiamentos":
    calcular_emprestimo()
elif calculadora == "Planejamento de Aposentadoria":
    calcular_aposentadoria()
else:  
    calcular_fire()

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem 0;'>
        <p style='font-size: 0.8rem;'>⚠️ Esta ferramenta é apenas para fins educacionais. Consulte um profissional certificado para decisões financeiras importantes. ⚠️</p>
    </div>
""", unsafe_allow_html=True)
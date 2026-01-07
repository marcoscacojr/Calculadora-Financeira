# Calculadora-Financeira
Uma aplicação web interativa desenvolvida em Python com Streamlit para auxiliar no planejamento financeiro pessoal.

# 💰 Calculadora Financeira Completa

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Ativo-success.svg)

Uma aplicação web interativa desenvolvida em Python com Streamlit para auxiliar no planejamento financeiro pessoal, oferecendo 4 calculadoras especializadas com visualizações gráficas avançadas.

[Sobre](#-sobre) • [Funcionalidades](#-funcionalidades) • [Tecnologias](#-tecnologias) • [Instalação](#-instalação) • [Uso](#-como-usar) • [Screenshots](#-screenshots) • [Contribuindo](#-contribuindo)

</div>

---

## 📋 Sobre

Esta aplicação foi desenvolvida para democratizar o acesso a ferramentas de planejamento financeiro, permitindo que qualquer pessoa possa simular cenários de investimentos, empréstimos, aposentadoria e independência financeira de forma visual e intuitiva.

O projeto utiliza cálculos financeiros precisos e apresenta os resultados através de gráficos interativos, tabelas detalhadas e métricas relevantes para tomada de decisão.

## ✨ Funcionalidades

### 📈 Calculadora de Juros Compostos
- Simulação de investimentos com aportes mensais
- Visualização da evolução do patrimônio ao longo do tempo
- Ajuste pela inflação (valor real vs. nominal)
- Tipos de aporte: início ou fim do mês
- Gráficos de composição e evolução patrimonial
- Identificação de marcos financeiros importantes

**Ideal para:** Planejamento de investimentos de longo prazo, simulação de fundos de emergência

### 🏠 Calculadora de Empréstimos e Financiamentos
- Suporte para sistemas **PRICE** (parcelas fixas) e **SAC** (amortização constante)
- Análise detalhada de juros, amortização e saldo devedor
- Comparação visual entre diferentes sistemas
- Tabela completa de parcelas
- Gráficos de evolução das parcelas e saldo devedor

**Ideal para:** Financiamento imobiliário, empréstimos pessoais, análise de diferentes cenários

### 👴 Planejamento de Aposentadoria
- Cálculo do patrimônio necessário para aposentadoria
- Simulação de fases de acumulação e usufruto
- Análise de viabilidade do plano atual
- Sugestões personalizadas de ajustes
- Projeção de renda mensal sustentável
- Consideração de inflação e diferentes taxas de retorno

**Ideal para:** Planejamento de longo prazo, análise de previdência privada

### 🔥 Calculadora FI/RE (Financial Independence / Retire Early)
- Cálculo baseado na Regra dos 4%
- Análise da taxa de poupança atual
- Projeção de tempo até independência financeira
- Níveis de FI: Lean FI, Flex FI, FI, Fat FI, Obese FI
- Análise de sensibilidade com diferentes cenários
- Ajuste automático pela inflação
- Acompanhamento do progresso em tempo real

**Ideal para:** Quem busca aposentadoria precoce, otimização de gastos e investimentos

## 🛠 Tecnologias

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Python** | 3.8+ | Linguagem base |
| **Streamlit** | 1.31.0 | Framework web interativo |
| **Pandas** | 2.1.4 | Manipulação de dados |
| **NumPy** | 1.26.3 | Cálculos matemáticos |
| **Plotly** | 5.18.0 | Visualizações interativas |

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a passo

1. **Clone o repositório**
```bash
git clone https://github.com/marcoscacojr/Calculadora-Financeira.git
cd Calculadora-Financeira

2. **Crie um ambiente virtual**
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate

3. **Instale as dependências**
pip install -r requirements.txt

4. **Execute a aplicação**
streamlit run main.py
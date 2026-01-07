import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def calcular_emprestimo():
    """Calculadora de Empréstimos e Financiamentos"""
    st.header("🏠 Calculadora de Empréstimos e Financiamentos")
    st.markdown("Analise parcelas, juros e compare diferentes cenários")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Dados do Financiamento")
        valor_emprestimo = st.number_input("Valor do Empréstimo (R$)", min_value=0.0, value=200000.0, step=1000.0)
        taxa_juros_anual = st.number_input("Taxa de Juros Anual (%)", min_value=0.0, value=9.0, step=0.1)
        prazo_anos = st.slider("Prazo (anos)", min_value=1, max_value=35, value=20)
        
    with col2:
        st.subheader("Opções")
        sistema = st.radio("Sistema de Amortização", ["PRICE (Parcelas Fixas)", "SAC (Amortização Constante)"])
        entrada = st.number_input("Entrada (R$)", min_value=0.0, value=0.0, step=1000.0)
        
    # Cálculos
    valor_financiado = valor_emprestimo - entrada
    taxa_mensal = taxa_juros_anual / 12 / 100
    num_parcelas = prazo_anos * 12
    
    parcelas_data = []
    
    if sistema == "PRICE (Parcelas Fixas)":
        # Sistema PRICE
        if taxa_mensal > 0:
            parcela = valor_financiado * (taxa_mensal * (1 + taxa_mensal) ** num_parcelas) / ((1 + taxa_mensal) ** num_parcelas - 1)
        else:
            parcela = valor_financiado / num_parcelas
        
        saldo_devedor = valor_financiado
        
        for i in range(1, int(num_parcelas) + 1):
            juros = saldo_devedor * taxa_mensal
            amortizacao = parcela - juros
            saldo_devedor -= amortizacao
            
            parcelas_data.append({
                'Parcela': i,
                'Valor Parcela': parcela,
                'Juros': juros,
                'Amortização': amortizacao,
                'Saldo Devedor': max(0, saldo_devedor)
            })
    
    else:  # SAC
        amortizacao = valor_financiado / num_parcelas
        saldo_devedor = valor_financiado
        
        for i in range(1, int(num_parcelas) + 1):
            juros = saldo_devedor * taxa_mensal
            parcela = amortizacao + juros
            saldo_devedor -= amortizacao
            
            parcelas_data.append({
                'Parcela': i,
                'Valor Parcela': parcela,
                'Juros': juros,
                'Amortização': amortizacao,
                'Saldo Devedor': max(0, saldo_devedor)
            })
    
    df_parcelas = pd.DataFrame(parcelas_data)
    
    # Métricas
    st.subheader("📊 Resumo do Financiamento")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Primeira Parcela", f"R$ {df_parcelas['Valor Parcela'].iloc[0]:,.2f}")
    with col2:
        st.metric("Última Parcela", f"R$ {df_parcelas['Valor Parcela'].iloc[-1]:,.2f}")
    with col3:
        total_pago = df_parcelas['Valor Parcela'].sum()
        st.metric("Total a Pagar", f"R$ {total_pago:,.2f}")
    with col4:
        total_juros = df_parcelas['Juros'].sum()
        st.metric("Total de Juros", f"R$ {total_juros:,.2f}")
    
    # Gráfico de evolução das parcelas
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_parcelas['Parcela'],
        y=df_parcelas['Valor Parcela'],
        name='Valor da Parcela',
        line=dict(color='#1f77b4', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=df_parcelas['Parcela'],
        y=df_parcelas['Juros'],
        name='Juros',
        fill='tonexty',
        line=dict(color='#d62728')
    ))
    
    fig.add_trace(go.Scatter(
        x=df_parcelas['Parcela'],
        y=df_parcelas['Amortização'],
        name='Amortização',
        fill='tozeroy',
        line=dict(color='#2ca02c')
    ))
    
    fig.update_layout(
        title='Composição das Parcelas ao Longo do Tempo',
        xaxis_title='Número da Parcela',
        yaxis_title='Valor (R$)',
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico de saldo devedor
    fig2 = go.Figure()
    
    fig2.add_trace(go.Scatter(
        x=df_parcelas['Parcela'],
        y=df_parcelas['Saldo Devedor'],
        fill='tozeroy',
        line=dict(color='#ff7f0e', width=3)
    ))
    
    fig2.update_layout(
        title='Evolução do Saldo Devedor',
        xaxis_title='Número da Parcela',
        yaxis_title='Saldo Devedor (R$)',
        height=400
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Tabela de parcelas (primeiras e últimas)
    st.subheader("📋 Detalhamento das Parcelas")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Primeiras 12 Parcelas**")
        st.dataframe(df_parcelas.head(12).style.format({
            'Valor Parcela': 'R$ {:,.2f}',
            'Juros': 'R$ {:,.2f}',
            'Amortização': 'R$ {:,.2f}',
            'Saldo Devedor': 'R$ {:,.2f}'
        }), hide_index=True, use_container_width=True)
    
    with col2:
        st.write("**Últimas 12 Parcelas**")
        st.dataframe(df_parcelas.tail(12).style.format({
            'Valor Parcela': 'R$ {:,.2f}',
            'Juros': 'R$ {:,.2f}',
            'Amortização': 'R$ {:,.2f}',
            'Saldo Devedor': 'R$ {:,.2f}'
        }), hide_index=True, use_container_width=True)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def calcular_juros_compostos():
    """Calculadora de Juros Compostos"""
    st.header("📈 Calculadora de Juros Compostos")
    st.markdown("Simule o crescimento dos seus investimentos ao longo do tempo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Parâmetros")
        valor_inicial = st.number_input("Valor Inicial (R$)", min_value=0.0, value=10000.0, step=100.0)
        aporte_mensal = st.number_input("Aporte Mensal (R$)", min_value=0.0, value=500.0, step=50.0)
        taxa_juros = st.number_input("Taxa de Juros Anual (%)", min_value=0.0, value=10.0, step=0.1)
        anos = st.slider("Período (anos)", min_value=1, max_value=50, value=10)
        
    with col2:
        st.subheader("Opções Avançadas")
        tipo_aporte = st.radio("Tipo de Aporte", ["Início do mês", "Fim do mês"])
        considerar_inflacao = st.checkbox("Considerar inflação")
        if considerar_inflacao:
            taxa_inflacao = st.number_input("Inflação Anual (%)", min_value=0.0, value=4.0, step=0.1)
        else:
            taxa_inflacao = 0.0
    
    # Cálculos
    meses = anos * 12
    taxa_mensal = (1 + taxa_juros/100) ** (1/12) - 1
    taxa_inflacao_mensal = (1 + taxa_inflacao/100) ** (1/12) - 1
    
    # Simulação mês a mês
    saldos = []
    investido = []
    juros_acumulados = []
    saldos_reais = []
    
    saldo = valor_inicial
    total_investido = valor_inicial
    
    for mes in range(meses + 1):
        if mes > 0:
            if tipo_aporte == "Início do mês":
                saldo += aporte_mensal
                total_investido += aporte_mensal
                saldo *= (1 + taxa_mensal)
            else:
                saldo *= (1 + taxa_mensal)
                saldo += aporte_mensal
                total_investido += aporte_mensal
        
        saldos.append(saldo)
        investido.append(total_investido)
        juros_acumulados.append(saldo - total_investido)
        
        # Valor real (descontando inflação)
        saldo_real = saldo / ((1 + taxa_inflacao_mensal) ** mes)
        saldos_reais.append(saldo_real)
    
    # Criar DataFrame
    df = pd.DataFrame({
        'Mês': range(meses + 1),
        'Ano': [m/12 for m in range(meses + 1)],
        'Saldo': saldos,
        'Investido': investido,
        'Juros': juros_acumulados,
        'Saldo Real': saldos_reais
    })
    
    # Métricas principais
    st.subheader("📊 Resultados")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Valor Final", f"R$ {saldos[-1]:,.2f}")
    with col2:
        st.metric("Total Investido", f"R$ {investido[-1]:,.2f}")
    with col3:
        st.metric("Juros Ganhos", f"R$ {juros_acumulados[-1]:,.2f}")
    with col4:
        rentabilidade = ((saldos[-1] / investido[-1]) - 1) * 100
        st.metric("Rentabilidade", f"{rentabilidade:.2f}%")
    
    # Gráfico de evolução
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['Ano'],
        y=df['Saldo'],
        name='Saldo Total',
        fill='tonexty',
        line=dict(color='#1f77b4', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['Ano'],
        y=df['Investido'],
        name='Total Investido',
        fill='tozeroy',
        line=dict(color='#ff7f0e', width=2)
    ))
    
    if considerar_inflacao:
        fig.add_trace(go.Scatter(
            x=df['Ano'],
            y=df['Saldo Real'],
            name='Saldo Real (ajustado pela inflação)',
            line=dict(color='#2ca02c', width=2, dash='dash')
        ))
    
    fig.update_layout(
        title='Evolução do Investimento',
        xaxis_title='Anos',
        yaxis_title='Valor (R$)',
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico de Pizza - Composição Final
    col1, col2 = st.columns(2)
    
    with col1:
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Total Investido', 'Juros Ganhos'],
            values=[investido[-1], juros_acumulados[-1]],
            hole=0.4,
            marker_colors=['#ff7f0e', '#1f77b4']
        )])
        fig_pie.update_layout(title='Composição do Valor Final', height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Tabela de marcos importantes
        st.subheader("🎯 Marcos Importantes")
        marcos = []
        valores_marco = [50000, 100000, 250000, 500000, 1000000]
        
        for valor_marco in valores_marco:
            mes_marco = next((i for i, v in enumerate(saldos) if v >= valor_marco), None)
            if mes_marco:
                anos_marco = mes_marco / 12
                marcos.append({
                    'Meta': f'R$ {valor_marco:,.0f}',
                    'Tempo': f'{anos_marco:.1f} anos'
                })
        
        if marcos:
            st.dataframe(pd.DataFrame(marcos), hide_index=True, use_container_width=True)
        else:
            st.info("Ajuste os parâmetros para ver quando atingirá marcos importantes")
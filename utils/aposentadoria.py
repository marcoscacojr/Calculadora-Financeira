import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def calcular_aposentadoria():
    """Calculadora de Planejamento de Aposentadoria"""
    st.header("👴 Planejamento de Aposentadoria")
    st.markdown("Calcule quanto você precisa acumular para se aposentar confortavelmente")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Situação Atual")
        idade_atual = st.number_input("Idade Atual", min_value=18, max_value=80, value=30)
        patrimonio_atual = st.number_input("Patrimônio Atual (R$)", min_value=0.0, value=50000.0, step=1000.0)
        aporte_mensal = st.number_input("Aporte Mensal (R$)", min_value=0.0, value=1000.0, step=100.0)
        
    with col2:
        st.subheader("Metas")
        idade_aposentadoria = st.number_input("Idade de Aposentadoria Desejada", min_value=idade_atual+1, max_value=100, value=60)
        renda_mensal_desejada = st.number_input("Renda Mensal Desejada (R$)", min_value=0.0, value=5000.0, step=500.0)
        expectativa_vida = st.number_input("Expectativa de Vida", min_value=idade_aposentadoria+1, max_value=120, value=85)
    
    st.subheader("Parâmetros Econômicos")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        taxa_acumulacao = st.number_input("Taxa de Retorno na Acumulação (%/ano)", min_value=0.0, value=8.0, step=0.1)
    with col2:
        taxa_aposentadoria = st.number_input("Taxa de Retorno Aposentado (%/ano)", min_value=0.0, value=5.0, step=0.1)
    with col3:
        taxa_inflacao = st.number_input("Inflação Estimada (%/ano)", min_value=0.0, value=4.0, step=0.1)
    
    # Cálculos
    anos_ate_aposentadoria = idade_aposentadoria - idade_atual
    anos_aposentado = expectativa_vida - idade_aposentadoria
    
    # Fase 1: Acumulação
    taxa_mensal_acum = (1 + taxa_acumulacao/100) ** (1/12) - 1
    meses_acumulacao = anos_ate_aposentadoria * 12
    
    patrimonio = patrimonio_atual
    evolucao_patrimonio = [patrimonio]
    
    for mes in range(meses_acumulacao):
        patrimonio = patrimonio * (1 + taxa_mensal_acum) + aporte_mensal
        evolucao_patrimonio.append(patrimonio)
    
    patrimonio_aposentadoria = patrimonio
    
    # Fase 2: Usufruto - Calcular quanto precisa
    taxa_mensal_apos = (1 + taxa_aposentadoria/100) ** (1/12) - 1
    meses_aposentado = anos_aposentado * 12
    
    # Valor presente necessário para gerar renda desejada
    if taxa_mensal_apos > 0:
        patrimonio_necessario = renda_mensal_desejada * ((1 - (1 + taxa_mensal_apos) ** (-meses_aposentado)) / taxa_mensal_apos)
    else:
        patrimonio_necessario = renda_mensal_desejada * meses_aposentado
    
    # Simular aposentadoria com patrimônio acumulado
    patrimonio_aposentado = patrimonio_aposentadoria
    renda_possivel = []
    saldo_apos = []
    
    for mes in range(meses_aposentado):
        if taxa_mensal_apos > 0 and mes == 0:
            # Calcular renda sustentável
            renda_sustentavel = patrimonio_aposentado * (taxa_mensal_apos * (1 + taxa_mensal_apos) ** meses_aposentado) / ((1 + taxa_mensal_apos) ** meses_aposentado - 1)
        elif mes == 0:
            renda_sustentavel = patrimonio_aposentado / meses_aposentado
        
        patrimonio_aposentado = patrimonio_aposentado * (1 + taxa_mensal_apos) - renda_mensal_desejada
        saldo_apos.append(max(0, patrimonio_aposentado))
        renda_possivel.append(renda_mensal_desejada if patrimonio_aposentado > 0 else 0)
    
    # Métricas
    st.subheader("📊 Resultados da Simulação")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Patrimônio aos " + str(idade_aposentadoria) + " anos", f"R$ {patrimonio_aposentadoria:,.2f}")
    with col2:
        st.metric("Patrimônio Necessário", f"R$ {patrimonio_necessario:,.2f}")
    with col3:
        diferenca = patrimonio_aposentadoria - patrimonio_necessario
        st.metric("Diferença", f"R$ {diferenca:,.2f}", delta=f"{'✅ Suficiente' if diferenca >= 0 else '❌ Insuficiente'}")
    
    # Calcular renda sustentável
    if taxa_mensal_apos > 0:
        renda_sustentavel = patrimonio_aposentadoria * (taxa_mensal_apos * (1 + taxa_mensal_apos) ** meses_aposentado) / ((1 + taxa_mensal_apos) ** meses_aposentado - 1)
    else:
        renda_sustentavel = patrimonio_aposentadoria / meses_aposentado
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Renda Mensal Sustentável", f"R$ {renda_sustentavel:,.2f}")
    with col2:
        deficit = renda_mensal_desejada - renda_sustentavel
        if deficit > 0:
            st.metric("Déficit Mensal", f"R$ {deficit:,.2f}", delta="Ajuste suas metas")
        else:
            st.metric("Superávit Mensal", f"R$ {-deficit:,.2f}", delta="Sobra de recursos")
    
    # Gráfico de acumulação
    anos_lista = list(range(len(evolucao_patrimonio)))
    df_evolucao = pd.DataFrame({
        'Mês': anos_lista,
        'Ano': [m/12 + idade_atual for m in anos_lista],
        'Patrimônio': evolucao_patrimonio
    })
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_evolucao['Ano'],
        y=df_evolucao['Patrimônio'],
        fill='tozeroy',
        name='Patrimônio Acumulado',
        line=dict(color='#2ca02c', width=3)
    ))
    
    fig.add_hline(y=patrimonio_necessario, line_dash="dash", line_color="red", 
                  annotation_text="Meta Necessária", annotation_position="right")
    
    fig.update_layout(
        title='Evolução do Patrimônio até a Aposentadoria',
        xaxis_title='Idade',
        yaxis_title='Patrimônio (R$)',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico da aposentadoria
    fig2 = go.Figure()
    
    anos_aposentado_lista = [idade_aposentadoria + m/12 for m in range(len(saldo_apos))]
    
    fig2.add_trace(go.Scatter(
        x=anos_aposentado_lista,
        y=saldo_apos,
        fill='tozeroy',
        name='Saldo Durante Aposentadoria',
        line=dict(color='#ff7f0e', width=3)
    ))
    
    fig2.update_layout(
        title='Evolução do Patrimônio Durante a Aposentadoria',
        xaxis_title='Idade',
        yaxis_title='Patrimônio (R$)',
        height=500
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Sugestões
    st.subheader("💡 Recomendações")
    
    if diferenca < 0:
        # Calcular quanto precisa aportar a mais
        if taxa_mensal_acum > 0:
            aporte_necessario = (patrimonio_necessario - patrimonio_atual * (1 + taxa_mensal_acum) ** meses_acumulacao) / (((1 + taxa_mensal_acum) ** meses_acumulacao - 1) / taxa_mensal_acum)
        else:
            aporte_necessario = (patrimonio_necessario - patrimonio_atual) / meses_acumulacao
        
        aporte_adicional = aporte_necessario - aporte_mensal
        
        st.warning(f"""
        ⚠️ **Atenção!** Seu patrimônio projetado está abaixo da meta necessária.
        
        **Opções para atingir sua meta:**
        - Aumentar o aporte mensal em R$ {aporte_adicional:,.2f} (total: R$ {aporte_necessario:,.2f}/mês)
        - Trabalhar {abs(diferenca) / (renda_sustentavel * 12):.1f} anos a mais
        - Reduzir a renda desejada para R$ {renda_sustentavel:,.2f}/mês
        - Buscar investimentos com maior rentabilidade
        """)
    else:
        st.success(f"""
        ✅ **Parabéns!** Você está no caminho certo para atingir sua meta de aposentadoria!
        
        Com o plano atual, você terá um excedente de R$ {diferenca:,.2f}, o que permite:
        - Aposentar-se {(diferenca / (renda_mensal_desejada * 12)):.1f} anos mais cedo
        - Aumentar sua renda mensal para R$ {renda_sustentavel:,.2f}
        - Deixar uma herança de aproximadamente R$ {max(saldo_apos):,.2f}
        """)
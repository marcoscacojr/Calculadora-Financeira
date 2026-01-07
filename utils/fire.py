import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def calcular_fire():
    """Calculadora FI/RE - Financial Independence / Retire Early"""
    st.header("🔥 Calculadora FI/RE - Financial Independence / Retire Early")
    st.markdown("Descubra quando você poderá alcançar independência financeira")
    
    st.info("""
    **O que é FI/RE?**
    
    FI/RE é um movimento que busca independência financeira e aposentadoria precoce através de:
    - Alta taxa de poupança (40-70% da renda)
    - Investimentos consistentes
    - Estilo de vida frugal porém consciente
    
    **Regra dos 4%:** Você precisa de 25x suas despesas anuais investidas para se aposentar com segurança.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Situação Financeira Atual")
        renda_mensal_liquida = st.number_input("Renda Mensal Líquida (R$)", min_value=0.0, value=8000.0, step=500.0)
        despesas_mensais = st.number_input("Despesas Mensais (R$)", min_value=0.0, value=4000.0, step=500.0)
        patrimonio_atual = st.number_input("Patrimônio Atual (R$)", min_value=0.0, value=100000.0, step=10000.0)
        idade_atual = st.number_input("Idade Atual", min_value=18, max_value=80, value=28)
        
    with col2:
        st.subheader("🎯 Parâmetros FI/RE")
        taxa_retorno = st.number_input("Taxa de Retorno Anual (%)", min_value=0.0, value=8.0, step=0.1)
        taxa_saque = st.number_input("Taxa de Saque Anual (% do patrimônio)", min_value=0.0, value=4.0, step=0.1)
        despesas_fire = st.number_input("Despesas Mensais Desejadas no FI/RE (R$)", min_value=0.0, value=despesas_mensais, step=500.0)
        incluir_inflacao = st.checkbox("Ajustar pela inflação", value=True)
        if incluir_inflacao:
            taxa_inflacao = st.number_input("Inflação Anual (%)", min_value=0.0, value=4.0, step=0.1)
        else:
            taxa_inflacao = 0.0
    
    # Cálculos
    poupanca_mensal = renda_mensal_liquida - despesas_mensais
    taxa_poupanca = (poupanca_mensal / renda_mensal_liquida * 100) if renda_mensal_liquida > 0 else 0
    
    # Número FI/RE (25x despesas anuais ou usando taxa de saque customizada)
    despesas_anuais = despesas_fire * 12
    numero_fire = despesas_anuais / (taxa_saque / 100)
    
    # Calcular tempo até FI/RE
    taxa_mensal = (1 + taxa_retorno/100) ** (1/12) - 1
    taxa_inflacao_mensal = (1 + taxa_inflacao/100) ** (1/12) - 1
    
    patrimonio = patrimonio_atual
    mes = 0
    evolucao = []
    meses_fire = None
    
    max_meses = 50 * 12  # Limite de 50 anos
    
    while patrimonio < numero_fire and mes < max_meses:
        patrimonio = patrimonio * (1 + taxa_mensal) + poupanca_mensal
        
        # Ajustar despesas pela inflação
        if incluir_inflacao and mes % 12 == 0 and mes > 0:
            despesas_fire_ajustado = despesas_fire * ((1 + taxa_inflacao/100) ** (mes/12))
            numero_fire = despesas_fire_ajustado * 12 / (taxa_saque / 100)
        
        evolucao.append({
            'Mês': mes,
            'Ano': mes / 12,
            'Idade': idade_atual + mes / 12,
            'Patrimônio': patrimonio,
            'Meta FI/RE': numero_fire
        })
        
        mes += 1
    
    if patrimonio >= numero_fire:
        meses_fire = mes
        anos_fire = mes / 12
        idade_fire = idade_atual + anos_fire
    
    df_evolucao = pd.DataFrame(evolucao)
    
    # Métricas principais
    st.subheader("📊 Análise FI/RE")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Taxa de Poupança", f"{taxa_poupanca:.1f}%")
        if taxa_poupanca >= 50:
            st.success("Excelente! 🔥")
        elif taxa_poupanca >= 30:
            st.info("Bom progresso 👍")
        else:
            st.warning("Tente poupar mais 💪")
    
    with col2:
        st.metric("Poupança Mensal", f"R$ {poupanca_mensal:,.2f}")
    
    with col3:
        st.metric("Número FI/RE", f"R$ {numero_fire:,.2f}")
    
    with col4:
        progresso_fire = (patrimonio_atual / numero_fire * 100) if numero_fire > 0 else 0
        st.metric("Progresso", f"{progresso_fire:.1f}%")
    
    # Resultado principal
    if meses_fire:
        st.success(f"""
        ### 🎉 Você alcançará FI/RE em {anos_fire:.1f} anos!
        
        - **Idade no FI/RE:** {idade_fire:.0f} anos
        - **Patrimônio Final:** R$ {patrimonio:,.2f}
        - **Renda Passiva Mensal:** R$ {(patrimonio * taxa_saque / 100 / 12):,.2f}
        """)
    else:
        st.error(f"""
        ### ⚠️ Com os parâmetros atuais, FI/RE levará mais de 50 anos
        
        **Sugestões:**
        - Aumentar a taxa de poupança
        - Reduzir despesas mensais
        - Buscar investimentos com maior retorno
        - Aumentar sua renda
        """)
    
    # Gráfico de evolução
    if not df_evolucao.empty:
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df_evolucao['Idade'],
            y=df_evolucao['Patrimônio'],
            name='Patrimônio',
            fill='tozeroy',
            line=dict(color='#2ca02c', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=df_evolucao['Idade'],
            y=df_evolucao['Meta FI/RE'],
            name='Meta FI/RE',
            line=dict(color='#d62728', width=2, dash='dash')
        ))
        
        if meses_fire:
            fig.add_vline(x=idade_fire, line_dash="dot", line_color="orange",
                          annotation_text=f"FI/RE aos {idade_fire:.0f} anos",
                          annotation_position="top")
        
        fig.update_layout(
            title='Caminho para Independência Financeira',
            xaxis_title='Idade',
            yaxis_title='Patrimônio (R$)',
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Níveis de FI/RE
    st.subheader("📈 Níveis de Independência Financeira")
    
    niveis = [
        {"Nome": "Lean FI", "Multiplicador": 0.5, "Descrição": "Cobre 50% das despesas"},
        {"Nome": "Flex FI", "Multiplicador": 0.75, "Descrição": "Permite trabalho part-time"},
        {"Nome": "FI", "Multiplicador": 1.0, "Descrição": "Independência financeira completa"},
        {"Nome": "Fat FI", "Multiplicador": 1.5, "Descrição": "FI com estilo de vida elevado"},
        {"Nome": "Obese FI", "Multiplicador": 2.0, "Descrição": "FI com muito conforto"}
    ]
    
    niveis_data = []
    for nivel in niveis:
        meta = numero_fire * nivel["Multiplicador"]
        progresso = (patrimonio_atual / meta * 100) if meta > 0 else 0
        
        # Calcular tempo para cada nível
        p_temp = patrimonio_atual
        m_temp = 0
        while p_temp < meta and m_temp < max_meses:
            p_temp = p_temp * (1 + taxa_mensal) + poupanca_mensal
            m_temp += 1
        
        tempo = m_temp / 12 if p_temp >= meta else None
        
        niveis_data.append({
            "Nível": nivel["Nome"],
            "Meta": f"R$ {meta:,.0f}",
            "Progresso": f"{progresso:.1f}%",
            "Tempo": f"{tempo:.1f} anos" if tempo else "> 50 anos",
            "Descrição": nivel["Descrição"]
        })
    
    st.dataframe(pd.DataFrame(niveis_data), hide_index=True, use_container_width=True)
    
    # Análise de sensibilidade
    st.subheader("🔬 Análise de Sensibilidade")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Impacto de aumentar poupança mensal:**")
        aumentos_poupanca = [0, 500, 1000, 2000, 5000]
        resultados = []
        
        for aumento in aumentos_poupanca:
            nova_poupanca = poupanca_mensal + aumento
            p_temp = patrimonio_atual
            m_temp = 0
            
            while p_temp < numero_fire and m_temp < max_meses:
                p_temp = p_temp * (1 + taxa_mensal) + nova_poupanca
                m_temp += 1
            
            if p_temp >= numero_fire:
                resultados.append({
                    "Aumento": f"+R$ {aumento}",
                    "Tempo": f"{m_temp/12:.1f} anos",
                    "Redução": f"{(meses_fire - m_temp)/12:.1f} anos" if meses_fire else "N/A"
                })
        
        if resultados:
            st.dataframe(pd.DataFrame(resultados), hide_index=True, use_container_width=True)
    
    with col2:
        st.write("**Impacto de reduzir despesas mensais:**")
        reducoes_despesa = [0, 500, 1000, 2000]
        resultados = []
        
        for reducao in reducoes_despesa:
            novas_despesas = max(0, despesas_fire - reducao)
            novo_numero_fire = novas_despesas * 12 / (taxa_saque / 100)
            
            p_temp = patrimonio_atual
            m_temp = 0
            
            while p_temp < novo_numero_fire and m_temp < max_meses:
                p_temp = p_temp * (1 + taxa_mensal) + (poupanca_mensal + reducao)
                m_temp += 1
            
            if p_temp >= novo_numero_fire:
                resultados.append({
                    "Redução": f"-R$ {reducao}",
                    "Nova Meta": f"R$ {novo_numero_fire:,.0f}",
                    "Tempo": f"{m_temp/12:.1f} anos"
                })
        
        if resultados:
            st.dataframe(pd.DataFrame(resultados), hide_index=True, use_container_width=True)
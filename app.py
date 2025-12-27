"""
Calculadora de Amortización de Hipotecas - Dashboard Streamlit
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from calculadora import (
    generar_cuadro_amortizacion,
    aplicar_amortizacion_parcial,
    aplicar_amortizaciones_recurrentes,
    calcular_resumen,
    calcular_penalizacion
)
from styles import get_custom_css, format_currency, format_percentage, create_metric_card


# Configuración de la página - DEBE SER LO PRIMERO
st.set_page_config(
    page_title="Calculadora de Hipotecas",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"  # Esto asegura que inicie expandido
)

# Aplicar estilos CSS DESPUÉS de set_page_config
st.markdown(get_custom_css(), unsafe_allow_html=True)


def main():
    # Título principal
    st.markdown("# 🏠 Calculadora de Amortización de Hipotecas")
    
    # Sidebar con inputs - IMPORTANTE: Usar st.sidebar antes que cualquier contenido principal
    with st.sidebar:
        st.markdown("## 📊 Datos del Préstamo")
        
        capital = st.number_input(
            "Capital (€)",
            min_value=1000.0,
            max_value=10000000.0,
            value=150000.0,
            step=1000.0,
            format="%.2f",
            help="Importe total del préstamo hipotecario"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            años = st.number_input(
                "Años",
                min_value=1,
                max_value=40,
                value=30,
                help="Duración del préstamo en años"
            )
        with col2:
            meses_extra = st.number_input(
                "Meses",
                min_value=0,
                max_value=11,
                value=0,
                help="Meses adicionales"
            )
        
        meses_totales = años * 12 + meses_extra
        
        tae = st.number_input(
            "TAE (%)",
            min_value=0.0,
            max_value=20.0,
            value=2.0,
            step=0.05,
            format="%.2f",
            help="Tipo Anual Efectivo"
        )
        
        st.markdown("---")
        st.markdown("## ⚙️ Sistema de Amortización")
        
        sistema = st.radio(
            "Sistema",
            options=["Francés (cuota constante)", "Alemán (amortización constante)"],
            index=0,
            help="El sistema francés mantiene cuota fija, el alemán mantiene amortización fija"
        )
        sistema_key = 'frances' if 'Francés' in sistema else 'aleman'
        
        st.markdown("---")
        st.markdown("## 💰 Amortización Parcial")
        
        modo_amortizacion = st.radio(
            "Al amortizar, reducir:",
            options=["📉 Cuota mensual", "⏱️ Plazo del préstamo"],
            index=0,
            help="Elige si prefieres reducir la cuota o la duración"
        )
        modo_key = 'cuota' if 'Cuota' in modo_amortizacion else 'plazo'
        
        habilitar_amortizacion = st.checkbox("Realizar amortización parcial", value=False)
        
        if habilitar_amortizacion:
            cantidad_amortizar = st.number_input(
                "Cantidad a amortizar (€)",
                min_value=0.0,
                max_value=float(capital),
                value=10000.0,
                step=500.0,
                format="%.2f"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                año_amortizacion = st.number_input(
                    "En el año",
                    min_value=1,
                    max_value=años,
                    value=2
                )
            with col2:
                mes_amortizacion = st.number_input(
                    "En el mes",
                    min_value=1,
                    max_value=12,
                    value=1
                )
        else:
            cantidad_amortizar = 0
            año_amortizacion = 1
            mes_amortizacion = 1
        
        st.markdown("---")
        st.markdown("## 🔄 Amortización Recurrente")
        
        habilitar_recurrente = st.checkbox("Activar amortizaciones recurrentes", value=False)
        
        if habilitar_recurrente:
            cantidad_recurrente = st.number_input(
                "Cantidad cada vez (€)",
                min_value=100.0,
                max_value=float(capital),
                value=500.0,
                step=100.0,
                format="%.2f"
            )
            
            periodicidad = st.selectbox(
                "Periodicidad (meses)",
                options=[1, 3, 6, 12, 24, 36],
                index=3,
                format_func=lambda x: f"Cada {x} meses ({x//12} años)" if x >= 12 else f"Cada {x} meses"
            )
            
            mes_inicio_recurrente = st.number_input(
                "Mes de inicio",
                min_value=1,
                max_value=meses_totales,
                value=13,
                help="Mes a partir del cual empiezan las amortizaciones recurrentes"
            )
        else:
            cantidad_recurrente = 0
            periodicidad = 12
            mes_inicio_recurrente = 13
        
        st.markdown("---")
        st.markdown("## ⚠️ Penalización")
        
        pct_penalizacion = st.number_input(
            "% Penalización",
            min_value=0.0,
            max_value=5.0,
            value=0.5,
            step=0.1,
            format="%.2f",
            help="Porcentaje de penalización por amortización anticipada"
        )
        
        años_penalizacion = st.number_input(
            "Años con penalización",
            min_value=0,
            max_value=20,
            value=10,
            help="Número de años durante los que aplica la penalización"
        )
    
    # Generar cuadros de amortización
    # Cuadro original (sin amortizaciones)
    cuadro_original = generar_cuadro_amortizacion(capital, tae, meses_totales, sistema_key)
    resumen_original = calcular_resumen(cuadro_original)
    
    # Cuadro con amortizaciones
    if habilitar_recurrente:
        cuadro_final = aplicar_amortizaciones_recurrentes(
            principal=capital,
            tae=tae,
            meses=meses_totales,
            cantidad_recurrente=cantidad_recurrente,
            periodicidad=periodicidad,
            mes_inicio=mes_inicio_recurrente,
            modo=modo_key,
            anios_penalizacion=años_penalizacion,
            pct_penalizacion=pct_penalizacion,
            sistema=sistema_key
        )
    elif habilitar_amortizacion:
        cuadro_final = aplicar_amortizacion_parcial(
            cuadro=cuadro_original.copy(),
            cantidad=cantidad_amortizar,
            año_aplicacion=año_amortizacion,
            mes_aplicacion=mes_amortizacion,
            tae=tae,
            modo=modo_key,
            anios_penalizacion=años_penalizacion,
            pct_penalizacion=pct_penalizacion,
            sistema=sistema_key
        )
    else:
        cuadro_final = cuadro_original.copy()
    
    
    resumen_final = calcular_resumen(cuadro_final)
    
    # Mostrar métricas principales
    st.markdown("## 📈 Resumen del Préstamo")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            create_metric_card("Cuota Mensual", format_currency(resumen_final['cuota_inicial']), "💳"),
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            create_metric_card("Total Intereses", format_currency(resumen_final['total_intereses']), "📊"),
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            create_metric_card("Total a Pagar", format_currency(resumen_final['total_pagado']), "💰"),
            unsafe_allow_html=True
        )
    
    with col4:
        duracion_str = f"{resumen_final['duracion_años']:.1f} años"
        st.markdown(
            create_metric_card("Duración Final", duracion_str, "⏱️"),
            unsafe_allow_html=True
        )
    
    # Comparativa si hay amortizaciones
    if habilitar_amortizacion or habilitar_recurrente:
        st.markdown("### 💡 Ahorro con Amortización Anticipada")
        
        ahorro_intereses = resumen_original['total_intereses'] - resumen_final['total_intereses']
        ahorro_tiempo = resumen_original['num_cuotas'] - resumen_final['num_cuotas']
        # Usar cuota_final para ver la cuota después de la amortización
        cuota_nueva = resumen_final['cuota_final']
        cuota_original = resumen_original['cuota_inicial']
        reduccion_cuota = cuota_original - cuota_nueva
        pct_reduccion_cuota = (reduccion_cuota / cuota_original * 100) if cuota_original > 0 else 0
        
        # Mostrar métricas según el modo de amortización
        if modo_key == 'cuota':
            # Modo cuota: mostrar reducción de cuota prominentemente
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="Nueva Cuota",
                    value=format_currency(cuota_nueva),
                    delta=f"-{format_currency(reduccion_cuota)}" if reduccion_cuota > 0 else None,
                    delta_color="normal"
                )
            
            with col2:
                st.metric(
                    label="Reducción de Cuota",
                    value=f"-{pct_reduccion_cuota:.2f}%",
                    delta=f"Antes: {format_currency(cuota_original)}"
                )
            
            with col3:
                st.metric(
                    label="Ahorro en Intereses",
                    value=format_currency(ahorro_intereses),
                    delta=f"{ahorro_intereses/resumen_original['total_intereses']*100:.1f}%" if resumen_original['total_intereses'] > 0 else "0%"
                )
            
            with col4:
                total_amort = resumen_final['total_amortizacion_anticipada']
                st.metric(
                    label="Total Amortizado",
                    value=format_currency(total_amort)
                )
        else:
            # Modo plazo: mostrar reducción de tiempo prominentemente
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="Reducción de Plazo",
                    value=f"{ahorro_tiempo} meses",
                    delta=f"{ahorro_tiempo/12:.1f} años menos"
                )
            
            with col2:
                st.metric(
                    label="Nueva Duración",
                    value=f"{resumen_final['duracion_años']:.1f} años",
                    delta=f"Antes: {resumen_original['duracion_años']:.1f} años"
                )
            
            with col3:
                st.metric(
                    label="Ahorro en Intereses",
                    value=format_currency(ahorro_intereses),
                    delta=f"{ahorro_intereses/resumen_original['total_intereses']*100:.1f}%" if resumen_original['total_intereses'] > 0 else "0%"
                )
            
            with col4:
                total_amort = resumen_final['total_amortizacion_anticipada']
                st.metric(
                    label="Total Amortizado",
                    value=format_currency(total_amort)
                )
    
    st.markdown("---")
    
    # Gráficos
    st.markdown("## 📊 Visualizaciones")
    
    tab1, tab2, tab3 = st.tabs(["📈 Evolución Capital", "📊 Interés vs Amortización", "⚖️ Comparativa"])
    
    with tab1:
        # Gráfico de evolución del capital pendiente
        fig_capital = go.Figure()
        
        fig_capital.add_trace(go.Scatter(
            x=list(range(len(cuadro_final))),
            y=cuadro_final['capital_pendiente'],
            mode='lines',
            name='Capital Pendiente',
            fill='tozeroy',
            line=dict(color='#667eea', width=3),
            fillcolor='rgba(102, 126, 234, 0.3)'
        ))
        
        # Marcar amortizaciones anticipadas
        amort_anticipadas = cuadro_final[cuadro_final['amortizacion_anticipada'] > 0]
        if len(amort_anticipadas) > 0:
            fig_capital.add_trace(go.Scatter(
                x=amort_anticipadas.index.tolist(),
                y=amort_anticipadas['capital_pendiente'].tolist(),
                mode='markers',
                name='Amortización Anticipada',
                marker=dict(color='#f56565', size=12, symbol='star')
            ))
        
        fig_capital.update_layout(
            title="Evolución del Capital Pendiente",
            xaxis_title="Mes",
            yaxis_title="Capital Pendiente (€)",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0'),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_capital, use_container_width=True)
    
    with tab2:
        # Gráfico de interés vs amortización por año
        cuadro_anual = cuadro_final.groupby('año').agg({
            'interes': 'sum',
            'amortizacion': 'sum',
            'cuota': 'sum'
        }).reset_index()
        cuadro_anual = cuadro_anual[cuadro_anual['año'] > 0]  # Excluir año 0
        
        fig_comp = go.Figure()
        
        fig_comp.add_trace(go.Bar(
            x=cuadro_anual['año'],
            y=cuadro_anual['interes'],
            name='Intereses',
            marker_color='#f56565'
        ))
        
        fig_comp.add_trace(go.Bar(
            x=cuadro_anual['año'],
            y=cuadro_anual['amortizacion'],
            name='Amortización',
            marker_color='#48bb78'
        ))
        
        fig_comp.update_layout(
            title="Distribución Anual: Intereses vs Amortización",
            xaxis_title="Año",
            yaxis_title="Importe (€)",
            barmode='stack',
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )
        
        st.plotly_chart(fig_comp, use_container_width=True)
    
    with tab3:
        # Gráfico comparativo con/sin amortizaciones
        fig_comparativa = go.Figure()
        
        # Capital pendiente original
        fig_comparativa.add_trace(go.Scatter(
            x=list(range(len(cuadro_original))),
            y=cuadro_original['capital_pendiente'],
            mode='lines',
            name='Sin Amortización Anticipada',
            line=dict(color='#a0aec0', width=2, dash='dash')
        ))
        
        # Capital pendiente con amortizaciones
        fig_comparativa.add_trace(go.Scatter(
            x=list(range(len(cuadro_final))),
            y=cuadro_final['capital_pendiente'],
            mode='lines',
            name='Con Amortización Anticipada',
            line=dict(color='#667eea', width=3)
        ))
        
        fig_comparativa.update_layout(
            title="Comparativa: Con vs Sin Amortizaciones Anticipadas",
            xaxis_title="Mes",
            yaxis_title="Capital Pendiente (€)",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e2e8f0'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_comparativa, use_container_width=True)
    
    st.markdown("---")
    
    # Cuadro de amortización completo
    st.markdown("## 📋 Cuadro de Amortización Completo")
    
    # Preparar datos para mostrar
    cuadro_display = cuadro_final.copy()
    cuadro_display.columns = ['Año', 'Mes', 'Cuota', 'Interés', 'Amortización', 'Capital Pendiente', 'Amort. Anticipada']
    
    # Formatear valores monetarios
    for col in ['Cuota', 'Interés', 'Amortización', 'Capital Pendiente', 'Amort. Anticipada']:
        cuadro_display[col] = cuadro_display[col].apply(lambda x: format_currency(x))
    
    # Mostrar con estilo
    st.dataframe(
        cuadro_display,
        use_container_width=True,
        height=600,
        hide_index=True
    )
    
    # Botón para descargar CSV
    csv = cuadro_final.to_csv(index=False, decimal=',', sep=';')
    st.download_button(
        label="📥 Descargar Cuadro (CSV)",
        data=csv,
        file_name="cuadro_amortizacion.csv",
        mime="text/csv"
    )


if __name__ == "__main__":
    main()
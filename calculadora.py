"""
Módulo de cálculos financieros para amortización de hipotecas.

Soporta:
- Sistema Francés (cuota constante)
- Sistema Alemán (amortización constante)
- Amortizaciones parciales (reducir cuota o plazo)
- Amortizaciones recurrentes
- Penalizaciones por amortización anticipada
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Literal, Optional
from copy import deepcopy


@dataclass
class ResultadoAmortizacion:
    """Resultado de los cálculos de amortización."""
    cuota_mensual: float
    total_intereses: float
    total_pagado: float
    num_cuotas: int
    cuadro: pd.DataFrame


def calcular_tipo_mensual(tae: float) -> float:
    """
    Convierte TAE a tipo de interés mensual.
    
    Args:
        tae: Tipo Anual Efectivo en porcentaje (ej: 2 para 2%)
    
    Returns:
        Tipo mensual como decimal
    """
    return (1 + tae / 100) ** (1/12) - 1


def calcular_cuota_francesa(principal: float, tipo_mensual: float, meses: int) -> float:
    """
    Calcula la cuota mensual con sistema francés (cuota constante).
    
    Fórmula: C = P × [r(1+r)^n] / [(1+r)^n - 1]
    
    Args:
        principal: Capital del préstamo
        tipo_mensual: Tipo de interés mensual como decimal
        meses: Número de meses del préstamo
    
    Returns:
        Cuota mensual
    """
    if tipo_mensual == 0:
        return principal / meses
    
    factor = (1 + tipo_mensual) ** meses
    return principal * (tipo_mensual * factor) / (factor - 1)


def generar_cuadro_amortizacion(
    principal: float,
    tae: float,
    meses: int,
    sistema: Literal['frances', 'aleman'] = 'frances'
) -> pd.DataFrame:
    """
    Genera el cuadro completo de amortización.
    
    Args:
        principal: Capital del préstamo
        tae: Tipo Anual Efectivo en porcentaje
        meses: Duración del préstamo en meses
        sistema: 'frances' o 'aleman'
    
    Returns:
        DataFrame con el cuadro de amortización
    """
    tipo_mensual = calcular_tipo_mensual(tae)
    
    # Inicializar listas para el cuadro
    datos = []
    capital_pendiente = principal
    
    # Fila inicial (mes 0)
    datos.append({
        'año': 0,
        'mes': 0,
        'cuota': 0.0,
        'interes': 0.0,
        'amortizacion': 0.0,
        'capital_pendiente': capital_pendiente,
        'amortizacion_anticipada': 0.0,
        'comision': 0.0
    })
    
    if sistema == 'frances':
        cuota = calcular_cuota_francesa(principal, tipo_mensual, meses)
        
        for i in range(1, meses + 1):
            interes = capital_pendiente * tipo_mensual
            amortizacion = cuota - interes
            capital_pendiente -= amortizacion
            
            # Evitar valores negativos por errores de redondeo
            if capital_pendiente < 0:
                capital_pendiente = 0
            
            año = (i - 1) // 12 + 1
            mes_del_año = (i - 1) % 12 + 1
            
            datos.append({
                'año': año,
                'mes': mes_del_año,
                'cuota': cuota,
                'interes': interes,
                'amortizacion': amortizacion,
                'capital_pendiente': capital_pendiente,
                'amortizacion_anticipada': 0.0,
                'comision': 0.0
            })
    
    else:  # Sistema alemán
        amortizacion_fija = principal / meses
        
        for i in range(1, meses + 1):
            interes = capital_pendiente * tipo_mensual
            cuota = amortizacion_fija + interes
            capital_pendiente -= amortizacion_fija
            
            if capital_pendiente < 0:
                capital_pendiente = 0
            
            año = (i - 1) // 12 + 1
            mes_del_año = (i - 1) % 12 + 1
            
            datos.append({
                'año': año,
                'mes': mes_del_año,
                'cuota': cuota,
                'interes': interes,
                'amortizacion': amortizacion_fija,
                'capital_pendiente': capital_pendiente,
                'amortizacion_anticipada': 0.0,
                'comision': 0.0
            })
    
    return pd.DataFrame(datos)


def calcular_penalizacion(
    cantidad: float,
    mes_actual: int,
    meses_totales: int,
    anios_penalizacion: int = 10,
    pct_penalizacion: float = 0.5
) -> float:
    """
    Calcula la penalización por amortización anticipada.
    
    Args:
        cantidad: Cantidad a amortizar
        mes_actual: Mes actual del préstamo (1-indexado)
        meses_totales: Duración total del préstamo en meses
        anios_penalizacion: Años durante los que aplica la penalización
        pct_penalizacion: Porcentaje de penalización
    
    Returns:
        Importe de la penalización
    """
    meses_penalizacion = anios_penalizacion * 12
    
    if mes_actual <= meses_penalizacion:
        return cantidad * (pct_penalizacion / 100)
    
    return 0.0


def aplicar_amortizacion_parcial(
    cuadro: pd.DataFrame,
    cantidad: float,
    año_aplicacion: int,
    mes_aplicacion: int,
    tae: float,
    modo: Literal['cuota', 'plazo'] = 'cuota',
    anios_penalizacion: int = 10,
    pct_penalizacion: float = 0.5,
    pct_comision: float = 0.25,
    sistema: Literal['frances', 'aleman'] = 'frances'
) -> pd.DataFrame:
    """
    Aplica una amortización parcial al cuadro existente.
    
    Args:
        cuadro: Cuadro de amortización existente
        cantidad: Cantidad a amortizar anticipadamente (Bruta, incluye comisión)
        año_aplicacion: Año en que se aplica la amortización
        mes_aplicacion: Mes del año en que se aplica
        tae: TAE del préstamo
        modo: 'cuota' para reducir cuota, 'plazo' para reducir duración
        anios_penalizacion: Años durante los que aplica penalización
        pct_penalizacion: Porcentaje de penalización
        pct_comision: Porcentaje de comisión por servicio
        sistema: Sistema de amortización
    
    Returns:
        Nuevo cuadro de amortización con la amortización aplicada
    """
    tipo_mensual = calcular_tipo_mensual(tae)
    cuadro_nuevo = cuadro.copy().reset_index(drop=True)
    
    # Buscar la fila que corresponde al año/mes especificado
    idx_encontrado = None
    for idx in range(len(cuadro_nuevo)):
        if cuadro_nuevo.iloc[idx]['año'] == año_aplicacion and cuadro_nuevo.iloc[idx]['mes'] == mes_aplicacion:
            idx_encontrado = idx
            break
    
    if idx_encontrado is None or idx_encontrado < 1:
        return cuadro_nuevo
    
    # Calcular mes global para penalizaciones
    mes_global = (año_aplicacion - 1) * 12 + mes_aplicacion
    
    # Calcular comisión
    comision = cantidad * (pct_comision / 100)
    cantidad_efectiva = cantidad - comision
    
    # Obtener capital pendiente antes de la amortización
    capital_antes = cuadro_nuevo.iloc[idx_encontrado]['capital_pendiente']
    
    # Calcular penalización (sobre la cantidad bruta o neta? Normalmente bruta, pero depende de la entidad)
    # Por defecto aplicamos sobre la cantidad aportada
    penalizacion = calcular_penalizacion(
        cantidad, mes_global, len(cuadro_nuevo) - 1,
        anios_penalizacion, pct_penalizacion
    )
    
    # Nuevo capital pendiente (se reduce por la cantidad efectiva amortizada)
    nuevo_capital = capital_antes - cantidad_efectiva
    if nuevo_capital < 0:
        # Si se paga de más, ajustamos la cantidad efectiva al capital restante
        # y la comisión proporcionalmente (o simplificamos)
        cantidad_efectiva = capital_antes
        comision = cantidad_efectiva / (1 - pct_comision / 100) * (pct_comision / 100)
        cantidad = cantidad_efectiva + comision
        nuevo_capital = 0
    
    # Marcar la amortización anticipada y comisión en el cuadro
    cuadro_nuevo.at[idx_encontrado, 'amortizacion_anticipada'] = cantidad_efectiva
    cuadro_nuevo.at[idx_encontrado, 'comision'] = comision
    cuadro_nuevo.at[idx_encontrado, 'capital_pendiente'] = nuevo_capital
    
    if nuevo_capital == 0:
        # Préstamo pagado, eliminar filas restantes
        return cuadro_nuevo.iloc[:idx_encontrado + 1].copy()
    
    # Calcular meses restantes del préstamo original
    meses_restantes_original = len(cuadro_nuevo) - idx_encontrado - 1
    
    if modo == 'cuota':
        # Reducir cuota manteniendo plazo
        if sistema == 'frances':
            nueva_cuota = calcular_cuota_francesa(nuevo_capital, tipo_mensual, meses_restantes_original)
        else:
            amortizacion_fija = nuevo_capital / meses_restantes_original
        
        capital_pendiente = nuevo_capital
        nuevas_filas = []
        
        for i in range(1, meses_restantes_original + 1):
            mes_absoluto = mes_global + i
            año = (mes_absoluto - 1) // 12 + 1
            mes_del_año = (mes_absoluto - 1) % 12 + 1
            
            interes = capital_pendiente * tipo_mensual
            
            if sistema == 'frances':
                amortizacion = nueva_cuota - interes
                cuota = nueva_cuota
            else:
                amortizacion = amortizacion_fija
                cuota = amortizacion + interes
            
            capital_pendiente -= amortizacion
            if capital_pendiente < 0:
                capital_pendiente = 0
            
            nuevas_filas.append({
                'año': año,
                'mes': mes_del_año,
                'cuota': cuota,
                'interes': interes,
                'amortizacion': amortizacion,
                'capital_pendiente': capital_pendiente,
                'amortizacion_anticipada': 0.0,
                'comision': 0.0
            })
        
        # Combinar cuadro original hasta el mes de amortización con nuevas filas
        cuadro_resultado = pd.concat([
            cuadro_nuevo.iloc[:idx_encontrado + 1],
            pd.DataFrame(nuevas_filas)
        ], ignore_index=True)
        
    else:  # modo == 'plazo'
        # Reducir plazo manteniendo cuota original
        cuota_original = cuadro_nuevo.iloc[idx_encontrado]['cuota']
        
        capital_pendiente = nuevo_capital
        nuevas_filas = []
        mes_contador = 1
        
        while capital_pendiente > 0.01:
            mes_absoluto = mes_global + mes_contador
            año = (mes_absoluto - 1) // 12 + 1
            mes_del_año = (mes_absoluto - 1) % 12 + 1
            
            interes = capital_pendiente * tipo_mensual
            amortizacion = cuota_original - interes
            
            if amortizacion >= capital_pendiente:
                amortizacion = capital_pendiente
                cuota = amortizacion + interes
                capital_pendiente = 0
            else:
                cuota = cuota_original
                capital_pendiente -= amortizacion
            
            nuevas_filas.append({
                'año': año,
                'mes': mes_del_año,
                'cuota': cuota,
                'interes': interes,
                'amortizacion': amortizacion,
                'capital_pendiente': capital_pendiente,
                'amortizacion_anticipada': 0.0,
                'comision': 0.0
            })
            
            mes_contador += 1
            
            if mes_contador > 1000:
                break
        
        cuadro_resultado = pd.concat([
            cuadro_nuevo.iloc[:idx_encontrado + 1],
            pd.DataFrame(nuevas_filas)
        ], ignore_index=True)
    
    return cuadro_resultado


def aplicar_amortizaciones_recurrentes(
    principal: float,
    tae: float,
    meses: int,
    cantidad_recurrente: float,
    periodicidad: int,
    mes_inicio: int,
    modo: Literal['cuota', 'plazo'] = 'cuota',
    anios_penalizacion: int = 10,
    pct_penalizacion: float = 0.5,
    pct_comision: float = 0.25,
    sistema: Literal['frances', 'aleman'] = 'frances'
) -> pd.DataFrame:
    """
    Genera un cuadro con amortizaciones automáticas recurrentes.
    
    Args:
        principal: Capital inicial del préstamo
        tae: TAE del préstamo
        meses: Duración original en meses
        cantidad_recurrente: Cantidad a amortizar cada vez
        periodicidad: Cada cuántos meses se amortiza
        mes_inicio: Mes a partir del cual empiezan las amortizaciones
        modo: 'cuota' o 'plazo'
        anios_penalizacion: Años con penalización
        pct_penalizacion: Porcentaje de penalización
        pct_comision: Porcentaje de comisión
        sistema: Sistema de amortización
    
    Returns:
        Cuadro de amortización con todas las amortizaciones aplicadas
    """
    # Generar cuadro inicial
    cuadro = generar_cuadro_amortizacion(principal, tae, meses, sistema)
    
    # Calcular meses donde se aplican amortizaciones (meses globales del préstamo original)
    meses_amortizacion = list(range(mes_inicio, meses + 1, periodicidad))
    
    # Para cada mes de amortización, necesitamos encontrar la fila correcta en el cuadro
    # ya que después de cada amortización el cuadro puede cambiar
    for mes_objetivo in meses_amortizacion:
        # Buscar la fila que corresponde a este mes global
        # Calculamos año y mes del año objetivo
        año_objetivo = (mes_objetivo - 1) // 12 + 1
        mes_del_año_objetivo = (mes_objetivo - 1) % 12 + 1
        
        # Buscar la fila en el cuadro actual que coincide con este año/mes
        fila_encontrada = None
        for idx in range(1, len(cuadro)):
            # Convertir a int para asegurar comparación correcta (evitar float 2.0 vs int 2)
            anio_fila = int(cuadro.iloc[idx]['año'])
            mes_fila = int(cuadro.iloc[idx]['mes'])
            if anio_fila == int(año_objetivo) and mes_fila == int(mes_del_año_objetivo):
                fila_encontrada = idx
                break

        if fila_encontrada is None:
            # Este mes ya no existe en el cuadro (plazo reducido)
            continue
        
        # Verificar si hay capital pendiente en esa fila
        if cuadro.iloc[fila_encontrada]['capital_pendiente'] <= 0.01:
            break
        
        cuadro = aplicar_amortizacion_parcial(
            cuadro=cuadro,
            cantidad=cantidad_recurrente,
            año_aplicacion=año_objetivo,
            mes_aplicacion=mes_del_año_objetivo,
            tae=tae,
            modo=modo,
            anios_penalizacion=anios_penalizacion,
            pct_penalizacion=pct_penalizacion,
            pct_comision=pct_comision,
            sistema=sistema
        )
    
    return cuadro


def calcular_resumen(cuadro: pd.DataFrame) -> dict:
    """
    Calcula el resumen de un cuadro de amortización.
    
    Args:
        cuadro: Cuadro de amortización
    
    Returns:
        Diccionario con métricas resumen
    """
    # Excluir fila 0 (mes inicial)
    cuadro_sin_inicio = cuadro.iloc[1:]
    
    total_intereses = cuadro_sin_inicio['interes'].sum()
    total_amortizado = cuadro_sin_inicio['amortizacion'].sum()
    total_amortizacion_anticipada = cuadro_sin_inicio['amortizacion_anticipada'].sum()
    total_comisiones = cuadro_sin_inicio['comision'].sum()
    total_cuotas = cuadro_sin_inicio['cuota'].sum()
    num_cuotas = len(cuadro_sin_inicio)
    
    # Cuota media (para sistema alemán)
    cuota_media = cuadro_sin_inicio['cuota'].mean()
    
    # Primera cuota (para mostrar)
    primera_cuota = cuadro_sin_inicio.iloc[0]['cuota'] if len(cuadro_sin_inicio) > 0 else 0
    
    # Cuota final (después de amortizaciones)
    cuota_final = primera_cuota
    filas_con_amortizacion = cuadro_sin_inicio[cuadro_sin_inicio['amortizacion_anticipada'] > 0]
    
    if len(filas_con_amortizacion) > 0:
        # Obtener el índice de la última amortización anticipada
        ultimo_idx_amort = filas_con_amortizacion.index[-1]
        # La cuota posterior está en la siguiente fila
        pos_ultimo = cuadro.index.get_loc(ultimo_idx_amort)
        if pos_ultimo + 1 < len(cuadro):
            cuota_final = cuadro.iloc[pos_ultimo + 1]['cuota']
        else:
            # Si es la última fila, tomar esa cuota
            cuota_final = cuadro.iloc[pos_ultimo]['cuota']
    
    return {
        'total_intereses': total_intereses,
        'total_pagado': total_cuotas + total_amortizacion_anticipada + total_comisiones,
        'num_cuotas': num_cuotas,
        'cuota_inicial': primera_cuota,
        'cuota_final': cuota_final,
        'cuota_media': cuota_media,
        'total_amortizacion_anticipada': total_amortizacion_anticipada,
        'total_comisiones': total_comisiones,
        'duracion_años': num_cuotas / 12
    }


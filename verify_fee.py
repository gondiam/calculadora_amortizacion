import pandas as pd
from calculadora import generar_cuadro_amortizacion, aplicar_amortizacion_parcial, calcular_resumen

def verify_amortization_fee():
    print("Verifying Amortization Fee Implementation...")
    
    # Setup test data
    principal = 100000.0
    tae = 3.0
    meses = 120
    cantidad_amortizar = 10000.0
    pct_comision = 0.75
    
    # 1. Generate base cuadro
    cuadro = generar_cuadro_amortizacion(principal, tae, meses)
    
    # 2. Apply partial amortization in Year 1, Month 5
    cuadro_final = aplicar_amortizacion_parcial(
        cuadro=cuadro,
        cantidad=cantidad_amortizar,
        año_aplicacion=1,
        mes_aplicacion=5,
        tae=tae,
        pct_comision=pct_comision
    )
    
    # 3. Check specific row
    row = cuadro_final[(cuadro_final['año'] == 1) & (cuadro_final['mes'] == 5)].iloc[0]
    
    expected_comision = cantidad_amortizar * (pct_comision / 100)
    expected_amort_neta = cantidad_amortizar - expected_comision
    
    print(f"Amortization applied: {cantidad_amortizar}€")
    print(f"Calculated commission: {row['comision']}€ (Expected: {expected_comision}€)")
    print(f"Effective principal reduction: {row['amortizacion_anticipada']}€ (Expected: {expected_amort_neta}€)")
    
    assert abs(row['comision'] - expected_comision) < 0.001
    assert abs(row['amortizacion_anticipada'] - expected_amort_neta) < 0.001
    
    # 4. Check summary
    resumen = calcular_resumen(cuadro_final)
    print(f"Total commissions in summary: {resumen['total_comisiones']}€")
    assert abs(resumen['total_comisiones'] - expected_comision) < 0.001
    
    print("Verification SUCCESSFUL!")

if __name__ == "__main__":
    verify_amortization_fee()

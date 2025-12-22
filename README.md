# 🏠 Calculadora de Amortización de Hipotecas

Aplicación web moderna para calcular y visualizar la amortización de préstamos hipotecarios, con soporte para amortizaciones parciales y recurrentes.

## ✨ Características

- **Sistemas de Amortización**: Francés (cuota constante) y Alemán (amortización constante)
- **Amortizaciones Parciales**: Reduce la cuota mensual o el plazo del préstamo
- **Amortizaciones Recurrentes**: Configura pagos automáticos periódicos
- **Penalizaciones**: Cálculo automático de penalizaciones por amortización anticipada
- **Visualizaciones Interactivas**: Gráficos dinámicos con Plotly
- **Cuadro de Amortización Completo**: Descargable en formato CSV
- **Interfaz Moderna**: Dashboard oscuro con animaciones y diseño responsive

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip o uv (gestor de paquetes)

### Pasos de Instalación

1. **Clonar o descargar el repositorio**

2. **Crear entorno virtual** (recomendado):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```

   O con `uv`:
   ```bash
   uv venv
   source .venv/bin/activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

   O con `uv`:
   ```bash
   uv pip install -r requirements.txt
   ```

## 📦 Ejecución Local

```bash
streamlit run app.py
```

La aplicación estará disponible en `http://localhost:8501`

## 🌐 Despliegue en Streamlit Cloud

1. Sube el proyecto a GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu repositorio de GitHub
4. Selecciona la rama y el archivo `app.py`
5. ¡Despliega!

## 📁 Estructura del Proyecto

```
calculadora_amortizacion/
├── app.py              # Aplicación principal Streamlit
├── calculadora.py      # Motor de cálculos financieros
├── styles.py           # Estilos CSS y funciones de formato
├── requirements.txt    # Dependencias del proyecto
└── README.md          # Este archivo
```

## 🛠️ Uso

### Configuración Básica

1. **Detalles del Préstamo**: Introduce el capital, plazo y TAE
2. **Sistema de Amortización**: Elige entre Francés o Alemán
3. **Modo de Amortización**: Selecciona si quieres reducir la cuota o el plazo

### Amortización Parcial

1. Activa "Realizar amortización parcial"
2. Introduce la cantidad a amortizar
3. Selecciona el año y mes de la amortización

### Amortización Recurrente

1. Activa "Activar amortizaciones recurrentes"
2. Configura la cantidad y periodicidad
3. Selecciona el mes de inicio

### Penalizaciones

- Configura el porcentaje de penalización
- Define el número de años con penalización (típicamente 10 años)

## 📊 Visualizaciones

- **Evolución del Capital**: Muestra cómo disminuye el capital pendiente
- **Interés vs Amortización**: Distribución anual de intereses y amortización
- **Comparativa**: Compara el préstamo con y sin amortizaciones anticipadas

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz un fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🐛 Reporte de Bugs

Si encuentras algún bug, por favor abre un issue en GitHub con:
- Descripción del problema
- Pasos para reproducirlo
- Comportamiento esperado vs actual
- Screenshots si es aplicable

## 💡 Soporte

Para preguntas o soporte, abre un issue en GitHub.
Muchas gracias :) 

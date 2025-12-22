"""
Estilos CSS personalizados para el dashboard de hipotecas.
"""

def get_custom_css() -> str:
    """Retorna el CSS personalizado para la aplicación."""
    return """
    <style>
        /* Variables de colores */
        :root {
            --primary-color: #667eea;
            --primary-dark: #5a67d8;
            --secondary-color: #764ba2;
            --background-dark: #1a1a2e;
            --card-bg: #16213e;
            --card-border: #0f3460;
            --text-primary: #ffffff;
            --text-secondary: #a0aec0;
            --success-color: #48bb78;
            --warning-color: #ed8936;
            --danger-color: #f56565;
        }
        
        /* Fondo general */
        .stApp {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
            border-right: 1px solid #0f3460;
        }
        
        [data-testid="stSidebar"] .stMarkdown h2 {
            color: #667eea;
            font-size: 1.1rem;
            font-weight: 600;
            margin-top: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #667eea;
        }
        
        /* Títulos */
        h1 {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 700;
            text-align: center;
            padding: 1rem 0;
        }
        
        h2, h3 {
            color: #e2e8f0 !important;
        }
        
        /* Cards de métricas */
        .metric-card {
            background: linear-gradient(135deg, #1e3a5f 0%, #16213e 100%);
            border: 1px solid #0f3460;
            border-radius: 16px;
            padding: 1.5rem;
            margin: 0.5rem 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(102, 126, 234, 0.3);
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .metric-label {
            color: #a0aec0;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 0.5rem;
        }
        
        /* Tabla de amortización */
        .dataframe {
            background-color: #16213e !important;
            border-radius: 12px;
            overflow: hidden;
        }
        
        .dataframe thead th {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 12px 16px !important;
            text-align: center !important;
        }
        
        .dataframe tbody tr:nth-child(even) {
            background-color: #1a1a2e !important;
        }
        
        .dataframe tbody tr:nth-child(odd) {
            background-color: #16213e !important;
        }
        
        .dataframe tbody tr:hover {
            background-color: #0f3460 !important;
        }
        
        .dataframe tbody td {
            color: #e2e8f0 !important;
            padding: 10px 16px !important;
            text-align: right !important;
        }
        
        /* Inputs */
        .stNumberInput > div > div > input {
            background-color: #1a1a2e;
            border: 1px solid #0f3460;
            border-radius: 8px;
            color: #e2e8f0;
        }
        
        .stNumberInput > div > div > input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.3);
        }
        
        /* Radio buttons */
        .stRadio > div {
            background-color: #1a1a2e;
            border-radius: 8px;
            padding: 0.5rem;
        }
        
        /* Selectbox */
        .stSelectbox > div > div {
            background-color: #1a1a2e;
            border-color: #0f3460;
        }
        
        /* Checkbox */
        .stCheckbox > label > div[data-testid="stMarkdownContainer"] > p {
            color: #e2e8f0;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background-color: #1a1a2e;
            border-radius: 8px;
            color: #e2e8f0 !important;
        }
        
        /* Info boxes */
        .stAlert {
            background-color: #1a1a2e;
            border-radius: 12px;
        }
        
        /* Botones */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #1a1a2e;
            border-radius: 12px;
            padding: 0.5rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            border-radius: 8px;
            color: #a0aec0;
            padding: 0.5rem 1rem;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        /* Divider */
        hr {
            border-color: #0f3460;
            margin: 2rem 0;
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #1a1a2e;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 4px;
        }
        
        /* Ocultar elementos de Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Animaciones */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .animate-fade-in {
            animation: fadeIn 0.5s ease forwards;
        }
        
        /* Contenedor de gráficos */
        .chart-container {
            background: linear-gradient(135deg, #1e3a5f 0%, #16213e 100%);
            border: 1px solid #0f3460;
            border-radius: 16px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        /* Sección de comparativa */
        .comparison-positive {
            color: #48bb78;
            font-weight: 600;
        }
        
        .comparison-negative {
            color: #f56565;
            font-weight: 600;
        }
    </style>
    """


def format_currency(value: float) -> str:
    """Formatea un valor como moneda en euros."""
    return f"{value:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")


def format_percentage(value: float) -> str:
    """Formatea un valor como porcentaje."""
    return f"{value:.2f}%".replace(".", ",")


def create_metric_card(label: str, value: str, icon: str = "💰") -> str:
    """Crea un HTML para una tarjeta de métrica."""
    return f"""
    <div class="metric-card">
        <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """

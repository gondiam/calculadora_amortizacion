"""
Estilos CSS personalizados para el dashboard de hipotecas.
"""

def get_custom_css() -> str:
    """Retorna el CSS personalizado para la aplicación."""
    return """
    <style>
        /* Modern Monochrome Design System */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        :root {
            --primary-color: #000000;
            --primary-hover: #333333;
            --bg-main: #ffffff;
            --bg-sidebar: #f8f9fa;
            --bg-card: #ffffff;
            --border-color: #e5e5e5;
            --text-main: #000000;
            --text-muted: #666666;
            --accent-soft: #f0f0f0;
            --success: #1a1a1a; /* Using black for success in a mono theme, or subtle gray */
            --shadow: 0 1px 3px rgba(0,0,0,0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);
        }

        /* Base styles */
        .stApp {
            background-color: var(--bg-main);
            color: var(--text-main);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        /* Sidebar Customization */
        [data-testid="stSidebar"] {
            background-color: var(--bg-sidebar);
            border-right: 1px solid var(--border-color);
        }

        [data-testid="stSidebar"] .stMarkdown h2 {
            color: var(--text-main);
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 700;
            border-bottom: 2px solid var(--primary-color);
            padding-bottom: 0.25rem;
            margin-bottom: 1rem;
        }

        /* Typography */
        h1, h2, h3 {
            color: var(--text-main) !important;
            font-family: 'Inter', sans-serif;
            font-weight: 700 !important;
        }

        h1 {
            font-size: 2.5rem !important;
            letter-spacing: -0.02em;
            margin-bottom: 2rem !important;
            text-align: left !important;
        }

        /* Metric Cards */
        .metric-card {
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 0.5rem 0;
            transition: all 0.2s ease;
            box-shadow: var(--shadow);
        }

        .metric-card:hover {
            box-shadow: var(--shadow-lg);
            border-color: var(--primary-color);
            transform: translateY(-2px);
        }

        .metric-value {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--text-main);
            letter-spacing: -0.01em;
        }

        .metric-label {
            color: var(--text-muted);
            font-size: 0.75rem;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.05em;
            margin-top: 0.5rem;
        }

        /* Buttons Mapping */
        .stButton > button {
            background-color: var(--primary-color) !important;
            color: white !important;
            border-radius: 4px !important;
            border: none !important;
            padding: 0.6rem 1.2rem !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            transition: all 0.2s ease !important;
            width: 100%;
        }

        .stButton > button:hover {
            background-color: var(--primary-hover) !important;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1) !important;
        }


        /* Input Controls - Fix Contrast */
        .stNumberInput input, .stSelectbox [data-baseweb="select"] {
            border-radius: 4px !important;
            border: 1px solid var(--border-color) !important;
            background-color: white !important;
            color: #000000 !important;
            caret-color: #000000 !important;
        }

        /* Fix label contrast in sidebar and main area */
        .stMarkdown p, .stMarkdown label, .stRadio label, .stCheckbox label {
            color: #000000 !important;
        }
        
        /* Specifically for input labels */
        [data-testid="stWidgetLabel"] p {
             color: #000000 !important;
             font-weight: 600 !important;
        }

        /* Table Aesthetics */
        .dataframe {
            border: 1px solid var(--border-color) !important;
            border-radius: 4px;
        }

        .dataframe thead th {
            background-color: #fcfcfc !important;
            color: #000 !important;
            border-bottom: 2px solid #000 !important;
            font-size: 0.8rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.02em !important;
        }

        .dataframe tbody tr {
            border-bottom: 1px solid var(--border-color) !important;
            color: #000000 !important;
        }

        .dataframe tbody tr:hover {
            background-color: #fafafa !important;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            background-color: transparent;
            border-bottom: 1px solid var(--border-color);
            gap: 24px;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: transparent !important;
            border: none !important;
            color: var(--text-muted) !important;
            padding: 12px 0 !important;
            font-weight: 600 !important;
        }

        .stTabs [aria-selected="true"] {
            color: var(--text-main) !important;
            border-bottom: 2px solid var(--primary-color) !important;
        }

        /* Divider & Scrollbar */
        hr { border-color: var(--border-color); }

        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-thumb { background: #ccc; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: #999; }

        /* Clean up Streamlit UI */
        header { background: transparent !important; }
        footer { display: none !important; }
        #MainMenu { display: none !important; }
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
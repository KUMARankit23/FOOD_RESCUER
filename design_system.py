"""
FoodRescue-MAS Design System & Reusable Components
Enterprise-grade UI/UX component library for consistent design across all pages.
"""

import streamlit as st
from typing import Optional, List, Dict, Any
import plotly.graph_objects as go
import plotly.express as px

# ============================================================================
# COLOR PALETTE - Sustainability-Inspired
# ============================================================================
COLORS = {
    "primary": "#166534",        # Deep forest green
    "primary_light": "#15803D",  # Emerald green
    "accent": "#10B981",          # Bright emerald
    "background": "#F7F9F7",      # Off-white
    "surface": "#FFFFFF",         # White
    "text_primary": "#17231D",    # Charcoal
    "text_secondary": "#69776E",  # Muted gray
    "border": "#E5EBE6",          # Subtle border
    "warning": "#F59E0B",         # Amber
    "danger": "#DC2626",          # Red
    "success": "#16A34A",         # Green
    "success_light": "#D1FAE5",   # Light green bg
    "warning_light": "#FEF3C7",   # Light amber bg
    "danger_light": "#FEE2E2",    # Light red bg
    "info": "#3B82F6",            # Blue
    "info_light": "#EFF6FF",      # Light blue bg
}

# ============================================================================
# TYPOGRAPHY HIERARCHY
# ============================================================================
TYPOGRAPHY = {
    "page_title": {"size": 32, "weight": 700, "family": "sans-serif"},
    "section_title": {"size": 24, "weight": 600, "family": "sans-serif"},
    "subsection_title": {"size": 18, "weight": 600, "family": "sans-serif"},
    "body": {"size": 14, "weight": 400, "family": "sans-serif"},
    "label": {"size": 12, "weight": 500, "family": "sans-serif"},
    "monospace": {"size": 12, "weight": 400, "family": "monospace"},
}

# ============================================================================
# SPACING SCALE
# ============================================================================
SPACING = {
    "xs": "0.25rem",
    "sm": "0.5rem",
    "md": "1rem",
    "lg": "1.5rem",
    "xl": "2rem",
    "2xl": "3rem",
    "3xl": "4rem",
}

# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================
def apply_global_styles():
    """Apply consistent global CSS styling."""
    css = f"""
    <style>
    :root {{
        --primary: {COLORS['primary']};
        --primary-light: {COLORS['primary_light']};
        --accent: {COLORS['accent']};
        --background: {COLORS['background']};
        --surface: {COLORS['surface']};
        --text-primary: {COLORS['text_primary']};
        --text-secondary: {COLORS['text_secondary']};
        --border: {COLORS['border']};
        --warning: {COLORS['warning']};
        --danger: {COLORS['danger']};
        --success: {COLORS['success']};
    }}

    * {{
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }}

    body {{
        background-color: {COLORS['background']};
        color: {COLORS['text_primary']};
        line-height: 1.6;
    }}

    /* Streamlit overrides */
    .main {{
        padding: 0;
        background-color: {COLORS['background']};
    }}

    [data-testid="stAppViewContainer"] {{
        background-color: {COLORS['background']};
    }}

    /* Buttons */
    .stButton > button {{
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
    }}

    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(22, 101, 52, 0.15);
    }}

    /* Primary buttons */
    .stButton > button[kind="primary"] {{
        background-color: {COLORS['primary']} !important;
        color: white !important;
    }}

    /* Cards */
    [data-testid="stMetric"] {{
        background-color: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }}

    /* Tables */
    .stDataFrame {{
        border-radius: 8px;
        border: 1px solid {COLORS['border']};
        overflow: hidden;
    }}

    /* Input fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {{
        border-radius: 8px;
        border: 1px solid {COLORS['border']} !important;
        padding: 10px 12px;
        font-size: 14px;
    }}

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {{
        border-color: {COLORS['primary']} !important;
        box-shadow: 0 0 0 3px rgba(22, 101, 52, 0.1);
    }}

    /* Slider */
    .stSlider > div > div > div {{
        background-color: {COLORS['border']};
    }}

    .stSlider > div > div > div > div {{
        background-color: {COLORS['primary']};
    }}

    /* Expander */
    .streamlit-expanderHeader {{
        background-color: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        padding: 12px 16px;
    }}

    .streamlit-expanderHeader:hover {{
        background-color: {COLORS['background']};
    }}

    /* Tabs */
    [data-baseweb="tab-list"] {{
        border-bottom: 2px solid {COLORS['border']};
    }}

    [data-baseweb="tab"] {{
        color: {COLORS['text_secondary']};
    }}

    [aria-selected="true"] [data-baseweb="tab"] {{
        color: {COLORS['primary']};
        border-bottom: 3px solid {COLORS['primary']};
    }}

    /* Alerts and messages */
    .stAlert {{
        border-radius: 8px;
        border-left: 4px solid;
    }}

    .stSuccess {{
        background-color: {COLORS['success_light']};
        border-color: {COLORS['success']};
    }}

    .stWarning {{
        background-color: {COLORS['warning_light']};
        border-color: {COLORS['warning']};
    }}

    .stError {{
        background-color: {COLORS['danger_light']};
        border-color: {COLORS['danger']};
    }}

    .stInfo {{
        background-color: {COLORS['info_light']};
        border-color: {COLORS['info']};
    }}

    /* Scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
    }}

    ::-webkit-scrollbar-track {{
        background: {COLORS['background']};
    }}

    ::-webkit-scrollbar-thumb {{
        background: {COLORS['border']};
        border-radius: 4px;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: {COLORS['text_secondary']};
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ============================================================================
# REUSABLE COMPONENTS
# ============================================================================

def render_sidebar():
    """Render premium sidebar navigation."""
    with st.sidebar:
        st.markdown(
            f"""
            <div style='padding: 24px 0; border-bottom: 1px solid {COLORS['border']};'>
                <h2 style='margin: 0; color: {COLORS['primary']}; font-size: 24px; font-weight: 700;'>
                    🍛 FoodRescue-MAS
                </h2>
                <p style='margin: 8px 0 0 0; color: {COLORS['text_secondary']}; font-size: 12px; font-weight: 500;'>
                    Intelligent Food Rescue Operations
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)


def render_page_header(
    title: str,
    subtitle: Optional[str] = None,
    icon: str = "📊"
):
    """Render a professional page header."""
    col1, col2 = st.columns([1, 10])
    with col1:
        st.markdown(f"<h1 style='font-size: 32px; margin: 0;'>{icon}</h1>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<h1 style='font-size: 32px; margin: 0; color: {COLORS['primary']};'>{title}</h1>", unsafe_allow_html=True)
        if subtitle:
            st.markdown(f"<p style='color: {COLORS['text_secondary']}; margin: 8px 0 0 0;'>{subtitle}</p>", unsafe_allow_html=True)
    st.markdown(f"<hr style='border: none; border-top: 1px solid {COLORS['border']}; margin: 24px 0;'>", unsafe_allow_html=True)


def render_kpi_card(
    label: str,
    value: str,
    icon: str = "📊",
    subtitle: Optional[str] = None,
    trend: Optional[str] = None,
    color: str = "primary"
):
    """Render a premium KPI card."""
    accent_color = COLORS.get(color, COLORS['primary'])
    
    html = f"""
    <div style='
        background: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
        cursor: default;
    ' onmouseover="this.style.boxShadow='0 4px 12px rgba(22, 101, 52, 0.1)'; this.style.transform='translateY(-2px)'"
       onmouseout="this.style.boxShadow='0 1px 3px rgba(0, 0, 0, 0.05)'; this.style.transform='translateY(0)'">
        <div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px;'>
            <div style='font-size: 24px;'>{icon}</div>
            <div style='font-size: 12px; color: {COLORS['text_secondary']};'>{label}</div>
        </div>
        <div style='font-size: 28px; font-weight: 700; color: {accent_color}; margin-bottom: 8px;'>
            {value}
        </div>
        {f'<div style="font-size: 12px; color: {COLORS["text_secondary"]};">{subtitle}</div>' if subtitle else ''}
        {f'<div style="font-size: 12px; color: {COLORS["success"]}; margin-top: 8px;"><strong>{trend}</strong></div>' if trend else ''}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_status_badge(status: str) -> str:
    """Return HTML for status badge."""
    status_config = {
        "dispatch": {"color": COLORS['success'], "bg": COLORS['success_light'], "label": "✓ Dispatch"},
        "hold": {"color": COLORS['warning'], "bg": COLORS['warning_light'], "label": "⏳ Hold"},
        "discard": {"color": COLORS['danger'], "bg": COLORS['danger_light'], "label": "✗ Discard"},
        "no_pickup": {"color": COLORS['text_secondary'], "bg": COLORS['background'], "label": "— No Pickup"},
        "success": {"color": COLORS['success'], "bg": COLORS['success_light'], "label": "✓ Success"},
        "failed": {"color": COLORS['danger'], "bg": COLORS['danger_light'], "label": "✗ Failed"},
        "pending": {"color": COLORS['warning'], "bg": COLORS['warning_light'], "label": "⏳ Pending"},
    }
    
    config = status_config.get(status.lower(), status_config["pending"])
    
    return f"""
    <span style='
        background-color: {config['bg']};
        color: {config['color']};
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        border: 1px solid {config['color']};
    '>
        {config['label']}
    </span>
    """


def render_agent_card(
    agent_name: str,
    agent_role: str,
    status: str,
    latency_ms: float,
    icon: str = "🤖"
):
    """Render a professional agent execution card."""
    status_color = {
        "success": COLORS['success'],
        "failed": COLORS['danger'],
        "running": COLORS['warning'],
        "pending": COLORS['text_secondary'],
    }.get(status, COLORS['text_secondary'])
    
    html = f"""
    <div style='
        background: {COLORS['surface']};
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    '>
        <div style='display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;'>
            <div style='display: flex; align-items: center; gap: 12px;'>
                <div style='font-size: 24px;'>{icon}</div>
                <div>
                    <div style='font-weight: 600; color: {COLORS['text_primary']}; font-size: 14px;'>{agent_name}</div>
                    <div style='font-size: 12px; color: {COLORS['text_secondary']};'>{agent_role}</div>
                </div>
            </div>
            <div style='text-align: right;'>
                <div style='
                    display: inline-block;
                    width: 10px;
                    height: 10px;
                    border-radius: 50%;
                    background-color: {status_color};
                    margin-bottom: 4px;
                '></div>
                <div style='font-size: 12px; color: {COLORS['text_secondary']};'>{status.title()}</div>
            </div>
        </div>
        <div style='font-size: 12px; color: {COLORS['text_secondary']};'>
            <strong>Latency:</strong> {latency_ms:.2f}ms
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_empty_state(
    icon: str = "📭",
    title: str = "No Data Available",
    subtitle: str = "Get started by taking action",
    cta_text: Optional[str] = None,
    cta_action: Optional[callable] = None
):
    """Render a professional empty state."""
    html = f"""
    <div style='
        text-align: center;
        padding: 60px 24px;
        background: {COLORS['surface']};
        border: 1px dashed {COLORS['border']};
        border-radius: 12px;
    '>
        <div style='font-size: 64px; margin-bottom: 16px;'>{icon}</div>
        <h3 style='color: {COLORS['text_primary']}; margin: 0 0 8px 0;'>{title}</h3>
        <p style='color: {COLORS['text_secondary']}; margin: 0; font-size: 14px;'>{subtitle}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
    
    if cta_text and cta_action:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button(cta_text, use_container_width=True):
                cta_action()


def render_metric_row(
    col_specs: List[Dict[str, Any]]
):
    """Render a row of metric cards."""
    cols = st.columns(len(col_specs))
    for col, spec in zip(cols, col_specs):
        with col:
            render_kpi_card(
                label=spec.get("label", ""),
                value=spec.get("value", "—"),
                icon=spec.get("icon", "📊"),
                subtitle=spec.get("subtitle"),
                trend=spec.get("trend"),
                color=spec.get("color", "primary")
            )


def render_section_header(title: str, icon: str = "📊"):
    """Render a section header."""
    st.markdown(
        f"<h3 style='color: {COLORS['primary']}; font-size: 18px; font-weight: 600; margin: 24px 0 16px 0;'>{icon} {title}</h3>",
        unsafe_allow_html=True
    )


# ============================================================================
# CHART CONFIGURATION
# ============================================================================

def get_chart_template() -> Dict:
    """Return consistent Plotly chart template."""
    return {
        "layout": {
            "plot_bgcolor": COLORS['background'],
            "paper_bgcolor": COLORS['surface'],
            "font": {"family": "Inter, sans-serif", "color": COLORS['text_primary']},
            "showlegend": True,
            "hovermode": "x unified",
            "margin": {"t": 30, "b": 30, "l": 40, "r": 20},
        },
        "config": {
            "responsive": True,
            "displayModeBar": False,
            "staticPlot": False,
        }
    }


def render_line_chart(
    data: Dict[str, List],
    title: str,
    x_label: str,
    y_label: str
) -> go.Figure:
    """Render a professional line chart."""
    fig = go.Figure()
    
    for key, values in data.items():
        if isinstance(values, list):
            fig.add_trace(go.Scatter(
                y=values,
                name=key,
                mode='lines+markers',
                line=dict(color=COLORS['primary'], width=3),
                marker=dict(size=6, color=COLORS['accent']),
                fill='tozeroy',
                fillcolor=f'rgba(22, 101, 52, 0.1)',
            ))
    
    template = get_chart_template()
    fig.update_layout(**template["layout"])
    fig.update_xaxes(title_text=x_label, gridcolor=COLORS['border'], showgrid=True)
    fig.update_yaxes(title_text=y_label, gridcolor=COLORS['border'], showgrid=True)
    
    return fig


def render_donut_chart(
    labels: List[str],
    values: List[float],
    title: str
) -> go.Figure:
    """Render a professional donut chart."""
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=[COLORS['primary'], COLORS['accent'], COLORS['warning'], COLORS['info']]),
        textinfo='label+percent',
        hoverinfo='label+value+percent',
    )])
    
    template = get_chart_template()
    fig.update_layout(
        **template["layout"],
        title={"text": title, "x": 0.5, "xanchor": "center"},
    )
    
    return fig


def render_bar_chart(
    data: Dict[str, List[float]],
    categories: List[str],
    title: str
) -> go.Figure:
    """Render a professional bar chart."""
    fig = go.Figure()
    
    colors = [COLORS['primary'], COLORS['accent'], COLORS['warning'], COLORS['info']]
    
    for idx, (key, values) in enumerate(data.items()):
        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            name=key,
            marker=dict(color=colors[idx % len(colors)]),
        ))
    
    template = get_chart_template()
    fig.update_layout(
        **template["layout"],
        barmode='group',
        xaxis_title="Category",
        yaxis_title="Value",
    )
    
    return fig

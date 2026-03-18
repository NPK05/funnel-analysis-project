"""
Funnel Analysis Dashboard
Multi-dataset interactive dashboard — Google Merch | Instacart | Olist
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from scipy.stats import norm
import warnings
warnings.filterwarnings('ignore')

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Funnel Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── THEME ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --navy:   #1a2744;
    --teal:   #0d9488;
    --amber:  #d97706;
    --coral:  #e05c3a;
    --slate:  #475569;
    --light:  #f8fafc;
    --border: #e2e8f0;
    --card:   #ffffff;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: #f1f5f9;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--navy) !important;
    border-right: none;
}
[data-testid="stSidebar"] * {
    color: #cbd5e1 !important;
}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
    font-family: 'DM Serif Display', serif !important;
}
[data-testid="stSidebar"] .stRadio label {
    color: #94a3b8 !important;
    font-size: 0.85rem !important;
}

/* Main area */
.main .block-container { padding: 1.5rem 2rem; max-width: 1400px; }

/* Hero header */
.hero {
    background: linear-gradient(135deg, var(--navy) 0%, #2d4a8a 60%, #1e3a6e 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%; right: -10%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(13,148,136,0.25) 0%, transparent 70%);
    border-radius: 50%;
}
.hero h1 {
    font-family: 'DM Serif Display', serif !important;
    font-size: 2rem !important;
    color: white !important;
    margin: 0 0 0.4rem 0 !important;
    letter-spacing: -0.5px;
}
.hero p { color: #94a3b8; margin: 0; font-size: 0.95rem; }
.hero .badge {
    display: inline-block;
    background: rgba(13,148,136,0.25);
    border: 1px solid rgba(13,148,136,0.5);
    color: #5eead4;
    padding: 0.2rem 0.75rem;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    margin-right: 0.5rem;
    margin-top: 0.75rem;
}

/* KPI cards */
.kpi-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
.kpi-card {
    flex: 1;
    background: white;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    border-left: 4px solid var(--teal);
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.kpi-card.amber { border-left-color: var(--amber); }
.kpi-card.coral { border-left-color: var(--coral); }
.kpi-card.navy  { border-left-color: var(--navy); }
.kpi-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--slate);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 0.3rem;
}
.kpi-value {
    font-family: 'DM Serif Display', serif;
    font-size: 1.9rem;
    color: var(--navy);
    line-height: 1.1;
}
.kpi-sub { font-size: 0.78rem; color: var(--slate); margin-top: 0.2rem; }

/* Section headers */
.section-header {
    font-family: 'DM Serif Display', serif;
    font-size: 1.25rem;
    color: var(--navy);
    margin: 1.5rem 0 0.75rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--border);
}

/* Finding callouts */
.finding {
    background: #f0fdf9;
    border-left: 4px solid var(--teal);
    border-radius: 0 8px 8px 0;
    padding: 0.85rem 1.1rem;
    margin: 0.75rem 0;
    font-size: 0.88rem;
    color: #134e4a;
}
.finding strong { color: var(--teal); }
.finding.warn {
    background: #fff7ed;
    border-left-color: var(--amber);
    color: #78350f;
}
.finding.warn strong { color: var(--amber); }
.finding.alert {
    background: #fef2f2;
    border-left-color: var(--coral);
    color: #7f1d1d;
}
.finding.alert strong { color: var(--coral); }

/* Tabs override */
[data-baseweb="tab-list"] { gap: 0.25rem; }
[data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    padding: 0.5rem 1.1rem !important;
    border-radius: 8px 8px 0 0 !important;
}

/* Insight box */
.insight-box {
    background: linear-gradient(135deg, #1a2744 0%, #1e3a6e 100%);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    color: #e2e8f0;
    font-size: 0.88rem;
    line-height: 1.7;
    margin: 0.75rem 0;
}
.insight-box h4 {
    color: #5eead4 !important;
    font-family: 'DM Serif Display', serif;
    margin: 0 0 0.4rem 0;
    font-size: 1rem;
}
</style>
""", unsafe_allow_html=True)


# ── HELPERS ───────────────────────────────────────────────────────────────────
def wilson_ci(s, n, z=1.96):
    if n == 0: return 0, 0
    p = s / n
    denom = 1 + z**2/n
    centre = (p + z**2/(2*n)) / denom
    margin = z * np.sqrt(p*(1-p)/n + z**2/(4*n**2)) / denom
    return (centre-margin)*100, (centre+margin)*100

COLORS = {
    'primary':  '#0d9488',
    'secondary':'#1a2744',
    'amber':    '#d97706',
    'coral':    '#e05c3a',
    'purple':   '#6d28d9',
    'slate':    '#64748b',
}

def plotly_layout(fig, title='', subtitle='', h=420, w=None):
    fig.update_layout(
        title=dict(
            text=f'{title}<br><sup style="color:#64748b">{subtitle}</sup>' if subtitle else title,
            x=0.5, xanchor='center',
            font=dict(family='DM Serif Display', size=17, color='#1a2744')
        ),
        font=dict(family='DM Sans', size=12, color='#334155'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=h,
        margin=dict(t=70, b=40, l=50, r=30),
        legend=dict(
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#e2e8f0', borderwidth=1,
            font=dict(size=11)
        )
    )
    if w: fig.update_layout(width=w)
    fig.update_xaxes(showgrid=False, linecolor='#e2e8f0', linewidth=1)
    fig.update_yaxes(gridcolor='#f1f5f9', linecolor='#e2e8f0')
    return fig

def kpi(label, value, sub='', color='teal'):
    return f"""
    <div class="kpi-card {color if color != 'teal' else ''}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>"""

def finding(text, kind=''):
    return f'<div class="finding {kind}">{text}</div>'


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1rem 0 1.5rem 0">
        <div style="font-family:'DM Serif Display',serif;font-size:1.3rem;color:white;line-height:1.2">
            Funnel Analysis<br>
        </div>
        <div style="font-size:0.78rem;color:#64748b;margin-top:0.4rem">
            NPK05 · 3 Datasets · 10 Phases
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Select Dataset")
    dataset = st.radio(
        label="dataset",
        options=[
            "🛒  Google Merchandise Store",
            "🥦  Instacart Grocery",
            "📦  Olist Brazilian E-Commerce"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.78rem;color:#475569;line-height:1.8">
        <div style="color:#94a3b8;font-weight:600;margin-bottom:0.5rem">PROJECT STATS</div>
        34M+ rows cleaned<br>
        38 data quality issues<br>
        6 statistical tests<br>
        15 interactive charts<br>
        3 funnel archetypes
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.78rem;color:#475569;line-height:1.8">
        <div style="color:#94a3b8;font-weight:600;margin-bottom:0.5rem">TECH STACK</div>
        Python · pandas · scipy<br>
        plotly · streamlit<br>
        chi-square · Mann-Whitney<br>
        Wilson CI · Spearman
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  GOOGLE MERCHANDISE STORE
# ══════════════════════════════════════════════════════════════════════════════
if "Google" in dataset:

    st.markdown("""
    <div class="hero">
        <h1>Google Merchandise Store</h1>
        <p>E-commerce conversion funnel analysis · Nov 2020 – Jan 2021</p>
        <span class="badge">CONVERSION FUNNEL</span>
        <span class="badge">719K EVENTS</span>
        <span class="badge">14.7K USERS</span>
        <span class="badge">3 MONTHS</span>
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    st.markdown('<div class="kpi-row">' +
        kpi("Overall CVR", "32.4%", "ATC → Purchase · CI [31.6%, 33.2%]") +
        kpi("ATC → Checkout", "51.0%", "Industry avg ~70% · Primary leak", "amber") +
        kpi("Revenue Leakage", "$552K", "3-month window · ~$2.2M annualized", "coral") +
        kpi("Avg Order Value", "$65.12", "Per purchasing session", "navy") +
    '</div>', unsafe_allow_html=True)

    # Tabs
    t1, t2, t3, t4, t5 = st.tabs([
        "📉 Funnel Overview",
        "📱 Device & Country",
        "🏷️ Category Analysis",
        "📅 Monthly Cohorts",
        "💰 Revenue Impact"
    ])

    # ── TAB 1: Funnel Overview ─────────────────────────────────────────────
    with t1:
        c1, c2 = st.columns([1, 1])

        with c1:
            st.markdown('<div class="section-header">Conversion Funnel</div>', unsafe_allow_html=True)
            fig = go.Figure(go.Funnel(
                y=['Add to Cart', 'Begin Checkout', 'Purchase'],
                x=[12545, 6404, 4066],
                textposition='inside',
                textinfo='value+percent initial+percent previous',
                opacity=0.88,
                marker=dict(
                    color=['#1a2744', '#0d9488', '#d97706'],
                    line=dict(width=2, color='white')
                ),
                connector=dict(line=dict(color='#e2e8f0', width=1, dash='dot'))
            ))
            fig.add_annotation(x=0.72, y=0.70,
                text='<b>49% drop-off</b><br>6,141 users lost',
                showarrow=True, arrowhead=2, arrowcolor='#e05c3a',
                ax=90, ay=0, font=dict(color='#e05c3a', size=11),
                bgcolor='rgba(255,255,255,0.95)', bordercolor='#e05c3a', borderwidth=1)
            fig.add_annotation(x=0.72, y=0.28,
                text='<b>36.5% drop-off</b><br>2,338 users lost',
                showarrow=True, arrowhead=2, arrowcolor='#e05c3a',
                ax=90, ay=0, font=dict(color='#e05c3a', size=11),
                bgcolor='rgba(255,255,255,0.95)', bordercolor='#e05c3a', borderwidth=1)
            plotly_layout(fig, 'Conversion Funnel', '12,545 users who added to cart', h=400)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.markdown('<div class="section-header">User Flow (Sankey)</div>', unsafe_allow_html=True)
            fig2 = go.Figure(go.Sankey(
                node=dict(
                    pad=15, thickness=20,
                    line=dict(color='white', width=0.5),
                    label=['All Users\n14,701', 'Add to Cart\n12,545', 'Never ATC\n2,156',
                           'Checkout\n6,404', 'Cart Abandoned\n6,141',
                           'Purchased\n4,066', 'Checkout Abandoned\n2,338'],
                    color=['#1a2744','#0d9488','#94a3b8',
                           '#d97706','#fbbf24','#059669','#e05c3a'],
                    x=[0.0,0.3,0.3,0.6,0.6,1.0,1.0],
                    y=[0.5,0.25,0.8,0.15,0.65,0.1,0.6]
                ),
                link=dict(
                    source=[0,0,1,1,3,3],
                    target=[1,2,3,4,5,6],
                    value=[12545,2156,6404,6141,4066,2338],
                    color=['rgba(13,148,136,0.25)','rgba(148,163,184,0.2)',
                           'rgba(217,119,6,0.25)','rgba(224,92,58,0.15)',
                           'rgba(5,150,105,0.25)','rgba(224,92,58,0.15)']
                )
            ))
            plotly_layout(fig2, 'User Flow', 'Where users convert and drop off', h=400)
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown(
            finding('<strong>Primary finding:</strong> 49% of users who add to cart never initiate checkout — this is the single biggest revenue leak. The problem is device-agnostic (mobile 28.25% vs desktop 27.28%, chi-square p=0.208, NOT significant).') +
            finding('<strong>Key insight:</strong> Mobile users are more hesitant to START checkout (50.5% vs 51.3%) but complete at a HIGHER rate (65.4% vs 62.3%) once they start. The fix is on the cart page CTA, not the checkout flow.', 'warn'),
            unsafe_allow_html=True
        )

    # ── TAB 2: Device & Country ───────────────────────────────────────────
    with t2:
        c1, c2 = st.columns([1, 1.2])

        with c1:
            st.markdown('<div class="section-header">CVR by Device</div>', unsafe_allow_html=True)
            devices = ['Desktop', 'Mobile', 'Tablet']
            metrics = {
                'ATC→Checkout': [51.3, 50.5, 53.3],
                'Checkout→Purchase': [62.3, 65.4, 59.6],
                'Overall CVR': [32.0, 33.1, 31.8]
            }
            fig = go.Figure()
            colors_dev = ['#1a2744', '#0d9488', '#d97706']
            for i, (metric, vals) in enumerate(metrics.items()):
                fig.add_trace(go.Bar(
                    name=metric, x=devices, y=vals,
                    marker_color=colors_dev[i], opacity=0.85,
                    text=[f'{v:.1f}%' for v in vals],
                    textposition='outside', textfont=dict(size=10)
                ))
            fig.add_hline(y=32.4, line_dash='dot', line_color='#94a3b8',
                         annotation_text='Overall avg 32.4%',
                         annotation_font_color='#94a3b8')
            plotly_layout(fig, 'Device Conversion Rates', 'p=0.208 — NOT statistically significant', h=380)
            fig.update_layout(barmode='group', yaxis=dict(range=[0,85], ticksuffix='%'))
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.markdown('<div class="section-header">CVR by Country (min 50 ATC users)</div>', unsafe_allow_html=True)
            countries = ['TR','RU','PH','CO','JP','NL','FR','IE','BR','DE','US','TW','IN','CA','CN','KR','ID','CH','BE']
            cvrs = [42.6,41.8,41.2,40.9,40.6,38.8,38.5,37.2,37.0,35.2,31.7,31.2,32.4,33.0,27.7,27.2,24.5,23.5,16.4]
            df_c = pd.DataFrame({'country':countries,'cvr':cvrs}).sort_values('cvr')
            bar_colors = ['#e05c3a' if v < 31.7 else '#0d9488' for v in df_c['cvr']]
            fig2 = go.Figure(go.Bar(
                y=df_c['country'], x=df_c['cvr'],
                orientation='h', marker_color=bar_colors, opacity=0.85,
                text=[f'{v:.1f}%' for v in df_c['cvr']], textposition='outside',
                textfont=dict(size=9)
            ))
            fig2.add_vline(x=31.7, line_dash='dash', line_color='#1a2744', line_width=1.5,
                          annotation_text='US 31.7%', annotation_font_color='#1a2744',
                          annotation_position='top right')
            plotly_layout(fig2, 'Country CVR', 'Green = above US baseline | Red = below', h=480)
            fig2.update_xaxes(range=[0,50], ticksuffix='%')
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown(
            finding('<strong>US is 1.4pp BELOW the global average (33.1%)</strong> — the largest market is underperforming. Turkey (42.6%), Russia (41.8%), Philippines (41.2%) all convert 10+ points higher than the US.') +
            finding('<strong>Country differences not yet statistically significant</strong> — sample sizes too small (FR: 234 users, p=0.119). Need 3x more data to confirm. This is an observed pattern, not a proven finding.', 'warn'),
            unsafe_allow_html=True
        )

    # ── TAB 3: Category Analysis ──────────────────────────────────────────
    with t3:
        st.markdown('<div class="section-header">Category Conversion Rates vs Apparel Baseline</div>', unsafe_allow_html=True)
        cats = ['Small Goods','Google','Stationery','Writing Instruments','Campus Collection',
                'Fun','Office','Drinkware','Bags','Electronics Acc.','Lifestyle',
                'New','Accessories','Clearance','Apparel','Shop by Brand','Notebooks & Journals']
        atcs = [3975,4206,6149,5382,40785,1017,23343,22068,23851,1933,25562,
                65046,60914,34162,265434,44481,16514]
        purs = [293,214,292,220,1456,36,798,680,671,48,583,1397,1173,633,4858,818,36]
        cvrs_cat = [round(p/a*100,1) for p,a in zip(purs,atcs)]
        sig = ['***','***','***','***','***','*','***','***','***','*','***','***','NO','***','baseline','***','***']

        df_cat = pd.DataFrame({
            'category':cats,'atc':atcs,'purchase':purs,'cvr':cvrs_cat,'sig':sig
        }).sort_values('cvr', ascending=True)

        cat_colors = ['#e05c3a' if v < 1.83 else
                      '#d97706' if v < 2.5 else '#0d9488'
                      for v in df_cat['cvr']]

        fig = go.Figure(go.Bar(
            y=df_cat['category'], x=df_cat['cvr'],
            orientation='h', marker_color=cat_colors, opacity=0.85,
            text=[f'{v:.1f}%' for v in df_cat['cvr']],
            textposition='outside', textfont=dict(size=10),
            customdata=df_cat[['atc','purchase','sig']].values,
            hovertemplate='<b>%{y}</b><br>CVR: %{x:.1f}%<br>ATC: %{customdata[0]:,}<br>Purchases: %{customdata[1]:,}<br>vs Apparel: %{customdata[2]}<extra></extra>'
        ))
        fig.add_vline(x=1.83, line_dash='dash', line_color='#94a3b8',
                     annotation_text='Apparel baseline 1.83%',
                     annotation_font_color='#94a3b8')
        plotly_layout(fig, 'Category CVR', 'Chi-square vs Apparel baseline · *** = p<0.001', h=520)
        fig.update_xaxes(range=[0,9], ticksuffix='%')
        st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                finding('<strong>Small Goods (7.4%) converts 4x better than Apparel (1.83%)</strong> — low price removes friction. Campus Collection (3.6%) and Office (3.4%) are statistically proven outperformers (p<0.001).'),
                unsafe_allow_html=True
            )
        with c2:
            st.markdown(
                finding('<strong>Notebooks & Journals: 0.2% CVR — catastrophically low.</strong> 16,514 ATC events → only 36 purchases. Something is broken: pricing, checkout bug, or product-market fit failure.', 'alert'),
                unsafe_allow_html=True
            )

    # ── TAB 4: Monthly Cohorts ────────────────────────────────────────────
    with t4:
        months = ['November', 'December', 'January']
        atc_m  = [2168, 6850, 3527]
        pur_m  = [1548, 1818,  700]
        cvr_m  = [71.4, 26.5, 19.8]
        lo_m   = [69.5, 25.5, 18.6]
        hi_m   = [73.3, 27.6, 21.2]
        atc_chk= [62.8, 53.3, 39.5]

        c1, c2 = st.columns([1.2, 1])
        with c1:
            st.markdown('<div class="section-header">Monthly CVR Trend with 95% CI</div>', unsafe_allow_html=True)
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=months + months[::-1], y=hi_m + lo_m[::-1],
                fill='toself', fillcolor='rgba(13,148,136,0.1)',
                line=dict(color='rgba(255,255,255,0)'),
                showlegend=False, name='95% CI'
            ))
            fig.add_trace(go.Scatter(
                x=months, y=cvr_m, mode='lines+markers+text',
                name='Overall CVR', line=dict(color='#0d9488', width=3),
                marker=dict(size=12, color='#0d9488', line=dict(width=2, color='white')),
                text=[f'<b>{v:.1f}%</b>' for v in cvr_m],
                textposition='top center', textfont=dict(size=13)
            ))
            fig.add_trace(go.Scatter(
                x=months, y=atc_chk, mode='lines+markers',
                name='ATC→Checkout', line=dict(color='#d97706', width=2, dash='dash'),
                marker=dict(size=8, color='#d97706')
            ))
            fig.add_annotation(x='November', y=71.4,
                text='<b>High-intent gift buyers</b>',
                showarrow=True, arrowhead=2, arrowcolor='#0d9488',
                ax=60, ay=-40, font=dict(color='#0d9488', size=10),
                bgcolor='rgba(255,255,255,0.9)', bordercolor='#0d9488', borderwidth=1)
            fig.add_annotation(x='December', y=26.5,
                text='<b>Holiday browsers dilute CVR</b>',
                showarrow=True, arrowhead=2, arrowcolor='#e05c3a',
                ax=70, ay=40, font=dict(color='#e05c3a', size=10),
                bgcolor='rgba(255,255,255,0.9)', bordercolor='#e05c3a', borderwidth=1)
            plotly_layout(fig, 'Monthly Conversion Rates',
                         'Shaded = 95% CI · All pairwise differences p < 0.001', h=420)
            fig.update_yaxes(range=[0, 90], ticksuffix='%')
            fig.update_layout(legend=dict(orientation='h', y=-0.15))
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.markdown('<div class="section-header">Monthly Volume vs Conversion</div>', unsafe_allow_html=True)
            fig2 = make_subplots(specs=[[{'secondary_y': True}]])
            fig2.add_trace(go.Bar(
                x=months, y=atc_m, name='ATC Users',
                marker_color='#1a2744', opacity=0.7
            ), secondary_y=False)
            fig2.add_trace(go.Scatter(
                x=months, y=cvr_m, name='CVR %',
                mode='lines+markers',
                line=dict(color='#0d9488', width=3),
                marker=dict(size=10, color='#0d9488')
            ), secondary_y=True)
            plotly_layout(fig2, 'Traffic vs Conversion',
                         'December has 3x traffic but 37% of November CVR', h=420)
            fig2.update_yaxes(title_text='ATC Users', secondary_y=False)
            fig2.update_yaxes(title_text='CVR %', ticksuffix='%', secondary_y=True)
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown(
            finding('<strong>November 71.4% vs December 26.5% vs January 19.8%</strong> — all three differences are statistically proven (chi-square p<0.001). These are fundamentally different user cohorts, not the same users in different months.') +
            finding('<strong>Note:</strong> November shows 113.7% checkout-to-purchase (>100%) — root cause: 935 users purchased without a recorded checkout event (GA4 session integrity gap flagged in cleaning). Overall CVR of 71.4% is correct.', 'warn'),
            unsafe_allow_html=True
        )

    # ── TAB 5: Revenue Impact ──────────────────────────────────────────────
    with t5:
        c1, c2 = st.columns([1.2, 1])
        with c1:
            st.markdown('<div class="section-header">Revenue Leakage Waterfall</div>', unsafe_allow_html=True)
            aov = 65.12
            fig = go.Figure(go.Waterfall(
                orientation='v', opacity=0.88,
                measure=['absolute','relative','relative','total'],
                x=['Potential Revenue\n(all ATC users)','Lost: Cart\nAbandonment',
                   'Lost: Checkout\nAbandonment','Revenue\nCaptured'],
                y=[12545*aov, -6141*aov, -2338*aov, 0],
                text=[f'${12545*aov:,.0f}',f'-${6141*aov:,.0f}',
                      f'-${2338*aov:,.0f}',f'${4066*aov:,.0f}'],
                textposition='outside', textfont=dict(size=11),
                connector=dict(line=dict(color='#e2e8f0', width=1)),
                decreasing=dict(marker=dict(color='#e05c3a')),
                increasing=dict(marker=dict(color='#0d9488')),
                totals=dict(marker=dict(color='#1a2744'))
            ))
            plotly_layout(fig, 'Revenue Leakage', f'AOV = ${aov} · 3-month window', h=420)
            fig.update_yaxes(tickprefix='$', tickformat=',.0f')
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.markdown('<div class="section-header">Recovery Scenarios</div>', unsafe_allow_html=True)
            scenarios = ['Current\n(51% checkout CVR)',
                         'Conservative\n(60% checkout CVR)',
                         'Industry Avg\n(70% checkout CVR)']
            revenues  = [4066*aov,
                         (int(12545*0.60)*0.635)*aov + 4066*aov - 4066*aov + 4066*aov,
                         (int(12545*0.70)*0.635)*aov]
            revenues  = [4066*aov,
                         4066*aov + int(12545*0.09)*0.635*aov,
                         4066*aov + int(12545*0.19)*0.635*aov]
            bar_c = ['#94a3b8','#0d9488','#1a2744']
            fig2 = go.Figure(go.Bar(
                x=scenarios, y=revenues,
                marker_color=bar_c, opacity=0.88,
                text=[f'${r:,.0f}' for r in revenues],
                textposition='outside', textfont=dict(size=11, color='#1a2744')
            ))
            plotly_layout(fig2, 'Revenue Recovery Scenarios',
                         'If checkout initiation rate improves', h=420)
            fig2.update_yaxes(tickprefix='$', tickformat=',.0f', range=[0, max(revenues)*1.2])
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown(f"""
        <div class="insight-box">
            <h4>💡 Business Recommendation</h4>
            The ATC→Checkout gap vs industry average (51% vs 70%) represents the highest-ROI
            single fix in this dataset. Every 1pp improvement in checkout initiation rate
            recovers approximately <strong style="color:#5eead4">$5,000 in quarterly revenue</strong>.
            Reaching industry average (70%) would recover
            <strong style="color:#5eead4">~$98,000 per quarter</strong> (~$392K annualized).
            Fix priority: cart page CTA friction, not checkout flow or device experience.
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  INSTACART
# ══════════════════════════════════════════════════════════════════════════════
elif "Instacart" in dataset:

    st.markdown("""
    <div class="hero">
        <h1>Instacart Grocery Delivery</h1>
        <p>Retention funnel analysis · 206,209 users · 3.3M orders</p>
        <span class="badge">RETENTION FUNNEL</span>
        <span class="badge">206K USERS</span>
        <span class="badge">33.8M ROWS</span>
        <span class="badge">GROCERY PLATFORM</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="kpi-row">' +
        kpi("Loyalty Rate", "76.0%", "Users reaching 6+ orders · CI [75.9%, 76.2%]") +
        kpi("Users at Risk", "49,404", "Stopping at 3-5 orders · 24% of all users", "amber") +
        kpi("Cadence Gap", "21.7pp", "Weekly 81% vs Monthly 59.3% · p=0.000000", "coral") +
        kpi("Weekly LTV", "5x", "Weekly users place 33.8 vs 6.7 avg orders", "navy") +
    '</div>', unsafe_allow_html=True)

    t1, t2, t3, t4 = st.tabs([
        "📉 Retention Funnel",
        "📆 Ordering Cadence",
        "🛒 Department Analysis",
        "⏰ Order Timing"
    ])

    # ── TAB 1 ─────────────────────────────────────────────────────────────
    with t1:
        c1, c2 = st.columns([1, 1.1])

        with c1:
            st.markdown('<div class="section-header">Retention Curve</div>', unsafe_allow_html=True)
            orders_x = list(range(3, 31))
            pct_remaining = [100.0,95.8,84.9,76.0,68.6,62.2,56.8,52.1,47.9,44.3,
                             41.0,38.2,35.5,33.1,30.9,28.7,26.9,25.3,23.7,22.4,
                             21.0,19.9,18.8,17.8,16.9,16.0,15.3,14.6]
            fig = go.Figure()
            fig.add_vrect(x0=3,x1=5,fillcolor='#1a2744',opacity=0.05,line_width=0)
            fig.add_vrect(x0=6,x1=30,fillcolor='#0d9488',opacity=0.04,line_width=0)
            fig.add_trace(go.Scatter(
                x=orders_x, y=pct_remaining,
                mode='lines+markers', fill='tozeroy',
                fillcolor='rgba(13,148,136,0.08)',
                line=dict(color='#0d9488', width=3),
                marker=dict(size=4, color='#0d9488')
            ))
            fig.add_hline(y=76.0, line_dash='dash', line_color='#e05c3a', line_width=2,
                         annotation_text='76% loyal threshold', annotation_font_color='#e05c3a')
            fig.add_annotation(x=5, y=84.9,
                text='<b>Steepest drop</b><br>order 4→5<br>loses 10.9%',
                showarrow=True, arrowhead=2, arrowcolor='#e05c3a',
                ax=55, ay=-45, font=dict(color='#e05c3a', size=10),
                bgcolor='rgba(255,255,255,0.9)', bordercolor='#e05c3a', borderwidth=1)
            plotly_layout(fig, 'User Retention Curve',
                         '% of users still ordering at each order number', h=420)
            fig.update_xaxes(range=[3,30], dtick=3, title='Order number')
            fig.update_yaxes(ticksuffix='%', range=[0,110])
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.markdown('<div class="section-header">Order Progression Drop-off</div>', unsafe_allow_html=True)
            ord_nums = [3,4,5,6,7,8,9,10]
            pcts_prog = [100.0,95.8,84.9,76.0,68.6,62.2,56.8,52.1]
            drops = [0,4.2,10.9,8.9,7.4,5.6,5.4,4.7]
            bar_c2 = ['#e05c3a' if d == max(drops) else
                      '#d97706' if d > 7 else '#0d9488'
                      for d in drops]
            fig2 = make_subplots(specs=[[{'secondary_y': True}]])
            fig2.add_trace(go.Bar(
                x=[f'Order {o}' for o in ord_nums],
                y=pcts_prog, name='% Still Active',
                marker_color='#1a2744', opacity=0.6
            ), secondary_y=False)
            fig2.add_trace(go.Scatter(
                x=[f'Order {o}' for o in ord_nums],
                y=drops, name='Drop at this order',
                mode='lines+markers',
                line=dict(color='#e05c3a', width=2),
                marker=dict(size=9, color=bar_c2)
            ), secondary_y=True)
            plotly_layout(fig2, 'Where Users Drop Off',
                         'Bars = % remaining | Line = % lost at each step', h=420)
            fig2.update_yaxes(ticksuffix='%', title_text='% Still Active', secondary_y=False)
            fig2.update_yaxes(ticksuffix='%', title_text='% Dropped', secondary_y=True)
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown(
            finding('<strong>Order 4→5 is the critical intervention point</strong> — loses 10.9% of users at a single step. This is 2x the average drop rate at other steps. A nudge (discount, push notification) targeted at users after their 4th order is the single highest-ROI retention action.'),
            unsafe_allow_html=True
        )

    # ── TAB 2 ─────────────────────────────────────────────────────────────
    with t2:
        c1, c2 = st.columns([1, 1])
        segs  = ['Weekly','Bi-weekly','Every 3wk','Monthly']
        rates = [81.0, 82.1, 71.0, 59.3]
        avgo  = [33.8, 17.8,  9.2,  6.7]
        errs  = [0.4,  0.25, 0.35,  0.75]
        users_s=[31626,83508,73388,17673]
        seg_c = ['#0d9488','#1a2744','#d97706','#e05c3a']

        with c1:
            st.markdown('<div class="section-header">Loyalty Rate by Cadence (with 95% CI)</div>', unsafe_allow_html=True)
            fig = go.Figure(go.Bar(
                x=segs, y=rates, marker_color=seg_c, opacity=0.88,
                error_y=dict(type='data', array=errs, arrayminus=errs,
                             color='#334155', thickness=2, width=6),
                text=[f'<b>{r:.1f}%</b><br>n={u:,}' for r,u in zip(rates,users_s)],
                textposition='outside', textfont=dict(size=11)
            ))
            fig.add_hline(y=76.0, line_dash='dot', line_color='#94a3b8',
                         annotation_text='Overall avg 76.0%', annotation_font_color='#94a3b8')
            plotly_layout(fig, 'Loyalty Rate by Cadence',
                         'Chi-square weekly vs monthly: p = 0.000000', h=420)
            fig.update_yaxes(range=[0,100], ticksuffix='%')
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.markdown('<div class="section-header">Average Total Orders by Cadence</div>', unsafe_allow_html=True)
            fig2 = go.Figure(go.Bar(
                x=segs, y=avgo, marker_color=seg_c, opacity=0.88,
                text=[f'<b>{v:.1f}</b>' for v in avgo],
                textposition='outside', textfont=dict(size=12)
            ))
            fig2.add_hline(y=np.mean(avgo), line_dash='dot', line_color='#94a3b8',
                          annotation_text=f'Avg {np.mean(avgo):.1f}',
                          annotation_font_color='#94a3b8')
            plotly_layout(fig2, 'Average Total Orders',
                         'Mann-Whitney weekly vs monthly: p = 0.000000', h=420)
            fig2.update_yaxes(range=[0,42])
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown(f"""
        <div class="insight-box">
            <h4>💡 The Cadence Insight</h4>
            Weekly users place <strong style="color:#5eead4">33.8 orders on average</strong> vs
            6.7 for monthly users — a <strong style="color:#5eead4">5x lifetime value difference</strong>.
            The 21.7pp loyalty gap (81% vs 59.3%) is the strongest statistical finding in the
            entire project (chi-square = 2,731, p = 0.000000, non-overlapping CIs).
            Converting just 20% of monthly users (3,535 users) to bi-weekly cadence would
            generate approximately <strong style="color:#5eead4">37,000 additional orders</strong>.
        </div>
        """, unsafe_allow_html=True)

    # ── TAB 3 ─────────────────────────────────────────────────────────────
    with t3:
        depts = ['babies','dairy eggs','snacks','beverages','produce','deli',
                 'bakery','pantry','household','frozen','dry goods pasta','canned goods']
        loy   = [79.5,78.2,77.7,77.4,77.3,77.2,77.1,75.9,75.5,75.2,74.9,74.1]
        aords = [19.3,17.8,16.8,16.8,17.3,16.0,16.6,16.1,15.4,15.5,15.2,14.5]
        d_c = ['#0d9488' if v > 76 else '#d97706' if v > 75 else '#e05c3a' for v in loy]

        c1, c2 = st.columns([1,1])
        with c1:
            st.markdown('<div class="section-header">Loyalty Rate by First Order Department</div>', unsafe_allow_html=True)
            df_d = pd.DataFrame({'dept':depts,'loyalty':loy,'avg_orders':aords}).sort_values('loyalty')
            fig = go.Figure(go.Bar(
                y=df_d['dept'], x=df_d['loyalty'],
                orientation='h',
                marker_color=['#0d9488' if v > 76 else '#d97706' if v > 75 else '#e05c3a'
                              for v in df_d['loyalty']],
                opacity=0.88,
                text=[f'{v:.1f}%' for v in df_d['loyalty']],
                textposition='outside', textfont=dict(size=10)
            ))
            fig.add_vline(x=76.0, line_dash='dash', line_color='#94a3b8',
                         annotation_text='Avg 76.0%', annotation_font_color='#94a3b8')
            plotly_layout(fig, 'Loyalty by First Order Department',
                         'Chi-square vs canned goods baseline · p<0.05 all fresh depts', h=460)
            fig.update_xaxes(range=[70,84], ticksuffix='%')
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.markdown('<div class="section-header">Avg Total Orders by Department</div>', unsafe_allow_html=True)
            df_d2 = pd.DataFrame({'dept':depts,'avg_orders':aords}).sort_values('avg_orders')
            fig2 = go.Figure(go.Bar(
                y=df_d2['dept'], x=df_d2['avg_orders'],
                orientation='h',
                marker_color=['#0d9488' if v > 16.5 else '#d97706' if v > 15.5 else '#1a2744'
                              for v in df_d2['avg_orders']],
                opacity=0.88,
                text=[f'{v:.1f}' for v in df_d2['avg_orders']],
                textposition='outside', textfont=dict(size=10)
            ))
            plotly_layout(fig2, 'Avg Orders by Department',
                         'Babies users place 4.8 more orders than canned goods users', h=460)
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown(
            finding('<strong>Department effect is real but weak</strong> — max 5.4pp spread (79.5% babies vs 74.1% canned goods). Cadence is 4.5x more predictive. Prioritize cadence interventions over department-based onboarding.') +
            finding('<strong>Babies (79.5%, 19.3 avg orders)</strong> has both the highest loyalty rate and highest avg order count. Parents have the most predictable recurring need — baby formula and diapers run out on a fixed schedule.', 'warn'),
            unsafe_allow_html=True
        )

    # ── TAB 4 ─────────────────────────────────────────────────────────────
    with t4:
        st.markdown('<div class="section-header">Order Volume Heatmap — Day × Hour</div>', unsafe_allow_html=True)
        days = ['Saturday','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday']
        heatmap_vals = [
            [3841,2336,1376,933,782,1142,3254,12097,27445,39764,47244,49711,50144,52414,53077,52538,48173,38674,28755,22014,17795,14075,10945,6708],
            [3594,1791,1091,728,791,1581,5282,16294,33561,51027,54719,50640,46153,45832,45853,45504,43868,36005,28381,21699,15979,11716,8781,5507],
            [3007,1543,928,709,731,1377,4670,13012,24227,35635,38486,37437,35018,35957,36387,36711,36762,31438,25899,19680,14780,10458,7971,5251],
            [2870,1460,932,635,691,1322,4467,12157,22124,31694,35316,34543,32789,33439,34060,35208,34538,29786,24454,18862,13544,10077,8041,5078],
            [2571,1477,870,669,718,1306,4313,12274,21392,30779,34305,33132,31519,32021,32930,33435,33363,28722,23854,18921,13883,10583,8621,5513],
            [3124,1626,996,825,896,1530,4757,13132,23476,33503,37587,37087,34944,35514,36561,36660,35047,29269,23719,18301,13052,9320,7304,5158],
            [3217,1870,1182,844,784,1116,3170,11066,22439,30127,34813,36066,36261,36708,37791,37151,34693,29539,23494,17864,13054,10257,8319,5924],
        ]
        hours = [f'{h:02d}:00' for h in range(24)]
        fig = go.Figure(go.Heatmap(
            z=heatmap_vals, x=hours, y=days,
            colorscale=[[0,'#f0fdf9'],[0.5,'#0d9488'],[1.0,'#1a2744']],
            text=[[f'{v:,}' for v in row] for row in heatmap_vals],
            texttemplate='%{text}', textfont=dict(size=8),
            colorbar=dict(title='Orders', tickformat=',')
        ))
        plotly_layout(fig, 'Order Volume by Day and Hour',
                     'Saturday 10-11am is the peak window (52,414 orders)', h=380)
        fig.update_layout(margin=dict(t=70,b=40,l=100,r=30))
        st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                finding('<strong>Saturday 10-11am: 52,414 orders</strong> — peak of the entire week. Grocery delivery follows a predictable weekly planning routine: morning of the weekend, stock up for the week ahead.'),
                unsafe_allow_html=True
            )
        with c2:
            st.markdown(
                finding('<strong>Weekday morning dip (6-7am)</strong> is the quietest window across all days. This is the optimal time for system maintenance. Never schedule promotions before 8am on any day.', 'warn'),
                unsafe_allow_html=True
            )


# ══════════════════════════════════════════════════════════════════════════════
#  OLIST
# ══════════════════════════════════════════════════════════════════════════════
else:

    st.markdown("""
    <div class="hero">
        <h1>Olist Brazilian E-Commerce</h1>
        <p>Marketplace fulfilment funnel analysis · Sep 2016 – Oct 2018</p>
        <span class="badge">FULFILMENT FUNNEL</span>
        <span class="badge">99K ORDERS</span>
        <span class="badge">9 TABLES</span>
        <span class="badge">2 YEARS</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="kpi-row">' +
        kpi("Fulfilment Rate", "97.0%", "Orders reaching delivered · CI [96.9%, 97.1%]") +
        kpi("Late Delivery Rate", "8.11%", "7,822 orders late · CI [7.94%, 8.28%]", "amber") +
        kpi("Review Score Gap", "1.73pts", "Late 2.56 vs On-time 4.29 · p=0.000000", "coral") +
        kpi("Revenue at Risk", "R$1.85M", "Direct + reputation impact from late orders", "navy") +
    '</div>', unsafe_allow_html=True)

    t1, t2, t3, t4 = st.tabs([
        "📦 Fulfilment Funnel",
        "⭐ Delivery vs Reviews",
        "🗺️ Geographic Analysis",
        "💰 Revenue Impact"
    ])

    # ── TAB 1 ─────────────────────────────────────────────────────────────
    with t1:
        c1, c2 = st.columns([1, 1])

        with c1:
            st.markdown('<div class="section-header">Fulfilment Funnel</div>', unsafe_allow_html=True)
            stages_o = ['Created','Approved','Shipped','Delivered','Reviewed']
            counts_o = [99441,99281,97658,96476,95832]
            colors_o = ['#1a2744','#0d9488','#0d9488','#0d9488','#6d28d9']
            fig = go.Figure(go.Funnel(
                y=stages_o, x=counts_o,
                textposition='inside',
                textinfo='value+percent initial+percent previous',
                opacity=0.88,
                marker=dict(color=colors_o, line=dict(width=2, color='white')),
                connector=dict(line=dict(color='#e2e8f0', width=1, dash='dot'))
            ))
            fig.add_annotation(x=0.7, y='Shipped',
                text='<b>Biggest drop: 1,623 orders</b><br>Seller fulfilment failures',
                showarrow=True, arrowhead=2, arrowcolor='#e05c3a',
                ax=120, ay=0, font=dict(color='#e05c3a', size=11),
                bgcolor='rgba(255,255,255,0.9)', bordercolor='#e05c3a', borderwidth=1)
            plotly_layout(fig, 'Fulfilment Funnel',
                         '99,441 orders · 97% fulfilment rate', h=440)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.markdown('<div class="section-header">Drop-off by Failure Type</div>', unsafe_allow_html=True)
            fail_types = ['Payment\nFailure','Seller\nFulfilment\nFailure',
                          'Last Mile\nFailure','No Review\n(Non-response)']
            fail_counts = [160,1623,1182,644]
            fail_colors = ['#d97706','#e05c3a','#e05c3a','#94a3b8']
            fig2 = go.Figure(go.Bar(
                x=fail_types, y=fail_counts,
                marker_color=fail_colors, opacity=0.88,
                text=[f'{c:,}\n({c/99441*100:.1f}%)' for c in fail_counts],
                textposition='outside', textfont=dict(size=11)
            ))
            plotly_layout(fig2, 'Orders Lost by Stage',
                         'Root cause classification of all funnel drop-off', h=440)
            fig2.update_yaxes(range=[0,2100])
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown(
            finding('<strong>97% fulfilment rate is exceptional</strong> — for a marketplace connecting independent sellers. The fulfilment challenge is not drop-off quantity but delivery quality among the 97% that complete.') +
            finding('<strong>Seller fulfilment failure (1,623 orders)</strong> is the biggest operational gap — these customers paid and received nothing. Seller accountability scoring is the recommended fix.', 'alert'),
            unsafe_allow_html=True
        )

    # ── TAB 2 ─────────────────────────────────────────────────────────────
    with t2:
        buckets = ['>3wk early','2-3wk early','1-2wk early','0-7d early',
                   '1-7d late','1-2wk late','>2wk late']
        avg_sc  = [4.28,4.34,4.31,4.20,3.18,1.74,1.71]
        p5star  = [63.7,64.5,63.0,57.5,33.1, 7.9, 7.0]
        p1star  = [ 7.8, 6.0, 6.4, 7.1,29.6,68.2,69.5]
        counts_b= [10610,24176,36161,17220,4410,1744,1503]
        b_c = ['#0d9488','#0d9488','#0d9488','#1a2744','#d97706','#e05c3a','#991b1b']

        c1, c2 = st.columns([1,1])
        with c1:
            st.markdown('<div class="section-header">Avg Review Score by Delivery Timing</div>', unsafe_allow_html=True)
            fig = go.Figure(go.Bar(
                x=buckets, y=avg_sc, marker_color=b_c, opacity=0.88,
                text=[f'{v:.2f}' for v in avg_sc],
                textposition='outside', textfont=dict(size=11),
                customdata=counts_b,
                hovertemplate='<b>%{x}</b><br>Avg score: %{y:.2f}<br>Orders: %{customdata:,}<extra></extra>'
            ))
            fig.add_hline(y=4.16, line_dash='dash', line_color='#94a3b8',
                         annotation_text='Overall avg 4.16', annotation_font_color='#94a3b8')
            fig.add_vline(x=3.5, line_dash='dot', line_color='#e05c3a', line_width=2,
                         annotation_text='LATE THRESHOLD', annotation_font_color='#e05c3a',
                         annotation_position='top right')
            plotly_layout(fig, 'Review Score vs Delivery Timing',
                         'Mann-Whitney p=0.000000 · 1.73 point gap late vs on-time', h=420)
            fig.update_yaxes(range=[0,5.5])
            fig.update_xaxes(tickangle=-20)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.markdown('<div class="section-header">% 5-star vs % 1-star by Timing</div>', unsafe_allow_html=True)
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                name='% 5-star', x=buckets, y=p5star,
                marker_color='#0d9488', opacity=0.85,
                text=[f'{v:.1f}%' for v in p5star],
                textposition='outside', textfont=dict(size=9)
            ))
            fig2.add_trace(go.Bar(
                name='% 1-star', x=buckets, y=p1star,
                marker_color='#e05c3a', opacity=0.85,
                text=[f'{v:.1f}%' for v in p1star],
                textposition='outside', textfont=dict(size=9)
            ))
            fig2.add_vline(x=3.5, line_dash='dot', line_color='#e05c3a', line_width=2)
            plotly_layout(fig2, '5-star vs 1-star Rate',
                         'Green = 5-star rate | Red = 1-star rate', h=420)
            fig2.update_layout(barmode='group', yaxis=dict(ticksuffix='%',range=[0,85]))
            fig2.update_xaxes(tickangle=-20)
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown(f"""
        <div class="insight-box">
            <h4>💡 The Threshold Effect</h4>
            The relationship between delay and review score is <strong style="color:#5eead4">non-linear</strong>.
            Spearman r=-0.176 (weak linear correlation) understates the real effect
            because the damage is <strong style="color:#5eead4">threshold-based</strong>:
            crossing from "early" to "late" drops the median score from 5 to 2.
            Being 2 weeks early (4.34) is almost identical to being 3 weeks early (4.28) — customers don't reward earliness.
            But being 1 week late drops to 1.74 — customers punish lateness catastrophically.
            <strong style="color:#5eead4">The fix is never being late, not being earlier.</strong>
        </div>
        """, unsafe_allow_html=True)

    # ── TAB 3 ─────────────────────────────────────────────────────────────
    with t3:
        states = ['AL','MA','PI','CE','SE','BA','RJ','TO','PA','ES','MS','PB','RN','PE',
                  'SC','GO','DF','RS','MT','SP','MG','PR','RO']
        late_r = [23.9,19.7,16.0,15.3,15.2,14.0,13.5,12.8,12.4,12.2,11.6,11.0,10.8,10.8,
                  9.8,8.2,7.1,7.1,6.8,5.9,5.6,5.0,2.9]
        scores_s=[3.85,3.83,3.99,3.94,3.91,3.93,3.97,4.15,3.91,4.08,4.16,4.08,4.15,4.08,
                  4.13,4.11,4.13,4.18,4.15,4.25,4.19,4.24,4.17]
        orders_s=[397,717,476,1279,335,3256,12350,274,946,1995,701,517,474,1593,
                  2219,1253,1065,5345,886,40501,11354,4923,243]

        df_s = pd.DataFrame({'state':states,'late_rate':late_r,
                             'avg_score':scores_s,'orders':orders_s})
        df_s = df_s.sort_values('late_rate', ascending=True)

        c1, c2 = st.columns([1,1])
        with c1:
            st.markdown('<div class="section-header">Late Delivery Rate by State</div>', unsafe_allow_html=True)
            s_colors = ['#991b1b' if v>15 else '#e05c3a' if v>10 else
                       '#d97706' if v>7 else '#0d9488' for v in df_s['late_rate']]
            fig = go.Figure(go.Bar(
                y=df_s['state'], x=df_s['late_rate'],
                orientation='h', marker_color=s_colors, opacity=0.88,
                text=[f'{v:.1f}%' for v in df_s['late_rate']],
                textposition='outside', textfont=dict(size=9),
                customdata=df_s['orders'].values,
                hovertemplate='<b>%{y}</b><br>Late rate: %{x:.1f}%<br>Orders: %{customdata:,}<extra></extra>'
            ))
            fig.add_vline(x=5.9, line_dash='dash', line_color='#0d9488', line_width=1.5,
                         annotation_text='SP 5.9%', annotation_font_color='#0d9488',
                         annotation_position='top right')
            plotly_layout(fig, 'Late Rate by State',
                         'Chi-square vs SP · All differences p<0.001 except MG (p=0.254)', h=540)
            fig.update_xaxes(range=[0,30], ticksuffix='%')
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.markdown('<div class="section-header">Avg Review Score by State</div>', unsafe_allow_html=True)
            sc_colors = ['#0d9488' if v>=4.2 else '#d97706' if v>=4.0 else '#e05c3a'
                        for v in df_s['avg_score']]
            fig2 = go.Figure(go.Bar(
                y=df_s['state'], x=df_s['avg_score'],
                orientation='h', marker_color=sc_colors, opacity=0.88,
                text=[f'{v:.2f}' for v in df_s['avg_score']],
                textposition='outside', textfont=dict(size=9)
            ))
            fig2.add_vline(x=4.16, line_dash='dash', line_color='#94a3b8',
                          annotation_text='Overall 4.16', annotation_font_color='#94a3b8')
            plotly_layout(fig2, 'Avg Review Score by State',
                         'Same state order — pattern mirrors late rate', h=540)
            fig2.update_xaxes(range=[3.5,4.5])
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown(
            finding('<strong>AL (23.9%) has 4x the late rate of SP (5.9%)</strong> — northeast Brazil has a structural logistics infrastructure gap. Both differences are statistically proven (p<0.001).') +
            finding('<strong>MG (5.6%) is statistically indistinguishable from SP (p=0.254)</strong> — shares its logistics infrastructure. MG is the model for other states to replicate.', 'warn') +
            finding('<strong>RJ (13.5%, 12,350 orders)</strong> is the highest-priority fix — largest volume at a high late rate. Fixing RJ alone would rescue ~1,670 late orders.', 'alert'),
            unsafe_allow_html=True
        )

    # ── TAB 4 ─────────────────────────────────────────────────────────────
    with t4:
        c1, c2 = st.columns([1.2,1])
        with c1:
            st.markdown('<div class="section-header">Revenue Impact Waterfall</div>', unsafe_allow_html=True)
            fig = go.Figure(go.Waterfall(
                orientation='v', opacity=0.88,
                measure=['absolute','relative','relative','total'],
                x=['Revenue in\nLate Orders','Reputation Loss\n(1-star deterrence)',
                   'Partial Recovery\n(8%→4% late rate)','Net Revenue\nat Risk'],
                y=[1351234,-1139800,636710,0],
                text=['R$1,351,234','-R$1,139,800','+R$636,710','R$1,854,323'],
                textposition='outside', textfont=dict(size=11),
                connector=dict(line=dict(color='#e2e8f0', width=1)),
                decreasing=dict(marker=dict(color='#e05c3a')),
                increasing=dict(marker=dict(color='#0d9488')),
                totals=dict(marker=dict(color='#1a2744'))
            ))
            plotly_layout(fig, 'Revenue at Risk',
                         'AOV = R$160.99 · 7,822 late orders · 8.1% late rate', h=440)
            fig.update_yaxes(tickprefix='R$', tickformat=',.0f')
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.markdown('<div class="section-header">Review Score Distribution</div>', unsafe_allow_html=True)
            stars = [1,2,3,4,5]
            counts_rev = [9352,2921,7916,18888,56755]
            star_c = ['#991b1b','#e05c3a','#d97706','#0d9488','#065f46']
            fig2 = go.Figure(go.Bar(
                x=[f'{s} ⭐' for s in stars], y=counts_rev,
                marker_color=star_c, opacity=0.88,
                text=[f'{c:,}\n({c/sum(counts_rev)*100:.1f}%)' for c in counts_rev],
                textposition='outside', textfont=dict(size=10)
            ))
            plotly_layout(fig2, 'Review Score Distribution',
                         '59.2% give 5-stars · 9.8% give 1-star · Bimodal pattern', h=440)
            fig2.update_yaxes(range=[0,70000])
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown(f"""
        <div class="insight-box">
            <h4>💡 Priority Action Plan</h4>
            <strong style="color:#5eead4">1. Fix RJ first</strong> — 12,350 orders, 13.5% late rate,
            statistically proven (p=0.000000). Negotiating priority carrier SLAs for RJ routes
            would rescue ~1,670 late orders worth R$269K direct.<br><br>
            <strong style="color:#5eead4">2. Proactive late order communication</strong> — flag orders
            at risk T-3 days before estimated delivery. A R$20 voucher converts a near-certain
            1-star review into potential loyalty. Cost: R$20 × 7,822 = R$156K to protect R$1.35M.<br><br>
            <strong style="color:#5eead4">3. Northeast logistics investment (AL, MA, CE)</strong> —
            AL at 23.9% is 4x worse than SP. Buffer delivery estimates for northeast states the
            same way Olist already does for Amazon region states.
        </div>
        """, unsafe_allow_html=True)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;font-size:0.8rem;color:#94a3b8;padding:0.5rem 0">
    Funnel Analysis · NPK05 ·
    Google Merch | Instacart | Olist ·
    Phases 1–10 Complete ·
    <a href="https://github.com/NPK05/funnel-analysis-project"
       style="color:#0d9488;text-decoration:none">GitHub →</a>
</div>
""", unsafe_allow_html=True)

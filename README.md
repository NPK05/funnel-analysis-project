# Funnel Analysis Portfolio Project

Multi-company funnel analysis across three real-world datasets
representing three distinct funnel archetypes.

**Google Merchandise Store** --> conversion funnel  
**Instacart** --> retention funnel  
**Olist Brazilian E-Commerce** --> fulfilment funnel

---

## Project Summary

| Dataset | Funnel Type | Size | Key Finding |
|---|---|---|---|
| Google Merch | Conversion | 719K events, 14.7K users | 49% ATC→Checkout drop, $552K leakage |
| Instacart | Retention | 33.8M rows, 206K users | Weekly users worth 5x monthly users |
| Olist | Fulfilment | 99K orders, 9 tables | 1.73pt score gap late vs on-time delivery |

---

## Ten-Phase Workflow

| Phase | Name | Status |
|---|---|---|
| 1 | Problem definition and hypotheses | Complete |
| 2 | Environment setup | Complete |
| 3 | Data cleaning — all 3 datasets | Complete |
| 4 | Exploratory data analysis | Complete |
| 5 | Core funnel analysis | Complete |
| 6 | Statistical testing | Complete |
| 7 | Visualization and dashboard | Complete |
| 8 | Business insights | Complete |
| 9 | Cross-dataset comparison | Complete |
| 10 | Portfolio packaging | Complete |

---

## Key Findings

### Google Merchandise Store
- Overall CVR: **32.4%** (ATC → Purchase)
- Largest drop-off: **ATC → Checkout at 49%** the primary leak
- Device CVR: Mobile 28.25% vs Desktop 27.28% **NOT significant** (p=0.208)
- Best category: Campus Collection **3.6% CVR** vs Apparel 1.8%
- Monthly cohorts: November **71.4%** vs December **26.5%** (p<0.001)
- Revenue leakage: **$552,179** over 3 months (~$2.2M annualized)

### Instacart
- Overall loyalty rate: **76.0%** CI [75.9%, 76.2%]
- Steepest drop: order **4→5 loses 10.9%** of users
- Weekly cadence loyalty: **81.0%** vs Monthly **59.3%** 21.7pp gap (p=0.000000)
- Weekly users place **33.8 orders** on average vs 6.7 for monthly users
- Babies department: **79.5% loyalty**, 19.3 avg orders highest LTV

### Olist
- Fulfilment rate: **97.0%** CI [96.9%, 97.1%]
- Late delivery rate: **8.11%** CI [7.94%, 8.28%]
- Review score gap: **1.73 points** late vs on-time (Mann-Whitney p=0.000000)
- Once >1 week late: **68% of customers give 1 star**
- Revenue at risk: **R$1,854,323** from late deliveries and reputation damage

---

## Statistical Tests Applied

| Test | Use case | Key result |
|---|---|---|
| Chi-square | Comparing conversion rates between groups | Mobile vs Desktop: p=0.208 NOT significant |
| Chi-square | Category CVR differences | Campus vs Apparel: p<0.001 SIGNIFICANT |
| Chi-square | Cadence loyalty differences | Weekly vs Monthly: p=0.000000 |
| Mann-Whitney U | Comparing non-normal distributions | Late vs on-time scores: p=0.000000 |
| Spearman | Correlation between continuous variables | Delay vs score: r=-0.176 |
| Wilson CI | Precision bounds on proportions | Overall CVR: [31.6%, 33.2%] |

---

## Tech Stack
```
Python 3.11 | pandas 2.3.3 | numpy 2.4.3 | scipy 1.17.1
matplotlib | seaborn | plotly | streamlit
jupyter notebook | git
```

---

## Project Structure
```
funnel_analysis_project/
├── notebooks/
│   ├── 01_google_merch.ipynb    ← Phases 3-8
│   ├── 02_instacart.ipynb       ← Phases 3-8
│   ├── 03_olist.ipynb           ← Phases 3-8
│   └── 04_comparison.ipynb      ← Phase 9
├── outputs/
│   └── dashboard/               ← 15 interactive Plotly charts
├── scripts/
├── docs/
├── requirements.txt
└── README.md
```

---

## How to Run
```bash
# Clone and setup
git clone https://github.com/NPK05/funnel-analysis-project
cd funnel-analysis-project
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

# Download datasets (see notebooks for links)
# Place raw files in data/raw/

# Run notebooks in order
jupyter notebook
```

---

## Datasets

| Dataset | Source | License |
|---|---|---|
| Google Merchandise Store | Kaggle — GA4 Obfuscated Data | Public |
| Instacart Market Basket | Kaggle — Instacart 2017 | CC BY 4.0 |
| Olist Brazilian E-Commerce | Kaggle — Olist | CC BY-NC-SA 4.0 |

> Raw data files are not included in this repository (file size).
> Download links and instructions are in each notebook.

---

## Cross-Dataset Insight

The three datasets represent three fundamentally different
funnel problems:

**Conversion funnels** (Google Merch) — drop-off is a user decision.
Fix: reduce friction at the decision point.

**Retention funnels** (Instacart) — drop-off is habit failure.
Fix: behavioural nudges before the habit forms.

**Fulfilment funnels** (Olist) — drop-off is operational failure.
Fix: accountability and infrastructure investment.

The right intervention only becomes clear when you correctly
identify which type of funnel you are analysing.

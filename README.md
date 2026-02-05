# 🇪🇹🇪🇹Financial Inclusion Forecasting — Ethiopia🇪🇹🇪🇹
### Overview
Ethiopia
---

This project builds a data-driven forecasting system to analyze and predict financial inclusion in Ethiopia, focusing on Access (account ownership) and Usage (digital payment adoption) as defined by the World Bank Global Findex. The work is conducted in the context of Ethiopia’s rapid digital finance expansion, including Telebirr and M-Pesa market entry.

---
### Business Context

Despite significant growth in mobile money infrastructure and users, Ethiopia’s account ownership rate increased only marginally between 2021 and 2024. Stakeholders seek to understand:

What drives financial inclusion outcomes

How events, policies, and infrastructure investments affect adoption

How inclusion is likely to evolve in 2026–2027
---
### Dataset

ethiopia_fi_unified_data.csv

- observation: Survey and operational metrics

- event: Policies, product launches, market entries

- target: Policy goals

impact_links.csv: Modeled relationships between events and indicators

reference_codes.csv: Valid indicator and field definitions
---

### Task 1: Data Exploration & Enrichment

- Reviewed dataset schema, record types, indicators, and temporal coverage

- Analyzed event–indicator relationships via impact_links

- Identified challenges in assigning pillars to events

- Enriched data with additional indicators, events, and modeled relationships

- Documented all additions with sources, confidence, and rationale
---

### Task 2: Exploratory Data Analysis

- Assessed dataset coverage, quality, and gaps

- Analyzed account ownership trends (2011–2024) and growth rates

- Investigated the 2021–2024 inclusion slowdown

- Examined digital payment adoption, including:

    - Registered vs. active usage

    - Payment use cases (P2P, ATM, Telebirr activity)

- Analyzed infrastructure enablers:

    - 4G population coverage

    - Mobile subscription penetration

    - ATM usage as a proxy for cash infrastructure

- Conducted correlation analysis between infrastructure, usage, and access

- Built event timelines and overlaid them on indicator trends
----
### Task 3: Event Impact Modeling

- Built event-indicator association matrix from impact_links data
- Modeled temporal effects with immediate and gradual impact functions
- Incorporated comparable country evidence for events lacking local data
- Validated model predictions against historical Telebirr launch impacts
- Adjusted magnitude estimates based on observed vs. predicted discrepancies
- Documented confidence levels and uncertainty ranges for each impact estimate
- Created scenario-weighted impact models for different policy environments

----
### Task 4: Forecasting Access and Usage

- Developed trend regression models for account ownership (2012-2024)
- Created digital payment usage forecasting with ARIMA components
- Integrated event impacts into baseline trend projections
- Generated three scenarios: Optimistic, Base, and Pessimistic for 2025-2027
- Calculated confidence intervals using bootstrapping methods
- Compared model predictions against World Bank Findex benchmarks
- Identified key uncertainty drivers and data limitations

----
### Task 5: Dashboard Development

Built interactive Streamlit dashboard with four main pages
- Implemented data loading from CSV files with fallback mechanisms
- Created visualization system using Plotly for time series and forecasts
- Added interactive controls (date selectors, scenario toggles, metric filters)
- Implemented data export functionality for all visualizations
- Designed Ethiopia-themed UI with national flag colors and styling
- Added target tracking visualization for 60% inclusion goal
- Integrated answers to consortium's key questions in overview page

----
### Key Insights

- Infrastructure readiness has improved faster than inclusion outcomes

- Cash usage remains persistent despite digital expansion

- Account ownership stagnation likely reflects trust, literacy, and use-case barriers rather than infrastructure constraints

- Data gaps remain in disaggregated (gender, rural/urban) and usage-intensity metrics


-----

### 🚀 How to Run This Project

#### Prerequisites
- **Python 3.8 or higher** (Download from [python.org](https://www.python.org/downloads/))
- **Git** (Download from [git-scm.com](https://git-scm.com/downloads))

#### Step 1: Clone the Repository
```bash
git clone https://github.com/Elbethel-dan/ethiopia-fi-forecast.git
cd ethiopia-fi-forecast
```
#### Step 2: Set Up Virtual Environment
On Windows:
```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate
```
On macOS/Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```
#### Step 3: Install Dependencies
```bash 
pip install --upgrade pip
pip install -r requirements.txt
```
#### Step 4: Run the Dashboard
```bash 
# Navigate to dashboard folder
cd dashboard

# Run the Streamlit app
streamlit run app.py
```
# Financial Inclusion Forecasting — Ethiopia
### Overview

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

Task 2: Exploratory Data Analysis

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

### Key Insights

- Infrastructure readiness has improved faster than inclusion outcomes

- Cash usage remains persistent despite digital expansion

- Account ownership stagnation likely reflects trust, literacy, and use-case barriers rather than infrastructure constraints

- Data gaps remain in disaggregated (gender, rural/urban) and usage-intensity metrics
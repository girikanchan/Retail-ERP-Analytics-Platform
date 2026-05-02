Retail ERP Analytics Platform

Technology: MySQL, Microsoft Fabric, PySpark, Power BI, Data Vault 2.0

Problem:
    Small and mid-size retailers lose ~10–15% revenue due to stockouts, overstocking, and margin leakage caused by siloed systems and lack of real-time analytics.

Solution
    Designed and implemented a full-stack retail ERP with an enterprise-grade analytics platform using Data Vault 2.0 modeling:

Transactional Layer
    Built a normalized 30-table MySQL ERP schema covering inventory, procurement (3-way match), POS billing, and GST compliance.
Data Modeling (Data Vault 2.0)
    Modeled enterprise data using:
Hubs (Business keys: Product, Supplier, Store, Customer)
Links (Relationships: Sales, Procurement, Inventory Movements)
Satellites (Descriptive attributes with historization & auditability)
Enabled full historical tracking, audit trails, and schema flexibility.
LLM-Assisted Metadata Mapping (position this carefully)
Leveraged LLMs to:
Automate source-to-target mapping from ERP schema → Data Vault entities
Generate Hub/Link/Satellite classification suggestions
Assist in schema documentation and column-level lineage
(Avoid implying the LLM “designed” the architecture—it assisted, not replaced modeling decisions.)
Data Engineering (Microsoft Fabric)
Implemented Medallion architecture aligned with Data Vault:
Bronze: Raw ERP ingestion
Silver: Data Vault (Hubs, Links, Satellites)
Gold: Business marts (denormalized star schema for BI)
Built scalable PySpark ETL pipelines for incremental loading and historization.
Analytics & Intelligence Layer
Demand forecasting models
Supplier performance scorecards
Margin erosion detection (price vs cost drift)
Inventory health scoring (stockout risk, overstock index)
BI Layer (Power BI)
Developed dashboards with:
Inventory health tracking
Supplier performance analytics
Sales & margin trends
AP aging insights
Regional/store-level performance
What you improved (and why it matters)
Moving to Data Vault 2.0 → shows enterprise data warehousing maturity
Introducing LLM-assisted metadata engineering → signals modern AI + data integration skill
Aligning Medallion + Data Vault → demonstrates architecture coherence, not just tools
What interviewers may challenge you on

Be ready for these:

Why Data Vault over Star Schema?
→ Answer: scalability, auditability, schema evolution, parallel loading
How did you design Hubs/Links?
→ Must explain business keys vs surrogate keys clearly
How exactly did LLM help?
→ Give concrete example:
Input: ERP table schema
Output: Suggested Hub = Product, Satellite = Product attributes
Then: You validated + implemented
How do you handle historization?
→ Talk about:
Load timestamps
Hash diff
Type 2 behavior via Satellites
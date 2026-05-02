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
            LLM-Assisted Metadata Mapping.
Leveraged LLMs to:
            Automate source-to-target mapping from ERP schema → Data Vault entities
            Generate Hub/Link/Satellite classification suggestions
            Assist in schema documentation and column-level lineage


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

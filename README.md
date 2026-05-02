# 🛒 Retail ERP Analytics Platform

**Tech Stack:** MySQL · Microsoft Fabric · PySpark · Power BI · Data Vault 2.0

---

## 📌 Overview

Small and mid-size retailers typically lose **10–15% of revenue** due to:

* Stockouts
* Overstocking
* Margin leakage

These issues are primarily driven by **disconnected systems** and lack of **real-time analytics visibility**.

This project delivers a **full-stack Retail ERP + Analytics Platform** that integrates transactional systems with an enterprise-grade data architecture to enable **data-driven decision-making**.

---

## 🏗️ Architecture

The platform follows a **Data Vault 2.0 + Medallion Architecture**:

```
        Source Systems (MySQL ERP)
                    │
                    ▼
            ┌───────────────┐
            │   Bronze      │  → Raw ingestion
            └───────────────┘
                    │
                    ▼
            ┌───────────────┐
            │   Silver      │  → Data Vault Layer
            │ Hubs | Links | Satellites
            └───────────────┘
                    │
                    ▼
            ┌───────────────┐
            │    Gold       │  → Business marts (Star Schema)
            └───────────────┘
                    │
                    ▼
               Power BI Dashboards
```

---

## 🧩 Core Components

### 1️⃣ Transactional Layer (ERP System)

* Designed a **normalized MySQL schema (30+ tables)** covering:

  * Inventory Management
  * Procurement (3-way matching)
  * POS Billing
  * GST Compliance

---

### 2️⃣ Data Modeling – Data Vault 2.0

Implemented a scalable and auditable data model:

* **Hubs** → Business keys

  * Product, Supplier, Store, Customer

* **Links** → Relationships

  * Sales, Procurement, Inventory Movements

* **Satellites** → Contextual attributes

  * Historical tracking
  * Audit trails
  * Schema flexibility

✅ Benefits:

* Full historization
* Auditability
* Easy schema evolution

---

### 3️⃣ LLM-Assisted Metadata Mapping

Integrated LLM capabilities to accelerate data engineering:

* Automated **Source → Target Mapping**
* Suggested **Hub / Link / Satellite classification**
* Generated **schema documentation**
* Enabled **column-level lineage tracking**

---

### 4️⃣ Data Engineering (Microsoft Fabric + PySpark)

Implemented a **Medallion Architecture**:

| Layer  | Description                          |
| ------ | ------------------------------------ |
| Bronze | Raw ERP ingestion                    |
| Silver | Data Vault (Hubs, Links, Satellites) |
| Gold   | Business marts (Star schema)         |

* Built **PySpark ETL pipelines** for:

  * Incremental loading
  * Change data capture (CDC)
  * Historization

---

## 📊 Analytics & Intelligence Layer

Developed advanced analytics use cases:

* 📈 **Demand Forecasting**
* 🏭 **Supplier Performance Scorecards**
* 💰 **Margin Erosion Detection** (Price vs Cost drift)
* 📦 **Inventory Health Scoring**

  * Stockout risk
  * Overstock index

---

## 📉 BI Layer (Power BI Dashboards)

Created interactive dashboards for:

* Inventory Health Monitoring
* Supplier Performance Analytics
* Sales & Margin Trends
* Accounts Payable Aging
* Regional & Store-Level Performance

---

## 🚀 Key Outcomes

* Enabled **real-time operational visibility**
* Reduced decision latency across supply chain
* Improved inventory optimization and margin tracking
* Delivered a **scalable, audit-ready data platform**

---

## 🧠 Key Learnings

* Practical implementation of **Data Vault 2.0 at scale**
* Aligning **Data Vault with Medallion Architecture**
* Leveraging **LLMs in data engineering workflows**
* Building **end-to-end analytics systems (ERP → BI)**

---

## 📌 Future Enhancements

* Real-time streaming (Kafka / Event Hub integration)
* ML-based dynamic pricing optimization
* Automated anomaly detection
* Data quality monitoring framework


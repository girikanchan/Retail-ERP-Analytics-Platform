import { useState } from "react";

const techBadges = [
  { label: "MySQL", color: "#00758F", bg: "#00758F15" },
  { label: "Microsoft Fabric", color: "#742774", bg: "#74277415" },
  { label: "PySpark", color: "#E25A1C", bg: "#E25A1C15" },
  { label: "Power BI", color: "#F2C811", bg: "#F2C81115" },
  { label: "Data Vault 2.0", color: "#10B981", bg: "#10B98115" },
];

const layers = [
  {
    id: "transactional",
    label: "Transactional Layer",
    icon: "🗄️",
    color: "#3B82F6",
    tag: "MySQL",
    headline: "30-Table Normalized ERP Schema",
    points: [
      "Inventory management & tracking",
      "Procurement with 3-way match validation",
      "POS billing & transaction processing",
      "GST compliance & tax computation",
    ],
  },
  {
    id: "modeling",
    label: "Data Vault 2.0",
    icon: "🏛️",
    color: "#8B5CF6",
    tag: "Modeling",
    headline: "Enterprise Data Modeling",
    points: [
      "Hubs: Product, Supplier, Store, Customer business keys",
      "Links: Sales, Procurement, Inventory movement relationships",
      "Satellites: Historized descriptive attributes",
      "Full audit trails & schema flexibility",
    ],
  },
  {
    id: "llm",
    label: "LLM-Assisted Mapping",
    icon: "🤖",
    color: "#EC4899",
    tag: "AI-Assisted",
    headline: "Metadata & Lineage Automation",
    points: [
      "Source-to-target mapping: ERP → Data Vault entities",
      "Hub/Link/Satellite classification suggestions",
      "Schema documentation generation",
      "Column-level lineage tracing",
    ],
    note: "LLM assisted metadata work — architectural decisions remained human-led.",
  },
  {
    id: "engineering",
    label: "Data Engineering",
    icon: "⚙️",
    color: "#F59E0B",
    tag: "Microsoft Fabric",
    headline: "Medallion Architecture + PySpark ETL",
    points: [
      "Bronze: Raw ERP data ingestion",
      "Silver: Data Vault (Hubs, Links, Satellites)",
      "Gold: Denormalized star schema for BI",
      "Incremental loading & historization pipelines",
    ],
  },
  {
    id: "analytics",
    label: "Analytics Layer",
    icon: "📊",
    color: "#10B981",
    tag: "Intelligence",
    headline: "Retail Intelligence Models",
    points: [
      "Demand forecasting models",
      "Supplier performance scorecards",
      "Margin erosion detection (price vs cost drift)",
      "Inventory health scoring (stockout risk, overstock index)",
    ],
  },
  {
    id: "bi",
    label: "BI Layer",
    icon: "📈",
    color: "#EF4444",
    tag: "Power BI",
    headline: "Executive & Operational Dashboards",
    points: [
      "Inventory health & replenishment tracking",
      "Supplier performance analytics",
      "Sales & margin trend analysis",
      "AP aging & regional store performance",
    ],
  },
];

const metrics = [
  { value: "10–15%", label: "Revenue leakage addressed", sub: "from stockouts & overstocking" },
  { value: "30", label: "MySQL tables", sub: "fully normalized ERP schema" },
  { value: "3-tier", label: "Medallion architecture", sub: "Bronze → Silver → Gold" },
  { value: "DV2.0", label: "Data Vault standard", sub: "with full historization" },
];

export default function App() {
  const [active, setActive] = useState(null);

  return (
    <div style={{
      background: "#0A0E1A",
      minHeight: "100vh",
      fontFamily: "'IBM Plex Mono', monospace",
      color: "#E2E8F0",
      padding: "0",
      overflowX: "hidden",
    }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600&family=Syne:wght@700;800&display=swap');

        * { box-sizing: border-box; margin: 0; padding: 0; }

        .hero-grid {
          background-image:
            linear-gradient(rgba(59,130,246,0.06) 1px, transparent 1px),
            linear-gradient(90deg, rgba(59,130,246,0.06) 1px, transparent 1px);
          background-size: 40px 40px;
        }

        .badge {
          display: inline-flex;
          align-items: center;
          padding: 3px 10px;
          border-radius: 4px;
          font-size: 11px;
          font-weight: 500;
          letter-spacing: 0.05em;
          border: 1px solid;
          font-family: 'IBM Plex Mono', monospace;
        }

        .layer-card {
          border: 1px solid #1E293B;
          border-radius: 8px;
          padding: 20px;
          background: #0F172A;
          cursor: pointer;
          transition: all 0.2s ease;
          position: relative;
          overflow: hidden;
        }
        .layer-card:hover {
          border-color: var(--card-color);
          background: #111827;
          transform: translateY(-2px);
        }
        .layer-card.active {
          border-color: var(--card-color);
          background: #111827;
        }
        .layer-card::before {
          content: '';
          position: absolute;
          top: 0; left: 0; right: 0;
          height: 2px;
          background: var(--card-color);
          opacity: 0;
          transition: opacity 0.2s;
        }
        .layer-card:hover::before, .layer-card.active::before {
          opacity: 1;
        }

        .metric-box {
          background: #0F172A;
          border: 1px solid #1E293B;
          border-radius: 6px;
          padding: 20px 16px;
          text-align: center;
          transition: border-color 0.2s;
        }
        .metric-box:hover { border-color: #3B82F6; }

        .arch-line {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 10px 16px;
          border-left: 2px solid;
          margin: 6px 0;
          border-radius: 0 6px 6px 0;
          background: #0A0E1A;
        }

        .section-label {
          font-size: 10px;
          letter-spacing: 0.2em;
          text-transform: uppercase;
          color: #64748B;
          margin-bottom: 8px;
        }

        .detail-panel {
          border: 1px solid #1E293B;
          border-radius: 8px;
          padding: 24px;
          background: #0D1425;
          margin-top: 12px;
          animation: fadeIn 0.2s ease;
        }

        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(8px); }
          to { opacity: 1; transform: translateY(0); }
        }

        .point-item {
          display: flex;
          gap: 10px;
          padding: 7px 0;
          font-size: 13px;
          color: #94A3B8;
          border-bottom: 1px solid #0F172A;
        }
        .point-item:last-child { border-bottom: none; }

        .note-box {
          background: #1A1F35;
          border-left: 3px solid #EC4899;
          padding: 10px 14px;
          border-radius: 0 6px 6px 0;
          margin-top: 14px;
          font-size: 12px;
          color: #94A3B8;
          font-style: italic;
        }

        .readme-block {
          background: #060A14;
          border: 1px solid #1E293B;
          border-radius: 8px;
          padding: 20px 24px;
          font-size: 12.5px;
          line-height: 1.9;
          color: #7DD3FC;
          white-space: pre-wrap;
          overflow-x: auto;
        }

        .tab-btn {
          padding: 8px 18px;
          border-radius: 4px;
          border: 1px solid #1E293B;
          background: transparent;
          color: #64748B;
          font-family: 'IBM Plex Mono', monospace;
          font-size: 12px;
          cursor: pointer;
          transition: all 0.15s;
        }
        .tab-btn.active, .tab-btn:hover {
          background: #1E293B;
          color: #E2E8F0;
          border-color: #334155;
        }

        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #0A0E1A; }
        ::-webkit-scrollbar-thumb { background: #1E293B; border-radius: 3px; }
      `}</style>

      {/* Hero */}
      <div className="hero-grid" style={{ padding: "56px 32px 40px", borderBottom: "1px solid #1E293B" }}>
        <div style={{ maxWidth: 860, margin: "0 auto" }}>
          <div className="section-label">📦 Portfolio Project</div>
          <h1 style={{
            fontFamily: "'Syne', sans-serif",
            fontSize: "clamp(28px, 5vw, 46px)",
            fontWeight: 800,
            lineHeight: 1.1,
            letterSpacing: "-0.02em",
            color: "#F8FAFC",
            marginBottom: 16,
          }}>
            Retail ERP<br />
            <span style={{ color: "#3B82F6" }}>Analytics Platform</span>
          </h1>
          <p style={{ fontSize: 14, color: "#64748B", maxWidth: 580, lineHeight: 1.7, marginBottom: 20 }}>
            A full-stack retail ERP with enterprise-grade analytics — from normalized MySQL schemas to Data Vault 2.0 modeling, Medallion architecture on Microsoft Fabric, and Power BI dashboards.
          </p>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
            {techBadges.map(b => (
              <span key={b.label} className="badge" style={{ color: b.color, borderColor: b.color + "40", background: b.bg }}>
                {b.label}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Problem/Solution strip */}
      <div style={{ padding: "28px 32px", borderBottom: "1px solid #1E293B", background: "#0D1120" }}>
        <div style={{ maxWidth: 860, margin: "0 auto", display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
          <div>
            <div className="section-label">⚠ Problem</div>
            <p style={{ fontSize: 13, color: "#94A3B8", lineHeight: 1.7 }}>
              Small and mid-size retailers lose <span style={{ color: "#EF4444", fontWeight: 600 }}>10–15% revenue</span> due to stockouts, overstocking, and margin leakage from siloed systems and lack of real-time analytics.
            </p>
          </div>
          <div>
            <div className="section-label">✦ Solution</div>
            <p style={{ fontSize: 13, color: "#94A3B8", lineHeight: 1.7 }}>
              End-to-end analytics platform built on <span style={{ color: "#10B981", fontWeight: 600 }}>Data Vault 2.0</span> modeling, Medallion architecture, and PySpark ETL — delivering historical traceability and real-time BI.
            </p>
          </div>
        </div>
      </div>

      {/* Metrics */}
      <div style={{ padding: "32px 32px 0", maxWidth: 860, margin: "0 auto" }}>
        <div className="section-label">At a glance</div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12, marginBottom: 36 }}>
          {metrics.map(m => (
            <div key={m.label} className="metric-box">
              <div style={{ fontSize: 22, fontWeight: 600, color: "#3B82F6", fontFamily: "'Syne', sans-serif", marginBottom: 4 }}>{m.value}</div>
              <div style={{ fontSize: 11, color: "#E2E8F0", fontWeight: 500, marginBottom: 2 }}>{m.label}</div>
              <div style={{ fontSize: 10, color: "#475569" }}>{m.sub}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Architecture layers */}
      <div style={{ padding: "0 32px 36px", maxWidth: 860, margin: "0 auto" }}>
        <div className="section-label">Architecture layers — click to expand</div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 10 }}>
          {layers.map(layer => (
            <div
              key={layer.id}
              className={`layer-card ${active === layer.id ? "active" : ""}`}
              style={{ "--card-color": layer.color }}
              onClick={() => setActive(active === layer.id ? null : layer.id)}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 10 }}>
                <span style={{ fontSize: 22 }}>{layer.icon}</span>
                <span className="badge" style={{ color: layer.color, borderColor: layer.color + "40", background: layer.color + "12", fontSize: 9 }}>
                  {layer.tag}
                </span>
              </div>
              <div style={{ fontSize: 12, fontWeight: 600, color: "#F1F5F9", marginBottom: 4 }}>{layer.label}</div>
              <div style={{ fontSize: 11, color: "#64748B" }}>{layer.headline}</div>
              <div style={{ fontSize: 10, color: layer.color, marginTop: 10, opacity: active === layer.id ? 0 : 1 }}>
                {active === layer.id ? "" : "▾ expand"}
              </div>
            </div>
          ))}
        </div>

        {/* Detail panel */}
        {active && (() => {
          const layer = layers.find(l => l.id === active);
          return (
            <div className="detail-panel" style={{ borderColor: layer.color + "30" }}>
              <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 16 }}>
                <span style={{ fontSize: 20 }}>{layer.icon}</span>
                <div>
                  <div style={{ fontFamily: "'Syne', sans-serif", fontSize: 16, fontWeight: 700, color: "#F8FAFC" }}>{layer.label}</div>
                  <div style={{ fontSize: 12, color: layer.color }}>{layer.headline}</div>
                </div>
              </div>
              {layer.points.map((p, i) => (
                <div key={i} className="point-item">
                  <span style={{ color: layer.color, flexShrink: 0 }}>→</span>
                  <span>{p}</span>
                </div>
              ))}
              {layer.note && <div className="note-box">ℹ {layer.note}</div>}
            </div>
          );
        })()}
      </div>

      {/* Data flow */}
      <div style={{ padding: "0 32px 36px", maxWidth: 860, margin: "0 auto" }}>
        <div className="section-label">Data flow — Medallion architecture</div>
        <div style={{ display: "flex", flexDirection: "column", gap: 0 }}>
          {[
            { label: "Bronze Layer", desc: "Raw ERP ingestion from MySQL", color: "#CD7F32", tag: "Raw" },
            { label: "Silver Layer", desc: "Data Vault 2.0 — Hubs, Links, Satellites", color: "#8B5CF6", tag: "DV2.0" },
            { label: "Gold Layer", desc: "Denormalized star schema for BI consumption", color: "#F59E0B", tag: "Marts" },
            { label: "BI Layer", desc: "Power BI dashboards & executive reporting", color: "#EF4444", tag: "Dashboards" },
          ].map((row, i, arr) => (
            <div key={row.label}>
              <div className="arch-line" style={{ borderColor: row.color }}>
                <span className="badge" style={{ color: row.color, borderColor: row.color + "40", background: row.color + "15", fontSize: 9 }}>{row.tag}</span>
                <span style={{ fontSize: 12, color: "#F1F5F9", fontWeight: 500 }}>{row.label}</span>
                <span style={{ fontSize: 11, color: "#64748B" }}>— {row.desc}</span>
              </div>
              {i < arr.length - 1 && (
                <div style={{ paddingLeft: 24, color: "#334155", fontSize: 16, lineHeight: 1 }}>↓</div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* README markdown preview */}
      <div style={{ padding: "0 32px 48px", maxWidth: 860, margin: "0 auto" }}>
        <div className="section-label">README.md — copy-ready markdown</div>
        <div className="readme-block">{`# 🏪 Retail ERP Analytics Platform

> **MySQL · Microsoft Fabric · PySpark · Power BI · Data Vault 2.0**

## Problem
Small and mid-size retailers lose **10–15% revenue** due to stockouts, overstocking,
and margin leakage caused by siloed systems and lack of real-time analytics.

## Solution
A full-stack retail ERP paired with an enterprise-grade analytics platform,
built on **Data Vault 2.0** modeling principles.

---

## Architecture

### 🗄️ Transactional Layer — MySQL
- Normalized **30-table ERP schema** covering inventory, procurement, POS billing
- **3-way match** procurement validation & GST compliance

### 🏛️ Data Vault 2.0 Modeling
| Component | Description |
|-----------|-------------|
| **Hubs** | Business keys: Product, Supplier, Store, Customer |
| **Links** | Relationships: Sales, Procurement, Inventory Movements |
| **Satellites** | Historized descriptive attributes with full auditability |

### 🤖 LLM-Assisted Metadata Mapping *(AI-assisted, not AI-designed)*
- Automated source-to-target mapping: ERP schema → Data Vault entities
- Hub/Link/Satellite classification suggestions
- Schema documentation & column-level lineage generation

> **Note**: LLMs assisted with metadata automation. All architectural decisions
> and modeling choices were human-led.

### ⚙️ Data Engineering — Microsoft Fabric & PySpark
\`\`\`
Bronze  →  Raw ERP ingestion
Silver  →  Data Vault (Hubs, Links, Satellites)
Gold    →  Business marts (star schema for BI)
\`\`\`
- Scalable PySpark ETL with incremental loading & historization

### 📊 Analytics & Intelligence Layer
- Demand forecasting models
- Supplier performance scorecards
- Margin erosion detection (price vs. cost drift)
- Inventory health scoring (stockout risk, overstock index)

### 📈 BI Layer — Power BI
- Inventory health & replenishment dashboards
- Supplier performance analytics
- Sales & margin trend tracking
- AP aging & regional store-level performance

---

## Tech Stack
\`MySQL\` \`Microsoft Fabric\` \`PySpark\` \`Power BI\` \`Data Vault 2.0\``}
        </div>
      </div>
    </div>
  );
}

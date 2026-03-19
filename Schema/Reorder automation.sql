-- ============================================================
-- FILE: Reorder_automation.sql
-- ============================================================

create TABLE reorder_rules (
    product_id           INT  NOT NULL,
    warehouse_id         INT  NOT NULL,
    min_stock_level      INT  NOT NULL DEFAULT 0,
    reorder_quantity     INT  NOT NULL DEFAULT 0,
    preferred_supplier_id INT NULL,                -- FIX: needed to auto-generate PO
    lead_time_days       INT  NOT NULL DEFAULT 0,  -- FIX: needed for reorder timing
    is_active            TINYINT NOT NULL DEFAULT 1,
    updated_at           TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (product_id, warehouse_id),
    FOREIGN KEY (product_id)            REFERENCES products(product_id),
    FOREIGN KEY (warehouse_id)          REFERENCES warehouses(warehouse_id),
    FOREIGN KEY (preferred_supplier_id) REFERENCES suppliers(supplier_id)
);
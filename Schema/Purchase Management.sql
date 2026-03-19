-- ============================================================
-- FILE: Purchase_Management.sql
-- ============================================================

-- ------------------------------------------------------------
-- Purchase Orders
-- ------------------------------------------------------------
CREATE TABLE purchase_orders (
    po_id                  INT AUTO_INCREMENT PRIMARY KEY,
    po_number              VARCHAR(30)    UNIQUE NOT NULL,
    supplier_id            INT            NOT NULL,
    warehouse_id           INT            NOT NULL,
    po_status              VARCHAR(20)    NOT NULL DEFAULT 'DRAFT',
                                          -- DRAFT, SENT, PARTIAL, RECEIVED, CANCELLED
    order_date             DATE           NOT NULL,
    expected_delivery_date DATE           NULL,
    total_amount           DECIMAL(14,2)  NOT NULL DEFAULT 0.00,
    created_by             INT            NULL,
    created_at             TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at             TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (supplier_id)  REFERENCES suppliers(supplier_id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id),
    FOREIGN KEY (created_by)   REFERENCES employees(employee_id)
);

-- ------------------------------------------------------------
-- Purchase Order Items
-- ------------------------------------------------------------
CREATE TABLE purchase_order_items (
    po_item_id        INT AUTO_INCREMENT PRIMARY KEY,
    po_id             INT            NOT NULL,
    product_id        INT            NOT NULL,
    quantity_ordered  DECIMAL(12,3)  NOT NULL,    -- FIX: was missing
    quantity_received DECIMAL(12,3)  NOT NULL DEFAULT 0.000,
    unit_cost         DECIMAL(12,2)  NOT NULL,
    line_total        DECIMAL(14,2)  GENERATED ALWAYS AS (quantity_ordered * unit_cost) STORED,
    FOREIGN KEY (po_id)        REFERENCES purchase_orders(po_id),
    FOREIGN KEY (product_id)   REFERENCES products(product_id)
);

-- ------------------------------------------------------------
-- Goods Receipt Note (GRN)  (NEW — PO → GRN → Invoice flow)
-- Physical confirmation that goods were received at the warehouse
-- ------------------------------------------------------------
CREATE TABLE goods_receipt_notes (
    grn_id         INT AUTO_INCREMENT PRIMARY KEY,
    grn_number     VARCHAR(30)   UNIQUE NOT NULL,
    po_id          INT           NOT NULL,
    warehouse_id   INT           NOT NULL,
    received_by    INT           NOT NULL,         -- employee_id
    receipt_date   DATE          NOT NULL,
    remarks        TEXT,
    grn_status     VARCHAR(20)   NOT NULL DEFAULT 'PENDING',
                                                   -- PENDING, ACCEPTED, REJECTED
    created_at     TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (po_id)        REFERENCES purchase_orders(po_id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id),
    FOREIGN KEY (received_by)  REFERENCES employees(employee_id)
);

CREATE TABLE grn_items (
    grn_item_id       INT AUTO_INCREMENT PRIMARY KEY,
    grn_id            INT            NOT NULL,
    po_item_id        INT            NOT NULL,
    product_id        INT            NOT NULL,
    quantity_received DECIMAL(12,3)  NOT NULL,
    quantity_accepted DECIMAL(12,3)  NOT NULL DEFAULT 0.000,
    quantity_rejected DECIMAL(12,3)  NOT NULL DEFAULT 0.000,
    unit_cost         DECIMAL(12,2)  NOT NULL,
    FOREIGN KEY (grn_id)      REFERENCES goods_receipt_notes(grn_id),
    FOREIGN KEY (po_item_id)  REFERENCES purchase_order_items(po_item_id),
    FOREIGN KEY (product_id)  REFERENCES products(product_id)
);
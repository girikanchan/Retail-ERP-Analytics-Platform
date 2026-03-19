-- ============================================================
-- FILE: 05_Inventory_valuation.sql
-- ============================================================

CREATE TABLE inventory_cost_layers (
    layer_id           INT AUTO_INCREMENT PRIMARY KEY,
    product_id         INT            NOT NULL,
    warehouse_id       INT            NOT NULL,
    po_item_id         INT            NULL,        -- FK added in Purchase_Management.sql
    quantity_received  DECIMAL(12,3)  NOT NULL,
    quantity_remaining DECIMAL(12,3)  NOT NULL,
    unit_cost          DECIMAL(12,2)  NOT NULL,
    received_date      DATE           NOT NULL,
    created_at         TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id)   REFERENCES products(product_id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
);
-- ============================================================
-- FILE: Inter_warehouse_transfer.sql
-- ============================================================

-- ------------------------------------------------------------
-- Warehouse Transfers (Header)

-- ------------------------------------------------------------
CREATE TABLE warehouse_transfers (
    transfer_id       INT AUTO_INCREMENT PRIMARY KEY,
    transfer_number   VARCHAR(30)   UNIQUE NOT NULL,
    from_warehouse_id INT           NOT NULL,
    to_warehouse_id   INT           NOT NULL,
    transfer_date     DATE          NOT NULL,
    status            VARCHAR(20)   NOT NULL DEFAULT 'PENDING',
                                    -- PENDING, IN_TRANSIT, COMPLETED, CANCELLED
    initiated_by      INT           NOT NULL,       -- employee_id
    completed_at      TIMESTAMP     NULL,
    notes             TEXT,
    created_at        TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at        TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (from_warehouse_id) REFERENCES warehouses(warehouse_id),  -- FIX: was missing
    FOREIGN KEY (to_warehouse_id)   REFERENCES warehouses(warehouse_id),  -- FIX: was missing
    FOREIGN KEY (initiated_by)      REFERENCES employees(employee_id)
);

-- ------------------------------------------------------------
-- Warehouse Transfer Items (Lines)
-- ------------------------------------------------------------
CREATE TABLE warehouse_transfer_items (
    transfer_item_id INT AUTO_INCREMENT PRIMARY KEY,
    transfer_id      INT            NOT NULL,
    product_id       INT            NOT NULL,
    quantity         DECIMAL(12,3)  NOT NULL,
    unit_cost        DECIMAL(12,2)  NULL,           -- FIX: needed for inventory valuation
    FOREIGN KEY (transfer_id)  REFERENCES warehouse_transfers(transfer_id),  -- FIX: was missing
    FOREIGN KEY (product_id)   REFERENCES products(product_id)
);
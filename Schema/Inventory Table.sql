-- ============================================================
-- FILE: Inventory_Table.sql

CREATE TABLE inventory_stock (
    product_id       INT            NOT NULL,
    warehouse_id     INT            NOT NULL,
    quantity_on_hand DECIMAL(12,3)  NOT NULL DEFAULT 0.000,
    last_updated     TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (product_id, warehouse_id),
    FOREIGN KEY (product_id)   REFERENCES products(product_id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
);

-- ------------------------------------------------------------
-- Inventory Transactions  (ledger — every stock movement)
-- ------------------------------------------------------------
CREATE TABLE inventory_transactions (
    transaction_id   INT AUTO_INCREMENT PRIMARY KEY,
    product_id       INT          NOT NULL,
    warehouse_id     INT          NOT NULL,
    transaction_type VARCHAR(20)  NOT NULL,       -- 'IN', 'OUT', 'TRANSFER', 'ADJUST'
    reference_type   VARCHAR(20)  NOT NULL,       -- 'PO', 'SALE', 'TRANSFER', 'ADJUSTMENT'
    reference_id     INT          NOT NULL,
    quantity         DECIMAL(12,3) NOT NULL,      -- positive = IN, negative = OUT
    unit_cost        DECIMAL(12,2) NULL,           -- cost at time of transaction
    created_by       INT          NULL,            -- employee_id
    transaction_date TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id)   REFERENCES products(product_id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id),
    FOREIGN KEY (created_by)   REFERENCES employees(employee_id)
);

-- ------------------------------------------------------------
-- Stock Adjustments  (NEW — damage, shrinkage, manual corrections)
-- ------------------------------------------------------------
CREATE TABLE stock_adjustments (
    adjustment_id    INT AUTO_INCREMENT PRIMARY KEY,
    product_id       INT           NOT NULL,
    warehouse_id     INT           NOT NULL,
    adjustment_type  VARCHAR(20)   NOT NULL,      -- 'DAMAGE', 'SHRINKAGE', 'MANUAL', 'COUNT'
    quantity_before  DECIMAL(12,3) NOT NULL,
    adjusted_qty     DECIMAL(12,3) NOT NULL,      -- positive = add, negative = deduct
    quantity_after   DECIMAL(12,3) NOT NULL,
    reason           TEXT,
    adjusted_by      INT           NOT NULL,       -- employee_id
    adjustment_date  TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id)   REFERENCES products(product_id),
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id),
    FOREIGN KEY (adjusted_by)  REFERENCES employees(employee_id)
);
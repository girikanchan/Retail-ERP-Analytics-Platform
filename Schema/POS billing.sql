-- ============================================================
-- FILE: 08_POS_billing.sql
-- ============================================================

-- ------------------------------------------------------------
-- POS Sales (Bill Header)
-- ------------------------------------------------------------
CREATE TABLE pos_sales (
    sale_id          INT AUTO_INCREMENT PRIMARY KEY,
    bill_number      VARCHAR(30)   UNIQUE NOT NULL,
    store_id         INT           NOT NULL,
    cashier_id       INT           NOT NULL,        -- employee_id
    customer_id      INT           NULL,             -- optional for walk-in
    sale_date        TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    subtotal_amount  DECIMAL(14,2) NOT NULL DEFAULT 0.00,
    discount_amount  DECIMAL(14,2) NOT NULL DEFAULT 0.00,
    tax_amount       DECIMAL(14,2) NOT NULL DEFAULT 0.00,
    total_amount     DECIMAL(14,2) NOT NULL DEFAULT 0.00,
    payment_method   VARCHAR(20)   NOT NULL DEFAULT 'CASH',
                                   -- CASH, CARD, UPI, CREDIT
    payment_status   VARCHAR(20)   NOT NULL DEFAULT 'PAID',
    created_at       TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (store_id)    REFERENCES stores(store_id),
    FOREIGN KEY (cashier_id)  REFERENCES employees(employee_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- ------------------------------------------------------------
-- POS Sale Items (Bill Lines)
-- ------------------------------------------------------------
CREATE TABLE pos_sale_items (
    sale_item_id    INT AUTO_INCREMENT PRIMARY KEY,
    sale_id         INT            NOT NULL,
    product_id      INT            NOT NULL,
    quantity        DECIMAL(12,3)  NOT NULL,
    unit_price      DECIMAL(12,2)  NOT NULL,
    discount_amount DECIMAL(12,2)  NOT NULL DEFAULT 0.00,
    tax_amount      DECIMAL(12,2)  NOT NULL DEFAULT 0.00,
    total_price     DECIMAL(12,2)  NOT NULL,        -- (unit_price * qty) - discount + tax
    FOREIGN KEY (sale_id)    REFERENCES pos_sales(sale_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
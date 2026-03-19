-- ============================================================
-- FILE: Purchase_order_and_invoice.sql
-- ============================================================

-- ------------------------------------------------------------
-- Supplier Invoices
-- ------------------------------------------------------------
CREATE TABLE supplier_invoices (
    invoice_id     INT AUTO_INCREMENT PRIMARY KEY,
    supplier_id    INT            NOT NULL,
    po_id          INT            NULL,
    grn_id         INT            NULL,             -- link to GRN for 3-way match
    invoice_number VARCHAR(50)    UNIQUE NOT NULL,
    invoice_date   DATE           NOT NULL,
    invoice_amount DECIMAL(14,2)  NOT NULL,
    tax_amount     DECIMAL(14,2)  NOT NULL DEFAULT 0.00,
    status         VARCHAR(20)    NOT NULL DEFAULT 'PENDING',
                                   -- PENDING, APPROVED, PAID, DISPUTED
    created_at     TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id),
    FOREIGN KEY (po_id)       REFERENCES purchase_orders(po_id),       -- FIX: was missing
    FOREIGN KEY (grn_id)      REFERENCES goods_receipt_notes(grn_id)
);

-- ------------------------------------------------------------
-- Supplier Payments
-- ------------------------------------------------------------
CREATE TABLE supplier_payments (
    payment_id        INT AUTO_INCREMENT PRIMARY KEY,
    invoice_id        INT            NOT NULL,
    payment_amount    DECIMAL(14,2)  NOT NULL,
    payment_date      DATE           NOT NULL,
    payment_method    VARCHAR(30)    NOT NULL DEFAULT 'BANK_TRANSFER',
                                     -- BANK_TRANSFER, CHEQUE, CASH, UPI
    reference_number  VARCHAR(50)    NULL,          -- cheque no / UTR / UPI ref
    notes             TEXT,
    created_at        TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (invoice_id) REFERENCES supplier_invoices(invoice_id)
);
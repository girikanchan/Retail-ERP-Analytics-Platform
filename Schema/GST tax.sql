-- ============================================================
-- FILE: GST_tax.sql
-- ============================================================

-- ------------------------------------------------------------
-- Tax Master  (CGST 9%, SGST 9%, IGST 18%, etc.)
-- ------------------------------------------------------------
CREATE TABLE tax_master (
    tax_id         INT AUTO_INCREMENT PRIMARY KEY,
    tax_name       VARCHAR(50)   NOT NULL,        -- e.g. 'GST 18%', 'CGST 9%'
    tax_percentage DECIMAL(5,2)  NOT NULL,
    tax_type       VARCHAR(20)   NOT NULL,        -- 'CGST', 'SGST', 'IGST', 'CESS'
    is_active      TINYINT(1)   NOT NULL DEFAULT 1,
    created_at     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Product → Tax mapping
-- ------------------------------------------------------------
CREATE TABLE product_tax_mapping (
    product_id  INT NOT NULL,
    tax_id      INT NOT NULL,
    PRIMARY KEY (product_id, tax_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (tax_id)     REFERENCES tax_master(tax_id)
);

-- ------------------------------------------------------------
-- GST Invoice Details  (NEW — required for GST compliance)
-- Stores the CGST/SGST/IGST split per sale or purchase invoice
-- ------------------------------------------------------------
CREATE TABLE gst_invoice_details (
    gst_detail_id   INT AUTO_INCREMENT PRIMARY KEY,
    reference_type  VARCHAR(20) NOT NULL,         -- 'SALE' or 'PURCHASE'
    reference_id    INT         NOT NULL,          -- sale_id or invoice_id
    tax_id          INT         NOT NULL,
    taxable_amount  DECIMAL(14,2) NOT NULL,
    tax_amount      DECIMAL(14,2) NOT NULL,
    created_at      TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tax_id) REFERENCES tax_master(tax_id)
);
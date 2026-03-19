-- ============================================================
-- FILE: Master_Tables.sql
-- ============================================================

-- ------------------------------------------------------------
-- Units of Measure (new table — required before products)
-- ------------------------------------------------------------
CREATE TABLE units_of_measure (
    uom_id        INT AUTO_INCREMENT PRIMARY KEY,
    uom_code      VARCHAR(10)  UNIQUE NOT NULL,   -- e.g. KG, PCS, LTR
    uom_name      VARCHAR(50)  NOT NULL,
    is_active     TINYINT(1)   NOT NULL DEFAULT 1,
    created_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Categories (new table — required before products)
-- ------------------------------------------------------------
CREATE TABLE categories (
    category_id   INT AUTO_INCREMENT PRIMARY KEY,
    category_code VARCHAR(20)  UNIQUE NOT NULL,
    category_name VARCHAR(100) NOT NULL,
    parent_id     INT          NULL,              -- for sub-categories
    is_active     TINYINT(1)   NOT NULL DEFAULT 1,
    created_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES categories(category_id)
);

-- ------------------------------------------------------------
-- Employees
-- ------------------------------------------------------------
CREATE TABLE employees (
    employee_id   INT AUTO_INCREMENT PRIMARY KEY,
    employee_code VARCHAR(20)  UNIQUE NOT NULL,
    first_name    VARCHAR(50),
    last_name     VARCHAR(50),
    role          VARCHAR(50),
    is_active     TINYINT(1)   NOT NULL DEFAULT 1,
    created_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Customers
-- ------------------------------------------------------------
CREATE TABLE customers (
    customer_id   INT AUTO_INCREMENT PRIMARY KEY,
    customer_code VARCHAR(20)  UNIQUE,
    customer_name VARCHAR(100),
    phone         VARCHAR(20),
    email         VARCHAR(100),
    address       TEXT,
    gstin         VARCHAR(20),                   -- GST Identification Number for B2B
    is_active     TINYINT(1)   NOT NULL DEFAULT 1,
    created_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Suppliers
-- ------------------------------------------------------------
CREATE TABLE suppliers (
    supplier_id    INT AUTO_INCREMENT PRIMARY KEY,
    supplier_code  VARCHAR(20)  UNIQUE,
    supplier_name  VARCHAR(100),
    contact_person VARCHAR(100),
    phone          VARCHAR(20),
    email          VARCHAR(100),
    address        TEXT,
    gstin          VARCHAR(20),                   -- mandatory for GST input credit
    payment_terms  VARCHAR(50),                   -- e.g. 'NET30', 'IMMEDIATE'
    is_active      TINYINT(1)  NOT NULL DEFAULT 1,
    created_at     TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Warehouses
-- ------------------------------------------------------------
CREATE TABLE warehouses (
    warehouse_id   INT AUTO_INCREMENT PRIMARY KEY,
    warehouse_code VARCHAR(20)  UNIQUE NOT NULL,
    warehouse_name VARCHAR(100) NOT NULL,
    address        TEXT,
    is_active      TINYINT(1)  NOT NULL DEFAULT 1,
    created_at     TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Stores  (NEW — was referenced in pos_sales but never defined)
-- ------------------------------------------------------------
CREATE TABLE stores (
    store_id      INT AUTO_INCREMENT PRIMARY KEY,
    store_code    VARCHAR(20)  UNIQUE NOT NULL,
    store_name    VARCHAR(100) NOT NULL,
    warehouse_id  INT          NOT NULL,          -- linked warehouse for stock
    address       TEXT,
    is_active     TINYINT(1)  NOT NULL DEFAULT 1,
    created_at    TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (warehouse_id) REFERENCES warehouses(warehouse_id)
);

-- ------------------------------------------------------------
-- Products
-- ------------------------------------------------------------
CREATE TABLE products (
    product_id     INT AUTO_INCREMENT PRIMARY KEY,
    sku            VARCHAR(30)    UNIQUE NOT NULL,
    product_name   VARCHAR(100)   NOT NULL,
    category_id    INT            NOT NULL,
    uom_id         INT            NOT NULL,
    hsn_code       VARCHAR(10)    NOT NULL,        -- mandatory for GST compliance
    purchase_price DECIMAL(12,2)  NOT NULL DEFAULT 0.00,
    selling_price  DECIMAL(12,2)  NOT NULL DEFAULT 0.00,
    reorder_level  INT            NOT NULL DEFAULT 0,
    is_active      TINYINT(1)    NOT NULL DEFAULT 1,
    created_at     TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (uom_id)      REFERENCES units_of_measure(uom_id)
);
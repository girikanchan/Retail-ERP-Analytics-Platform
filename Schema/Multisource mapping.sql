CREATE TABLE supplier_product_rules (
    supplier_id INT,
    product_id INT,
    priority_rank INT,
    PRIMARY KEY (supplier_id, product_id)
);

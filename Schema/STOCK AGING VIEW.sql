-- ============================================================
-- FILE: STOCK_AGING_VIEW.sql
-- ============================================================

CREATE VIEW vw_stock_aging AS
SELECT
    p.product_id,
    p.sku,
    p.product_name,
    w.warehouse_id,
    w.warehouse_name,                            
    ic.layer_id,
    ic.quantity_remaining,
    ic.unit_cost,
    ROUND(ic.quantity_remaining * ic.unit_cost, 2)              AS stock_value,
    ic.received_date,
    DATEDIFF(CURDATE(), ic.received_date)                       AS aging_days,
    CASE
        WHEN DATEDIFF(CURDATE(), ic.received_date) <= 30  THEN '0-30 days'
        WHEN DATEDIFF(CURDATE(), ic.received_date) <= 60  THEN '31-60 days'
        WHEN DATEDIFF(CURDATE(), ic.received_date) <= 90  THEN '61-90 days'
        ELSE '90+ days'
    END                                                         AS aging_bucket
FROM inventory_cost_layers ic
JOIN products   p ON ic.product_id   = p.product_id
JOIN warehouses w ON ic.warehouse_id = w.warehouse_id
WHERE ic.quantity_remaining > 0;
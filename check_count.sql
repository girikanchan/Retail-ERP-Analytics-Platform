SELECT 'units_of_measure'       AS table_name, COUNT(*) AS exact_count FROM units_of_measure        UNION ALL
SELECT 'categories',                           COUNT(*)                 FROM categories               UNION ALL
SELECT 'warehouses',                           COUNT(*)                 FROM warehouses               UNION ALL
SELECT 'stores',                               COUNT(*)                 FROM stores                   UNION ALL
SELECT 'employees',                            COUNT(*)                 FROM employees                UNION ALL
SELECT 'suppliers',                            COUNT(*)                 FROM suppliers                UNION ALL
SELECT 'customers',                            COUNT(*)                 FROM customers                UNION ALL
SELECT 'tax_master',                           COUNT(*)                 FROM tax_master               UNION ALL
SELECT 'products',                             COUNT(*)                 FROM products                 UNION ALL
SELECT 'product_tax_mapping',                  COUNT(*)                 FROM product_tax_mapping      UNION ALL
SELECT 'purchase_orders',                      COUNT(*)                 FROM purchase_orders          UNION ALL
SELECT 'purchase_order_items',                 COUNT(*)                 FROM purchase_order_items     UNION ALL
SELECT 'goods_receipt_notes',                  COUNT(*)                 FROM goods_receipt_notes      UNION ALL
SELECT 'grn_items',                            COUNT(*)                 FROM grn_items                UNION ALL
SELECT 'inventory_cost_layers',                COUNT(*)                 FROM inventory_cost_layers    UNION ALL
SELECT 'inventory_transactions',               COUNT(*)                 FROM inventory_transactions   UNION ALL
SELECT 'inventory_stock',                      COUNT(*)                 FROM inventory_stock          UNION ALL
SELECT 'supplier_invoices',                    COUNT(*)                 FROM supplier_invoices        UNION ALL
SELECT 'supplier_payments',                    COUNT(*)                 FROM supplier_payments        UNION ALL
SELECT 'pos_sales',                            COUNT(*)                 FROM pos_sales                UNION ALL
SELECT 'pos_sale_items',                       COUNT(*)                 FROM pos_sale_items           UNION ALL
SELECT 'warehouse_transfers',                  COUNT(*)                 FROM warehouse_transfers      UNION ALL
SELECT 'warehouse_transfer_items',             COUNT(*)                 FROM warehouse_transfer_items UNION ALL
SELECT 'stock_adjustments',                    COUNT(*)                 FROM stock_adjustments        UNION ALL
SELECT 'gst_invoice_details',                  COUNT(*)                 FROM gst_invoice_details      UNION ALL
SELECT 'reorder_rules',                        COUNT(*)                 FROM reorder_rules            UNION ALL
SELECT 'supplier_product_rules',               COUNT(*)                 FROM supplier_product_rules
ORDER BY table_name;
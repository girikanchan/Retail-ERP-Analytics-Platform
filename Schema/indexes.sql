CREATE INDEX idx_fifo 
ON inventory_cost_layers (product_id, warehouse_id, received_date);

CREATE INDEX idx_transactions 
ON inventory_transactions (product_id, warehouse_id, transaction_date);
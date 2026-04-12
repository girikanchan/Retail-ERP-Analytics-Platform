DELIMITER $$

CREATE PROCEDURE receive_stock (
    IN p_product_id INT,
    IN p_warehouse_id INT,
    IN p_qty DECIMAL(12,3),
    IN p_unit_cost DECIMAL(12,2),
    IN p_reference_id INT
)
BEGIN
    START TRANSACTION;

    -- Create FIFO layer
    INSERT INTO inventory_cost_layers (
        product_id,
        warehouse_id,
        quantity_received,
        quantity_remaining,
        unit_cost,
        received_date
    )
    VALUES (
        p_product_id,
        p_warehouse_id,
        p_qty,
        p_qty,
        p_unit_cost,
        CURDATE()
    );

    -- Insert inventory transaction
    INSERT INTO inventory_transactions (
        product_id,
        warehouse_id,
        transaction_type,
        reference_type,
        reference_id,
        quantity,
        unit_cost
    )
    VALUES (
        p_product_id,
        p_warehouse_id,
        'IN',
        'PURCHASE',
        p_reference_id,
        p_qty,
        p_unit_cost
    );

    COMMIT;

END$$

DELIMITER ;
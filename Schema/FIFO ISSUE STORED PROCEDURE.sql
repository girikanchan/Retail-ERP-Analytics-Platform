-- ============================================================
-- FILE: 13_FIFO_ISSUE_STORED_PROCEDURE.sql

-- ============================================================

DELIMITER $$

DROP PROCEDURE IF EXISTS fifo_issue_stock $$

CREATE PROCEDURE fifo_issue_stock (
    IN p_product_id INT,
    IN p_warehouse_id INT,
    IN p_issue_qty DECIMAL(12,3),
    IN p_reference_id INT   -- sale_id / transaction reference
)
BEGIN
    DECLARE v_done INT DEFAULT 0;
    DECLARE v_layer_id INT;
    DECLARE v_layer_qty DECIMAL(12,3);
    DECLARE v_unit_cost DECIMAL(12,2);
    DECLARE v_remaining DECIMAL(12,3);

    DECLARE v_total_available DECIMAL(12,3);

    DECLARE cur CURSOR FOR
        SELECT layer_id, quantity_remaining, unit_cost
        FROM inventory_cost_layers
        WHERE product_id = p_product_id
          AND warehouse_id = p_warehouse_id
          AND quantity_remaining > 0
        ORDER BY received_date ASC
        FOR UPDATE;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done = 1;

    -- Start transaction (ACID)
    START TRANSACTION;

    SET v_remaining = p_issue_qty;

    -- Check stock availability
    SELECT COALESCE(SUM(quantity_remaining),0)
    INTO v_total_available
    FROM inventory_cost_layers
    WHERE product_id = p_product_id
      AND warehouse_id = p_warehouse_id
    FOR UPDATE;

    IF v_total_available < p_issue_qty THEN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Insufficient stock';
    END IF;

    OPEN cur;

    read_loop: LOOP

        FETCH cur INTO v_layer_id, v_layer_qty, v_unit_cost;

        IF v_done = 1 OR v_remaining = 0 THEN
            LEAVE read_loop;
        END IF;

        IF v_layer_qty <= v_remaining THEN

            -- FULL LAYER CONSUME
            UPDATE inventory_cost_layers
            SET quantity_remaining = 0
            WHERE layer_id = v_layer_id;

            -- Insert transaction
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
                'OUT',
                'SALE',
                p_reference_id,
                -v_layer_qty,
                v_unit_cost
            );

            SET v_remaining = v_remaining - v_layer_qty;

        ELSE

            -- PARTIAL CONSUME
            UPDATE inventory_cost_layers
            SET quantity_remaining = quantity_remaining - v_remaining
            WHERE layer_id = v_layer_id;

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
                'OUT',
                'SALE',
                p_reference_id,
                -v_remaining,
                v_unit_cost
            );

            SET v_remaining = 0;

        END IF;

    END LOOP;

    CLOSE cur;

    COMMIT;

END$$

DELIMITER ;
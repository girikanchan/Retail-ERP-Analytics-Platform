-- ============================================================
-- FILE: 13_FIFO_ISSUE_STORED_PROCEDURE.sql

-- ============================================================

DELIMITER $$

CREATE PROCEDURE fifo_issue_stock (
    IN  p_product_id   INT,
    IN  p_warehouse_id INT,
    IN  p_issue_qty    DECIMAL(12,3)   -- FIX: match column type (DECIMAL not INT)
)
BEGIN
    DECLARE v_done      INT           DEFAULT 0;
    DECLARE v_layer_id  INT;           -- FIX: renamed from layer_id to avoid collision
    DECLARE v_layer_qty DECIMAL(12,3); -- FIX: renamed from layer_qty
    DECLARE v_remaining DECIMAL(12,3) DEFAULT p_issue_qty;

    -- Cursor walks layers oldest-first (FIFO order)
    DECLARE cur CURSOR FOR
        SELECT layer_id, quantity_remaining
        FROM   inventory_cost_layers
        WHERE  product_id   = p_product_id
          AND  warehouse_id = p_warehouse_id
          AND  quantity_remaining > 0
        ORDER BY received_date ASC;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done = 1;

    -- Guard: refuse if insufficient stock
    IF (SELECT COALESCE(SUM(quantity_remaining), 0)
        FROM   inventory_cost_layers
        WHERE  product_id   = p_product_id
          AND  warehouse_id = p_warehouse_id) < p_issue_qty THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Insufficient stock to fulfil issue quantity';
    END IF;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO v_layer_id, v_layer_qty;

        IF v_done = 1 OR v_remaining = 0 THEN
            LEAVE read_loop;
        END IF;

        IF v_layer_qty <= v_remaining THEN
            -- Exhaust this layer completely
            UPDATE inventory_cost_layers
            SET    quantity_remaining = 0
            WHERE  layer_id = v_layer_id;   -- FIX: now uses variable v_layer_id, not column name

            SET v_remaining = v_remaining - v_layer_qty;
        ELSE
            -- Partially consume this layer
            UPDATE inventory_cost_layers
            SET    quantity_remaining = quantity_remaining - v_remaining
            WHERE  layer_id = v_layer_id;   -- FIX: same

            SET v_remaining = 0;
        END IF;
    END LOOP;

    CLOSE cur;
END$$

DELIMITER ;
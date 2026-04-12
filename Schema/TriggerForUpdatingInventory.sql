DELIMITER $$

DROP TRIGGER IF EXISTS trg_inventory_update $$

CREATE TRIGGER trg_inventory_update
AFTER INSERT ON inventory_transactions
FOR EACH ROW
BEGIN
    DECLARE v_current_stock DECIMAL(12,3);

    -- Lock row to prevent race condition
    SELECT quantity_on_hand INTO v_current_stock
    FROM inventory_stock
    WHERE product_id = NEW.product_id
      AND warehouse_id = NEW.warehouse_id
    FOR UPDATE;

    -- If row does not exist → insert
    IF v_current_stock IS NULL THEN

        IF NEW.quantity < 0 THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Stock cannot go negative (no existing stock)';
        END IF;

        INSERT INTO inventory_stock (
            product_id,
            warehouse_id,
            quantity_on_hand
        )
        VALUES (
            NEW.product_id,
            NEW.warehouse_id,
            NEW.quantity
        );

    ELSE
        -- Prevent negative stock
        IF v_current_stock + NEW.quantity < 0 THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Stock cannot go negative';
        END IF;

        UPDATE inventory_stock
        SET quantity_on_hand = v_current_stock + NEW.quantity
        WHERE product_id = NEW.product_id
          AND warehouse_id = NEW.warehouse_id;

    END IF;

END$$

DELIMITER ;
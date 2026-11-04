
USE inventory_db;

CREATE OR REPLACE VIEW vw_stock_status AS
SELECT p.product_id, p.sku, p.product_name, p.category,
       w.warehouse_id, w.warehouse_name,
       sl.quantity_on_hand, p.reorder_level, p.max_stock_level, p.reorder_quantity,
       CASE WHEN sl.quantity_on_hand < p.reorder_level   THEN 'LOW_STOCK'
            WHEN sl.quantity_on_hand > p.max_stock_level THEN 'OVERSTOCK'
            ELSE 'OK' END AS stock_status
FROM stock_levels sl
JOIN products   p ON p.product_id   = sl.product_id
JOIN warehouses w ON w.warehouse_id = sl.warehouse_id
WHERE p.is_active = 1;

DROP PROCEDURE IF EXISTS sp_products_below_reorder;
DROP PROCEDURE IF EXISTS sp_overstocked_products;
DROP PROCEDURE IF EXISTS sp_record_stock_movement;

DELIMITER $$


CREATE PROCEDURE sp_products_below_reorder(IN p_warehouse_id INT)
BEGIN
    SELECT p.product_id, p.sku, p.product_name,
           w.warehouse_id, w.warehouse_name,
           sl.quantity_on_hand,
           p.reorder_level,
           (p.reorder_level - sl.quantity_on_hand) AS shortage_qty,
           p.reorder_quantity                      AS suggested_order_qty,
           s.supplier_name, s.email AS supplier_email
    FROM stock_levels sl
    JOIN products   p ON p.product_id   = sl.product_id
    JOIN warehouses w ON w.warehouse_id = sl.warehouse_id
    JOIN suppliers  s ON s.supplier_id  = p.supplier_id
    WHERE p.is_active = 1
      AND sl.quantity_on_hand < p.reorder_level
      AND (p_warehouse_id IS NULL OR sl.warehouse_id = p_warehouse_id)
    ORDER BY shortage_qty DESC, p.product_id;
END$$


CREATE PROCEDURE sp_overstocked_products(IN p_warehouse_id INT)
BEGIN
    SELECT p.product_id, p.sku, p.product_name, w.warehouse_name,
           sl.quantity_on_hand, p.max_stock_level,
           (sl.quantity_on_hand - p.max_stock_level) AS excess_qty,
           ROUND((sl.quantity_on_hand - p.max_stock_level) * p.unit_price, 2) AS excess_value
    FROM stock_levels sl
    JOIN products   p ON p.product_id   = sl.product_id
    JOIN warehouses w ON w.warehouse_id = sl.warehouse_id
    WHERE p.is_active = 1
      AND sl.quantity_on_hand > p.max_stock_level
      AND (p_warehouse_id IS NULL OR sl.warehouse_id = p_warehouse_id)
    ORDER BY excess_value DESC;
END$$


CREATE PROCEDURE sp_record_stock_movement(
    IN p_product_id    INT,
    IN p_warehouse_id  INT,
    IN p_movement_type VARCHAR(10),
    IN p_quantity      INT,
    IN p_reason        VARCHAR(255))
BEGIN
    DECLARE v_signed_qty INT;
    DECLARE v_current    INT DEFAULT 0;

    IF p_movement_type NOT IN ('IN', 'OUT', 'ADJUSTMENT') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'movement_type must be IN, OUT or ADJUSTMENT';
    END IF;
    IF p_quantity = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'quantity cannot be zero';
    END IF;

    SET v_signed_qty = CASE p_movement_type WHEN 'IN'  THEN  ABS(p_quantity)
                                            WHEN 'OUT' THEN -ABS(p_quantity)
                                            ELSE p_quantity END;

    SELECT COALESCE(SUM(quantity_on_hand), 0) INTO v_current
    FROM stock_levels WHERE product_id = p_product_id AND warehouse_id = p_warehouse_id;

    IF v_current + v_signed_qty < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insufficient stock: movement would make stock negative';
    END IF;

    INSERT INTO stock_movements (product_id, warehouse_id, movement_type, quantity,
                                 movement_date, reference_no, reason)
    VALUES (p_product_id, p_warehouse_id, p_movement_type, v_signed_qty, CURRENT_DATE,
            CONCAT('MAN-', DATE_FORMAT(NOW(), '%Y%m%d%H%i%s')), p_reason);

    SELECT p_product_id AS product_id, p_warehouse_id AS warehouse_id,
           v_current AS old_quantity, v_current + v_signed_qty AS new_quantity;
END$$

DELIMITER ;


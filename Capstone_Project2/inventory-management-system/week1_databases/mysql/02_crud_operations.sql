
USE inventory_db;

DELETE FROM stock_levels    WHERE product_id = 900;
DELETE FROM stock_movements WHERE product_id = 900;
DELETE FROM products        WHERE product_id = 900;
DELETE FROM suppliers       WHERE supplier_id = 900;


INSERT INTO suppliers (supplier_id, supplier_name, contact_person, email, phone, city)
VALUES (900, 'Test Supplier Pvt Ltd', 'Asha Menon', 'asha@test-supplier.example', '+91-44-5550-0900', 'Chennai');

INSERT INTO products (product_id, sku, product_name, category, unit_price, supplier_id,
                      reorder_level, max_stock_level, reorder_quantity)
VALUES (900, 'TST-0900', 'Test Product - Wireless Keyboard', 'Electronics', 1499.00, 900, 30, 180, 100);

-- Receiving stock = insert a movement. The trigger creates/updates stock_levels automatically.
INSERT INTO stock_movements (product_id, warehouse_id, movement_type, quantity, movement_date, reference_no, reason)
VALUES (900, 1, 'IN', 50, CURRENT_DATE, 'PO-TEST-001', 'Initial purchase order receipt');

SELECT w.warehouse_name, sl.quantity_on_hand, sl.last_updated
FROM stock_levels sl JOIN warehouses w ON w.warehouse_id = sl.warehouse_id
WHERE sl.product_id = 900;

SELECT w.warehouse_name, SUM(sl.quantity_on_hand) AS total_units,
       ROUND(SUM(sl.quantity_on_hand * p.unit_price), 2) AS stock_value
FROM stock_levels sl
JOIN warehouses w ON w.warehouse_id = sl.warehouse_id
JOIN products   p ON p.product_id   = sl.product_id
GROUP BY w.warehouse_name ORDER BY total_units DESC;

SELECT movement_id, movement_date, movement_type, quantity, reference_no, reason
FROM stock_movements WHERE product_id = 900 ORDER BY movement_id;


SELECT sl.product_id, sl.warehouse_id, sl.quantity_on_hand, m.calc_qty
FROM stock_levels sl
JOIN (SELECT product_id, warehouse_id, SUM(quantity) AS calc_qty
      FROM stock_movements GROUP BY product_id, warehouse_id) m
  ON m.product_id = sl.product_id AND m.warehouse_id = sl.warehouse_id
WHERE sl.quantity_on_hand <> m.calc_qty;


UPDATE products SET reorder_level = 40, unit_price = 1599.00 WHERE product_id = 900;

INSERT INTO stock_movements (product_id, warehouse_id, movement_type, quantity, movement_date, reference_no, reason)
VALUES (900, 1, 'OUT', -12, CURRENT_DATE, 'SO-TEST-001', 'Customer order');


INSERT INTO stock_movements (product_id, warehouse_id, movement_type, quantity, movement_date, reference_no, reason)
VALUES (900, 1, 'ADJUSTMENT', -3, CURRENT_DATE, 'ADJ-TEST-001', 'Damaged goods found during cycle count');


UPDATE stock_levels SET quantity_on_hand = 35 WHERE product_id = 900 AND warehouse_id = 1;

SELECT * FROM stock_levels WHERE product_id = 900;       


UPDATE products SET is_active = 0 WHERE product_id = 900;


DELETE FROM stock_levels    WHERE product_id = 900;
DELETE FROM stock_movements WHERE product_id = 900;
DELETE FROM products        WHERE product_id = 900;
DELETE FROM suppliers       WHERE supplier_id = 900;

SELECT COUNT(*) AS test_rows_left FROM products WHERE product_id = 900;   -- expect 0

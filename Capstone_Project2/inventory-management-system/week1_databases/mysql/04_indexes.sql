
USE inventory_db;


CREATE INDEX idx_mov_product_wh_date ON stock_movements (product_id, warehouse_id, movement_date);

CREATE INDEX idx_mov_warehouse_date  ON stock_movements (warehouse_id, movement_date);

CREATE INDEX idx_sl_warehouse        ON stock_levels (warehouse_id, quantity_on_hand);


CREATE INDEX idx_products_name       ON products (product_name);
CREATE INDEX idx_products_category   ON products (category, is_active);

SHOW INDEX FROM stock_movements;
SHOW INDEX FROM stock_levels;

EXPLAIN SELECT * FROM stock_movements WHERE product_id = 5;
EXPLAIN SELECT * FROM stock_movements WHERE warehouse_id = 2 AND movement_date >= '2026-06-01';
EXPLAIN SELECT * FROM stock_levels    WHERE warehouse_id = 3 AND quantity_on_hand < 20;
